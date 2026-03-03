---
name: spec-test
description: Use when 需要在 Spec Pack 的 verification 阶段生成/更新测试计划、用例、套件或测试报告，并要求严格门禁、可追溯落盘与不越权路由。
---

# Spec Pack 验证（Verification）主技能：spec-test

本技能是 verification 阶段的 **worker skill 入口**：负责统一门禁、输入/输出约束、追溯与 DoD 自检。实际产物由子技能 `spec-test-*` 生成。

**权威口径：** `design/aisdlc_spec_verification.md`（本文档即本技能的 SSOT）。

---

## 何时使用

- 需要为某个 Spec Pack 产出或更新以下任一文件：
  - `verification/test-plan.md`
  - `verification/usecase.md`
  - `verification/suites.md`
  - `verification/report-{date}-{version}.md`
- 你发现自己开始出现以下“危险信号”（说明很容易违规）：
  - 想“先随便写到 `./verification/`，之后再迁移”
  - 想跳过 `requirements/*` 或项目级 memory，说“先写个模板占位”
  - 想用 `TBD/待补` 代替 AC 追溯与影响面
  - 想在技能内决定下一步流程（越权路由）

## 何时不使用

- 你在做“下一步该走哪里/是否跳过 verification”的分流判断：这属于 Router，应该回到 `using-aisdlc`。
- 你要写自动化测试代码：verification 阶段此技能只负责文档产物与门禁，不要求自动化代码实现。

---

## 硬门禁（必须遵守）

### 1) 先定位再读写：必须先得到 `FEATURE_DIR`

- **凡读写 `verification/*`，必须先运行 `spec-context` 获取 `FEATURE_DIR` 并回显**。
- **`spec-context` 失败即停止**：不得猜路径、不得用当前工作目录推断、不得“先写到根目录再说”。

### 2) 必读上下文（渐进式披露）

读取失败或不存在时，必须显式写出 `CONTEXT GAP`，不得静默跳过：

- `project/memory/product.md`
- `project/memory/tech.md`
- `project/memory/glossary.md`

需求级最小必要输入（至少其一必须存在）：

- `{FEATURE_DIR}/requirements/solution.md` 或 `{FEATURE_DIR}/requirements/prd.md`

### 3) Worker 边界：禁止越权路由

- 本技能与子技能 **只负责门禁 + 产物落盘 + DoD 自检**。
- 完成后 **不得**在技能内部决定“下一步做什么”，只能输出 `ROUTER_SUMMARY`，并提示“回到 Router（using-aisdlc）继续路由”。

---

## 子技能一览（调用/路由入口）

| 子技能 | 产物（落盘） | 目标 |
|---|---|---|
| `spec-test-plan` | `{FEATURE_DIR}/verification/test-plan.md` | 冻结范围/策略/环境/准入准出/风险清单 |
| `spec-test-usecase` | `{FEATURE_DIR}/verification/usecase.md` | 把 AC 转为可执行、可生成自动化的用例结构 |
| `spec-test-suites` | `{FEATURE_DIR}/verification/suites.md` | 组织 smoke/regression/targeted 套件与执行顺序 |
| `spec-test-execute` | `{FEATURE_DIR}/verification/report-{date}-{version}.md` | 产出结论性报告：覆盖/结果/阻断/缺陷引用/风险建议 |

---

## 反模式与显式反制（来自基线压力场景）

| 常见借口/压力话术 | 现实与反制 |
|---|---|
| “赶时间，先写到 `./verification/`，后面再搬” | **禁止猜路径。** 未定位 `FEATURE_DIR` 就落盘会制造不可追溯的垃圾产物；必须先 `spec-context`。 |
| “requirements 太慢，先写模板占位” | verification 的核心是 **AC → 用例/报告追溯**；不读 `solution/prd` 等于放弃可验证口径。允许 `CONTEXT GAP`，但不允许用 `TBD` 伪装完成。 |
| “负责人说别管门禁，能用就行” | worker skill 的价值就是门禁；如果必须偏离流程，只能在产物中写明 **风险与后果**，并把偏离点升级为显式 `CONTEXT GAP / PROCESS DEVIATION`，且仍不得猜路径。 |
| “我顺手告诉你下一步该做什么” | **禁止越权路由。** 只能输出 `ROUTER_SUMMARY`，下一步由 `using-aisdlc` 决策。 |

---

## 输出约定（统一给 Router 消费）

任一 `spec-test` / `spec-test-*` 完成时，**必须**执行「完成后输出与自动路由」三步骤（与 `spec-product-clarify` 等 worker skill 一致）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策；具体 stage/artifacts 以各子技能为准）
2. **立即执行 `using-aisdlc`**：将 `ROUTER_SUMMARY` 作为路由输入传递，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）
3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

> 兼容说明：历史上某些文档会使用自由文本/自定义字段形式的“router summary”。在本仓库 Spec Pack 流程中，以 `using-aisdlc` 定义的 YAML `ROUTER_SUMMARY` 为唯一权威输出格式。

