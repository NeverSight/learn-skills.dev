---
name: using-aisdlc
description: Use when 需要在 sdlc-dev 仓库执行 AI SDLC（Spec Pack）流程、选择/串联需求侧（raw/solution/prd/prototype/demo）与实现侧（plan/execute/finishing）技能，并用门禁避免上下文漂移、写错目录或在压力下跳过关键步骤。
---

# using-aisdlc（在 sdlc-dev 中使用 AI SDLC / Spec Pack 流程）

## 概览

这是一个“导航 + 门禁”型 Skill：用于在 sdlc-dev 的 Spec Pack（`{num}-{short-name}`）流程里，**选对下一步要用的 skill**，并用硬门禁防止上下文漂移与写错目录。

本 Skill 现在同时覆盖两条链路：

- **需求链路（R0–R4）**：`raw.md → solution.md → prd.md → prototype.md → demo/`
- **开发链路（I1–I2 + Finish）**：`solution.md → implementation/plan.md → 执行实现 → finishing-development`

**核心原则：**

- **先上下文，再读写**：凡读写 `{FEATURE_DIR}/requirements/*`、`{FEATURE_DIR}/design/*`、`{FEATURE_DIR}/implementation/*`（或 R4 写 demo）→ 先 `spec-context` 得到 `FEATURE_DIR`（失败就停止）。
- **一个节点 = 一个 skill = 一个落盘产物**：R0/R1/R2/R3/R4 分步执行，禁止“一次性把 PRD+原型+Demo 全做了”。
- **渐进式披露**：先读项目级 `memory/` 与相关契约索引；明确处理某个 Spec 后再读写 `{FEATURE_DIR}/requirements/*`。
- **不确定性不写“待确认问题清单”**：统一进入“验证清单”（Owner/截止/信号/动作）。
- **回流闭环**：R3/R4 的验证发现会回流更新 R1/R2/R3（必要时再做 R4）。
- **实现侧 SSOT**：实现阶段以 `{FEATURE_DIR}/implementation/plan.md` 作为**唯一执行清单与状态 SSOT**（checkbox + 审计信息）；执行状态只回写到 `plan.md`。

## 何时使用 / 不使用

- **使用时机**
  - 你要开始/继续一个 Spec：生成或更新 `raw.md / solution.md / prd.md / prototype.md / demo`
  - 你要把一个“简单需求”直接推进到开发闭环：`solution.md → plan.md → execute → finishing`
  - 你不确定“现在该跑哪个 spec-product-* skill”
  - 你不确定“现在该跑 spec-implementation-plan / spec-implementation-execute 还是先补需求输入”
  - 用户在施压时提出：不想跑脚本、直接给你路径、要求你先写再补上下文
- **不要用在**
  - 仅讨论概念、不涉及本仓库 Spec Pack 的落盘文件与目录结构

## 唯一门禁（必须遵守）

**规则：只要任务会读写以下任意内容，就必须先跑 `spec-context` 并回显 `FEATURE_DIR=...`：**

- `{FEATURE_DIR}/requirements/raw.md`
- `{FEATURE_DIR}/requirements/solution.md`
- `{FEATURE_DIR}/requirements/prd.md`
- `{FEATURE_DIR}/requirements/prototype.md`
- `{FEATURE_DIR}/design/*.md`（例如 `design/design.md`、`design/research.md`）
- `{FEATURE_DIR}/implementation/plan.md`
- `{REPO_ROOT}/demo/prototypes/{CURRENT_BRANCH}/...`（R4）

**即使用户口头给了 `FEATURE_DIR` 也不例外。**（基线压测中最常见的违规点：把“用户给的路径”当成可信上下文。）

> 命令书写约定：默认面向 PowerShell；同一行多命令请用 `;` 分隔（不要用 `&&`）。

## 你要的最短闭环（简单需求开发）：raw → solution.md → plan.md → execute → finishing-development

适用前提（满足其一即可）：

- **范围单一、边界清晰**，风险低，不需要额外设计阶段决策文档（可按 `design/aisdlc_spec_design.md` 的 D0 判定跳过 design）
- **验收口径可追溯**：至少能在 `solution.md`（或更完整的 `prd.md`）里写清楚验收点

最短闭环（建议先跑通）：

1. **R0：落盘 raw（如尚未建包）**
   - 用什么：`spec-init`
   - 输出：`{FEATURE_DIR}/requirements/raw.md`
2. **门禁：定位 Spec 上下文**
   - 用什么：`spec-context`
   - 要求：对话中必须回显 `FEATURE_DIR=...`；失败即停止
3. **R1：raw → solution（收敛方案）**
   - 用什么：`spec-product-clarify`
   - 输出：`{FEATURE_DIR}/requirements/solution.md`
   - 兼容说明：用户可能会说 `solutions.md`，但本仓库需求侧 SSOT 以 **`solution.md`（单数）** 为准；不要新建 `solutions.md` 造成双 SSOT
4. **I1：solution → plan（写到可执行）**
   - 用什么：`spec-implementation-plan`
   - 输出：`{FEATURE_DIR}/implementation/plan.md`（唯一执行清单与状态 SSOT）
5. **I2：按 plan 分批执行（实现 + 回写状态/审计）**
   - 用什么：`spec-implementation-execute`
   - 规则：执行状态只回写 `implementation/plan.md`；遇到 `NEEDS CLARIFICATION` / 阻塞即停
6. **Finish：开发收尾确认（仅验证，全绿才算完成）**
   - 用什么：`finishing-development`
   - 输出：一份“完成确认报告”（包含实际运行的命令与结果）

## 核心工作流（需求侧 R0 → R4；实现侧 I1 → I2 → Finish）

```dot
digraph aisdlc_flow {
  rankdir=LR;
  node [shape=box];
  "要处理某个需求（Spec）" -> "是否已有合法 spec 分支/Spec Pack？";
  "是否已有合法 spec 分支/Spec Pack？" [shape=diamond];
  "是否已有合法 spec 分支/Spec Pack？" -> "R0: spec-init" [label="否 / 不确定"];
  "R0: spec-init" -> "运行 spec-context" ;
  "是否已有合法 spec 分支/Spec Pack？" -> "运行 spec-context" [label="是"];
  "运行 spec-context" -> "得到 FEATURE_DIR / CURRENT_BRANCH / REPO_ROOT";
  "得到 FEATURE_DIR / CURRENT_BRANCH / REPO_ROOT" -> "选择需求链路 R1-R4（可选）";
  "得到 FEATURE_DIR / CURRENT_BRANCH / REPO_ROOT" -> "选择开发链路 I1-I2（必做）";
  "选择需求链路 R1-R4（可选）" -> "R1: raw->solution";
  "R1: raw->solution" -> "R2: solution->prd（可选）";
  "R2: solution->prd（可选）" -> "R3: prd->prototype（可选）";
  "R3: prd->prototype（可选）" -> "R4: prototype->demo（可选）";
  "R1: raw->solution" -> "I1: spec-implementation-plan";
  "R2: solution->prd（可选）" -> "I1: spec-implementation-plan";
  "R3: prd->prototype（可选）" -> "I1: spec-implementation-plan";
  "I1: spec-implementation-plan" -> "I2: spec-implementation-execute";
  "I2: spec-implementation-execute" -> "Finish: finishing-development";
}
```

### R0：初始化新 Spec Pack

- **用什么**：`spec-init`
- **什么时候**：还没有 `{num}-{short-name}` 分支与 `.aisdlc/specs/{num}-{short-name}/` 目录
- **输出**：`{FEATURE_DIR}/requirements/raw.md`（UTF-8 with BOM）
- **下一步**：`spec-context` → R1

### R1：澄清 + 方案决策（raw → solution）

- **用什么**：`spec-product-clarify`
- **前置输入**：`spec-context` 成功；`{FEATURE_DIR}/requirements/raw.md` 存在且非空
- **关键纪律**：一次一问（优先选择题）+ 增量回写 `raw.md/## 澄清记录` + 停止机制
- **输出**：`{FEATURE_DIR}/requirements/solution.md`
- **下一步**：
  - 需求还不够“可交付规格”→ R2（PRD，可选）
  - 交互/流程有歧义→ R3/R4（可选）
  - **简单需求要开发**→ 直接进入 I1（实现计划）

### R2：PRD（solution → prd，可选）

- **用什么**：`spec-product-prd`
- **前置输入**：`{FEATURE_DIR}/requirements/solution.md` 必须存在
- **输出**：`{FEATURE_DIR}/requirements/prd.md`
- **下一步**：按需 R3 或直达 design

### R3：原型（prd → prototype，可选）

- **用什么**：`spec-product-prototype`
- **前置输入**：`{FEATURE_DIR}/requirements/prd.md` 必须存在
- **输出**：`{FEATURE_DIR}/requirements/prototype.md`
- **下一步**：原型评审/最小验证；按需 R4；发现问题回流 R1/R2/R3

### R4：可交互 Demo（prototype → demo，可选）

- **用什么**：`spec-product-demo`
- **前置输入**：`{FEATURE_DIR}/requirements/prototype.md` 必须存在；Demo 工程根目录可定位（找不到就停止并要 `DEMO_PROJECT_ROOT`）
- **输出**：默认 `{REPO_ROOT}/demo/prototypes/{CURRENT_BRANCH}/`
- **下一步**：运行走查；发现问题回流更新 R1/R2/R3/R4

### I1：实现计划（solution/prd/design → plan.md，必做）

- **用什么**：`spec-implementation-plan`
- **前置输入**：`spec-context` 成功；`{FEATURE_DIR}/requirements/solution.md` 或 `prd.md` 至少其一存在（否则必须在 `plan.md` 标注 `NEEDS CLARIFICATION` 并阻断进入 I2）
- **输出**：`{FEATURE_DIR}/implementation/plan.md`（唯一执行清单与状态 SSOT）
- **下一步**：I2

### I2：执行（按 plan.md 分批实现并回写，必做）

- **用什么**：`spec-implementation-execute`
- **前置输入**：`{FEATURE_DIR}/implementation/plan.md` 必须存在且可执行；不存在/不可执行则回到 I1
- **输出**：代码与配置变更 + `plan.md` checkbox/审计信息回写（唯一状态来源）
- **下一步**：Finish

### Finish：开发收尾确认（仅验证，全绿才算完成）

- **用什么**：`finishing-development`
- **输出**：完成确认报告（实际运行的命令与结果可复现）

## Quick reference（高频速查）

| 你要做什么 | 必须先有 | 执行 skill | 主要产物 |
|---|---|---|---|
| 新需求建包 | 原始需求（文本或文件） | `spec-init` | `requirements/raw.md` |
| 收敛方案 | `raw.md` | `spec-product-clarify` | `requirements/solution.md` |
| 冻结交付规格 | `solution.md` | `spec-product-prd` | `requirements/prd.md` |
| 消除交互歧义 | `prd.md` | `spec-product-prototype` | `requirements/prototype.md` |
| 高保真走查 | `prototype.md` + 可运行 demo 工程根目录 | `spec-product-demo` | `demo/prototypes/{branch}/` |
| 写可执行计划（必做） | `solution.md` 或 `prd.md` | `spec-implementation-plan` | `implementation/plan.md` |
| 按计划实现（必做） | `implementation/plan.md` | `spec-implementation-execute` | 代码变更 + `plan.md` 回写 |
| 开发收尾确认（必做） | 代码已实现 + 计划任务已完成 | `finishing-development` | 完成确认报告 |

> 只要会读写 `{FEATURE_DIR}/requirements/*`、`{FEATURE_DIR}/design/*`、`{FEATURE_DIR}/implementation/*`，或 R4 写 demo：先 `spec-context`，失败就停止。

## 红旗清单（出现任一条：停止并纠正）

- 没跑 `spec-context` 就开始读写 `{FEATURE_DIR}/requirements/*`、`{FEATURE_DIR}/design/*`、`{FEATURE_DIR}/implementation/*`（或开始 R4 写 demo）
- 用户口头给了 `FEATURE_DIR`，你就“信了并跳过脚本”
- `spec-context` 报错仍继续（例如 main 分支也要“先写一版”）
- 为了赶进度先生成文档，事后再补上下文/再回头澄清
- 在 R4 找不到可运行 demo 工程根目录时，自行初始化 Vite/Next.js 工程“放你觉得合适的位置”
- 没有 `{FEATURE_DIR}/implementation/plan.md`（或 plan 不可执行）就开始“直接写代码”
- 执行中把状态/审计写到别处（issue/聊天记录/另一个文件），而不是回写 `implementation/plan.md`

## 常见错误（以及怎么修）

- **把“用户给的路径/分支名”当作上下文**：仍然必须 `spec-context` 回显 `FEATURE_DIR=...`；无法执行就停止。
- **先生成再回头澄清/补证据**：先完成 R1 澄清循环（一次一问 + 回写），达到 DoD 后再生成产物。
- **越级执行**：缺 `solution.md` 就写 `prd.md`，缺 `prd.md` 就写 `prototype.md`，缺 `prototype.md` 就做 demo → 一律停止并回到上一步。
- **越级开发**：缺 `implementation/plan.md` 就开始实现 → 回到 I1 写到“可执行 + 可验证 + 可审计”，再进入 I2。

## 常见借口与反制（来自基线压测）

| 借口（压力来源） | 常见违规行为 | 必须的反制动作 |
|---|---|---|
| “我已经把 FEATURE_DIR 告诉你了，别跑脚本” | 接受口头路径并直接写文件 | **仍然必须跑 `spec-context`**；跑不了就停止，只交付“阻断原因 + 需要的输入/下一步” |
| “我很急，先在 main 上写 solution.md” | 跳过门禁、猜目录写入 | `spec-context` 失败 → **停止**；先切到合法 spec 分支或先 `spec-init` |
| “把 PRD/原型/Demo 一次性都做了” | 节点耦合导致漂移、无法回流 | 拆成 R1→R2→R3→R4；每步完成给下一步与 DoD 自检 |
| “别写 plan 了，直接改代码吧” | 跳过 I1、执行不可审计、容易越界 | 先 `spec-implementation-plan` 产出 `implementation/plan.md`（SSOT），再 `spec-implementation-execute` 分批执行与回写 |

## 一个好例子（最短路径的正确开场）

用户：“我要做一个新需求，先出方案（solution.md），我不想自己找目录。”

正确做法（第一轮）：

- 若尚未创建 spec 分支/Spec Pack → 先 `spec-init`（把原始需求落到 `raw.md`）
- 然后执行 `spec-context` 并回显 `FEATURE_DIR=...`
- 进入 R1：对用户只问 **1 个最高杠杆选择题**；回答后增量回写 `raw.md/## 澄清记录`
- DoD 达标或触发停止机制后生成 `solution.md`，并给出下一步：
  - **简单需求要开发**：I1 `spec-implementation-plan` → I2 `spec-implementation-execute` → `finishing-development`
  - **需要更完整规格/原型**：R2/R3/R4（按需）后再进入 I1/I2

