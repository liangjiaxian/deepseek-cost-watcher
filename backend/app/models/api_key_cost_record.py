from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint

from app.core.database import Base


class ApiKeyCostRecord(Base):
    """Per-key cost bucket returned by DeepSeek's by_api_key/cost endpoint.

    Kept separate from ApiKeyUsageRecord because the cost endpoint reports a
    merged model name (e.g. "deepseek-chat & deepseek-reasoner"), so the two
    payloads cannot be joined on model.
    """
    __tablename__ = "api_key_cost_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_id = Column(String(64), nullable=False, index=True)
    key_name = Column(String(128), nullable=False, default="")
    sensitive_id = Column(String(128), nullable=False, default="")
    model = Column(String(128), nullable=False)
    bucket_time = Column(DateTime, nullable=False, index=True)
    cost = Column(Float, nullable=False, default=0)
    currency = Column(String(10), nullable=False, default="CNY")
    __table_args__ = (UniqueConstraint("tracking_id", "model", "bucket_time", name="uq_key_model_cost_bucket"),)
