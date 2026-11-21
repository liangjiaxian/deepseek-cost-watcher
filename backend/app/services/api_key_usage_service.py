from datetime import date, datetime, time, timedelta, timezone
import logging
import httpx
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.api_key_usage_record import ApiKeyUsageRecord
from app.models.api_key_cost_record import ApiKeyCostRecord
from app.schemas.usage import KeyUsageRanking, KeyUsageRankingSet, KeyUsageRankings
from app.services.cost_service import PLATFORM_BASE_URL, CostService

logger = logging.getLogger(__name__)

# The platform only serves a short range per request (its own UI asks for 30
# days), so history is backfilled in UTC day-aligned 30-day requests.
HISTORY_CHUNK_DAYS = 30
HISTORY_DAYS = 365


class ApiKeyUsageService:
    def __init__(self, db: AsyncSession): self.db = db

    async def sync(self, start: datetime, end: datetime) -> int:
        payload = await self._fetch(await self._get_token(), start, end, "amount"); count = 0
        for series in payload.get("series", []):
            key = series.get("api_key", {}); tracking_id = key.get("tracking_id")
            if not tracking_id: continue
            for bucket in series.get("buckets", []):
                if bucket.get("time") is None: continue
                usage = bucket.get("usage", {}); bucket_time = datetime.fromtimestamp(bucket["time"], tz=timezone.utc).replace(tzinfo=None)
                stmt = select(ApiKeyUsageRecord).where(ApiKeyUsageRecord.tracking_id == tracking_id, ApiKeyUsageRecord.model == series.get("model", "unknown"), ApiKeyUsageRecord.bucket_time == bucket_time)
                row = (await self.db.execute(stmt)).scalar_one_or_none()
                values = {"key_name": key.get("name") or "Unnamed key", "sensitive_id": key.get("sensitive_id") or "", "response_tokens": int(usage.get("RESPONSE_TOKEN", 0)), "request_count": int(usage.get("REQUEST", 0)), "prompt_cache_hit_tokens": int(usage.get("PROMPT_CACHE_HIT_TOKEN", 0)), "prompt_cache_miss_tokens": int(usage.get("PROMPT_CACHE_MISS_TOKEN", 0))}
                if row:
                    for field, value in values.items(): setattr(row, field, value)
                else: self.db.add(ApiKeyUsageRecord(tracking_id=tracking_id, model=series.get("model", "unknown"), bucket_time=bucket_time, **values))
                count += 1
        await self.db.commit(); return count

    async def sync_cost(self, start: datetime, end: datetime) -> int:
        """Fetch per-key costs from by_api_key/cost.

        The payload wraps series per currency: biz_data.data[] = {currency, series}.
        """
        payload = await self._fetch(await self._get_token(), start, end, "cost"); count = 0
        for entry in payload.get("data", []):
            currency = entry.get("currency") or "CNY"
            for series in entry.get("series", []):
                key = series.get("api_key", {}); tracking_id = key.get("tracking_id")
                if not tracking_id: continue
                for bucket in series.get("buckets", []):
                    if bucket.get("time") is None: continue
                    bucket_time = datetime.fromtimestamp(bucket["time"], tz=timezone.utc).replace(tzinfo=None)
                    stmt = select(ApiKeyCostRecord).where(ApiKeyCostRecord.tracking_id == tracking_id, ApiKeyCostRecord.model == series.get("model", "unknown"), ApiKeyCostRecord.bucket_time == bucket_time)
                    row = (await self.db.execute(stmt)).scalar_one_or_none()
                    values = {"key_name": key.get("name") or "Unnamed key", "sensitive_id": key.get("sensitive_id") or "", "cost": float(bucket.get("cost") or 0), "currency": currency}
                    if row:
                        for field, value in values.items(): setattr(row, field, value)
                    else: self.db.add(ApiKeyCostRecord(tracking_id=tracking_id, model=series.get("model", "unknown"), bucket_time=bucket_time, **values))
                    count += 1
        await self.db.commit(); return count

    def _history_chunks(self):
        today_start = datetime.combine(date.today(), time.min, tzinfo=timezone.utc)
        cursor = today_start - timedelta(days=HISTORY_DAYS)
        while cursor < today_start:
            chunk_end = min(cursor + timedelta(days=HISTORY_CHUNK_DAYS), today_start)
            yield cursor, chunk_end
            cursor = chunk_end

    async def sync_initial_history(self) -> int:
        if (await self.db.execute(select(ApiKeyUsageRecord.id).limit(1))).scalar_one_or_none(): return 0
        return sum([await self.sync(s, e) for s, e in self._history_chunks()])

    async def sync_cost_initial_history(self) -> int:
        if (await self.db.execute(select(ApiKeyCostRecord.id).limit(1))).scalar_one_or_none(): return 0
        return sum([await self.sync_cost(s, e) for s, e in self._history_chunks()])

    async def rankings(self) -> KeyUsageRankings:
        now = datetime.utcnow(); today = datetime.combine(date.today(), time.min); year = datetime(now.year, 1, 1)
        return KeyUsageRankings(today=await self._ranking(today, now), year=await self._ranking(year, now), last_30_days=await self._ranking(now-timedelta(days=30), now))
    async def ranking_for_range(self, start: datetime, end: datetime): return await self._ranking(start, end)

    async def _ranking(self, start, end):
        total = ApiKeyUsageRecord.response_tokens + ApiKeyUsageRecord.prompt_cache_hit_tokens + ApiKeyUsageRecord.prompt_cache_miss_tokens
        stmt = select(ApiKeyUsageRecord.tracking_id, func.max(ApiKeyUsageRecord.key_name).label("name"), func.max(ApiKeyUsageRecord.sensitive_id).label("sensitive_id"), func.coalesce(func.sum(total), 0).label("total_tokens"), func.coalesce(func.sum(ApiKeyUsageRecord.request_count), 0).label("request_count")).where(ApiKeyUsageRecord.bucket_time >= start, ApiKeyUsageRecord.bucket_time < end).group_by(ApiKeyUsageRecord.tracking_id)
        rows = (await self.db.execute(stmt)).all()

        cost_stmt = select(ApiKeyCostRecord.tracking_id, func.max(ApiKeyCostRecord.key_name).label("name"), func.max(ApiKeyCostRecord.sensitive_id).label("sensitive_id"), func.coalesce(func.sum(ApiKeyCostRecord.cost), 0).label("cost")).where(ApiKeyCostRecord.bucket_time >= start, ApiKeyCostRecord.bucket_time < end).group_by(ApiKeyCostRecord.tracking_id)
        cost_rows = (await self.db.execute(cost_stmt)).all()

        # The two payloads are aggregated independently (their model strings
        # differ), so merge them per key rather than per model.
        entries = {
            r.tracking_id: {
                "tracking_id": r.tracking_id, "name": r.name, "sensitive_id": r.sensitive_id,
                "total_tokens": r.total_tokens, "request_count": r.request_count, "cost": 0.0,
            }
            for r in rows
        }
        for r in cost_rows:
            entry = entries.setdefault(r.tracking_id, {
                "tracking_id": r.tracking_id, "name": r.name, "sensitive_id": r.sensitive_id,
                "total_tokens": 0, "request_count": 0, "cost": 0.0,
            })
            entry["cost"] = r.cost

        merged = [
            KeyUsageRanking(
                rank=0,
                tracking_id=e["tracking_id"],
                name=e["name"],
                sensitive_id=e["sensitive_id"],
                total_tokens=e["total_tokens"],
                request_count=e["request_count"],
                cost=round(e["cost"], 6),
            )
            for e in entries.values()
        ]
        merged.sort(key=lambda k: (-k.cost, -k.total_tokens, k.tracking_id))
        for i, item in enumerate(merged, 1): item.rank = i

        cost_available = (await self.db.execute(
            select(func.count()).select_from(ApiKeyCostRecord)
            .where(ApiKeyCostRecord.bucket_time >= start, ApiKeyCostRecord.bucket_time < end)
        )).scalar() > 0
        return KeyUsageRankingSet(items=merged, cost_available=cost_available)

    async def _get_token(self):
        service = CostService(self.db)
        token = await service._get_platform_token()
        if token:
            return token
        try:
            return await service._get_api_key()
        except RuntimeError as exc:
            raise RuntimeError(
                "No usable platform token or active API key. Save and test the platform token "
                "after configuring a stable MASTER_KEY, then restart the backend."
            ) from exc

    async def _fetch(self, token, start, end, path="amount"):
        # Accept a raw access token or a copied full Authorization header value.
        # The endpoint requires exactly one Bearer scheme.
        token = token.strip()
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "x-app-version": "1.0.0",
                "Referer": "https://platform.deepseek.com/usage",
            }
            async with httpx.AsyncClient(timeout=30) as client: response = await client.get(f"{PLATFORM_BASE_URL}/api/v0/usage/by_api_key/{path}", headers=headers, params={"start": int(start.timestamp()), "end": int(end.timestamp()), "tz": 0})
            if response.status_code != 200: raise RuntimeError(f"DeepSeek key usage API error: HTTP {response.status_code}")
            body = response.json()
            if body.get("code") != 0 or body.get("data", {}).get("biz_code", 0) != 0: raise RuntimeError(f"DeepSeek key usage API error: {body.get('msg') or body.get('data', {}).get('biz_msg')}")
            return body.get("data", {}).get("biz_data", {})
        except httpx.TimeoutException: raise RuntimeError("DeepSeek key usage API timeout")
        except httpx.ConnectError: raise RuntimeError("Cannot connect to platform.deepseek.com")


async def poll_api_key_cost():
    from app.core.database import async_session_factory
    from app.models.scheduler_log import SchedulerLog

    async with async_session_factory() as db:
        log = SchedulerLog(task_name="poll_api_key_cost", started_at=datetime.utcnow(), status="running")
        db.add(log)
        try:
            service = ApiKeyUsageService(db)
            initial = await service.sync_cost_initial_history()
            now = datetime.now(timezone.utc)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            # Re-fetch today's buckets because the current bucket can still change.
            count = initial + await service.sync_cost(today_start - timedelta(days=1), today_start)
            log.status, log.message = "success", f"Upserted {count} key cost buckets"
            logger.info("Key cost polled: %d buckets", count)
        except Exception as exc:
            log.status, log.message = "error", f"{type(exc).__name__}: {exc}"
            logger.error("Key cost error: %s", exc)
        log.finished_at = datetime.utcnow()
        await db.commit()
