---
version: 0.2.0
name: cawplan-risk-assessment
description: |
  Assess CawPlan version release risk via QA Insights rule engine: compute risk level, structured reasons, suggested actions, and save confirmed assessment to Version.
  Use when: release risk assessment, can we release, version risk level, 发版风险评估、能不能发版、版本风险、评估发版风险、保存风险结论.
  NOT for: test execution progress only (use `cawplan-test-execution-progress`); using `cawplan-plan-track` schedule/ticket-completion risk as the A5 conclusion (read-only `release_at`/completion from `versions track` is allowed for display context); defect filing (use `cawplan-defect-ticket`); test plan layout; or ticket QA report release readiness.
argument-hint: "[product portal link or product_id + version_id + optional ticket_id]"
allowed-tools: Bash
---

# CawPlan Risk Assessment — A5 发版风险评估

```bash
cawplan skill check
```

## 硬门禁（MUST）

1. **规则算等级、AI 做摘要**：`risk_level` 以 `compute` 响应为准；Agent **不得**自行重算或静默降级 `CRITICAL`。
2. **保存须双闸**：展示 compute 结果 → 用户确认 → `--body-file` + `--dry-run` → 提交闸 → `--confirm` 执行 `save`。
3. **禁止**把 A3 执行进度、`cawplan-plan-track` 的排期 `risk`/`risk_reason` 当作 A5 结论；**禁止**声称本结论等同于 A8 Ticket Report 的 Release Readiness。
   **允许**调用 `versions track` / `tickets search` / `execution failures` 作**只读上下文富化**，须标注「不参与规则计算」。
4. **禁止** `cawplan api`、直连 TestRail、A1/A2/A4/A8 写操作。
5. **用户展示**：友好字段名；`product_id`/`version_id`/UUID 默认隐藏；Agent 自行 `AskUserQuestion`（不写入 `allowed-tools`）。

## Reference 加载（MUST）

| 时机 | Read | 禁止 |
|------|------|------|
| 开场 | 无 | 一次性 Read 全部 references |
| 解析上下文 / compute / 富化 / 解读 reasons | `compute-rules.md` | — |
| 输出模板 / 富化表 / runs 附录 | `ux.md` | 与 `save-rules.md` 一并 Read |
| 保存 / override / 衔接 A4·A7 | `save-rules.md` | — |

## 允许命令

| Step | 命令 |
|------|------|
| 辅助 | `products list`、`versions list` |
| 只读富化（Step 4b） | `versions track <product_id> <version_id>` |
| 只读富化（Step 4b） | `tickets search --unique_ids <id1,id2,...>`（**无需** `--time_range`） |
| 只读富化（Step 4b） | `qa-insights testrail execution failures <product_id> <version_id> [--run-id] [--limit]` |
| 阈值（可选） | `qa-insights risk-rules get <product_id>` |
| 历史 | `qa-insights risk-assessment get <product_id> <version_id>` |
| 计算 | `qa-insights risk-assessment compute <product_id> <version_id> [--ticket-id] [--plan-mapping-ids] [--no-refresh-execution]` |
| 保存 | `qa-insights risk-assessment save <product_id> <version_id> --body-file <path> [--dry-run] --confirm` |

## Workflow

| Step | 动作 | Detail |
|------|------|--------|
| **0** | 解析 product / version；可选 `ticket_id` | `compute-rules.md §0` |
| **1** | 意图分流：仅查历史 vs 重算 vs 保存 | `compute-rules.md §Intent` |
| **2** | 可选 `risk-rules get`（用户问阈值或 HIGH 原因） | `compute-rules.md §Rules` |
| **3** | 可选 `risk-assessment get`（仅历史且未要求重算） | `compute-rules.md §Get` |
| **4** | `risk-assessment compute`（默认刷新执行数据） | `compute-rules.md §Compute` |
| **4b** | 只读富化（compute 或 get 后；按 reason 条件触发；可并行） | `compute-rules.md §Enrich` · `ux.md §Enrich` |
| **5** | Agent 解读：摘要 + 分层报告；**不改** `risk_level` | `ux.md §Output` |
| **6** | 保存决策闸（用户未要求保存则停） | `save-rules.md §Prompts` |
| **7** | 组装 body-file → `--dry-run` → 提交闸 → `--confirm` | `save-rules.md §Save` |
| **8** | 保存结果 + 文末衔接一句（A4/A7） | `save-rules.md §Handoff` |

**用户明确「只要上次结论 / 不重算」** → 跳过 Step 4，走 Step 3 → **4b** → 5。  
**用户明确「保存」但本会话无 compute** → 先 Step 4 或确认沿用 `get` 记录后再 `save`。

## 输出概要

未保存：风险等级 + 发布/完成度上下文 + 覆盖率优先指标 + 富化详情表 + 建议行动 + 是否保存询问。  
已保存：追加 `saved_at`、`saved_by`、`note`、`ai_summary`。  
模板见 `ux.md §Output`、`save-rules.md §Saved`。

## References

- [compute-rules.md](references/compute-rules.md) — 上下文、compute/get、等级与 reasons 解读、富化触发
- [ux.md](references/ux.md) — 报告模板、富化表、runs 附录、建议行动展示
- [save-rules.md](references/save-rules.md) — 保存 body、override、确认闸、A4/A7 衔接
