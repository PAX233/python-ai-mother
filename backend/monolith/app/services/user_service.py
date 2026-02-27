import re

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginUserVO, UserLoginRequest, UserRegisterRequest
from app.services.session_service import SessionService

USER_ROLE_USER = "user"
USER_ROLE_ADMIN = "admin"


class UserService:
    _account_pattern = re.compile(r"^[A-Za-z0-9_]{4,64}$")

    def __init__(self, settings: Settings, session_service: SessionService) -> None:
        self.settings = settings
        self.session_service = session_service

    async def register(self, db: AsyncSession, payload: UserRegisterRequest) -> int:
        user_account = (payload.user_account or "").strip()
        user_password = payload.user_password or ""
        check_password = payload.check_password or ""
        self._validate_register_fields(user_account, user_password, check_password)

        exists = await db.scalar(self._active_user_select().where(User.user_account == user_account).limit(1))
        if exists is not None:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Account already exists")

        new_user = User(
            user_account=user_account,
            user_password=hash_password(user_password, self.settings.password_salt),
            user_name=f"user_{user_account}",
            user_role=USER_ROLE_USER,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user.id

    async def login(self, db: AsyncSession, payload: UserLoginRequest) -> tuple[LoginUserVO, str]:
        user_account = (payload.user_account or "").strip()
        user_password = payload.user_password or ""
        if not user_account or not user_password:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Account or password is empty")

        user = await db.scalar(self._active_user_select().where(User.user_account == user_account).limit(1))
        if user is None:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Invalid account or password")
        if not verify_password(user_password, user.user_password, self.settings.password_salt):
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Invalid account or password")

        session_id = await self.session_service.create_session(user.id, user.user_role)
        return self._to_login_vo(user), session_id

    async def get_login_user(self, db: AsyncSession, session_id: str | None) -> LoginUserVO:
        user = await self.get_login_user_entity(db, session_id)
        return self._to_login_vo(user)

    async def get_login_user_entity(self, db: AsyncSession, session_id: str | None) -> User:
        if not session_id:
            raise BusinessException(ErrorCode.NOT_LOGIN_ERROR, "Not logged in")

        session_payload = await self.session_service.get_session(session_id)
        if session_payload is None:
            raise BusinessException(ErrorCode.NOT_LOGIN_ERROR, "Not logged in")

        user = await db.scalar(
            self._active_user_select().where(User.id == session_payload.user_id).limit(1)
        )
        if user is None:
            await self.session_service.delete_session(session_id)
            raise BusinessException(ErrorCode.NOT_LOGIN_ERROR, "Not logged in")
        return user

    async def logout(self, session_id: str | None) -> bool:
        if not session_id:
            return True
        await self.session_service.delete_session(session_id)
        return True

    def assert_role(self, user: User, required_role: str) -> None:
        if user.user_role != required_role:
            raise BusinessException(ErrorCode.NO_AUTH_ERROR, "No permission")

    def _validate_register_fields(self, user_account: str, user_password: str, check_password: str) -> None:
        if not user_account or not user_password or not check_password:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Account or password is empty")
        if len(user_password) < 8:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Password too short")
        if user_password != check_password:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Password and checkPassword do not match")
        if not self._account_pattern.fullmatch(user_account):
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Invalid account format")

    @staticmethod
    def _to_login_vo(user: User) -> LoginUserVO:
        return LoginUserVO(
            id=user.id,
            user_account=user.user_account,
            user_name=user.user_name,
            user_avatar=user.user_avatar,
            user_profile=user.user_profile,
            user_role=user.user_role,
            create_time=user.create_time,
            update_time=user.update_time,
        )

    @staticmethod
    def _active_user_select() -> Select[tuple[User]]:
        return select(User).where(User.is_delete == 0)
