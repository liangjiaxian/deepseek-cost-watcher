import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, date
from typing import Optional
import httpx

from app.models.usage_cost_record import UsageCostRecord
from app.models.api_key import ApiKey
from app.models.system_config import SystemConfig
from app.core.security import decrypt_api_key, encrypt_api_key
from app.schemas.usage import MonthlyCostSummary, DailyCost, DailyModelCost, ModelCostItem, WeeklyCostSummary, WeeklyCostDay, WeeklyCostModel

logger = logging.getLogger(__name__)

PLATFORM_BASE_URL = "https://platform.deepseek.com"


class CostService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch_and_store_monthly_cost(self, year: int, month: int) -> MonthlyCostSummary:
        token = await self._get_platform_token()
        if token:
            try:
                data = await self._fetch_cost(token, year, month)
            except RuntimeError as e:
                if "Authorization Failed" in str(e):
                    logger.warning("Platform token expired, falling back to API key")
                    data = await self._fetch_cost(await self._get_api_key(), year, month)
                else:
                    raise
        else:
            data = await self._fetch_cost(await self._get_api_key(), year, month)

        for day in data.get("days", []):
            for model_entry in day.get("data", []):
                model_name = model_entry["model"]
                usage_map = {}
                for u in model_entry.get("usage", []):
                    usage_map[u["type"]] = float(u["amount"])

                total = sum(usage_map.values())

                stmt = select(UsageCostRecord).where(and_(
                    UsageCostRecord.date == day["date"],
                    UsageCostRecord.model == model_name,
                ))
                existing = (await self.db.execute(stmt)).scalar_one_or_none()

                if existing:
                    existing.prompt_token_cost = usage_map.get("PROMPT_TOKEN", 0)
                    existing.cache_hit_token_cost = usage_map.get("PROMPT_CACHE_HIT_TOKEN", 0)
                    existing.cache_miss_token_cost = usage_map.get("PROMPT_CACHE_MISS_TOKEN", 0)
                    existing.response_token_cost = usage_map.get("RESPONSE_TOKEN", 0)
                    existing.request_cost = usage_map.get("REQUEST", 0)
                    existing.total_cost = total
                    existing.currency = data.get("currency", "CNY")
                else:
                    record = UsageCostRecord(
                        date=day["date"],
                        model=model_name,
                        prompt_token_cost=usage_map.get("PROMPT_TOKEN", 0),
                        cache_hit_token_cost=usage_map.get("PROMPT_CACHE_HIT_TOKEN", 0),
                        cache_miss_token_cost=usage_map.get("PROMPT_CACHE_MISS_TOKEN", 0),
                        response_token_cost=usage_map.get("RESPONSE_TOKEN", 0),
                        request_cost=usage_map.get("REQUEST", 0),
                        total_cost=total,
                        currency=data.get("currency", "CNY"),
                    )
                    self.db.add(record)

        await self.db.commit()

        return self._build_summary(data, year, month)

    async def get_monthly_cost(self, year: int, month: int) -> MonthlyCostSummary:
        month_str = f"{year:04d}-{month:02d}"
        stmt = select(UsageCostRecord).where(
            UsageCostRecord.date.like(f"{month_str}%")
        ).order_by(UsageCostRecord.date)

        rows = (await self.db.execute(stmt)).scalars().all()

        if not rows:
            return MonthlyCostSummary(
                year=year, month=month,
                total=[], days=[], currency="CNY",
            )

        day_map = {}
        for r in rows:
            if r.date not in day_map:
                day_map[r.date] = []
            day_map[r.date].append(r)

        days_data = []
        for d in sorted(day_map.keys()):
            models = []
            for r in day_map[d]:
                items = [
                    ModelCostItem(type="PROMPT_TOKEN", amount=r.prompt_token_cost),
                    ModelCostItem(type="PROMPT_CACHE_HIT_TOKEN", amount=r.cache_hit_token_cost),
                    ModelCostItem(type="PROMPT_CACHE_MISS_TOKEN", amount=r.cache_miss_token_cost),
                    ModelCostItem(type="RESPONSE_TOKEN", amount=r.response_token_cost),
                    ModelCostItem(type="REQUEST", amount=r.request_cost),
                ]
                models.append(DailyModelCost(model=r.model, usage=items))
            days_data.append(DailyCost(date=d, data=models))

        totals_by_model = {}
        for r in rows:
            if r.model not in totals_by_model:
                totals_by_model[r.model] = {
                    "prompt_token_cost": 0,
                    "cache_hit_token_cost": 0,
                    "cache_miss_token_cost": 0,
                    "response_token_cost": 0,
                    "request_cost": 0,
                }
            totals_by_model[r.model]["prompt_token_cost"] += r.prompt_token_cost
            totals_by_model[r.model]["cache_hit_token_cost"] += r.cache_hit_token_cost
            totals_by_model[r.model]["cache_miss_token_cost"] += r.cache_miss_token_cost
            totals_by_model[r.model]["response_token_cost"] += r.response_token_cost
            totals_by_model[r.model]["request_cost"] += r.request_cost

        total_list = []
        for model, costs in totals_by_model.items():
            items = [
                ModelCostItem(type="PROMPT_TOKEN", amount=costs["prompt_token_cost"]),
                ModelCostItem(type="PROMPT_CACHE_HIT_TOKEN", amount=costs["cache_hit_token_cost"]),
                ModelCostItem(type="PROMPT_CACHE_MISS_TOKEN", amount=costs["cache_miss_token_cost"]),
                ModelCostItem(type="RESPONSE_TOKEN", amount=costs["response_token_cost"]),
                ModelCostItem(type="REQUEST", amount=costs["request_cost"]),
            ]
            total_list.append(DailyModelCost(model=model, usage=items))

        currency = rows[0].currency if rows else "CNY"

        return MonthlyCostSummary(
            year=year,
            month=month,
            total=total_list,
            days=days_data,
            currency=currency,
        )

    async def get_weekly_cost(self, year: int, week: int) -> WeeklyCostSummary:
        from datetime import timedelta, date as date_type
        week_start = date_type.fromisocalendar(year, week, 1)
        week_end = week_start + timedelta(days=7)
        week_dates = [(week_start + timedelta(days=i)).isoformat() for i in range(7)]

        stmt = select(UsageCostRecord).where(
            UsageCostRecord.date >= week_start.isoformat(),
            UsageCostRecord.date < week_end.isoformat(),
        ).order_by(UsageCostRecord.date)
        rows = (await self.db.execute(stmt)).scalars().all()

        if not rows:
            return WeeklyCostSummary(
                year=year, week=week, total_cost=0, daily_avg_cost=0,
                daily_breakdown=[], model_breakdown=[], active_models=0,
            )

        day_map = {}
        model_map = {}
        all_total = 0
        model_set = set()
        for r in rows:
            all_total += r.total_cost
            model_set.add(r.model)
            if r.date not in day_map:
                day_map[r.date] = 0
            day_map[r.date] += r.total_cost
            if r.model not in model_map:
                model_map[r.model] = 0
            model_map[r.model] += r.total_cost

        daily_breakdown = [
            WeeklyCostDay(date=d, total_cost=day_map.get(d, 0))
            for d in week_dates
        ]
        model_breakdown = [
            WeeklyCostModel(model=m, cost=c)
            for m, c in sorted(model_map.items(), key=lambda x: x[1], reverse=True)
        ]

        from app.models.balance_snapshot import BalanceSnapshot

        start_stmt = select(BalanceSnapshot.balance).where(
            BalanceSnapshot.recorded_at >= datetime.combine(week_start, datetime.min.time())
        ).order_by(BalanceSnapshot.recorded_at.asc()).limit(1)
        start_row = (await self.db.execute(start_stmt)).scalar_one_or_none()

        end_stmt = select(BalanceSnapshot.balance).where(
            BalanceSnapshot.recorded_at < datetime.combine(week_end, datetime.min.time())
        ).order_by(BalanceSnapshot.recorded_at.desc()).limit(1)
        end_row = (await self.db.execute(end_stmt)).scalar_one_or_none()

        bal_start = start_row
        bal_end = end_row
        bal_change = (bal_end - bal_start) if (bal_start is not None and bal_end is not None) else None
        if bal_change is not None:
            bal_change = round(bal_change, 4)

        return WeeklyCostSummary(
            year=year, week=week,
            total_cost=round(all_total, 4),
            daily_avg_cost=round(all_total / 7, 4),
            daily_breakdown=daily_breakdown,
            model_breakdown=model_breakdown,
            balance_start=bal_start,
            balance_end=bal_end,
            balance_change=bal_change,
            active_models=len(model_set),
        )

    async def _get_platform_token(self) -> Optional[str]:
        stmt = select(SystemConfig).where(SystemConfig.config_key == "platform_token")
        result = (await self.db.execute(stmt)).scalar_one_or_none()
        if not result or not result.config_value:
            return None
        try:
            return decrypt_api_key(result.config_value)
        except Exception:
            return None

    async def _get_api_key(self) -> str:
        key_obj = await self._get_active_key()
        if not key_obj:
            raise RuntimeError("No active API key in database")
        try:
            return decrypt_api_key(key_obj.key_encrypted)
        except Exception as e:
            raise RuntimeError(f"Failed to decrypt API key: {type(e).__name__}")

    async def _get_active_key(self) -> Optional[ApiKey]:
        stmt = select(ApiKey).where(ApiKey.is_active == 1).order_by(ApiKey.id.asc()).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _fetch_cost(self, api_key: str, year: int, month: int) -> dict:
        url = f"{PLATFORM_BASE_URL}/api/v0/usage/cost?month={month}&year={year}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "x-app-version": "1.0.0",
            "Referer": "https://platform.deepseek.com/usage",
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    raise RuntimeError(f"DeepSeek usage API error: HTTP {resp.status_code}")
                body = resp.json()
                if body.get("code") != 0:
                    raise RuntimeError(f"DeepSeek usage API error: code={body.get('code')} msg={body.get('msg')}")
                biz_data = body.get("data", {}).get("biz_data", [])
                if not biz_data:
                    raise RuntimeError("DeepSeek usage API returned empty biz_data")
                return biz_data[0]
        except httpx.ConnectError:
            raise RuntimeError("Cannot connect to platform.deepseek.com")
        except httpx.TimeoutException:
            raise RuntimeError("DeepSeek usage API timeout")
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"DeepSeek usage API error: {type(e).__name__}: {e}")

    def _build_summary(self, data: dict, year: int, month: int) -> MonthlyCostSummary:
        total_list = []
        for t in data.get("total", []):
            items = [ModelCostItem(type=u["type"], amount=float(u["amount"])) for u in t.get("usage", [])]
            total_list.append(DailyModelCost(model=t["model"], usage=items))

        days_list = []
        for d in data.get("days", []):
            models = []
            for m in d.get("data", []):
                items = [ModelCostItem(type=u["type"], amount=float(u["amount"])) for u in m.get("usage", [])]
                models.append(DailyModelCost(model=m["model"], usage=items))
            days_list.append(DailyCost(date=d["date"], data=models))

        return MonthlyCostSummary(
            year=year,
            month=month,
            total=total_list,
            days=days_list,
            currency=data.get("currency", "CNY"),
        )


    @staticmethod
    async def test_platform_token(token: str) -> tuple[bool, str]:
        today = date.today()
        url = f"{PLATFORM_BASE_URL}/api/v0/usage/cost?month={today.month}&year={today.year}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "x-app-version": "1.0.0",
            "Referer": "https://platform.deepseek.com/usage",
        }
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    body = resp.json()
                    if body.get("code") == 0:
                        return True, "Token is valid"
                    return False, f"API error: {body.get('msg', 'unknown')}"
                return False, f"HTTP {resp.status_code}"
        except httpx.ConnectError:
            return False, "Cannot connect to platform.deepseek.com"
        except httpx.TimeoutException:
            return False, "Connection timeout"
        except Exception as e:
            return False, str(e)


async def poll_usage_cost():
    from app.core.database import async_session_factory
    from app.models.scheduler_log import SchedulerLog

    try:
        async with async_session_factory() as db:
            started_at = datetime.utcnow()
            log = SchedulerLog(task_name="poll_usage_cost", started_at=started_at, status="running")
            db.add(log)
            await db.flush()

            try:
                today = date.today()
                service = CostService(db)
                summary = await service.fetch_and_store_monthly_cost(today.year, today.month)
                finished_at = datetime.utcnow()
                log.finished_at = finished_at
                log.status = "success"
                log.message = f"Fetched {len(summary.days)} days, {len(summary.total)} models"
                logger.info("Usage cost polled: %d days, %d models", len(summary.days), len(summary.total))
            except RuntimeError as e:
                log.status = "error"
                log.message = str(e)
                log.finished_at = datetime.utcnow()
                logger.error("Usage cost error: %s", e)
            except Exception as e:
                emsg = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
                log.status = "error"
                log.message = emsg
                log.finished_at = datetime.utcnow()
                logger.error("Usage cost error [%s]: %s", type(e).__name__, e)

            await db.commit()
    except Exception as e:
        logger.error("poll_usage_cost failed before log creation: %s", e)
