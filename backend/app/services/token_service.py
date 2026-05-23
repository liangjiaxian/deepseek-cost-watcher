from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from datetime import datetime, timedelta, date, timezone
from typing import List, Optional

from app.models.token_record import TokenRecord
from app.schemas.usage import (
    RealtimeUsage, TrendData, TrendPoint,
    ModelDistribution, RecentCall, DailySummary, WeeklySummary,
)
from app.services.key_service import KeyService


class TokenService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_realtime_usage(self) -> RealtimeUsage:
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = today_start + timedelta(days=1)

        stmt = select(
            func.coalesce(func.sum(TokenRecord.total_tokens), 0).label("total_tokens"),
            func.count(TokenRecord.id).label("total_calls"),
            func.count(func.distinct(TokenRecord.model)).label("active_models"),
        ).where(
            TokenRecord.created_at >= today_start,
            TokenRecord.created_at < today_end,
        )
        result = (await self.db.execute(stmt)).one()

        yesterday_start = today_start - timedelta(days=1)
        yesterday_stmt = select(
            func.coalesce(func.sum(TokenRecord.total_tokens), 0)
        ).where(
            TokenRecord.created_at >= yesterday_start,
            TokenRecord.created_at < today_start,
        )
        yesterday_total = (await self.db.execute(yesterday_stmt)).scalar() or 0

        daily_change = None
        if yesterday_total > 0:
            daily_change = round((result.total_tokens - yesterday_total) / yesterday_total * 100, 1)

        balance = await self._get_latest_balance()

        return RealtimeUsage(
            total_tokens_today=result.total_tokens,
            total_calls_today=result.total_calls,
            active_models=result.active_models,
            balance=balance,
            daily_change_percent=daily_change,
        )

    async def get_trend(self, range_hours: int = 24) -> TrendData:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=range_hours)

        bucket_fmt = "%Y-%m-%dT%H:00:00"
        if range_hours <= 1:
            bucket_fmt = "%Y-%m-%dT%H:%M:00"
        elif range_hours > 168:
            bucket_fmt = "%Y-%m-%dT00:00:00"

        stmt = select(
            func.strftime(bucket_fmt, TokenRecord.created_at).label("bucket"),
            func.coalesce(func.sum(TokenRecord.prompt_tokens), 0).label("prompt_tokens"),
            func.coalesce(func.sum(TokenRecord.completion_tokens), 0).label("completion_tokens"),
            func.coalesce(func.sum(TokenRecord.total_tokens), 0).label("total_tokens"),
        ).where(
            TokenRecord.created_at >= start_time,
            TokenRecord.created_at < end_time,
        ).group_by("bucket").order_by("bucket")

        rows = (await self.db.execute(stmt)).all()

        points = [
            TrendPoint(
                time=row.bucket + "Z",
                prompt_tokens=row.prompt_tokens,
                completion_tokens=row.completion_tokens,
                total_tokens=row.total_tokens,
            )
            for row in rows
        ]

        return TrendData(range=f"{range_hours}h", points=points)

    async def get_model_distribution(self) -> List[ModelDistribution]:
        today_start = datetime.combine(date.today(), datetime.min.time())

        stmt = select(
            TokenRecord.model,
            func.coalesce(func.sum(TokenRecord.total_tokens), 0).label("total_tokens"),
        ).where(
            TokenRecord.created_at >= today_start,
        ).group_by(TokenRecord.model)

        rows = (await self.db.execute(stmt)).all()
        grand_total = sum(r.total_tokens for r in rows) or 1

        return [
            ModelDistribution(
                model=r.model,
                total_tokens=r.total_tokens,
                percentage=round(r.total_tokens / grand_total * 100, 1),
            )
            for r in sorted(rows, key=lambda x: x.total_tokens, reverse=True)
        ]

    async def get_recent_calls(self, limit: int = 20) -> List[RecentCall]:
        stmt = select(TokenRecord).order_by(TokenRecord.created_at.desc()).limit(limit)
        rows = (await self.db.execute(stmt)).scalars().all()
        return [
            RecentCall(
                id=r.id,
                model=r.model,
                prompt_tokens=r.prompt_tokens,
                completion_tokens=r.completion_tokens,
                total_tokens=r.total_tokens,
                duration_ms=r.duration_ms,
                created_at=r.created_at.replace(tzinfo=timezone.utc),
            )
            for r in rows
        ]

    async def get_daily_summary(self, target_date: date) -> DailySummary:
        day_start = datetime.combine(target_date, datetime.min.time())
        day_end = day_start + timedelta(days=1)

        total_tokens = 0
        total_calls = 0
        try:
            stmt = select(
                func.coalesce(func.sum(TokenRecord.total_tokens), 0),
                func.count(TokenRecord.id),
            ).where(
                TokenRecord.created_at >= day_start,
                TokenRecord.created_at < day_end,
            )
            row = (await self.db.execute(stmt)).one()
            total_tokens = row[0]
            total_calls = row[1]
        except Exception:
            pass

        stmt_models = select(
            func.count(func.distinct(TokenRecord.model))
        ).where(
            TokenRecord.created_at >= day_start,
            TokenRecord.created_at < day_end,
        )
        active_models = (await self.db.execute(stmt_models)).scalar() or 0

        hourly = await self._get_hourly_breakdown(day_start, day_end)
        rankings = await self._get_model_rankings(day_start, day_end)

        return DailySummary(
            date=target_date.isoformat(),
            total_tokens=total_tokens,
            total_calls=total_calls,
            avg_tokens_per_call=round(total_tokens / total_calls, 1) if total_calls else 0,
            active_models=active_models,
            hourly_breakdown=hourly,
            model_rankings=rankings,
        )

    async def get_weekly_summary(self, year: int, week: int) -> WeeklySummary:
        week_start = date.fromisocalendar(year, week, 1)
        week_end = week_start + timedelta(days=7)

        dt_start = datetime.combine(week_start, datetime.min.time())
        dt_end = datetime.combine(week_end, datetime.min.time())

        stmt = select(
            func.coalesce(func.sum(TokenRecord.total_tokens), 0),
            func.count(TokenRecord.id),
        ).where(
            TokenRecord.created_at >= dt_start,
            TokenRecord.created_at < dt_end,
        )
        row = (await self.db.execute(stmt)).one()
        total_tokens = row[0]
        total_calls = row[1]

        daily_break = []
        for i in range(7):
            d = week_start + timedelta(days=i)
            ds = datetime.combine(d, datetime.min.time())
            de = ds + timedelta(days=1)
            s = select(func.coalesce(func.sum(TokenRecord.total_tokens), 0)).where(
                TokenRecord.created_at >= ds, TokenRecord.created_at < de,
            )
            t = (await self.db.execute(s)).scalar() or 0
            daily_break.append(TrendPoint(time=d.isoformat(), total_tokens=t, prompt_tokens=0, completion_tokens=0))

        rankings = await self._get_model_rankings(dt_start, dt_end)

        prev_start = dt_start - timedelta(days=7)
        prev_end = dt_start
        prev = select(func.coalesce(func.sum(TokenRecord.total_tokens), 0)).where(
            TokenRecord.created_at >= prev_start, TokenRecord.created_at < prev_end,
        )
        prev_total = (await self.db.execute(prev)).scalar() or 0
        wow_change = round((total_tokens - prev_total) / prev_total * 100, 1) if prev_total else None

        return WeeklySummary(
            year=year,
            week=week,
            total_tokens=total_tokens,
            total_calls=total_calls,
            daily_avg_tokens=round(total_tokens / 7, 1),
            week_over_week_change=wow_change,
            daily_breakdown=daily_break,
            model_comparison=rankings,
        )

    async def _get_hourly_breakdown(self, start: datetime, end: datetime) -> List[TrendPoint]:
        stmt = select(
            func.strftime("%Y-%m-%dT%H:00:00", TokenRecord.created_at).label("hour"),
            func.coalesce(func.sum(TokenRecord.prompt_tokens), 0),
            func.coalesce(func.sum(TokenRecord.completion_tokens), 0),
            func.coalesce(func.sum(TokenRecord.total_tokens), 0),
        ).where(
            TokenRecord.created_at >= start,
            TokenRecord.created_at < end,
        ).group_by("hour").order_by("hour")

        rows = (await self.db.execute(stmt)).all()
        return [
            TrendPoint(time=r.hour + "Z", prompt_tokens=r[1], completion_tokens=r[2], total_tokens=r[3])
            for r in rows
        ]

    async def _get_model_rankings(self, start: datetime, end: datetime) -> List[ModelDistribution]:
        stmt = select(
            TokenRecord.model,
            func.coalesce(func.sum(TokenRecord.total_tokens), 0),
        ).where(
            TokenRecord.created_at >= start,
            TokenRecord.created_at < end,
        ).group_by(TokenRecord.model)

        rows = (await self.db.execute(stmt)).all()
        gt = sum(r[1] for r in rows) or 1
        return [
            ModelDistribution(model=r.model, total_tokens=r[1], percentage=round(r[1] / gt * 100, 1))
            for r in sorted(rows, key=lambda x: x[1], reverse=True)
        ]

    async def _get_latest_balance(self) -> Optional[float]:
        from app.models.balance_snapshot import BalanceSnapshot
        stmt = select(BalanceSnapshot.balance).order_by(BalanceSnapshot.recorded_at.desc()).limit(1)
        result = await self.db.execute(stmt)
        row = result.scalar_one_or_none()
        return row


class TokenRecordService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_record(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        duration_ms: Optional[int] = None,
        request_id: Optional[str] = None,
        api_key_id: Optional[int] = None,
    ) -> TokenRecord:
        record = TokenRecord(
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            duration_ms=duration_ms,
            request_id=request_id,
            api_key_id=api_key_id,
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
