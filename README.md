# Python AI Mother

`python-ai-mother` 是对 `yu-ai-code-mother` 的 Python 化重构项目。

## 当前进度
- 已完成 M00（初始化与基础依赖）
- 后端：FastAPI 单体骨架 + 健康检查 + 统一响应/异常 + 资源管理骨架
- 前端：保留原技术栈并完成 `/api` 代理与 baseURL 适配

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
uv pip install -r requirements.txt
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
- 前端代理健康接口：`http://localhost:5173/api/health/`

## 开发流程
- 所有开发在临时分支进行
- 验收通过后再合并到 `master`
- 提交信息与变更日志统一中文维护

