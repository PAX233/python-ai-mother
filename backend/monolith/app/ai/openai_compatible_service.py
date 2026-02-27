import json
from collections.abc import AsyncIterator

import httpx

from app.core.config import Settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException


class OpenAICompatibleService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate_stream(self, system_prompt: str, user_prompt: str) -> AsyncIterator[str]:
        if not self.settings.llm_base_url or not self.settings.llm_api_key:
            raise BusinessException(ErrorCode.SYSTEM_ERROR, "LLM config is missing")

        payload = {
            "model": self.settings.llm_model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": self.settings.llm_stream,
        }
        headers = {
            "Authorization": f"Bearer {self.settings.llm_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(
            base_url=self.settings.llm_base_url,
            timeout=self.settings.llm_timeout_seconds,
        ) as client:
            try:
                async with client.stream(
                    "POST",
                    "/chat/completions",
                    headers=headers,
                    json=payload,
                ) as response:
                    if response.status_code != 200:
                        body = await response.aread()
                        error_text = body.decode("utf-8", errors="ignore")
                        raise BusinessException(ErrorCode.SYSTEM_ERROR, f"LLM request failed: {error_text[:300]}")

                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            payload_json = json.loads(data_str)
                            choices = payload_json.get("choices") or []
                            if not choices:
                                continue
                            delta = choices[0].get("delta") or {}
                            content = delta.get("content")
                            if content:
                                yield str(content)
                        except json.JSONDecodeError:
                            continue
            except httpx.TimeoutException as exc:
                raise BusinessException(
                    ErrorCode.SYSTEM_ERROR,
                    f"LLM request timeout, please increase LLM_TIMEOUT_SECONDS (current={self.settings.llm_timeout_seconds})",
                ) from exc
            except httpx.HTTPError as exc:
                raise BusinessException(ErrorCode.SYSTEM_ERROR, f"LLM request network error: {exc}") from exc
