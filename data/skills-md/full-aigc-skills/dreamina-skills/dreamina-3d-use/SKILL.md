---
name: dreamina-3d-use
description: Use when the user wants to turn a DCC preview into a Dreamina render without naming the source DCC. Routes the request to the right workflow.
license: Complete terms in LICENSE
metadata:
  type: router
  plugin: dreamina-3d
  status: stable
---

# dreamina-3d-use

## When to use

The user wants a Dreamina 3D render but has not specified whether the source
preview comes from Blender or Maya. This Skill routes to the right workflow.

## Three explicit entries

- `preview_only`: produce and validate a local Blender/Maya preview, then stop
  at `PreviewValidated` without web handoff or paid submission.
- `jimeng_web`: delegate to `dreamina-3d-jimeng-web` and stop at
  `JimengLinkReady`. A ready link is not a submitted or Completed Seedance
  artifact.
- `auto_seedance`: delegate to `dreamina-3d-auto-seedance`; require
  approval, submit once, query the same ID, download, and verify before
  `Completed`.

If the user's intent does not distinguish these outcomes, explain them and ask
for one choice. Never silently upgrade a local preview into a web or paid
operation.

## Report availability honestly

State each entry's availability before the user chooses. Do not imply a
capability is production-ready when it is not:

- `preview_only` and `auto_seedance` are production routes on macOS + Blender.
- `jimeng_web` is `OPTIONAL_UNAVAILABLE` whenever the user-installed official
  uploader is absent. Report it as optional and unavailable, never as verified.
  Probe for it; never install or enable it to make the route available.
- `dreamina-3d-from-maya` is **experimental** with runtime status
  `NOT_RUN`. It is fixture-compatible only and is not part of the production
  release. Do not present Maya as production-ready, and do not route a user
  there without saying so.

## Workflow

1. **Discover companions.** Call `discover_companions(search_roots)` from
   `scripts/capability_probe.py`. Do not crawl user directories and do not
   install anything.
2. **Choose the companion.** Call `select_companion(candidates, requested=None)`.
   - zero companions: surface `install_guidance()` and stop.
   - one companion: route to `dreamina-3d-from-blender`, or to
     `dreamina-3d-from-maya` only after flagging it experimental.
   - two companions: ask the user to pick.
3. **Select entry.** Report availability per the section above, then apply the
   explicit route.
4. **Delegate** to the selected bounded Skill and stop.

## Never do

- Never install or modify a companion plugin.
- Never skip the companion detection step.
- Never proceed to Dreamina submission before the preview is validated.
- Never report `jimeng_web` as production-verified while the official add-on is
  absent.
- Never treat `JimengLinkReady` as `Completed`.
- Never present the Maya route as part of the production release.

## Gate signals

- Local preview status: `PreviewValidated` in the job ledger.
- Dreamina submission status: `Submitted | Querying | Unknown` in the ledger.
- Final artifact acceptance: `Completed` (only after `result.sha256` is on
  disk and matches the declared hash).
- Web handoff status: `JimengLinkReady`, or `OPTIONAL_UNAVAILABLE` when the
  official add-on is absent. Neither is Seedance completion.

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user wants to turn a DCC preview into a Dreamina render without naming the source DCC. Routes the request to the right workflow.。

## Rules

- 先读后写：先确认当前状态与真实能力，再执行会改变外部状态的动作。
- 权限最小化：只使用完成当前步骤所需的文件、工具、账户与网络范围。
- 证据优先：运行结果、资源 ID、版本、哈希或测试输出缺失时，明确标记为 `NOT_VERIFIED`。
- 幂等优先：保留请求标识与阶段状态；结果不明确时先查询，不进行盲目重试。
- 隐私安全：日志、示例、回执和错误信息不得包含 token、cookie、密钥或个人敏感数据。

## Workflow

### Step 1：澄清意图

确认本技能是否匹配目标；若只是相邻需求，交给更精确的技能。
### Step 2：执行预检

确认目标、输入、约束、可用工具、成功标准和失败边界；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按最小充分步骤执行，并在关键状态变化处记录证据；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

输出结果、验证证据、未完成项、风险和明确的下一步，并把事实、推断和未验证项分开陈述。

## Validation checklist

- [ ] 技能触发条件与用户意图一致，没有把相邻任务误路由到本技能。
- [ ] 输入、目标对象、版本和输出位置均已明确，且没有使用猜测值替代必填值。
- [ ] 所有写入、付费、发布或不可逆动作都在用户授权范围内。
- [ ] 结果已用独立检查验证；仅有“命令成功”或“文件存在”不算完整验收。
- [ ] 输出包含实际证据、失败/跳过项、剩余风险和可执行的下一步。

## Gotchas

1. **把计划当结果**：文档或提示词不等于真实执行；必须标明实际运行层级。
2. **错误重试**：超时或响应丢失可能已经产生远端状态，先查询再决定是否重试。
3. **隐式扩大范围**：批量、全量、发布、覆盖和付费不是普通读写的自然延伸。
4. **版本漂移**：引用外部资源时记录版本、tag 或提交；不要把可变分支当发布证据。
5. **证据过期**：缓存、旧截图和历史测试不能证明当前环境；在交付前刷新关键证据。

## 不适用与边界

不超出用户给定范围；写入、付费、发布和不可逆动作需要明确授权。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
