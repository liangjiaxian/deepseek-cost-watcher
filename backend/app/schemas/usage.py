from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RealtimeUsage(BaseModel):
    total_tokens_today: int = 0
    total_calls_today: int = 0
    active_models: int = 0
    balance: Optional[float] = None
    daily_change_percent: Optional[float] = None


class TrendPoint(BaseModel):
    time: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class TrendData(BaseModel):
    range: str
    points: List[TrendPoint]


class ModelDistribution(BaseModel):
    model: str
    total_tokens: int
    percentage: float


class RecentCall(BaseModel):
    id: int
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    duration_ms: Optional[int] = None
    created_at: datetime


class DailySummary(BaseModel):
    date: str
    total_tokens: int
    total_calls: int
    avg_tokens_per_call: float
    active_models: int
    hourly_breakdown: List[TrendPoint]
    model_rankings: List[ModelDistribution]


class WeeklySummary(BaseModel):
    year: int
    week: int
    total_tokens: int
    total_calls: int
    daily_avg_tokens: float
    week_over_week_change: Optional[float] = None
    daily_breakdown: List[TrendPoint]
    model_comparison: List[ModelDistribution]


class BalanceTrendPoint(BaseModel):
    time: str
    balance: float
    total_usage: Optional[float] = None


class BalanceTrend(BaseModel):
    points: List[BalanceTrendPoint]


class DailyBalanceSummary(BaseModel):
    date: str
    balance_start: Optional[float] = None
    balance_end: Optional[float] = None
    balance_change: Optional[float] = None
    points: List[BalanceTrendPoint]


class ModelCostItem(BaseModel):
    type: str
    amount: float


class DailyModelCost(BaseModel):
    model: str
    usage: List[ModelCostItem]


class DailyCost(BaseModel):
    date: str
    data: List[DailyModelCost]


class MonthlyCostSummary(BaseModel):
    year: int
    month: int
    total: List[DailyModelCost]
    days: List[DailyCost]
    currency: str


class WeeklyCostDay(BaseModel):
    date: str
    total_cost: float


class WeeklyCostModel(BaseModel):
    model: str
    cost: float


class WeeklyCostSummary(BaseModel):
    year: int
    week: int
    total_cost: float
    daily_avg_cost: float
    daily_breakdown: List[WeeklyCostDay]
    model_breakdown: List[WeeklyCostModel]
    balance_start: Optional[float] = None
    balance_end: Optional[float] = None
    balance_change: Optional[float] = None
    active_models: int = 0
