---
name: spec-implementation-execute
description: Use when 需要在 sdlc-dev 的 Spec Pack 中执行 I2（实现执行），以 `{FEATURE_DIR}/implementation/plan.md` 为唯一 SSOT 分批实现、运行最小验证、回写审计信息，并在批次检查点汇报；遇阻塞/澄清项立即停止。
---

# spec-implementation-execute（I2：执行 / plan.md SSOT）

## 概览

I2 的目标是把 `{FEATURE_DIR}/implementation/plan.md` 中的任务**按批次执行**，并把执行状态与最小审计信息**只回写到 `plan.md`**（作为唯一执行清单与状态 SSOT）。

本技能是 `skills/executing-plans/SKILL.md` 的 Spec 实现阶段版：**重度复用其“五步执行 + 批次检查点 + 遇阻塞即停”骨架**，但将“计划文件”的语义替换为实现阶段 SOP（见 `design/aisdlc_spec_implementation.md`）的硬约束：

- `plan.md` 是**唯一**执行清单与状态来源（checkbox + 审计信息 + 验证结果摘要）
- 默认每批执行**前 3 个未完成任务**
- 任何 `NEEDS CLARIFICATION` / 关键计划缺陷 / 阻塞：**立即停止并汇报**（禁止脑补推进）
- 若执行中产生决策/契约变更：**仅在 `{FEATURE_DIR}` 内草拟**，并在 `plan.md` 追加 **Merge-back 待办清单**（本阶段禁止直接更新 `project/*`）

**开始时宣布：**「我正在使用 spec-implementation-execute 技能按 plan.md 分批执行并回写 SSOT。」

## 何时使用 / 不使用

- **使用时机**
  - 已有 `{FEATURE_DIR}/implementation/plan.md`（I1 已完成），现在进入 I2 按任务实现。
  - 你需要在执行中严格做“批次检查点汇报”，并把状态/审计回写到 `plan.md`。
- **不要用在**
  - `spec-context` 失败、拿不到 `FEATURE_DIR`（此时必须停止）。
  - `plan.md` 不存在，或缺少可执行的任务清单（此时回到 I1：`spec-implementation-plan`）。
  - `plan.md` 的 `NEEDS CLARIFICATION` 仍未消除、或存在关键缺陷导致无法开始（此时必须先停止并提出澄清/修计划）。

## 门禁 / 停止（严格执行）

**REQUIRED SUB-SKILL：先执行 `spec-context` 并在对话中回显 `FEATURE_DIR=...`。**

```powershell
$repoRoot = (git rev-parse --show-toplevel)
. (Join-Path $repoRoot "skills\spec-context\spec-common.ps1")
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

立刻停止（满足其一即可）：

- 未得到 `FEATURE_DIR`
- 当前分支是 `main/master`（或你未得到用户明确同意在主分支实施）
- `{FEATURE_DIR}/implementation/plan.md` 不存在或不可读
- `plan.md` 中存在未消除的 `NEEDS CLARIFICATION`，且其会阻断继续执行
- 计划存在关键缺陷：缺失可执行命令/缺失最小验证/范围不清/依赖不明，导致无法安全开始
- 执行中遇到阻塞：缺依赖/权限/环境/数据、测试反复失败、某条指令不理解

**寻求澄清，而非猜测。**

## 输入 / 输出（落盘约定）

- **读取（渐进式披露，最少必要）**
  - `{FEATURE_DIR}/implementation/plan.md`（必须；SSOT）
  - `plan.md` 引用到的 `{FEATURE_DIR}/requirements/*`、`{FEATURE_DIR}/design/*`（按需读取，不要全量展开）
  - 项目级索引（只读，按需）：`project/memory/*`、`project/contracts/`、`project/adr/`
- **写入（唯一状态来源）**
  - **只把状态/审计写回** `{FEATURE_DIR}/implementation/plan.md`：勾选任务、补齐 `commit/pr/changed_files`、记录关键验证结果摘要与阻塞取证路径
- **代码与配置变更**
  - 按 `plan.md` 每任务声明的路径实现（创建/修改/测试）
- **Spec 内决策/契约草案（如执行中产生）**
  - ADR 草案：优先写到 `{FEATURE_DIR}/design/design.md` 的“决策/权衡”段；必要时新增 `{FEATURE_DIR}/design/adr/*.md`
  - 契约草案：写到 `{FEATURE_DIR}/design/contracts/`
  - 同步要求：在 `plan.md` 追加/更新 “Merge-back 待办清单”（仅记录，不在 I2 直接改 `project/*`）

> 命令书写约定：默认面向 PowerShell；同一行多命令请用 `;` 分隔（不要用 `&&`）。

## 流程（重用 executing-plans 的五步骨架）

### 步骤 1：加载并审查计划（Review）

1. 打开并阅读 `{FEATURE_DIR}/implementation/plan.md`
2. 严格审查——识别任何会阻断执行的问题或疑虑，例如：
   - 任务未写清“改哪些文件/跑什么命令/期望看到什么信号”
   - 缺失最小验证方式或验证不可执行
   - 任务越界（与 plan.md 的范围 / 里程碑不一致）
   - 依赖/权限/环境未满足
   - `NEEDS CLARIFICATION` 未消除
3. 若有关键疑虑：**在开始前停止并汇报**（把问题写清、给出取证路径；必要时回到 I1 修订 plan.md）
4. 若无疑虑：创建 TodoWrite 并进入批次执行

### 步骤 2：执行批次（Batch execute）

**默认：前 3 个未完成任务**（可根据风险与依赖调整，但必须解释原因）。

对每个任务：

1. 标记为 in_progress
2. **严格按任务步骤执行**（不要跳步；不要替换命令；不要暗改验收）
3. 按任务声明运行最小验证，并记录关键输出/信号（PASS/FAIL 的判据）
4. **频繁提交**（如果计划要求更细提交点，优先按计划来）
   - Commit message **必须中文**
5. 回写 `plan.md`（唯一状态来源）：
   - `- [ ]` → `- [x]`
   - 补齐 `commit/pr/changed_files`
   - 记录该任务的关键验证结果摘要（含命令与关键信号）
   - 若阻塞：写清“缺什么、如何补齐、向谁/从哪取证”，并停止进入下一任务
6. 标记为 completed（或 blocked）

### 步骤 3：批次检查点报告（Report checkpoint）

批次完成时必须汇报：

- 已完成任务列表（对应 Task ID）
- 验证结果摘要（关键命令 + 关键输出/信号）
- `plan.md` 已回写的位置与审计信息（commit/pr/changed_files）
- 未完成任务概览
- 阻塞项清单（如有）

然后说：「准备好反馈。」并**等待反馈**后再继续下一批。

### 步骤 4：继续 / 回到审查（Continue / Re-review）

根据反馈：

- 如对计划做了更新或出现新的关键疑虑：返回 **步骤 1** 重新审查
- 否则：执行下一批并重复步骤 2–3，直至任务清单处理完毕

### 步骤 5：完成开发（Finish）

当 `plan.md` 中计划内任务全部完成且最小验证通过后：

- 宣布：「我正在使用 finishing-development 技能做开发收尾确认（仅验证，确保测试/检查全绿）。」
- **必需子技能：** 使用 `finishing-development`
- 产物要求：确保 `plan.md` 的审计信息完整可追溯（至少包含 `commit` 与关键验证结果摘要；若有 PR 则补齐 `pr`）

## 何时停止并寻求帮助（Stop on block）

**立即停止执行：**

- 批次中遇到阻塞（缺失依赖/权限/环境/数据）
- 测试或验证反复失败（无法在当前证据下定位或修复）
- 不理解某条指令或验收口径
- 发现 `plan.md` 有关键缺陷（无法继续安全执行）
- 发现/新增 `NEEDS CLARIFICATION` 会影响正确性或范围

**寻求澄清，而非猜测。**

## 何时返回 earlier 步骤

**返回审查（步骤 1）时：**

- 协作方根据你的反馈更新了 `plan.md`
- 你需要对任务顺序/拆分做调整才能继续（必须先在 `plan.md` 明确化，再执行）
- 根本方案需要重新考虑（先停、再修计划/补证据）

## 牢记

- 始终先 `spec-context` 拿到 `FEATURE_DIR=...`，失败就停止
- `plan.md` 是唯一执行清单与状态 SSOT：**不要另起“状态来源”**
- 严格按 `plan.md` 步骤执行；不要跳过验证
- 默认每批前 3 个未完成任务；批次之间只汇报并等待
- 遇到阻塞/澄清项立刻停止，不要猜测推进
- 执行中产生 ADR/契约：只在 `{FEATURE_DIR}` 内落盘草案，并在 `plan.md` 记录 Merge-back 待办（I2 不直接改 `project/*`）

## 集成

**上游 / 下游技能：**

- `spec-implementation-plan` - 生成 `{FEATURE_DIR}/implementation/plan.md`（SSOT）
- `finishing-development` - 所有任务完成后做开发收尾确认

