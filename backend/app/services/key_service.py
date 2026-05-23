from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.api_key import ApiKey
from app.schemas.settings import ApiKeyInfo, TestKeyResult
from app.core.security import encrypt_api_key, decrypt_api_key
from app.services.proxy_service import ProxyService


class KeyService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_key(self, name: str, key_value: str) -> ApiKey:
        encrypted = encrypt_api_key(key_value)
        prefix = key_value[:8] if len(key_value) >= 8 else key_value
        api_key = ApiKey(name=name, key_encrypted=encrypted, key_prefix=prefix)
        self.db.add(api_key)
        await self.db.commit()
        await self.db.refresh(api_key)
        return api_key

    async def list_keys(self) -> List[ApiKeyInfo]:
        stmt = select(ApiKey).order_by(ApiKey.created_at.desc())
        rows = (await self.db.execute(stmt)).scalars().all()
        return [
            ApiKeyInfo(
                id=r.id,
                name=r.name,
                key_prefix=r.key_prefix or "",
                is_active=bool(r.is_active),
                created_at=r.created_at,
            )
            for r in rows
        ]

    async def delete_key(self, key_id: int) -> bool:
        stmt = select(ApiKey).where(ApiKey.id == key_id)
        key = (await self.db.execute(stmt)).scalar_one_or_none()
        if not key:
            return False
        await self.db.delete(key)
        await self.db.commit()
        return True

    async def test_key(self, key_value: str) -> TestKeyResult:
        proxy = ProxyService()
        ok, msg, balance = await proxy.test_connection(key_value)
        return TestKeyResult(success=ok, message=msg, balance=balance)

    async def get_decrypted_key(self, key_id: int) -> Optional[str]:
        stmt = select(ApiKey).where(ApiKey.id == key_id, ApiKey.is_active == 1)
        key = (await self.db.execute(stmt)).scalar_one_or_none()
        if not key:
            return None
        return decrypt_api_key(key.key_encrypted)

    async def get_first_active_key(self) -> Optional[str]:
        stmt = select(ApiKey).where(ApiKey.is_active == 1).order_by(ApiKey.id.asc()).limit(1)
        key = (await self.db.execute(stmt)).scalar_one_or_none()
        if not key:
            return None
        return decrypt_api_key(key.key_encrypted)
