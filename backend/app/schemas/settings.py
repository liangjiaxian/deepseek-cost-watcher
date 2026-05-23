from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PlatformTokenUpdate(BaseModel):
    token: str


class ApiKeyCreate(BaseModel):
    name: str
    key_value: str


class ApiKeyInfo(BaseModel):
    id: int
    name: str
    key_prefix: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TestKeyRequest(BaseModel):
    key_value: str


class TestKeyResult(BaseModel):
    success: bool
    message: str
    balance: Optional[float] = None


class ConfigUpdate(BaseModel):
    config_key: str
    config_value: str


class ConfigInfo(BaseModel):
    config_key: str
    config_value: str
    updated_at: datetime
