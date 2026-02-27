from collections.abc import AsyncGenerator, Callable

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException
from app.models.user import User
from app.services.session_service import SessionService
from app.services.user_service import UserService


def get_app_settings() -> Settings:
    return get_settings()


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_factory = request.app.state.resources.session_factory
    if session_factory is None:
        raise BusinessException(ErrorCode.SYSTEM_ERROR, "Database is not ready")
    async with session_factory() as session:
        yield session


def get_redis_client(request: Request) -> Redis | None:
    return request.app.state.resources.redis_client


def get_user_service(
    settings: Settings = Depends(get_app_settings),
    redis_client: Redis | None = Depends(get_redis_client),
) -> UserService:
    return UserService(settings=settings, session_service=SessionService(redis_client, settings))


async def get_login_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_app_settings),
    user_service: UserService = Depends(get_user_service),
) -> User:
    session_id = request.cookies.get(settings.session_cookie_name)
    return await user_service.get_login_user_entity(db, session_id)


def require_role(required_role: str) -> Callable[..., User]:
    async def _verify_role(
        login_user: User = Depends(get_login_user),
        user_service: UserService = Depends(get_user_service),
    ) -> User:
        user_service.assert_role(login_user, required_role)
        return login_user

    return _verify_role
