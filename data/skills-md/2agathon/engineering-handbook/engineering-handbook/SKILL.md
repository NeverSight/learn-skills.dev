---
name: engineering-handbook
description: 把本仓库的工程手册 Tier0 规则注入到 AI vibe coding（跨语言：Java/Python/TS/React/Vue）。
---

# Engineering Handbook (Tier0 for AI Vibe Coding)

## When to Use

- 默认：任何编码/重构/评审任务。
- 特别适用：你希望 AI 产出“可验收、可回滚、契约清晰、边界清晰”的最小可逆变更。

## Tier0 Rules (Always Apply)

- IN-001：任何对外可见变化必须给出 verify + rollback（expected vs actual）。
- AR-001：核心逻辑不得依赖不稳定细节（DB/网络/框架类型/时间/随机/env）；通过 port + adapter 注入。
- CT-001：跨边界业务结构不得使用裸 dict/map/object 作为合同；必须使用显式 DTO/type。
- AR-002 + BD-001：跨模块依赖只能通过公开出口（facade/public API），禁止深层 import 内部目录/包。
- MD-001：边界资产必须自描述；字段级数据需要 data_classification；日志/错误/导出/埋点最小化暴露。

## Required Output Format

1) 先输出：my understanding + acceptance。

2) 若要执行改动：先输出 goal / scope(files/modules/paths) / budget / verify / rollback（scope 未列出不得改）。

3) 不确定处用 TODO/ASSUMPTION/IMPACT 标记，避免扩散改动（smallest diff first）。

## On-demand References (Read Only When Triggered)

- 规则 SSOT：universal/rules.md
- 方法论与十问：universal/method.md
- 边界契约实践：practices/boundary-contracts.md
- 重构配方（smallest diff）：playbooks/refactoring-playbook.md
- 语言映射（按栈选读）：mappings/python.md, mappings/typescript.md, mappings/jvm.md, mappings/go.md, mappings/dotnet.md, mappings/sql.md
