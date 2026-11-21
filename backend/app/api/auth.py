"""Dashboard access-key authentication.

The key lives in the backend environment (ACCESS_KEY); the login endpoint
exchanges it for a signed, expiring session token. Tokens are signed with
APP_SECRET (falling back to MASTER_KEY) — no extra dependency needed.
"""

import base64
import hashlib
import hmac
import json
import secrets
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

_FALLBACK_SECRET = secrets.token_hex(32)


class LoginPayload(BaseModel):
    key: str


def _secret() -> bytes:
    raw = settings.app_secret or settings.master_key or _FALLBACK_SECRET
    return raw.encode("utf-8")


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _key_fingerprint() -> str:
    return hashlib.sha256(settings.access_key.encode("utf-8")).hexdigest()[:16]


def create_session_token() -> tuple[str, int]:
    expires_at = int(time.time()) + settings.auth_token_ttl_hours * 3600
    payload = _b64encode(json.dumps(
        {"sub": "dashboard", "exp": expires_at, "ak": _key_fingerprint()},
        separators=(",", ":"),
    ).encode("utf-8"))
    signature = hmac.new(_secret(), payload.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}", expires_at


def verify_token(token: str) -> bool:
    if not token:
        return False
    try:
        payload, signature = token.split(".", 1)
        expected = hmac.new(_secret(), payload.encode("ascii"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return False
        data = json.loads(_b64decode(payload))
        return (
            data.get("sub") == "dashboard"
            and data.get("ak") == _key_fingerprint()
            and int(data.get("exp", 0)) > time.time()
        )
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return False


@router.post("/login", response_model=ApiResponse[dict])
async def login(payload: LoginPayload):
    if not settings.access_key:
        raise HTTPException(status_code=503, detail="后端未配置 ACCESS_KEY")
    key = payload.key.strip()
    if not key or not secrets.compare_digest(key, settings.access_key):
        raise HTTPException(status_code=401, detail="访问密钥不正确")

    token, expires_at = create_session_token()
    return ApiResponse(data={
        "token": token,
        "expires_at": expires_at,
        "expires_in": settings.auth_token_ttl_hours * 3600,
    })
