---
name: dreamina-3d-from-blender
description: Use when the user has a Blender scene and wants a Seedance 2.5 render from it. Drives the preview through the validated Dreamina 3D pipeline.
license: Complete terms in LICENSE
metadata:
  type: workflow
  plugin: dreamina-3d
  source_dcc: blender-design
  status: stable
---

# dreamina-3d-from-blender

## When to use

The user wants a Dreamina 3D render from a Blender scene. Companion
`blender-design` is already installed.

## Workflow

### Automatic run policy

When the user provides one `auto_with_budget` envelope — approved reference
upload, model/resolution/duration preferences, a maximum charge, and
permission for one remote submission — perform the following workflow without
asking at every state transition. Resolve capability, validate the preview,
obtain and compare the quote, submit once only when it is within the cap,
query the recorded identifier, download, and independently verify the final
artifact. Return one final artifact inventory.

Stop and ask only when the quote exceeds the cap, a required reference was
not authorized for upload, a platform-mandated confirmation or web
prerequisite is pending, validation fails, or recovery would require another
paid submission. `interactive` retains the review at each gate; `review_only`
does not upload or submit.

Because Dreamina Design currently exposes no authoritative quote tool,
`auto_with_budget` stops at `QUOTE_UNAVAILABLE`. The user may instead approve
one fully specified `auto_exact_request`; that grants one submission only and
does not bypass the native paid-action approval in Dreamina Design.

1. **Inspect.** Call `inspect_scene(executable=blender_adapter,
   scene=<user_scene>)`. Reject if the scene cannot be inspected.
2. **Specify preview.** Collect user-approved camera, frame range, output
   path, and dimensions. Build a `PreviewSpec`.
3. **Export.** Call `request_preview_export(...)` with the user's prompt
   metadata embedded in the request payload. Independent re-hash is
   performed by the orchestrator — never trust the producer's declared
   sha256 alone.
4. **Validate.** Run `validate_artifact(receipt, current_file)` from
   `scripts/handoff_validator.py`. On any error, transition the job to
   `Failed` with the classified `error_category`.
   调用方若需限定生产者版本，可传 `version_ranges={"blender-design": [("1.0.0", "1.9.9")]}`；
   显式映射替换默认范围，`{}` 拒绝全部生产者，`None` 保留默认范围。
   版本通过仍必须完成路径、字节数、摘要与其余元数据校验。
5. **Resolve readiness.** Use `McpDesignClient` to call
   `dreamina_cli_status` and `dreamina_account`. On user action required, stop
   with the returned remediation.
6. **Bind request.** Build `QuoteInputs(prompt, model, resolution, ratio,
   duration)` and the validated preview reference. Record that an authoritative
   quote is unavailable; never synthesize one.
7. **Authorize.** Require `auto_exact_request` (or a future authoritative
   quote within `auto_with_budget`) plus reference-upload and one-submit flags.
8. **Submit.** Let `McpDesignClient` call `dreamina_submit_video`; Dreamina
   Design obtains native approval internally. Persist `submit_id` before
   reporting `Submitted`.
9. **Query.** Let `McpDesignClient` call `dreamina_query_task` for the stored
   identifier and approved download root. `Unknown` is query-only.
10. **Download + verify.** Re-hash the downloaded artifact and compare to
    the declared hash; reject on mismatch.

## Ledger transitions

Drive the job through `Draft → DccSelected → PreviewSpecified →
PreviewValidated → CapabilityResolved → Quoted → Approved → Submitted →
Querying → Completed | Failed | Unknown` exactly once each.

## Never do

- Never resubmit a job whose `design_submit_id` is already set.
- Never skip the preview validation gate.
- Never send DCC scene data to the design plugin — only the validated
  artifact reference (artifact_id + sha256), the user prompt, and the
  quote inputs.
- Never use the consumer plugin's internal `design_handoff.py` fixture for a
  production route. It is not shipped by this granular skill and exists only
  as a deterministic compatibility harness in the plugin test suite.

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user has a Blender scene and wants a Seedance 2.5 render from it. Drives the preview through the validated Dreamina 3D pipeline.。

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
