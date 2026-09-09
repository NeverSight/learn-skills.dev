---
name: oodle-o11y-review
description: Reviews a code change's telemetry during authoring or code review — checks business-context attributes and cardinality placement, telemetry duplication, RED/USE/queue/fan-out coverage, and alert-driven scrutiny of code guarded by existing alerts and SLOs. Writes findings into the O11y Change Context manifest and hands fixes off to oodle-monitors, oodle-drop-rules, and oodle-log-metrics. Use when reviewing or authoring instrumentation changes.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,observability,code-review,instrumentation,cardinality,slo
  globs: ""
  alwaysApply: "false"
---

# Oodle Telemetry Review — Left-Side Observability

Review the telemetry in a code change with the judgment a senior SRE brings to a
PR. This skill does **not** teach how to instrument — modern agents already know
the SDKs. It applies the judgment that is easy to skip: is the emitted telemetry
carrying the right business context at the right cardinality, is it
non-duplicative, does it cover the failure modes that matter, and is it adequate
to debug the alerts that already guard this code.

Review the **diff**, not the whole repository. Findings are recorded in the
[O11y Change Context](../oodle-o11y-context/SKILL.md) manifest so they travel
downstream to triage. Concrete fixes are handed off to the existing Oodle skills
rather than re-explained here.

## When to use

- Reviewing or authoring a change that adds or alters metrics, spans, or logs.
- A PR touches instrumented or service code on a path that carries request
  context (tenant/account/user) or does measurable work (I/O, loops, pools).

Skip telemetry review for docs-only or cosmetic changes.

## Backend discovery (do this first)

Resolve what observability backend is reachable, by **capability and tool
shape** — never by a hard-coded server name (names vary: `oodle-ai-us1`, `ap1`,
`staging`, `dev`, or a customer-custom name).

1. Look for an observability MCP exposing metric / alert / log / trace query
   tools. Prefer discovering tools by their function (e.g. "find monitors",
   "query metrics", "search traces") over any fixed prefix.
2. If the tool suite matches Oodle's shape (monitors, PromQL query, logs, traces,
   plus `load_skill__*` workflows), use the **Oodle tight path**: pick the
   environment that owns the touched service, and load a matching
   `load_skill__*` when one fits.
3. If a different vendor's observability MCP is present, use its equivalents.
4. If **no** observability backend is reachable, run checks 1–3 (they are
   static, from the diff) and explicitly report check 4 as degraded — do not
   skip it silently.

## Check 1 — Business context & cardinality placement

Where request context carries identity (tenant, account, user, org), that
identity must ride the telemetry — placed by cardinality:

- **Low cardinality → metric labels.** Bounded sets only: route, method, status
  class, region, tier, queue name. These multiply the time series.
- **High cardinality → span attributes and log fields.** `tenant_id`,
  `account_id`, `user_id`, `order_id`, `request_id` belong here, where they add
  debuggability without exploding series.
- **Loops and batches** must carry an iteration or batch identifier
  (`item_index`, `sku`, `batch_id`) on the span/log so per-iteration work is
  attributable.

Flag: a high-cardinality value on a metric label (recommend relocation to a span
attribute or log field, and hand off to `oodle-drop-rules` if the metric already
ships); tenant/account absent from telemetry in tenant-scoped code.

## Check 2 — No duplicate telemetry

Every added metric, span, or log must serve a distinct job. If a new signal
overlaps one that already exists (a timer duplicating a histogram; a log line
restating a span; two counters measuring the same event), flag it. Recommend
removal — recorded as a `-` line with a reason in the manifest `telemetry`
field — or an explicit statement of the distinct purpose that justifies it.

If a signal's purpose cannot be named in one line, it should not be added.

## Check 3 — Perf-coverage patterns

On the touched code, check for the coverage that catches performance regressions:

- **RED** on request handlers — Rate, Errors, Duration (a latency histogram by
  route/method, an error counter by class).
- **USE** on resource pools — Utilization, Saturation, Errors (DB/HTTP/thread
  pools: active vs max, wait time / queue depth, connection errors).
- **Queue saturation** on async work — depth, consumer lag, processing time.
- **Fan-out / N+1** — a loop issuing per-iteration I/O (DB, cache, RPC) with no
  batched call and no span measuring the loop. Flag it and record the risk in
  the manifest `watch` field.

Report missing coverage on touched code as a gap; do not demand coverage for
untouched code.

## Check 4 — Alert-driven scrutiny

This is the differentiator: align review effort with what production already
cares about.

1. From the backend, resolve which alerts and SLOs **guard the touched code**
   (by service/route/metric the change affects).
2. For guarded code, demand the telemetry needed to *debug that alert* exists. A
   latency alert guarding a path that lacks the spans/attributes to localize
   where time is spent is a **critical** finding — an alert nobody can act on.
3. Record the guards in the manifest `guarded-by` field and mark the change
   higher-risk (upgrade `type` toward `critical-path` when a critical SLO is
   involved).
4. If a guarded failure mode has a known blind spot, add it to the manifest
   `gaps` field so triage knows the data cannot answer it.

When no backend is reachable, state that guards could not be resolved and
recommend the author confirm them manually.

## Output discipline

- Report only high-confidence findings. Tag each
  `critical` / `important` / `minor`. Do not produce a wall of nitpicks — the
  goal is signal, matching Oodle's avoid-alert-fatigue ethos.
- **Write results into the manifest**: fill or refine `telemetry` purposes,
  `guarded-by`, `watch`, and `gaps` per the
  [O11y Change Context](../oodle-o11y-context/SKILL.md) contract.
- **Hand off concrete fixes** rather than re-teaching them:
  - add or tune a guarding monitor → [oodle-monitors](../oodle-monitors/SKILL.md)
  - drop or sample a high-cardinality / high-volume metric → [oodle-drop-rules](../oodle-drop-rules/SKILL.md)
  - derive a metric from logs → [oodle-log-metrics](../oodle-log-metrics/SKILL.md)
- Say **what** to change and **why** it matters. The agent already knows **how**
  to write the instrumentation.
