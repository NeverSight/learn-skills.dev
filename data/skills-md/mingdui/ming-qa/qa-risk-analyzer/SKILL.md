---
name: qa-risk-analyzer
description: >
  在测试用例设计之前，先识别高风险业务路径和必需的验证断言（oracle）。分析需求文档、代码 diff、已有用例和上下文，
  找出资金/权限/状态机/并发/异步/数据一致性等高危区域，输出每条风险的 businessPath、requiredAssertions、suggestedTestLayers，
  以及覆盖率缺口。不要在风险未明确前写业务用例。
  不适用：写业务用例、写测试代码、修改产品代码。
---

# QA Risk Analyzer — 风险分析

> **CLI 调用约定**：本工具包的 CLI 是 `quality-assurance-agent/scripts/qa_agent.py`。
> 它**不以 PATH 命令的形式分发**——命令由你（agent）执行，人不必手敲。
> 开工前解析一次 skill 目录，之后所有命令一律写成
> `python "$QA_AGENT_DIR/scripts/qa_agent.py" <cmd>`：
>
>     QA_AGENT_DIR="${QA_AGENT_CLI:-$(dirname "$(find ~/.claude/skills ~/.agents/skills ~/.codex/skills .claude/skills .agents/skills .codex/skills -maxdepth 2 -name SKILL.md -path '*quality-assurance-agent/*' 2>/dev/null | head -1)")}"
>
> 运行环境若已告知本 skill 目录（Claude Code 会），直接用，不必跑上面的查找。
> 完整命令语法见 `$QA_AGENT_DIR/references/cli-reference.md`。

## 你的定位

你的任务是**在写用例之前先找 bug 思路**。如果你跳过这步直接写用例，用例会变成机械覆盖 API 参数而非针对业务风险的防守性测试。
你的产出不是"一个必须交的 JSON 文件"，而是后续 `qa-testcase-designer` 的判断依据——每条 P0/P1 风险必须要么有一条对应用例，要么是一条明确记录的 open question。

你不上手修代码，不自己跑测试，不做 Ready 判定。

## CLI 命令

本阶段所有命令的完整语法、参数说明见**主 skill（quality-assurance-agent）→ CLI 命令参考 → 阶段 1**。这里不重复维护命令语法。

## --module 参数的使用约定

这是本阶段最关键的一个参数选择：

- **验收已有模块**：**必须带 --module**，逗号分隔列出目标代码文件（绝对路径、相对路径、目录路径或 glob）。这样 `affectedFiles` 只包含你真正关心的代码，不会混入全仓库 160 个无关文件。
- **开发新功能、有 git diff**：不带 --module，工具会自动从 git diff 提取变更文件。
- **裸跑（不带 --module 且无 diff）**：工具回退到全仓库关键词扫描，结果中 `businessPath` 全是"待映射到业务操作路径"，`affectedFiles` 包含大量 skill/doc/config 文件——**这种情况产出的 risk-analysis.json 不能直接使用**，必须手工重写。

## 工作流

### 1. 前置检查

确保 `.qa-agent/current/context.json` 和 `.qa-agent/current/existing-case-index.json` 存在。需要时读 `manifest.json` 确认上游阶段已完成。如果缺失，先退回 `qa-context-profiler`。

### 2. 加载历史缺陷模式（bug-pattern）

读 `.qa-agent/knowledge/` 下的 `bug-pattern` 类经验，了解本项目历史上出过什么 bug、根因、修法：

```bash
python "$QA_AGENT_DIR/scripts/qa_agent.py"show-knowledge --repo . --module <module> --category bug-pattern
```

读代码时把这些历史缺陷模式当作**优先验证点**——历史上"并发扣款没加锁"出过 bug，这次扫到资金代码就重点查行锁。历史缺陷不是风险定论，而是把"盲扫"变成"带着怀疑查"。

### 3. 深入读代码，做因果推理

不要只看 context.json 的文件列表。用 Read 工具把 scope 内的核心实现文件全部读一遍——Controller、Service、Mapper XML、DTO/VO、前端页面组件和 service 层。

**关键词匹配不是风险分析。** 读代码时按 `references/code-reading-checklist.md` 的六大维度逐文件审查：资金流转、状态机、并发窗口、权限边界、异步链路、异常路径。

### 4. 运行 analyze-risks，产出骨架

带 --module 运行命令。工具产出的是**关键词匹配的风险骨架**——它告诉你"哪些文件匹配了 money/permission/async 等关键词"，但不做因果推理。

### 5. 手工增强骨架

工具的原始产出不能直接用于下游。你必须：
- 给每条风险填具体的 `businessPath`（例如"POST /orders/create → createOrder → 库存校验 → selectForUpdate → 扣款 → 流水记录"而不是"待映射到业务操作路径"）
- 给 `requiredAssertions` 填具体的可验证断言（例如"最新 t_user_usd_balance_log 记录的 change_amount 绝对值等于 totalDeducted"而不只是"金额计算正确"）
- 把工具的 `affectedFiles` 从 160 个无关文件裁剪为真正相关的 5-10 个代码文件
- 给 `coverageStatus` 标注真实状态（"missing" 如果没有任何已有用例覆盖，"partial" 如果有部分覆盖）
- 对前端交互类风险（`suggestedTestLayers` 含 e2e，或 affectedFiles 含 `.tsx/.vue/.html`）标注 `requiresE2E: true`——这会强制 script-generator 即使 acceptance-mode 也生成 e2e task，UI 行为断言不会被降级成 api 层
- **`category` 只用固定枚举**（收敛，不随意新增）：`permission-boundary | money-reward-settlement | state-transition | async-callback-retry | data-consistency | negative-path | concurrency | provably-fair | business-rule | privacy`。中文随枚举定义在报告渲染层，你不需要（也不应该）自己造新类别——新风险归类到最接近的既有枚举，确有全新类别才和工具链维护者协商新增枚举。

### 6. 写 coverageGaps 和 requiredOracles

每条 missing/partial 的风险生成一条 coverage gap，带 requiredAssertions。
按 oracle 类型分类：ui、api、db、sideEffects、negativeAssertions。
这些会直接进入 spec-task 的 oracle 字段和断言设计。

### 7. 产物移交

产物落地：`.qa-agent/current/risk-analysis.json`。
运行后 `manifest.json` 会自动更新为 `currentStage: risk-analyzer` 并记录产物路径。

向下游反馈：**P0/P1 风险必须映射到 `qa-testcase-designer` 的业务用例或 open question。未映射的风险不能因为"忘记了"而遗漏。**

## 容错与降级

- **上游产物缺失**：`context.json` 或 `existing-case-index.json` 不存在时，退回 `qa-context-profiler` 补齐，不静默跳过。
- **工具裸跑结果不可用**：不带 `--module` 且无 git diff 时的全仓库扫描结果不可直接传给下游——必须手工重写 `businessPath` 和 `affectedFiles`。
- **编码损坏**：`risk-analysis.json` 写完必须跑 `check-mojibake --strict`。检出 U+FFFD → `safe-write-json` 重写。
- **MCP/Read 工具不可用**：无法读代码文件时，记录为 blocker，不凭空编造风险。

## 禁令

- **不写用例，不写测试，不修改产品代码**。你现在唯一产出的就是 risk-analysis.json。
- **不凭空说"这里有个 bug"**。如果只有代码迹象但没有执行证据，用 "risk" 或 "potentialBug" 措辞，不要下确定性判断。
- **不把工具裸跑结果当最终风险定论直接传给下游**。关键词匹配不是代码审查。
- **不降级 P0/P1 风险**。资金、权限、状态损坏、重复奖励、数据一致性、安全问题——除非你有对抗证据，否则保持原优先级。
- **如果没有发现任何风险**，仍然输出一个显式声明了 scope 和证据的空 risk-analysis.json。不要跳过。
