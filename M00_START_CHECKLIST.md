# M00 开工清单（启动 FastAPI 单体骨架）

## 1. 分支与流程检查
- [ ] 当前分支为临时分支（非 `master`）
- [ ] 分支命名符合：`temp/m00-yyyymmdd-主题`
- [ ] `REFACTOR_PLAN.md` 与 `CHANGELOGS.md` 已同步最新规则

## 2. 环境检查（项目内虚拟环境）
- [ ] `.venv/` 已存在（`uv venv .venv`）
- [ ] 使用 `uv run` 执行命令，不使用全局 `python/pip`
- [ ] Node 版本固定（如需要联调前端）

## 3. M00 目录初始化
- [ ] 创建 `backend/monolith/app/main.py`
- [ ] 创建 `backend/monolith/app/core/`（配置、日志、错误码、统一响应）
- [ ] 创建 `backend/monolith/tests/`（至少 1 个 smoke test）
- [ ] 创建 `backend/monolith/requirements.txt`

## 4. M00 功能目标
- [ ] 提供 `GET /health` 健康接口
- [ ] 统一错误码与统一响应结构
- [ ] 全局异常处理可用
- [ ] 前端可访问健康接口（或本地 curl 验证）

## 5. M00 验收门禁（通过后才可申请合并）
- [ ] `uv run pytest` 通过
- [ ] `GET /health` 返回成功
- [ ] 更新 `CHANGELOGS.md` 的 `进行中`
- [ ] 提交信息使用中文

## 6. 推荐提交拆分（中文提交）
1. `feat(m00): 初始化FastAPI单体目录结构`
2. `feat(m00): 增加统一响应与错误码处理`
3. `feat(m00): 新增健康检查接口与基础测试`
4. `docs(m00): 更新变更日志与启动清单`

