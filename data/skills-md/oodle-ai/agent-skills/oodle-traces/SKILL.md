---
name: oodle-traces
description: Search and analyze Oodle traces by service, operation, duration, and error status, and run TraceQL searches and metrics.
metadata:
  version: "1.1.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,traces,spans,opentelemetry,apm,traceql
  globs: "**/*trace*,**/*span*,**/*otel*"
  alwaysApply: "false"
---

# Oodle Traces — Search and Analysis

This skill teaches the agent to search Oodle traces with the right service / time / duration filters, to fetch full trace detail by ID, and to run TraceQL.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
```

Confirm the traces endpoint works (use a recent time window):

```bash
oodle traces list --start -15m --end now -o json | jq 'length'
```

## Command Execution Order

Before running any oodle command:
1. Check whether a service name and approximate time window are already in context.
2. If not, run `oodle traces label-values resource::service.name --start -1h --end now -o json` to discover services that emitted traces recently.
3. Build the search with `--service`, `--start`, `--end` and at least one of `--tags '{"span_status":"Error"}'` / `--min-duration` / `--operation`. For conditions on any span attribute, use `oodle traces traceql search`.
4. To inspect a single trace, run `oodle traces get <trace-id> --start -1h --end now -o json`.
5. Do not run `oodle traces list` without a `--service` filter on production environments.

## Quick Reference

| Task | Command |
|------|---------|
| List traces in a service | `oodle traces list --service <svc> --start -1h --end now -o json` |
| List error traces only | `oodle traces list --service <svc> --tags '{"span_status":"Error"}' --start -1h --end now -o json` |
| List slow traces (>500ms) | `oodle traces list --service <svc> --min-duration 500ms --start -1h --end now -o json` |
| Filter by operation | `oodle traces list --service <svc> --operation GET_/users --start -1h --end now -o json` |
| Get full trace | `oodle traces get <trace-id> --start -1h --end now -o json` |
| TraceQL search | `oodle traces traceql search '{ status = error }' --start -1h --end now` |
| TraceQL metrics | `oodle traces traceql metrics '{ status = error } \| rate() by (resource.service.name)' --start -1h --end now --step 1m` |

## Common Operations

### Searching for errors in the last hour

```bash
# ✅ CORRECT — scoped to one service, narrow time window, error filter on
oodle traces list --service api --tags '{"span_status":"Error"}' --start -1h --end now -o json

# ❌ WRONG — no service, no error filter, huge result set
oodle traces list --start -1h --end now -o json
```

### Searching for slow traces

```bash
# ✅ CORRECT — slow checkout traces in the last hour
oodle traces list --service checkout --min-duration 500ms --start -1h --end now -o json

# ✅ CORRECT — narrow further by operation when you know the endpoint
oodle traces list --service checkout --operation POST_/cart --min-duration 500ms --start -1h --end now -o json

# ❌ WRONG — listing everything and sorting client-side wastes the API budget
oodle traces list --service checkout --start -1h --end now -o json | jq '.data | sort_by(.spans[0].duration) | reverse | .[0:10]'
```

### Fetching a full trace

```bash
# ✅ CORRECT — list to discover trace ids, then get the one of interest
TRACE_ID=$(oodle traces list --service api --tags '{"span_status":"Error"}' --start -15m --end now -o json | jq -r '.data[0].traceID')
oodle traces get "$TRACE_ID" --start -1h --end now -o json

# ❌ WRONG — `oodle traces get` without an id (it expects the id as a positional arg)
oodle traces get

# ❌ WRONG — `oodle traces get` without --start and --end (both are required)
oodle traces get "$TRACE_ID" -o json
```

### Time window flags

`--start` and `--end` are required for `list` and `get`. They accept the same formats as the rest of the CLI:

| Format | Example |
|--------|---------|
| Epoch seconds | `1731628800` |
| RFC 3339 | `2026-01-02T00:00:00Z` |
| `now` | `now` |
| Relative duration | `-1h`, `-30m`, `-7d` |

```bash
# ✅ CORRECT
oodle traces list --service api --start -30m --end now -o json

# ❌ WRONG — human strings are not parsed
oodle traces list --service api --start "30 minutes ago"
```

### TraceQL

`oodle traces traceql` has the alias `oodle traces tql`. Put the query in single quotes so the shell does not change `{`, `}`, `"`, or `!`.

```bash
# Find traces (filter only; a metrics query is rejected)
oodle traces traceql search '<filter>' [--start -1h] [--end now] [--limit 20]

# Time series from spans (needs a metrics function; a plain filter is rejected)
oodle traces traceql metrics '<filter> | <function>' [--start -1h] [--end now] [--step 5m] [--exemplars N] [-o graph|stats|json]

# Attribute names and values (reads only the last hour; no --start/--end)
oodle traces traceql tags [--scope resource|span|intrinsic|all] [-q '<filter>']
oodle traces traceql tag-values <tag> [-q '<filter>']
```

| Flag | Meaning |
|------|---------|
| `--start`, `--end` | `search` and `metrics`: default `-1h` and `now`. |
| `--limit` | `search`: maximum traces (default 20). |
| `--step` | `metrics`: `30s`, `5m`, `1h`, `1d`, or a number of seconds. Default `1m`, made larger to keep 300 points or fewer per series. |
| `--exemplars` | `metrics`: maximum exemplar traces. Shown only with `-o json` or `-o yaml`. |
| `-q`, `--query` | `tags`, `tag-values`: only look at spans that match this filter. |

Output: `search` prints one row per trace; `-o json` adds the matching spans and attributes. `metrics` prints one row per series (point count, last, min, max, average); `-o graph` draws a terminal chart, `-o stats` gives a summary, `-o json` gives all points.

#### Supported syntax

| Part | Supported |
|------|-----------|
| Spanset filter | `{ <condition> }` |
| Attribute scopes | `resource.<name>`, `span.<name>`, and unscoped `.<name>` (matches span or resource) |
| Intrinsics | `name`, `status`, `duration`, `kind` |
| Comparison | `=` `!=` `=~` `!~` `>` `>=` `<` `<=` |
| Combine in one spanset | `&&`, `||`, `!( ... )` |
| Union of spansets | `{ A } || { B }` |
| Attribute present / absent | `span.foo != nil`, `span.foo = nil` |
| Literals | strings `"x"`, numbers, durations `10s` `250ms`, `status = error` / `ok` / `unset`, `kind = server` / `client` / `internal` / `producer` / `consumer` |
| Metrics functions | `rate()`, `count_over_time()`, `avg_over_time(<field>)`, `min_over_time(<field>)`, `max_over_time(<field>)`, `sum_over_time(<field>)`, `histogram_over_time(<field>)`, `quantile_over_time(<field>, 0.5, 0.95, ...)` |
| Grouping | `by (<attribute>, ...)` after a metrics function |

#### Not supported yet

| Syntax | Use instead |
|--------|-------------|
| Scalar filters: `{ ... } \| count() > 2`, `\| avg(duration) > 1s` | `traceql metrics` with `count_over_time()` or `avg_over_time()`, and read the values |
| `{ A } && { B }` (two different spans of one trace) | One spanset `{ A && B }` when one span must match both |
| Structural operators `>>`, `<<`, `~` | Search for each span on its own, then compare trace ids |
| `parent.` and `link.` scopes | `span.` or `resource.` attributes |
| `rootName`, `traceDuration` | `name` and `duration` of a single span (for example, the root span by its name) |
| Bare existence: `{ span.foo }` | `{ span.foo != nil }` |

If a query fails with "not supported", rewrite it with the table above. Do not tell the user that TraceQL is not available.

#### Examples

```bash
# Errors in one service
oodle traces traceql search '{ resource.service.name = "checkout" && status = error }' --start -1h --limit 20

# GenAI tool calls over 10 s
oodle traces traceql search '{ span.gen_ai.tool.name != nil && duration > 10s }' --start -24h --limit 50

# Error rate by service
oodle traces traceql metrics '{ status = error } | rate() by (resource.service.name)' --start -6h --step 5m

# p50 and p95 latency per route, as a terminal chart
oodle traces traceql metrics '{ kind = server } | quantile_over_time(duration, 0.5, 0.95) by (span.http.route)' --start -1h -o graph

# Error rate with 5 example traces, for drill-down
oodle traces traceql metrics '{ status = error } | rate()' --start -1h --exemplars 5 -o json

# Attribute names and values
oodle traces traceql tags --scope span
oodle traces traceql tag-values span.http.route -q '{ resource.service.name = "checkout" }'
```

Monitors run PromQL, not TraceQL. To alert on traces, write the monitor query on the `oodle_trace_metrics` metric, or on the `oodle_genai_*` metrics for GenAI spans (see the oodle-monitors skill).

## Best Practices

### Always specify `--service` to scope the search

Trace volume can be massive; an unfiltered list is expensive and rate-limited.

```bash
# ✅ CORRECT
oodle traces list --service api --start -1h --end now -o json

# ❌ WRONG — full-tenant scan
oodle traces list --start -1h --end now -o json
```

### Use `--tags` to find failing traces, not client-side filtering

`--tags '{"span_status":"Error"}'` pushes the predicate to the server and returns matches faster.

```bash
# ✅ CORRECT
oodle traces list --service api --tags '{"span_status":"Error"}' --start -1h --end now -o json

# ❌ WRONG — fetches every trace then filters client-side
oodle traces list --service api --start -1h --end now -o json | jq '.data[] | select(.spans[].tags[] | .key=="error")'
```

### Use `--min-duration` to find slow traces, not client-side sort

```bash
# ✅ CORRECT — server-side filter, returns ~the right number of rows
oodle traces list --service api --min-duration 500ms --start -1h --end now -o json

# ❌ WRONG — pulls everything, sorts on the client
oodle traces list --service api --start -1h --end now -o json | jq '.data | sort_by(.spans[0].duration) | reverse'
```

### Keep time windows ≤ 24h for `list`; widen by re-querying, not by lowering `--start`

A 7-day list returns too many rows and risks timeouts. Page by hour.

```bash
# ✅ CORRECT — bounded window
oodle traces list --service api --tags '{"span_status":"Error"}' --start -1h --end now -o json

# ❌ WRONG — multi-day list
oodle traces list --service api --tags '{"span_status":"Error"}' --start -7d --end now -o json
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Trace ID does not exist or has aged out of retention | Re-list with a recent `--start` to find a current trace id |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var |
| Empty result | Wrong service name or time window outside retention | List recent services: `oodle traces label-values resource::service.name --start -1h --end now`; reduce the `--start` offset if it is past retention, or widen it if the window is too short (the CLI prints the range it read) |
| Request times out | Time window too large or no service filter | Narrow `--start`/`--end`, add `--service`, add `--min-duration` or `--tags` |
| 429 Too Many Requests | Concurrent trace fetches | Add `--retries 3`; throttle to <5 requests / second |
| `required flag(s) "end", "start" not set` | `list` and `get` need both flags | Add `--start -1h --end now` |
| 400 on `--min-duration` | Duration has no unit | Use `500ms`, `2s` |
| TraceQL `... is not supported` | Syntax from "Not supported yet" | Rewrite with the replacements in that table |
| `search` rejects the query | It has a metrics function (`\| rate()` …) | Use `oodle traces traceql metrics` |
| `metrics` rejects the query | It has no metrics function | Add one, or use `oodle traces traceql search` |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
- [OpenTelemetry trace concepts](https://opentelemetry.io/docs/concepts/signals/traces/)
- [TraceQL](https://grafana.com/docs/tempo/latest/traceql/)
