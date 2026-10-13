---
name: kubesense-slo
description: Create, read and manage KubeSense service level objectives (SLOs) over the REST API — by_count, time_slice and alert-uptime SLIs, error budgets, burn-rate alerting and grouping — and translate Datadog SLOs into equivalent KubeSense ones. Covers the exact POST /api/slo payload, the good/total query config shape it shares with alert rules, and the traps that make an SLO store cleanly and then evaluate nothing.
metadata:
  version: "1.0.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,slo,sli,error-budget,burn-rate,datadog-migration,reliability
---

# KubeSense SLOs

An SLO here is a stored definition plus a background evaluator. Every
`evaluation_interval_seconds` the evaluator scores one bucket, writes it to
ClickHouse, and emits Prometheus series (`kubesense_slo_*`). Compliance is then a
rolling aggregate over `evaluation_window_days`.

> [!IMPORTANT]
> **There are no SLO MCP tools.** Logs, traces, metrics and alerts have them; SLOs
> do not. Everything here is the **REST API** at `/api/slo`, authenticated exactly
> like the MCP server (`x-api-key`, or `Authorization: Bearer <token>`). Use the
> MCP query tools to *discover* metric and field names, then build the SLO body.
>
> **So this skill needs two things an MCP connection does not give you**: a way to make
> HTTP calls (a shell with `curl`, or an HTTP tool), and the API credentials as a value
> you can put in a header — the MCP server's own credentials are not readable from
> inside a tool call. An agent with MCP alone can still build and explain the payload,
> and should say plainly that the user has to send it.

## The Lifecycle

Follow it in order. Steps 5 and 6 are the ones people skip, and they are the ones that
catch an SLO that stored cleanly and evaluates nothing.

1. **Discover.** Real metric names (`get-available-metrics`, `get-metric-labels`) and
   real field names (`get-trace-or-log-fields`). Channel ids for the burn-rate alerts
   (`list-notification-channels`). Alert rule uuids if it is an alert SLO.
2. **Construct** the body — the type, the two queries, the window, `alert_types`.
3. **Preview** with `POST /api/slo/preview`, knowing what preview does and does not
   check. A wildly wrong number is usually a filter bug. `no_data` **is not proof of
   one** — a genuinely quiet service produces empty windows too; tell the two apart
   before changing anything (step 6). For an **alert** SLO, pass `from_time`/`to_time`
   explicitly: the default window reaches back before the rules existed, where the
   absence of firing rows reads as perfect uptime.
4. **Create** with `POST /api/slo` and keep the returned id. No id, no SLO.
5. **Read back** with `GET /api/slo/{id}?current_time=…` and check the stored config is
   what you sent — particularly `slo_type`, `operation`, and both `groupBy` lists.
6. **Verify real buckets** after one or two evaluation intervals:
   `GET /api/slo/{id}/metrics?from_time=…&to_time=…`, plus the SLO read-back.
   - **`last_evaluated` advancing** between two reads is what proves the evaluator
     picked the SLO up. Null, or frozen, means it never did — check `status`, the
     interval, and the group cap.
   - A **non-zero** `total_events` (or `total` slices/seconds) additionally proves the
     query resolves and matches.
   - **Zero is not automatically a bug.** A quiet service legitimately produces empty
     buckets — `no_data` for `by_count`, uptime for `time_slice`. Before touching the
     SLO, query the same scope and window directly with `analyze-traces` /
     `analyze-logs` / `analyze-metrics`: no rows there either means the telemetry is
     absent, which is a different problem to fix somewhere else.
   - **Never widen the user's filter to make numbers appear.** That changes what is
     being measured into something nobody asked for. Report the empty result and what
     you checked.
7. **Verify the generated alerts** if you set `alert_types` — they should exist as
   rules named `"<SLO name> Fast Burn Rate"` and so on, with your channel ids.
8. **Update or delete** with `PUT` (full body, id inside) or `DELETE /api/slo/{id}`,
   then repeat steps 5–7. An update rebuilds the generated rules.

## The Three SLI Types

| `slo_type` | Numerator / denominator | What you configure | Count unit |
|---|---|---|---|
| `by_count` | good events / total events | **two** queries: `good_events_filter` and `total_events_filter` | `events` |
| `time_slice` | good slices / total slices | **one** query (`total_events_filter`) + `operation` + `threshold_value` | `slices` |
| `alert` | non-firing seconds / total seconds | alert rule ids in `total_events_filter.alert_ids` | `seconds` |

`slo_type` defaults to `by_count` when omitted. The UI calls them "By Count", "By
Time Slices" and "By Uptime".

## Routing

| The user is asking… | Do this |
|---|---|
| "create an SLO for X" | build the `POST /api/slo` body — [references/api-payloads.md](./references/api-payloads.md) |
| "will this SLO pass?" / "what would compliance have been?" | `POST /api/slo/preview` **before** creating — it costs nothing and stores nothing, but it is an estimate, not a replay ([limits](./references/api-payloads.md#preview--always-do-this-first)) |
| "what SLOs do we have / which are breached?" | `POST /api/slo/list?status=active&current_time=…`, or `POST /api/slo/stats` |
| "why is this SLO burning budget?" | `GET /api/slo/{id}/burn-rate/timeseries`, then [kubesense-traces](../kubesense-traces/SKILL.md) / [kubesense-logs](../kubesense-logs/SKILL.md) on the same filter |
| "alert me when the budget burns" | `alert_types` on the SLO — do **not** hand-write burn-rate alert rules |
| "port our Datadog SLOs" | [references/datadog-migration.md](./references/datadog-migration.md) |
| "put SLOs on a dashboard" | [kubesense-dashboards](../kubesense-dashboards/SKILL.md) — `panelType: "slo"` |

## Endpoints

All under `/api/slo`, RBAC module `slo`. Create/update/delete additionally need
**write** access on that module.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/slo` | create — returns the new SLO id in `data` |
| `PUT` | `/api/slo` | update — the id goes in the **body** as `id`, not the path |
| `DELETE` | `/api/slo/{id}` | soft delete (sets `removed`) and drops its burn-rate alert rules |
| `GET` | `/api/slo/{id}?current_time=<RFC3339>` | one SLO with its rollups |
| `POST` | `/api/slo/list?status=active&current_time=<RFC3339>` | list; filters in the JSON body |
| `GET` | `/api/slo/search?search=<substr>&limit=50` | `{id, name}` only — for pickers |
| `POST` | `/api/slo/stats` | counts by status: normal / warning / breached / no_data |
| `POST` | `/api/slo/preview` | dry-run compliance over a window, stores nothing (status is `normal`/`breached`/`no_data` — never `warning`) |
| `GET` | `/api/slo/{id}/metrics?from_time=&to_time=` | good/bad/total + budget for a window |
| `GET` | `/api/slo/{id}/groups?windows=last_24_hour,last_7_days` | per-group figures, several windows in one scan |
| `GET` | `/api/slo/{id}/timeseries` | compliance over time |
| `GET` | `/api/slo/{id}/burn-rate/timeseries` | burn rate over time |
| `POST` | `/api/slo/filters`, `/api/slo/filter/search` | filter values for the list page |

> [!WARNING]
> **`current_time` is required on `/list` and `GET /{id}`, and `status` is required
> on `/list`.** Both are **query parameters**, not body fields. Omit `current_time`
> and the call 500s ("currentTime must not be zero"); omit `status` and the
> `WHERE status = ?` matches nothing and you get an empty list that reads like
> "no SLOs exist". Send `status=active`.

## The Create Payload

Minimum viable `by_count` SLO over traces:

```json
{
  "name": "Checkout availability",
  "description": "Successful checkout spans / all checkout spans",
  "slo_type": "by_count",
  "metric": "requests",
  "slo_target_percentage": 99.9,
  "evaluation_window_days": 30,
  "evaluation_time_interval_seconds": 60,
  "evaluate_from": "2026-09-01T00:00:00Z",
  "evaluation_start_time": "2026-09-01T00:00:00Z",
  "status": "active",
  "cluster": "", "namespace": "", "workload": "", "customer_identifier": "",
  "operation": "", "threshold_value": 0, "value": 0,
  "good_events_filter":  { "selectedMode": "traces", "value_operation": "row_count", "groupBy": [], "unified_filter": { "type": "common", "common_filter": [ {"field": "app_service", "operation": "IN", "values": ["checkout"]}, {"field": "status", "operation": "IN", "values": ["ok"]} ], "adv_filters": {} } },
  "total_events_filter": { "selectedMode": "traces", "value_operation": "row_count", "groupBy": [], "unified_filter": { "type": "common", "common_filter": [ {"field": "app_service", "operation": "IN", "values": ["checkout"]} ], "adv_filters": {} } },
  "alert_types": ["burn_rate_fast", "error_budget_low"],
  "notification_channels": [1]
}
```

Every per-type shape, the metrics and logs variants, and the response bodies are in
**[references/api-payloads.md](./references/api-payloads.md)**.

Rules of the body:

- `evaluation_time_interval_seconds` **must be > 0** — the server rejects 0 outright,
  and the evaluator skips an SLO whose interval is 0 rather than looping forever.
- `status: "active"` or the evaluator never picks it up.
- `slo_target_percentage` is a percentage (`99.9`), not a fraction.
- `warning_target_percentage`, when set, should be **higher** than the target — it is
  where you want to be warned *before* breaching. The UI enforces `>= target + 0.1`;
  **the API does not validate it at all**, and a value below the target is stored and
  never reached, because the breached check runs first.
- `metric` is a **label**, not a query. `"requests"` for a traces SLI, the PromQL
  metric name for a metrics SLI, `"alert_uptime"` for an alert SLI. Nothing is
  evaluated from it — it just lands on the list page and in filters.
- `operation` / `threshold_value` are the **time_slice condition only**. `by_count`
  ignores them; fold a latency cutoff into the good query as a duration filter
  instead.
- Update is a **full replace**: `PUT /api/slo` writes every column from the body, so
  send the whole object (read it back with `GET /api/slo/{id}` first), and put the
  id in the body as `id`.

## Good and Total Are Alert Query Configs

`good_events_filter` and `total_events_filter` are the **same `query_config` object
an alert rule uses** — same JSON keys, same executors, same field allow-lists. That
is the single most useful thing to know: anything you know about building an alert
rule's query applies here.

| Key | Meaning |
|---|---|
| `selectedMode` | `traces` \| `logs` \| `metrics`. **Defaults to `traces`** when empty. |
| `unified_filter` | traces/logs filter tree: `{type, common_filter[], adv_filters{}}` |
| `promql` | metrics only — the whole metrics query. (An alert rule's `queryMode` has no field here and is dropped.) |
| `value_operation` | `row_count` (the normal choice), `unique_count`, `avg`, `sum`, `min`, `max`, percentiles |
| `fields` | required for any non-count `value_operation` |
| `groupBy` | `[{field, type, is_attribute}]` — see Grouping |
| `alert_ids` | alert-type SLOs only |

> [!IMPORTANT]
> **Field names follow the ALERT engine's vocabulary, not the query tools'.**
> Logs and traces SLI queries run through the same rule-engine executors alert rules
> use, so `app_service` (not `service`), `level` (not `type`), `pod_name`/`pod`,
> `node_name`/`node`, `return_code`/`status_code`. The full allow-lists are in
> [kubesense-alerts](../kubesense-alerts/SKILL.md#field-names--a-different-vocabulary)
> — they are the authority for SLOs too.
>
> There is one divergence to know about: **`POST /api/slo/preview` runs the query
> through the API's own explore engine, while the evaluator runs it through the
> rule-engine.** Their field maps overlap but are not identical, so a name that
> previews fine can still error on every evaluation. Preview also **hardcodes
> `row_count` for traces and logs** (ignoring `value_operation` and `fields`, so a
> latency SLI previews request counts) and **samples ~300 points** for metrics rather
> than evaluating every bucket. Preview catches an empty or wrong filter; it does not
> validate the number. Confirm on the first real buckets after creating.

## Formulas and Ratios

A Datadog monitor or SLO built from several queries and an expression like
`(A/B)*100` does not port as one thing. Where it lands decides the shape:

| What you are porting | Where it goes | How |
|---|---|---|
| An SLO whose SLI is numerator / denominator | **`by_count` SLO** | **Two queries, no formula.** A → `good_events_filter`, B → `total_events_filter`. The evaluator divides them itself. |
| A monitor that thresholds a ratio | **Alert rule** | Alerts have a real formula mode — keep A, B and `expression` as separate queries and point `metric_query_label` at the formula's label. See [kubesense-alerts](../kubesense-alerts/SKILL.md). |
| An SLI that is a ratio compared to a threshold each interval | **`time_slice` SLO** | One inlined PromQL, with `operation` + `threshold_value`. |
| Ad-hoc analysis, no SLO or rule | `analyze-telemetry` (MCP) | An array of labelled queries plus `{"selectedMode": "formula", "expression": "(A/B)*100"}` — it composes across logs, traces and metrics. |

> [!WARNING]
> **`selectedMode: "formula"` does not work in an SLO.** The evaluator resolves its
> query through an executor factory that knows `logs`, `metrics` and `traces` and
> returns `unsupported query type: formula` for anything else — on every evaluation,
> so the SLO sits at `no_data` forever. Alerts are the surface with formula support;
> SLOs are not.

**Inline it into one PromQL string instead.** That is what the product does: the SLO
editor's formula builder substitutes each label with its parenthesised query before it
posts, and stores one flat `promql`. So `(A/B)*100` is stored as

```promql
(sum(increase(http_requests_total{status=~"5.."}[5m])) / sum(increase(http_requests_total[5m]))) * 100
```

> [!IMPORTANT]
> **Do not inline a ratio into a `by_count` SLO.** There the ratio *is* the SLO — the
> evaluator computes good/total and builds the error budget from it. Feed it a
> percentage as `total_events_filter` and it counts percentages as events, and every
> number downstream is meaningless. Ratios belong in `time_slice` (one value per
> slice, compared to a threshold) or in an alert rule.

When an inlined ratio is grouped, keep `by (…)` on **both** sides of the division and
a non-empty `groupBy` on the query — `by (…)` alone leaves the SLO on the single-series
path (see Grouping).

## Grouping

Put `groupBy` on `total_events_filter` (and the matching one on
`good_events_filter`) and the SLO splits into one compliance figure per group,
joined on group identity.

- Groups are emitted as Prometheus labels on every `kubesense_slo_*` series, plus a
  pooled overall series labelled `slo_group="*"`.
- `slo_id`, `slo_group`, `window`, `target_percentage`, `error_budget` and
  `__name__` are **reserved** — a groupBy on a field that renders to one of those
  names is dropped. Grouping by `workload`, `namespace` or `cluster` is fine and is
  exactly how you get them onto the series.
- Field names are sanitised to valid Prometheus label names: anything outside
  `[a-zA-Z0-9_]` becomes `_`, so `service.name` → `service_name`.
- **Hard cap of 100 groups.** Past that the evaluator *skips the whole bucket* and
  logs it — the SLO silently stops producing data. Never group by `pod`, `instance`,
  `trace_id` or any unbounded field.
- Groups on the good side that have no matching total group are clamped away, with a
  warning. Keep the two `groupBy` lists identical.
- **A metrics SLI needs a non-empty `groupBy` too.** `by (…)` in the PromQL does not
  switch grouping on by itself: the evaluator reads `total_events_filter.groupBy`, and
  with an empty list a multi-series result is reduced to its **first series**, the rest
  discarded silently. (`time_slice` over metrics is the exception — it always runs
  multi-series.) See
  [references/api-payloads.md](./references/api-payloads.md#grouping-a-metrics-by_count-slo).

## Burn-Rate Alerting Comes From `alert_types`

Set `alert_types` and the API **creates alert rules for you**, inside the same
transaction as the SLO:

| `alert_types` value | Rule | Severity |
|---|---|---|
| `burn_rate_fast` | `kubesense_slo_burn_rate{window="1h"}` over `(days × 24 × 0.02) / 1` | critical |
| `burn_rate_slow` | `kubesense_slo_burn_rate{window="6h"}` over `(days × 24 × 0.05) / 6` | warning |
| `error_budget_critical` | `kubesense_slo_error_budget_balance` < 5 | critical |
| `error_budget_low` | `kubesense_slo_error_budget_balance` < 10 | warning |

Thresholds are derived from `evaluation_window_days`, so a 30-day window gives the
familiar 14.4× / 6× multi-window burn rates. They are recomputed on every update.

> [!WARNING]
> **Never hand-write these rules.** `PUT /api/slo` **deletes every alert rule
> attached to the SLO and rebuilds them** from `alert_types`; `DELETE` removes them.
> An edit to a *generated* rule is silently reverted on the next SLO update.
>
> "Attached" means the rule's **own `labels.slo_id`**, not its PromQL. The delete is
> `WHERE JSON_EXTRACT(labels, '$.slo_id') = <id>`, and it does not care who created
> the rule. So a hand-written rule that merely *selects*
> `kubesense_slo_burn_rate{slo_id="…"}` in its query survives, while one that carries
> `slo_id` in its own labels — the obvious thing to do when copying a generated rule —
> is deleted along with them. Keep `slo_id` out of the labels of any rule you want to
> keep.
>
> `notification_channels` on the SLO is what those generated rules page. Call
> `list-notification-channels` (MCP) or `GET /api/alerts/notification-channels`
> first — a non-existent id fails rule creation and takes the whole create
> transaction down with it.

## Window, Cadence and Backfill

- `evaluation_window_days` is the **rolling** compliance window (7, 30, 90 …).
- `evaluation_time_interval_seconds` is the bucket size — and, for `time_slice`, the
  **slice size**. The UI offers 60 and 300 for slices; they are the same two values
  Datadog offers.
- `evaluate_from` is where evaluation **starts**, and the evaluator backfills from
  there to now in batches of 20 buckets per pass. Setting it months back on a 60s
  interval means tens of thousands of buckets before it catches up to live — set it
  to the start of the window you actually care about.
- `evaluation_start_time` is clamped forward to `evaluate_from` if it is earlier.
- Rollups the UI and `/groups` expose: `last_2_hour`, `last_24_hour`, `last_7_days`,
  `last_28_days`.

## Traps

| Trap | Consequence |
|---|---|
| `evaluation_time_interval_seconds: 0` | 500 on create; an existing 0 makes the evaluator skip the SLO |
| `status` not `"active"` | Stored, listed, and never evaluated |
| `/list` without `status=active` | Empty list that looks like "no SLOs" |
| `/list` or `GET /{id}` without `current_time` | 500 |
| `selectedMode` omitted | **Silently treated as `traces`** — a metrics SLI with only `promql` set queries traces and finds nothing |
| Query-tool field names (`service`, `type`) in `unified_filter` | Errors on every evaluation; the SLO sits at `no_data` |
| `groupBy` resolving to > 100 groups | Every bucket skipped — no data, no error surfaced in the UI |
| `groupBy` lists differing between good and total | Orphaned good groups are clamped; compliance reads as 100% for them |
| Alert SLO with no `alert_ids` | Evaluator skips it (it would otherwise report a flawless 100% forever) |
| `warning_target_percentage` **below** the target | Never warns — warning must be above target |
| `time_slice` `operation` as a long form (`less_than`) or lowercase (`lt`) | Passes API validation, unreadable to the evaluator — **every slice scores as downtime**, 0% forever. Uppercase `GT`/`GTE`/`LT`/`LTE`/`EQ` only |
| `time_slice` `operation: "NEQ"` | Rejected at create, despite being offered in the UI's dropdown |
| Metrics `by_count` with `by (…)` but an empty `groupBy` | Only the **first series** is counted; the rest vanish silently |
| A hand-written rule carrying `slo_id` in its own labels | Deleted on the next `PUT /api/slo` along with the generated ones |
| Alert SLO with `evaluate_from` before its rules existed | Backfills **invented perfect uptime** — it is not recorded as no-data |
| Editing a generated burn-rate rule | Reverted on the next `PUT /api/slo` |
| `PUT` with a partial body | Full replace — unsent fields are written as their zero values |
| `evaluation_window_days` not a multiple of 7 and > 31 (e.g. 90) | Works over the API, but the UI's period input (1–31 × day/week) cannot represent it, so a later edit in the UI fails validation |

## Missing-Data Semantics Differ By Type — Deliberately

- **`by_count`**: an empty denominator is `no_data`. Compliance is not computed, the
  bucket is not scored.
- **`time_slice`**: missing data counts as **uptime**, matching Datadog. A count
  query returning 0 is treated as "no data", so a zero-traffic minute is a good
  slice. This does mean a telemetry outage reads as a healthy SLO.
- **`alert`**: downtime is the union of firing intervals of the named rules; a rule
  still firing at the window edge is counted as firing up to that edge. A bucket with
  **no firing rows at all scores as fully healthy, not as no-data** — so an
  `evaluate_from` earlier than the rules themselves backfills invented perfect uptime
  into the budget. Set `evaluate_from` to when the rules started existing.

Say which one applies when you hand an SLO over. It is the single most common source
of "this number looks wrong".

## Error Budget and Burn Rate

- `error_budget_percentage` = `100 - slo_target_percentage`.
- `error_budget_balance` = `(1 - error% / budget%) × 100`, **unclamped** — a blown
  budget goes negative (99.52% actual against a 99.9% target is −380%), matching
  Datadog. Do not "fix" a negative number; it is the burndown.
- Burn rate is normalised: 1.0 consumes exactly the budget over the window, whatever
  the window's length. The list page's indicator uses the 2h window, critical above
  6 and elevated above 1 — the same thresholds Datadog shows.
- Series emitted: `kubesense_slo_evaluated_events_total` / `_good`,
  `kubesense_slo_evaluated_events_bad_percent`, `kubesense_slo_error_budget_balance`,
  `kubesense_slo_burn_rate` (windows `1h`, `2h`, `6h`), `kubesense_slo_breached`,
  `kubesense_slo_status`, `kubesense_slo_burn_rate_status`. Query them with
  [kubesense-metrics](../kubesense-metrics/SKILL.md).

## Rules

1. Discover real metric and field names first (`get-available-metrics`,
   `get-trace-or-log-fields`). Never invent one.
2. Use the **alert engine's** field vocabulary in `unified_filter` — `app_service`,
   not `service`; `level`, not `type`.
3. Always `POST /api/slo/preview` before creating, and show the user the compliance
   and budget numbers it returns. Preview is free and stores nothing.
4. Set `selectedMode` explicitly on both filters. The default is `traces`.
5. `evaluation_time_interval_seconds > 0` and `status: "active"`, always.
6. Keep `groupBy` identical on good and total, and bounded well under 100 groups — and
   set it even on a metrics SLI, where `by (…)` alone leaves you with one series.
7. Never hand-write burn-rate alert rules — use `alert_types`, and verify the channel
   ids exist first.
8. `PUT` sends the **whole** object; read the SLO back before editing it.
9. `time_slice` operators are uppercase `GT`, `GTE`, `LT`, `LTE`, `EQ`. Nothing else
   works end to end.
10. State the missing-data semantics for the type you built — and for an alert SLO, set
   `evaluate_from` to when its rules started existing.
11. Never claim an SLO was created unless `POST /api/slo` returned an id — and never
   call it working until a real bucket came back with events (step 6).
