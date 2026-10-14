---
name: kubesense-logs
description: Search and aggregate Kubernetes logs via KubeSense MCP — the exact log field catalog (type, instance, container, node — not level/pod_name/host), WHERE syntax, body text search, counts and percentiles, and window-based pagination.
metadata:
  version: "2.0.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,logs,search,clickhouse,observability,errors,log-analysis
---

# KubeSense Logs

Requires the KubeSense MCP server; see **[kubesense-mcp](../kubesense-mcp/SKILL.md)** for
connection, auth, and the shared WHERE-clause reference. Tools here resolve RBAC against
the **`logs`** module.

## Tools

| Tool | Use when | Returns |
|---|---|---|
| `get-trace-or-log-fields` (`signal: "logs"`) | Always, first | Field catalog for your window |
| `search-logs` | You want to *read* individual log lines | Up to `page_size` rows (default 10) |
| `analyze-logs` | You want counts, rates, trends, percentiles | Aggregated series |

**Reading rows to compute a total is the most common mistake.** If the question is "how
many", "how often", or "which is worst", use `analyze-logs` — one call over the whole
window beats paginating raw rows, and is more accurate.

## Field Names — Catalog Labels Only

The server **rejects storage column names** at every input slot (`where`,
`required_fields`, `group_by_fields`, `fields`, `sort_by`) with:

```
field "pod_name" is a storage column; use the catalog label "instance" instead
```

| Concept | Use this label | Storage column (rejected) |
|---|---|---|
| log severity | **`type`** | `level` |
| pod | **`instance`** | `pod_name` |
| container | **`container`** | `container_name` |
| node / host | **`node`** | `host` |
| workload | `workload` | — |
| namespace | `namespace` | — |
| cluster | `cluster` | — |
| log message | `body` | — |
| log format | `format` | — |
| source | `source` | — |
| region | `region` | — |
| app version | `app_version` | — |
| environment | `env_type` | — |

That is the complete set of 13 fields `get-trace-or-log-fields` advertises for logs.
Three more parse but are hidden from discovery: `timestamp`, `pattern_id`, `body_length`.

> [!WARNING]
> **There is no `service` field on logs.** `service` exists only on traces
> (→ `app_service`). `service = checkout` against logs returns
> `unknown field "service" for signal=logs`. Use `workload` for the application name.
>
> **`node` on logs, `node_name` on traces.** The two signals disagree — logs use `node`
> (→ `host`), traces use `node_name`. Carrying a field name across signals is a
> predictable failure.

### Enum values are UPPERCASE on logs

`type` accepts exactly: `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`, `FATAL`, `PANIC`.
Casing is significant — `type = error` matches nothing.

(Traces use lowercase `status = error`. The two signals differ in both the field name
*and* the casing.)

`format` accepts `json`, `klog`, `nginx` — lowercase.

> [!NOTE]
> Read casing off the **`enum_values`** column of `get-trace-or-log-fields`, not the
> `example` column. The example generator misses several enum fields (including `type`)
> and returns a blank cell for them. `enum_values` is always correct.

## WHERE Syntax

```
type = ERROR AND namespace = production
type IN (ERROR, FATAL) AND workload = checkout
NOT (env_type = dev)
body ILIKE "%timeout%"
@user.id = abc-123
```

Operators the WHERE parser actually accepts: `=` `!=` `<` `>` `<=` `>=` `LIKE` `ILIKE`
`SUBSTR_ILIKE` `IN`, combined with `AND` / `OR` / `NOT` and parentheses.

> [!WARNING]
> The `operators` column of `get-trace-or-log-fields` **over-advertises**. `HAS_TOKEN`,
> `HAS_ALL`, `HAS_ANY`, `LIKE_AND`, `ILIKE_LOG`, `IS_IP_ADDRESS` appear in the legend but
> have **no WHERE-string syntax** — `body HAS_TOKEN oom` fails to parse. Stick to the
> list above.

**Quoting.** Bare values may contain only letters, digits, `_`, `.`, `-`. Anything with a
slash, colon, `%`, or space **must be double-quoted**:

```
body ILIKE "%connection refused%"      ✓
timestamp > "2026-07-30T10:00:00Z"     ✓
body ILIKE %timeout%                   ✗ parse error
```

**`NOT IN` does not parse as a leaf.** Write `NOT (namespace IN (kube-system, default))`.

**Attributes** carry an `@` prefix in WHERE and work correctly on logs:

```
@user.id = abc-123
@http.status_code > 400
```

Attribute operators: `=` `!=` `IN` `<` `>` `<=` `>=` `LIKE` `ILIKE`. Unquoted numeric
attribute values are coerced to numbers, so `@latency > 100` compares numerically.

> [!WARNING]
> `exist(@field)` is **broken** on both signals — it emits an `EXIST` operator carrying a
> value, which the validator rejects (`operator "EXIST" takes no values (got 1)`). There
> is no working existence check. Filter on a concrete value instead.

In `group_by_fields` / `fields` / `required_fields` / `sort_by` there is **no `@`** — set
the flag instead:

```json
{ "field": "user.id", "is_attribute": true }
```

## search-logs

```json
{
  "from_time": "2026-07-30T10:00:00Z",
  "to_time": "2026-07-30T11:00:00Z",
  "where": "type = ERROR AND namespace = production",
  "required_fields": [
    { "field": "instance", "is_attribute": false },
    { "field": "body", "is_attribute": false }
  ],
  "page_size": 50
}
```

Output is TSV: a `# total_count=<N> error_count=<N> is_free_search=<bool>` line, a header
row, then one row per log. `total_count` is for the **whole window**, ignoring
`page_size` — compare it to the rows you received to know whether more exist.

### Pagination is window-based

There is **no `page` or `offset` parameter.** The window is half-open
(`from_time <= timestamp < to_time`), so you page by narrowing `to_time`:

1. Query your real window.
2. Take the **minimum** `timestamp` among the returned rows — do not assume the last row
   is the oldest.
3. Call again with the same `from_time` and `where`, and `to_time` = that minimum,
   copied verbatim.
4. Stop when a call returns fewer rows than `page_size`, or the answer is settled.

Timestamps are RFC3339 UTC with **millisecond** precision. Copy the cell exactly —
truncating to whole seconds re-reads or skips rows within that second.

> [!IMPORTANT]
> **A paged scan is a sample, not a census.** Rows are ordered
> `toStartOfHour(timestamp) DESC, cluster DESC, timestamp DESC` — hour-bucket first, then
> cluster. When one hour holds more matching rows than `page_size` across several
> clusters, advancing `to_time` can skip rows in a cluster the scan hadn't reached. To
> read exhaustively, pin `clusters` to a single cluster and use a large `page_size`.
> Otherwise prefer a bigger `page_size` over more pages, and `analyze-logs` over
> pagination for anything aggregate.

### `is_free_search`

Touching `body`, `trace_id`, `span_id`, or any attribute routes the query to the raw
table instead of the pre-aggregated rollups — slower, but the only way to see message
text. It is computed automatically and reported in the output header. Column-only
filters stay on the fast rollup path.

`body ILIKE "…"` here is rewritten server-side to use the body text index. Raw SQL gets
no such rewrite, so do not move a message search into `execute-sql` unless the shape
needs it — and if it does, follow *Searching Log Text* in
[kubesense-sql](../kubesense-sql/SKILL.md).

## analyze-logs

```json
{
  "from_time": "2026-07-30T10:00:00Z",
  "to_time": "2026-07-30T11:00:00Z",
  "query_type": "range",
  "where": "type = ERROR",
  "group_by_fields": [ { "field": "workload", "is_attribute": false } ],
  "value_operation": "row_count",
  "sort_direction": "DESC",
  "limit": 10
}
```

- `query_type`: `range` for a time series, `instant` for one number per series.
- `value_operation`: `row_count`, `unique_count`, `avg`, `sum`, `min`, `max`, `p50`,
  `p90`, `p95`, `p99`.
- `fields` supplies the operand for everything except `row_count`:
  `unique_count` of pods → `value_operation: "unique_count"`,
  `fields: [{"field": "instance"}]`.
- `limit` caps series on `range` queries (top-N by max value, default 20); ignored for
  `instant`.

> [!WARNING]
> `value_operation: "count"` is **not valid** — the correct name is `row_count`. The tool
> schema's own summary line says "Common: count, avg, …", which is wrong.

`body` cannot be used in `group_by_fields` (it doesn't exist on the rollup tables). It is
a filter-only field. Group by `pattern_id` if you want to cluster similar messages.

### Output shape

Columnar JSON keyed by query label (`"A"`). For `range`, a single shared `timestamps`
array (Unix seconds) is emitted once and each series carries a positionally-aligned
`values` array (`null` = no data in that bucket). For `instant`, each series carries one
scalar `value`. `total_series`/`truncated` report how many non-zero series existed before
the top-N cap.

## Worked Examples

**Error count per workload, last hour, as a trend**
`query_type: range`, `where: "type = ERROR"`,
`group_by_fields: [{"field":"workload"}]`, `value_operation: row_count`

**How many distinct pods logged a fatal error right now**
`query_type: instant`, `where: "type = FATAL"`, `value_operation: unique_count`,
`fields: [{"field":"instance"}]`

**Read the actual timeout messages**
`search-logs`, `where: 'body ILIKE "%timeout%" AND workload = checkout'`,
`required_fields: [{"field":"instance"},{"field":"body"}]`, `page_size: 50`

**Error rate as a percentage** — needs two queries plus a formula, so use
`analyze-telemetry`; see [kubesense-mcp](../kubesense-mcp/SKILL.md).

## Rules

1. Call `get-trace-or-log-fields` with `signal: "logs"` first, passing the **same window**
   you will query — attribute keys are window-scoped.
2. Use catalog labels: `type`, `instance`, `container`, `node`. Never `level`, `pod_name`,
   `container_name`, `host`.
3. There is no `service` field on logs — use `workload`.
4. `type` values are UPPERCASE (`ERROR`, not `error`). Read casing from `enum_values`,
   never from `example`.
5. Quote any value containing `/`, `:`, `%`, or a space.
6. `NOT (x IN (...))`, not `x NOT IN (...)`.
7. Stick to `=  !=  <  >  <=  >=  LIKE  ILIKE  SUBSTR_ILIKE  IN` — the advertised
   token/index operators have no WHERE syntax.
8. `value_operation` is `row_count`, not `count`.
9. `analyze-logs` for counts and trends; `search-logs` only to read messages. Never
   paginate to compute an aggregate.
10. Page by narrowing `to_time` to the **minimum** timestamp returned; there is no offset.
    Treat multi-cluster paged scans as samples unless you pin one cluster.
11. `body` is filter-only — it cannot be a group-by.
