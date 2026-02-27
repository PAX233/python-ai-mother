# Python AI Mother

`python-ai-mother` 是对 `yu-ai-code-mother` 的 Python 技术栈重构项目。

## 当前进度
- M00：已完成并合并 `master`
- M01：已完成并合并 `master`
- M02：已完成并合并 `master`
- M03：已完成并合并 `master`
- M04：已完成并合并 `master`
- M05：已完成并合并 `master`
- M06：已完成并合并 `master`
- M07：已完成并合并 `master`
- M08：已完成并合并 `master`

## 目录结构

```text
python-ai-mother/
  backend/monolith/
  frontend/
  docs/
  REFACTOR_PLAN.md
  CHANGELOGS.md
```

## 本地启动

### 后端

```powershell
cd backend/monolith
uv venv .venv
uv pip install -r requirements.txt
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8123
```

### 前端

```powershell
cd frontend
npm ci
npm run dev
```

## 联调检查
- 前端地址：`http://localhost:5173`
- 后端健康接口：`http://localhost:8123/api/health/`
- 代理健康接口：`http://localhost:5173/api/health/`
- M02 应用接口：
  - `POST /api/app/add`
  - `GET /api/app/get/vo?id={appId}`
  - `GET /api/app/chat/gen/code?appId={appId}&message=...`（SSE）

## 模型配置（运行时注入）

不要将真实 `api_key` 写入 Git 文件。建议仅在当前终端会话临时设置：

```powershell
$env:LLM_BASE_URL="https://api.ikuncode.cc/v1"
$env:LLM_API_KEY="<你的密钥>"
$env:LLM_MODEL_NAME="gpt-5.1-codex-mini"
$env:LLM_STREAM="true"
$env:LLM_TIMEOUT_SECONDS="180"
```

## 开发流程
- 所有开发必须在临时分支进行
- 验收通过后再合并 `master`
- commit 描述与 `CHANGELOGS.md` 统一使用中文
