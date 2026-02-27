# 变更日志（CHANGELOGS）

本文件记录项目的重要变更，统一使用中文维护。

## 维护规范
- 开发中变更先写入 `进行中`。
- 验收通过并合并到 `master` 后，将条目归档到对应日期。
- 每条记录建议附带提交哈希，便于追踪。

## 进行中
- M05 启动：进入工程项目生成阶段开发（对标 `19b1bcd`、`1695a3a`、`845a82c`、`76df070`）。
- M05 目标：多文件工程生成、工具调用流式输出、工程浏览部署与前端对接。
- M05 已创建开工清单：`M05_START_CHECKLIST.md`。

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

### M04 收尾归档
- M04 对话历史与会话增强完成，范围对齐 `092f62f`、`bc7aaac`、`55a5613`、`3818b73`、`94fdc9a`。
- 已完成能力：
  - 新增 `chat_history` 模型、迁移、服务和接口，支持按应用查询历史与管理员分页检索
  - 打通 `GET /api/chatHistory/app/{appId}` 与 `POST /api/chatHistory/admin/list/page/vo`
  - `GET /api/app/chat/gen/code` 生成链路接入 user / assistant 消息持久化
  - 前端对话页支持历史加载、游标分页与只读模式文案优化
- 已完成验证：
  - 数据迁移：`uv run alembic upgrade head` 通过
  - 自动化测试：`uv run pytest -q -p no:faulthandler` 通过（`18 passed`）
  - 前端构建：`npm run build` 通过
- 相关提交：
  - `648364b` `docs(m04): 完成开工准备与清单初始化`
  - `132d70d` `feat(m04): 完成对话历史模块与生成链路持久化`
  - `33ca8a9` `docs(m04): 完成清单收尾并优化只读文案`
- M04 已按流程合并到 `master`。
  - `74e635d` `merge(m04): 合并对话历史与会话增强重构成果`

### M03 收尾归档
- M03 应用模块与部署完成，范围对齐 `868c65b`、`9112c1f`、`e05b173`、`44f81d6`、`fc48d1e`、`81eeda3`。
- 已完成能力：
  - 应用 CRUD、分页查询、管理员应用接口
  - 应用部署（`deployKey` / `deployedTime`）、静态访问、下载
  - 前端默认部署地址适配，作品可直接访问
- 已完成验证：
  - 自动化测试：`uv run pytest -q -p no:faulthandler` 通过（`16 passed`）
  - 前端构建：`npm run build` 通过
  - 端到端 smoke：注册登录 -> 创建应用 -> AI 生成 -> 部署 -> 静态访问 -> 下载
- 相关提交：
  - `cb6f90f` `docs(m03): 完成开工准备与清单初始化`
  - `79d85d0` `feat(m03): 补齐应用模块CRUD分页与部署下载接口`
  - `7d8adb0` `test(m03): 增加应用模块接口集成测试`
  - `03bb2ab` `docs(m03): 更新阶段进展与验收清单`
  - `0535307` `feat(m03): 适配前端默认部署地址到静态资源`
  - `4c52baf` `test(m03): 修复测试配置污染并增加静态访问断言`
  - `9eff615` `docs(m03): 更新对标进度与端到端演示记录`
- M03 已按流程合并到 `master`。
  - `4454c50` `merge(m03): 合并应用模块与部署重构成果`

### M02 收尾归档
- M02 AI 应用生成初版完成，范围对齐 `2f783b3`、`6c38f1d`。
- 已完成能力：
  - 模型接入、Prompt 加载、最小生成链路
  - `POST /api/app/add`、`GET /api/app/get/vo`、`GET /api/app/chat/gen/code`（SSE）
  - 解析器执行器化、保存器执行器化、通用 SSE 事件构建
- 已完成验证：
  - 自动化测试：`uv run pytest -q -p no:faulthandler` 通过
  - 前端构建：`npm run build` 通过
  - 非 mock 联调：真实模型请求可返回并成功落盘生成文件
- 相关提交：
  - `b626004` `docs(m02): 完成开工准备与清单初始化`
  - `c25a3b7` `feat(m02): 打通应用生成主链路并完成执行器化重构`
  - `cac41e8` `test(m02): 增加应用生成链路与SSE测试`
  - `48a4d39` `docs(m02): 更新清单日志与模型配置说明`
  - `50a25e6` `chore(test): 兼容Windows测试输出并禁用faulthandler`
- M02 已按流程合并到 `master`。
  - `d8dc16c` `merge(m02): 合并AI应用生成初版重构成果`

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

