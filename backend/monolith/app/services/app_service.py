import io
import zipfile
from datetime import UTC, datetime
from math import ceil
from pathlib import Path

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_codes import ErrorCode
from app.core.exceptions import BusinessException
from app.models.app import App
from app.models.user import User
from app.schemas.app import (
    AppAddRequest,
    AppAdminUpdateRequest,
    AppDeployRequest,
    AppQueryRequest,
    AppUpdateRequest,
    AppVO,
    PageAppVO,
)
from app.schemas.user import UserVO
from app.services.user_service import USER_ROLE_ADMIN

GOOD_APP_PRIORITY = 99


class AppService:
    _sortable_fields = {
        "id": App.id,
        "createTime": App.create_time,
        "updateTime": App.update_time,
        "appName": App.app_name,
        "priority": App.priority,
        "deployedTime": App.deployed_time,
    }

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

    async def update_app(self, db: AsyncSession, payload: AppUpdateRequest, login_user: User) -> bool:
        app_id = payload.id or 0
        app_entity = await self.get_app_entity_by_id(db, app_id)
        if app_entity.user_id != login_user.id:
            raise BusinessException(ErrorCode.NO_AUTH_ERROR, "No permission")
        app_name = (payload.app_name or "").strip()
        if app_name:
            app_entity.app_name = app_name[:128]
        await db.commit()
        return True

    async def delete_app(self, db: AsyncSession, app_id: int, login_user: User) -> bool:
        app_entity = await self.get_app_entity_by_id(db, app_id)
        if app_entity.user_id != login_user.id and login_user.user_role != USER_ROLE_ADMIN:
            raise BusinessException(ErrorCode.NO_AUTH_ERROR, "No permission")
        app_entity.is_delete = 1
        await db.commit()
        return True

    async def delete_app_by_admin(self, db: AsyncSession, app_id: int) -> bool:
        app_entity = await self.get_app_entity_by_id(db, app_id)
        app_entity.is_delete = 1
        await db.commit()
        return True

    async def update_app_by_admin(self, db: AsyncSession, payload: AppAdminUpdateRequest) -> bool:
        app_id = payload.id or 0
        app_entity = await self.get_app_entity_by_id(db, app_id)
        if payload.app_name is not None:
            app_name = payload.app_name.strip()
            app_entity.app_name = app_name[:128] if app_name else app_entity.app_name
        if payload.cover is not None:
            app_entity.cover = payload.cover
        if payload.priority is not None:
            app_entity.priority = payload.priority
        await db.commit()
        return True

    async def get_app_vo_by_id(self, db: AsyncSession, app_id: int) -> AppVO:
        app_entity = await self.get_app_entity_by_id(db, app_id)
        user_map = await self._load_user_vo_map(db, [app_entity.user_id])
        return self._to_app_vo(app_entity, user_map.get(app_entity.user_id))

    async def list_my_app_vo_by_page(
        self, db: AsyncSession, payload: AppQueryRequest, login_user: User
    ) -> PageAppVO:
        payload.user_id = login_user.id
        return await self._list_app_vo_by_page(db, payload, max_page_size=20)

    async def list_good_app_vo_by_page(self, db: AsyncSession, payload: AppQueryRequest) -> PageAppVO:
        payload.priority = GOOD_APP_PRIORITY
        return await self._list_app_vo_by_page(db, payload, max_page_size=20)

    async def list_app_vo_by_page_by_admin(self, db: AsyncSession, payload: AppQueryRequest) -> PageAppVO:
        return await self._list_app_vo_by_page(db, payload, max_page_size=100)

    async def deploy_app(
        self,
        db: AsyncSession,
        payload: AppDeployRequest,
        login_user: User,
        generated_root: Path,
        deploy_domain: str,
    ) -> str:
        app_id = payload.app_id or 0
        app_entity = await self.get_app_entity_by_id(db, app_id)
        if app_entity.user_id != login_user.id:
            raise BusinessException(ErrorCode.NO_AUTH_ERROR, "No permission")

        source_dir_name = f"{app_entity.code_gen_type}_{app_entity.id}"
        source_dir = generated_root / source_dir_name
        if not source_dir.exists() or not source_dir.is_dir():
            raise BusinessException(ErrorCode.NOT_FOUND_ERROR, "Generated code not found, please generate first")

        deploy_key = source_dir_name
        app_entity.deploy_key = deploy_key
        app_entity.deployed_time = datetime.now(UTC)
        await db.commit()
        return f"{deploy_domain.rstrip('/')}/{deploy_key}/"

    async def build_download_zip_bytes(self, db: AsyncSession, app_id: int, login_user: User, generated_root: Path) -> bytes:
        app_entity = await self.get_app_entity_by_id(db, app_id)
        if app_entity.user_id != login_user.id:
            raise BusinessException(ErrorCode.NO_AUTH_ERROR, "No permission")

        source_dir = generated_root / f"{app_entity.code_gen_type}_{app_entity.id}"
        if not source_dir.exists() or not source_dir.is_dir():
            raise BusinessException(ErrorCode.NOT_FOUND_ERROR, "Generated code not found, please generate first")
        return self._zip_directory_to_bytes(source_dir)

    async def get_app_entity_by_id(self, db: AsyncSession, app_id: int) -> App:
        if app_id <= 0:
            raise BusinessException(ErrorCode.PARAMS_ERROR, "Invalid app id")
        app_entity = await db.scalar(select(App).where(App.id == app_id, App.is_delete == 0).limit(1))
        if app_entity is None:
            raise BusinessException(ErrorCode.NOT_FOUND_ERROR, "App not found")
        return app_entity

    async def _list_app_vo_by_page(
        self,
        db: AsyncSession,
        payload: AppQueryRequest,
        max_page_size: int,
    ) -> PageAppVO:
        page_num = payload.page_num or 1
        page_size = payload.page_size or 10
        if page_num <= 0:
            page_num = 1
        if page_size <= 0:
            page_size = 10
        page_size = min(page_size, max_page_size)

        filters = [App.is_delete == 0]
        if payload.id and payload.id > 0:
            filters.append(App.id == payload.id)
        if payload.app_name:
            filters.append(App.app_name.like(f"%{payload.app_name.strip()}%"))
        if payload.cover:
            filters.append(App.cover.like(f"%{payload.cover.strip()}%"))
        if payload.init_prompt:
            filters.append(App.init_prompt.like(f"%{payload.init_prompt.strip()}%"))
        if payload.code_gen_type:
            filters.append(App.code_gen_type == payload.code_gen_type.strip())
        if payload.deploy_key:
            filters.append(App.deploy_key == payload.deploy_key.strip())
        if payload.priority is not None:
            filters.append(App.priority == payload.priority)
        if payload.user_id and payload.user_id > 0:
            filters.append(App.user_id == payload.user_id)

        query_stmt = select(App).where(*filters)
        count_stmt = select(func.count(App.id)).where(*filters)

        sort_column = self._sortable_fields.get(payload.sort_field or "")
        sort_order = (payload.sort_order or "").lower()
        if sort_column is not None:
            order_by = desc(sort_column) if "desc" in sort_order else asc(sort_column)
            query_stmt = query_stmt.order_by(order_by)
        else:
            query_stmt = query_stmt.order_by(desc(App.id))

        offset = (page_num - 1) * page_size
        apps = (await db.scalars(query_stmt.offset(offset).limit(page_size))).all()
        total_row = int(await db.scalar(count_stmt) or 0)
        total_page = ceil(total_row / page_size) if total_row > 0 else 0

        user_ids = [app.user_id for app in apps]
        user_map = await self._load_user_vo_map(db, user_ids)
        records = [self._to_app_vo(item, user_map.get(item.user_id)) for item in apps]

        return PageAppVO(
            records=records,
            page_number=page_num,
            page_size=page_size,
            total_page=total_page,
            total_row=total_row,
            optimize_count_query=True,
        )

    async def _load_user_vo_map(self, db: AsyncSession, user_ids: list[int]) -> dict[int, UserVO]:
        clean_user_ids = sorted({item for item in user_ids if item > 0})
        if not clean_user_ids:
            return {}
        users = (
            await db.scalars(select(User).where(User.id.in_(clean_user_ids), User.is_delete == 0))
        ).all()
        return {item.id: self._to_user_vo(item) for item in users}

    @staticmethod
    def _to_user_vo(user: User) -> UserVO:
        return UserVO(
            id=user.id,
            user_account=user.user_account,
            user_name=user.user_name,
            user_avatar=user.user_avatar,
            user_profile=user.user_profile,
            user_role=user.user_role,
            create_time=user.create_time,
        )

    @staticmethod
    def _to_app_vo(app_entity: App, user_vo: UserVO | None) -> AppVO:
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

    @staticmethod
    def _build_app_name(init_prompt: str | None) -> str:
        if not init_prompt:
            return "My App"
        name = init_prompt.strip().replace("\n", " ")
        if not name:
            return "My App"
        return name[:32]

    @staticmethod
    def _zip_directory_to_bytes(source_dir: Path) -> bytes:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for path in source_dir.rglob("*"):
                if path.is_file():
                    arc_name = path.relative_to(source_dir).as_posix()
                    zip_file.write(path, arcname=arc_name)
        return zip_buffer.getvalue()
