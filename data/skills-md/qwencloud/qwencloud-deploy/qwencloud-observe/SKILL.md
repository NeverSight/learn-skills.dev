---
name: qwencloud-observe
version: "1.0"
description: >-
  Report the health, performance, resource status, and actual billed cost of an application
  deployed by qwencloud-deploy to Alibaba Cloud International (alibabacloud.com), in plain
  language and without opening the console. Reads the local .qwencloud-deploy state file to
  identify the app and its ECS (and optional RDS MySQL) resources, then queries read-only
  cloud APIs to summarize application availability, ECS/RDS performance, and USD cost.
  Use when: the user asks how their deployed app is doing, wants a health/performance/cost
  overview, asks about CPU/memory/connections/slow SQL risk, or asks the monthly cost of a
  qwencloud-deployed app.
  Do not use when: no .qwencloud-deploy state file exists, the target is Aliyun China
  (use qianwenai-observe), or the user wants to change/recover resources (use qwencloud-operate).
prerequisites:
  - aliyun CLI 3.x configured with international-site credentials
  - a .qwencloud-deploy state file in the project directory
  - Python >= 3.8 (only if you render a report file with scripts/render_report.py)
input: >-
  A project directory containing .qwencloud-deploy. Optional: time window (15m / 1h / 24h,
  default 1h).
output: >-
  A plain-language overview: one-line overall status, then Application / ECS / RDS / Cost
  summaries, risks with evidence, data timestamp, and unknown items. Offers a next step into
  qwencloud-operate when a fault is found.
---

# Qwen Cloud Observe

Read-only observability for an application deployed by `qwencloud-deploy`. Answers "how is my
app doing and what will it cost" without the console. All prices are **USD**.

## Quick Path

1. **Identify the app** — read `.qwencloud-deploy` in the project directory (`references/workflow.md`).
2. **Pick the window** — default last 1h; user may pick 15m / 1h / 24h.
3. **Check each layer** — Application, ECS, (optional) RDS, Cost. Each check returns one of the
   unified result states; a failed check never blocks the others.
4. **Report** — one-line conclusion, then per-layer summary, risks, data timestamp, unknowns.

## Scope

| In Scope | Out of Scope |
|----------|--------------|
| Apps deployed by `qwencloud-deploy` (state file present) | Apps without a `.qwencloud-deploy` state file |
| Single ECS, or ECS + RDS MySQL 8.0 | Other topologies / self-managed servers |
| Read-only availability, performance, cost overview | Any change to cloud resources → use `qwencloud-operate` |
| Report runtime status (availability, performance, cost) | Source-code review, finding bugs/vulns, judging which line is wrong, editing code |
| Alibaba Cloud International, USD | Aliyun China → use `qianwenai-observe` |

## Code issues are out of scope

This skill is read-only observation, reporting runtime availability, performance, and cost. It
does not review source code, locate defects, or edit code.

When code is involved, tell the user plainly: editing code is outside this skill's scope, the user
must decide and make the change themselves, and any consequences are the user's own.

## Prerequisites

> **Aliyun CLI**: run `aliyun version` (need 3.x). All queries use the PascalCase native form
> straight to OpenAPI — no plugin dependency. Credentials: check with `aliyun configure list` only.
> **Never** read, echo, print, or ask for AK/SK/tokens. If no valid profile exists, stop and ask
> the user to configure credentials outside this session. See `references/cli_installation_guide.md`.

## States and scoring

Every layer returns one state — `healthy` · `degraded` · `unavailable` · `unknown` — carrying its
check time, target resource, key evidence, and data source. When a single query fails, keep
checking the other layers and mark the failed item `unknown` — never silently drop it, never
fabricate data.

Each layer also gets a score, and the layer scores sum to a 0-100 health score with an A/B/C/D
grade (`>=90` A · `>=75` B · `>=60` C · `<60` D). Four dimensions are scored:

| Dimension | Weight (with RDS) | Weight (no RDS) | Signals |
|-----------|-------------------|-----------------|---------|
| Application | 35 | 45 | reachability, `/healthz`, response time, error rate, certificate validity (with domain) |
| ECS | 30 | 45 | CPU, memory, disk usage, disk IO, network |
| RDS | 25 | — | connections, slow SQL, space, row-lock waits |
| Availability | 10 | 10 | ECS/RDS run status, recent system events, EIP status and bandwidth, security-group exposure |

When the app has no RDS, its weight moves to Application and ECS. **Cost is never scored** — it is
shown separately as the actual bill plus a utilization-based optimization note.

Missing backups/snapshots and security-group hardening are surfaced as risks and recommendations,
**not scored**; availability-affecting signals — EIP unbound, bandwidth saturated, missing 80/443
ingress — count toward the Availability dimension.

## How to check

Start by identifying the app, then look at each layer. Read the linked guide before running its
commands. A failed check never blocks the others — mark it `unknown` and move on.

The layer checks are independent and read-only — after identifying the app, fire each layer's
read-only APIs in parallel (background `&` + `wait`) rather than waiting serially; merge the Cloud
Assistant commands on one ECS into a single script fetched in one round trip.

1. **Identify the app** — read `.qwencloud-deploy` for the region and resource IDs.
   See [workflow](references/workflow.md).
2. **Is the app reachable?** — probe the public address and `/healthz`, check the app and Nginx
   services and their ports, and summarize recent errors. See
   [observe-application](references/observe_application.md).
3. **How is the server doing?** — ECS status plus CPU, network, disk, and memory over the window.
   See [observe-ecs](references/observe_ecs.md).
4. **How is the database doing?** (only when the app has RDS) — status, connections, QPS/TPS,
   space, row-lock waits, and redacted slow SQL. See [observe-rds](references/observe_rds.md).
5. **How are the public entry and exposure?** — EIP status and bandwidth, security-group 80/443
   and exposure risks. See [observe-network](references/observe_network.md).
6. **Any maintenance or backups?** — ECS system events, system-disk snapshots, RDS backups. See
   [observe-resilience](references/observe_resilience.md).
7. **What is it costing?** — the actual billed cost for the app, with an optional month-end
   projection. See [observe-cost](references/observe_cost.md).
8. **Score and pull it together** — score each layer, sum to the health score and grade, and write
   one plain-language conclusion. See [workflow](references/workflow.md).

The default window is the last hour; honor an explicit 15 minutes / 1 hour / 24 hours request and
state the window used.

## What to tell the user

Lead with the health score and grade plus a one-line verdict, then a short line each for the
application, server, database (if any), and cost — each with the evidence behind it. Call out risks
and note anything you could not determine and why, plus the data timestamp. When `operate_audit.jsonl`
exists in the project directory, include the most recent operate action (time, action, result) so
the score lines up with the latest recovery. When you find a real fault, offer to move on to fault
diagnosis with `qwencloud-operate`: use AskUserQuestion to present **Diagnose and fix now** /
**Just look, no changes**; picking the former enters `qwencloud-operate`. Also write the evidence
already gathered to `observe_handoff.json` in the project directory (fault layer, key metrics, data
timestamp; never any password/signed URL) so operate can use it as a starting point and skip
repeating the read-only checks.

```text
Health score: 87 / 100 (B, Good) — app healthy; watch the RDS connection trend.

Application: reachable, current response time 186 ms; app and Nginx services healthy.
Certificate: valid, 54 days remaining (app.example.com).
ECS: healthy, last 1h average CPU 31%, no sustained high load.
RDS: healthy, active connections rose from 12 to 38 — watch the connection-pool trend.
Cost: actual bill for 2026-08 so far $12.40 (ECS $7.80, RDS $4.60).

Data as of: 2026-08-03 16:20 UTC+8
```

After the summary, proactively ask whether to export a report file, e.g. "Want me to export a
Markdown or HTML report?" — the user decides; do not force it.

## Interaction form

- **Read-only information** (checkup verdict, status, cost): plain text, with one evidence line after
  each judgment (metric, status, timestamp).
- **State-changing actions** (entering operate, exporting a report): use AskUserQuestion whose prompt
  answers **what it does** · **impact** · **how to verify**; do nothing before the user confirms.
- **Proactive discipline**: stay quiet when healthy; speak up only on a risk or real fault, and offer
  at most one follow-up action (diagnose / export report) for the user to choose.

## Render a report file (optional)

When the user wants a saved Markdown or HTML report, gather every layer's state, per-layer score,
key metrics, and evidence into one JSON object and let `scripts/render_report.py` render it — do
not hand-format the final file. The HTML output is a multi-card report (overview with the score
and anomalies, one card per layer with a metric table, a cost card, and recommendations); Markdown
is the lightweight equivalent.

1. Print the schema and fill it in: `python3 scripts/render_report.py --schema`. Each layer needs a
   `state`, a `score`/`max_score`, `metrics[]`, and `detail`; `assessment.health_score` must equal
   the sum of the layer scores and match its grade; cost carries the actual billed amount only.
2. Validate before rendering: `python3 scripts/render_report.py --validate -i data.json`. Fix any
   reported issue (bad state, `unknown` without a reason, grade/score mismatch, any estimate in cost).
3. Render in the format the user picks:
   `python3 scripts/render_report.py -i data.json -f md -o report.md` (or `-f html`).

## Handoff to operate (optional)

When you find a real fault and the user chooses to enter `qwencloud-operate`, write
`observe_handoff.json` to the project directory so operate can start from it and verify the named
layer first:

```json
{
  "from": "qwencloud-observe",
  "generated_at": "2026-08-03T16:20:00+08:00",
  "fault_layer": "rds",
  "symptoms": ["RDS active connections rose from 12 to 190, near the cap"],
  "metrics": {"rds_active_connections": 190, "app_http_code": 200}
}
```

`fault_layer` is one of `app` / `nginx` / `ecs` / `rds` / `network` / `disk`. Write only read-only
observed evidence; **never** a password, connection string, or signed URL. It is a hint only —
operate still verifies independently before proposing any recovery action.

## Security

| Rule | Detail |
|------|--------|
| Read-only only | Cloud Assistant commands must be read-only; never modify instance/app state. |
| No secrets | Never read/output passwords from `.qwencloud-deploy.local`. |
| Redaction | Mask AccessKey, tokens, passwords, connection-string passwords, and cookies in any log output. |
| Slow SQL | Output SQL templates / redacted SQL only, length-limited; never raw literal values. |
| Cost | Show actual billed cost only (USD) with the billing cycle; never show an estimate. When there is no bill yet, mark cost `unknown`. |

## Required Permissions

See `references/ram_policies.md`. Read-only except `cms:InstallMonitoringAgent` (lazy agent install):
`ecs:DescribeInstances`,
`ecs:RunCommand` + `ecs:DescribeInvocations` (read-only commands), `cms:DescribeMetricList`,
`cms:DescribeMonitoringAgentStatuses`, `cms:InstallMonitoringAgent`, `ecs:DescribeSecurityGroupAttribute`,
`ecs:DescribeInstanceHistoryEvents`, `ecs:DescribeSnapshots`, `vpc:DescribeEipAddresses`,
`bssopenapi:QueryInstanceBill`, `bssopenapi:QueryBill`, and (with RDS)
`rds:DescribeDBInstances`, `rds:DescribeDBInstanceAttribute`, `rds:DescribeDBInstancePerformance`,
`rds:DescribeSlowLogRecords`, `rds:DescribeBackups`.

## More detail

The per-layer guides are linked from "How to check" above. Two setup references:

- [CLI setup](references/cli_installation_guide.md) — install and credential check.
- [CLI gotchas](references/api_gotchas.md) — parameter shapes, time formats, response parsing.
- [RAM policies](references/ram_policies.md) — the read-only permissions this skill needs.
