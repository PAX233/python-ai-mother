import asyncio

import pytest
from fastapi.testclient import TestClient

from app.core.error_codes import ErrorCode
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
