---
name: kubesense-traces
description: Query spans and distributed traces via KubeSense MCP — latency percentiles, error rates, the exact trace field catalog (service, role, method, status_code, resource — not app_service/kind/subtype/return_code), duration units, and the distributed-trace waterfall for root-causing which hop broke or burned the time.
metadata:
  version: "2.0.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,traces,apm,spans,latency,p99,distributed-tracing,error-rate,waterfall
---

# KubeSense Traces (APM)

Use for anything about **requests**: latency, p99/p95, error rate, HTTP method, status
code, endpoint, service-to-service calls, downstream dependencies. (Log lines and panics
→ [kubesense-logs](../kubesense-logs/SKILL.md).)

Requires the KubeSense MCP server; see **[kubesense-mcp](../kubesense-mcp/SKILL.md)**.
Tools resolve RBAC against the **`traces`** module.

## Tools

| Tool | Use when |
|---|---|
| `get-trace-or-log-fields` (`signal: "traces"`) | Always, first |
| `analyze-traces` | Latency percentiles, error rates, counts, trends |
| `search-traces` | Read individual spans |
| `get-distributed-trace` | You have a `trace_id` and need the full call chain |

**`get-distributed-trace` is the highest-leverage tool here.** A single span tells you
something failed; the trace tells you *which hop* failed and *where the time went*.

## Field Names — Catalog Labels Only

Storage column names are **rejected** at every input slot.

| Concept | Use this label | Storage column (rejected) |
|---|---|---|
| **service identity** | **`service`** | `app_service` |
| k8s workload | `workload` | — |
| pod | **`instance`** | `pod_name` |
| container | **`container`** | `container_name` |
| **node** | **`node_name`** | — |
| HTTP method | **`method`** | `subtype` |
| HTTP status code | **`status_code`** | `return_code` |
| resource / endpoint | **`resource`** | `clustered_resource` |
| span role | **`role`** | `kind` |
| protocol | **`protocol`** | `protocol_type` |
| span outcome | `status` | — |
| latency | `duration` | — |
| external call? | `request_type` | `is_external` |
| issue reason | `reason` | `issue_reason` |
| customer / tenant | `domain` | `customer_identifier` |
| trace / span id | `trace_id`, `span_id` | — |
| issue id | `issue_id` | — |
| namespace, cluster, region, app_version, env_type, source, server, client, server_namespace, client_namespace, operation_name, partner_cluster | same | — |

Also parse but hidden from discovery: `timestamp` (→ `start_timestamp`), `duration`,
`primary_workload`/`primary_namespace` (→ `perspective_*`),
`associate_workload`/`associate_namespace` (→ `partner_*`).

### `service` vs `workload`

Prefer **`service`** for application identity — it is the cross-platform identifier
(Kubernetes, Docker, legacy). Use `workload` only when you specifically need Kubernetes
topology.

> [!NOTE]
> This is the opposite of the guidance for **alert rules**, where `workload` groups more
> reliably. See [kubesense-alerts](../kubesense-alerts/SKILL.md) — the alert engine
> resolves `service` against a rollup column that is only populated for
> SDK-instrumented services.

> [!WARNING]
> **`node` is not valid on traces** — it is `node_name`. (Logs are the reverse: `node`,
> not `node_name`.) Never carry a field name across signals.
>
> **There is no `body` field on traces.** Text search over a message is logs-only.

### Enum values are lowercase on traces

| Field | Values |
|---|---|
| `status` | `error`, `ok` |
| `role` | `server`, `client` |
| `protocol` | `HTTP`, `gRPC`, `TCP`, `MongoDB`, `Redis`, `MySQL`, `PostgreSQL` |
| `method` | `GET`, `POST`, `PUT`, `DELETE`, `PATCH` |
| `source` | `eBPF`, `OTel` |
| `status_code` | `200`, `400`, `401`, `403`, `404`, `500`, `502`, `503`, `504` |

`status = error` — lowercase, unlike logs' UPPERCASE `type = ERROR`.

`status_code` is a **string** field, so its values stay quoted strings even when they look
numeric: `status_code IN (500, 502)` yields the strings `"500"`, `"502"`. Range
comparisons therefore do not work — enumerate the codes, or use
`status_code LIKE "5%"` for a class.

Read casing from the `enum_values` column, not `example` — the example generator returns
a blank cell for `method`, `protocol`, and `status_code`.

## Duration: ms in, ns out

> [!IMPORTANT]
> **Filtering `duration` takes MILLISECONDS. Aggregating `duration` returns NANOSECONDS.**
> These are different units in the same field, and getting it wrong is silent.

```
where: "duration > 500"        →  spans slower than 500 milliseconds
```

The parser multiplies your value by 1e6 to reach the nanosecond storage column. So:

| You want | Write |
|---|---|
| slower than 250ms | `duration > 250` |
| slower than 1s | `duration > 1000` |
| slower than 1.5s | `duration > 1.5e3` or `duration > 1500` |

> [!WARNING]
> The `search-traces` tool description shows `"duration > 250000"` as an example. That is
> **wrong** — it means 250,000 ms = 250 seconds and will match nothing. Ignore it.

Aggregation is the other direction — `p95`/`avg`/`max` over
`fields: [{"field": "duration"}]` come back in **nanoseconds**:

| Result | Means |
|---|---|
| `250000000` | 250 ms |
| `1000000000` | 1 s |

Divide by 1e6 to report milliseconds. There is no `duration_ms` field at the MCP layer —
it is rejected as an unknown field.

## Trace attributes: group-by only

> [!WARNING]
> **`@attr` in a traces WHERE clause does not work.** It is rejected with
> `unknown field "<key>" for signal=traces`, because the parser clears the attribute
> discriminator during the ARRAY_MAP remap and the field then fails column validation.
> The tool descriptions advertise `@db.system = postgresql` as working; it does not.

Trace attributes **do** work everywhere the field is passed structurally — set the flag
instead of a prefix:

```json
"group_by_fields": [ { "field": "db.system", "is_attribute": true } ]
```

Valid in `group_by_fields`, `fields`, `required_fields`, and `sort_by`. To filter by an
attribute value, group by it and read the series labels, or filter on an equivalent
top-level column.

(Log attributes are unaffected — `@user.id = abc` works fine on logs.)

## analyze-traces

```json
{
  "from_time": "2026-07-30T10:00:00Z",
  "to_time": "2026-07-30T11:00:00Z",
  "query_type": "range",
  "group_by_fields": [ { "field": "service", "is_attribute": false } ],
  "fields": [ { "field": "duration", "is_attribute": false } ],
  "value_operation": "p95"
}
```

`value_operation`: `row_count`, `unique_count`, `avg`, `sum`, `min`, `max`, `p50`, `p90`,
`p95`, `p99`. **`count` is not valid — it is `row_count`**, despite what the schema's
summary line suggests.

| Question | Shape |
|---|---|
| p95 latency by service, over time | `range`, group `service`, `fields: [duration]`, `p95` |
| top 5 services by errors, now | `instant`, `where: "status = error"`, group `service`, `row_count`, `sort_direction: DESC`, `limit: 5` |
| errors by status code | `instant`, `where: "status = error"`, group `status_code`, `row_count` |
| slowest endpoints | `instant`, group `resource`, `fields: [duration]`, `p99`, `sort_direction: DESC` |
| server-side only | add `where: "role = server"` — otherwise client spans double-count |

**Error rate as a percentage** needs two queries plus a formula → `analyze-telemetry`.
See [kubesense-mcp](../kubesense-mcp/SKILL.md).

Output is columnar JSON: for `range`, one shared `timestamps` array plus a positionally
aligned `values` array per series; for `instant`, one scalar `value` per series.

## search-traces

Same input shape as `search-logs`. Output is TSV with a
`# total_count=<N> is_free_search=<bool>` header.

### Pagination — and its hard limit

Page by narrowing `to_time` to the **minimum `start_timestamp`** returned (not
`timestamp`, which is the span's *end* time; `start_timestamp` is the sort and filter
key). The window is half-open, so the cursor row is not repeated.

> [!WARNING]
> **Exhaustive paging is not achievable for traces.** Rows are ordered
> `toStartOfHour(start_timestamp) DESC, observation_point DESC, cluster DESC,
> start_timestamp DESC`. Both `observation_point` **and** `cluster` outrank the timestamp,
> so pinning `clusters` alone is not enough — spans at other observation points in the
> same hour get skipped. And `observation_point` **is not in the trace field catalog**, so
> the `where` clause cannot pin it (the tool description suggests
> `"observation_point = s-app"`; that is rejected as an unknown field).
>
> Practical consequences: keep the window short enough that `total_count` fits in one
> page, or use `analyze-traces`. Treat any paged trace scan as a sample.

Touching `duration`, `trace_id`, `span_id`, or any attribute sets `is_free_search` and
routes to the raw table — slower, no rollups.

## get-distributed-trace

The span tree for one request. Start here when investigating a failing or slow request.

```json
{
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "from_time": "2026-07-30T10:20:00Z",
  "to_time": "2026-07-30T10:40:00Z",
  "max_spans": 200
}
```

`trace_id`, `from_time`, `to_time` are all **required**. The window must *contain* the
trace's `start_timestamp` — traces are time-partitioned, so a window that misses it finds
nothing. Use ~10 minutes either side. `max_spans` defaults to 200, max 500.

> [!NOTE]
> Key on `trace_id`, not a span's `kuid`. One trace has many spans; they all share the
> `trace_id`.

### Reading the output

**Block 1** — one row per span in preorder (a span is immediately followed by its
children), with a `tree` column drawing the call chain. Key columns:

| Column | Read it for |
|---|---|
| `tree` | who called whom |
| `status` / `return_code` | which span failed |
| `duration_us` | total span time in **microseconds**, including everything it called |
| `self_time_us` | time in **this** service, excluding children — the bottleneck ranking |
| `start_time` / `end_time` | RFC3339 ms — paste straight into `search-logs` |
| `workload` / `namespace` / `cluster` | scope for follow-up log/metric queries |
| `resource_name` / `protocol_type` / `subtype` | what was called |

**Block 2** — `## services`, one row per (cluster, workload), **ordered worst-first** by
errors then self time. Read this *before* the span rows to pick your suspect. It always
covers every span, even when block 1 was truncated.

### Two diagnostic rules

- **A trace with no error may still be the problem.** The top row of `## services` is the
  hop that burned the time.
- **Large `duration_us` + small `self_time_us` = the service was waiting, not working.**
  Investigate what it called (its children), not the service itself. Conversely, if a span
  errored but every child succeeded, the fault is *in* that service.

`namespace` may be blank when spans are attributed to a collector agent rather than the
workload's pod; take it from a span row that has one, or from `get-workload-detail`.
Rarely it lists several joined by `|`, meaning that cluster runs the same workload name in
more than one namespace.

## Investigation Flow

```
1. get-distributed-trace(trace_id, ±10min)   → the call chain, errors marked
2. read "## services"                        → who owns the errors / the time
3. search-logs                               → scoped to that workload + the failing
                                               span's start_time/end_time (widen a few s)
4. get-recent-changes / get-infra-issues     → why: deploy, OOM, probe failure
5. analyze-metrics                           → confirm resource pressure
```

Steps 4–5 use [kubesense-infra](../kubesense-infra/SKILL.md) and
[kubesense-metrics](../kubesense-metrics/SKILL.md).

## Rules

1. `get-trace-or-log-fields` with `signal: "traces"` first, same window as the query.
2. Catalog labels only: `service`, `instance`, `method`, `status_code`, `resource`,
   `role`, `protocol`. Never `app_service`, `pod_name`, `subtype`, `return_code`,
   `clustered_resource`, `kind`, `protocol_type`.
3. `node_name` on traces, `node` on logs. Never carry a field across signals.
4. Prefer `service` over `workload` for app identity — but the *alert engine* prefers
   `workload`.
5. **`duration` in WHERE is milliseconds; aggregated `duration` is nanoseconds.** Divide
   results by 1e6 to report ms. `duration_ms` does not exist here.
6. `@attr` filters do **not** work on traces. Use `is_attribute: true` in
   `group_by_fields`/`fields` instead.
7. Enum values are lowercase (`status = error`, `role = server`); `status_code` is a
   string, so enumerate codes or use `LIKE "5%"` rather than a range.
8. `value_operation` is `row_count`, not `count`.
9. Add `role = server` when counting requests, or client spans double-count.
10. `get-distributed-trace` needs a window containing the trace's start; widen it first if
    nothing is found.
11. Don't try to page traces exhaustively — `observation_point` can't be pinned. Shorten
    the window or aggregate.
