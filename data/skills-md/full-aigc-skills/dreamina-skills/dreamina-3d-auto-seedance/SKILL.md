---
name: dreamina-3d-auto-seedance
description: Use when the user wants a validated DCC preview turned into an approved Seedance video through Dreamina Design MCP. Covers submit-once recovery and verified download.
license: Complete terms in LICENSE
---

# Automatic Seedance Entry

Use when the user explicitly wants the validated Blender preview turned
into a final Seedance video automatically rather than opened in Jimeng Web.

## 能力边界说明

### ✅ 能做

- Validate the local preview receipt and current SHA-256.
- Discover live Dreamina capabilities/account readiness.
- Obtain action-time approval, submit once, query, download and verify.

### ⚠ 需要用户确认

- A paid request must have an exact model, resolution, duration and either an
  authoritative maximum-charge envelope or explicit `auto_exact_request`
  permission when Dreamina exposes no quote API.
- Dreamina authentication or Web compliance prerequisites may require user
  action.

### ❌ 超出范围

- Never send the `.blend` scene; send only the validated preview.
- Never resubmit after timeout or an unknown state.
- Never treat CLI exit zero or `querying` as Completed.

## Workflow

1. Require `PreviewValidated`; independently re-hash the local artifact.
2. Instantiate `McpDesignClient` over the host's MCP tool invoker. It may call
   only `dreamina_cli_status`, `dreamina_account`, `dreamina_submit_video`, and
   `dreamina_query_task`.
3. Build the exact `multimodal2video` request from live capability data.
4. Never invent a quote. If none is available, stop unless the exact request
   has `auto_exact_request` authorization; native paid-action approval still
   occurs inside `dreamina_submit_video`.
5. Call `dreamina_submit_video` once and persist its submit ID before reporting
   `Submitted`.
6. Call `dreamina_query_task` for the same ID until success, failure, or
   `Unknown`; unknown permits query-only recovery.
7. Download into the approved root, verify media metadata, bytes and SHA-256,
   then and only then transition to `Completed`.

## Privacy

Keep account identity, credentials, approval material and local absolute paths
out of the cross-plugin ledger. Persist non-secret hashes, submit IDs, states,
timestamps and error categories only.

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **为当前请求选择并执行可验证、可恢复的专业工作流** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user wants a validated DCC preview turned into an approved Seedance video through Dreamina Design MCP. Covers submit-once recovery and verified download.。

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
