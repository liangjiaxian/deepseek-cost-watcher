from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.core.database import Base


class UsageCostRecord(Base):
    __tablename__ = "usage_cost_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10), nullable=False, index=True)
    model = Column(String(64), nullable=False)
    prompt_token_cost = Column(Float, default=0)
    cache_hit_token_cost = Column(Float, default=0)
    cache_miss_token_cost = Column(Float, default=0)
    response_token_cost = Column(Float, default=0)
    request_cost = Column(Float, default=0)
    total_cost = Column(Float, default=0)
    currency = Column(String(10), default="CNY")
    recorded_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("date", "model", name="uq_date_model"),
    )
