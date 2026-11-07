---
name: dreamina-video-production
description: Use when creating a complete Dreamina video project from a local reference video, including analysis, redesign or authorized replication, batch generation, evaluation, audio, subtitles, composition, recovery, and verified export.
license: Complete terms in LICENSE
---

# Dreamina Video Production

Orchestrate one reference video into one verified final MP4. Every step below is
a separate Dreamina tool call; the project ledger is the only source of truth
for what has already happened.

## Example request

```text
Use dreamina-video-production with /approved/input.mp4 in original-redesign mode.
Show the complete storyboard, task count, model specifications, and maximum credit
ceiling before requesting one whole-batch approval. Do not submit paid work yet.
```

## 能力边界说明

### ✅ 能做

- Create and resume a private, versioned video project.
- Analyze a local reference video into shots, frames, contact sheets, and a typed recut.
- Plan exact Dreamina requests, quote the whole batch, and activate one non-expandable allowance.
- Execute, evaluate, compose, verify, and export the result with a comparison report.

### ⚠ 需要素材

- A local reference video inside an approved root.
- Enrolled trusted media tools (`ffmpeg`, `ffprobe`, and optionally `whisper` and a narration provider).
- Native confirmation for enrollment, rights, whole-batch approval, and export.

### ❌ 超出范围

- Do not call `ffmpeg`, `ffprobe`, or any local binary directly. Only the project tools may.
- Do not assert rights on the user's behalf. Only the user's literal assertion is recorded.
- Do not resubmit a paid request. `Submitted`, `Querying`, and `Unknown` are query-only.
- Do not treat a Jimeng Web link as Seedance completion.

## Workflow

1. **Read status first.** Call `dreamina_video_project` with `action=runtime_status`,
   then `action=get` for an existing project. Never guess the current state.
2. **Enroll tools when required.** `action=enroll_media_tools` is a native-gated side
   effect. It binds each executable by absolute path, owner, and digest.
3. **Seed and analyze.** `dreamina_analyze_reference_video` with `action=seed` copies the
   source under containment; `frames`, `sheets`, and `recut` derive versions from it.
4. **Annotate via the specialist.** Hand contact sheets to
   `dreamina-shot-annotator`. Persist only through
   `dreamina_validate_shot_analysis`, which refuses a stale machine fingerprint.
5. **Design.** `dreamina_create_redesign`. `original_redesign` replaces expressive
   content; `authorized_replication` additionally requires a complete, unexpired,
   scope-matching rights assertion.
6. **Quote, then approve.** `dreamina_quote_video_batch` returns the exact request
   fingerprints and the total credit ceiling. `dreamina_approve_video_batch` activates
   one whole-batch allowance after native confirmation. An activated batch can only
   reduce work.
7. **Execute.** `dreamina_execute_video_batch` with `run_next`, `reconcile`, or `resume`.
   `reconcile` never submits.
8. **Evaluate via the specialist.** Measure first, then hand the measurement to
   `dreamina-video-evaluator`. The same semantic payload must never serve as both
   the design intent and the acceptance verdict.
9. **Compose, verify, export.** `dreamina_compose_video`, then
   `dreamina_export_video_project`, which verifies every required gate before it
   touches the destination.

## Gate signals

- `PreviewValidated` / analysis version: local, deterministic evidence.
- `JimengLinkReady`: a web handoff finished. Never Seedance completion.
- `Submitted` / `Querying` / `Unknown`: paid, query-only.
- `Completed`: only after a downloaded artifact was independently re-hashed.

## Never do

- Never skip the status read before a transition.
- Never let one semantic payload serve as both design and acceptance verdict.
- Never claim a skipped gate passed.

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when creating a complete Dreamina video project from a local reference video, including analysis, redesign or authorized replication, batch generation, evaluation, audio, subtitles, composition, recovery, and verified export.。

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

校验输入、模型/工具能力、输出路径、预算上限和审批状态；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按一次批准执行并记录请求标识；模糊结果先查询而不是重提；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

验证产物存在性、格式、哈希/标识、成本状态和质量门禁，并把事实、推断和未验证项分开陈述。

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

付费、发布、覆盖、上传或外部写入必须使用当前任务的显式授权；不自动扩大次数和预算。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
