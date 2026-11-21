from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.usage import (
    RealtimeUsage, TrendData, ModelDistribution,
    RecentCall, DailySummary, WeeklySummary, BalanceTrend, BalanceLatest,
    DailyBalanceSummary, MonthlyCostSummary, WeeklyCostSummary,
    KeyUsageRankings, KeyUsageRankingSet, MonthlyCostReport,
)
from app.services.token_service import TokenService
from app.services.balance_service import BalanceService
from app.services.cost_service import CostService
from app.services.api_key_usage_service import ApiKeyUsageService
from app.core.timeutil import today_beijing, beijing_day_start_utc_naive

router = APIRouter(prefix="/api/v1/usage", tags=["Usage"])


@router.get("/realtime", response_model=ApiResponse[RealtimeUsage])
async def get_realtime_usage(db: AsyncSession = Depends(get_db)):
    service = TokenService(db)
    data = await service.get_realtime_usage()
    return ApiResponse(data=data)


@router.get("/trend", response_model=ApiResponse[TrendData])
async def get_trend(
    range: str = Query("24h", description="Time range: 1h, 6h, 24h, 7d"),
    db: AsyncSession = Depends(get_db),
):
    range_map = {"1h": 1, "6h": 6, "24h": 24, "7d": 168}
    hours = range_map.get(range, 24)
    service = TokenService(db)
    data = await service.get_trend(hours)
    return ApiResponse(data=data)


@router.get("/daily", response_model=ApiResponse[DailySummary])
async def get_daily_summary(
    date_str: str = Query(default=None, alias="date", description="Date in YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
):
    target = date.fromisoformat(date_str) if date_str else today_beijing()
    service = TokenService(db)
    data = await service.get_daily_summary(target)
    return ApiResponse(data=data)


@router.get("/weekly", response_model=ApiResponse[WeeklySummary])
async def get_weekly_summary(
    year: int = Query(default=None, description="Year"),
    week: int = Query(default=None, description="Week number (1-53)"),
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime
    today = today_beijing()
    iso = today.isocalendar()
    y = year if year else iso[0]
    w = week if week else iso[1]
    service = TokenService(db)
    data = await service.get_weekly_summary(y, w)
    return ApiResponse(data=data)


@router.get("/recent", response_model=ApiResponse[list[RecentCall]])
async def get_recent_calls(
    limit: int = Query(default=20, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = TokenService(db)
    data = await service.get_recent_calls(limit)
    return ApiResponse(data=data)


@router.get("/models/distribution", response_model=ApiResponse[list[ModelDistribution]])
async def get_model_distribution(db: AsyncSession = Depends(get_db)):
    service = TokenService(db)
    data = await service.get_model_distribution()
    return ApiResponse(data=data)


@router.get("/balance/trend", response_model=ApiResponse[BalanceTrend])
async def get_balance_trend(
    range: str = Query("7d", description="Time range: 1d, 7d, 30d"),
    db: AsyncSession = Depends(get_db),
):
    range_map = {"1d": 24, "7d": 168, "30d": 720}
    hours = range_map.get(range, 168)
    service = BalanceService(db)
    data = await service.get_balance_trend(hours)
    return ApiResponse(data=data)


@router.get("/balance/latest", response_model=ApiResponse[Optional[BalanceLatest]])
async def get_latest_balance(db: AsyncSession = Depends(get_db)):
    """Latest balance snapshot with the grant/top-up split."""
    return ApiResponse(data=await BalanceService(db).get_latest())


@router.get("/balance/daily", response_model=ApiResponse[DailyBalanceSummary])
async def get_daily_balance(
    date_str: str = Query(default=None, alias="date", description="Date in YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
):
    target = date.fromisoformat(date_str) if date_str else today_beijing()
    service = BalanceService(db)
    data = await service.get_daily_balance(target)
    return ApiResponse(data=data)


@router.get("/cost", response_model=ApiResponse[MonthlyCostSummary])
async def get_usage_cost(
    year: int = Query(default=None, description="Year"),
    month: int = Query(default=None, description="Month (1-12)"),
    refresh: bool = Query(default=False, description="Fetch fresh data from DeepSeek"),
    db: AsyncSession = Depends(get_db),
):
    today = today_beijing()
    y = year if year else today.year
    m = month if month else today.month
    service = CostService(db)
    if refresh:
        try:
            data = await service.fetch_and_store_monthly_cost(y, m)
        except RuntimeError as e:
            existing = await service.get_monthly_cost(y, m)
            if existing.days:
                return ApiResponse(code=1002, message=str(e), data=existing)
            return ApiResponse(code=1002, message=str(e), data=MonthlyCostSummary(
                year=y, month=m, total=[], days=[], currency="CNY",
            ))
    else:
        data = await service.get_monthly_cost(y, m)
    return ApiResponse(data=data)


@router.get("/cost/weekly", response_model=ApiResponse[WeeklyCostSummary])
async def get_weekly_cost(
    year: int = Query(default=None, description="Year"),
    week: int = Query(default=None, description="ISO week number (1-53)"),
    db: AsyncSession = Depends(get_db),
):
    from datetime import date as date_type
    today = date_type.today()
    iso = today.isocalendar()
    y = year if year else iso[0]
    w = week if week else iso[1]
    service = CostService(db)
    data = await service.get_weekly_cost(y, w)
    return ApiResponse(data=data)


@router.get("/cost/monthly", response_model=ApiResponse[MonthlyCostReport])
async def get_monthly_report(
    year: int = Query(default=None, description="Year"),
    month: int = Query(default=None, description="Month (1-12)"),
    db: AsyncSession = Depends(get_db),
):
    today = today_beijing()
    service = CostService(db)
    data = await service.get_monthly_report(
        year if year else today.year,
        month if month else today.month,
    )
    return ApiResponse(data=data)


@router.get("/key-rankings", response_model=ApiResponse[KeyUsageRankings])
async def get_key_rankings(db: AsyncSession = Depends(get_db)):
    return ApiResponse(data=await ApiKeyUsageService(db).rankings())


@router.get("/key-rankings/daily", response_model=ApiResponse[KeyUsageRankingSet])
async def get_daily_key_rankings(
    date_str: str = Query(default=None, alias="date"), db: AsyncSession = Depends(get_db),
):
    target = date.fromisoformat(date_str) if date_str else today_beijing()
    start = beijing_day_start_utc_naive(target)
    end = beijing_day_start_utc_naive(target + timedelta(days=1))
    return ApiResponse(data=await ApiKeyUsageService(db).ranking_for_range(start, end))


@router.get("/key-rankings/weekly", response_model=ApiResponse[KeyUsageRankingSet])
async def get_weekly_key_rankings(
    year: int = Query(default=None), week: int = Query(default=None), db: AsyncSession = Depends(get_db),
):
    current = today_beijing().isocalendar()
    week_start = date.fromisocalendar(year or current[0], week or current[1], 1)
    start = beijing_day_start_utc_naive(week_start)
    end = beijing_day_start_utc_naive(week_start + timedelta(days=7))
    return ApiResponse(data=await ApiKeyUsageService(db).ranking_for_range(start, end))


@router.get("/key-rankings/monthly", response_model=ApiResponse[KeyUsageRankingSet])
async def get_monthly_key_rankings(
    year: int = Query(default=None), month: int = Query(default=None), db: AsyncSession = Depends(get_db),
):
    today = today_beijing()
    y = year or today.year
    m = month or today.month
    start = beijing_day_start_utc_naive(date(y, m, 1))
    next_month = date(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1)
    end = beijing_day_start_utc_naive(next_month)
    return ApiResponse(data=await ApiKeyUsageService(db).ranking_for_range(start, end))
