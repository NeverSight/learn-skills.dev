---
name: requirement-analysis
slug: requirement-analysis
displayName: 需求分析
version: 0.8.1
description: "Model a requirement/system: extract goals, scope, roles, rules, exceptions, dependencies from PRD, docs, bugs, code; outputs a structured model with clarifications. Not for: writing cases, strategy decisions, the pipeline. 建模需求/系统：从 PRD、文档、Bug、代码提炼目标/范围/角色/规则/异常/依赖。不用于：直接写用例、策略、流水线。"
---

# 需求分析（requirement-analysis）

回答"**这个需求到底要做什么**"——建立对系统的正确理解，而不是写测试。

- **输入**：PRD、设计文档、API 文档、Bug、Issue、代码仓库；旁路场景下消费 `exploratory-testing` 的探索笔记（系统理解 + 风险清单）
- **输出（落盘）**：`{项目}/需求模型.md`——按下方 Schema 组织，含澄清记录与用户裁决
- **边界**：不产出用例（→ `test-case-writing`）；澄清后仍模糊的项如实标注 `open_questions`，**不硬猜**

## When to Use

- 拿到 PRD/设计文档，需要系统性理解"这个需求到底要做什么"再进入测试
- 多输入源（文档 + 代码 + Bug 单）需要交叉核对、暴露矛盾与缺口
- 为 `test-strategy` / `test-case-writing` 准备结构化的需求模型输入

## When NOT to Use

- 端到端测试整个需求 → `qa` 编排
- 已有需求模型、直接写用例 → `test-case-writing`（其阶段一内联轻量研读，够用即不必先建模）
- "这个功能应该怎么测" → `test-strategy`
- 完全无文档且系统陌生 → 先走 `exploratory-testing` 探索，再回来建模

## 需求模型 Schema（产出结构）

```yaml
requirement_model:
  goal:                     # 需求目标（一句话 + 成功标准）
  scope:                    # 功能范围（含明确的非目标）
  roles: []                 # 角色 → 能做什么 / 不能做什么
  inputs: []                # 输入（来源、格式、约束）
  outputs: []               # 输出（去向、格式、消费方）
  states: []                # 状态与流转（状态A --事件--> 状态B，逐条）
  rules: []                 # 业务规则，每条带 evidence（文档章节或 文件:行）
  exceptions: []            # 异常情况（错误场景的预期行为）
  dependencies: []          # 依赖关系（上下游系统、共享数据、时序依赖）
  open_questions: []        # 不明确事项 → 澄清记录（含用户裁决）
```

> 证据标注（此时加载 `../core/evidence.md`）：rules / states / exceptions 每条标注 evidence（level E0–E4 + source）；用户在澄清环节的裁决记入 open_questions 的裁决字段，后续 skill 不得用代码推翻。

## 工作流

### 1. 输入收集与盘点

- 清点可用输入源：PRD / 设计文档 / API 文档 / Bug 单 / FAQ / 会议纪要 / 代码仓库
- 有代码仓库 → 主动索取（路径 + 分支 + 改动范围 + **对比基线 base**——阶段 7 回归范围凭它划界），代码是静态事实的最高来源；分支名 + commit（或拉取时间）+ 对比基线记入需求模型文件头部，流水线续跑或进入执行阶段前先核对分支未变——对旧分支建模的结论不可复用，变了则标注受影响字段并复核
- 有探索笔记（`探索笔记_{主题}.md`）→ 消费其"系统理解"与"风险清单"作为建模输入
- 输入缺失项列入 `open_questions`（如"无性能指标文档"）

### 2. 初读与要素提取

逐文档通读，按 Schema 的十个字段收集要素：

- **goal / scope**：目标与成功标准；显式的"非目标"声明单独收录（后续要转化为验证边界）
- **roles**：角色 × 能做 / 不能做（权限矩阵的雏形）
- **inputs / outputs**：数据从哪来、到哪去、谁消费（无下游消费的输出是证伪线索）
- **states**：状态与流转边；有代码时从代码状态字段提取**实际**状态机，与文档对照，差异记入澄清
- **rules**：业务规则逐条编号，标注 evidence
- **exceptions / dependencies**：错误场景行为、上下游依赖

### 3. 一致性检查（冲突发现）

- **文档内部矛盾**：同一文档不同位置对同一功能的描述不一致
- **跨文档矛盾**：PRD 与技术设计的规则 / 流程 / 字段不一致
- **文档 vs 代码**（有代码时）：按 `../core/evidence.md` 静态裁决规则——默认以代码为准，偏离记录并提交澄清

### 4. 澄清（⏸ 检查点，不硬猜）

**触发与扫描的单一权威源在 `../core/clarify-pattern.md`（此时加载）**：基础触发按其「何时必须问」6 条，深度扫描按其「需求歧义九类漏网模式」A–I **逐类过筛材料**（本节不再维护独立清单，防止跨 skill 口径分裂），命中的必须进澄清清单——其中 I 类（NFR 指标空缺）单独提醒：性能/兼容性描述常见"快、稳定、支持多端"而无数值，问到指标或显式排除二选一，不允许跳过。

提问格式与裁决落盘同样统一按 `../core/clarify-pattern.md`（逐条独立成卡，单条简单问题用其紧凑单行模板），等待用户答复，不自行假设。

用户裁决记入 `open_questions`（问题 / 裁决 / 依据），具有最终裁决力。

### 5. 落盘与交付

- 按 Schema 写 `{项目}/需求模型.md`；澄清后仍模糊的项**保留在 open_questions 并标注"未裁决"**，不硬猜填入规则
- 交付时给下游（`test-strategy` / `test-case-writing`）一句话索引：模型路径 + 未裁决项数量

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 硬猜模糊项填入 rules | 模型基于错误假设，下游全部污染 | 模糊项进 open_questions，等用户裁决 |
| 只读 PRD 不读代码（有代码时） | 规则与实现脱节 | 代码优先，文档降为对照（`../core/evidence.md`） |
| 把测试想法混进需求模型 | 职责越界（那是策略/用例的事） | 模型只描述"系统是什么/要什么"，不描述"怎么测" |
| 用户裁决不落盘 | 后续 skill 重新发起同样的问题或推翻裁决 | 裁决记入 open_questions，文件即流水线状态 |
| 非目标声明被忽略 | 测试范围误扩、漏掉"限制的验证" | 非目标单独收录进 scope |
| 性能/兼容性只有定性描述就放行 | 无指标的 NFR 不可测，执行阶段临时编阈值 | 按九类模式 I 类过筛：问到数值或显式裁定"本版不验证" |
| 出现新事实仍抱着旧裁决走 | 模型基于已失效的假设继续下游 | 触发裁决重开：呈现新旧证据重新澄清，重开新起一条不覆写 |
| 空字段和漏提取分不清 | 下游无法判断"没有"还是"没查" | 落盘前自检：空字段标注"已核对，无此类要素" |
