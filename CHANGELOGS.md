# 变更日志（CHANGELOGS）

本文件用于记录项目的重要变更，统一使用中文维护。

## 维护规范
- 所有新增记录必须使用中文描述。
- 开发中变更先写入 `进行中`。
- 验收通过并合并 `master` 后，将条目归档到对应日期。
- 每条记录建议附带提交哈希，便于追踪。

## 进行中
- 规范升级：强制“临时分支开发 -> 验收通过 -> 合并 master”流程。
- 规范升级：提交说明使用中文描述。
- 规范升级：重构计划补充分支、验收、门禁规则。

## 2026-02-26

### 新增
- 初始化仓库，新增基础文档与重构计划初版。
  - `aaa357a` `docs: initialize python-ai-mother with refactor plan`
- 新增变更日志文件并写入初始历史。
  - `a3ad0e5` `docs: add CHANGELOGS.md with initial history`

### 变更
- 强制项目内 Python 虚拟环境策略，统一使用 `uv`。
  - `83fb120` `docs: enforce project-local env policy with uv`
- 优化重构路线，按 `yu-ai-code-mother` 历史里程碑对齐。
  - `8f9bded` `docs: optimize refactor roadmap aligned to yu-ai git milestones`

