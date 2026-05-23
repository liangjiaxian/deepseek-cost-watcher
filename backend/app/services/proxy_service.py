from typing import Optional, Dict, Any, Tuple
import httpx
import time

from app.core.config import settings


DEEPSEEK_CHAT_URL = f"{settings.deepseek_base_url}/chat/completions"
DEEPSEEK_BETA_URL = f"{settings.deepseek_base_url}/beta/completions"
DEEPSEEK_MODELS_URL = f"{settings.deepseek_base_url}/models"


class ProxyService:

    async def forward_chat_completion(self, body: Dict[str, Any], api_key: str) -> Tuple[Optional[Dict], Optional[Dict], Optional[int]]:
        return await self._forward(DEEPSEEK_CHAT_URL, body, api_key)

    async def forward_beta_completion(self, body: Dict[str, Any], api_key: str) -> Tuple[Optional[Dict], Optional[Dict], Optional[int]]:
        return await self._forward(DEEPSEEK_BETA_URL, body, api_key)

    async def _forward(self, url: str, body: Dict[str, Any], api_key: str) -> Tuple[Optional[Dict], Optional[Dict], Optional[int]]:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post(url, json=body, headers=headers)
                duration_ms = int((time.monotonic() - start) * 1000)
                resp_data = resp.json()
                usage = resp_data.get("usage")
                return resp_data, usage, duration_ms
        except httpx.TimeoutException:
            return {"error": "request timeout", "status": 408}, None, None
        except Exception as e:
            return {"error": str(e), "status": 500}, None, None

    async def test_connection(self, api_key: str) -> Tuple[bool, str, Optional[float]]:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
        url = f"{settings.deepseek_base_url}/user/balance"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    infos = data.get("balance_infos") or []
                    total_balance = float(infos[0]["total_balance"]) if infos and infos[0].get("total_balance") else None
                    return True, "Connection OK", total_balance
                return False, f"API error: {resp.status_code}", None
        except httpx.ConnectError:
            return False, "Cannot connect to DeepSeek API", None
        except Exception as e:
            return False, str(e), None

    async def fetch_models(self, api_key: str) -> list:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(DEEPSEEK_MODELS_URL, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("data", [])
        except Exception:
            pass
        return []
