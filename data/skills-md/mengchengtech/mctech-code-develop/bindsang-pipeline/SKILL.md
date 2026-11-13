---
name: bindsang-pipeline
名称: bindsang-pipeline
版本: 1.2.1
description: >
  编排子 Agent 完成 OpenSpec Change（探索→设计→审核→规划→实施→验证；含需求变更与外部 BUG）。
  使用：用户要求「流水线 / 子智能体 / 多 Agent」；跨模块功能、重构、公共接口变更；只要设计+评审；已有 Spec 要实施验证；
  需求变更；外部 BUG；继续/恢复某 Change；点名 explorer/designer/reviewer/planner/executor/verifier。
  不要使用：单模块小功能、已定位根因的 bug 修复、样式或文案、依赖升级、纯代码解释/代码评审、概念咨询、与仓库无关问答
  （直接完成请求，不建 Change、不派子 Agent）。轻量改代码可只做最小 preflight+验证，不必 full-flow。
描述: 识别任务类型与复杂度，编排六角色子 Agent；产物在 changes/<id>/.pipeline/ 与 OpenSpec。选用与派发见 references/orchestrator-protocol.md。
---

# 主 Skill：Agent + Subagent 开发流水线

## 1. 目标与边界

你是开发流水线的**主 Agent（Orchestrator）**。你负责识别意图、准备工作区、创建或恢复 Change、选择流水线、分派子 Agent、检查交付物、推进状态、请求人工决策以及维护可回滚记录。

你不是所有专业工作的执行者。探索、分析、设计、审核、规划、编码和验证应优先委派给对应子 Agent。主 Agent 对所有结果负责，但不得把子 Agent 的结论未经检查直接当作事实。

本 Skill 不依赖某一款 Agent 工具。若运行环境不支持真正的多 Agent，则由主 Agent 按角色提示分阶段模拟执行，并保持相同的输入、输出和检查协议。

## 2. 何时使用 / 不使用

与 `references/orchestrator-protocol.md` §选用 一致：命中「使用」→ 读 §3 分类并打开对应 `pipelines/<id>.md`；命中「不使用」→ **不加载本 Skill 编排**，直接完成用户请求。

### 2.1 使用（满足任一条即可考虑）

| 用户意图 / 关键词 | 典型 `task_type` |
|---|---|
| 流水线、子智能体、多 Agent、分角色、bindsang | 按 §3 分类 |
| 新功能、大重构、跨模块、公共接口/契约变更 | `full-flow` |
| 出设计、方案、架构、先不实现、设计评审 | `design-review` |
| 按已定设计/OpenSpec 实施、执行 Task、验证 | `implement-verify` |
| 需求变了、改规则、扩范围、行为变更 | `requirement-change` |
| 报 BUG、崩溃、不一致、线上异常（外部输入） | `bug-feedback` |
| 继续 / 恢复 / 调整未结束 Change | 读 `pipeline-state.yaml` 续跑 |
| 点名 `explorer` / `designer` / … 或描述角色顺序 | 单点或 §3.1 临时组合 |

各流水线「先问再用」条件（跨多文件、 unfamiliar 代码、多方案取舍、验收不明等）见 `pipelines/full-flow.md` 等 **触发** 节；满足时一句话说明多 Agent 代价后询问，用户同意再 preflight。

### 2.2 不使用（勿建 Change、勿派子 Agent）

以下情形 **直接做**，不启动完整流水线：

- 单模块小功能、局部一两处修改且边界清晰  
- **已定位根因** 的缺陷修复，用户未要求流水线  
- 样式、文案、配置微调（无行为/契约变化）  
- 仅升级依赖、锁版本（无配套改造流水线）  
- 代码解释、走读、**代码评审**（非独立 reviewer 角色委派）  
- 概念咨询、算法/语法问答、与当前仓库无关的一次性问题的  
- 用户明确「不要流水线 / 不用子 Agent / 你直接改」

内部 verifier 发现的实现问题：留在当前 Change 的 `implement-verify` 循环，**不**为此新建 `bug-feedback`。

### 2.3 轻量路径

用户要小改代码但未禁流水线时：可 **L1** 裁剪（§5，合并探索+分析、简化审核），仍须 `brief.md`、基线、必要验证与 `.pipeline/` 记录；不得跳过用户已声明的破坏性风险确认。

### 2.4 歧义

无法判断「讨论方案」是否授权改代码 → **只问一个关键问题**；未确认前不得 executor。不得把「一起看看」默认为实施许可。

## 3. 入口识别与任务分类

按以下优先级判断：

1. 用户明确指定的任务类型优先。
2. 明确 BUG 现象优先归类为 `bug-feedback`，除非用户明确要求将其作为新需求设计。
3. 明确“只出方案/设计评审/不实现”归类为 `design-review`。
4. 明确“直接实施/执行/验证”，且已有获批设计或需求基线，归类为 `implement-verify`。
5. 对现有功能的扩展、优化、行为改变归类为 `requirement-change`。
6. 新功能或重构归类为 `full-flow`。
7. 无法判断时，只问一个最关键的澄清问题；不得擅自将“讨论方案”理解为“允许改代码”。

任务类型：
- `full-flow`：新功能/重构的探索到实现验证全流程。
- `design-review`：探索、分析、设计与审核，停在人类确认。
- `implement-verify`：基于已有批准输入进行规划、执行、验证。
- `requirement-change`：对既有功能提出变更，完成影响分析、设计审核、确认和实施验证。
- `bug-feedback`：接收外部 BUG，先复现与定位，再按修复规模选择快速修复或升级到设计变更流程。

## 3.1 用户指定角色与临时流水线组合

除预定义流水线外，支持用户直接点名一个或多个角色，或用自然语言描述协作顺序。

- 用户点名角色时，将其视为角色选择约束；用户描述顺序时，严格保留明确顺序。
- 同时指定角色与顺序时，两者都必须满足；若冲突，向用户澄清。
- 若角色组合/顺序匹配预定义流水线，使用预定义流水线；否则创建仅对当前 Change 生效的临时自定义流水线，不修改标准 `pipelines/` 文件。
- 未指定顺序时按角色依赖关系排序；不得违反输入依赖。例如 reviewer 必须先有可审核的设计或规格。
- 自动补齐必要的前置准备、权限检查、人工确认门禁和收尾步骤；用户明确只出设计或禁止执行时，不得加入代码执行。
- 缺少必要前置输入时暂停并请求补充；不得让后置角色基于不存在的产物工作。
- 在 `.pipeline/custom-pipeline.md` 记录用户原始要求、角色序列、依赖、裁剪理由、门禁和退出条件；状态文件标记 `task_type: custom`、角色序列及自定义定义文件路径。
- 临时流水线仍遵循角色权限、交互协议、产物规范、回滚和状态机；主 Agent 是唯一状态管理者。

示例：
- `explorer → designer`：探索后设计，最后人工确认。
- `designer → reviewer → designer → reviewer`：按指定顺序循环，直到通过或达到退出条件。
- `planner → executor → verifier`：先检查已有批准设计和验收标准，再规划实施验证。
- `explorer + reviewer`：只有 reviewer 已有可审查输入时才可并行，否则先满足依赖。

## 4. 前置准备阶段（所有流水线必经）

阶段 ID：`preflight`。在调用任何专业子 Agent 前执行。

### 4.1 准备任务

1. 确认当前工作目录、仓库根目录、分支、工作区是否干净。
2. 识别项目技术栈、模块边界、构建/测试/静态检查命令、代码规范和重要约束。
3. 检查是否已有未完成 Change；询问或依据用户指定恢复目标，禁止静默覆盖。
4. 创建唯一 Change 标识：`YYYYMMDD-短名称`；若冲突追加序号。
5. 创建 Change 根目录及 `.pipeline/` 子目录（含初始状态文件）。
6. 建立基线：记录当前 Git commit、分支、工作区差异、关键测试基线（若可执行）。
7. 读取项目现有规范、架构文档、OpenSpec 配置及 ADR 目录约定；优先沿用项目既有规范。
8. 明确任务目标、非目标、已知约束、验收标准、风险和待确认事项。
9. 生成初始任务简报并提交/保存到仓库。

### 4.2 Change 根目录与 `.pipeline/`

Change 根目录默认为 `changes/<change-id>/`。若仓库已有 `openspec/changes/<change-id>/` 等既定结构，以其为 Change 根目录，不另建平行目录。

**OpenSpec 交付物**写在 Change 根（`proposal.md`、`design.md`、`tasks.md`、`specs/` 等），便于 `openspec` CLI 校验。**流水线编排与子 Agent 产出的文档**一律写在 Change 根下的 `.pipeline/` 中，与规格交付物分离：

```
<change-root>/
├── proposal.md、design.md、tasks.md、specs/…   # OpenSpec（Designer / Planner）
└── .pipeline/
    ├── pipeline-state.yaml
    ├── brief.md
    ├── baseline.md
    ├── decisions-log.md
    ├── custom-pipeline.md          # 仅 task_type: custom 时
    ├── exploration/、analysis/、decision/、review/
    ├── planning/、execution/、verification/、bug/
    └── …各阶段 ADR 与执行记录
```

### 4.3 前置准备输出

在 `<change-root>/.pipeline/` 下创建：
- `pipeline-state.yaml`：机器可读的流程状态。
- `brief.md`：目标、背景、范围、非目标、约束、**可验证验收标准**、**验证命令**、**验证环境**、开关（含 `commit_policy`，默认 `checkpoint`）、角色映射、`role_models`（可选）、用户原始输入。
- `baseline.md`：仓库状态、基线 commit、分支、已有差异、测试基线。
- `decisions-log.md`：人工决策与重要流程决策记录（仅主 Agent 追加，规则见 `orchestrator-protocol.md`）。
- `run.log`：派发审计（初始为空）。

委派子 Agent 时，路径以 Change 根为基准：流水线文档使用 `.pipeline/` 前缀（例如 `.pipeline/brief.md`）；OpenSpec 文件使用 Change 根相对路径（例如 `design.md`）。

## 5. 复杂度评估与动态裁剪

由主 Agent 在 `preflight` 后给出复杂度：`L1-轻量`、`L2-中等`、`L3-复杂`。说明依据并记录在 `.pipeline/brief.md`。

| 维度 | L1 | L2 | L3 |
|---|---|---|---|
| 影响范围 | 单函数/单文件/局部配置 | 单模块或少量服务 | 跨模块/跨服务/平台级 |
| 业务不确定性 | 清晰 | 少量待澄清 | 核心规则或边界不清 |
| 技术风险 | 低、可逆 | 有兼容/数据风险 | 架构、迁移、数据或安全风险 |
| 变更规模 | 小 | 中 | 大/多阶段 |
| 验证难度 | 单测/静态检查 | 集成或回归 | 多系统、性能、迁移或灰度 |

建议规则：
- L1：可合并探索与分析；设计与审核可由不同角色快速检查或使用轻量检查清单；规划可简化为任务清单。不得省略基线、风险识别、必要验证和结果记录。
- L2：按标准步骤执行；设计至少一轮审核；执行按可独立验证的批次推进。
- L3：完整流程；设计/审核可多轮；规划拆分里程碑；执行与验证多轮；高风险变更设置额外人工确认点。

裁剪只允许合并或缩短步骤，不允许省略以下门禁：
- 未确认范围和破坏性风险，不得执行不可逆操作。
- 未有验收标准，不得宣称验证通过。
- 未记录基线，不得进行仓库级回滚。
- 未经用户授权，不得提交、推送、发布、执行生产数据迁移或删除数据。

## 6. 流水线总览

| 类型 | 主路径 |
|---|---|
| 全流程开发 | 见 `pipelines/full-flow.md` |
| 只设计评审 | 见 `pipelines/design-review.md` |
| 只实现和验证 | 见 `pipelines/implement-verify.md` |
| 需求变更 | 见 `pipelines/requirement-change.md` |
| BUG 反馈 | 见 `pipelines/bug-feedback.md` |

`*` 表示可重复。设计审核循环由审核结论驱动；执行验证循环由验证结果驱动。

## 7. 主 Agent 调度规则

编排层协议（选用、派发块、硬约束、并发、角色解析、恢复、结束汇报）见 **`references/orchestrator-protocol.md`**。

1. 每个阶段开始前，读取当前状态与该阶段输入；确认前置产物存在。
2. 根据 `roles.md` 选择角色与**模式**，读取 `agents/role-*.md`，并按 `pipelines/<task_type>.md` 执行阶段与预算。
3. 委派遵守派发块：只传路径与约束，不复述产物全文（见 orchestrator-protocol）；**默认不传 `model`**，沿用 `.cursor/agents/` 注册模型；仅 `brief.role_models` 或用户当轮显式指定时可覆盖。
4. 子 Agent 不推进总状态、不派生子 Agent、不改写 `decisions-log.md` 已确认项。
5. 主 Agent 验收产物；读返回时优先 verdict，按需读节（见 orchestrator-protocol §读返回）。
6. 阶段完成后更新 `pipeline-state.yaml`；确认决策追加 `decisions-log.md`；每次派发返回后追加 `run.log`；`commit_policy=checkpoint`（默认）且用户已授权 commit 时按 `git-checkpoints.md` 做检查点 commit 并记 `last_checkpoint_commit`。
7. 到达人工确认点：按流水线「检查点」指令表停等用户（见 `pipelines/design-review.md` 等）。
8. 用户反馈按 §8 路由；临时角色组合默认不自动循环（orchestrator-protocol）。
9. 任何外部输入不得覆盖已批准决策；须追加记录并评估影响。

## 8. 人工确认后的自动路由

收到用户确认或修改意见后，先将反馈拆成原子事项，再逐项路由：

- **探索回退**：事实不足、代码现状理解错误、依赖关系遗漏、需要补充调研。
- **分析回退**：目标/需求理解错误、边界条件遗漏、影响面或风险分析不足。
- **设计回退**：目标不变，但方案、接口、数据模型、兼容策略或技术取舍需调整。
- **审核回退**：设计内容已基本正确，仅需补齐审查意见或证据。
- **规划回退**：设计不变，但任务拆分、依赖、顺序、验收点需调整。
- **继续后续**：确认内容与已批准产物一致，无阻塞项。
- **需求变更新 Change**：用户新增目标、改变业务规则或扩大范围，且会改变已批准基线。不得把实质需求变更伪装成普通修订。

多个反馈点可能路由到不同阶段。按最早受影响阶段回退，并重新执行其后的依赖阶段。主 Agent 必须说明路由依据。

## 9. 设计审核循环

设计 Agent 输出版本化方案。审核 Agent 独立审查，不得仅复述设计。

审核结论只能是：
- `APPROVE`：通过，可进入人工确认或下一阶段。
- `REVISE`：列出必须修改项，回到设计。
- `REJECT`：方案存在根本性问题，回到分析或探索，并说明原因。
- `NEED_INFO`：证据不足，回到探索/分析补充。

每轮设计与审核都保存独立 ADR，不覆盖上一轮。主 Agent 维护轮次与当前有效版本。

## 10. 执行验证循环

执行 Agent 按规划中的一个或多个任务批次实施。每批完成后交由验证 Agent 验证。

验证结论：
- `PASS`：该批达到验收标准，可进入下一批或结束。
- `FAIL`：明确失败证据、复现方式和影响，回到执行修复。
- `BLOCKED`：环境/依赖/权限阻塞，主 Agent 请求用户处理或调整计划。
- `SCOPE_CHANGE`：实现过程中发现需求或设计基线不成立，暂停执行并回到分析/设计，不得自行扩大范围。

每轮执行记录代码差异、测试命令、结果、未覆盖项和已知风险。

## 11. BUG 与内部验证缺陷的区别

- 验证阶段发现的问题属于**内部验证缺陷**，留在当前 Change 的执行—验证循环，不创建外部 BUG 流水线。
- 用户/业务方/监控系统新输入的问题属于**外部 BUG 反馈**，进入 `bug-feedback`。
- 若外部 BUG 经分析实为新需求或既有规则调整，转成 `requirement-change` 或新 Change，并保留原 BUG 与新 Change 的关联。

## 12. 需求变更处理

需求变更必须记录：
- 变更来源、提出人/渠道（若已知）、提出时间；
- 变更前后行为对比；
- 变更原因与期望结果；
- 受影响的已批准 ADR、OpenSpec 规格、任务和代码；
- 兼容性、数据迁移、回滚和发布风险。

变更若发生在执行中：暂停受影响任务；评估已完成代码是否保留；更新设计和任务计划；重新经过必要审核与人工确认。不得直接在原任务描述上覆盖历史。

## 13. 持久化、Git 与恢复

- 每个阶段结束后保存文档；每个执行批次结束后保存代码和验证证据。
- 默认只在本地工作区创建/更新文件，不自动 push；`brief.md` 默认 `commit_policy: checkpoint`。
- **阶段性提交**：用户授权 commit 且 `commit_policy` 为 `checkpoint`（或未写明，视同 `checkpoint`）时，按 **`references/git-checkpoints.md`** 在子 Agent 单次派发终态、每个 Task 完成、verifier `PASS`、确认门等检查点提交，避免未提交变更积压。消息形如 `docs(<change-id>): …`、`feat(<change-id>): task …`。
- 仅用户授权可 commit；push、发布和生产操作必须单独授权。
- 每次状态变化更新 `.pipeline/pipeline-state.yaml`，包含当前阶段、状态、轮次、产物清单、基线 commit、`last_checkpoint_commit` 与待办。
- 恢复时读 `pipeline-state.yaml`、`brief.md`、`run.log` 末行与产物首行 verdict（见 orchestrator-protocol §恢复）；并核对 Git 与文档/代码一致性。

## 14. 结束条件

满足以下条件方可结束：
- 所有范围内任务均已完成或明确标记未完成；
- 验证达到验收标准，或明确记录阻塞与豁免；
- 设计/变更/BUG 决策有记录；
- OpenSpec 与实现状态一致；
- 风险、未解决问题、回滚方式和后续事项已记录；
- `.pipeline/pipeline-state.yaml` 标记 `completed`、`completed_with_exceptions` 或 `awaiting_human`。

结束时向用户输出：完成摘要、变更文件、验证证据、未解决项、风险、回滚点和下一步建议。
