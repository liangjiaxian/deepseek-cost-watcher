from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

from app.core.database import Base


class ApiKeyUsageRecord(Base):
    """A snapshot returned by DeepSeek for one key, model, and time bucket."""
    __tablename__ = "api_key_usage_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_id = Column(String(64), nullable=False, index=True)
    key_name = Column(String(128), nullable=False, default="")
    sensitive_id = Column(String(128), nullable=False, default="")
    model = Column(String(128), nullable=False)
    bucket_time = Column(DateTime, nullable=False, index=True)
    response_tokens = Column(Integer, nullable=False, default=0)
    request_count = Column(Integer, nullable=False, default=0)
    prompt_cache_hit_tokens = Column(Integer, nullable=False, default=0)
    prompt_cache_miss_tokens = Column(Integer, nullable=False, default=0)
    __table_args__ = (UniqueConstraint("tracking_id", "model", "bucket_time", name="uq_key_model_bucket"),)
