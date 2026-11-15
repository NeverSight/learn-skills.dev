---
name: xapi-workers
description: Deploy, operate, and verify applications on xAPI-managed Cloudflare Workers for Platforms through the xAPI CLI. Use for Workers projects, preview/production deployment, KV, D1, R2, Durable Objects, Queues, Workflows, Containers, schedules, runtime logs, consumption queries, billing reconciliation, retention, recovery, and test-resource cleanup. Includes real resource acceptance and cost evidence; does not administer a Cloudflare account directly.
---

# xAPI Workers for Platforms

Use the `xapi` CLI (`xapi-to` is the same executable). Verify `xapi workers --help` before using it; an older published installation may lack these commands even when the repository already contains them. Stop and report the version mismatch instead of silently replacing managed deployment with Wrangler direct deployment. Wrangler `deploy --dry-run --outfile` is allowed only as a local framework packaging step; the resulting Artifact must still be published with xAPI.

## Start with scope

- Identify the control-plane host, Worker ID, and **preview or production** from the project and `workers get`. Test control plane and preview environment are separate choices.
- Authentication precedence: `XAPI_KEY`, `XAPI_API_KEY`, then `~/.xapi/config.json`. Keys need `workers:read` and, for changes, `workers:write`, plus access to the target Worker. A scoped-out Worker can return 404.
- Production API host is `api.xapi.to`; testing uses `XAPI_API_HOST=api.test.xapi.to` (host only). Load secrets from the user's existing secure environment. Never print keys, include them in code/artifacts, or send the xAPI key to a public Worker URL or Cloudflare. Runtime application authentication is separate.
- For an existing linked project, start with `workers inspect [worker-id] --env <environment>` and `workers capabilities`. For a new unlinked project, use capabilities and plan; inspect needs a real Worker ID. Use `workers plan --env <environment>` when a local project is available and desired-state drift matters. `inspect` reads current runtime state only. `plan` runs the configured local build with credential-shaped environment variables removed, validates the exact Artifact, and compares it with live state without writing to the xAPI control plane. It also shows the budget cap, active price-book visibility, and usage-dependent resource changes; never present those estimates as an accrued invoice. Use existing user authorization for changes; don't expand cleanup from a test environment to production.
- Treat Worker execution and data placement separately. Worker code remains global. Use environment `defaultResourceLocation` only as the default for newly created D1/R2 resources and `placementMode: smart` only for Cloudflare Smart Placement. Never claim either setting migrates existing data.

## Build where the CLI runs

The MVP deployment path builds where the CLI runs, uploads the immutable artifact
and publishes it through xAPI. That execution environment may be a computer, CI
runner or user-owned Sandbox. A user-owned Sandbox remains under its own billing
and lifecycle; Worker deployment never implies its automatic deletion. Managed
server-side `workers build` retains the main-branch unavailable contract. New user
delegation and a separate cloud-build customer charge are deferred; do not claim
that an ordinary `workers push` creates or bills a managed build Sandbox.

## D1 migrations are explicit

`workers push` and `workers promote` preserve resource creation/binding and Queue/Cron `AFTER_CODE`, but do not read or execute D1 SQL. Use `workers d1 migrations plan` for a local-only plan and `workers d1 migrations apply` for explicit remote execution. Both take `--binding NAME --env preview|production [--config PATH]`. Read [the complete migration workflow](references/deployment.md#explicit-d1-migrations) before migration work, including first-deployment ordering and failure handling. Ordinary publishing does not require migration-ledger repair; code rollback does not undo SQL.

## Before creating a Worker or resource

Briefly tell the user: provisioning/deployment prepares the server-calculated protected retention funds and a separate operating reserve; an empty project record does not freeze funds. Storage can cost money while paused. After overdue retention begins, Preview and Production receive at least 168 hours of protection. Preservation continues beyond that minimum while spendable retention funds remain; exhaustion after the minimum permits system cleanup. Unused funds are returned after confirmed cleanup and the settlement window. Recharging does not automatically resume service, and ephemeral Container disk is not a protected persistent volume.

This is an informational reminder, not a separate approval gate. Use existing creation/deployment authorization; do not require `retention accept`, a per-resource quote sequence or a mandatory price-version argument. Plan shows funding estimates; the server validates account funds and freezes them atomically, including when optional automatic maintenance is disabled. A user-selected `--retention-price-version` remains an optional explicit input. See [lifecycle.md](references/lifecycle.md). An older backend requiring extra policy enrollment is a version mismatch to report, not a reason to bypass managed funding.


## Load the relevant workflow

- **Build/deploy/import/CI:** read [deployment.md](references/deployment.md).
- **Use and verify resources, including Containers:** read [resources.md](references/resources.md).
- **Export owned D1/R2 data:** read [the export workflow](references/resources.md#export-d1-and-r2-business-data). Binding selection needs `workers:read` plus the separate `workers:data:read` scope; management read/write does not grant data access. Export completion does not establish migration or import completion.
- **Configure public vars and runtime credentials (including first-project setup):** read [secrets.md](references/secrets.md). Secret values go to the environment's Cloudflare User Worker binding; never ask xAPI to reveal them.
- **How much did it cost?** Read [billing.md](references/billing.md) before answering, collecting, or reconciling consumption.
- **Funding protection/recover/delete/refund:** read [lifecycle.md](references/lifecycle.md) before lifecycle mutations.
- **Bind/switch a domain, handle DNS conflicts, or buy an xdomain domain:** read [domains.md](references/domains.md). Check zone eligibility and existing records first. Use combined attach for xdomain, or challenge plus manual TXT and attach for an eligible zone without an xdomain record. Do not manually create a CNAME to the Dispatcher or expose Cloudflare zone IDs.

## Evidence and completion

Follow a full round: execute real business operations → collect failures → confirm reproduction and affected paths → fix together → rerun affected real operations. Unit tests supplement this; label them separately from live acceptance.

`ACTIVE` deployment, a provisioned resource, an accepted asynchronous job, and a passing HTTP health check prove different things. Verify the intended business result and persisted state. Preserve sanitized evidence: host, environment, IDs, times, request/job IDs, statuses, snapshot and ledger IDs, exact decimal amounts, and unresolved gaps. Exclude tokens, cookies, passwords, and customer file contents.

For Cloudflare Containers, `ACTIVE` means the Worker upload, matching Durable Object namespace resolution, and the required Container Application create/update plus rollout request were accepted and recorded. Cloudflare may still be converging the native rollout; verify the application resource and business route separately. A Docker image build or registry push is a separate prerequisite and is never implied by an xAPI Artifact upload.

For incomplete observations report **unknown**, not zero or success. Keep deployment completion, resource behavior, xAPI consumption, storage-day finalization, provider invoice reconciliation, and physical cleanup as separate verdicts. Report only verified outcomes and the next concrete unresolved check.

Lifecycle action exit 0 or `ACCEPTED` confirms a returned receipt, not completion.
With `SUSPENDING` / `CONTAINER_STOP_PENDING`, inspect `billing lifecycle` and
`retention show --format json` for the current steps. Runtime upload success or a
`SKIPPED` native stop does not prove the Container stopped. `retryRequired` calls
for inspecting the evidence before an explicit retry, not automatic control replay
or forced recovery.

For billing usage, read [the quantity and coverage guidance](references/billing.md)
before reconciliation. `workers billing usage` defaults to complete aggregate
pagination and human output; quantities remain exact strings, with coverage and
UTC cutoff shown separately. Observed totals are not invoices or proof of complete
metering. Older services without aggregates remain explicitly unverified.

### Direct artifact uploads and deployment configuration

The CLI checks `artifact-provider/status`. When R2 direct upload is available,
it prepares an owned temporary session, uploads checksummed bytes directly to
R2 without the xAPI key, then asks xAPI to verify and seal the immutable artifact.
There is no deployment/fund hold while uploading. Cancelled or expired sessions
do not block the next push; native deployment starts only after confirmation.
Transient object failures get at most three attempts within the same authorization,
upload deadline and eight PUT slots; retry progress is visible. Cancellation or
expiry stops recovery. Query the displayed upload ID before an explicit new push;
object recovery does not replay confirmation or deployment. The temporary channel
has a 15-minute lifetime; an expired channel needs an explicit new upload.
Never paste signed object URLs in reports. The legacy upload API remains usable
when the configured storage does not support direct upload.

Use `xapi workers pull --env preview --format json` to inspect the confirmed
active deployment's public configuration and differences against local Wrangler
settings. `--output deployment-snapshot.json` saves that snapshot separately,
preserving unknown native metadata. It does not rewrite Wrangler, download code
or restore business data. `resources pull` refreshes resource IDs/declarations.
The explicit output may be outside the project, for example
`--output ../evidence/deployment.json` or an absolute file path. Relative paths
remain based on the Worker project root; the parent directory must already
exist. Pull protects this project's configuration files and refuses a symbolic
link output. It atomically replaces a chosen existing snapshot and checks for
local changes on a best-effort basis; coordinate simultaneous writers yourself.
Snapshots contain public variable values, but only Secret names; protect local
snapshot files. A legacy deployment without a recorded snapshot reports that
configuration is unavailable. Pull does not force a subsequent deployment.
Plan and push reuse a matching current ACTIVE deployment, including a successful
rollback whose recorded target proves the same Artifact and deployment inputs.
This also covers a previous successful rollback when every exact link to the
matching release is already present in the returned history. No extra history
queries are made; missing links or cycles require normal deployment.
Missing target evidence or changed configuration requires normal deployment;
this no-op does not promise that every edge has instantly converged.
For `workers push` and `workers rollback`, JSON-mode stdout contains one final
result. Build logs and intermediate plan diagnostics go to stderr; capture the
streams separately when parsing receipts. Confirmation requirements are
unchanged. Pull treats absent and empty Queue binding-alias maps as equivalent
for differences, while preserving the actual saved deployment snapshot.

A successful native deletion with pending financial bookkeeping is already
physically deleted. Inspect returned `financialFinalization` and access status;
do not repeat deletion to repair platform accounting. Funds remain frozen until
verified local close and existing tail-invoice/refund rules permit release.

### 删除确认与部署声明

- 删除回执标记 `deletionCompleted: false` 表示尚未完成；CLI 命令结束不能代替这个字段。若操作记录证明原生 DELETE 已成功、只缺 script GET 确认，SDK `recoverWorkerControlOperation` / `POST /api/v1/workers/:id/control-operations/:operationId/recover` 只补查询和本地收尾，不重复 DELETE。其他资源尚未清理或原生 DELETE 本身 UNKNOWN 时不会通过这条路径重放。
- 回滚操作身份包含当前版本和目标版本；更新后再次选择相同历史版本会发起一次新的显式回滚，不复用旧成功回执。
- 部署快照 `requiredSecrets` 记录项目环境和所选 Wrangler 环境的必需 Secret 名称，不保存值。

### Platform authentication failures

A complete CF 401 authentication rejection is a recorded failed write, not an
unknown accepted mutation. Report the platform credential error accurately.
Do not automatically replay the write or expand permissions. Incomplete
responses/transport failures remain UNKNOWN; old UNKNOWN records need their
own evidence and are not silently rewritten by this classifier.
