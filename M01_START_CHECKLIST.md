# M01 开工清单（用户模块）

## 1. 分支与流程检查
- [x] 当前分支为临时分支（非 `master`）
- [x] 分支命名符合：`temp/m01-yyyymmdd-主题`
- [x] `REFACTOR_PLAN.md` 与 `CHANGELOGS.md` 已更新到 M01 状态

## 2. M01 目标范围（对标第3期）
- [ ] 用户注册：`POST /user/register`
- [ ] 用户登录：`POST /user/login`
- [ ] 登录态获取：`GET /user/get/login`
- [ ] 用户登出：`POST /user/logout`
- [ ] 基础权限（`user/admin`）控制
- [ ] Redis Session 落地与读取

## 3. 技术与目录准备
- [ ] 新建用户领域目录（model/service/router/repository）
- [ ] 新增用户表实体与迁移脚本
- [ ] 新增密码加密工具
- [ ] 新增会话读写封装（基于 Redis）
- [ ] 前端用户登录/注册页面联调接口改造

## 4. M01 DoD（验收门禁）
- [ ] 四个用户核心接口可用
- [ ] 未登录访问受限接口返回预期错误码
- [ ] 登录后可获取当前用户
- [ ] 登出后会话失效
- [ ] `uv run pytest` 通过
- [ ] `npm run build` 通过
- [ ] `CHANGELOGS.md` 已更新
- [ ] 提交信息使用中文

## 5. 推荐提交拆分（中文）
1. `feat(m01): 新增用户实体与基础迁移`
2. `feat(m01): 实现注册登录与会话管理`
3. `feat(m01): 增加登录态与登出接口`
4. `feat(m01): 接入基础权限校验`
5. `test(m01): 补充用户模块接口测试`
6. `docs(m01): 更新验收记录与变更日志`

