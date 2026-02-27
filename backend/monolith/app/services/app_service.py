from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException
from app.models.app import App
from app.models.user import User
from app.schemas.app import AppAddRequest, AppVO
from app.schemas.user import UserVO


class AppService:
    async def add_app(self, db: AsyncSession, payload: AppAddRequest, login_user: User) -> int:
        app_name = self._build_app_name(payload.init_prompt)
        new_app = App(
            app_name=app_name,
            init_prompt=(payload.init_prompt or "").strip() or None,
            code_gen_type="html",
            user_id=login_user.id,
        )
        db.add(new_app)
        await db.commit()
        await db.refresh(new_app)
        return new_app.id

    async def get_app_vo_by_id(self, db: AsyncSession, app_id: int) -> AppVO:
        app_entity = await self.get_app_entity_by_id(db, app_id)
        owner = await db.scalar(select(User).where(User.id == app_entity.user_id, User.is_delete == 0).limit(1))
        user_vo = None
        if owner:
            user_vo = UserVO(
                id=owner.id,
                user_account=owner.user_account,
                user_name=owner.user_name,
                user_avatar=owner.user_avatar,
                user_profile=owner.user_profile,
                user_role=owner.user_role,
                create_time=owner.create_time,
            )
        return AppVO(
            id=app_entity.id,
            app_name=app_entity.app_name,
            cover=app_entity.cover,
            init_prompt=app_entity.init_prompt,
            code_gen_type=app_entity.code_gen_type,
            deploy_key=app_entity.deploy_key,
            deployed_time=app_entity.deployed_time,
            priority=app_entity.priority,
            user_id=app_entity.user_id,
            create_time=app_entity.create_time,
            update_time=app_entity.update_time,
            user=user_vo,
        )

    async def get_app_entity_by_id(self, db: AsyncSession, app_id: int) -> App:
        if app_id <= 0:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Invalid app id")
        app_entity = await db.scalar(select(App).where(App.id == app_id, App.is_delete == 0).limit(1))
        if app_entity is None:
            raise BusinessException(ErrorCode.NOT_FOUND_ERROR, "App not found")
        return app_entity

    @staticmethod
    def _build_app_name(init_prompt: str | None) -> str:
        if not init_prompt:
            return "My App"
        name = init_prompt.strip().replace("\n", " ")
        if not name:
            return "My App"
        return name[:32]
