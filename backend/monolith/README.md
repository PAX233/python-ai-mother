# backend/monolith

## 1. 环境准备（项目内虚拟环境）

```bash
uv venv .venv
uv pip install -r requirements.txt
```

## 2. 数据库迁移

```bash
uv run alembic upgrade head
uv run alembic current
```

## 3. 启动后端

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8123
```

或使用脚本：

```powershell
./scripts/run_dev.ps1
```

## 4. 运行测试

```bash
uv run pytest -q
```

或使用脚本：

```powershell
./scripts/run_test.ps1
```

## 5. M01 用户接口

- `POST /api/user/register`
- `POST /api/user/login`
- `GET /api/user/get/login`
- `POST /api/user/logout`
- `GET /api/user/admin/ping`（admin 权限示例）

统一响应格式：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```
