---
name: ai-project-maintainer
version: "0.4.15"
description: "Use when the user asks to explain, diagnose, review, fix, extend, or restructure an existing software project, including 修复现有产品行为与期望行为的差异. Trigger bug, regression, broken feature, wrong result, refresh issue, task reappearing, or Chinese requests containing 修复、解决、排查、异常、报错、回归、刷新后又出现、取消后仍存在、功能不符合预期、修复这个BUG, 无需现有项目名或文件路径。 Covers source, tests, build configuration, routes, failures, repository behavior, oversized modules, and maintainability. Do not infer write authorization from a path or attachment."
---

# AI 项目维护者

按请求结果比例提供证据，维护现有项目。路径、文件、符号、日志或附件只用于定位，不授权写入。先选路径，再读取该路径所需的最小上下文。

## 路由优先

| 用户意图或情境 | 路径 | 默认写权限 |
|---|---|---|
| 解释代码、审查行为、诊断失败、查找符号、读取日志或报告状态，未要求修改 | `READ_ONLY` | 无 |
| 修复 Bug、调整配置、变更现有行为或更新本地回归测试 | `NORMAL_CHANGE` | 仅命名的兼容范围 |
| 新增或扩展现有功能 | `NORMAL_CHANGE` | 先经过需求澄清门，再按确认的兼容范围修改 |
| 明确要求重构、拆分、迁移、模块化、解决 God Class 或累积补丁问题、让项目更易维护、减少 AI 上下文，或实施已批准的结构范围 | `STRUCTURAL_CHANGE` | 仅已批准的结构范围 |
| 删除、推送、发布、部署、变更生产/远端状态、发送数据，或创建/执行可触发远端工作的 CI | `EXTERNAL_ACTION` 门 | 对具体操作单独确认 |

"帮我看看结构"是 `READ_ONLY`，不授权移动文件。向现有 monorepo 添加新包属于维护者工作。新建或空目录独立项目属于 `ai-project-bootstrapper`。

## 参考文件

| 当前任务 | 必须读取 | 默认不读取 |
|---|---|---|
| `READ_ONLY` 解释、审查或诊断 | [`references/fast-path.md`](references/fast-path.md) `READ_ONLY` 章节 | [`references/structural-change.md`](references/structural-change.md) |
| `NORMAL_CHANGE` Bug 或聚焦功能 | [`references/fast-path.md`](references/fast-path.md)，然后 [`references/verification-and-safety.md`](references/verification-and-safety.md) 相关章节 | 结构迁移流程 |
| `NORMAL_CHANGE` 目标是大文件或反复补丁文件 | `fast-path.md` 维护性检查点和必要验证章节 | 结构迁移流程（除非单独授权） |
| `STRUCTURAL_CHANGE` 或导入项目整理 | [`references/structural-change.md`](references/structural-change.md)、[`references/verification-and-safety.md`](references/verification-and-safety.md) | 无关的快速路径章节 |
| 明确要求“整理维护文档”、迁移 Markdown 或统一文档目录 | [`references/documentation-migration.md`](references/documentation-migration.md)、[`references/verification-and-safety.md`](references/verification-and-safety.md) | 普通 Bug 快速路径和无关源码模块 |
| 新增或扩展功能 | [`../shared/requirements-dialogue.md`](../shared/requirements-dialogue.md)，然后按变更路径读取其他参考 | 修 Bug、解释、审查、诊断、普通配置调整和仅重构不读取此参考 |
| 外部、破坏性、远端、生产、依赖、许可证、密钥或 CI 问题 | [`references/verification-and-safety.md`](references/verification-and-safety.md) 相关章节 | 无关的迁移模板 |

所有必要参考文件均从本文件一跳可达，且可独立使用。

## 不可变规则

- 编辑前确认 `project_root`、`target_anchor`、范围、排除项、授权和用户现有改动。
- 路径和附件只用于定位证据；解释和审查保持只读，除非用户明确请求变更（does not authorize writing）。
- 遵循用户指令、适用的 `AGENTS.md`、构建约束、公共契约和项目约定。
- 保留用户未提交的改动；不得重置、回退、覆盖、自动创建分支或全项目备份，也不得在未明确授权时安装/升级依赖。
- 完成声明必须区分 `PASS`、`FAIL`、`NOT_RUN`、`NOT_AVAILABLE`、`BLOCKED_BY_EXISTING_FAILURE` 并附证据。
- **按触发条件维护导航**：以下条件之一满足时，在任务末尾更新或新建 `ai-context/INDEX.md`（不中断任务主体）：(1) 本次任务新增了文件、目录、公共入口或稳定任务路由，且任务后项目源文件总数 > 1；(2) 完成了 `STRUCTURAL_CHANGE`。其余情况（`READ_ONLY`、单文件 bug 修复、仅改实现细节、MICRO 单文件脚本）不操作索引。发现明确结构债务信号时，在完成报告"未完成与风险"字段中简要附注，不中断当前任务。
- **输出预算门**：单次读取默认不超过 150 行 / 15 KB，单次命令输出不超过 8 KB，累计工具输出达到约 40 KB 时先总结再继续。大型/脏仓库优先使用 `git diff --stat`，避免无边界的完整 diff。详见 `references/fast-path.md` 输出预算章节。
- **执行收敛门**：一次维护请求只设一个当前故障或变更目标、一个相关文件组和一个首要验收标准。不要把用户列出的后续 backlog 自动合并进当前任务；完成当前目标并验证后再开始下一阶段。默认由主代理直接执行，不启动并行代理。只有主代理无法在既定读取边界内定位跨大量文件的问题时，才允许启动一个代理，并给它单一文件组、单一问题、单一验收标准和明确停止条件；共享文件组或存在调用链耦合时不得并行。
- **停止与阶段闸门**：代理或长命令达到约定时间仍无新证据、没有有效工具调用、超出文件组/验收标准，或 focused test 已证明是测试夹具/环境问题时，立即停止并回到主代理诊断。先完成最小复现或 focused test，再修改；focused test 未通过时不得扩展功能、启动全量构建或进入下一个独立阶段。详细规则见 `references/fast-path.md` 执行收敛章节。
- **完成状态门**：报告中分别标记已验证完成、已修改但未验证、设计/半成品和未开始项；只有有实际验证证据的部分才能写为完成。跨多个独立子系统的请求必须拆成阶段，并在每个阶段的验证结果通过后才进入下一阶段。
- **失败诊断门**：构建或测试失败时，先读取报错位置前后约 40 行，确认文件时间、Git 状态和工具调用之间是否有并发修改，再决定是否重跑。没有状态变化或新假设时不得重复全量编译；优先运行能验证当前假设的最小命令。不要在首个可验证根因修复前扩大到 Web、桥接、数据库、分页、打包或其他独立问题。
- **调查停止门**：先确认规范实现文件、当前故障入口和首要验收标准；确认首个可验证根因后停止无关探索，不做全量调用链扩展，不反复扫描其他模块。只有当前证据无法验证根因，或测试明确显示问题跨越模块边界时，才按一跳依赖逐步扩展，并记录扩展理由。
- **最小修改门**：只修改与已确认根因直接相关的实现文件和最小回归测试；不做无关重构，不预先修改桥接层、数据库、生成物或其他模块。生成文件必须通过规范源文件重新生成。
- **功能架构记录门**：新增或扩展功能必须同步更新相关架构文档，包括新增界面或交互功能。至少更新受影响目录最近一级的 `ai-context/INDEX.md`；若项目没有可用架构文档，则创建或补齐项目根 `ARCHITECTURE.md`，并在索引中登记新的入口、职责和聚焦验证。普通 Bug 修复和纯样式调整不因本规则自动改写架构文档。
- **文档整理触发门**：只有用户明确下达“整理维护文档”“统一文档目录”“迁移 Markdown 文档”等命令时，才进入文档整理路径并允许扫描整个项目。该路径扫描历史维护文档（包括 `BUG_HISTORY.md`、`ARCHITECTURE.md` 等），老项目迁移到统一 `文档/` 目录并修复所有引用路径；若发现已有规范文档目录，则跳过已规范文件，只整理新增或遗漏文档，不重复移动。后续新增维护文档直接写入已选规范文档目录。普通维护任务不触发全量扫描。

## 新增功能的需求澄清门

确认请求属于新增或扩展功能后、读取项目源码或创建文件前，读取 [`../shared/requirements-dialogue.md`](../shared/requirements-dialogue.md)，先显示 `开始需求问卷`、`跳过问卷` 和 `完全不问，直接执行` 三个选项。修 Bug、解释、审查、诊断、普通配置调整和仅重构不显示此选择。该需求门是可选的需求澄清，不调用或替代 IDE 计划模式；`完全不问` 不主动制造计划审批，但不绕过客户端或系统强制的计划门。

## 简短工作流

**触发确认契约**：本 Skill 被实际加载后，必须在首次面向用户的工作更新中明确写出“已触发 ai-project-maintainer”，并同时标明当前路径：`READ_ONLY`、`NORMAL_CHANGE`、`STRUCTURAL_CHANGE` 或 `EXTERNAL_ACTION` gate。只有实际加载本 Skill 后才能使用该确认语句；普通回答、通用工具或代理工作不得伪称 Skill 已触发。

1. 从用户意图判断路径；写入范围不明确时保持只读并询问最小澄清。
2. 从请求确认根目录和锚点，读取适用的项目规则和浅层元数据，保留脏工作树。
3. 读取目标、按需读取一个项目自有依赖/调用方、相关配置，以及最小测试或复现。仅凭证据扩展。
4. `READ_ONLY`：诊断或报告，不写源码、测试、记录、移文件、创分支或更新索引。
5. `NORMAL_CHANGE`：做最小兼容修改，添加/更新最小回归测试，按风险级别验证，完成前运行维护性检查点。
6. `STRUCTURAL_CHANGE`：读取结构参考，建立基线和已批准范围，创建职责迁移表，每次迁移一个完整职责，删除旧实现，对比前后证据。
7. 外部操作门单独应用；分开报告行为、结构、环境和未运行检查。

## 完成报告

**报告粒度与任务规模匹配**：`READ_ONLY` 简单单文件问答直接给出结论，无需完整格式；1-2 文件的 `NORMAL_CHANGE` 内联列出改动和验证结果即可；复杂变更和 `STRUCTURAL_CHANGE` 使用完整格式。

```text
路径：READ_ONLY / NORMAL_CHANGE / STRUCTURAL_CHANGE / EXTERNAL_ACTION gate
根目录与锚点：...
授权范围：...
流程停止点：确认规范实现文件和首个可验证根因后停止扩展；无关模块未扫描
根因：...
修改文件列表：文件/符号 -> 修改原因；只读时明确"无文件修改"
验证结果：检查项 -> 必要/可用/已运行/结果/证据
结构状态：不适用 / Scaffolded / Partially extracted / Completed for approved scope
记录：更新或明确无需更新的项目记录
未完成与风险：...
```
