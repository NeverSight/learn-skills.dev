---
name: bkn-ontology-builder
description: 当需要基于 PRD、会议纪要、流程说明、系统/数据材料、BKN_Creator 交接摘要或已有方案，生成、修订或对比业务可评审的 OpenBKN BKN 本体建模方案时使用。
---

# BKN Ontology Builder

## 目标

`bkn-ontology-builder` 面向 OpenBKN BKN 项目生成业务可评审的本体建模方案。它把 PRD、会议纪要、流程说明、系统与数据材料、`BKN_Creator` 交接摘要或粗略业务描述，整理为业务侧可以确认的建模方案：业务世界如何抽象为对象、关系、逻辑、行动、治理和协作边界。

核心交付物是 `《<项目或场景> 本体建模方案》`，不是评审报告，也不是 `.bkn` 文件。

## 定位与边界

本 Skill 是需求发现和正式 BKN 建模之间的可选环节：

```text
业务材料 / PRD / handoff
  -> 可选 bkn-ontology-builder
  -> 业务可评审的本体建模方案
  -> BKN_Creator
  -> .bkn、校验、绑定、测试、平台操作
```

不做以下事情：

- 不生成 `.bkn` 文件；
- 不绑定数据源或平台数据视图；
- 不推送知识网络到 OpenBKN；
- 不执行平台 Action 或平台查询；
- 不替代 `bkn-requirement` 生成 PRD；
- 不替代 `bkn-creator` 做正式 BKN 建模、校验、绑定和推送；
- 不把本体建模方案作为 `BKN_Creator` 的强制准入门禁。

若用户明确要求创建、更新、校验、绑定、测试或推送 BKN，应转交 `bkn-creator`。若用户只有很粗略想法且业务目标、场景、流程和验收问题不足，应先输出成熟度缺口，必要时建议使用 `bkn-requirement`。

## 输出模式

按输入状态选择模式，不默认强行生成完整方案。

| 输入状态 | 默认模式 | 输出 |
|---|---|---|
| 只有粗略想法，业务目标或材料不足 | `intake_or_readiness_check` | 缺口、建议补充材料、是否建议先走 `bkn-requirement` |
| 有 PRD、handoff、会议纪要、流程说明、系统/数据材料或足够业务描述 | `scheme_mode` | 本体建模方案 |
| 有既有本体建模方案，要求基于业务反馈、Verifier findings、BKN 构建、数据绑定、Action / Skill 实现、测试、Trace / Eval 或运行证据优化 | `refine_mode` | 修订版方案、针对性修订建议或交付归档版方案 |
| 要求对比 PRD 与本体建模方案 | `compare_mode` | 差异、缺口、补强建议 |

如果用户说“给 `BKN_Creator` 参考”，仍使用 `scheme_mode` 或 `refine_mode` 输出/修订方案 Markdown，不另设独立 handoff 输出模式。

`refine_mode` 必须识别修订依据：

| 子类型 | 触发 | 处理重点 |
|---|---|---|
| `business_feedback_refine` | 业务评审意见、新会议纪要、补充材料、PRD 迭代 | 修订对象、关系、场景路径、确认状态和待确认问题 |
| `verifier_refine` | Verifier findings 指出 hard stop、major 或 minor | 按 findings 定向修订，不重新发散生成 |
| `implementation_feedback_refine` | BKN 构建、`.bkn`、数据绑定、Action / Skill 实现、测试、Trace / Eval 或运行审计反向暴露建模问题 | 回填对象边界、关系方向、Action 边界、Skill 契约、治理和证据链变化 |

`implementation_feedback_refine` 说明本体建模方案是项目交付物之一，会随实现、验证和运行证据持续提炼；但本 Skill 仍只修订方案，不生成 `.bkn`、不绑定数据、不推送平台。

## 项目目录与输入归档

与 `bkn-requirement` 共享项目文件夹规则，默认项目目录为：

```text
projects/prj-<客户或项目简称>/
```

每轮输入材料应归档或登记到：

```text
projects/prj-<客户或项目简称>/inputs/round-XX/source-manifest.md
```

规则：

1. 外部输入文件先复制到本轮 `inputs/round-XX/`，再登记。
2. 项目目录内已有 PRD、验证输出、handoff 或建模方案只登记路径和版本，不重复复制。
3. 标记为已复制的文件必须校验归档路径真实存在。
4. 复制失败、权限不足或路径无法访问时，不得伪造归档状态；方案开头必须说明“输入归档未完成”及影响。
5. 本体建模方案开头必须列出“本轮输入来源”，说明使用了哪些原始材料、需求发现产物、未归档材料，以及本方案是初版、基于 PRD 生成还是基于上一版修订。

若用户只提供项目目录，自动识别最新材料：

1. 最高版本的 `<项目名>-本体建模方案 vX.Y.md`；
2. 最高版本的 `<项目名>-PRD vX.Y.md`；
3. 最新需求发现验证输出、`BKN_Creator` 交接摘要或 PRD 末尾交接内容；
4. 最新会议纪要、调研大纲和本轮 `inputs/round-XX/` 材料；
5. 数据字典、字段说明、样例数据和系统材料。

只有存在多个同等可信输入且会影响输出时，才要求用户确认。

## 主流程

正式本体建模方案必须执行 Agentic Harness：

```text
Archive / Context
→ Generator
→ Verifier
→ Reviser（如有必要）
→ Final Gate
→ Final Output
```

### Archive / Context

- 识别输入材料类型、版本、路径和用途；
- 归档或登记输入，并校验 manifest；
- 区分已确认业务事实、材料假设、建模候选、冲突信息和缺失信息；
- 抽取业务目标、用户角色、P0/P1 场景、关键决策、输入、输出、验收问题、数据来源、协同边界和治理风险。

### Generator

生成候选建模方案，不直接声明最终通过。必须从业务目标和场景开始，按“业务目标 → 被管理和判断的业务对象 → 稳定业务关系 → 事实/属性/指标 → 逻辑/Skill 候选 → 有副作用行动 → 运行状态和审计 → 治理边界 → 证据路径”推导。

方案结构和写法见 `assets/ontology-scheme-template.md` 与 `references/ontology-builder-method.md`。

### Verifier

独立检查候选方案，不直接改文档。至少检查：

- 是否从业务目标和场景开始，而不是从源表、字段、页面、报表或接口开始；
- 输入是否归档或登记，引用是否标明版本和路径；
- 对象是否避免源表、报表行、临时结果、角色名、规则和提示词逻辑的误对象化；
- 核心对象、关系、Skill、Action 和治理边界是否说明业务定义、建模原因、边界、风险和确认状态；
- 稳定事实与运行状态是否分离；
- 指标、算子、解释逻辑、Skill、Agent 和 Action 边界是否清楚；
- 是否覆盖对象生命周期、工作流、状态推进、任务队列、行动触发、异常处理和反馈闭环；
- 工作空间、协同、私有视角、TraceAI / Eval 对接是否只在材料支持时出现；
- 已确认内容、建模候选、待业务确认、待下游判定是否分开；
- 是否错误声称本方案是 `BKN_Creator` 门禁或 `.bkn` 草案。

Verifier findings 分为 `hard_stop`、`major`、`minor`。`hard_stop` 必须修订，`major` 原则上修订，`minor` 可修订或在最终摘要说明。

若本轮在项目目录落盘候选方案，必须同步落盘独立的 `*-verifier-findings.md`。Verifier findings 不应只内嵌在主方案正文里。

### Reviser

只根据 Verifier findings 定向修订：

- 先修 `hard_stop`，再修 `major`；
- 不删除已确认业务事实，除非确认状态错误；
- 不把候选项改写成已确认内容；
- 不把方案改写成 `.bkn`、schema 或平台执行说明；
- 修订后必须再次执行 Verifier；
- 自动修订最多 2 轮，超过后停止并输出剩余问题和下一步建议。

### Final Gate

Final Gate 只判断方案质量，不决定项目是否可以进入 `BKN_Creator`。

| 状态 | 条件 | 输出 |
|---|---|---|
| `pass` | 无 hard stop，major 已处理或可解释 | 正式本体建模方案 |
| `warn` | 无 hard stop，但仍有关键待确认 | Candidate 方案，附待确认问题和下一步 |
| `fail` | hard stop 未清除 | 不声明方案可评审，输出未通过原因和补充材料清单 |

若本轮在项目目录落盘方案，必须同步落盘独立的 `*-final-gate.md`，记录 gate 状态、依据、剩余风险和下一步。

### Harness 产物边界

正式 `scheme_mode` 或 `refine_mode` 落盘时，使用以下产物边界：

| Harness 环节 | 标准产物 | 命名建议 | 说明 |
|---|---|---|---|
| Archive / Context | `source-manifest.md` | `inputs/round-XX/source-manifest.md` | 输入归档或登记，不重复复制项目内文件 |
| Generator | 候选方案 | `<项目名>-本体建模方案 vX.Y-candidate.md` | 候选输出，不声明最终通过 |
| Verifier | 独立 findings | `<项目名>-本体建模方案 vX.Y-verifier-findings.md` | 只检查，不直接改方案 |
| Reviser | 修订版候选方案 | `<项目名>-本体建模方案 vX.Y-revised-candidate.md` | 仅在需要修订时产生 |
| Final Gate | Gate 结论 | `<项目名>-本体建模方案 vX.Y-final-gate.md` | 只判断方案质量，不决定是否进入 BKN_Creator |
| Final Output | 最终方案 | `<项目名>-本体建模方案 vX.Y.md` 或 `<项目名>-本体建模方案 vX.Y-candidate.md` | `warn` 时保持 Candidate 标识 |

开发测试时可额外输出 `*-harness-run-report.md` 汇总一次样例运行，但它不是业务交付物，也不是 Verifier、Reviser 或 Final Gate 的替代品。

实现反馈修订可额外输出 `<项目名>-本体建模方案 vX.Y-实现反馈修订说明.md`。若用于项目交付归档，可输出 `<项目名>-本体建模方案 vX.Y-交付归档版.md`，但必须区分业务评审口径、实现验证结果、工程 workaround 和待业务复核项。

## 必要章节

默认输出 `《<项目或场景> 本体建模方案》`，建议章节：

1. 建模目标
2. 业务目标到本体承接方式
3. 本体设计思想
4. 总体分层
5. 业务对象设计
6. 关系设计
7. 指标 / 算子 / 解释逻辑建模
8. 业务运行层设计
9. Action / 行动建模
10. Skill / Agent 应用契约
11. 场景到本体路径映射
12. 业务证据链与可解释性设计
13. 协同 / 工作空间 / 私有视角边界（按需）
14. 模型治理原则
15. 跨场景或跨行业扩展方法（按需）
16. 最终本体蓝图
17. 方案边界与后续增强

第 7、8、9、10、12、13、15 节必须按材料裁剪。不适用时说明原因，不能强行套模板。

## 何时读取参考材料

- 生成或修订完整方案时，读取 `references/ontology-builder-method.md` 和 `assets/ontology-scheme-template.md`。
- 处理 BKN 构建、绑定、Action / Skill、测试、Trace / Eval 反向修订时，读取 `references/ontology-builder-method.md` 的 `implementation_feedback_refine` 协议，并使用 `assets/implementation-feedback-refine-template.md`。
- 需要落盘独立 Verifier 或 Final Gate 产物时，使用 `assets/verifier-findings-template.md` 和 `assets/final-gate-template.md`。
- 涉及 BKN 对象、关系、指标、算子、Action、治理或 Skill / Agent 边界时，读取 `references/bkn-methodology.md`。
- 涉及复杂协同、共享 Base、私有判断、运行状态与事件审计分离时，读取 `references/complex-ontology-patterns.md`。

## 最终自检

输出前确认：

- 本轮输入来源已列明；
- 方案从业务目标和场景开始；
- 核心对象、关系、逻辑、Action、Skill 和治理边界都有设计理由；
- 稳定事实与运行状态分离；
- 查询、计算、解释不直接误建为 Action；
- 有副作用操作才建模为 Action；
- 业务运行层说明生命周期、状态机、工作队列、人工确认、行动记录和反馈闭环；
- 关键判断能追溯到对象、关系、来源、规则、人工确认和行动结果；
- 确认状态严格隔离；
- `refine_mode` 已说明修订依据属于业务反馈、Verifier findings 还是实现反馈；
- 实现反馈修订已区分业务事实、实现验证结果、工程 workaround、待业务复核和待下游平台判定；
- 已执行 Generator、Verifier、必要 Reviser 和 Final Gate；
- 未把方案声明为 `.bkn`、平台执行结果或 `BKN_Creator` 强制门禁。
