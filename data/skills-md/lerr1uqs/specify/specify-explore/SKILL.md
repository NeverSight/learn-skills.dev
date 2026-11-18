---
name: specify-explore
description: 在 Specify 项目中探索需求、Contract 边界和 change 方案。适用于用户还在讨论做什么或如何划分 spec，尚未要求创建 change 或实施代码时。
---

# 探索 Specify 变更

先确认项目存在 `spec/config.yaml`，读取其中的 `specTypes`、`kinds` 和相关模板。根据讨论主题查看 `specify list --spec`、`specify show <type>:<id>`、相关 formal spec，以及现有 change 的 `change.md`、`meta-data.yaml` 和 delta。命令默认作用于当前目录；在本仓库源码中可用 `uv run specify` 替代 `specify`。

帮助用户弄清问题、受影响的 Contract、可观察结果和实现约束。区分“修改正式 Contract”和“仅修复实现”：后者可以使用不带 `--affect` 的 change。若多个 change 涉及同一 spec，重点检查它们实际操作的 Contract ID 与正文，而不是仅凭 spec 路径判定冲突。

讨论尚未定案时，概括已经确认的目标、待决定的问题和可行的下一步。用户要求落盘时，按其意图创建或修改 Specify 文件；仅探索时不要擅自创建 change 或修改 formal spec。

## 探索姿态

探索阶段没有必须走完的步骤，也不预设一定会创建 change。先理解问题，再追踪相关 Contract 和实现，依据证据比较方案。提问只针对会改变结论的缺口；能从仓库中查到的事实先自己查。适合用简短表格或图解释边界、依赖和影响范围，但不把讨论变成固定模板。

可以主动核查用户的前提：现有 Contract 是否已经覆盖目标？看似“加功能”的请求是否只是修复实现？某个方案会不会改变另一个 spec 的承诺？区分已存在的行为、计划中的行为和个人建议。

## 从项目取得上下文

先用 `specify list --spec` 查看 formal spec，必要时用 `specify show <type>:<spec-id>` 阅读完整正文。`specify list` 默认输出活跃 change 的 JSON；`specify status` 查看整个项目，两者都包含 change 的 `id`、`kind`、`status`、`tasks` 与 `affects`。人类终端需要表格时才加 `--human`。如果用户提到具体 change，读取它的 `change.md`、`tasks.md`、`meta-data.yaml` 与 delta，再看关联的代码。

若当前目录没有 `spec/config.yaml`，先从用户指定的路径找项目；没有 Specify 项目时仍可讨论问题，但不要假装已查过正式规范。`specify init` 是创建项目的操作，只有用户确实要初始化时才运行。

## 常见入口

**只有模糊想法**：帮助界定用户、触发条件、可观察结果和失败场景。可列出几种范围，指出各自会影响的 spec 或 Contract；有足够信息后再确定是否需要 change。

**已有明确问题**：阅读相关 formal spec 与源码，判断是实现违反现有 Contract、Contract 本身不完整，还是两者都需要调整。给出能被验证的判断依据。

**实施中卡住**：读取当前 change 的目标、delta 和未完成 tasks，追踪阻碍所在；讨论是否要调整 delta、拆分任务、补充验证或改变实现。若 Contract 已变化，提醒先 verify 并按最新正文调整自己的 delta。

**比较方案**：先列出真正影响选择的项目约束，再比较方案对 Contract、组件边界、实现成本和迁移路径的影响。给出有条件的建议，说明尚未验证的假设。

## 把结论放在哪里

| 结论类型 | Specify 中合适的位置 |
| --- | --- |
| change 的问题、目标和边界 | `spec/changes/.../change.md` |
| 实施和验证步骤 | `spec/changes/.../tasks.md` |
| 将来正式 Contract 的增删改名 | 对应 `deltas/<type>/<id>.md` |
| 正式生效的 Contract | `spec/specs/<type>/<id>/spec.md`，由 sync 更新 |
| 无正式 spec 影响的理由 | `meta-data.yaml` 的 `specImpact.reason` |

用户只是讨论时，先给出结论和待决问题；用户明确要求记录时，再写入相应 change 材料。不要为了“留痕”直接编辑正式 spec，也不要把探索笔记塞进不相干的文件。

## 结束方式

讨论可能得到一项明确 change，也可能只是排除错误方向。适时总结当前问题、已确认的约束、推荐路径和仍未解决的问题；若用户已决定实施，转向起草或实施流程继续完成，不强迫继续探索。没有实际写入时，不报告“已创建 proposal”。

## 对话示例

当用户说“登录太慢，要不要拆 auth-service”时，不直接创建 architecture change。先看 `component:auth-service` 的职责和相关 requirement，定位慢发生在认证、网络调用还是会话签发，再比较“优化现有组件”和“拆分组件”对现有 Contract 的影响。若性能指标没有定义，说明需要观察的指标与测量位置。

当用户说“两个 change 都改 user-auth，会不会冲突”时，分别查看各自 delta 的 Contract ID 和捕获的基线；同一 spec 内的不同 Contract 不必然冲突，同一 Contract 的先后同步则需要后者重新 verify。讨论结果可以是实施顺序、delta 调整或进一步测试，不必生成新 change。

当用户实施中发现需求与现有 Contract 相反时，指出具体 Contract 文本、现有 change 的 delta 和代码行为三者的关系。若需要写入结论，在该 change 的 `change.md`、delta 和 tasks 中保持一致；正式 spec 仍由 sync 更新。

回复可以采用“当前事实、可选方案、推荐理由、待决问题”的短结构；对已经明确的简单问题直接回答，不强求每次都输出完整报告。
