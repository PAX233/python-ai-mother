import logging
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ai_codegen_facade import AiCodeGeneratorFacade
from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException
from app.core.response import BaseResponse, success_response
from app.core.sse import build_sse_data, build_sse_event
from app.dependencies import (
    get_ai_codegen_facade,
    get_app_service,
    get_db_session,
    get_login_user,
)
from app.models.user import User
from app.schemas.app import AppAddRequest, AppVO
from app.services.app_service import AppService
from app.services.user_service import USER_ROLE_ADMIN

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/app", tags=["app"])


@router.post("/add", response_model=BaseResponse[int])
async def add_app(
    payload: AppAddRequest,
    login_user: User = Depends(get_login_user),
    db: AsyncSession = Depends(get_db_session),
    app_service: AppService = Depends(get_app_service),
) -> BaseResponse[int]:
    app_id = await app_service.add_app(db, payload, login_user)
    return success_response(app_id)


@router.get("/get/vo", response_model=BaseResponse[AppVO])
async def get_app_vo_by_id(
    id: int,
    db: AsyncSession = Depends(get_db_session),
    app_service: AppService = Depends(get_app_service),
) -> BaseResponse[AppVO]:
    app_vo = await app_service.get_app_vo_by_id(db, id)
    return success_response(app_vo)


@router.get("/chat/gen/code")
async def chat_to_gen_code(
    app_id: int = Query(alias="appId", gt=0),
    message: str = Query(min_length=1),
    login_user: User = Depends(get_login_user),
    db: AsyncSession = Depends(get_db_session),
    app_service: AppService = Depends(get_app_service),
    ai_facade: AiCodeGeneratorFacade = Depends(get_ai_codegen_facade),
) -> StreamingResponse:
    app_entity = await app_service.get_app_entity_by_id(db, app_id)
    if app_entity.user_id != login_user.id and login_user.user_role != USER_ROLE_ADMIN:
        raise BusinessException(ErrorCode.NO_AUTH_ERROR, "No permission")

    user_prompt = message.strip()
    if app_entity.init_prompt:
        user_prompt = f"{app_entity.init_prompt}\n\n{user_prompt}"

    async def _stream() -> AsyncIterator[str]:
        try:
            async for chunk in ai_facade.generate_and_save_code_stream(
                app_id=app_entity.id,
                user_message=user_prompt,
                code_gen_type=app_entity.code_gen_type,
            ):
                yield build_sse_data({"d": chunk})
            yield build_sse_event("done", "done")
        except BusinessException as exc:
            yield build_sse_event(
                "business-error",
                {"code": int(exc.code), "message": exc.message},
            )
        except Exception as exc:
            logger.exception("Unexpected SSE error: %s", exc)
            yield build_sse_event(
                "business-error",
                {"code": int(ErrorCode.SYSTEM_ERROR), "message": "System error"},
            )

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(_stream(), media_type="text/event-stream", headers=headers)
