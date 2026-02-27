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
uv run pytest -q -p no:faulthandler
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

## 6. M02 应用生成接口

- `POST /api/app/add`
- `GET /api/app/get/vo?id={appId}`
- `GET /api/app/chat/gen/code?appId={appId}&message=...`（SSE）

## 7. M06 扩展接口

- `POST /api/app/route/codegen`
- `POST /api/app/screenshot`
- `GET /api/app/download/project/{appId}`

## 8. 模型环境变量（仅运行时）

不要把真实密钥写入仓库文件（包括 `.env.example`、`README`、提交记录）。

```powershell
$env:LLM_BASE_URL="https://api.ikuncode.cc/v1"
$env:LLM_API_KEY="<你的密钥>"
$env:LLM_MODEL_NAME="gpt-5.1-codex-mini"
$env:LLM_STREAM="true"
$env:LLM_TIMEOUT_SECONDS="180"
```
