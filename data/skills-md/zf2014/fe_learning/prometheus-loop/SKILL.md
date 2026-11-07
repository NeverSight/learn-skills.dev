---
name: prometheus-loop
description: Use when setting multi-step goals, running complex projects, or enabling autonomous AI-driven development that requires iterative plan-execute-verify cycles.
---

# Prometheus Spec-Driven Loop 技能

## 概述

**Prometheus Spec-Driven Loop** 是一个自驱动系统，能够接受高层目标，并自主经历规范定义（Spec）、计划、执行、验证和决策循环，直到目标完成。

**核心理念**：你不再手动提示 Agent——你设计让 Agent 自主循环。

**9 阶段流程**：
```
用户: "/prometheus-loop 实现博客系统，CRUD+评论+标签"
→ Loop: Parse Goal → Specify (含 Clarify 子阶段) → Plan → Review →
  Execute → Verify → Fidelity Check → Route →
  Loop back until all subgoals done → Complete
```

**关键改进**（相较于原始 7 阶段流程）：

| 改进 | 说明 |
|------|------|
| **Spec/Plan 分离** | 新增 Specify 阶段，明确定义"做什么"（Spec）与"怎么做"（Plan） |
| **批量澄清机制** | Specify 阶段内的 Clarify 子阶段，批量收集歧义并一次性提交用户确认 |
| **保真度验证** | 新增 Fidelity Check 阶段，验证实现结果与 Spec 的保真度 |
| **可追溯性** | Spec → Plan → Execution → Verification 全链路可追溯 |

**所需 Agent**（均为内置）：
- Prometheus — 战略规划
- Sisyphus（`/start-work`）— 计划执行
- Momus — 对抗性验证

---

## 触发模式（Trigger Patterns）

在以下情况使用此技能：
- 设定长期目标，让系统自主执行
- 运行复杂的多步骤项目，无需手动逐步骤提示
- 将大型任务分解为带依赖链的 subgoal
- 从上次会话恢复部分完成的目标
- 自主验证执行结果并迭代改进

**触发格式**：`/prometheus-loop {目标描述}` 或 `启动 Prometheus Loop: {目标描述}`

### 何时不使用

- **简单的单步骤任务**——改用常规的 `/writing-plans` 工作流。Loop 的开销（解析→规划→审查→执行→验证→路由）对于适合一个 Plan 的任务来说是浪费。
- **探索性或研究性工作**——先使用 `/brainstorming` 或 `/grill-me`。Loop 需要明确的目标；模糊的目标会导致重复的 REQUIREMENT_CHANGE 升级。
- **一次性运维操作**（配置更改、单次部署、快速修复）——无需迭代循环。直接执行即可。
- **Pull Request 审查/集成验证**——改用 `/review-work`。Loop 是为构建而设计的，而非审查。
- **用户需要手动检查点**——Loop 本质上是自主的。如果你需要批准每个阶段，说明在对抗架构设计。

---

## 9 阶段循环流程

### 阶段 1：解析目标（Parse Goal）

**作用**：从用户输入中提取目标描述，创建 Goal Registry 条目。

**步骤**：
1. 解析用户的目标描述（标题、可选详细信息）
2. 调用 `goals:init`（参见 [`commands.md`](./commands.md)），在 `.omo/goals/active/{goalId}.json` 中创建新目标
3. 如果用户提到子步骤，通过 `goals:add-subgoal` 添加，可通过 `specRef` 参数关联 Spec（可选）
4. 如果子步骤有依赖关系，设置 `blockedBy` 链
5. 报告：目标已注册，包含 N 个子目标

**示例**：
```
用户: "/prometheus-loop 实现博客系统，需要数据层、API 层、前端页面"
→ goals:init "实现博客系统" "数据层 + API 层 + 前端页面"
→ goals:add-subgoal blog-system "数据层" "" --specRef "spec-001"
→ goals:add-subgoal blog-system "API 层" "" --specRef "spec-001"
→ goals:add-subgoal blog-system "前端页面" "" --specRef "spec-001"
→ goals:update-subgoal blog-system sg-002 blockedBy '["sg-001"]'
→ goals:update-subgoal blog-system sg-003 blockedBy '["sg-002"]'
```

---

### 阶段 2：规范定义（Specify）← 新增

**作用**：创建或加载 Spec（规范文档），明确"要做什么"，为后续 Plan（怎么做）提供精确输入。

**步骤**：
1. 读取当前 subgoal，检查是否已关联 Spec（`specRef` 字段）
2. 如果已有 Spec → 加载并确认 Spec 状态
3. 如果无 Spec → 创建 Spec 文档到 `.omo/specs/{specName}/spec.md`
4. Spec 文档必须包含：
   - **用户故事**：P1/P2/P3 优先级分类
   - **功能需求**：FR-{NNN} 格式，每个需求含可验证的验收标准
   - **成功标准**：可衡量的完成条件
5. 如果检测到歧义 → 进入 **Clarify 子阶段**（见下文）

#### Clarify 子阶段 ← 新增

**作用**：批量收集 Spec 中的歧义问题，一次性提交用户确认，避免多次打断。

**触发条件**：Spec 中存在以下情况时触发：
- 需求描述存在多种合理解读
- 验收标准缺少客观判断条件
- 用户故事优先级不明确
- 范围边界模糊

**流程**：

```
1. 批量收集 Spec 中所有[NEEDS CLARIFICATION]标记
2. 将所有歧义问题整理为结构化列表（每个问题含上下文和可选方案）
3. 一次性提交给用户：
   - 问题列表（建议不超过 5 个，优先最关键的问题）
   - 每个问题给出推荐选项
   - 告知用户如果超时未响应将使用默认值
4. 等待用户响应（超时时间：config.clarifyTimeoutMin，默认 30 分钟）
5. 用户响应后：
   - 将 Q&A 记录写入 Spec 的 Clarification History 章节
   - 更新 Spec 状态为 `clarified`
   - 消除所有歧义标记，继续后续流程
6. 如果超时：
   - 使用默认值填充所有未回答问题
   - 将 Spec 标记为 `isAssumed: true`
   - 记录超时事件到 Clarification History
   - 继续后续流程（不阻塞）
```

**重要**：Clarify 是批量机制——收集所有歧义后一次性提交，而非每发现一个问题就打断用户。

**示例**：
```
用户正在查看 Spec
→ Agent 检测到 3 个歧义点
→ Agent 整理问题列表：

  问题 1: "数据层"是否包含缓存层？
  选项 A: 包含 Redis 缓存  B: 仅数据库访问层  C: 不确定
  
  问题 2: API 层是否需要 GraphQL 支持？
  选项 A: 仅 REST  B: 仅 GraphQL  C: 两者都支持
  
  问题 3: 前端页面是否需要移动端适配？
  选项 A: 仅桌面端  B: 响应式设计  C: 独立移动端页面

→ 用户选择: A, A, B
→ Spec 已更新，Clarification History 已记录
→ Spec 状态: clarified
→ 继续到 Plan 阶段
```

---

### 阶段 3：计划制定（Planning Phase）

**作用**：Prometheus 为当前 subgoal 创建详细的 Plan（计划文档），Plan 引用 Spec 而非重新定义需求。

**步骤**：
1. 通过 `goals:next {goalId}` 读取当前 subgoal
2. 如果无 subgoal 就绪，报告：目标被阻塞或已完成
3. 检查 subgoal 是否关联 Spec（`specRef` / `specPath` 字段）
   - 如果有关联 → 加载 Spec，作为 Plan 的输入
   - 如果无关联 → 按传统方式直接从需求规划
4. 将 subgoal 呈现给 Prometheus 进行规划
5. Prometheus 生成 Plan → 保存到 `.omo/plans/{subgoalId}.md`
6. Plan 中引用 Spec 的 ID（`specRef`），而非重新抄写需求
7. 通过 `goals:update-subgoal {goalId} {subgoalId} planRef ".omo/plans/{subgoalId}.md"` 更新 subgoal

**Spec 与 Plan 的职责区分**：

| 文档 | 回答的问题 | 存储位置 | 内容 |
|------|-----------|---------|------|
| Spec | 做什么（What） | `.omo/specs/{name}/spec.md` | 用户故事、功能需求、验收标准 |
| Plan | 怎么做（How） | `.omo/plans/{subgoalId}.md` | 实施步骤、技术方案、QA 场景 |

---

### 阶段 4：Momus 审查（Momus Review）

**作用**：Momus 在执行前对抗性审查 Plan。

**步骤**：
1. 从 `.omo/plans/{subgoalId}.md` 加载 Plan 文件
2. 如果 Plan 关联了 Spec，也加载 Spec 供 Momus 参考
3. 调用 Momus 审查 Plan：
   - Plan 是否完整且正确？
   - 验收标准是否具体可执行？
   - QA 场景是否可由 Agent 执行？
   - Plan 是否忠实于 Spec 的定义？（不偏离原始需求）
4. 如果 Momus **通过** → 进入阶段 5
5. 如果 Momus **拒绝** → 捕获 Verdict，进入阶段 8（Router），类型为 PLAN_ISSUE

**重要**：Plan 必须在 Momus 审查通过后方可执行。审查是安全门。

---

### 阶段 5：自动执行（Auto-Execute）

**作用**：自动执行 Plan——无需手动调用 `/start-work`。

**步骤**：
1. 更新 subgoal 状态为 `in_progress`
2. 将 Plan 传递给执行器触发执行
3. 执行器读取 `.omo/plans/{subgoalId}.md` 并执行每个任务
4. 每个任务生成 QA 证据到 `.omo/evidence/task-{N}-{scenario}.txt`
5. 所有任务完成后，捕获执行摘要

**延续 Hook（关键）**：
Plan 执行完成后：
```
1. 更新 subgoal 状态为 "completed"（如果成功）
2. 更新 subgoal 的 lastResult 为执行摘要
3. 读取 Goal Registry → 检查下一个待处理的 subgoal
4. 如果存在下一个 subgoal → 循环回到阶段 3
5. 如果没有更多 subgoal → 进入阶段 7
```

关键要点：系统不会等待用户。它自动检查 Goal Registry 并继续到下一个 subgoal。

---

### 阶段 6：验证结果（Verify Result）

**作用**：Momus 验证执行输出。

**步骤**：
1. 收集执行证据（`.omo/evidence/` 文件）
2. 将结果呈现给 Momus 进行验证
3. Momus 检查：
   - 是否所有任务都已完成？
   - 验收标准是否通过？
   - 输出是否正确且健壮？
4. Momus 输出 **Verdict**：PASS 或 REJECT（含失败类型）

**Verdict 输出格式**（可通过 VerdictParser 解析）：
```
Verdict: PASS/REJECT
Type: EXECUTION_ERROR | PLAN_ISSUE | QUALITY_FAIL | REQUIREMENT_CHANGE | ADVERSE | FIDELITY_FAIL
Details: <description of what failed and why>
File: <specific file references if applicable>
```

> **新增类型**：`FIDELITY_FAIL` — 实现与 Spec 定义不符，将在阶段 7 中进一步处理。

---

### 阶段 7：保真度验证（Fidelity Verification）← 新增

**作用**：验证实现结果与原始 Spec 的保真度——确保"做出来的"就是"Spec 规定的"。

**触发条件**：阶段 6（Verify Result）的 Verdict 为 PASS 或含有 FIDELITY_FAIL 类型。

**与阶段 6 的区别**：

| 维度 | 阶段 6：验证结果 | 阶段 7：保真度验证 |
|------|----------------|-------------------|
| 关注点 | Plan 是否正确执行 | Spec 的需求是否被正确实现 |
| 检查对象 | 执行产出 vs Plan | 实现结果 vs Spec |
| 检查内容 | 代码质量、测试覆盖、功能正确 | 需求保真度、用户故事完成度 |

**验证流程**：
```
1. 加载 Spec 文档（通过 subgoal 的 specRef 定位）
2. 逐条检查 Spec 中的：
   - 功能需求（FR-{NNN}）：每个需求是否在实现中满足
   - 验收标准：每个验收标准是否可通过证据验证
   - 用户故事：P1/P2/P3 各自完成度
3. 评估每个需求的状态：
   - ✅ 完全满足   — 实现与 Spec 一致
   - ⚠️ 部分满足   — 实现了核心逻辑但有偏差
   - ❌ 未满足     — 需求未被实现或实现错误
4. 生成保真度报告（Fidelity Report）
5. 如果所有需求满足 → 进入阶段 9（Complete）
6. 如果有需求未满足 → 进入阶段 8（Router），类型为 FIDELITY_FAIL
```

**保真度报告格式**：
```json
{
  "specRef": "spec-001",
  "specPath": ".omo/specs/feature-x/spec.md",
  "verifiedAt": "ISO 8601 timestamp",
  "overallStatus": "PASS | PARTIAL | FAIL",
  "requirementResults": [
    {
      "frId": "FR-001",
      "title": "需求标题",
      "status": "MET | PARTIAL | UNMET",
      "evidence": ["证据文件路径或描述"],
      "gapDescription": "如果 PARTIAL 或 UNMET，描述差距"
    }
  ],
  "unmetCount": 0,
  "partialCount": 0,
  "summary": "保真度验证摘要"
}
```

---

### 阶段 8：路由决策（Route）

**作用**：Router 分析 Verdict（来自阶段 6 和/或阶段 7），决定下一步操作。

**输入**：Momus Verdict + 保真度报告（可选）+ 当前 subgoal 状态
**输出**：决策（继续、重试、重新规划、升级）

**VerdictParser** — 通过结构化适配器解析 Momus 输出（非硬编码字符串匹配）：
```
VerdictParser 接口：
  input: 原始字符串（Momus 输出）
  output: { verdict: PASS|REJECT, type: failure_type, details: string }

实现：读取 Momus 输出，提取结构化字段。
如果将来格式发生变化，只需修改解析器——Router 逻辑保持不变。
```

**六种失败类型及其处理**：

| 类型 | 含义 | 处理方式 |
|------|------|---------|
| `EXECUTION_ERROR` | 工具调用失败、超时、网络错误 | **重试** — 重新执行 |
| `PLAN_ISSUE` | Plan 设计错误、遗漏需求 | **重新规划** — 回到阶段 3，附带反馈 |
| `QUALITY_FAIL` | 代码质量问题、缺少测试 | **重试 2 次** 然后 **重新规划** |
| `REQUIREMENT_CHANGE` | 需求不清晰、矛盾 | **升级** — 通知用户 |
| `ADVERSE` | 对抗性验证推翻核心结论 | **重新规划** — 必须重新设计 |
| `FIDELITY_FAIL` | 实现与 Spec 不符 | **根据失败类型分流**（见下方） |

**保真度失败分流逻辑**（新增）：

保真度失败需要判断根源——是 Spec 定义错误，还是实现偏离：

```
FIDELITY_FAIL 处理:

1. 分析保真度报告中 UNMET/PARTIAL 的需求
2. 判断失败来源：
   a) Spec 错误：Spec 中的需求定义不合理、矛盾或无法实现
      → 路由到阶段 2（Specify），附带保真度报告
      → 用户需要重新审视并修正 Spec
      
   b) 实现偏离：Spec 正确定义了需求，但实现偏离了 Spec
      → 路由到阶段 3（Planning Phase），附带保真度报告
      → Agent 需要重新规划实现方案
      
   c) 混合情况：部分 Spec 错误 + 部分实现偏离
      → 先路由到阶段 2 修正 Spec
      → Spec 修正后，重新到阶段 3 重新规划
```

**决策算法**：
```
function route(parsedVerdict, subgoal, fidelityReport):
  if parsedVerdict.verdict == PASS && (!fidelityReport || fidelityReport.overallStatus == "PASS"):
    mark subgoal as completed
    return CONTINUE_TO_NEXT_SUBGOAL

  // 检查尝试限制
  if subgoal.attempts >= subgoal.maxAttempts:
    mark subgoal as escalated
    return ESCALATE_TO_HUMAN("超过最大重试次数")

  // 分类处理
  switch parsedVerdict.type:
    case EXECUTION_ERROR:
      increment attempts
      return RETRY_EXECUTION

    case PLAN_ISSUE:
      increment attempts
      return REPLAN(parsedVerdict.details)

    case QUALITY_FAIL:
      increment attempts
      if attempts < 2:
        return RETRY_EXECUTION(parsedVerdict.details)
      else:
        return REPLAN(parsedVerdict.details)

    case REQUIREMENT_CHANGE:
      increment attempts
      return ESCALATE_TO_HUMAN(parsedVerdict.details)

    case ADVERSE:
      increment attempts
      return REPLAN(parsedVerdict.details)

    case FIDELITY_FAIL:
      increment attempts
      // 保真度失败 - 分析根因
      if fidelityReport.hasSpecError():
        return RESPECIFY(fidelityReport.details)  // 回到阶段 2
      else:
        return REPLAN(fidelityReport.details)      // 回到阶段 3

    default:
      return ESCALATE_TO_HUMAN("未知失败类型: " + parsedVerdict.type)
```

**升级流程**：
当需要升级时：
1. 设置 subgoal 状态为 `escalated`
2. 设置 subgoal 的 `lastResult` 和 `lastError` 为详细信息
3. 通知用户：
   - 什么升级了（目标 + subgoal）
   - 为什么（失败类型 + 详情）
   - 建议操作（澄清需求、批准绕过等）
4. 等待用户输入后再继续
5. 用户决策后 → 更新 subgoal，从阶段 2 或阶段 3 恢复

**尝试追踪**：每次执行/重试递增 `subgoal.attempts`。Goal Registry 配置中的 `maxAttemptsPerSubgoal` 限制了强制升级前的总尝试次数。

---

### 阶段 9：完成（Complete）

**作用**：所有 subgoal 完成——输出完成声明。

**步骤**：
1. 如果关联了 Spec，将 Spec 归档（移动到 `.omo/specs/{specName}/` 的归档目录）
2. 调用 `goals:archive {goalId}` 将目标移至已完成
3. 生成 **完成报告**，包括：
   - 目标标题和描述
   - 总 subgoal 数及每个的尝试次数
   - 发生的任何升级事件
   - 保真度验证摘要（如果使用了 Spec）
   - 执行时间线
4. 输出：`<promise>Goal "{title}" completed: {completed}/{total} subgoals done</promise>`
5. 向用户呈现报告

---

## 循环状态机（Loop State Machine）

Prometheus Spec-Driven Loop 的状态转换：

```
IDLE
  │  用户设定目标
  ▼
SPECIFYING ←──────────────┐
  │  Spec 完成             │ (保真度失败 — Spec 错误)
  ▼                        │
PLANNING ──────────────────┤
  │  Plan 就绪             │ (Replan 路由)
  ▼                        │
EXECUTING ─────────────────┘
  │  执行完成
  ▼
VERIFYING
  │  Momus Verdict 产生
  ▼
FIDELITY_CHECK
  │  保真度报告完成
  ▼
ROUTING ──────────────────────────────────────────────────┐
  │  │     │       │         │            │              │
  │  ✅    🔄    🧠      ⚠️         🔙              │
  │  Pass  Retry  Replan  Escalate  FidelityFail        │
  │         │      │        │            │              │
  │         ▼      └──►PLANNING         │              │
  │      EXECUTING          │           ▼              │
  │                         ▼      ┌──────────┐       │
  │  Next subgoal → PLANNING       │Spec错误 →│       │
  │  All done → COMPLETED          │ SPECIFYING       │
  │  Safety triggered → TERMINATED │实现偏离 →│       │
  │                                │ PLANNING  │       │
  │                                └──────────┘       │
  └───────────────────────────────────────────────────┘
```

### 状态定义

| 状态 | 含义 | 进入条件 | 退出条件 |
|------|------|---------|---------|
| **IDLE** | 等待目标 | 启动/重置 | 用户设定目标 |
| **SPECIFYING** | 正在定义 Spec（含 Clarify 子阶段） | 新目标或保真度失败（Spec 错误） | Spec 完成 |
| **PLANNING** | Prometheus 正在创建 Plan | 新目标、Spec 完成或 replan | Plan 保存 |
| **EXECUTING** | Sisyphus 执行 Plan | Plan 就绪或 retry | 执行完成 |
| **VERIFYING** | Momus 验证执行结果 | 执行完成 | Verdict 产生 |
| **FIDELITY_CHECK** | 验证实现与 Spec 的保真度 | Verdict 通过或含 FIDELITY_FAIL | 保真度报告完成 |
| **ROUTING** | Router 决定下一步操作 | Verdict 和/或保真度报告就绪 | 决策做出 |
| **ESCALATED** | 等待用户输入 | 升级路由 | 用户响应 |
| **COMPLETED** | 所有 subgoal 完成 | 最终路由决策 | —（终止） |
| **TERMINATED** | 安全边界触发 | 安全断路器 | —（终止） |

---

## 安全边界（Safety Boundaries）

Loop 包含多种安全机制，防止无限或失控执行。

### 1. 全局断路器（Global Circuit Breaker）

**阈值**：所有 subgoal 累计 20 次失败
**行为**：自动暂停整个 Loop
**操作**：向用户升级，附带失败摘要

```
if totalFailures >= globalCircuitBreakerThreshold:
  pauseLoop()
  notifyUser("断路器触发: {totalFailures} 次失败")
```

### 2. Subgoal 重试限制（Subgoal Retry Limit）

**阈值**：每个 subgoal 的 `maxAttemptsPerSubgoal`（来自 Goal Registry 配置，默认：5）
**行为**：耗尽重试次数后，subgoal 状态 → `escalated`
**操作**：向用户升级

### 3. 超时保护（Timeout Protection）

**单次执行超时**：30 分钟
**行为**：如果单个 Plan 执行超过 30 分钟，强制中断
**操作**：标记为 EXECUTION_ERROR，路由到重试或重新规划

**总 Loop 超时**：2 小时（可在目标的 `config.maxExecutionTimeMin` 中配置）
**行为**：如果整个 Loop 超过时间预算，强制终止
**操作**：终止 Loop，输出部分完成报告

### 4. Clarify 超时保护 ← 新增

**阈值**：`config.clarifyTimeoutMin`（默认：30 分钟）
**行为**：如果用户在 Clarify 子阶段的规定时间内未响应：
1. 使用各问题的默认值选项
2. 将 Spec 标记为 `isAssumed: true`
3. 在 Clarification History 中记录超时事件
4. 继续后续流程（不阻塞整体进度）
5. 完成后通知用户哪些决策使用了默认值

**操作**：使用默认值继续，记录超时事件

### 5. 用户停止信号（User STOP Signal）

**停止方式**：用户说 "stop"、"STOP"、"停"、"/stop-prometheus-loop"
**行为**：优雅终止——完成当前任务后退出
**操作**：输出包含当前状态的部分完成报告

### 6. 迭代上限（Iteration Cap）

**最大 subgoal 迭代次数**：100（跨所有 subgoal 的重试 + 重新规划总和）
**行为**：100 次迭代后，强制终止
**操作**：终止 Loop，输出终止报告

---

## 监视与恢复（Monitoring and Resumption）

### 检查循环状态

在 Loop 运行时（或会话结束后）检查进度：

```
1. goals:list
   → 查看所有目标、状态和进度

2. goals:get {goalId}
   → 查看目标详情、当前 subgoal、尝试次数

3. 查看 .omo/goals/index.json
   → 活跃 vs 已完成目标

4. 查看 .omo/specs/ 目录
   → 查看已创建的 Spec 文档

5. 查看 .omo/plans/ 目录
   → 查看已生成的 Plan
```

### 会话恢复

会话结束后恢复工作时：

1. 运行 `goals:list` 查看所有目标
2. 对于活跃目标，运行 `goals:get {goalId}` 查看当前状态
3. 查看是否有关联的 Spec（根据 subgoal 的 `specRef` 字段）
4. 检查 `loopContext.sessionCount` 和 `loopContext.continuationToken`
5. 运行 `goals:next {goalId}` 查找下一个 subgoal
6. 根据 subgoal 状态确定恢复阶段：
   - 需要重新规划 → 阶段 3（Planning Phase）
   - 需要重新定义 Spec → 阶段 2（Specify）
   - 继续执行 → 阶段 5（Auto-Execute）
7. 更新 `loopContext.sessionCount += 1`

### 恢复示例

```
用户: "继续之前的任务"
→ goals:list
→ Active Goals: blog-system (in_progress — 1/3 subgoals)
→ goals:get blog-system
  → currentSubgoalIndex: 1
  → sg-002: in_progress, attempts: 2, lastError: "缺少鉴权"
  → sg-002.specRef: "spec-001"
→ 查看 .omo/specs/001-prometheus-spec-loop/spec.md
→ goals:next blog-system
  → sg-002 ready (sg-001 completed, dependency unblocked)
→ 从阶段 3（Planning Phase）恢复：使用 Spec + 上次失败的反馈重新规划 sg-002
```

---

## 错误处理参考（Error Handling Reference）

| 场景 | 检测方式 | 处理方式 |
|------|---------|---------|
| Goal 文件丢失 | 文件读取失败 | 通过 goals:init 初始化新目标 |
| Index.json 损坏 | JSON 解析错误 | 从现有 goal 文件重建索引 |
| Plan 文件未找到 | 文件检查失败 | 重新规划：回到阶段 3（Planning Phase） |
| Spec 文件未找到 | 文件检查失败 | 回到阶段 2（Specify）重新创建 Spec |
| Momus 不可用 | Agent 调用失败 | 跳过验证，谨慎继续 |
| 执行工具失败 | 退出码非零 | 阶段 6（Verify Result）会捕获 |
| Clarify 超时 | 用户未在 `clarifyTimeoutMin` 内响应 | 使用默认值，将 Spec 标记为 `isAssumed: true`，记录超时事件，继续流程 |
| 保真度验证失败 | 保真度报告中存在 UNMET/PARTIAL | 分析失败类型：Spec 错误回阶段 2，实现偏离回阶段 3 |
| 循环执行中断 | 会话结束 | 会话恢复（见监视与恢复章节） |
| Goal 无 subgoal | goals:next 返回 null | 设置 successCriteria，作为单个任务执行 |

---

## 常见错误（Common Mistakes）

- **Subgoal 过大**：每个 subgoal 应对应 1-3 个文件 / 一个 Plan。如果一个 subgoal 需要多个 Plan，拆分为更细的 subgoal。
- **缺少依赖链**：没有 `blockedBy` 的 subgoal 可能并行执行，因缺少前置条件而失败。始终在阶段 1（Parse Goal）中建模依赖关系。
- **模糊的目标描述**：初始描述驱动 subgoal 分解。模糊输入 → 模糊 subgoal → PLAN_ISSUE 失败。要具体：`"博客系统含文章 CRUD + 评论区 + 标签管理"` 而非 `"做个博客"`。
- **期望手动干预**：Loop 是自主的。如果你需要批准每个阶段，说明在用错工具。Loop 自动处理重试、重新规划和升级。
- **忽略 Momus 拒绝详情**：当 Momus 拒绝 Plan（阶段 4）或 Result（阶段 6）时，Verdict 详情准确告诉你需要修复什么。仔细阅读可以节省重试周期。
- **跳过 Specify 阶段直接进入 Plan**：这是 9 阶段流程中最常见的错误。先定义"做什么"（Spec），再定义"怎么做"（Plan）。跳过 Specify 会导致需求模糊→Plan 返工→保真度失败。
- **Spec 中包含实现细节**：Spec 只应描述"要解决什么问题"和"验收标准"，不应包含技术选型或实现方案。实现细节属于 Plan。
- **Clarify 阶段一次只问一个问题**：Clarify 是批量机制——收集所有歧义后一次性提交。逐条提问会打断用户，降低效率。

---

## 内部命令参考（Internal Commands Reference）

8 个 Goal CRUD 命令（`goals:init`、`goals:list`、`goals:get`、`goals:update`、`goals:add-subgoal`、`goals:update-subgoal`、`goals:archive`、`goals:next`）在 [`commands.md`](./commands.md) 中有详细文档，包括 Goal JSON Schema、Spec 文档模板和存储布局。

> 新增的 `specRef` 和 `specPath` 字段使 subgoal 可以与 Spec 文档关联，实现全链路可追溯性。
