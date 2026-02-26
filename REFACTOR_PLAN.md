# Python AI Mother 重构计划（基于 yu-ai-code-mother 提交历史）

## 1. 目标与边界
- 目标：在 `python-ai-mother` 中重建一个与 `yu-ai-code-mother` 功能等价的项目。
- 约束：前端技术栈保持不变（Vue3 + TS + Vite + Ant Design Vue）。
- 约束：后端全部由 Java 迁移为 Python 技术栈。
- 策略：严格按原项目 Git 历史的功能演进顺序推进，先单体，后微服务。

## 2. 当前状态
- 已完成：创建目录 `python-ai-mother`。
- 已完成：初始化 Git 仓库。
- 待完成：项目骨架、重构实现、测试、部署、可观测性、微服务化。

## 3. 后端技术栈替换矩阵（Java -> Python）
- Spring Boot Web -> FastAPI
- MyBatis-Flex -> SQLAlchemy 2.x + Alembic
- Spring Validation -> Pydantic v2
- Spring Session + Redis -> Redis Session（自定义中间件 / fastapi-sessions）
- AOP + Interceptor -> FastAPI Middleware + Dependency + Decorator
- Knife4j / OpenAPI -> FastAPI OpenAPI + Swagger UI
- LangChain4j -> LangChain Python
- LangGraph4j -> LangGraph Python
- Redisson 限流 -> Redis + slowapi（或自定义令牌桶）
- Actuator + Micrometer -> Prometheus FastAPI Instrumentator + OpenTelemetry
- Dubbo + Nacos -> gRPC/HTTP + Nacos（Python SDK）服务注册发现

## 4. 目录规划（目标形态）
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
  frontend/                # 基于原前端技术栈复用
  deploy/
    docker/
    k8s/
  docs/
    architecture/
    api/
    runbooks/
```

## 5. 重构顺序（严格映射 yu-ai 提交历史）

### Phase 00：项目初始化（对应 67a0407, 93a80d4, 33d879a, ba30735, aadf53e）
- 目标：Python 后端与前端工程骨架建立完成。
- 后端任务：
  - 初始化 FastAPI 项目结构。
  - 配置 SQLAlchemy、Alembic、Redis 客户端、日志模块。
  - 建立统一响应格式、异常基类、错误码体系。
  - 建立基础中间件（CORS、请求日志、异常处理）。
- 前端任务：
  - 拷贝并验证原前端可运行。
  - 将 API 基础地址改为 Python 后端。
- 验收：
  - 健康接口可访问。
  - 前后端基本联通。

### Phase 01：用户模块（对应 c96ffa8, d52f335, 55ab6c7）
- 目标：实现用户注册、登录、获取登录态、退出登录。
- 后端任务：
  - User 表模型、DAO、Service、Router。
  - 密码加密、会话写入 Redis。
  - 管理员角色与基础权限判断。
- 前端任务：
  - 登录页、注册页、登录态存储、路由守卫联调。
- 验收：
  - 注册/登录/退出全链路可用。
  - 未登录访问受限接口返回正确错误码。

### Phase 02：AI 应用生成初版（对应 2f783b3, 6c38f1d）
- 目标：实现 AI 生成基础能力。
- 后端任务：
  - 接入 LLM（OpenAI 兼容接口）。
  - 设计 Prompt 模板加载机制。
  - 初版代码解析与保存逻辑。
- 验收：
  - 可根据简单提示词返回可用生成结果。

### Phase 03：应用模块与部署流程（对应 868c65b, 9112c1f, e05b173, 44f81d6, fc48d1e, 81eeda3）
- 目标：应用 CRUD、应用生成、应用部署闭环。
- 后端任务：
  - App 表模型、CRUD API、分页查询。
  - 应用生成接口与部署接口。
  - 静态资源访问与下载入口。
- 前端任务：
  - 首页、应用管理、应用编辑、应用详情联调。
- 验收：
  - 完整应用管理流程可演示。

### Phase 04：对话历史与会话增强（对应 092f62f, bc7aaac, 55a5613, 3818b73, 94fdc9a）
- 目标：对话记录持久化，Redis Session 稳定运行。
- 后端任务：
  - ChatHistory 表模型、写入与分页查询。
  - AI 对话记忆持久化策略。
- 前端任务：
  - 对话历史展示与回放。
- 验收：
  - 对话上下文可持续。
  - 刷新后历史可见。

### Phase 05：工程级项目生成（对应 19b1bcd, 1695a3a, 845a82c, 76df070）
- 目标：支持工程模式生成与流式工具调用。
- 后端任务：
  - 工程模板生成器。
  - 工具调用执行器（读写改删文件）。
  - SSE 流式输出协议。
- 前端任务：
  - 工程模式聊天页联调，流式展示消息。
- 验收：
  - 可生成多文件工程并实时输出过程。

### Phase 06：功能扩展（对应 6519021, 499312b, 695d809）
- 目标：截图、打包下载、AI 路由。
- 后端任务：
  - Screenshot 服务（Playwright 优先）。
  - 项目打包下载。
  - 多模型路由策略。
- 验收：
  - 一键截图可用。
  - 打包下载可用。

### Phase 07：可视化修改（对应 cce4ad1, e05c04c, 89c7725）
- 目标：可视化编辑（全量与增量模式）。
- 后端任务：
  - 增量修改与全量重写接口。
  - 文件差异检测与安全回滚。
- 前端任务：
  - 可视化编辑交互联调。
- 验收：
  - 同一应用可执行全量和增量两种修改。

### Phase 08：AI 工作流（对应 f69f244, c755246, cd25d72, 1ac37d8, 62b5655, 5dd51f0, c55d713）
- 目标：基于 LangGraph Python 实现工作流编排。
- 后端任务：
  - Router / PromptEnhancer / CodeGenerator / QualityCheck 节点。
  - 图片并发收集子图。
  - 工作流状态管理与可观测日志。
- 验收：
  - 工作流生成链路可运行并可追踪节点执行。

### Phase 09：系统优化（对应 08cb772, 1939024, 2d32bb4, 566d530, 3e71e72, 5d45f3a, b99d502）
- 目标：并发、缓存、实时性、安全性、稳定性、成本优化。
- 后端任务：
  - AI 调用并发控制。
  - Redis + 本地缓存策略。
  - 限流、Prompt 安全审查、重试与熔断。
  - 成本控制（token 配额、低成本模型路由）。
- 验收：
  - 压测指标优于 Phase 08 基线。
  - 关键安全策略可验证。

### Phase 10：部署与可观测性（对应 ad303cc, 18c86bc）
- 目标：可部署、可监控、可告警。
- 任务：
  - Docker Compose 部署单体版本。
  - Prometheus + Grafana 指标接入。
  - 关键业务指标（QPS、耗时、模型调用次数、失败率）上报。
- 验收：
  - 一键部署可运行。
  - 监控面板可观察核心指标。

### Phase 11：微服务改造（对应 9211e98 -> 893918c）
- 目标：完成 Python 微服务化，顺序必须与原项目一致。
- 顺序与任务：
  - 11.1 通用模块：common（配置、异常、工具、中间件）。
  - 11.2 数据模型模块：model（实体、DTO、VO、枚举）。
  - 11.3 服务接口模块：client（内部服务协议定义）。
  - 11.4 用户服务：user-service（认证鉴权、用户管理）。
  - 11.5 AI 服务：ai-service（模型、Prompt、工作流、工具调用）。
  - 11.6 应用服务：app-service（业务聚合、编排、静态资源）。
  - 11.7 截图服务：screenshot-service。
  - 11.8 跨服务调用：服务注册发现 + 服务间协议（gRPC/HTTP）。
  - 11.9 微服务收敛：完成单体兼容与微服务双形态。
- 验收：
  - 服务独立可启动。
  - 跨服务调用链路稳定。
  - 与单体功能等价。

## 6. 提交与分支策略（按阶段小步快跑）
- 分支命名：`temp/py-refactor-phase-{nn}-{date}`
- 每个 Phase 至少拆成 2~5 个原子提交。
- 提交信息模板：
  - `feat(phase-xx): {功能点}`
  - `fix(phase-xx): {问题修复}`
  - `test(phase-xx): {测试补充}`
- 每个提交必须附带本地验证记录（接口/测试/截图）。

## 7. 测试策略
- 单元测试：`pytest` + `pytest-asyncio`
- 接口测试：`httpx` / `pytest` 集成测试
- 前端联调：保持原有 `npm run build` / `npm run lint` 校验
- E2E（后期）：Playwright
- 阶段门禁：每个 Phase 完成后至少通过一次回归测试清单

## 8. 关键风险与回滚方案
- 风险：一次性替换全部后端导致联调中断。
  - 方案：先构建 Python 单体等价版本，再拆微服务。
- 风险：AI 工作流迁移复杂，行为不一致。
  - 方案：先保留“简化工作流”可运行版本，再逐步对齐高级特性。
- 风险：跨服务协议与发现机制不稳定。
  - 方案：先 HTTP 内部调用，稳定后升级 gRPC + 注册发现。
- 风险：前端改动过大影响节奏。
  - 方案：前端只做必要 API 适配，不做风格重构。

## 9. 第一阶段（下一步要做）
- [ ] 建立 `backend/monolith` FastAPI 骨架。
- [ ] 建立基础配置加载与日志体系。
- [ ] 落地统一响应与错误码。
- [ ] 提供 `/health` 接口并完成前端连通测试。
- [ ] 生成 Phase 00 的第一批提交。

