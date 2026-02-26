from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

from app.core.response import BaseResponse, success_response

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=BaseResponse[dict[str, Any]])
async def health_check() -> BaseResponse[dict[str, Any]]:
    payload = {
        "status": "UP",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return success_response(payload)

