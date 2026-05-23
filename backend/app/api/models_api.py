from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.services.key_service import KeyService
from app.services.proxy_service import ProxyService

router = APIRouter(prefix="/api/v1/models", tags=["Models"])


@router.get("", response_model=ApiResponse[list])
async def list_models(db: AsyncSession = Depends(get_db)):
    key_service = KeyService(db)
    api_key = await key_service.get_first_active_key()
    if not api_key:
        return ApiResponse(code=1001, message="No active API key", data=[])
    proxy = ProxyService()
    models = await proxy.fetch_models(api_key)
    return ApiResponse(data=models)
