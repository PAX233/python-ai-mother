import asyncio

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.core.error_codes import ErrorCode
from app.core.security import hash_password
from app.db.base import metadata
from app.main import app
from app.models import User  # noqa: F401


class FakeRedis:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def setex(self, key: str, _: int, value: str) -> bool:
        self.store[key] = value
        return True

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def delete(self, key: str) -> int:
        return 1 if self.store.pop(key, None) is not None else 0

    async def aclose(self) -> None:
        return None


def _reset_user_table() -> None:
    async def _run() -> None:
        engine = app.state.resources.engine
        if engine is None:
            raise RuntimeError("database engine is not initialized")
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: metadata.drop_all(sync_conn, tables=[User.__table__]))
            await conn.run_sync(lambda sync_conn: metadata.create_all(sync_conn, tables=[User.__table__]))

    asyncio.run(_run())


def _drop_user_table() -> None:
    async def _run() -> None:
        engine = app.state.resources.engine
        if engine is None:
            return
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: metadata.drop_all(sync_conn, tables=[User.__table__]))

    asyncio.run(_run())


def _seed_admin_user(account: str = "admin_root", password: str = "adminPass123") -> None:
    async def _run() -> None:
        session_factory = app.state.resources.session_factory
        if session_factory is None:
            raise RuntimeError("session factory is not initialized")
        settings = get_settings()
        async with session_factory() as session:
            user = User(
                user_account=account,
                user_password=hash_password(password, settings.password_salt),
                user_name="admin",
                user_role="admin",
            )
            session.add(user)
            await session.commit()

    asyncio.run(_run())


def _login(client: TestClient, account: str, password: str) -> None:
    response = client.post(
        "/api/user/login",
        json={"userAccount": account, "userPassword": password},
    )
    assert response.status_code == 200
    assert response.json()["code"] == int(ErrorCode.SUCCESS)


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        app.state.resources.redis_client = FakeRedis()
        _reset_user_table()
        yield test_client
        _drop_user_table()


def test_user_register_login_logout_flow(client: TestClient) -> None:
    register_payload = {
        "userAccount": "demo_user",
        "userPassword": "strongPass123",
        "checkPassword": "strongPass123",
    }
    register_response = client.post("/api/user/register", json=register_payload)
    assert register_response.status_code == 200
    register_body = register_response.json()
    assert register_body["code"] == int(ErrorCode.SUCCESS)
    assert isinstance(register_body["data"], int)

    login_response = client.post(
        "/api/user/login",
        json={"userAccount": "demo_user", "userPassword": "strongPass123"},
    )
    assert login_response.status_code == 200
    login_body = login_response.json()
    assert login_body["code"] == int(ErrorCode.SUCCESS)
    assert login_body["data"]["userAccount"] == "demo_user"
    assert "set-cookie" in login_response.headers

    current_response = client.get("/api/user/get/login")
    assert current_response.status_code == 200
    current_body = current_response.json()
    assert current_body["code"] == int(ErrorCode.SUCCESS)
    assert current_body["data"]["userAccount"] == "demo_user"

    logout_response = client.post("/api/user/logout")
    assert logout_response.status_code == 200
    logout_body = logout_response.json()
    assert logout_body["code"] == int(ErrorCode.SUCCESS)
    assert logout_body["data"] is True

    after_logout_response = client.get("/api/user/get/login")
    after_logout_body = after_logout_response.json()
    assert after_logout_response.status_code == 200
    assert after_logout_body["code"] == int(ErrorCode.NOT_LOGIN_ERROR)


def test_user_login_with_invalid_password(client: TestClient) -> None:
    client.post(
        "/api/user/register",
        json={
            "userAccount": "another_user",
            "userPassword": "strongPass123",
            "checkPassword": "strongPass123",
        },
    )
    response = client.post(
        "/api/user/login",
        json={"userAccount": "another_user", "userPassword": "wrong_password"},
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["code"] == int(ErrorCode.PARAMS_ERROR)


def test_user_get_login_without_session(client: TestClient) -> None:
    response = client.get("/api/user/get/login")
    payload = response.json()
    assert response.status_code == 200
    assert payload["code"] == int(ErrorCode.NOT_LOGIN_ERROR)


def test_admin_crud_and_page_flow(client: TestClient) -> None:
    _seed_admin_user()
    _login(client, "admin_root", "adminPass123")

    add_response = client.post(
        "/api/user/add",
        json={
            "userAccount": "managed_user",
            "userName": "Managed User",
            "userRole": "user",
        },
    )
    assert add_response.status_code == 200
    add_payload = add_response.json()
    assert add_payload["code"] == int(ErrorCode.SUCCESS)
    managed_user_id = add_payload["data"]
    assert isinstance(managed_user_id, int)

    get_response = client.get("/api/user/get", params={"id": managed_user_id})
    get_payload = get_response.json()
    assert get_response.status_code == 200
    assert get_payload["code"] == int(ErrorCode.SUCCESS)
    assert get_payload["data"]["userAccount"] == "managed_user"

    get_vo_response = client.get("/api/user/get/vo", params={"id": managed_user_id})
    get_vo_payload = get_vo_response.json()
    assert get_vo_response.status_code == 200
    assert get_vo_payload["code"] == int(ErrorCode.SUCCESS)
    assert get_vo_payload["data"]["userAccount"] == "managed_user"

    update_response = client.post(
        "/api/user/update",
        json={"id": managed_user_id, "userName": "Managed User v2", "userRole": "admin"},
    )
    update_payload = update_response.json()
    assert update_response.status_code == 200
    assert update_payload["code"] == int(ErrorCode.SUCCESS)
    assert update_payload["data"] is True

    list_response = client.post(
        "/api/user/list/page/vo",
        json={"pageNum": 1, "pageSize": 10, "userAccount": "managed"},
    )
    list_payload = list_response.json()
    assert list_response.status_code == 200
    assert list_payload["code"] == int(ErrorCode.SUCCESS)
    assert list_payload["data"]["totalRow"] >= 1
    assert len(list_payload["data"]["records"]) >= 1

    delete_response = client.post("/api/user/delete", json={"id": managed_user_id})
    delete_payload = delete_response.json()
    assert delete_response.status_code == 200
    assert delete_payload["code"] == int(ErrorCode.SUCCESS)
    assert delete_payload["data"] is True

    after_delete_response = client.get("/api/user/get", params={"id": managed_user_id})
    after_delete_payload = after_delete_response.json()
    assert after_delete_response.status_code == 200
    assert after_delete_payload["code"] == int(ErrorCode.NOT_FOUND_ERROR)


def test_admin_api_requires_admin_role(client: TestClient) -> None:
    client.post(
        "/api/user/register",
        json={
            "userAccount": "normal_user",
            "userPassword": "normalPass123",
            "checkPassword": "normalPass123",
        },
    )
    _login(client, "normal_user", "normalPass123")

    response = client.post(
        "/api/user/list/page/vo",
        json={"pageNum": 1, "pageSize": 10},
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["code"] == int(ErrorCode.NO_AUTH_ERROR)
