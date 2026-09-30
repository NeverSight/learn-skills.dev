---
name: implement
description: "按已确认的 issue / spec 实施。Leaf 自动实现并交给独立 reviewer；Parent 自动编排子 issue DAG、独立 review 每个子票并做最终 integration review。Controller 独占 workflow state。"
disable-model-invocation: true
---

# Implement

实现用户指定的 issue / spec，不把实施阶段变成重新设计需求的机会。默认用中文报告，保留项目已有技术标识符。

> **Controller 管状态，Implementer 写代码，Reviewer 独立验收。** 每份实现都由没有参与该实现的独立 reviewer agent 审查；只有 Controller 可以改变 issue workflow state。

## 1. 读取目标并自动选择模式

读取项目 `AGENTS.md` / `CLAUDE.md`、相关 glossary / ADR、目标 issue / spec 全文及评论，以及项目 tracker 配置（项目说明指向的文件，其次 `docs/agents/issue-tracker.md`）。读取 issue、列子票、读 blocker、推进状态和关闭都按该配置中的操作执行；配置只有自然语言描述、缺少具体命令时（例如旧版 setup 生成的配置），按其描述用对应 provider 的标准工具执行，并建议重跑 `/setup` 补齐；不因此阻塞。目标在远程 tracker 上但找不到配置时，不写任何状态，提示先运行 `/setup`；不要自行猜 repo 或状态机。

读取 `Proposed Changes`（旧 spec 没有也正常）、完整验收条件、父子关系和真实 blockers，然后自动选择：

- **Leaf mode**：目标没有需要编排的 child issues，直接实现当前目标。
- **Parent mode**：目标有 child issues，读取 [orchestration.md](references/orchestration.md)，当前 session 作为 Controller，用当前 harness 的 sub-agent 完成整组编排，无需用户额外开启。

已有 issue graph 是已确认的执行计划：默认**不重新拆票、不重排需求、不自行新增产品决策**。
发现 blocker 错误、子票无法独立完成、spec 与代码事实冲突，或必须改变 external contract 时，暂停受影响分支并向用户说明。

## 2. Workflow state 的唯一 owner

当前 `/implement <target>` session 是 **Controller**，也是目标及本次编排范围内 child issues 唯一的 workflow-state writer。状态、labels、终态和完成条件都来自 tracker 配置，不由本 skill 发明；没有中间状态时只在内部记录进度。

- Implementer 只返回实现事实、commit 和验证结果；Reviewer 只返回 verdict 和 findings。两者都不 close issue、不改状态、不解除 blocker。
- 一个 issue 只有在独立 review 通过、要求的 verification 通过、交付内容与审查内容一致后，才推进到完成状态。
- 每次写 tracker 前重读该对象及其依赖 / 状态，只提交本次必要的最小变更，写后读回核对。人工改动使计划或状态转换失效时，暂停受影响分支并说明，不用旧快照覆盖；写入失败时如实报告，不假报推进成功。

用户要求“不改 tracker / 不关 issue”时照做，review gate 不变，并报告本来会执行的状态转换。

## 3. Leaf mode

主 session 同时是 Controller 和 Implementer；**Reviewer 必须是独立 sub-agent**。

1. 确认 blockers 已满足；记录起点 commit、当前分支和已有的未提交修改。
2. 配置有对应状态时，标记 in-progress。
3. 按第 4 节实现，持续运行相关测试 / typecheck。
4. 配置有对应状态时标记 in-review；读取 [review.md](references/review.md)，启动未参与实现的独立 Reviewer。
5. 任一轴不通过：修复后交给独立 Reviewer 复审。
6. 两轴通过后运行最终 verification，把本次目标范围的修改提交到当前分支并记录 commit。提交失败不能宣告已交付；commit hook 改变内容时，补做受影响的 review 与验证。
7. 按 tracker 配置推进完成状态。

用户明确要求“不提交”时保留未提交修改并如实报告；若完成条件要求 commit，则不推进终态。
当前 harness 无法启动独立 reviewer agent 时，可以完成实现和测试，但报告“等待独立 review”，不推进完成状态。

## 4. 实现纪律

本节同时约束 Parent mode 中的 Implementer sub-agent。

选择最小充分实现：

- 先读相关代码、真实调用链和约束，再判断是否需要新增代码；不能用小 diff 代替理解问题。
- 先复用项目已有实现，再看标准库、平台原生能力和已安装依赖；检查围绕当前任务，不扩展成全库审计。
- 确实存在缺口才新增代码或依赖。新增通用层、工厂、配置项或扩展点要有当前用例或明确约束支撑；单一实现本身不是删除已有接口的理由，已有隔离边界、测试 seam 和项目约定仍可能需要它。
- 以完整满足契约为前提减少维护负担，不追求最少行数；不牺牲可读性、信任边界校验、安全、可访问性、防数据丢失处理和必要验证。
- 验收满足且 review / verification 通过后停止扩展，不顺手重构相邻模块。

测试：

- 写测试前读取 [tdd.md](references/tdd.md)，能 TDD 时按垂直切片：`一条行为测试 → 因目标行为缺失而失败 → 最小实现使其通过 → 下一条`。修 bug 先写能复现问题的 regression test。
- 覆盖关键成功、失败、兼容 / migration 和异步状态路径，不要求穷举边界。纯文档、配置或无法合理 TDD 的工作用静态检查 / smoke test，并说明验证限制。
- 持续运行小范围测试与 typecheck，完成前运行项目要求的完整检查。没实际运行的检查不能记为通过。

涉及模块 / interface 设计、依赖组织、测试 seam 或重构时，读取并应用 [codebase-design.md](references/codebase-design.md)，不改变已确认 spec。

## 5. External contract 不得偷偷改变

保持已确认的 API、CLI、UI、config/env、输入输出、错误、默认值、完成语义、旧数据与 migration 承诺。
实现必须改变这些 contract 时，不让 Implementer 自行拍板。Controller 暂停受影响分支，说明原 contract、为什么不可行、proposed change 和 compatibility / migration 影响；取得用户确认并更新 spec 后再继续。

未经单独授权不访问生产凭据、真实账户，不下实盘订单，不运行破坏性迁移或生产发布。

## 6. Git 与交接

保护开始前已有的用户修改，不把无关工作纳入 commit。多个 sub-agent 不同时写同一个 working tree。

`/implement` 授权本次目标范围内的本地 commit 和必要的 issue workflow transitions，但**不自动授权** push、merge PR、production deploy / migration、修改目标图之外的 issue，或改写已确认 spec。

最终报告：

- 完成 / 未完成的 issues；
- 每份 review 与 parent integration review 的结果；
- external contract / compatibility 的实际变化；
- verification 证据；
- commits 与集成分支；
- 任何未解决或未验证事项。
