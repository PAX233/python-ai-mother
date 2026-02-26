# backend/monolith

## 本地运行

```bash
uv pip install -r requirements.txt
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8123
```

或使用脚本：

```powershell
./scripts/run_dev.ps1
```

## 测试

```bash
uv run pytest -q
```

或使用脚本：

```powershell
./scripts/run_test.ps1
```

## 数据库迁移

```bash
uv run alembic revision -m "init"
uv run alembic upgrade head
```
