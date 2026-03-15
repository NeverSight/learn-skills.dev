---
name: heroagent
description: 帮你定目标、拆计划、管进度、沉淀知识的工作流 skill，适用于目标推进、复盘总结和项目知识维护。
---

# HeroAgent

## 适用场景

当用户要处理以下问题时，使用 `heroagent`：

- 把模糊意图收敛为明确目标
- 把目标拆成阶段计划、任务清单和当前焦点
- 维护长期推进过程中的状态、完成记录和验收结论
- 复盘问题、提炼原则、固化流程、淘汰旧规则
- 维护 `.heroagent/wiki/` 项目知识库，并在后续动作中优先消费它

若用户只是做一次性代码修改、排错或实现功能，且不涉及目标推进或知识沉淀，不要强行使用 `heroagent`。

## 核心闭环

- 初始化动作：`init`
- 知识动作：`wiki`
- 推进闭环：`want -> plan -> todo -> focus -> achieve | abandon`
- 沉淀闭环：`reflect -> realize -> master -> synthesize -> forget`

优先保持单一主目标。若用户同时提出多个目标，先区分主目标、并行目标、暂存目标，再继续推进。

## 动作入口

默认推荐用 `~动作` 触发，对人和对 AI 都更稳定。

| 指令 | 目的 | 关键约束 |
| --- | --- | --- |
| `~init` | 初始化 `.heroagent/` 工作区 | 先建工作区，再进入后续动作 |
| `~wiki` | 维护并消费 `.heroagent/wiki/` | 先消费现有 wiki，再决定是否补写 |
| `~want` | 定义目标 | 先评分，未达标时只做澄清 |
| `~plan` | 制定路径 | 输出阶段、风险、完成标志 |
| `~todo` | 形成执行单元 | 默认按优先级连续执行，不逐项确认 |
| `~focus` | 查看当前态势 | 只保留当前最值得关注的信息 |
| `~achieve` | 验证目标达成 | 不把任务完成等同于目标达成 |
| `~abandon` | 停止目标并收口 | 明确停损、保留资产与重启条件 |
| `~reflect` | 复盘问题 | 先拆现象、影响、根因 |
| `~realize` | 提炼原则 | 只提炼可迁移原则 |
| `~master` | 固化做法 | 只固化稳定做法，避免过早流程化 |
| `~synthesize` | 传授知识 | 优先用例子而不是定义 |
| `~forget` | 清理过时认知 | 给出替代认知或替代流程 |

规则：

- 用户显式输入 `~动作` 时，直接命中对应动作
- 显式指令优先级高于自然语言路由
- 未使用显式指令时，再按自然语言判断当前最阻塞的一步
- 若一次请求命中多个动作，先处理推进闭环中的阻塞动作，再处理沉淀闭环

## 路由与状态原则

进入任何动作前，先明确三件事：

- 当前对象是什么：目标、计划、任务、问题、知识、流程
- 当前阶段是什么：新建、推进、复盘、归档、淘汰
- 成功标准是什么：完成定义、验收条件、停止条件

始终维护一份轻量状态，至少包含：

- 当前目标
- 当前阶段
- 已知进展
- 下一步动作
- 风险或阻塞

若用户没有提供历史状态，先根据对话重建，不要假装存在外部记忆。

## 核心执行规则

### 先收敛，再展开

若关键信息缺失，先用最少的问题补齐；若可以安全假设，则明确假设后继续。

### 区分事实与判断

输出时区分三类信息：

- **事实**：用户已确认或已观察到的信息
- **判断**：基于事实得出的分析
- **待确认**：影响决策但尚未确认的信息

### 优先产出可执行结果

每个动作都要优先产出可直接使用的结果，例如：

- 清晰目标
- 可执行计划
- 可勾选任务
- 当前进度
- 验收结论
- 可复用原则或流程

### `todo` 默认执行策略

- 进入 `todo` 后，默认按优先级一次性连续执行全部任务，不逐项向用户确认
- 只有遇到关键取舍、高风险变更、权限受限、外部依赖阻塞或需求边界变动时，才暂停并请求确认
- 若任务之间存在明确依赖，先按依赖顺序执行，再继续后续任务
- 若执行中出现新信息，只更新当前状态和剩余任务，不回退成逐项确认模式
- 当 `todo` 全部执行完成后，自动进入“已完成，待验收”的内部状态，下一步默认转入 `achieve`

### `want` 评分门槛

- 先按 [`references/requirement-scoring.md`](./references/requirement-scoring.md) 做 10 分制评分
- 阈值是 `8`
- 评分 `< 8` 时，只做 `目标澄清`，不要直接进入 `plan`
- 达到可进入下一步时，必须让用户在 `继续 ~plan`、`继续补充需求`、`暂不处理` 中选择
- 应同步把状态写入 `progress/workflow-state.json`

### `wiki` 执行门槛

- 命中知识维护或知识消费意图时，优先执行 `wiki`
- 若 `.heroagent/wiki/` 存在，在 `want`、`plan`、`todo`、`focus`、`reflect` 中优先消费其内容
- 先消费现有 wiki，再决定是否补写、生成草稿、合并草稿或切换策略
- 若本轮只生成草稿，必须明确标注“未直接写入正式 wiki”
- 默认只在执行任务后出现代码、接口、数据或架构变化时，自动做 wiki 轻判断
- `want`、`plan`、`todo` 默认不自动触发 wiki 轻判断；它们主要更新目标、计划、任务和当前焦点
- 只有在需求边界、项目事实或技术约束被显式改写时，`want`、`plan`、`todo` 才需要额外触发 wiki 轻判断
- `achieve`、显式 `wiki` 请求前，应优先检查是否存在待同步的 wiki 变化
- wiki 轻判断属于 skill 内部机制，不要求用户手动调用脚本

## 输出约定

使用 `heroagent` 时，回复首行应使用单行状态头，例如：

```md
✅ HeroAgent · 计划制定
❓ HeroAgent · 需要确认
⚠️ HeroAgent · 进度聚焦
💡 HeroAgent · 咨询问答
```

建议紧跟：

```md
重点摘要：
- ...
- ...
```

统一要求：

- 先给结论，再给依据
- 缺失信息明确标注，不伪造内容
- 需要用户决策时，优先给 2 到 3 个低成本选项，并包含 `暂不处理`
- 最后给 `下一步`
- 若需要落盘，优先与 `assets/templates/` 保持一致

详细字段与场景名称，按需读取 [`references/output-contracts.md`](./references/output-contracts.md)。

## 按需加载

不要一次性全量加载资料。按场景读取：

- 路由与状态：
  [`references/command-routing.md`](./references/command-routing.md)
  [`references/state-management.md`](./references/state-management.md)
  [`references/action-trigger-matrix.md`](./references/action-trigger-matrix.md)
- 提问与输出：
  [`references/prompt-patterns.md`](./references/prompt-patterns.md)
  [`references/output-contracts.md`](./references/output-contracts.md)
  [`references/action-examples.md`](./references/action-examples.md)
- 落盘与归档：
  [`references/file-conventions.md`](./references/file-conventions.md)
  [`references/init-conventions.md`](./references/init-conventions.md)
  [`references/bootstrap-conventions.md`](./references/bootstrap-conventions.md)
  [`references/focus-update-conventions.md`](./references/focus-update-conventions.md)
  [`references/archive-conventions.md`](./references/archive-conventions.md)
- wiki：
  [`references/wiki-conventions.md`](./references/wiki-conventions.md)
  [`references/wiki-context-consumption.md`](./references/wiki-context-consumption.md)
  [`references/wiki-sync-rules.md`](./references/wiki-sync-rules.md)

如需直接落盘，优先复用：

- [`assets/templates/goal-card.md`](./assets/templates/goal-card.md)
- [`assets/templates/milestone-plan.md`](./assets/templates/milestone-plan.md)
- [`assets/templates/todo-list.md`](./assets/templates/todo-list.md)
- [`assets/templates/progress-snapshot.md`](./assets/templates/progress-snapshot.md)
- [`assets/templates/retrospective.md`](./assets/templates/retrospective.md)
- [`assets/templates/principle-card.md`](./assets/templates/principle-card.md)
- [`assets/templates/process-card.md`](./assets/templates/process-card.md)

## 优先脚本

只在需要实际落盘、批处理或巡检时调用脚本。优先使用：

- 初始化与状态：`scripts/init_heroagent.py`、`scripts/bootstrap_first_goal.py`、`scripts/update_current_focus.py`、`scripts/archive_goal.py`、`scripts/doctor_heroagent.py`
- `want` 状态：`scripts/update_want_state.py`
- wiki 维护：`scripts/update_wiki_context.py`、`scripts/suggest_wiki_updates.py`、`scripts/refresh_wiki_registry.py`
- wiki 草稿闭环：`scripts/sync_wiki_from_changes.py`、`scripts/apply_wiki_draft.py`、`scripts/reconcile_wiki_state.py`、`scripts/promote_wiki_maintenance.py`
- wiki 增强：`scripts/compact_wiki_memory.py`、`scripts/score_wiki_signals.py`、`scripts/assemble_wiki_context.py`、`scripts/extract_wiki_facts.py`、`scripts/run_wiki_strategy.py`

内部状态机制：

- wiki 轻判断由 skill 自动触发，可复用 `scripts/update_wiki_signal_state.py`，但不作为面向用户的公开命令

## 响应风格

保持语言简洁、明确、可执行。优先：

- 先给结论，再给依据
- 少讲术语，多讲动作
- 少给大而空的框架，多给当前可用结果
- 对未确认事项直接标注，不自行脑补

除非用户明确要求，不要引入复杂理论命名或冗长方法论。
