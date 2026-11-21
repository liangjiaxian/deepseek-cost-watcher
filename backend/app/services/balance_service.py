import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, date
from typing import List, Optional
import httpx

from app.models.balance_snapshot import BalanceSnapshot
from app.models.api_key import ApiKey
from app.schemas.usage import BalanceTrend, BalanceTrendPoint, BalanceLatest, DailyBalanceSummary
from app.core.config import settings
from app.core.security import decrypt_api_key
from app.core.timeutil import beijing_range_utc_naive
from app.models.system_config import SystemConfig

logger = logging.getLogger(__name__)

DEEPSEEK_BALANCE_URL = f"{settings.deepseek_base_url}/user/balance"


class BalanceService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def take_snapshot(self, api_key_id: Optional[int] = None) -> Optional[BalanceSnapshot]:
        key_obj = await self._get_active_key(api_key_id)
        if not key_obj:
            return None

        try:
            raw_key = decrypt_api_key(key_obj.key_encrypted)
        except Exception as e:
            raise RuntimeError(f"Failed to decrypt API key: {type(e).__name__}")

        ok, payload, err = await self._fetch_balance(raw_key)
        if not ok:
            raise RuntimeError(f"DeepSeek API error: {err}")
        if payload is None:
            raise RuntimeError("DeepSeek returned null balance (no data available yet)")

        snapshot = BalanceSnapshot(
            api_key_id=key_obj.id,
            balance=payload["balance"],
            total_usage=None,
            currency=payload["currency"],
            granted_balance=payload["granted_balance"],
            topped_up_balance=payload["topped_up_balance"],
            is_available=1 if payload["is_available"] else 0,
        )
        self.db.add(snapshot)
        return snapshot

    async def get_latest(self) -> Optional[BalanceLatest]:
        stmt = select(BalanceSnapshot).order_by(BalanceSnapshot.recorded_at.desc()).limit(1)
        row = (await self.db.execute(stmt)).scalar_one_or_none()
        if not row:
            return None
        return BalanceLatest(
            balance=row.balance,
            granted_balance=row.granted_balance,
            topped_up_balance=row.topped_up_balance,
            currency=row.currency or "CNY",
            is_available=None if row.is_available is None else bool(row.is_available),
            recorded_at=self._point_time(row.recorded_at),
        )

    @staticmethod
    def _point_time(recorded_at) -> str:
        return (recorded_at.isoformat() if hasattr(recorded_at, "isoformat") else str(recorded_at)) + "Z"

    async def get_balance_trend(self, range_hours: int = 168) -> BalanceTrend:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=range_hours)

        stmt = select(BalanceSnapshot).where(
            BalanceSnapshot.recorded_at >= start_time,
            BalanceSnapshot.recorded_at < end_time,
        ).order_by(BalanceSnapshot.recorded_at.asc())

        rows = (await self.db.execute(stmt)).scalars().all()

        points = [
            BalanceTrendPoint(
                time=self._point_time(r.recorded_at),
                balance=r.balance,
                total_usage=r.total_usage,
                granted_balance=r.granted_balance,
                topped_up_balance=r.topped_up_balance,
            )
            for r in rows
        ]
        return BalanceTrend(points=points)

    async def get_daily_balance(self, target_date: date) -> DailyBalanceSummary:
        day_start, day_end = beijing_range_utc_naive(target_date, target_date + timedelta(days=1))

        stmt = select(BalanceSnapshot).where(
            BalanceSnapshot.recorded_at >= day_start,
            BalanceSnapshot.recorded_at < day_end,
        ).order_by(BalanceSnapshot.recorded_at.asc())

        rows = (await self.db.execute(stmt)).scalars().all()

        points = [
            BalanceTrendPoint(
                time=self._point_time(r.recorded_at),
                balance=r.balance,
                total_usage=r.total_usage,
                granted_balance=r.granted_balance,
                topped_up_balance=r.topped_up_balance,
            )
            for r in rows
        ]

        balance_start = rows[0].balance if rows else None
        balance_end = rows[-1].balance if rows else None
        balance_change = round(balance_end - balance_start, 2) if balance_start is not None and balance_end is not None else None

        return DailyBalanceSummary(
            date=target_date.isoformat(),
            balance_start=balance_start,
            balance_end=balance_end,
            balance_change=balance_change,
            points=points,
        )

    async def _get_active_key(self, api_key_id: Optional[int] = None) -> Optional[ApiKey]:
        if api_key_id:
            stmt = select(ApiKey).where(ApiKey.id == api_key_id, ApiKey.is_active == 1)
        else:
            stmt = select(ApiKey).where(ApiKey.is_active == 1).order_by(ApiKey.id.asc()).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _fetch_balance(self, api_key: str) -> tuple:
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(DEEPSEEK_BALANCE_URL, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    infos = data.get("balance_infos") or []
                    if not infos:
                        return False, None, "DeepSeek returned no balance_infos"
                    # Prefer CNY; fall back to whatever single currency is present.
                    primary = next((i for i in infos if i.get("currency") == "CNY"), infos[0])
                    if primary.get("total_balance") is None:
                        return False, None, "DeepSeek returned null total_balance"
                    payload = {
                        "currency": primary.get("currency") or "CNY",
                        "balance": float(primary["total_balance"]),
                        "granted_balance": float(primary.get("granted_balance") or 0),
                        "topped_up_balance": float(primary.get("topped_up_balance") or 0),
                        "is_available": bool(data.get("is_available", True)),
                    }
                    return True, payload, None
                return False, None, f"HTTP {resp.status_code}"
        except httpx.ConnectError:
            return False, None, "Cannot connect to DeepSeek API"
        except Exception as e:
            return False, None, str(e)


async def _save_run_log(db: AsyncSession, status: str, message: str):
    now = datetime.utcnow().isoformat()
    for key in ("scheduler_last_run", "scheduler_last_status", "scheduler_last_message"):
        stmt = select(SystemConfig).where(SystemConfig.config_key == key)
        row = (await db.execute(stmt)).scalar_one_or_none()
        val = now if key == "scheduler_last_run" else (status if key == "scheduler_last_status" else message)
        if row:
            row.config_value = val
        else:
            db.add(SystemConfig(config_key=key, config_value=val))


async def poll_balance():
    from app.core.database import async_session_factory
    from app.models.scheduler_log import SchedulerLog

    try:
        async with async_session_factory() as db:
            started_at = datetime.utcnow()
            log = SchedulerLog(task_name="poll_balance", started_at=started_at, status="running")
            db.add(log)
            await db.flush()

            try:
                service = BalanceService(db)
                snapshot = await service.take_snapshot()
                finished_at = datetime.utcnow()
                log.finished_at = finished_at
                if snapshot:
                    log.status = "success"
                    split = f", Grant={snapshot.granted_balance}, TopUp={snapshot.topped_up_balance}"
                    log.message = f"Balance={snapshot.balance}{split}, Available={bool(snapshot.is_available)}"
                    logger.info(
                        "Balance snapshot taken: balance=%s grant=%s top_up=%s available=%s",
                        snapshot.balance, snapshot.granted_balance, snapshot.topped_up_balance,
                        bool(snapshot.is_available),
                    )
                else:
                    log.status = "skipped"
                    log.message = "No active API key in database"
                    logger.warning("Balance snapshot skipped: no active API key")
            except RuntimeError as e:
                log.status = "error"
                log.message = str(e)
                log.finished_at = datetime.utcnow()
                logger.error("Balance API error: %s", e)
            except Exception as e:
                emsg = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
                log.status = "error"
                log.message = emsg
                log.finished_at = datetime.utcnow()
                logger.error("Balance snapshot error [%s]: %s", type(e).__name__, e)

            await _save_run_log(db, log.status, log.message)
            await db.commit()
    except Exception as e:
        logger.error("poll_balance failed before log creation: %s", e)
