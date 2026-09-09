---
name: oodle-metrics-query
description: Execute PromQL instant and range queries against Oodle metrics using the Prometheus-compatible query API.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,metrics,query,promql,prometheus
  globs: "**/*query*,**/*.promql,**/*metric*"
  alwaysApply: "false"
---

# Oodle Metrics Query — PromQL Instant and Range Queries

This skill teaches the agent to execute PromQL instant and range queries against Oodle metrics using the Prometheus-compatible query API.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
```

Confirm the query endpoint works:

```bash
oodle metrics query --query "up" -o json | jq '.status'
```

## Command Execution Order

Before running any query command:
1. Check whether the required metric name is already known.
2. If not, run `oodle metrics names --start -1h --end now` to discover metric names.
3. Run `oodle metrics labels <name> --start -1h --end now` to discover available labels.
4. Build the PromQL expression using only confirmed metric names and labels.
5. Do not run speculative queries — always confirm metric and label existence first.

## Quick Reference

| Task | Command |
|------|---------|
| Instant PromQL query | `oodle metrics query --query "sum(up)" -o json` |
| Instant query at specific time | `oodle metrics query --query "up" --time 1700000000 -o json` |
| Range PromQL query | `oodle metrics query-range --query "rate(http_requests_total[5m])" --start -1h --end now --step 60s -o json` |
| Range query with partial response | `oodle metrics query-range --query "up" --start -1h --end now --step 60s --partial-response -o json` |

## Common Operations

### Instant query

Evaluate a PromQL expression at a single point in time. Returns the current value by default, or the value at a specific timestamp.

```bash
# CORRECT — instant query with JSON output for scripting
oodle metrics query --query "sum(up)" -o json

# CORRECT — instant query at a specific time
oodle metrics query --query "up{job=\"prometheus\"}" --time 1700000000 -o json

# CORRECT — use relative time
oodle metrics query --query "up" --time -5m -o json

# WRONG — omitting --query flag
oodle metrics query -o json
```

### Range query

Evaluate a PromQL expression over a time range. All four flags (`--query`, `--start`, `--end`, `--step`) are required.

```bash
# CORRECT — range query over the last hour with 60-second resolution
oodle metrics query-range --query "rate(http_requests_total[5m])" --start -1h --end now --step 60s -o json

# CORRECT — range query with absolute timestamps
oodle metrics query-range --query "up" --start 1700000000 --end 1700003600 --step 60s -o json

# CORRECT — enable partial response for degraded-mode queries
oodle metrics query-range --query "up" --start -1h --end now --step 60s --partial-response -o json

# WRONG — missing --step flag
oodle metrics query-range --query "up" --start -1h --end now -o json

# WRONG — missing --start or --end
oodle metrics query-range --query "up" --step 60s -o json
```

## Best Practices

### Use `oodle metrics` to discover before querying

Always confirm metric names and labels exist before building a PromQL query. Querying a nonexistent metric returns empty results, not an error.

```bash
# CORRECT — discover first, then query
oodle metrics names --start -1h --end now -o json | jq '.[] | select(startswith("http"))'
oodle metrics labels http_requests_total --start -1h --end now
oodle metrics query --query "sum(rate(http_requests_total[5m]))" -o json

# WRONG — guessing metric names
oodle metrics query --query "sum(rate(requests_total[5m]))" -o json
```

### Choose the right step for range queries

The step determines the resolution of the returned time series. Too small a step returns excessive data; too large a step misses detail.

```bash
# CORRECT — 60s step for a 1-hour window (60 data points)
oodle metrics query-range --query "up" --start -1h --end now --step 60s -o json

# CORRECT — 5m step for a 24-hour window (288 data points)
oodle metrics query-range --query "up" --start -1d --end now --step 5m -o json

# WRONG — 1s step for a 24-hour window (86400 data points — too many)
oodle metrics query-range --query "up" --start -1d --end now --step 1s -o json
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 400 Bad Request | Invalid PromQL expression | Check syntax at https://prometheus.io/docs/prometheus/latest/querying/basics/ |
| Empty result (not an error) | Metric does not exist or no data in time range | Run `oodle metrics names` to verify the metric exists; widen the time range |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var, ensure no trailing slash |
| 429 Too Many Requests | Rate limited | Add `--retries 3`, back off, reduce query frequency |
| `required flag "step"` | Missing required flag for range query | Add `--step` flag (e.g. `--step 60s`) |
| `required flag "query"` | Missing required flag | Add `--query` flag with a PromQL expression |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
- [PromQL documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
