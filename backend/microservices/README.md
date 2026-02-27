# backend/microservices

## 1. 服务划分（M11）
- `common`：统一响应与错误码
- `model`：跨服务模型定义
- `client`：跨服务调用客户端
- `user-service`：注册/登录/会话校验
- `ai-service`：代码生成服务
- `app-service`：应用聚合服务（含用户透传接口）
- `screenshot-service`：截图服务

## 2. 本地启动（项目内 uv）
```bash
cd backend/microservices
uv pip install -r requirements.txt
```

分别启动：
```bash
uv run uvicorn user-service.app.main:app --host 0.0.0.0 --port 8201
uv run uvicorn ai-service.app.main:app --host 0.0.0.0 --port 8202
uv run uvicorn app-service.app.main:app --host 0.0.0.0 --port 8203
uv run uvicorn screenshot-service.app.main:app --host 0.0.0.0 --port 8204
```

## 3. 微服务编排
- 使用：`deploy/docker/docker-compose.microservices.yml`
- 聚合入口：`app-service`（`http://localhost:8203`）
