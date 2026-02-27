from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_app_settings, get_db_session, get_user_service, require_role
from app.models.user import User
from app.schemas.user import LoginUserVO, UserLoginRequest, UserRegisterRequest
from app.services.user_service import USER_ROLE_ADMIN, UserService
from app.core.config import Settings
from app.core.response import BaseResponse, success_response

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=BaseResponse[int])
async def user_register(
    payload: UserRegisterRequest,
    db: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
) -> BaseResponse[int]:
    user_id = await user_service.register(db, payload)
    return success_response(user_id)


@router.post("/login", response_model=BaseResponse[LoginUserVO])
async def user_login(
    payload: UserLoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_app_settings),
    user_service: UserService = Depends(get_user_service),
) -> BaseResponse[LoginUserVO]:
    login_user, session_id = await user_service.login(db, payload)
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_id,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
        path="/",
    )
    return success_response(login_user)


@router.get("/get/login", response_model=BaseResponse[LoginUserVO])
async def get_login_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_app_settings),
    user_service: UserService = Depends(get_user_service),
) -> BaseResponse[LoginUserVO]:
    session_id = request.cookies.get(settings.session_cookie_name)
    login_user = await user_service.get_login_user(db, session_id)
    return success_response(login_user)


@router.post("/logout", response_model=BaseResponse[bool])
async def user_logout(
    request: Request,
    response: Response,
    settings: Settings = Depends(get_app_settings),
    user_service: UserService = Depends(get_user_service),
) -> BaseResponse[bool]:
    session_id = request.cookies.get(settings.session_cookie_name)
    result = await user_service.logout(session_id)
    response.delete_cookie(
        key=settings.session_cookie_name,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
        path="/",
    )
    return success_response(result)


@router.get("/admin/ping", response_model=BaseResponse[bool])
async def admin_ping(_: User = Depends(require_role(USER_ROLE_ADMIN))) -> BaseResponse[bool]:
    return success_response(True)
