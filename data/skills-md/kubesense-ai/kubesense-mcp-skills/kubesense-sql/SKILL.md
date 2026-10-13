---
name: kubesense-sql
description: Run raw ClickHouse SQL against KubeSense logs and traces via execute-sql / validate-sql — the queryable column set, the $__timeFilter/$__clusters macros, @attr access, and the joins, CTEs and window functions the analyze-* tools cannot express.
metadata:
  version: "2.0.1"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,sql,clickhouse,logs,traces,query,observability,mcp
---

# KubeSense SQL

Requires the KubeSense MCP server; see **[kubesense-mcp](../kubesense-mcp/SKILL.md)** for
connection and auth. Tools here resolve RBAC against the **`logs`** or **`traces`** module,
matching the `signal` you pass.

## Tools

| Tool | Use when | Returns |
|---|---|---|
| `get-trace-or-log-fields` | Always, first | Field catalog for your window |
| `validate-sql` | Before running anything non-trivial | `valid=true/false` + the SQL that would run |
| `execute-sql` | The query is right | Result rows as TSV |

Both SQL tools take the same arguments: `signal` (`"logs"` or `"traces"`), `query`,
`from_time`, `to_time`, and optional `clusters`.

## Use SQL Only When analyze-* Cannot

`analyze-logs` / `analyze-traces` cover filter → group → aggregate, which is most
questions. They are cheaper, their arguments are checked more strictly, and their output
is smaller. Reach for SQL only when the shape genuinely does not fit:

| Question shape | Tool |
|---|---|
| count / rate / p95 / top-N, grouped | `analyze-logs`, `analyze-traces` |
| two metrics divided (error rate %) | `analyze-telemetry` with a formula |
| read individual rows | `search-logs`, `search-traces` |
| **join two result sets** | **SQL** |
| **CTE chain / multi-step derivation** | **SQL** |
| **window function** (`row_number`, `lag`, running total) | **SQL** |
| **arithmetic between two aggregates in one pass** | **SQL** |
| **`UNION`, `DISTINCT ON`, `argMax`, `quantileIf`** | **SQL** |
| **compare two time ranges in one result** | **SQL** |

If you find yourself writing `SELECT field, count(*) ... GROUP BY field`, stop — that is
`analyze-*` with `value_operation: row_count`.

### A filter condition is never the reason to use SQL

The `where` argument of `search-*` / `analyze-*` is the same language as the **Advanced**
query tab on the Logs and Traces pages. If a condition can be written there, write it
there — the server rewrites `body` searches to the text-index form and routes
column-only filters to the pre-aggregated rollup tables. SQL does neither: it always
reads the raw table and runs your predicate as typed.

Decide in this order:

1. Can the **condition** be written as a `where` string — `=` `!=` `<` `>` `LIKE` `ILIKE`
   `SUBSTR_ILIKE` `IN`, `AND` / `OR` / `NOT`, `@attr` filters, `body ILIKE "%…%"`? →
   `search-*` / `analyze-*`. This covers nearly every "find / count lines where …".
2. Is it only the **shape of the result** that does not fit (join, CTE, window function,
   arithmetic across aggregates)? → SQL, keeping the same conditions and following
   *Searching Log Text* below for anything on `body`.
3. Does the condition itself need something the `where` language lacks — a regex, a
   comparison between two columns, a function of a column? → SQL, with an indexed
   predicate alongside it to narrow the scan first (a `workload` / `namespace` equality,
   or a `hasToken(lower(body), …)` for a word the regex must contain).

Several values for one field is `IN` or `OR` in the `where` string, not a reason for SQL.

## Tables

| Write | Reads |
|---|---|
| `FROM logs` | the logs table |
| `FROM traces` | the traces table |

Nothing else is addressable. A database-qualified name (`kube_logs.logs_combined`) is
rejected outright — this is the first thing that breaks when pasting a query from another
SQL tool. `signal` must match the table you select `FROM`.

## Field Names

**Same catalog labels as every other KubeSense tool** — the set
`get-trace-or-log-fields` returns. Storage column names are rejected:

| Write | Not |
|---|---|
| `type` | `level` |
| `instance` | `pod_name` |
| `container` | `container_name` |
| `domain` | `cluster` (see below), `customer_identifier` |
| `service` | `app_service` |
| `role` | `kind` |
| `status_code` | `return_code` |
| `method` | `subtype` |
| `resource` | `clustered_resource` |
| `reason` | `issue_reason` |
| `request_type` | `is_external` |
| `timestamp` | `start_timestamp` |
| `duration_ms` | `duration` |

`SELECT *` expands to the catalog columns, not the raw table.

### SQL accepts four things discovery does not list

`get-trace-or-log-fields` hides fields flagged non-filterable, but SQL still takes them.
Do not conclude a name is invalid because discovery omitted it:

| Field | Signal | Note |
|---|---|---|
| `timestamp` | both | **Not listed by discovery**, yet every query needs it for `$__timeFilter(timestamp)` |
| `duration_ms` | traces | Milliseconds. Discovery would show `duration` (nanoseconds) — SQL **rejects** that name |
| `primary_namespace`, `primary_workload` | traces | The perspective columns |
| `body_length` | logs | Computed as `length(body)` |

Also queryable but not catalog fields: `cluster` (same column as `domain`, and what
`$__clusters` expands to), plus the raw attribute containers — `string_attributes` /
`float_attributes` on logs, `attribute_names` / `attribute_values` on traces.

> [!WARNING]
> **`duration` vs `duration_ms` is the trap that bites hardest.** `analyze-traces` takes
> `duration` in nanoseconds. SQL takes `duration_ms` in **milliseconds** and rejects
> `duration` entirely. A threshold carried across from an analyze call is off by 10⁶.

## Macros

Expanded server-side before the query runs.

| Macro | Becomes |
|---|---|
| `$__timeFilter(timestamp)` | the `from_time` / `to_time` window |
| `$__fromTime` / `$__toTime` | the bounds as scalars, for use in expressions |
| `$__clusters` | the cluster filter; `1=1` when `clusters` is empty |

```sql
SELECT workload, count(*) AS cnt
FROM logs
WHERE $__timeFilter(timestamp) AND $__clusters AND type = 'ERROR'
GROUP BY workload ORDER BY cnt DESC
```

`$__timeFilter` takes the **column name** `timestamp` on both signals. Plain SQL time
predicates work too (`WHERE timestamp >= now() - INTERVAL 1 HOUR`), but the macro keeps
the query aligned with the window you passed.

> [!NOTE]
> String values in SQL use **single quotes** (`type = 'ERROR'`), unlike the `where`
> argument of the analyze/search tools, which uses bare words or double quotes. Enum
> casing is unchanged: `ERROR` uppercase on logs, `error` lowercase on traces `status`.

## Custom Attributes

`@`-prefixed, as everywhere else. `@http.status_code`, or `@"key.with spaces"`.

```sql
SELECT @http.status_code, count(*) AS cnt
FROM logs
WHERE $__timeFilter(timestamp) AND @http.status_code != ''
GROUP BY 1 ORDER BY cnt DESC
```

Attributes are stored as strings — cast before comparing numerically:

```sql
WHERE toFloat64OrNull(@latency_ms) > 500
```

> [!WARNING]
> **Attribute names are never validated — by any tool, at any stage.** `@` expressions
> are compiled into a map lookup before the query is even parsed, so a misspelled key is
> not an error: it yields `NULL` on logs and `''` on traces. `validate-sql` will report
> `valid=true`. A query returning all-empty values for one column almost always means the
> attribute key is wrong, not that the data is missing. Confirm every key with
> `get-trace-or-log-fields` first.

## Searching Log Text (`body`)

> [!CAUTION]
> **In SQL, a predicate on bare `body` scans every log line in the window.** The body
> indexes are built on `lower(body)`. `body LIKE`, `body ILIKE`, `position(body, …)`,
> `match(body, …)` — and `position(lower(body), …)` — match no index, so the query
> decompresses the whole message column. On a production cluster a multi-day search
> written this way has read terabytes and stalled ingestion for everyone.

`search-logs` and `analyze-logs` rewrite `body ILIKE "…"` to the indexed form for you.
**SQL does not** — it runs the predicate exactly as written. So prefer those tools for
"find lines containing X", and when the search has to live inside SQL, write one of:

| Looking for | Write | Index |
|---|---|---|
| one word or ID | `hasToken(lower(body), 'abc123')` | text index — best |
| any of several | `hasAnyTokens(lower(body), ['abc123', 'def456'])` | text index |
| all of several | `hasAllTokens(lower(body), ['connection', 'refused'])` | text index |
| exact substring, punctuation included | `lower(body) LIKE '%connection refused%'` | n-gram filter |

- **Lowercase the needle.** The index holds lowercased text; `hasToken(lower(body), 'OOM')`
  matches nothing.
- A token is a run of letters and digits. `hasToken` takes exactly one — `'node-agent'`
  or `'a b'` is an error. Split on the punctuation and use `hasAllTokens`, or fall back to
  `lower(body) LIKE`.
- `hasAllTokens` means "contains all these words", not "contains this phrase". Add a
  `lower(body) LIKE '%…%'` alongside it only when adjacency matters.
- Tokens must be whole: `hasToken(lower(body), 'timeo')` does not match `timeout`. For a
  partial word, use `lower(body) LIKE '%timeo%'`.

```sql
SELECT toDate(timestamp) AS d, workload, count(*) AS n
FROM logs
WHERE $__timeFilter(timestamp) AND $__clusters
  AND hasAnyTokens(lower(body), ['6abffe8am1sw6', '636ce0fe6khta'])
GROUP BY d, workload ORDER BY d, n DESC
```

Measured on one hour of a production cluster (9,640 granules after time pruning):
bare `body LIKE '%…%'` read all 9,640; `lower(body) LIKE` 213; `hasToken` 202.

**Narrow before you widen.** Add `workload` / `namespace` / `type` when you know them and
start with an hour, not days. Run **one** body search at a time — do not fan the same
search out across time slices in parallel; each one competes with ingestion for the same
disk. `validate-sql` cannot warn you: an unindexed body scan is perfectly valid SQL.

## validate-sql

Call it before `execute-sql` for anything with a CTE, a join, or a field you have not used
before. It scans no data, so it is cheap to call repeatedly.

It checks two things:

1. **The rewrite** — parse, single statement, `SELECT` only, table access, blocked
   functions, and column names. The column check covers **bare column references in the
   top-level SELECT list only**, and is skipped entirely when the query has a `WITH` clause.
2. **ClickHouse's own analysis** of the rewritten query, which resolves every identifier.
   This is what catches a bad column in `WHERE`, `GROUP BY`, or inside a CTE.

On success it returns the SQL that would actually run, under `## rewritten_sql`. **Read
it.** It shows which storage column each label resolved to (`level AS type`,
`pod_name AS instance`), which is the only way to confirm you addressed the field you
meant — and the fastest way to catch a name that quietly resolved to something else.

## Reading the Output

`execute-sql` returns TSV: a `# signal=… rows=N` line, then a header row of **your own
SELECT columns in your own order**, then one row per result.

```
# signal=logs rows=2
workload	cnt
checkout	412
payments	87
```

An empty result is the header line alone. That means the query ran and matched nothing —
it is not a failure, and rewriting the query is usually the wrong response. Check the
window and the cluster filter first.

## Limits

- **1000 rows** unless the query carries its own `LIMIT`. Aggregate in SQL rather than
  pulling rows back to count them.
- Execution is read-only. `INSERT` / `ALTER` / `DROP`, multiple statements, and functions
  that reach outside the table (`sleep`, `url`, `s3`, `file`, `remote`, `mysql`) are
  rejected.
- The cluster filter is applied at the table scan and cannot be bypassed by the query.

> [!WARNING]
> **Both tools are unavailable to scope-restricted roles.** If the API key or role is
> limited to specific clusters, namespaces, or workloads, the call is refused — the SQL
> layer applies a cluster filter only and cannot enforce namespace or workload rules. Use
> `search-*` / `analyze-*`, which do. The refusal message says so; do not retry, and do
> not try to express the scope in the SQL yourself.

## Worked Examples

**Compare this hour against the same hour yesterday, in one result**

```sql
SELECT service,
       countIf(timestamp >= $__toTime - INTERVAL 1 HOUR) AS now_errors,
       countIf(timestamp <  $__fromTime + INTERVAL 1 HOUR) AS then_errors
FROM traces
WHERE $__timeFilter(timestamp) AND $__clusters AND status = 'error'
GROUP BY service HAVING now_errors > then_errors ORDER BY now_errors DESC
```

**Slowest endpoint per service (window function)**

```sql
SELECT service, resource, p95_ms FROM (
  SELECT service, resource, quantile(0.95)(duration_ms) AS p95_ms,
         row_number() OVER (PARTITION BY service ORDER BY quantile(0.95)(duration_ms) DESC) AS rn
  FROM traces
  WHERE $__timeFilter(timestamp) AND $__clusters AND role = 'server'
  GROUP BY service, resource
) WHERE rn = 1 ORDER BY p95_ms DESC
```

**Workloads that logged an error but served no failing span (CTE join)**

```sql
WITH bad_logs AS (
  SELECT DISTINCT workload FROM logs
  WHERE $__timeFilter(timestamp) AND $__clusters AND type = 'ERROR'
)
SELECT workload FROM bad_logs
```
then a second `traces` query — the two signals are **separate tables and cannot be joined
in one statement**. Correlate the results yourself, or use `analyze-telemetry`, which
combines signals in one call.

More patterns: [references/recipes.md](references/recipes.md).

## Rules

1. Try `analyze-*` first. Use SQL only for joins, CTEs, window functions, or arithmetic
   across aggregates. If the condition can be written as a `where` string (the Advanced
   query language), it does not belong in SQL.
2. Call `get-trace-or-log-fields` for the window before writing the query.
3. `validate-sql` before `execute-sql` for anything non-trivial, and **read the
   `rewritten_sql`** it returns.
4. `FROM logs` / `FROM traces` only, matching `signal`. Never a database-qualified name.
5. Catalog labels, never storage columns: `type` not `level`, `instance` not `pod_name`,
   `service` not `app_service`, `domain` not `customer_identifier`.
6. `duration_ms` (milliseconds) on traces. `duration` is rejected — do not carry a
   nanosecond threshold over from `analyze-traces`.
7. `timestamp` is valid on both signals even though discovery does not list it.
8. Single quotes for string values — SQL, not the `where` mini-language.
9. Attribute keys are never validated. All-empty column = wrong key, not missing data.
10. An empty result set is an answer. Check the window before rewriting the query.
11. Aggregate in SQL; never paginate rows to compute a total. 1000-row cap.
12. Logs and traces cannot be joined in one statement — they are different tables.
13. If the call is refused for a scoped role, switch to `search-*` / `analyze-*`.
14. Never filter on bare `body` in SQL. Use `hasToken` / `hasAnyTokens` / `hasAllTokens`
    on `lower(body)` with a lowercased needle, or `lower(body) LIKE '%…%'` — anything
    else is a full scan of the message column.
15. One body search at a time, on the narrowest window and filters that answer the
    question. Never run them in parallel.
