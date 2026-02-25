---
name: openspec-parallel-agents
description: Use when OpenSpec workflows need dependency-aware parallel subagents across OPSX commands, legacy openspec commands, and Codex CLI prompt aliases.
---

# OpenSpec Parallel Agents

## 概述

该技能用于 OpenSpec 的并发子代理编排，兼容三类入口：

1. OPSX 新命令（`/opsx:*`）
2. 旧版命令（`/openspec:*`）
3. Codex CLI 提示词命令（`/prompts:*`）

目标是同时覆盖新旧命令语义，并在多 change 场景下安全并发、受控汇总、避免写冲突。

## 命令兼容矩阵（必须识别）

| 场景 | 命令形态 | 说明 |
|---|---|---|
| OPSX 新版 | `/opsx:explore` `/opsx:new` `/opsx:continue` `/opsx:ff` `/opsx:apply` `/opsx:verify` `/opsx:sync` `/opsx:archive` `/opsx:bulk-archive` `/opsx:onboard` | 当前主流程 |
| Legacy 旧版 | `/openspec:proposal` `/openspec:apply` `/openspec:archive` | 兼容旧工作流 |
| Codex CLI（新） | `/prompts:opsx-explore` `/prompts:opsx-new` `/prompts:opsx-continue` `/prompts:opsx-ff` `/prompts:opsx-apply` `/prompts:opsx-verify` `/prompts:opsx-sync` `/prompts:opsx-archive` `/prompts:opsx-bulk-archive` `/prompts:opsx-onboard` | 对应 `~/.codex/prompts/opsx-<id>.md` |
| Codex CLI（旧） | `/prompts:openspec-proposal` `/prompts:openspec-apply` `/prompts:openspec-archive` | 历史提示词写法，需兼容 |

## 旧命令到新流程映射

1. `/openspec:proposal` 或 `/prompts:openspec-proposal`
- 等价到“创建规划产物”语义。
- 推荐映射为：`/opsx:new` + `/opsx:ff`（或按需 `/opsx:continue` 逐步创建）。

2. `/openspec:apply` 或 `/prompts:openspec-apply`
- 直接映射到 `/opsx:apply`。

3. `/openspec:archive` 或 `/prompts:openspec-archive`
- 直接映射到 `/opsx:archive`。

## Codex CLI 特殊处理

1. Prompt 文件目录优先识别 `$CODEX_HOME/prompts`，否则使用 `~/.codex/prompts`。
2. 若同义命令同时存在新旧别名，优先采用 OPSX 语义执行，并在汇总中注明“兼容入口触发”。
3. 对 `/prompts:*` 入口，参数可能以整串形式传入；无法唯一定位 change 时必须先做 change 选择，不得猜测。

## 触发条件

满足任一条件即启用：

1. 同时处理 2 个及以上 change，且部分任务可独立执行。
2. 需要批量归档或归档前检查（尤其 `/opsx:bulk-archive`）。
3. 任务中同时存在可并行节点与强依赖链。
4. 用户使用上表中的任一新旧命令，并明确要求并行子代理执行。

## 并发执行规则

1. 每轮默认拆分 3-6 个子任务；不足 3 个必须说明改串行原因。
2. 仅并发无前置依赖节点；强依赖链必须串行。
3. 禁止并发写同一文件重叠区域；发现冲突风险立即降级串行。
4. 归档与规格合并涉及共享索引时，最终提交必须串行。
5. 一轮并发必须全量返回后统一汇总，不允许边返回边跨轮推进。

## 命令级策略

### 新命令（`/opsx:*`）

- `/opsx:new`：可并发创建互不依赖 change。
- `/opsx:ff`：按 change 分组并发生成规划产物。
- `/opsx:apply`：按模块边界并发实现。
- `/opsx:verify`：可并发验证各 change，再统一裁决。
- `/opsx:archive`：归档前检查可并发，最终归档串行提交。
- `/opsx:bulk-archive`：先并发做健康检查，再按冲突顺序串行归档。

### 旧命令（`/openspec:*`）

- 保留用户入口，不强制要求用户改命令。
- 执行时按“旧到新映射”转换为 OPSX 语义并应用同一并发规则。

### Codex CLI（`/prompts:*`）

- 新旧 prompt 名称均识别。
- 调度规则与 `/opsx:*` 一致，仅入口别名不同。

## 标准循环

1. 识别入口类型（OPSX / Legacy / Codex Prompt）。
2. 标准化为 OPSX 语义（必要时做旧命令映射）。
3. 依赖分析并拆分 3-6 个无冲突任务卡。
4. 并发执行可并行节点。
5. 汇总冲突、阻塞、风险，决定下一轮并行或转串行。

## 轮次汇总模板

```markdown
## 第 {N} 轮汇总

### 触发入口
- 原始命令: {如 /openspec:proposal 或 /prompts:opsx-apply}
- 规范化语义: {对应 /opsx:*}

### 本轮目标
- {一句话目标}

### 子任务状态（3-6）
1. {任务A} | {完成/阻塞/失败} | 产出: {文件或结果}
2. {任务B} | {完成/阻塞/失败} | 产出: {文件或结果}
3. {任务C} | {完成/阻塞/失败} | 产出: {文件或结果}

### 冲突与处理
- 写冲突检查: {无/有，位置}
- 处理动作: {重排并发/改串行/拆分边界}

### 依赖链状态
- 串行链: {A -> B -> C}
- 当前推进: {节点}

### 下一轮计划
- 并行任务: {列表}
- 串行任务: {列表}
- 归档准备状态: {可归档/不可归档 + 原因}
```
