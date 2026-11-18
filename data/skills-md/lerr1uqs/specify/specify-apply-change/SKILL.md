---
name: specify-apply-change
description: 实施 Specify proposed change 中的 tasks，并在开始实施前核对 Contract 基线。适用于用户要求开始或继续实现一个已有 change 时。
---

# 实施 Specify change

根据用户给出的 ID 或上下文定位 `spec/changes/proposed/<kind>/<change-id>/`。若有多个可能目标且无法判断，先列出候选 change 并请用户选择。读取 `change.md`、`tasks.md`、`meta-data.yaml`、所有 delta 与相关 formal spec。命令默认作用于当前目录；在本仓库源码中可用 `uv run specify` 替代 `specify`。

**每次开始实施前**运行 `specify change verify <change-id>`。若报告 Contract 正文基线变化，先阅读最新 formal spec，重新审查 change 的目标和 delta，按新正文调整 delta，再显式运行 `specify change baseline <change-id>` 和 `specify change verify <change-id>`。不要只重捕 hash 来消除错误；必要时同步调整 tasks 和已经写好的实现。

校验通过后按 `tasks.md` 实施、验证，并在对应任务实际完成时将 `- [ ]` 改为 `- [x]`。用户中途要求修改方案时，先更新 change 文件和 delta，再继续实施。完成所有 tasks 后再次运行 `specify change verify <change-id>`，再执行 `specify change implement <change-id>`；该命令会检查任务完成状态并将目录移到 implemented。

报告已完成的工作、验证结果和 change 状态。正式 Contract 的更新交给 `specify change sync`，不要手工套用 delta。

## 选择 change 并了解进度

用户给出 ID 时直接定位；未给出时先从对话推断。`specify status` 默认提供 JSON，可读取 `changes` 中的 `id`、`kind`、`status`、`validation`、`tasks`。只有一个明确的 proposed change 时可直接使用；多个候选且上下文不足时，列出名称与进度，请用户选目标。开始时告知本次使用的 change ID 与路径。

先判断生命周期状态：

| 状态 | 处理 |
| --- | --- |
| `proposed` | 读取材料并实施未完成的 tasks |
| `implemented` | 核对是否已有未汇报的实现；同步和归档属于下一阶段 |
| `rejected`、`archived` | 不把它当作可实施草稿 |

Specify 没有 OpenSpec 的 schema、artifact graph 或 `instructions apply --json`。实际上下文来自 `change.md`、`tasks.md`、`meta-data.yaml`、delta、当前 formal spec，以及待改源码。先读这些文件，再判断具体任务。

## 开始前的状态分支

运行 `specify change verify <change-id>` 后：

- **通过且仍有未完成 tasks**：报告 `已完成/总数` 和下一项任务，开始实施。
- **通过且 tasks 已全部完成**：核对相应实现与验证证据。若尚未进入 implemented，运行 `specify change implement <change-id>`；否则交给同步归档阶段。
- **Contract 基线变化**：读取报错引用的最新 Contract，比较当前正文、delta 与变更意图。先改自己的 delta，必要时修正 tasks 或已写代码，然后显式运行 `change baseline` 和 verify。不要只刷新 hash。
- **文件或结构无效**：根据 CLI 报错修正材料；缺少决定性需求时说明具体问题并请求澄清。verify 通过前不继续新增实现。

对同一 spec 并行的多个 change，检查的是本 change 依赖的 Contract 正文。另一个 change 同步后，每次恢复本 change 都要再 verify；不能沿用上次通过的结果。

## 逐项执行

按 `tasks.md` 的顺序处理未勾选项。每项先定位需要修改的代码，完成对应实现和适当验证，再把该项从 `- [ ]` 改为 `- [x]`。完成一项就记录进度，然后继续下一项；验证失败或功能尚缺时保留未勾选。不要只为了显示进度而批量勾选。

实施中如果发现计划不成立，更新 `change.md`、delta 和 tasks，使它们重新一致，再运行 verify。用户要求改变范围时同样处理；需要新增或修改旧正文操作时，审查最新 Contract 后显式重捕基线。已成功 sync 的 delta 不在此阶段修改，后续语义变更另建 change。

## 结束与交接

全部 tasks 完成后，运行针对改动的验证和 `specify change verify <change-id>`，再执行 `specify change implement <change-id>`。CLI 会校验任务完成情况并把目录从 proposed 移到 implemented。报告本次完成的任务、验证结果、最终 `已完成/总数` 和新路径；下一步才是 sync 与 archive。

如果中途遇到阻碍，报告已完成项、剩余项、真实错误和可选的下一步，保留 proposed 状态。不要因为本次对话结束就把未完成任务标成完成。

## 进度表达示例

开始时可以简短报告：`正在实施 adjust-login-rule，tasks 2/5 已完成。先处理 2.1：补全错误凭据的拒绝路径。` 完成一项并验证后更新为 `3/5`，说明做了什么、运行了什么检查。不要把 CLI 的 `change status` 当作项目总览；项目列表使用 `specify status`。

全部完成时报告：change ID、`5/5` tasks、代码变更摘要、测试结果，以及 `change implement` 后的 implemented 状态。此时尚未更新 formal spec；提醒下一步 sync 和 archive 即可。

如果暂停，说明例如：`2.1 的预期错误码与当前 Contract 冲突；已完成 2/5，尚未修改该 task 的勾选。需要决定是修实现还是改 Contract。` 给出具体选择和受影响的文件，保留可继续工作的状态。用户回应后接着做，勿从头重复已完成任务。

## 执行边界

- `change verify` 是开始实施和恢复实施时的只读检查；`change baseline` 会改 metadata，只有审查并调整 delta 后才调用。
- `change implement` 只改变 change 生命周期，不会同步 formal spec。正式规范仍以 `spec/changes/.../deltas/` 为待应用内容。
- 有无正式 spec 影响都需要如实完成 tasks；`specImpact.kind: none` 只表示没有 Contract delta。
- 任务描述若与代码现实不符，应修订任务或解释阻碍，不为了按原文打勾而留下错误实现。
