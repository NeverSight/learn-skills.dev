---
name: spec-test-usecase
description: Use when 需要在 Spec Pack 的 verification 阶段生成或更新 `{FEATURE_DIR}/verification/usecase.md`（测试用例），并要求 AC 可追溯与结构可生成自动化脚本。
---

# Spec 测试用例（V2：Usecase）

把 `requirements/solution.md` / `requirements/prd.md` 中的验收口径（AC）转成 **可执行、可判定、可追溯、可机器提取** 的手工测试用例结构。

**权威口径：** `design/aisdlc_spec_verification.md`

---

## 硬门禁（必须遵守）

- **先定位再读写**：必须先运行 `spec-context` 得到并回显 `FEATURE_DIR=...`；失败即停止，禁止猜路径。
- **必读项目级 memory**：`project/memory/product.md`、`project/memory/tech.md`、`project/memory/glossary.md`；读不到必须写 `CONTEXT GAP`。
- **需求级最小输入**：`{FEATURE_DIR}/requirements/solution.md` 或 `{FEATURE_DIR}/requirements/prd.md` 至少其一必须存在；否则停止并写 `CONTEXT GAP`。
- **强制结构化**：每条用例必须满足“编号/类型/步骤+断言点/追溯/套件”最小结构，不允许用自由散文代替。
- **禁止越权路由**：完成后只输出 `ROUTER_SUMMARY`，下一步由 `using-aisdlc` 决策。

---

## 红旗清单（出现任一条就停止）

- 没有回显 `FEATURE_DIR=...` 就开始编写用例
- 想用“覆盖登录/覆盖支付”这种描述代替 `TC-*` 可执行步骤
- 想把“预期结果”写成主观判断（如“看起来正常”）而不是可观测断言点
- 想用 `TBD/待补` 代替 AC 追溯链接

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
$out = Join-Path $FEATURE_DIR "verification/usecase.md"
Write-Host "OUTPUT=$out"
```

---

## 用例结构（强制，自动化友好）

每条用例必须包含：

- **稳定编号**：`TC-<DOMAIN>-<NNN>`（例：`TC-AUTH-001`）。编号发布后不随意改动。
- **优先级**：P0 / P1 / P2
- **类型**：UI / API / 集成 / 回归（可按需扩展，但必须可枚举）
- **标签**：影响面/模块/风险（数组形式）
- **追溯**：至少链接到 1 条 AC（来自 `solution/prd`）
- **套件**：至少标注 `smoke`/`regression`（如有 `targeted` 也可标注）
- **前置条件**：可准备、可执行（含账号/权限/开关/环境）
- **测试数据**：给出示例值或生成方式（禁止“自行准备”）
- **步骤**：逐步编号；**每步必须包含预期结果（可观测断言点）**
- **后置条件/清理**：会污染数据时必须写清楚

---

## 最小模板（单条用例）

```markdown
## TC-XXX-001: [标题]

**优先级：** P0 | P1 | P2
**类型：** UI | API | 集成 | 回归
**标签：** [tag1, tag2]
**追溯：** AC-001（`requirements/prd.md#...` 或 `requirements/solution.md#...`）
**套件：** smoke, regression

### 目标
[一句话说明验证什么]

### 前置条件
- ...

### 测试数据
- ...

### 测试步骤
1. ...
   **预期：** ...
2. ...
   **预期：** ...

### 后置条件/清理
- ...
```

---

## DoD 自检（V2-DoD）

- [ ] P0/P1 用例均“可执行”：前置条件与数据不缺失
- [ ] 每一步都有“预期结果”（可观测、可判定）
- [ ] AC 覆盖关系明确（至少能回答“哪些 AC 被哪些用例覆盖”）
- [ ] 用例结构满足后续自动化生成的最小信息要求（编号/类型/步骤/断言点）

---

## 完成后输出与自动路由（必须执行）

`usecase.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: V2
  artifacts:
    - "{FEATURE_DIR}/verification/usecase.md"
  needs_human_review: false
  blocked: false
  block_reason: ""
  notes: "软检查点：测试用例已生成/更新；Router 可继续自动推进到 V3（spec-test-suites）或 V4（spec-test-execute）"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill（如 V3、V4 等）
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

---
name: spec-test-usecase
description: Use when 需要在 sdlc-dev 的 Spec Pack 中生成/更新 verification 阶段 V2 测试用例（verification/usecase.md），并且必须保证用例结构可执行、每步有预期且可追溯 AC。
---

# Spec 测试用例（V2：verification/usecase.md）

## 概览

本技能是 **verification 阶段 worker skill**，只负责：

- 门禁校验（先定位 `{FEATURE_DIR}`，再读必要输入）
- 生成/更新 `{FEATURE_DIR}/verification/usecase.md`
- 按 V2-DoD 自检（可执行 + 可追溯 + 自动化友好结构）
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

任一缺失：在 `usecase.md` 中显式写 `CONTEXT GAP`（并说明对用例口径的影响）。

### 3) AC 来源至少其一存在

必须读取其一作为验收口径来源：

- `{FEATURE_DIR}/requirements/solution.md` 或
- `{FEATURE_DIR}/requirements/prd.md`

两者都不存在：停止并回到 `using-aisdlc`。

### 4) 测试计划建议作为约束输入

若 `{FEATURE_DIR}/verification/test-plan.md` 已存在：应读取以约束范围/环境/优先级口径；若不存在：在 `usecase.md` 写明 `CONTEXT GAP` 并把缺口放入风险/阻断项（不得用 `TBD` 悬空）。

## 输出（落盘）

- `{FEATURE_DIR}/verification/usecase.md`

## `usecase.md` 结构要求（强制）

### 编号规范

- 稳定编号：`TC-<DOMAIN>-<NNN>`（例如 `TC-AUTH-001`）
- 编号发布协作后不随意改动
- 禁止自创 `UC-001`、`CASE-1` 等编号体系

### 单条用例最小模板（必须字段齐全）

```markdown
## TC-XXX-001: [标题]

**优先级：** P0 | P1 | P2
**类型：** UI | API | 集成 | 回归
**标签：** [tag1, tag2]
**追溯：** AC-001（`requirements/solution.md#...` 或 `requirements/prd.md#...`）
**套件：** smoke, regression

### 目标
[一句话说明验证什么]

### 前置条件
- ...

### 测试数据
- ...

### 测试步骤
1. ...
   **预期：** ...（可观测、可判定）
2. ...
   **预期：** ...

### 后置条件/清理
- ...
```

### “可观测预期”的最低标准

预期必须指向可判定信号，例如（择一即可，越具体越好）：

- UI 文案/控件状态/跳转路径
- HTTP 状态码/响应体字段
- 数据记录是否创建/更新（含关键字段）
- 日志关键字/审计事件

禁止用“成功/正常/符合预期”之类不可判定措辞。

## V2-DoD 自检

- [ ] P0/P1 用例可执行（前置条件与数据不缺失）
- [ ] 每步都有可观测预期结果（可判定 pass/fail）
- [ ] AC 覆盖关系可回答（哪些 AC 被哪些用例覆盖）
- [ ] 用例编号稳定、结构可供后续自动化生成

## 反模式（必须避免）

| 反模式 | 为什么不行 | 正确做法 |
|---|---|---|
| 用 `TBD/待确认` 占位步骤或数据 | 用例不可执行 | 缺失进入风险/阻断项并说明影响 |
| 每步没有预期结果 | 无法判定通过/失败 | 每步写可观测断言点 |
| 只写“覆盖很多面”的标题 | 不可执行 | 标题之外必须补全前置/数据/步骤/预期 |

## 红旗 STOP

- 未回显 `FEATURE_DIR=...` 就开始写 `usecase.md`
- 用例编号体系偏离 `TC-<DOMAIN>-<NNN>`
- 步骤预期出现“成功/正常/符合预期”这类不可判定措辞

## 完成后输出与自动路由（必须执行）

`usecase.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: V2
  artifacts:
    - "{FEATURE_DIR}/verification/usecase.md"
  needs_human_review: false
  blocked: false
  block_reason: ""
  notes: "软检查点：测试用例已生成/更新；Router 可继续自动推进到 V3（spec-test-suites）或 V4（spec-test-execute）"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill（如 V3、V4 等）
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

