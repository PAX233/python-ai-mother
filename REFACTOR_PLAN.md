# Python AI Mother 重构计划（强对标 yu-ai Git 历史）

## 1. 重构目标
- 在 `python-ai-mother` 中重建与 `yu-ai-code-mother` 等价的产品能力。
- 前端保持原技术栈：Vue3 + TypeScript + Vite + Ant Design Vue。
- 后端完全替换为 Python 技术栈。
- 迭代顺序严格对标原仓库提交演进路径（先单体，后微服务）。

## 2. 环境规范（强制）
- Python 虚拟环境必须在项目内：`.venv/`
- Python 包管理统一使用 `uv`，禁止全局 `pip install`
- 标准命令：
  - `uv venv .venv`
  - `uv pip install -r requirements.txt`
  - `uv run python xxx.py`
  - `uv run pytest`
- Node 版本使用 `nvm` 固定，依赖仅在项目目录安装。

## 3. 后端替换技术栈（Java -> Python）
- Spring Boot -> FastAPI
- MyBatis-Flex -> SQLAlchemy 2.x + Alembic
- Spring Validation -> Pydantic v2
- Spring Session + Redis -> Redis Session Middleware
- AOP/Interceptor -> Middleware + Dependency + Decorator
- LangChain4j -> LangChain Python
- LangGraph4j -> LangGraph Python
- Redisson 限流 -> Redis + slowapi（或自定义令牌桶）
- Actuator/Micrometer -> Prometheus + OpenTelemetry
- Dubbo + Nacos -> gRPC/HTTP + Nacos 注册发现

## 4. 目标目录结构
```text
python-ai-mother/
  backend/
    monolith/
    microservices/
      common/
      model/
      client/
      user-service/
      app-service/
      ai-service/
      screenshot-service/
  frontend/
  deploy/
    docker/
    k8s/
  docs/
    architecture/
    api/
    runbooks/
```

## 5. 对标总览（按 yu-ai 提交顺序）

| 里程碑 | 对标提交 | 核心主题 |
|---|---|---|
| M00 | `67a0407` `93a80d4` `33d879a` `ba30735` `aadf53e` | 初始化与基础依赖 |
| M01 | `c96ffa8` `d52f335` `55ab6c7` | 用户模块 |
| M02 | `2f783b3` `6c38f1d` | AI 应用生成初版 |
| M03 | `868c65b` `9112c1f` `e05b173` `44f81d6` `fc48d1e` `81eeda3` | 应用模块 + 部署 |
| M04 | `092f62f` `bc7aaac` `55a5613` `3818b73` `94fdc9a` | 对话历史 + Redis Session |
| M05 | `19b1bcd` `1695a3a` `845a82c` `76df070` | 工程项目生成 |
| M06 | `6519021` `499312b` `695d809` | 截图 + 打包 + AI 路由 |
| M07 | `cce4ad1` `e05c04c` `89c7725` | 可视化修改 |
| M08 | `f69f244` `c755246` `cd25d72` `1ac37d8` `62b5655` `5dd51f0` `c55d713` | AI 工作流 |
| M09 | `08cb772` `1939024` `2d32bb4` `566d530` `3e71e72` `5d45f3a` `b99d502` | 系统优化 |
| M10 | `ad303cc` `18c86bc` | 部署上线 + 可观测性 |
| M11 | `9211e98` 到 `893918c` | 微服务改造完成 |

## 6. 详细重构计划（逐里程碑）

### M00 初始化与基础依赖（对标第2期）
- 范围：
  - 初始化 FastAPI 单体骨架
  - 接入 SQLAlchemy/Alembic/Redis
  - 建立统一错误码、统一响应、全局异常
  - 前端接入 Python 后端 baseURL
- 交付：
  - `backend/monolith/app/main.py`
  - `backend/monolith/app/core/*`
  - `frontend` 可调用 `GET /health`
- DoD：
  - 健康接口可访问
  - 前后端可联通
  - `uv run pytest` 至少有 smoke test

### M01 用户模块（对标第3期）
- 范围：
  - 用户注册、登录、登出、登录态查询
  - 用户角色（user/admin）基础权限
  - Redis Session 写入与读取
- 交付：
  - `POST /user/register`
  - `POST /user/login`
  - `GET /user/get/login`
  - `POST /user/logout`
- DoD：
  - 四个接口联调通过
  - 未登录访问管理接口返回预期错误码
  - 前端路由守卫行为一致

### M02 AI 应用生成初版（对标第4期）
- 范围：
  - 模型接入与 prompt 加载
  - 简化版代码生成
  - 初版结果落盘
- 交付：
  - AI 生成服务与最小 API
- DoD：
  - 通过提示词返回可用生成结果
  - 异常输入有明确错误处理

### M03 应用模块与部署（对标第5期）
- 范围：
  - 应用 CRUD、分页、详情、编辑
  - 应用生成与部署
  - 静态资源访问和项目下载
- 交付（关键接口）：
  - `POST /app/add`
  - `POST /app/update`
  - `POST /app/delete`
  - `GET /app/get/vo`
  - `POST /app/my/list/page/vo`
  - `POST /app/good/list/page/vo`
  - `POST /app/deploy`
  - `GET /app/download/{appId}`
- DoD：
  - 应用主流程可演示
  - 前端对应页面全联调通过

### M04 对话历史与会话增强（对标第6期）
- 范围：
  - chat_history 持久化
  - 对话历史查询
  - 会话持续性与刷新恢复
- 交付：
  - `GET /chatHistory/app/{appId}`
- DoD：
  - 历史记录可写可查
  - 刷新后可恢复历史

### M05 工程项目生成（对标第7期）
- 范围：
  - 多文件工程生成
  - 工具调用（读写改删）
  - SSE 流式输出
- 交付：
  - `GET /app/chat/gen/code`（SSE）
- DoD：
  - 生成过程可流式展示
  - 工具调用日志可追踪

### M06 功能扩展（对标第8期）
- 范围：
  - 截图服务（推荐 Playwright）
  - 打包下载
  - AI 路由（多模型选择）
- 交付：
  - 截图 API、打包 API、模型路由策略
- DoD：
  - 截图和打包可稳定运行
  - 至少两种模型路由策略可验证

### M07 可视化修改（对标第9期）
- 范围：
  - 全量修改与增量修改接口
  - 变更差异处理与安全回滚
- 交付：
  - 可视化修改相关 API
- DoD：
  - 同一应用支持全量/增量两种改法
  - 回滚能力可演示

### M08 AI 工作流（对标第10期）
- 范围：
  - LangGraph Python 工作流
  - 并发子图（图片收集）
  - 节点执行日志
- 交付：
  - 工作流入口与核心节点（Router/Enhancer/Generator/QualityCheck）
- DoD：
  - 工作流端到端可跑通
  - 节点级日志可追踪

### M09 系统优化（对标第11期）
- 范围：
  - 并发优化、缓存优化、实时性优化
  - 限流、Prompt 安全审查
  - 稳定性与成本优化
- 交付：
  - 限流与审查中间件
  - 缓存策略（Redis + 本地缓存）
- DoD：
  - 压测指标有对比提升
  - 安全策略可验证

### M10 部署与可观测性（对标第12-13期）
- 范围：
  - Docker Compose 部署
  - Prometheus + Grafana
  - 核心指标埋点
- 交付：
  - 可一键启动的部署脚本
  - 仪表盘配置
- DoD：
  - 服务可部署
  - 指标可观测（QPS/延迟/错误率/模型调用）

### M11 微服务改造（对标第14期）
- 说明：原仓库第14期存在多个“中间态提交”，必须整体对标最终态 `893918c`。
- 范围顺序（必须按序）：
  - M11.1 `common`
  - M11.2 `model`
  - M11.3 `client`
  - M11.4 `user-service`
  - M11.5 `ai-service`
  - M11.6 `app-service`
  - M11.7 `screenshot-service`
  - M11.8 跨服务调用（注册发现 + RPC/HTTP）
  - M11.9 微服务完成态收敛
- DoD：
  - 各服务可独立启动
  - 跨服务链路稳定
  - 与单体能力等价

## 7. 接口兼容优先级（先保核心）
- P0（必须首批完成）：
  - `/user/register` `/user/login` `/user/get/login` `/user/logout`
  - `/app/add` `/app/update` `/app/my/list/page/vo` `/app/chat/gen/code`
- P1（第二批完成）：
  - `/app/deploy` `/app/download/{appId}` `/chatHistory/app/{appId}`
- P2（后续扩展）：
  - 管理端接口、工作流演示接口、可视化修改接口

## 8. 分支与提交策略（对标历史的“小步快跑”）
- 分支命名：
  - `temp/py-m{milestone}-{yyyymmdd}`
- 每个里程碑拆 2~6 次提交，不做超大提交。
- 提交信息模板：
  - `feat(mXX): ...`
  - `fix(mXX): ...`
  - `test(mXX): ...`
  - `docs(mXX): ...`
- 每次提交附带最小验证记录（命令 + 结果摘要）。

## 9. 测试门禁（每个里程碑都要过）
- 后端：
  - `uv run pytest`
  - 关键 API 集成测试通过
- 前端：
  - `npm run build`
  - `npm run lint`（如已有规则）
- 联调：
  - 至少 1 条端到端主链路可演示

## 10. 风险与回滚策略
- 风险：后端全量替换导致联调中断
  - 回滚：保持“单体可运行主分支”，微服务在独立分支推进
- 风险：工作流迁移复杂度高
  - 回滚：先交付简化工作流，再逐步补高级节点
- 风险：跨服务协议不稳定
  - 回滚：先内部 HTTP，稳定后再升级 gRPC
- 风险：前端改动膨胀
  - 回滚：前端仅做接口适配，不做无关 UI 重构

## 11. 下一步（立即执行）
- [ ] 建立 `backend/monolith` FastAPI 初始工程
- [ ] 建立基础配置、日志、错误码、统一响应
- [ ] 建立 `/health` 并完成前端连通
- [ ] 提交 `M00` 第 1 批 commit

