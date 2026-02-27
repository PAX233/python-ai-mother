# M10 开工清单（部署与可观测性）

## 1. 分支与流程检查
- [ ] 当前分支为临时分支（非 `master`）
- [ ] 分支命名符合：`temp/m10-yyyymmdd-主题`
- [ ] `REFACTOR_PLAN.md` 与 `CHANGELOGS.md` 已切换到 M10 进行中

## 2. M10 对标范围（对标第 12-13 期）
- [ ] Docker Compose 一键启动（前端 + 后端 + Redis）
- [ ] Prometheus 指标采集
- [ ] Grafana 仪表盘配置
- [ ] 关键运行文档（启动、排障、验收）

## 3. M10 DoD（验收门禁）
- [ ] `docker compose up -d` 可启动核心服务
- [ ] 可看到后端健康指标与基础资源指标
- [ ] 至少 1 条 M10 部署 smoke 流程通过
- [ ] `uv run pytest -q -p no:faulthandler` 通过
- [ ] `npm run build` 通过
- [ ] `CHANGELOGS.md` 已更新
- [ ] 提交信息使用中文
