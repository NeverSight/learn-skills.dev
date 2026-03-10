---
name: spec-plan
description: Use when 需要在 sdlc-dev 的 Spec Pack 中执行 I1（实现计划），把 requirements/design 转成 `{FEATURE_DIR}/implementation/plan.md`（唯一执行清单与状态 SSOT），并为后续 I2 执行提供无歧义任务清单。
---

# spec-plan（I1：实现计划 / plan.md SSOT）

## 概览

I1 的目标是把 `{FEATURE_DIR}/requirements/*` 与 `{FEATURE_DIR}/design/*` 转换为**可直接执行**的实现计划 `{FEATURE_DIR}/implementation/plan.md`，并将其作为**唯一执行清单与状态 SSOT**（checkbox 任务 + 每任务步骤 + 最小验证 + 提交点 + 按 repo 审计信息）。

**开始时宣布：**「我正在使用 spec-plan 技能创建实现计划（plan.md SSOT）。」

## 何时使用 / 不使用

- **使用时机**
  - 你需要产出或更新 `{FEATURE_DIR}/implementation/plan.md`（I1 必做）。
  - 你准备进入 I2 执行，但当前没有“可勾选 + 可执行”的任务清单。
- **不要用在**
  - `spec-context` 失败、拿不到 `FEATURE_DIR`（此时必须停止）。
  - 输入侧 SSOT 不足：`requirements/solution.md` 与 `requirements/prd.md` 都不存在，且无法追溯范围/验收（必须在 plan.md 标注 NEEDS CLARIFICATION 并阻断进入 I2）。

## 门禁 / 停止（严格执行）

**REQUIRED SUB-SKILL：正在执行 `spec-context` 获取上下文，并在对话中回显 `FEATURE_DIR=...`（允许 `(reuse)`）。**

立刻停止（满足其一即可）：

- 未得到 `FEATURE_DIR`
- 分支/目录不确定（你发现自己想“猜 `.aisdlc/specs/...` 路径”）
- `requirements/solution.md` 与 `requirements/prd.md` 均缺失，导致目标/范围/验收口径无法追溯
- 任何关键不确定性无法在输入中证据化（必须写入 `plan.md/## NEEDS CLARIFICATION`，并明确“阻断进入 I2”）

## 输入 / 输出（落盘约定）

- **读取（渐进式披露，最少必要）**
  - 项目级（必读其索引或必要片段）：`project/memory/*`、`project/contracts/`、`project/adr/`
  - Spec 级（按需最少读）：`{FEATURE_DIR}/requirements/solution.md` 或 `{FEATURE_DIR}/requirements/prd.md`（至少其一）
  - **影响分析（强制，若有 solution.md）**：必须读取 `{FEATURE_DIR}/requirements/solution.md#impact-analysis`，提取受影响模块清单与需遵守的不变量，作为 I1 的约束输入（缺失则停止并回到 R1 补齐）
  - Spec 级（如存在且相关）：`{FEATURE_DIR}/design/design.md`、`{FEATURE_DIR}/design/research.md`
  - `.gitmodules`（如存在；用于识别可参与实现的 submodule 静态清单）
- **写入（唯一）**
  - `{FEATURE_DIR}/implementation/plan.md`

## 小块任务粒度（重用 writing-plans）

**每一步是一个动作（2–5 分钟）**，并在 `plan.md` 中写到“任何人照抄即可执行”：

- 「写失败测试」（如适用）- 一步
- 「运行确保失败」- 一步
- 「实现让测试通过的最少代码」- 一步
- 「运行验证确保通过」- 一步
- 「提交」（频繁提交）- 一步

> 约束：I1 只写计划，不写代码；但每个任务必须声明其**最小验证方式**（命令 + 期望信号）。

## `plan.md` 头部（必须）

**必须以该头部开头**（模板见 `./assets/plan-template.md`）：

```markdown
# [需求名] 实现计划（SSOT）

> **必需技能：** `spec-execute`（按批次执行本计划）
> **上下文获取：** 必须先执行 `spec-context` 获取上下文，定位 `{FEATURE_DIR}`，失败即停止

**目标：** [一句话描述要交付什么]
**范围：** In / Out
**架构：** [2–3 句方法说明 + 关键约束]
**验收口径：** [引用 requirements/solution.md 或 requirements/prd.md 的 AC/验收点]
**影响范围：** [引用 requirements/solution.md#impact-analysis 的受影响模块清单]
**需遵守的不变量：** [从 requirements/solution.md#impact-analysis 提取的关键 API/Data 契约不变量]
**子仓范围：** [若存在 `.gitmodules`，列出本次需求涉及的 submodule；无则写“无”]

---
```

## 计划正文（必须）

- **TL;DR**：一句话概括计划目标与范围
- **范围与边界**：In/Out（对齐需求与设计）
- **影响范围与约束（必填）**：
  - 受影响模块清单及影响类型（引用 `requirements/solution.md#impact-analysis`）
  - 需遵守的 API/Data 契约不变量（逐条列出，标注来源模块/锚点）
  - 跨模块影响与协调事项（基于依赖关系图/影响分析）
- **代码工作区清单（如适用，必填）**：
  - 从 `.gitmodules` 引用受影响子仓路径
  - 标记每个子仓是否 `required`
  - 默认分支要求：与根项目 `CURRENT_BRANCH` 同名
  - 若存在例外，显式记录 `exception_reason`
- **里程碑与节奏**：阶段拆分、时间预估、交付物清单
- **依赖与资源**：外部系统/团队/权限/环境/数据依赖
- **风险与验证**：风险清单、验证方式、Owner
- **验收口径**：对应 PRD/方案的关键 AC 与验收人
- **NEEDS CLARIFICATION（必须有）**：统一列出未消除的不确定项（未消除前不得进入 I2）

## 任务结构（重用 writing-plans，但加入 SSOT/审计/门禁）

`plan.md` 内必须包含**可勾选**的任务清单，作为唯一的执行清单与状态来源（`- [ ]/- [x]`）。

每个任务必须包含：

- 精确文件路径（创建/修改/测试）
- 可验证验收点（可测试条件）
- 可执行步骤（命令 + 期望输出/信号）
- 提交点与最小审计信息（按 repo 记录 `branch/commit/pr/changed_files`）

任务模板（示例骨架）：

```markdown
## 任务清单（SSOT）

### Task T1: [任务标题]

- [ ] **状态**：未开始 / 进行中 / 完成 / 阻塞（阻塞必须写明取证路径）

**代码仓范围：**
- 根项目：
- 子仓：（如适用；填写 `.gitmodules` 中的路径，并注明 `required=true/false`）

**文件：**
- 创建：`exact/path/to/new.file`
- 修改：`exact/path/to/existing.file`（可选：精确到段落/函数）
- 测试：`tests/exact/path/to/test.file`（如适用）

**验收点：**
- [可验证条件 1]
- [可验证条件 2]

**步骤 1：写失败测试（如适用）**
- 修改点：`tests/...`
- Run: `[精确命令]`
- Expected: FAIL（写出期望看到的关键失败信号）

**步骤 2：写最少实现**
- 修改点：`path/to/file`

**步骤 3：运行验证**
- Run: `[精确命令]`
- Expected: PASS（写出期望看到的关键通过信号）

**步骤 4：提交（频繁提交；commit message 必须中文）**
- Commit message: `[一句话说明 why（中文）]`
- 审计信息：
  - repo: `root`
    branch: `{CURRENT_BRANCH}`
    commit: `<TBD>`
    pr: `<TBD>`
    changed_files: `<TBD>`
  - repo: `<submodule path>`（如适用）
    branch: `{CURRENT_BRANCH}`
    commit: `<TBD>`
    pr: `<TBD>`
    changed_files: `<TBD>`
```

> 命令书写约定：默认面向 PowerShell；同一行多命令请用 `;` 分隔（不要用 `&&`）。

## I1-DoD（门禁：缺一不可）

- 计划范围与 `{FEATURE_DIR}/requirements/*`、`{FEATURE_DIR}/design/*` **一致且可追溯**
- 里程碑明确且可验收（每一项有对应产物或可验证标准）
- 依赖与风险已列出，并有最小验证/缓解动作（含 Owner）
- 关键验收口径可追溯（至少引用 `requirements/prd.md` 或 `requirements/solution.md`）
- **影响范围与约束已注入**：`plan.md` 包含"影响范围与约束"段落，受影响模块与需遵守的不变量已从 `requirements/solution.md#impact-analysis` 提取并逐条列出
- 若 `.gitmodules` 存在且影响分析命中子仓：`plan.md` 已声明受影响子仓、`required` 标记、默认同名分支要求与例外原因
- `plan.md` 内存在“任务清单（SSOT）”，且每个任务包含：文件路径、验收点、最小验证方式、提交点与审计信息
- 任何不确定项均进入 `NEEDS CLARIFICATION`，且**未消除前不得进入 I2**

## 牢记（高频规则速查）

- 始终先执行 `spec-context` 获取上下文，拿到 `FEATURE_DIR=...`，失败就停止
- 始终写**精确路径**、**精确命令**与**期望信号**
- 不要把不确定性写成已知；统一进入 `NEEDS CLARIFICATION` 并阻断 I2
- DRY、YAGNI、TDD、频繁提交（计划里也要体现提交节奏）
- 若本次实现涉及子仓：在 I1 中先写清受影响子仓与同名分支要求；子仓分支创建/校验发生在 I1 -> I2 之间

## 执行交接（写完 plan.md 之后）

保存计划后，本技能不再决定“下一步/执行方式”。统一做法：

- 宣布：`{FEATURE_DIR}/implementation/plan.md` 已落盘，且是实现侧唯一 SSOT
- 提示：**立即调用** `using-aisdlc` 路由下一步（通常路由到 I2：`spec-execute`，再到 Finish：`finishing-development`）
- 若用户明确要求“本会话使用 subagent-driven-development 并行执行”，也应先**调用** `using-aisdlc` 明确路由结论后再开始执行（避免出现第二个路由源）

## 完成后输出与自动路由（必须执行）

`plan.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: I1
  artifacts:
    - "{FEATURE_DIR}/implementation/plan.md"
  needs_human_review: false
  blocked: false
  block_reason: ""
  notes: "软检查点：plan.md 建议评审；如不触发硬中断 Router 可继续自动推进"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill（如 I2、Finish 等）
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

