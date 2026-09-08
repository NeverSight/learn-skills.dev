---
version: 0.2.0
name: cawplan-testrail-link
description: |
  Manually link existing TestRail Cases or Plans/Runs back to CawPlan mappings after QA hand-imported or hand-created TestRail artifacts.
  Link matches requirement_id + test_point_id in refs only (no hash validation).
  Use when: linking CSV-imported cases by refs; binding hand-made TestPlan/TestRun to CawPlan tickets; 用例回链、refs 映射、Plan Run 绑定、手工导入后 link.
  Ideal path after A3 CSV import: auto Suite → AutoScan → one confirm.
  NOT for: creating TestRail cases (use `cawplan-testcase-import`); creating Plans/Runs (use `cawplan-testplan-layout`); generating/exporting cases (use `cawplan-testcase-generate`); execution progress or defect filing.
argument-hint: "[Product link or product_id + Requirement or Version + optional TestRail URL]"
allowed-tools: Bash
---

# CawPlan TestRail Link — T2-A8 手工映射回链

```bash
cawplan skill check
```

## 硬门禁（MUST）

1. **preview-first** → **确认闸** → `execute --confirm`；禁止跳闸。
2. **Workflow B 前置**：`milestone mapping-get` → `has_mapping=false` **必须停止**（固定文案见 `link-plans.md §MilestoneGate`）；不得继续 preview/execute。
3. **Workflow A 冲突**：`conflicts` 非空 → **禁止 execute**；须先人工处理 TestRail/CawPlan 侧冲突。
4. **禁止**：直连 TestRail API；调用 `import/execute` 或 `plan/execute` 冒充 link；无 preview 的 `execute`。
5. **用户展示**：`ux.md §Glossary`；`preview_id`/`mapping_id`/UUID 默认隐藏；**Case / Plan / Run / Suite ID 必须可点击**（`ux.md §TestRailLinks`）。
6. **热接力 + AutoScan（Workflow A）**：P1 可跳过 A1；`suites.length===1` **无感采用** Suite；Section 走 `link-cases.md §AutoScan`（无 parent preview → 无感 retry 1 次 → 仍失败才框 A3s）。**禁止**每轮框 3.5「新建顶级 / 缩小」。
7. **Cost**：按 `ux.md §Cost` 懒加载 reference、缓存 `mappings get`、preview 表截断展示；禁止为消歧重复全量 `sections list`（AutoScan retry 时允许按 suite 缓存调一次）。

## Reference 加载（MUST · 降本）

| 时机 | Read | 禁止 |
|------|------|------|
| 路由 / 框 0 / 确认闸 / Preview·Result 模板 / 错误 | `ux.md` 对应 § | 一次性 Read 全部 references |
| 仅 Workflow A | `link-cases.md` 对应 § | 未路由到 A 时 Read |
| 仅 Workflow B | `link-plans.md` 对应 § | 未路由到 B 时 Read |

## Prompt 路由（框 0）

| 命中 | Workflow |
|------|----------|
| 用例 / Case / CSV / refs / 导入后回链 / link case | **A** |
| Plan / Run / 测试计划 / 工单绑定 / link plan | **B** |
| A 与 B 同时命中 | `AskUserQuestion` 二选一（`ux.md §Prompts` 框 0） |
| 均未命中 | 框 0：链接 **用例** 还是 **计划/运行**？ |

路由后 **只走一条 Workflow**；禁止同轮混跑 A+B。

## 允许命令

| 用途 | 命令 |
|------|------|
| 映射 / origin | `qa-insights testrail mappings get <product_id>` |
| Section 查找（A · AutoScan / 框 A3s） | `qa-insights testrail sections list <product_id> <suite_id> [--refresh]` |
| Milestone 闸门（B · Step 1） | `qa-insights testrail milestone mapping-get <product_id> <version_id>` |
| URL 解析（B · 可选） | `qa-insights testrail resolve-url <product_id> --url <url>` |
| A preview / execute | `qa-insights testrail link cases preview …` · `… link cases execute … --preview-id … --confirm` |
| B preview / execute | `qa-insights testrail link plans preview …` · `… link plans execute … --preview-id … --confirm [--supersede]` |
| 辅助解析 | `products list`、`versions list`、`requirements get`、`testpoints list`（仅缺上下文时） |

**禁止**：`cawplan api`、链式 `&&`、直连 TestRail。

---

## Workflow A — Link Cases（CSV refs 回链）

| Step | 动作 | Detail |
|------|------|--------|
| **0** | Agent 自检 CSV 导入前提 | 不单独 Ask；同会话 A3 / 用户说「已导入」→ 假定满足；preview 全失败时再引导 |
| **1** | 解析 `product_id`、`requirement_id` | 热接力可跳过 A1；缺则 `ux.md §Prompts` 框 A1 |
| **2** | `mappings get`；**§AutoSuite** | `link-cases.md §Mappings` · `§AutoSuite` |
| **3** | **§AutoScan**（先无 `parent_section_id` preview） | 无感 retry ≤1 次；仍失败 → 框 A3s |
| **4** | 展示 preview（含超链接） | `ux.md §PreviewCases`；`conflict>0` → 停止 |
| **5** | **确认闸**（仅 `to_link>0`） | `to_link=0` → 不弹；`already_linked>0` 且全跳过 → 成功说明 |
| **6** | `link cases execute --confirm` | `ux.md §ResultCases` |

> Step 3–4 合并执行：AutoScan 的首次失败 preview **不对用户展示**，直接 retry 或进 A3s。

---

## Workflow B — Link Plans（手工 Plan/Run 绑 Ticket）

| Step | 动作 | Detail |
|------|------|--------|
| **0** | 解析 `product_id`、`version_id` | 缺则 `ux.md §Prompts` 框 B1 |
| **1** | `milestone mapping-get` | `has_mapping=false` → `link-plans.md §MilestoneGate`，停止 |
| **2** | 收集绑定：Ticket + TestRail Plan/Run URL 或 ID | `link-plans.md §CollectBindings` · 框 B2 |
| **3** | 组装 `bindings[]`；`plan_id=0` = Run-only | `link-plans.md §BindingRules` |
| **4** | `link plans preview` | `link-plans.md §PreviewCLI` |
| **5** | 展示 preview（含超链接） | `ux.md §PreviewPlans`；`supersede_required>0` → 框 B-supersede |
| **6** | **确认闸** | `ux.md §Prompts` 框 B-confirm |
| **7** | `link plans execute --confirm`（替换时加 `--supersede`） | `ux.md §ResultPlans` |

---

## 错误（Agent）

| code | Workflow | 处理 |
|------|----------|------|
| `MILESTONE_NOT_BOUND` | B | `link-plans.md §MilestoneGate`；引导 `cawplan-testplan-layout` |
| `CONFLICT_BLOCKS_EXECUTE` | A | 列 `conflicts`（`ux.md §ConflictMessages`）；停止 |
| `SUPERSEDE_REQUIRED` | B | 框 B-supersede；补 `--supersede` |
| `REQUIREMENT_NOT_FOUND` / `TICKET_NOT_IN_VERSION` | A/B | `ux.md §Errors` |
| `SUITE_NOT_IN_PROJECT` / `SECTION_*` | A | 重走框 A3 / 框 A3s |
| `PLAN_NOT_FOUND` / `RUN_NOT_FOUND` / `RUN_NOT_IN_PLAN` | B | 核对 URL/ID；`link-plans.md §CollectBindings` |
| `PREVIEW_EXPIRED` | A/B | 重新 preview（确认态可复用） |
| `TESTRAIL_UNAVAILABLE` | A/B | 勿重复 execute |
| `CONFIRMATION_REQUIRED` | A/B | 补 `--confirm` |
| `auth`/403 | A/B | `ux.md §Errors` |

**Workflow A 冲突 message 速查**（BE 原文 → 见 `ux.md §ConflictMessages`）：

- `TestRail case is already mapped to a different test point` — 同 Case 已绑其他测试点
- `TestRail case does not match the case already mapped for this test point` — 同测试点已映射其他 Case
- `another TestRail case in this preview claims the same test point and case identity` — 本次预览 refs 重复

## References

- [ux.md](references/ux.md) — 路由、Ask 框、TestRail 超链接、Preview/Result 模板、降本、错误
- [link-cases.md](references/link-cases.md) — Workflow A：MatchingRules、AutoScan、CLI、preview 字段
- [link-plans.md](references/link-plans.md) — Workflow B：Milestone 闸门、bindings 收集、Run-only、supersede
