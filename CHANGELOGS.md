# 变更日志（CHANGELOGS）

本文件记录项目的重要变更，统一使用中文维护。

## 维护规范
- 开发中变更先写入 `进行中`。
- 验收通过并合并到 `master` 后，将条目归档到对应日期。
- 每条记录建议附带提交哈希，便于追踪。

## 进行中
- M00：初始化 FastAPI 单体后端骨架（`backend/monolith/app`、`backend/monolith/tests`）。
- M00：新增统一响应模型、错误码定义、业务异常与全局异常处理。
- M00：新增健康检查接口 `GET /api/health/`。
- M00：补充日志中间件、CORS 配置、资源管理器（SQLAlchemy/Redis 初始化骨架）。
- M00：补充 `.env.example` 与 `backend/monolith/README.md`。
- M00：扩展测试覆盖参数校验与业务异常处理，并通过 `uv run pytest`（3 passed）。
- 规范升级：强制“临时分支开发 -> 验收通过 -> 合并 master”流程。
- 规范升级：提交说明使用中文描述。

## 2026-02-26

### 新增
- 初始化仓库，新增基础文档与重构计划初版。
  - `aaa357a` `docs: initialize python-ai-mother with refactor plan`
- 新增变更日志文件并写入初始历史。
  - `a3ad0e5` `docs: add CHANGELOGS.md with initial history`
- 新增 M00 开工清单。
  - `4d26bab` `docs(m00): 完成计划终检并新增开工清单`

### 变更
- 强制项目内 Python 虚拟环境策略，统一使用 `uv`。
  - `83fb120` `docs: enforce project-local env policy with uv`
- 优化重构路线，按 `yu-ai-code-mother` 历史里程碑对齐。
  - `8f9bded` `docs: optimize refactor roadmap aligned to yu-ai git milestones`
- 固化分支流程规范，并将重构计划与日志改为中文维护。
  - `62a9cc7` `docs: 规范分支流程并改为中文提交与日志`
