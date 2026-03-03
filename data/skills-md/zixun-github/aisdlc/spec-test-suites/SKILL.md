---
name: spec-test-suites
description: Use when 需要在 Spec Pack 的 verification 阶段生成或更新 `{FEATURE_DIR}/verification/suites.md`（测试套件），把用例组织成可执行集合并定义阻断规则与执行顺序。
---

# Spec 测试套件（V3：Suites）

把 `usecase.md` 里的用例编号组织成可执行集合（**smoke / regression / targeted**），并明确 **执行顺序、依赖与阻断口径**。

**权威口径：** `design/aisdlc_spec_verification.md`

---

## 硬门禁（必须遵守）

- **先定位再读写**：必须先运行 `spec-context` 得到并回显 `FEATURE_DIR=...`；失败即停止，禁止猜路径。
- **必读项目级 memory**：`project/memory/product.md`、`project/memory/tech.md`、`project/memory/glossary.md`；读不到必须写 `CONTEXT GAP`。
- **输入依赖**：`{FEATURE_DIR}/verification/usecase.md` 与 `{FEATURE_DIR}/verification/test-plan.md` 应已存在；缺失时必须写 `CONTEXT GAP` 并停止（避免凭空编排）。
- **套件必须可定位**：套件条目必须指向具体用例编号（禁止“覆盖登录流程”这类模糊描述）。
- **禁止越权路由**：完成后只输出 `ROUTER_SUMMARY`，下一步由 `using-aisdlc` 决策。

---

## 红旗清单（出现任一条就停止）

- 想在没有 `usecase.md` 的情况下“凭经验”编套件
- smoke 套件没有“失败即阻断交付”的清晰口径
- 套件条目不能落到具体 `TC-*` 编号

---

## 唯一做法（PowerShell）

### 1) 获取 `FEATURE_DIR`

```powershell
. ".\skills\spec-context\scripts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

### 2) 目标输出路径

```powershell
$out = Join-Path $FEATURE_DIR "verification/suites.md"
Write-Host "OUTPUT=$out"
```

---

## 输出物最小结构（建议）

写入 `{FEATURE_DIR}/verification/suites.md`，至少包含：

- **Smoke（冒烟）**
  - 目标：关键路径快速阻断
  - 预计时长
  - **阻断规则**（与 `test-plan.md` 的准出标准一致）
  - 用例清单：`TC-...`（列表）
- **Targeted（定向回归）**
  - 触发条件（例如：命中 impact-analysis 的模块/风险）
  - 用例清单：`TC-...`
- **Regression（回归）**
  - 覆盖范围说明（按模块/能力/风险）
  - 用例清单：`TC-...`
- **执行顺序与依赖**
  - 推荐顺序：smoke → targeted → regression（可根据项目约束调整，但必须写清楚）

---

## DoD 自检（V3-DoD）

- [ ] 套件中的每条目都能定位到具体 `TC-*` 编号
- [ ] smoke 套件有明确“失败即阻断交付”的口径，且与 `test-plan.md` 一致
- [ ] targeted 套件能追溯到影响面/风险来源（如有 `requirements/solution.md#impact-analysis`）

---

## 完成后输出与自动路由（必须执行）

`suites.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: V3
  artifacts:
    - "{FEATURE_DIR}/verification/suites.md"
  needs_human_review: false
  blocked: false
  block_reason: ""
  notes: "软检查点：测试套件已生成/更新；Router 可继续自动推进到 V4（spec-test-execute）"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill（如 V4 等）
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

---
name: spec-test-suites
description: Use when 需要在 sdlc-dev 的 Spec Pack 中生成/更新 verification 阶段 V3 测试套件编排（verification/suites.md），以 smoke/regression/targeted 组织用例并明确阻断规则与追溯来源。
---

# Spec 测试套件（V3：verification/suites.md）

## 概览

本技能是 **verification 阶段 worker skill**，只负责：

- 门禁校验（先定位 `{FEATURE_DIR}`，再读必要输入）
- 生成/更新 `{FEATURE_DIR}/verification/suites.md`
- 按 V3-DoD 自检（套件条目可定位到用例编号）
- 输出 `ROUTER_SUMMARY` 后回到 `using-aisdlc`

## 硬门禁（不得绕过）

### 1) 先定位 FEATURE_DIR（禁止猜路径）

```powershell
. ".\skills\spec-context\scripts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

失败即停止。

### 2) 必读项目级 Memory（缺失写 CONTEXT GAP）

- `.aisdlc/project/memory/product.md`
- `.aisdlc/project/memory/tech.md`
- `.aisdlc/project/memory/glossary.md`

任一缺失：在 `suites.md` 中显式写 `CONTEXT GAP`。

### 3) 必须读取用例与计划（否则无法编排）

- `{FEATURE_DIR}/verification/usecase.md`（必须存在）
- `{FEATURE_DIR}/verification/test-plan.md`（建议存在；缺失写 `CONTEXT GAP` 并把风险放入阻断项）

若存在 `{FEATURE_DIR}/requirements/solution.md#impact-analysis`：应读取用于 targeted 套件追溯；不存在则说明 targeted 的依据来源。

## 输出（落盘）

- `{FEATURE_DIR}/verification/suites.md`

## `suites.md` 最小结构（必须包含）

- smoke
  - 预计执行时长
  - 阻断规则（与 V1 准出标准一致）
  - 用例列表（必须写 TC 编号）
- regression
  - 用例列表（TC 编号，可按模块/影响面分组）
- targeted（如适用）
  - 触发条件（来自 impact-analysis / 风险清单）
  - 用例列表（TC 编号）
- 执行顺序与依赖（例如 smoke → targeted → regression）

## V3-DoD 自检

- [ ] 套件条目能定位到具体用例编号（禁止模糊描述）
- [ ] smoke 套件阻断规则与 V1 准出标准一致
- [ ] targeted 套件有可追溯来源（impact-analysis/风险清单/变更说明）

## 红旗 STOP

- 未回显 `FEATURE_DIR=...` 就开始写 `suites.md`
- 套件条目没有引用任何 `TC-...` 编号

## 完成后输出与自动路由（必须执行）

`suites.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: V3
  artifacts:
    - "{FEATURE_DIR}/verification/suites.md"
  needs_human_review: false
  blocked: false
  block_reason: ""
  notes: "软检查点：测试套件已生成/更新；Router 可继续自动推进到 V4（spec-test-execute）"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill（如 V4 等）
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

