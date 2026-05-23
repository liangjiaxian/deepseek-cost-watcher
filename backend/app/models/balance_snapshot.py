from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class BalanceSnapshot(Base):
    __tablename__ = "balance_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=True)
    balance = Column(Float, nullable=False)
    total_usage = Column(Float, nullable=True)
    currency = Column(String(10), default="CNY")
    recorded_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
