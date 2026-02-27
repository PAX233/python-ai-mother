# 变更日志（CHANGELOGS）

本文件记录项目的重要变更，统一使用中文维护。

## 维护规范
- 开发中变更先写入 `进行中`。
- 验收通过并合并到 `master` 后，将条目归档到对应日期。
- 每条记录建议附带提交哈希，便于追踪。

## 进行中
- M02 启动：进入 AI 应用生成初版开发（对标 `2f783b3`、`6c38f1d`）。
- M02 目标：模型接入、Prompt 加载、代码解析/保存、SSE 流式输出最小链路。
- M02 已创建开工清单：`M02_START_CHECKLIST.md`。
- M02 已完成主链路：`/api/app/add`、`/api/app/get/vo`、`/api/app/chat/gen/code`（SSE）。
- M02 已完成第一轮结构优化：代码解析执行器、文件保存执行器、通用 SSE 事件构建器。
- M02 联调记录：使用真实模型配置完成非 mock 验证，生成文件成功落盘。
- 安全约束：模型 `api_key` 仅通过运行时环境变量注入，不写入仓库文件。

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

### M01 收尾归档
- M01 用户模块与管理员能力已完成，并通过自动化与人工验收。
  - `31dd5c1` `feat(m01): 完成用户注册登录与会话鉴权`
  - `390b1b2` `test(m01): 增加用户模块接口集成测试`
  - `b158be0` `docs(m01): 更新验收清单与阶段文档`
  - `11f54d3` `feat(m01): 补齐管理员用户CRUD与分页接口`
  - `6bcc799` `test(m01): 增加管理员接口权限与分页测试`
  - `291b1a1` `docs(m01): 更新管理员模块对标与验收记录`
- M01 对标结论：`c96ffa8`、`d52f335`、`55ab6c7` 已全部对齐。
- M01 人工测试状态：Postman 全链路通过（用户 + 管理员 + 权限负例）。
- M01 已按流程合并到 `master`。
  - `7cacc86` `merge(m01): 合并用户模块重构成果`

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

