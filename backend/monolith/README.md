# backend/monolith

## 本地运行

```bash
uv pip install -r requirements.txt
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8123
```

## 测试

```bash
uv run pytest -q
```

