---
name: aile-writing-plans
description: 面向团队工作流的写计划技能（阶段2）。在开发前，将 Jira Story + UI 示意细化为可执行计划，并输出到 docs/plans/{Story-Key}/plan.md
---

# Aile：写计划（aile-writing-plans）

## 概述

这是团队自有的计划产出技能，用于把阶段 1（PM 需求 + UI 示意）的输入，转化为阶段 2 的标准化产物：

- 计划主入口：`docs/plans/{Story-Key}/plan.md`
- 可选设计文件：`docs/plans/{Story-Key}/design.pen`

假設工程師對我們的程式碼庫的背景為零且品味有問題，則編寫全面的實施計劃。記錄他們需要知道的一切：每個任務要接觸哪些文件、程式碼、測試、他們可能需要檢查的文檔、如何測試它。將整個計劃作為小任務交給他們。乾燥。亞格尼。時分驅動。頻繁提交。

假設他們是一位熟練的開發人員，但對我們的工具集或問題領域幾乎一無所知。假設他們不太瞭解良好的測試設計。

## 何时使用

在以下情形使用：

- 你已经拿到 Jira Story 的需求描述与（至少）UI 示意/交互说明
- 需要产出可被执行的、任务颗粒度 2-5 分钟的实施计划
- 需要把验收标准（AC）从业务视角细化为技术可测试视角，并回写到 Story（如启用 Jira MCP）

## 核心产出契约（必须遵守）

1. 计划文件必须落在：`docs/plans/{Story-Key}/plan.md`
2. 文件必须包含：
   - 状态管理（整体进度、任务状态总览、执行记录）
   - 需求理解与风险
   - UI 设计（有 UI 变更则必须有 `design.pen` 或明确写“本 Story 无 UI 设计”）
   - 任务拆解（每个任务 2-5 分钟）
   - 测试用例与验收标准（可测试、无歧义）
   - AI 执行指引（明确执行顺序、约束、人工 Gate 节点）
3. 每个任务必须以 TDD 方式描述：RED → 验证失败 → GREEN → 验证通过 → REFACTOR → 再次验证
4. 启用 Jira MCP 时：任务拆解后必须为每个实施任务创建 Jira Sub-task，并回填到 `plan.md` 的 Jira 关联章节
5. 状态管理必须可追踪：每个任务都要有 `状态`、`负责人`、`开始时间`、`完成时间`、`阻塞原因`，初始状态统一为 `待开始`

## 一口大小的任務粒度

**每一步都是一個動作（2-5 分鐘）：**
- “編寫失敗的測試”-步驟
- 「運行它以確保它失敗」-步驟
- “實現最少的程式碼以使測試通過” - 步驟
- “運行測試並確保它們通過”- 步驟
- “提交”-步驟



## Jira 子任务契约（启用 MCP 时）

创建 Sub-task 使用 `jira_create_issue`，并满足最小字段：

- `summary`：与任务名一一对应（便于追踪）
- `description`：任务目标、范围、验收要点
- `parent`：父 Story Key（例如 `ABC-123`）
- `labels`：至少包含 Story-Key 与阶段标签（例如 `stage2-planning`）
- `assignee`：可选；若未知可留空并在 `plan.md` 标注待分配

执行失败时必须降级为“仅本地产出 + 人工补录”，不得声称已完成 Jira 同步。

## 执行流程

**开始时声明：**“我正在使用 aile-writing-plans 技能来生成团队计划。”

### Step 0：读取上下文

- 读取 `docs/README.md` 与相关模块文档（如影响范围涉及 `docs/modules/*`）
- 读取（如存在）`docs/specs/PRD.md`、`docs/specs/SAD.md`
- 读取（如存在）本 Story 之前的计划产物（`docs/plans/{Story-Key}/`）

### Step 1：确认 Story-Key 与范围边界

- 明确 Story-Key（例如 `ABC-123`），作为目录名
- 明确“做什么 / 不做什么”（YAGNI：把不需要的需求从计划中删掉）

### Step 2：任务拆解与排序

- 任务粒度：单任务 2-5 分钟
- 输出：每个任务明确文件路径、测试、验证命令、预期输出
- DRY：复用现有模式，不新增不必要抽象

### Step 3：写入计划文件

将内容写入 `docs/plans/{Story-Key}/plan.md`，并确保其结构符合团队模板（参考 `docs-templates/stage2-plan-template.md`）。

- 初始化状态管理模块：
  - 填写“整体进度”
  - 建立“任务状态总览”（所有任务默认 `待开始`）
  - 建立“执行记录”并写入首条记录

### Step 6：创建 Jira Sub-task（可选）

- 前置条件：Jira MCP 可用，且已确认父 Story Key
- 按任务列表逐条调用 `jira_create_issue` 创建 Sub-task
- 创建时写入字段：`summary`、`description`、`parent`、`labels`、`assignee`（可选）
- 将创建结果回填 `plan.md`：
  - 成功：记录 Sub-task Key（如 `ABC-234`）
  - 失败：记录“未创建（原因：xxx，需人工补录）”

### Step 6：Jira MCP 回写状态（可选）
- Jira状态变更时调用 `jira_update_issue` 更新对应 Story 的状态字段为 developing


### Step 7：交接到执行阶段

- 推荐后续执行技能：`aile-tdd` 或 `aile-subagent-dev`
