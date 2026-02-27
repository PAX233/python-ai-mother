# 变更日志（CHANGELOGS）

本文件记录项目的重要变更，统一使用中文维护。

## 维护规范
- 开发中变更先写入 `进行中`。
- 验收通过并合并到 `master` 后，将条目归档到对应日期。
- 每条记录建议附带提交哈希，便于追踪。

## 进行中
- M01 启动：进入用户模块开发（对标 `c96ffa8`、`d52f335`、`55ab6c7`）。
- M01 目标：注册、登录、登录态、登出、基础权限与 Redis Session。
- M01 已创建开工清单：`M01_START_CHECKLIST.md`。

## 2026-02-27

### 新增
- 引入前端工程到 `frontend/`，保持原技术栈。
  - `7909720` `feat(m00): 引入前端工程并完成baseURL适配`
- 新增仓库根 README，补齐项目入口说明。
  - `68150ce` `docs(m00): 补充仓库根README说明`
- 新增 M00 验收记录与前端 baseURL 适配记录。
  - `c90553b` `docs(m00): 完成验收记录并准备提合并`
  - `d8dd299` `docs(m00): 更新前端联通验收与清单状态`

### 变更
- M00 阶段已完成并合并到 `master`。
  - `202d2ce` `feat(m00): 完成初始化与基础依赖阶段`

## 2026-02-26

### 新增
- 初始化仓库，新增基础文档与重构计划初版。
  - `aaa357a` `docs: initialize python-ai-mother with refactor plan`
- 新增变更日志文件并写入初始历史。
  - `a3ad0e5` `docs: add CHANGELOGS.md with initial history`
- 新增 M00 开工清单。
  - `4d26bab` `docs(m00): 完成计划终检并新增开工清单`
- 初始化 FastAPI 单体骨架与健康检查。
  - `858063e` `feat(m00): 初始化FastAPI单体骨架与健康检查`
- 增加中间件、资源管理器、Alembic 骨架和开发脚本。
  - `00488ad` `feat(m00): 补充中间件与资源管理骨架`
  - `898b17b` `feat(m00): 增加迁移骨架与开发脚本`

### 变更
- 强制项目内 Python 虚拟环境策略，统一使用 `uv`。
  - `83fb120` `docs: enforce project-local env policy with uv`
- 优化重构路线，按 `yu-ai-code-mother` 历史里程碑对齐。
  - `8f9bded` `docs: optimize refactor roadmap aligned to yu-ai git milestones`
- 固化分支流程规范，并将重构计划与日志改为中文维护。
  - `62a9cc7` `docs: 规范分支流程并改为中文提交与日志`
- 补充统一响应文档、验收清单与日志。
  - `72b9c1e` `docs(m00): 更新进行中日志与开工清单`
  - `e4d0ea5` `docs(m00): 补充统一响应文档与验收清单`


## 2026-02-27（M01 临时分支进展）

### 新增
- 新增用户模块核心能力：注册、登录、登录态、登出（`/api/user/*`）。
- 新增用户领域代码：`app/models/user.py`、`app/schemas/user.py`、`app/services/user_service.py`、`app/services/session_service.py`。
- 新增权限基础能力：`require_role` 依赖与 `GET /api/user/admin/ping` 验证路由。
- 新增用户表迁移脚本：`migrations/versions/20260227_0001_add_user_table.py`。
- 新增用户模块测试：`tests/test_user_auth.py`（注册/登录/登录态/登出/异常场景）。

### 变更
- 扩展后端配置：增加 `password_salt`、session cookie 与 TTL 相关配置。
- `migrations/env.py` 引入模型元数据，保证 Alembic 能识别用户表。

### 验证
- `uv run pytest -q`：通过（6 passed）。
- `uv run alembic upgrade head`、`uv run alembic current`：通过（head=20260227_0001）。
- `npm run build`：通过。

### 待办
- 按规范拆分中文提交信息。
- 分支验收通过后合并到 `master`，并将本段归档为正式发布记录。
