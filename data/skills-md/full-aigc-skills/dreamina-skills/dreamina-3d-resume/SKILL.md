---
name: dreamina-3d-resume
description: Use when the user wants to continue an in-flight Dreamina 3D job without re-paying or re-exporting. Resumes the job from its ledger state.
license: Complete terms in LICENSE
metadata:
  type: workflow
  plugin: dreamina-3d
  status: stable
---

# dreamina-3d-resume

## When to use

The user references an existing job id and wants to continue without
restarting local export or remote submission. The job ledger is the
single source of truth for what has already happened.

Use `McpDesignClient` for all Dreamina Design operations. Resume may call only
the typed status, account, submit, and query mappings; after a stored
`design_submit_id` exists it may call only the query mapping.

## Workflow

For a persisted `auto_with_budget` job, automatically resume only the safe
next state: capability/quote work before a submission, or query/download work
after its stored submit identifier. Never convert a budget stop, missing web
prerequisite, failed validation, `Unknown`, or failed job into a new paid
submission without a new user instruction.

1. **Load.** `JobLedger.read()` on the user's job file. If the file does
   not exist, stop and ask the user to specify a valid `job_id`.
2. **Map state → next action.**

   | Current state       | Next action                                                                 |
   |---------------------|------------------------------------------------------------------------------|
   | `Draft`             | ask the user to choose a companion DCC                                        |
   | `DccSelected`       | resume from the PreviewSpecified step                                         |
   | `PreviewSpecified`  | re-validate the existing preview receipt; on mismatch re-export              |
   | `PreviewValidated`  | resume capability resolution                                                  |
   | `CapabilityResolved`| resume quote (do not reuse a quote for inputs that have changed)              |
   | `Quoted`            | ask the user to confirm or reject the quote                                   |
   | `Approved`          | check `submit.design_submit_id` — if present, only query, never resubmit      |
   | `Submitted`         | only query the design plugin; never re-export or re-submit                   |
   | `Querying`          | continue polling                                                             |
   | `Completed`         | verify the on-disk artifact hash; if missing, transition to Failed           |
   | `Failed` / `Unknown`| ask the user to authorise a recovery action (re-quote / re-query / restart)  |

3. **Never repeat completed work.**
   - A `Completed` job must never be re-submitted or re-exported.
   - A `Submitted`/`Querying`/`Unknown` job must never be re-exported.
   - Only `Draft`, `DccSelected`, and `PreviewSpecified` may re-invoke the
     DCC adapter, and only if the on-disk artifact hash no longer matches.

## Never do

- Never auto-resubmit a paid action.
- Never silently rewrite history; append to the job ledger instead.
- Never invent a `design_submit_id`; the design plugin is the only source.

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **从已记录状态恢复中断任务，避免重复提交或重复计费** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user wants to continue an in-flight Dreamina 3D job without re-paying or re-exporting. Resumes the job from its ledger state.。

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

核对任务标识、最后成功阶段、远端状态、预算和授权范围；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

仅继续尚未完成且可证明安全的阶段；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

返回复用结果、新执行步骤、未恢复项和下一人工决策点，并把事实、推断和未验证项分开陈述。

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

没有幂等键、远端状态或用户授权时不重提任务；恢复不扩大原批准范围。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
