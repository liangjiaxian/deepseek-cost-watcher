from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.settings import (
    ApiKeyCreate, ApiKeyInfo, TestKeyRequest,
    TestKeyResult, ConfigUpdate, ConfigInfo, PlatformTokenUpdate,
)
from app.services.key_service import KeyService
from app.services.cost_service import CostService
from app.models.system_config import SystemConfig
from app.core.security import encrypt_api_key
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/settings", tags=["Settings"])


@router.post("/keys", response_model=ApiResponse[ApiKeyInfo])
async def add_api_key(body: ApiKeyCreate, db: AsyncSession = Depends(get_db)):
    service = KeyService(db)
    key = await service.create_key(body.name, body.key_value)
    return ApiResponse(data=ApiKeyInfo(
        id=key.id, name=key.name,
        key_prefix=key.key_prefix or "",
        is_active=bool(key.is_active),
        created_at=key.created_at,
    ))


@router.get("/keys", response_model=ApiResponse[List[ApiKeyInfo]])
async def list_api_keys(db: AsyncSession = Depends(get_db)):
    service = KeyService(db)
    data = await service.list_keys()
    return ApiResponse(data=data)


@router.delete("/keys/{key_id}", response_model=ApiResponse)
async def delete_api_key(key_id: int, db: AsyncSession = Depends(get_db)):
    service = KeyService(db)
    ok = await service.delete_key(key_id)
    if not ok:
        return ApiResponse(code=1004, message="Key not found")
    return ApiResponse(message="Key deleted")


@router.post("/keys/test", response_model=ApiResponse[TestKeyResult])
async def test_api_key(body: TestKeyRequest, db: AsyncSession = Depends(get_db)):
    service = KeyService(db)
    result = await service.test_key(body.key_value)
    return ApiResponse(data=result)


@router.get("/config", response_model=ApiResponse[list])
async def get_config(db: AsyncSession = Depends(get_db)):
    stmt = select(SystemConfig)
    rows = (await db.execute(stmt)).scalars().all()
    data = [
        ConfigInfo(config_key=r.config_key, config_value=r.config_value, updated_at=r.updated_at)
        for r in rows
    ]
    return ApiResponse(data=data)


@router.put("/config", response_model=ApiResponse)
async def update_config(body: ConfigUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(SystemConfig).where(SystemConfig.config_key == body.config_key)
    row = (await db.execute(stmt)).scalar_one_or_none()
    if row:
        row.config_value = body.config_value
    else:
        row = SystemConfig(config_key=body.config_key, config_value=body.config_value)
        db.add(row)
    await db.commit()

    if body.config_key == "poll_interval":
        from app.tasks.scheduler import reschedule_polling
        await reschedule_polling(int(body.config_value))

    return ApiResponse(message="Config updated")


@router.get("/platform-token")
async def get_platform_token_status(db: AsyncSession = Depends(get_db)):
    stmt = select(SystemConfig).where(SystemConfig.config_key == "platform_token")
    row = (await db.execute(stmt)).scalar_one_or_none()
    return ApiResponse(data={"configured": bool(row and row.config_value), "updated_at": row.updated_at if row else None})


@router.put("/platform-token")
async def update_platform_token(body: PlatformTokenUpdate, db: AsyncSession = Depends(get_db)):
    encrypted = encrypt_api_key(body.token)
    stmt = select(SystemConfig).where(SystemConfig.config_key == "platform_token")
    row = (await db.execute(stmt)).scalar_one_or_none()
    if row:
        row.config_value = encrypted
    else:
        row = SystemConfig(config_key="platform_token", config_value=encrypted)
        db.add(row)
    await db.commit()
    return ApiResponse(message="Platform token saved")


@router.post("/platform-token/test")
async def test_platform_token(body: PlatformTokenUpdate):
    ok, msg = await CostService.test_platform_token(body.token)
    return ApiResponse(data=TestKeyResult(success=ok, message=msg))
