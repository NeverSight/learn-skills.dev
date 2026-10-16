---
name: cohestra
description: 通过 init 初始化项目协作上下文，按 need、design、code、review、fix、validate 执行指定阶段，按 verify 做阶段间偏差核对，或按 report 只读汇总项目任务状态与遗留问题。六阶段可从任意阶段起步；阶段缺 .cohestra 时先提醒并初始化，report 不初始化或写入；任务 README Front Matter 提供机器可读契约；仅讨论流程不触发执行。
license: MIT
---

# Cohestra

一个技能，按阶段读取说明。技能包保存协作规则和提示词；项目 `.cohestra` 只保存项目入口、任务交付和复盘。技能版本见 [release.json](release.json)，协作协议为 v0.8。任务 README 的 YAML Front Matter 提供机器可读契约（Orchestrator Contract），Markdown 正文保持人类/智能体可读，字段与枚举见 [公共流程](references/workflow.md) 第 7 节。AC、handoff、findings、候选、轮次、阶段状态与工作项状态等术语见 [公共流程](references/workflow.md)。
 
## 路由

`$cohestra <入口>` 表示技能调用意图，不是终端命令；其他工具采用其技能调用写法。阶段调用后附原始需求、handoff 文件或任务目录，以及本次补充；未附 handoff 与任务目录时按[公共流程](references/workflow.md)第 1 节的自动衔接规则取用。`report` 默认汇总当前项目全部任务，不选择单个上游交付。

| 入口 | 按需读取 | 职责 |
|---|---|---|
| init | [init](references/init.md) | 建立或复用项目上下文容器，不执行任务 |
| need | [need](references/need.md) | 澄清需求（含提问）、范围与验收 |
| design | [design](references/design.md) | 设计方案、执行计划和验证方法 |
| code | [code](references/code.md) | 按有效设计实施并交付候选 |
| review | [review](references/review.md) | 审查固定候选，输出 findings |
| fix | [fix](references/fix.md) | 裁决并修复审查问题 |
| validate | [validate](references/validate.md) | 补足证据，判断验收状态 |
| verify | [verify](references/verify.md) | 核对某阶段产出与其上游依据的偏差 |
| report | [report](references/report.md) | 只读展示项目任务总览、遗留问题与状态异常，不落盘 |

## 起步位置

六阶段 **need → design → code → review → fix → validate** 是职责清单，不是必经路线。用户指定哪个入口就从哪里开始，终点也由用户决定。`init` 由技能在容器缺失时自动补做，用户不必先手工执行。

| 常见诉求 | 起步 |
|---|---|
| 新的完整产品需求 | need，走到 validate |
| 发现 bug，或已定位的缺陷 | fix（已有 findings）或 code（本轮直接定位） |
| 页面样式探索与优化 | design → code |
| 接口参数、文案等明确小改 | code → review |
| 已有候选、只缺证据 | validate |

## 执行规则

以下规则适用于所有入口。

1. 先固定目标项目绝对路径并读取适用项目规则；目标不因技能安装位置或切换目录而改变。未给路径时使用当前任务项目，多个候选无法区分时再询问。
2. 按用户指定入口执行；自然语言已明确阶段时可直接路由。缺少阶段、阶段互相矛盾或名称未知时澄清，不猜测阶段，也不在目标未确认时初始化。`validate` 与 `verify` 是规范名称，不可混用：前者补验收证据，后者只核对偏差。
3. `report` 全程只读：缺 `.cohestra` 时报告未初始化，不触发 init；不写交付物、索引、状态或报告文件。其余阶段进入前先确认目标项目已有 `.cohestra`：缺失时报告目标绝对路径并说明将执行一次初始化，然后按最小范围执行 init（只建容器与项目入口，不读业务任务、不清旧副本、不生成任务、不暂存或提交），完成后继续本阶段；容器存在则直接进入，不重复初始化。目标不明确、指向技能源仓库或无法安全写入时不初始化，先澄清或报告。
4. `init` 只读取初始化说明及所需模板；`report` 只读 [report](references/report.md)、发行版本、目标项目任务索引及其必要问题来源，字段解释有疑问时查 [公共流程](references/workflow.md) 第 7 节，不预读各阶段说明。其余入口读取一次公共流程、本阶段说明和发行版本，再定位任务索引及必要输入，不预读其他阶段、所有任务或全部复盘。写交付时再读对应骨架。
5. 业务规范、有效任务决定和已有用户授权保持效力。只执行指定的阶段，不因阶段相邻或仍在链条内而自动继续；为进入阶段而做的初始化是前置动作，不构成跨阶段继续。不自动提交、发布或启动其他智能体。
6. need、design、code、fix 交付后向用户提议一次 `verify` 并给出建议核对范围，是否执行由用户决定，不设前置条件；`review`、`validate` 本身是正式验证关口，交付后不提议 verify，需要时由用户主动调用。
7. 正式阶段交付后按[公共流程](references/workflow.md)第 5、7 节把结构化状态写入任务 README Front Matter，正文「推荐下一步」与 `next` 字段保持一致；必须先收到并确认发布前校验成功结果，再用后续工具调用发布，校验失败不继续。外部编排只读该契约即可判断控制流。Cohestra 一次阶段调用只执行一个阶段，`report` 是查询入口，不占阶段或轮次，不推进任务；不含 queue、batch、run-all、scheduler 等多任务调度入口，编排由外部系统负责。
8. 调用方声明 `execution_mode: unattended` 时按[公共流程](references/workflow.md)第 7.4 节执行无人值守语义：不提问空等、不自行选择产品方向、不扩大范围、不产生新的隐含授权、不降低质量门禁；无法在现有信息下合法继续时标记受阻并停止。该模式下规则 6 的 verify 提议按跳过处理并记入交付物，不改控制字段。默认 `attended` 行为不变。`report` 在两种模式下均只读，缺口仅在回复中说明，不写入受阻状态。

## 来源与版本

- 从本次实际加载的技能目录读取规则和模板，不从工作目录猜测技能位置；也不把提示词复制回项目 `.cohestra/prompts`。
- 每轮交付记录实际 Skill 发行版本和协议版本，保留旧版交付与合并文件。升级技能不改写任务决定、验收要求或历史结果。
- 同名技能存在多份时使用明确选择的入口；无法确定来源时报告位置并澄清，不假设用户级或项目级一定优先。
- 用户级升级影响后续调用。项目需要独立固定版本时使用项目级安装并随 Git 管理；不要从初始化记录推断当前实际技能版本。
- 不提供项目模板同步的 `update` 入口。用户提出旧 `$cohestra update` 时说明改由技能管理器升级；仅在安装、升级或迁移问题中读取 [安装说明](references/installation.md)，不自动运行更新命令。

## 交付

阶段结果必须先落盘再交接。最终回复给出交付物绝对路径、结论、索引是否同步、必要待办、对口 verify 的提议与用户选择，以及下一阶段调用和准确输入；无需复述整份文档。`report` 例外：直接在对话中输出报告与来源链接，不落盘、不同步索引、不提议 verify，输出后停止。
