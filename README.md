# Python AI Mother

`python-ai-mother` 是对 `yu-ai-code-mother` 的 Python 技术栈重构项目。

## 当前进度
- M00：已完成并合并 `master`
- M01：开发完成，待按流程拆分提交并验收合并

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

## 开发流程
- 所有开发必须在临时分支进行
- 验收通过后再合并 `master`
- commit 描述与 `CHANGELOGS.md` 统一使用中文
