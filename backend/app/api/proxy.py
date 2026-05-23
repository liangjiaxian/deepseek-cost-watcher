import logging

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.core.database import async_session_factory
from app.services.proxy_service import ProxyService
from app.services.key_service import KeyService
from app.services.token_service import TokenRecordService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Proxy"])


def _get_api_key(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    api_key = request.headers.get("X-API-Key", "")
    if api_key:
        return api_key
    raise HTTPException(status_code=401, detail="Missing API key")


async def _get_raw_key(provided_key: str) -> str:
    async with async_session_factory() as db:
        key_service = KeyService(db)
        raw_key = await key_service.get_first_active_key()
        if raw_key:
            return raw_key
    return provided_key


@router.post("/v1/chat/completions")
async def proxy_chat_completions(request: Request):
    body = await request.json()
    provided_key = _get_api_key(request)
    raw_key = await _get_raw_key(provided_key)

    proxy = ProxyService()
    resp_data, usage, duration_ms = await proxy.forward_chat_completion(body, raw_key)

    if usage and "total_tokens" in usage:
        try:
            async with async_session_factory() as db:
                svc = TokenRecordService(db)
                await svc.create_record(
                    model=body.get("model", "unknown"),
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    total_tokens=usage.get("total_tokens", 0),
                    duration_ms=duration_ms,
                    request_id=None,
                )
            logger.info("Captured tokens: model=%s prompt=%d completion=%d total=%d",
                        body.get("model", "unknown"),
                        usage.get("prompt_tokens", 0),
                        usage.get("completion_tokens", 0),
                        usage.get("total_tokens", 0))
        except Exception as e:
            logger.error("Failed to save token record: %s", e)
    else:
        logger.warning("No usage data in DeepSeek response (status=%s, has_usage=%s)",
                       resp_data.get("status", 200) if isinstance(resp_data, dict) else "?",
                       bool(usage))

    status = resp_data.get("status", 200) if isinstance(resp_data, dict) else 200
    return JSONResponse(content=resp_data, status_code=status)


@router.post("/v1/beta/completions")
async def proxy_beta_completions(request: Request):
    body = await request.json()
    provided_key = _get_api_key(request)
    raw_key = await _get_raw_key(provided_key)

    proxy = ProxyService()
    resp_data, usage, duration_ms = await proxy.forward_beta_completion(body, raw_key)

    if usage and "total_tokens" in usage:
        try:
            async with async_session_factory() as db:
                svc = TokenRecordService(db)
                await svc.create_record(
                    model=body.get("model", "unknown"),
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    total_tokens=usage.get("total_tokens", 0),
                    duration_ms=duration_ms,
                    request_id=None,
                )
            logger.info("Captured tokens (beta): model=%s prompt=%d completion=%d total=%d",
                        body.get("model", "unknown"),
                        usage.get("prompt_tokens", 0),
                        usage.get("completion_tokens", 0),
                        usage.get("total_tokens", 0))
        except Exception as e:
            logger.error("Failed to save token record (beta): %s", e)
    else:
        logger.warning("No usage data in DeepSeek beta response (has_usage=%s)", bool(usage))

    return JSONResponse(content=resp_data)
