---
name: academic-paper-cn
description: "12代理学术论文写作流程。10种模式（full/plan/outline/revision/revision-coach/abstract/lit-review/format-convert/citation-check/disclosure）。6种论文类型，5种引用格式，双语摘要，LaTeX/DOCX-via-Pandoc/PDF 输出。风格校准 写作质量检查 IRON RULE 异常模式标记。触发器：写论文、学术论文、引导我的论文、解析评审意见、AI披露、写论文、学术论文、引导我写论文、审查意见。"
metadata:
  version: "3.1.2"
  last_updated: "2026-05-18"
  status: active
  data_access_level: redacted
  task_type: open-ended
  related_skills:
    - deep-research
    - academic-paper-reviewer
    - academic-pipeline
---

# 学术论文 — 学术论文写作代理 Team

 一种通用学术论文写作工具 — 涵盖所有学科的12代理流水线，以高等教育领域作为默认参考。

**v2.5** 增加了两个写作质量功能：
- **风格校准**（输入步骤10，可选）—— 提供3份往年试卷，系统学习你的写作风格（句子节奏、词汇偏好、引用整合方式）。在起草过程中作为软性指导；学科规范始终优先。参见 `shared/style_calibration_protocol.md`。
- **写作质量检查** (`references/writing_quality_check.md`) — 在草稿自我审查步骤中使用的写作质量清单。能发现过度使用的 AI- 典型词汇、过多使用破折号、清嗓开头句、段落长度一致以及句子节奏单调的情况。这些都是好的写作规则，而非规避检测的方法。

> **路由策略 (v3.9.2):** 请参阅 `.claude/CLAUDE.md` “路由策略 (v3.9.2)” 以及 `shared/references/intent_clarification_protocol.md` 获取跨技能路由规则。本技能假设路由已确定——模糊的跨阶段材料应在上游澄清。

## 快速开始

**最小命令:**
```
Write a paper on the impact of AI on higher education quality assurance
```

```
Write a paper on the impact of declining birth rates on private university management strategies
```

**执行流程：**

1. 配置访谈 — 论文类型、学科、引用格式、输出格式

2. 文献检索 — 系统检索策略、文献筛选

3. 架构设计 — 论文结构、提纲、字数分配

4. 论证构建 — 论点-证据链、逻辑流程

5. 全文起草 — 分章节草稿、文体调整

6. 引用合规 — 双语摘要（平行）

7. 同行评审 — 五维度评分、修改建议

8. 输出格式化 — LaTeX/DOCX（通过 Pandoc）
/PDF/Markdown

---

## 触发条件

### 触发关键词

**英文**: 写论文, 学术论文, 论文大纲, 写摘要, 修改论文, 文献综述论文, 检查引用, 转 LaTeX, 转换格式, 排版论文, 会议论文, 期刊文章, 论文章节, 研究论文, 指导我的论文, 帮我规划论文, 逐步写论文, 起草手稿, 写方法论, 写讨论, 解析审稿意见, 修订路线图, 帮我修改, 我收到审稿意见, 转换引用格式

当用户需要指导、逐步规划或对论文结构表示不确定时，激活 `plan` 模式。**默认规则**：当在 `plan` 和 `full` 之间不明确时，优先选择 `plan`。

> 有关完整意图信号和激活规则，请参见 `references/plan_mode_protocol.md`。

### NOT 是否触发

| 场景 | 改用 |
|----------|-------------|
| 深度研究/事实核查（非写论文） | `deep-research` |
| 审阅论文（结构化审阅） | `academic-paper-reviewer` |
| 从研究到论文的完整流程 | `academic-pipeline` |

### 与 `deep-research` 的区别

| 特性 | `academic-paper` | `deep-research` |
|---------|-------------------|-----------------|
| 主要输出 | 可发表的论文草稿 | 研究报告 |
| 结构 | 期刊就绪（IMRaD 等） | APA 7.0 报告 |
| 引用 | 多格式（APA/Chicago/MLA/IEEE/Vancouver） | 仅 APA 7.0 |
| 摘要 | 双语（繁体中文 - 英文） | 单语言 |
| 同行评审 | 模拟五维度评审 | 编辑评审 |
| 输出格式 | LaTeX/DOCX（通过 Pandoc）/PDF/Markdown | 仅 Markdown |
| 修订循环 | 最多 2 轮，提供针对性反馈 | 最多 2 轮 |

---

## 代理团队（12 位代理）

| # | 代理 | 角色 | 阶段 |
|---|-------|------|-------|
| 1 | `intake_agent` | 配置面谈：论文类型、学科、期刊、引用格式、输出格式、语言、字数；交接检测；计划模式简化面谈 | 阶段 0 |
| 2 | `literature_strategist_agent` | 搜索策略设计、来源筛选、带注释的参考书目、文献矩阵 | 阶段 1 |
| 3 | `structure_architect_agent` | 论文结构选择、详细大纲、字数分配、证据映射 | 阶段 2 |
| 4 | `argument_builder_agent` | 论证构建、论点-证据链、逻辑流程、反论点处理；计划模式下的论证压力测试 | 第3阶段 / 计划第3步 |
| 5 | `draft_writer_agent` | 分章节完整草稿写作、学科用语调整、字数跟踪 | 第4阶段 |
| 6 | `citation_compliance_agent` | 引文格式验证、参考资料 list 完整性、DOI 检查 | 第5a阶段 |
| 7 | `abstract_bilingual_agent` | 双语摘要（繁体中文-英文），每种语言5-7个关键词 | 第5b阶段 |
| 8 | `peer_reviewer_agent` | 模拟双盲审稿，五维度评分，修改建议（最多2轮） | 阶段6 |
 | 9 | `formatter_agent` | 转换为 LaTeX/DOCX（通过 Pandoc）/PDF/Markdown，期刊格式，封面信，引用格式转换（APA 7 / Chicago / MLA / IEEE / Vancouver） | 阶段7 |
 | 10 | `socratic_mentor_agent` | 计划模式苏格拉底导师：逐章指导，收敛标准（4个信号），问题分类（4类型），提取INSIGHT | 计划步骤0-3 |
| 11 | `visualization_agent` | 解析论文数据并生成符合出版质量的图表代码（Python matplotlib / R ggplot2），使用 APA 7.0 格式、色盲安全调色板，并支持 LaTeX 集成 | 第4阶段 / 第7阶段 |
| 12 | `revision_coach_agent` | 将非结构化审稿人评论解析为结构化修订路线图；分类、映射并优先处理评论；可独立工作，无需先前的流程执行 | 修订专家模式 |

---

## 输出格式

### 文本格式
LaTeX (.tex .bib), DOCX（通过 Pandoc）, PDF（通过 LaTeX 或 Pandoc）, Markdown.

### 图表
当论文包含定量结果时，`visualization_agent` 可以使用 Python (matplotlib/seaborn) 或 R (ggplot2) 生成可用于发表的图表，并提供 APA 7.0 格式和色盲友好调色板。图表以可运行代码和 LaTeX `\includegraphics` 集成代码的形式提供。有关图表类型决策树和代码模板，请参见 `references/statistical_visualization_standards.md`。

### 引用格式
APA 7.0（默认），芝加哥（作者-日期或注释-参考书目），MLA 9，IEEE，温哥华。该`formatter_agent`支持通过“将引用转换为[格式]”在任意两个支持格式之间进行后期引用格式转换。

---

## 编排工作流程（8个阶段）

```
Phase 0: CONFIG        -> [intake_agent]              -> Paper Configuration Record
Phase 1: RESEARCH      -> [literature_strategist]      -> Search Strategy + Source Corpus
Phase 2: ARCHITECTURE  -> [structure_architect]        -> Paper Outline + Evidence Map
Phase 3: ARGUMENTATION -> [argument_builder]           -> Argument Blueprint
Phase 4: DRAFTING      -> [draft_writer]               -> Complete Draft
Phase 5a: CITATIONS    -> [citation_compliance] ──┐    -> Citation Audit Report
Phase 5b: ABSTRACT     -> [abstract_bilingual]   ─┘    -> Bilingual Abstract + Keywords  (parallel)
Phase 6: PEER REVIEW   -> [peer_reviewer]              -> Review Report (max 2 revision loops)
Phase 7: FORMAT        -> [formatter]                  -> Final Output Package
```

> 详见 `references/workflow_phase_details.md` 以获取每个阶段代理行为和输出的详细描述。

### 检查点规则

1. ⚠️ **IRON RULE**：用户必须在进入第1阶段前确认论文配置记录
2. **阶段 2 -> 3**：用户必须批准提纲（可请求重组）
3. ⚠️ **IRON RULE**：最多允许 2 次修订循环；未解决的事项 -> “已知限制”
4. **同行评审** 严重问题将阻止进入第7阶段
5. 如果提供自己的资料来源，用户可以跳过第1阶段（文献）

---

> **v3.4.0 合规性（适用于 `full` 模式）：** 在最终确定之前，`compliance_agent` 会运行 RAISE 仅原则检查（仅警告；主要研究不在 PRISMA-trAIce 范围内）。警告列在披露声明中，但从不阻塞流程。请参见 `shared/raise_framework.md §Scope disclaimer`.

## 分阶段调用协议（v3.9.2）

 学术论文流程分 8 个阶段运行（阶段 0 输入 → 阶段 7 格式化）。两种调用模式：

**模式 A — 编排器驱动（默认）：** `pipeline_orchestrator_agent`（在 `academic-pipeline` 技能中）运行所有阶段的端到端流程，并通过材料护照进行状态跟踪。

**模式B——逐阶段（跨会话续接）：** 用户在长周期项目中每个阶段跨会话调用一个代理。常见模式：在一次会话中撰写草稿，下周再独立进行引用检查/摘要/同行评审。

在模式B中，**单相代理（根据 `docs/design/2026-05-18-ars-v3.9.2-agent-phase-classification.md` 的 A 桶）在写入时严格保持在其分配的阶段内**。在 academic-paper 中的 7 个 A 桶代理是：`literature_strategist`（P1）、`structure_architect`（P2）、`draft_writer`（调用时 P4/P6）、`citation_compliance`（P5a）、`abstract_bilingual`（P5b）、`peer_reviewer`（P6）、`formatter`（P7）。允许从上游阶段读取。

多阶段代理（B类：`argument_builder` P3计划，`visualization` P4 P7）严格执行调用者针对该阶段的调用所指定的工作——不会扩展到同一调用的其他阶段。下面的v3.6.6生成器-评估器合同还对`draft_writer`和`peer_reviewer`子阶段行为（阶段4a/4b，阶段6a/6b）进行了约束。

进入B模式需要用户明确信号——`/ars-<mode>`斜杠命令或`[direct-mode]`前缀。跨阶段输入模糊时，默认根据`.claude/CLAUDE.md`路由规范`shared/references/intent_clarification_protocol.md`进行澄清。

**执行 (v3.9.2)：** 通过 Bucket A 代理上的相位边界块进行提示级别的执行，咨询验证器 (`scripts/check_pipeline_integrity.py`)。确定性 PreToolUse 钩子，多相包延迟至 v3.10 活动导体 (#134)。

## v3.6.6 生成器-评估器合同协议

> v3.6.6 合同门控阶段分割内 `academic-paper full` 模式的权威编排块。自 v3.6.6（`shared/sprint_contract.schema.json`）起的架构 13.1。模板：`shared/contracts/writer/full.json` `shared/contracts/evaluator/full.json`。设计规范：`docs/design/2026-04-27-ars-v3.6.6-generator-evaluator-contract-design.md` §5.
>
> **仅适用于 `academic-paper full` 模式。** 九种非全模式（`plan`、`outline-only`、`revision`、`revision-coach`、`abstract-only`、`lit-review`、`format-convert`、`citation-check`、`disclosure`）在 v3.6.5 → v3.6.6 之间是字节等效的，并且不会调用此协议。流水线边界保持不变：`academic-pipeline` 阶段 2 在计划或全模式下分派 `academic-paper`（仅全模式调用此协议）；阶段 3 分派单独的 `academic-paper-reviewer` 技能（5 面板外部编辑审查）。在该协议下的成对第 6 阶段评估者与第 3 阶段审核员属于不同的审核层级 — 见设计文档 §5.1审计结论 2。

### 概述

v3.6.6 将第4阶段（作者起草）和第6阶段（双人评估者审核）拆分为由 `writer_full` 和 `evaluator_full` 合同控制的纸面盲/纸面可见通话对。此拆分方式类似于 `academic-paper-reviewer/references/sprint_contract_protocol.md`（v3.6.2 评审者模式），但将其适配到没有小组且（对于作者）没有评分计划的单代理生成器模式。

承载机制是**调用的物理分离**：Phase 4a 的编写者从未看到运行时起草的人工制品；Phase 6a 的评估者从未看到 Phase 4b 编写者的草稿。这破坏了在双人自我质量关口上的“先读论文，然后再推理标准”的偏移路径。

### 四调用结构

对于每次 `academic-paper full` 调用，Phase 4 和 Phase 6 从两个单独调用扩展为四个独立的模型调用。每个调用都有其自己的系统提示和用户内容，遵循下文的系统对用户内容规范。

1. **阶段 4a — 作者在不查看论文的情况下进行预提交。**
   - 系统提示：`### Phase 4a — Writer paper-blind pre-commitment` 在 `academic-paper/agents/draft_writer_agent.md` § "v3.6.6 生成器-评估器合同协议" 子部分。
   - 用户内容：`writer_full` 合同 JSON   仅限论文元数据 (`title`, `field`, `word_count`)。
   - 输出：`## Acceptance Criteria Paraphrase` 部分   终端 `[PRE-COMMITMENT-ACKNOWLEDGED]` 标签。
   - 语法检查：3 个结构检查 (见下文 § "阶段 4a / 6a 输出语法检查").
2. **阶段 4b — 作者在可见论文情况下起草与自评分。**
- 系统提示：在相同代理文件中的 `### Phase 4b — Writer paper-visible drafting + self-scoring` 子部分。
   - 用户内容：`writer_full` 合同 JSON（重新注入）   第 4a 阶段输出封装在 `<phase4a_output>...</phase4a_output>` 数据分隔符中   上游起草产物（纸质配置记录、纸质大纲、论证蓝图、带注释的参考书目，可选样式配置文件，可选知识隔离指令）。
   - 输出：`## Draft Body` → `## Dimension Scores` → `## Failure Condition Checks` → `## Writer Decision`。
   - 代码检查：4 个结构检查（见下文 §“第 4b / 6b 阶段输出代码检查”）。
3. **第6a阶段 — 评估者纸质盲预承诺。**
 - 系统提示：`academic-paper/agents/peer_reviewer_agent.md`条“v3.6.6发电-评估员合同协议”中的`### Phase 6a — Evaluator paper-blind pre-commitment`小节。
 - 用户内容：`evaluator_full`合同JSON论文元数据，作者最近的`<phase4a_output>`（作者作品，评审员必须依`disagreement_handling.pre_commitment_check_protocol.check_writer_artifact`核实）。
- 输出：`## Contract Paraphrase`   `## Scoring Plan`（每维度 `dimension_id` / `what_to_look_for` / `what_triggers_block` / `what_triggers_warn`）   终端 `[PRE-COMMITMENT-ACKNOWLEDGED]` 标签.
   - Lint：5 个结构检查.
4. **阶段 6b — 评估者纸面可见评分决策。**
   - 系统提示：`### Phase 6b — Evaluator paper-visible scoring + decision` 在同一代理文件中的子部分。
- 用户内容：`evaluator_full` 合同 JSON（重新注入） 第6a阶段输出封装在 `<phase6a_output>...</phase6a_output>` 中 作者的 `<phase4a_output>`（根据 `pre_commitment_check_protocol.check_writer_artifact` 无条件） 作者第4b阶段草稿（正在审查的工件）。
 - 输出：`## Dimension Scores` → `## Failure Condition Checks` → `## Review Body` → `## Evaluator Decision`。
 - Lint：5 个结构检查。

### 系统提示与用户内容学科

镜像`sprint_contract_protocol.md` §2 审稿人模式逐字：

- **系统提示仅包含不变的政策文本**：代理文件`## v3.6.6 Generator-Evaluator Contract Protocol`块中的阶段子部分指令、lint 描述以及阶段边界标签约定。
- **用户内容携带合同 JSON（每次调用重新注入）以及该阶段允许的运行时输入**：论文元数据、`<phase4a_output>` / `<phase6a_output>` 分隔块、上游起草文档、论文草稿。

所有动态 LLM 输出（Phase Na 运行时排放，论文内容）通过数据分隔符存储在用户内容中，绝不存储在系统提示中。这可以防止动态的每篇论文内容意外提升为不变的策略表面。

### 架构字段名与运行时排放的区别

`pre_commitment_artifacts`（蛇形命名法，反引号）是 `shared/sprint_contract.schema.json` 中的模式字段名——这是冻结合同基线中的一个配置声明。“writer Phase 4a pre-commitment output” 是运行时输出——writer 代理在 Phase 4a 中生成的实际 Markdown 文本。运行时输出位于 `<phase4a_output>` 中，并被传递给 Phase 4b / Phase 6a / Phase 6b。`disagreement_handling`（模式字段）与“evaluator Phase 6a pre-commitment output”（运行时输出）的模式相同。混淆两者会导致合同基线配置与 LLM- 生成的内容之间的混乱。

### 阶段 4a / 6a 输出 lint

 按 `sprint_contract_protocol.md` §4 枚举约定的模式特定结构检查计数：

- **作家阶段 4a（3 次检查）**：按顺序所需部分 (`## Acceptance Criteria Paraphrase`，终端 `[PRE-COMMITMENT-ACKNOWLEDGED]`)；段落改写数量 ≥ `pre_commitment_artifacts.acceptance_criteria_paraphrase.minimum_dimensions`；阶段 4a 内容参考合同 JSON 仅限论文元数据。**无 `## Scoring Plan` 部分** — `writer_full` 不包含评分计划。
- **评估阶段 6a（5 次检查）**：按顺序要求的部分（`## Contract Paraphrase`、`## Scoring Plan`、终端 `[PRE-COMMITMENT-ACKNOWLEDGED]`）；改写段落数量 ≥ `disagreement_handling.paraphrase_minimum_dimensions`；每个验收维度对应一个 `### <Dn>: <name>` 子部分；每个 scoring_plan 子部分包含 `disagreement_handling.scoring_plan.per_dimension_criteria` 四字段形式（`dimension_id`、`what_to_look_for`、`what_triggers_block`、`what_triggers_warn`）；阶段 6a 内容引用合同 JSON 的论文元数据及作者 `<phase4a_output>`（仅限，不含完整草稿/论文内容）。

重试语义：第一次尝试时出现 lint 失败 → 根据系统提示中提示的特定 lint 缺口重试一次；第二次失败 → 根据下文 §“单代理生成器不可用处理” 将此角色标记为不可用。

### 第 4b / 6b 阶段输出 lint

- **写作者阶段 4b（4 次检查）**：按顺序要求的部分 — `## Draft Body`、`## Dimension Scores`、`## Failure Condition Checks`、`## Writer Decision`；七个写作者维度 D1–D7 的维度分数一一对应（根据 `shared/contracts/writer/full.json`）；失败条件检查一一对应 F1 / FF / F2 / F3 / F0；写作者决策可从 F 条件严重性优先级推导。**不允许多重异议重试**（写作者没有 scoring_plan 来提出异议）。**不进行一致性检查**（写作者阶段 4a 不发出任何 scoring_plan 触发令牌）。
- **评估阶段 6b（5 次检查）**：所需部分顺序为——`## Dimension Scores`、`## Failure Condition Checks`、`## Review Body`、`## Evaluator Decision`；维度评分在五个评估维度 D1–D5（根据 `shared/contracts/evaluator/full.json`）中一一对应；失败条件检查在 F1 / F2 / F3 / F6 / F4 / F5 / F0 中一一对应；一致性检查（阶段 6b 分数子字符串与阶段 6a `disagreement_handling.scoring_plan.per_dimension_criteria` 触发标记匹配）；评估决策可由 F 条件严重性优先级推导。**不允许多重异议重试**（评估者阶段内的意见分歧以编码形式表示为通过 `disagreement_handling.disagreement_resolution` 进行 F 条件操作，而不是作为重试触发器).

多异议重试仍仅限于审稿人（`academic-paper-reviewer` 技能）；生成器模式没有面板，也没有 scoring_plan 异议锚。

 三种模式的 lint 计数摘要：

| 阶段 | 审稿人（零接触） | 编写者 | 评估者 |
|---|---|---|---|
| 阶段 1 / 4a / 6a | 5 | 3 | 5 |
| 阶段 2 / 4b / 6b | 6 | 4 | 5 |

### 单代理生成器不可用处理

当编写者或评估者阶段变得不可用（阶段 Na lint 两次失败或阶段 Nb lint 失败）时，`academic-paper` 发出阶段级中止标签并引导到用户干预：

- **Writer 第4阶段不可用** → `[GENERATOR-PHASE-ABORTED: role=writer, contract=<id>, reason=<lint_failure_kind>]` → 中止 `academic-paper` 第4阶段 → 用户干预决定重试 / 回退 / 退回到第3阶段（论点蓝图）。

- **Evaluator 第6阶段不可用** → `[GENERATOR-PHASE-ABORTED: role=evaluator, contract=<id>, reason=<lint_failure_kind>]` → 中止 `academic-paper` 第6阶段 → 用户干预决定重试 / 回退 / 退回到第5阶段（草稿完成）。

`[GENERATOR-PHASE-ABORTED]` **不**构成有效的Phase 6b发射，因此不能进入Stage 3审核分配。根据设计文档§5.1，有两条有效的Stage 3进入路径：

- **标准路径**：评估者Phase 6b发射F0 `evaluator_decision=accept`或F4 `evaluator_decision=accept_with_dissent_note`。

- **特殊路径**：在成对修订循环在第2轮耗尽且强制维度块重复后，评估者Phase 6b发射F5 `evaluator_decision=flag_for_reviewer_stage`。

`academic-paper` 对作家/评估者没有面板基数不变量（没有 `panel_size` 字段 — 架构 13.1 §3.3.5 审阅者条件）。在生成器端没有 `[PANEL-SHRUNK]` 对应项；`[GENERATOR-PHASE-ABORTED]` 是阶段级中止。

**操作监控器**：跟踪 `[GENERATOR-PHASE-ABORTED]` 在 v3.6.6 部署的前三个月的速率。分母是 **每 `academic-paper full` 运行** — 一次用户感知的顶级调用。5% 的阈值是 `(runs_with_any_abort) / (total_runs)`。如果速率超过 5%，v3.6.7 会引入渐进降级回退（见下面“已知限制” §）。

### 跨会话恢复范围

v3.6.6 生成器-评估器轮次（第4a阶段 第4b阶段 第6a阶段 第6b阶段 配对修订循环）是一个**会话内原子单元**。手动在轮次中期拆分会话 → 撰写者第4a阶段输出会丢失；新会话必须从第0阶段重新启动`academic-paper full`模式。

v3.6.3 `ARS_PASSPORT_RESET=1` `reset_boundary[]` 机制（根据 `academic-pipeline/references/passport_as_reset_boundary.md`）在 `academic-pipeline` 阶段边界操作，而不是在 `academic-paper` 内部阶段边界操作。`academic-paper` 内部阶段（4a / 4b / 6a / 6b）**不是**边界点；它们之间不会生成 `kind: boundary` 账本条目。如果操作数据需要，v3.6.7 可能引入 `pre_commitment_history[]`，以在会话之间保留写入器 Phase 4a 工件——见下文 “已知限制” §。

## 已知限制

- **v3.6.6中没有优雅降级回退**：当writer或evaluator阶段通过`[GENERATOR-PHASE-ABORTED]`中止时，`academic-paper full`会中止并路由至用户干预。v3.6.7可能会引入一个回退，将受影响的阶段降级为v3.6.5单次调用行为并记录降级情况。v3.6.6仅提供中止行为。操作5%/三个月监控详情请参见上文“单代理生成器不可用处理”章节。
- **禁止在回合中跨会话恢复**：四阶段生成-评估回合是会话内的原子单元。在回合中手动拆分会话会导致丢失写入者第4a阶段的工件，并强制从第0阶段重新开始。v3.6.7 可能会在模式9中引入 `pre_commitment_history[]` 账本条目，以在会话边界之间保留写入者第4a阶段的工件；v3.6.6 不实现此功能。
- **成对阶段6评估员与`academic-paper-reviewer`外部审核**：成对的`peer_reviewer_agent`（具有v3.6.6合同关卡的阶段6评估员）和独立的`academic-paper-reviewer`技能（阶段3五人组外部编辑审核）服务于不同的审核层级，并根据设计文档§1已知限制记录为已知技术债务。路由/合并决策将由v3.7.x决定。

## 操作模式（10种模式）

有关详细信息，请参见`references/mode_selection_guide.md`。

| 模式 | 触发器 | 代理 | 输出 |
|------|---------|--------|--------|
| `full` | “写论文” | 所有9个（如果是定量则为11个） | 完整论文草稿（如适用，含图表） |
| `outline-only` | “论文大纲” | 1->2->3 | 详细大纲及证据图 |
| `revision` | “修改论文” | 8->5->6 | 带修改痕迹的修订稿（使用`templates/revision_tracking_template.md`） |
| `abstract-only` | “写摘要” | 1->7 | 双语摘要及关键词 |
| `lit-review` | “文献综述” | 1->2 | 注释书目及综合分析 |
| `format-convert` | “转换为 LaTeX” / “将引用转换为[格式]” | 仅 9 | 格式化文档；包括引用格式转换 (APA 7 / 芝加哥 / MLA / IEEE / 温哥华) |
| `citation-check` | “检查引用” | 仅 6 | 引用错误报告 |
| `plan` | “指导我的论文” / “帮助我规划论文” | 1->10->3->4 | 章节计划   INSIGHT 收集 |
| `revision-coach` | “解析评论” / “修订路线图” / “我收到了评审意见” | 仅 12 | 修订路线图   可选跟踪模板   回复信模板 |
| **`disclosure`** (v3.2) | **“《自然》AI披露” / “生成AI使用声明”** | **仅限9** | **场地特定AI-使用披露段落的放置说明** |

### 快速模式选择指南

| 您的情况 | 推荐模式 | 范围 |
|----------------|-----------------|----------|
| 从零开始且有明确研究问题 | `full` | 平衡 |
| 在写作前需要规划帮助 | `plan` | 原创性 |
| 只需要一个大纲 | `outline-only` | 平衡 |
| 有草稿，收到审稿反馈 | `revision` | 保真 |
| 有非结构化的审稿人意见 | `revision-coach` | 平衡 |
| 只需要摘要 | `abstract-only` | 保真 |
| 需要提供引用 | `citation-check` | 保真 |
| 需要转换格式（LaTeX, DOCX）或引用风格 | `format-convert` | 保真 |
| 想要一篇系统的文献综述论文 | `lit-review` | 可信度 |
| 需要一个针对特定刊物的 AI- 使用披露声明以提交 | `disclosure` | 可信度 |

**谱系** (v3.2)：*保真度* = 模板重、输出可预测；*平衡* = 默认；*原创性* = 探索性强、模板少。完整的跨技能谱系表见 `shared/mode_spectrum.md`。

 不确定？从 `plan` 开始——它会逐步引导你。`disclosure` 是最后一步——在论文草稿完成后运行，针对你计划提交的期刊或会议。

 ### 模式选择逻辑

 > 触发到模式映射及完整选择流程图见 `references/mode_selection_guide.md`。

 ---

 ## 计划模式：逐章指导计划

苏格拉底模式，通过逐章指导用户进行论文规划。通过结构化对话构建完整的论文蓝图。

> 有关完整的逐章对话流程和论文蓝图结构，请参见 `references/plan_mode_protocol.md`。

---

## 移交协议：深度研究 -> 学术论文

`intake_agent` 会自动检测深度研究材料（RQ 简报 / 参考书目 / 综合 / INSIGHT 收藏）并跳过冗余步骤。完整的移交材料格式请参见 `deep-research/SKILL.md` 移交协议。

---

## 失败路径

详情请参见 `references/failure_paths.md`。快速参考：

| 失败场景 | 处理策略 |
|---------|---------|
| 研究基础不足 | 建议先运行 `deep-research` |
| 论文结构选择错误 | 返回第二阶段，建议替代结构 |
| 字数显着偏离 over/under 目标 | 识别有问题的章节，建议 trimming/expansion |
| 引用格式完全错误 | 重新运行整个引用阶段 |
| 同行评审拒稿 | 分析拒稿原因，建议重大修改或重组 |
| 计划模式未收敛 | 建议切换至仅大纲模式 |
| 不完整的交接材料 | 列出缺失项目，建议补充或重新执行 |
| 用户中途放弃 | 保存已完成的章节计划 |

---

## 完整学术流程

请参见 `academic-pipeline/SKILL.md` 获取完整工作流程。

---

## 阶段 0：配置访谈

请参见 `agents/intake_agent.md` 获取阶段 0 配置访谈的完整字段定义。访谈涵盖 9 项内容：论文类型、学科、目标期刊、引用格式、输出格式、语言、摘要、字数以及现有材料。输出论文配置记录，等待用户确认。

---

## 文件结构

**代理定义**：`agents/{agent_name}.md` — 每个代理一个文件（共 12 个，与上表“代理团队”对应）。

**参考文献**（`references/` 中的 19 个文件）：
- 引用：`apa7_extended_guide`、`apa7_chinese_citation_guide`、`citation_format_switcher`
- 写作：`academic_writing_style`、`writing_quality_check`、`writing_judgment_framework`
- 结构：`paper_structure_patterns`（6 种类型）、`abstract_writing_guide`
- 领域：`hei_domain_glossary`（双语）、`journal_submission_guide`、`latex_template_reference`
- 过程：`failure_paths`（12 个场景）、`mode_selection_guide`（10 种模式）、`plan_mode_protocol`、`workflow_phase_details`
- 伦理：`credit_authorship_guide`（CRediT 14 个角色）、`funding_statement_guide`、`statistical_visualization_standards`
- 披露 (v3.2)：`disclosure_mode_protocol`（特定场馆 AI- 使用声明生成）、`venue_disclosure_policies`（v1 数据库：ICLR，NeurIPS，Nature，Science，ACL，EMNLP）
- 另外：`deep-research/references/apa7_style_guide.md`（基础参考，此处扩展）

**模板**（`templates/` 中的 11 个文件）：`imrad`、`literature_review`、`case_study`、`theoretical_paper`、`policy_brief`、`conference_paper`、`latex_article_template.tex`、`bilingual_abstract`、`credit_statement`、`funding_statement`、`revision_tracking`（4 种状态类型）。


**示例**（`examples/` 中的 5 个文件）：`imrad_hei_example`、`literature_review_example`、`plan_mode_guided_writing`、`chinese_paper_example`、`revision_mode_example`。

---


## 反模式



明确的禁止以防止常见失败模式：

| # | 反模式 | 失败原因 | 正确行为 |
|---|-------------|-------------|-----------------|
| 1 | **典型的过度使用词语** | “深入探讨”、“至关重要”、“需要注意的是”=瞬间被AI检测 | 使用学科特定的词汇；参见`references/writing_quality_check.md` |
| 2 | **破折号滥用** | 每页超过2个破折号表明AI写作 | 使用括号、逗号，或重构句子 |
| 3 | **开场白冗余** | “在本节中，我们将讨论……”没有提供信息 | 直接从论点或发现开始 |
| 4 | **统一段落长度** | 每段为 4-5 句 = 单调的 AI 节奏 | 自然变化段落长度（2-8 句） |
| 5 | **⚠️ IRON RULE：捏造引用** | 编造听起来合理但不存在的参考文献 | 每条引用必须通过 DOI 或 WebSearch 验证；参见 `academic-pipeline/agents/integrity_verification_agent.md` |
| 6 | **谄媚式修改** | 在没有批判性评估的情况下接受所有审稿人反馈 | 当审稿人错误时使用 REVIEWER_DISAGREE 状态；提供证据进行说明 |
| 7 | **修订期间范围蔓延** | 添加未请求的 sections/analyses 来“改进”论文 | 修订仅解决审稿人关注的问题；新内容需要明确的用户批准 |
| 8 | **忽略失败路径** | 尽管出现直接拒稿信号或严重方法学缺陷，仍然继续 | 检查 `references/failure_paths.md`；触发时调用 F11 直接拒稿恢复 |

---

## 质量标准

### 写作质量
1. **每一条论断都必须有引用**，或由论文自身数据支持
2. **不得有孤立引用** — 文中引用<->与参考文献list必须完全对应
3. **术语一致** — 使用适合本学科的学术语气
4. **逻辑流畅** — 段落和章节之间过渡清晰
5. **字数符合要求** — 在目标字数的+/-10%范围内

### 双语摘要质量
6. **独立撰写** — 中文（繁体）和英文摘要独立完成，NOT 机械翻译
7. **结构对齐** — 两种摘要涵盖相同的关键点且顺序一致
8. **关键词** — 每种语言 5-7 个，反映论文的核心概念
9. **字数** — 英文：150-300 词；中文（繁体）：300-500 字

### 引用质量
10. **格式符合性** — 完全遵守所选引用格式
11. ⚠️ IRON RULE: **DOI 包含** — 每个带有 DOI 的来源都必须包含它；每个引用都必须通过 DOI 或网络搜索验证
12. **时效性** — 标记超过10年的来源（除非是开创性作品）
13. **自引比率** — 如果 >15% 则标记

### 同行评审
14. **五个维度** — 创新性（20%）、方法严谨性（25%）、证据充分性（25%）、论证连贯性（15%）、写作质量（15%）
15. **可操作的反馈** — 每条批评必须包括具体建议
16. **最多2轮修订** — 未解决的问题将成为已知限制

### 强制性包含内容
⚠️ **IRON RULE**：每篇论文MUST必须包含：数据可用性声明、伦理声明、作者贡献（CRediT）、利益冲突声明、资金致谢。
17. **AI披露声明** — 每篇论文必须包含一条关于AI工具使用的声明
18. **局限性部分** — 明确讨论研究局限性
19. **伦理声明** — 在适用的情况下（涉及人体受试者、敏感数据）

---

## 输出语言

遵循用户语言。学术术语保持英文。无论主体文本语言为何，均提供双语摘要。

---

## 与其他技能的整合

```
academic-paper + tw-hei-intelligence  -> Evidence-based HEI paper with real MOE data
academic-paper + deep-research        -> Deep research phase -> paper writing phase (auto-handoff)
academic-paper + report-to-website    -> Interactive web version of the paper
academic-paper + notebooklm-slides-generator -> Presentation slides from paper
academic-paper + academic-paper-reviewer -> Peer review -> revision loop
```

---

## Version Info

|项目 |内容 |
|------|---------|
|技能版 |3.1.1 |
|最后更新 |2026-04-27 |
|维护者 |吴承一 |
|依赖技能 |深度研究v1.0（上游）、学术论文评审v1.0（下游） |

---

## 版本历史

>完整版本历史请参见`references/changelog.md`。
