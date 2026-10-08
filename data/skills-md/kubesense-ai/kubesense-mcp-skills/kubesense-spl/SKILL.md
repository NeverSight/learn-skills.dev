---
name: kubesense-spl
description: Write, validate and run KubeSense SPL — the piped log query language — via validate-spl and execute-spl. Covers the storage-name field contract that inverts every other KubeSense surface, log_processed attributes, the command and aggregation vocabulary, and why an SPL query can compile and still fail.
metadata:
  version: "2.0.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,spl,logs,query,search,pipeline,observability,mcp
---

# KubeSense SPL

Requires the KubeSense MCP server; see **[kubesense-mcp](../kubesense-mcp/SKILL.md)** for connection
and auth. Tools here resolve RBAC against the **`logs`** module.

**SPL is logs only.** There is no SPL for traces or metrics — use
[kubesense-traces](../kubesense-traces/SKILL.md) and
[kubesense-metrics](../kubesense-metrics/SKILL.md).

## Tools

| Tool | Use when | Returns |
|---|---|---|
| `get-trace-or-log-fields` (`signal: "logs"`) | To find dynamic attribute keys — **not** column names, see below | Field catalog for your window |
| `validate-spl` | Before handing any query over | `valid` + the ClickHouse SQL it compiles to |
| `execute-spl` | To answer a question yourself | Rows (TSV), capped at 1000 |

**Validate before you execute.** SPL's parser accepts an unknown field and an unknown function alike,
so a wrong name compiles and fails at run time — after the scan has already been paid for.
`validate-spl` costs no scan, so the pair is cheap in that order and wasteful in the other.

`execute-spl` needs `clusters` and a time window; `validate-spl` needs neither. Prefer `search-logs`
or `analyze-logs` when they can express the question — they enforce namespace- and workload-level
access rules the SPL endpoints cannot, which is also why both SPL tools are refused outright for a
scope-restricted role.

## Field Names Are the Opposite of Everywhere Else

Every other KubeSense surface — `search-logs`, `analyze-logs`, the SQL endpoints, the field catalog —
takes **catalog labels** and rejects storage column names. SPL does the reverse.

| SPL uses | Every other tool uses |
|---|---|
| **`level`** | `type` |
| **`pod_name`** | `instance` |
| **`cluster`** | `domain` |
| **`container_name`** (or `container`) | `container` |
| **`node_name`** (or `node`) | `node` |
| `host` | — a *different* column from `node_name`; both exist |

The complete set SPL knows: `timestamp` (or `@timestamp`) · `body` (or `@message`) · `level` ·
`cluster` · `namespace` · `workload` · `pod_name` (or `@logstream`) · `container_name` (or
`container`) · `node_name` (or `node`) · `host` · `service` · `source` · `format` · `env_type` ·
`raw` · `@loggroup` (= `workload`).

> [!WARNING]
> **SPL has no `region`, `app_version`, `instance`, `type`, `domain`, `body_length` or `kuid`.**
> A name SPL does not know is not an error — it is passed through to ClickHouse as a bare column
> name, so the query parses, compiles, and fails only when someone runs it.

> [!WARNING]
> **`get-trace-or-log-fields` returns the wrong names for SPL.** It reports catalog labels — `type`,
> `instance`, `domain` — which SPL does not accept. Use it **only** to discover dynamic attribute
> keys, and address those as `log_processed.<key>`. For columns, use the table above.

### Dynamic attributes

Parsed JSON fields are reached with the `log_processed.` prefix — SPL's equivalent of the SQL
endpoints' `@attr`:

```
filter log_processed.status = "500"
| stats count(*) as errors by log_processed.url
```

Resolution is string attributes → float attributes → JSON-parsed body.

## The Pipeline

Commands separated by `|`, read left to right.

```
"connection refused"
| filter level = "ERROR" AND namespace = "production"
| stats count(*) as errors by workload
| sort errors desc
| head 20
```

**Commands:** `fields` · `filter` (aliases `where`, `search`) · `parse` · `rex` · `eval` · `stats` ·
`timechart` · `dedup` · `head` · `tail` · `sort` · `limit` · `rename` · `table` · `top` · `rare`.
A bare quoted string is a full-text search on the message body and must come **first**. `#` starts a
comment.

**Order is semantic, not cosmetic.** A `filter` before `stats` becomes a `WHERE`; the same `filter`
after `stats` becomes a `HAVING` over the aggregate:

```
filter level = "ERROR" | stats count(*) as n by workload | filter n > 100
```

**Aggregations** for `stats` / `timechart`: `count(*)` · `sum` · `avg` · `min` · `max` · `dc`
(distinct count) · `median` · `mode` · `range` · `stdev` · `stdevp` · `var` · `sumsq` · `latest` ·
`earliest` · `values` · `list` · `perc<N>`.

> [!WARNING]
> **Percentiles are `perc95(x)`, never `p95(x)`.** `p95` is not a function. Like an unknown field it
> compiles and fails at run time — and KubeSense's own SPL manual taught the wrong form for a while,
> so it appears in older examples.

`timechart` takes `span=<N><s|m|h|d>` and names its bucket column `_time`:

```
timechart span=5m count(*) as errors by workload
```

## The Server Owns the Time Window

The time range and cluster filter are applied by the server, from the request — **not** from the
query. Write no timestamp condition. This is the inverse of the SQL endpoints, where
`$__timeFilter(timestamp)` is mandatory.

## Always Validate

`validate-spl` is not a formality here, because SPL's parser accepts more than ClickHouse will run:

| Mistake | Parses? | Compiles? | Caught by |
|---|---|---|---|
| `filter level =` (syntax) | ✗ | — | parse |
| `filter region = "x"` (unknown field) | ✓ | ✓ | **only `validate-spl`** |
| `stats p95(x)` (unknown function) | ✓ | ✓ | **only `validate-spl`** |
| `log_processed.typo` | ✓ | ✓ | nothing — returns nulls |

`validate-spl` resolves every identifier and function against the real log table without scanning a
row, and returns the compiled SQL under `## translated_sql`. **Read it** — it is how you confirm
`pod_name` resolved to the column you meant.

Attribute keys are the one thing it cannot check: a wrong `log_processed.<key>` returns nulls
silently, exactly as a wrong `@attr` does on the SQL side. Confirm keys with
`get-trace-or-log-fields` first.

## Limits

- **1000 rows** unless the pipeline ends with `| head N`, `| tail N` or `| limit N`.
- Read-only; filesystem, network and system functions are rejected.
- Unavailable to roles scoped to specific clusters, namespaces or workloads — the SPL endpoints apply
  a cluster filter only and cannot enforce finer rules. Use `search-logs` / `analyze-logs`, which do.

## Worked Examples

**Error count per workload, worst first**
```
filter level = "ERROR"
| stats count(*) as errors by workload
| sort errors desc
```

**Find the timeouts and read them**
```
"timeout"
| filter workload = "checkout"
| fields timestamp, pod_name, body
| head 50
```

**Error rate over time, split by namespace**
```
filter level = "ERROR"
| timechart span=5m count(*) as errors by namespace
```

**Latency percentiles from a JSON field**
```
filter log_processed.duration_ms > 0
| stats perc95(log_processed.duration_ms) as p95, avg(log_processed.duration_ms) as mean by log_processed.route
| sort p95 desc
```

**Extract fields from unstructured lines**
```
"APICallLogs:"
| parse 'Path:* Method:* StatusCode:*' as path, method, code
| filter code != "200"
| stats count(*) as errors by path, code
```

## Rules

1. Storage names, never catalog labels: `level` not `type`, `pod_name` not `instance`, `cluster` not
   `domain`.
2. `get-trace-or-log-fields` is for attribute keys only — its column names are wrong for SPL.
3. Call `validate-spl` before handing a query over or running it, and read the `translated_sql` it
   returns.
4. `perc95(x)`, never `p95(x)`.
5. Write no time or cluster filter — the server applies both.
6. A bare quoted search string goes first in the pipeline.
7. `filter` before `stats` is a WHERE; after `stats` it is a HAVING.
8. Aggregate in SPL; do not ask for raw rows to count them. 1000-row cap.
9. `log_processed.<key>` for parsed JSON fields — and a wrong key returns nulls, not an error.
10. Logs only. Traces and metrics have no SPL.
