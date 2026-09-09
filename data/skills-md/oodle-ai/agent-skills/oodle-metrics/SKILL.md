---
name: oodle-metrics
description: Query Oodle metrics, discover labels and values, and build PromQL expressions using the label discovery workflow.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,metrics,promql,labels
  globs: "**/*metric*,**/*.promql,**/*.prom"
  alwaysApply: "false"
---

# Oodle Metrics — Discovery and Querying

This skill teaches the agent to find metric names, enumerate their labels, and build PromQL queries that return data on the first try.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
```

Confirm the metrics endpoint works:

```bash
oodle metrics list --limit 5 -o json | jq 'length'
```

## Command Execution Order

Before running any oodle command:
1. Check whether the required metric name is already in context.
2. If not, run `oodle metrics list --match <prefix>` to discover it.
3. Run `oodle metrics labels <name>` to enumerate labels.
4. Run `oodle metrics label-values <name> <label>` to enumerate the values you need to filter on.
5. Build the PromQL query using only labels confirmed in step 3 and values confirmed in step 4.

## Quick Reference

| Task | Command |
|------|---------|
| List metric names (filtered) | `oodle metrics list --match "<prefix>" -o json` |
| List metric names (paged) | `oodle metrics list --limit 100 -o json` |
| Get one metric's metadata | `oodle metrics get <name> -o json` |
| List labels for a metric | `oodle metrics labels <name>` |
| List values for a label | `oodle metrics label-values <name> <label>` |

## Common Operations

### The 3-step label discovery workflow

Always run these three commands in order before writing a PromQL expression for a metric you have not used before.

```bash
# Step 1 — find the metric name
oodle metrics list --match "http_requests" -o json
# returns e.g. ["http_requests_total", "http_requests_in_flight"]

# Step 2 — list available labels
oodle metrics labels http_requests_total
# returns e.g. ["service", "method", "status", "env"]

# Step 3 — list values for a label
oodle metrics label-values http_requests_total service
# returns e.g. ["api", "checkout", "auth"]
```

```bash
# ✅ CORRECT — query built from confirmed labels and values
sum by (service) (rate(http_requests_total{service="api",env="prod",status=~"5.."}[5m]))

# ❌ WRONG — guessing label names; query returns no data
sum by (svc) (rate(http_requests{app="api",environment="production",http_status=~"5.."}[5m]))
```

### Filtering and paging metric lists

```bash
# ✅ CORRECT — narrow with --match
oodle metrics list --match "http_requests" -o json

# ✅ CORRECT — page with --limit when sweeping a namespace
oodle metrics list --match "kube_" --limit 200 -o json

# ❌ WRONG — listing every metric in the system, then grepping
oodle metrics list -o json | jq '.[] | select(. | contains("http"))'
```

### Cardinality-aware querying

Before grouping by a label, confirm cardinality is bounded:

```bash
# ✅ CORRECT — confirm `service` has <100 values before grouping by it
oodle metrics label-values http_requests_total service | wc -l

# ❌ WRONG — grouping by a high-cardinality label like `request_id` melts the query
sum by (request_id) (rate(http_requests_total[5m]))
```

## Best Practices

### Always use `--match <prefix>` when listing metrics

The metrics namespace can be large; an unfiltered `oodle metrics list` is slow and noisy.

```bash
# ✅ CORRECT
oodle metrics list --match "http_requests" -o json

# ❌ WRONG — returns thousands of results, may time out
oodle metrics list -o json
```

### Run the 3-step discovery workflow before writing PromQL

Guessed label names produce queries that return no data and look like a metric is missing.

```bash
# ✅ CORRECT — labels confirmed by step 2, values confirmed by step 3
oodle metrics labels http_requests_total
oodle metrics label-values http_requests_total service
sum by (service) (rate(http_requests_total{service="api"}[5m]))

# ❌ WRONG — writing the query first, then debugging "why is it empty?"
sum by (service_name) (rate(http_request_count{service_name="api"}[5m]))
```

### Always pipe to `jq` for scripting, never parse table output

Column ordering and widths in table output are not stable.

```bash
# ✅ CORRECT
oodle metrics list --match "http_" -o json | jq -r '.[]'

# ❌ WRONG
oodle metrics list --match "http_" | tail -n +2 | awk '{print $1}'
```

### Prefix every counter rate with `rate(...[5m])` not `rate(...[1m])`

`[1m]` rates are noisy on low-volume series and don't smooth across scrape gaps.

```bash
# ✅ CORRECT
sum by (service) (rate(http_requests_total[5m]))

# ❌ WRONG — flapping graphs, false alerts when a single scrape is missed
sum by (service) (rate(http_requests_total[1m]))
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Metric name does not exist | Run `oodle metrics list --match <prefix>` to find the correct name |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var |
| Empty result from a query | Wrong label name or wrong label value | Re-run step 2 (`labels`) and step 3 (`label-values`); fix the selector |
| Query timeout | Cardinality too high (e.g. `by (request_id)`) | Drop high-cardinality labels from `by (...)`; add a tighter time window |
| `parse error` | Broken PromQL syntax | Validate the expression in the UI metrics explorer first |
| 429 Too Many Requests | Heavy concurrent label-values calls | Add `--retries 3`; cache label-values output in scripts |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
- [PromQL reference](https://prometheus.io/docs/prometheus/latest/querying/basics/)
