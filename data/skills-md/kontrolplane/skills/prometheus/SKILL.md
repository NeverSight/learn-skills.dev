---
name: prometheus
description: Prometheus metrics and PromQL queries. Use when writing PromQL queries, creating recording or alerting rules, debugging metric scraping issues, or understanding counter/gauge/histogram behavior.
---

# Prometheus

## PromQL Gotchas

### Counter Functions (Critical)
Counters only increase. Never use raw counter values—always use rate functions:
```promql
rate(http_requests_total[5m])      # Per-second average rate
irate(http_requests_total[5m])     # Instant rate (last 2 points, spiky)
increase(http_requests_total[1h])  # Total increase over range
```
- `rate()` handles counter resets automatically
- Use `rate()` for dashboards, `irate()` only for high-resolution spikes

### Range Vector Required
Rate functions need `[duration]`:
```promql
rate(metric[5m])    # Correct
rate(metric)        # Error: expected range vector
```

### Vector Matching
Binary operations require matching labels:
```promql
# This fails if label sets differ:
metric_a / metric_b

# Ignore extra labels:
metric_a / ignoring(extra_label) metric_b

# Match on specific labels only:
metric_a / on(common_label) metric_b
```

### Histogram Quantiles
```promql
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)
```
- Must use `_bucket` metric with `le` label
- Always wrap in `rate()` for counters
- `by (le)` is required; add other labels as needed: `by (le, endpoint)`

## Common Query Patterns

```promql
# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m]))

# CPU usage (node_exporter)
100 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m]) * 100)

# Memory usage
1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)

# Container memory (Kubernetes)
sum by (pod) (container_memory_working_set_bytes{container!=""})
```

## Alerting Rules

```yaml
groups:
  - name: example
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
            / sum(rate(http_requests_total[5m])) by (job)
            > 0.05
        for: 5m          # Must be firing for this duration
        labels:
          severity: warning
        annotations:
          summary: "Error rate {{ $value | humanizePercentage }} on {{ $labels.job }}"
```

### for Clause
- Prevents flapping on brief spikes
- Alert stays "pending" until duration met
- Missing `for` = immediate alerting

## Recording Rules

Pre-compute expensive queries:
```yaml
rules:
  - record: job:http_requests:rate5m
    expr: sum by (job) (rate(http_requests_total[5m]))
```

Naming convention: `level:metric:operations`

## Staleness

- Samples older than 5 minutes are "stale"
- `up == 0` only fires if target was recently scraped
- Use `absent(metric)` to detect missing metrics entirely
