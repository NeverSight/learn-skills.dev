---
name: kubesense-metrics
description: Query Kubernetes, infrastructure and cloud-provider metrics from KubeSense with PromQL/MetricsQL — metric discovery, label inspection, the metric families KubeSense actually collects (kube-state-metrics, cAdvisor, node-exporter, OTel hostmetrics, DCGM GPU, JVM, and AWS/GCP/Azure/MongoDB Atlas/Confluent/Kong cloud resources), and the label conventions (clusterId, kubesense_cloud_resource_metric) needed to write a query that returns data.
metadata:
  version: "2.1.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,metrics,promql,metricsql,victoriametrics,prometheus,kube-state-metrics,cadvisor,node-exporter,gpu,jvm,interval-macros,cloud,aws,gcp,azure,cloudwatch,mongodb-atlas,confluent,kong
---

# KubeSense Metrics

Metrics are stored in **VictoriaMetrics** and queried with **PromQL** (plus MetricsQL
extensions — see below). Requires the KubeSense MCP server; see
**[kubesense-mcp](../kubesense-mcp/SKILL.md)** for connection and auth.

## Tools

| Tool | Purpose | Notes |
|---|---|---|
| `get-available-metrics` | List metric names | `search_keywords` are **AND**-matched, case-insensitive substrings |
| `get-metric-labels` | List label names on one metric | `name` required |
| `analyze-metrics` | Execute PromQL | `from_time`, `to_time`, `query_type`, `promql` all required |

All three resolve RBAC against the **`infrastructure`** module — a permission error here
means the caller lacks infrastructure access, not that the metric is missing.

## Discovery-First Rule

**Never guess a metric name.** Metric names are deployment-specific: they depend on
which collectors a cluster ships (kube-state-metrics vs OTel, node-exporter vs
hostmetrics). A query against a metric that does not exist returns an empty result that
is indistinguishable from "the value is zero".

```
get-available-metrics  →  get-metric-labels  →  analyze-metrics
```

`get-available-metrics` defaults to the **last 1 hour**. A sparse metric that reported
90 minutes ago will not appear — widen `from_time`/`to_time` before concluding it does
not exist.

```json
{ "search_keywords": ["container", "memory"], "limit": 40 }
```

Both keywords must appear in the name, so `["container","memory"]` matches
`container_memory_working_set_bytes` but not `container_cpu_usage_seconds_total`.

`get-metric-labels` returns **label names only**, not values. To see values, query the
metric with `analyze-metrics` and read the series labels off the result.

## Label Conventions (the #1 cause of empty results)

> [!IMPORTANT]
> The cluster label is **`clusterId`** — camelCase, no underscore. Not `cluster`, not
> `kubesense_cluster`, not `cluster_id`. Every kube-state-metrics / cAdvisor series in
> KubeSense carries it.

| Concept | Label on k8s/cAdvisor metrics | Label on OTel hostmetrics |
|---|---|---|
| cluster | `clusterId` | `kubesense_cluster` |
| host / node | `node` | `host_name` |
| environment | — | `kubesense_env_type` |
| namespace | `namespace` | — |
| pod | `pod` | — |
| container | `container` | — |
| workload | `deployment` / `daemonset` / `statefulset` (per metric family) | — |

The two families exist because a cluster ships telemetry either via
node-exporter/process-exporter **or** via the OpenTelemetry collector. Run
`get-metric-labels` to see which convention a given metric follows rather than assuming.

Cloud-provider metrics (AWS/GCP/Azure/Atlas/Confluent/Kong) are a **third** convention
with none of these labels — see [Cloud Resource Metrics](#cloud-resource-metrics) below.

Process metrics: the exporter family uses `groupname` (formatted `{pid}-{command}`);
the OTel family splits it into `process_pid`, `process_command_line`, and
`process_executable_name`.

## Writing Queries

```json
{
  "from_time": "2026-07-30T10:00:00Z",
  "to_time": "2026-07-30T11:00:00Z",
  "query_type": "range",
  "promql": "sum(rate(container_cpu_usage_seconds_total{container!='',clusterId='prod-us'}[5m])) by (namespace)"
}
```

- `query_type: "range"` → a time series (trends). `"instant"` → one scalar per series
  (totals, current state, top-N).
- **Step is computed for you**: `max(window/30, 15)` seconds. You cannot set it.

### Interval macros

A `rate()` window narrower than the step leaves gaps — the step for a 1-hour window is
120s, so `rate(x[30s])` samples less than one bucket's worth and returns a broken series.
Rather than picking a literal that happens to clear the step, use a macro. The API
resolves these before the query reaches VictoriaMetrics:

| Macro | Resolves to | Use for |
|---|---|---|
| `$__rate_interval` | `max(step + 15s, 60s)` | **`rate()` and `increase()`** — the default choice |
| `$__interval` | the step itself | `*_over_time` rollups, where the window should equal one bucket |
| `$__time_filter` | the query's whole time range (`to - from`) | a single total across the window |

```promql
sum(rate(container_cpu_usage_seconds_total{container!='',clusterId='prod-us'}[$__rate_interval])) by (namespace)
```

`$__rate_interval` tracks the step at every window size, so the same query works over 5
minutes and over 7 days. A literal like `[5m]` is still valid and still a safe default,
but it is the thing the macro exists to stop you having to reason about.

Two limits worth knowing:

- Only these three are resolved. `$__interval_ms` and `$__range` are **not** implemented
  and will reach VictoriaMetrics unexpanded, which fails.
- A macro inside a label value is left alone — `up{job="$__interval"}` matches the
  literal string, it is not rewritten into a duration.

### Two container-metric rules

1. **Always filter `container!=''`** on `container_*` metrics. cAdvisor emits an extra
   pod-level rollup series with an empty `container` label; without the filter every
   `sum()` double-counts.
2. **CPU is in cores.** `rate(container_cpu_usage_seconds_total[5m])` yields cores;
   multiply by 1000 for millicores, which is how KubeSense's own UI reports it.

### `kube_pod_container_resource_limits` / `_requests`

These are a *single* metric for both CPU and memory, discriminated by a `resource`
label — not separate metrics. Select it:

```promql
kube_pod_container_resource_limits{resource="memory"}
kube_pod_container_resource_limits{resource="cpu"}
```

Memory-usage-vs-limit is therefore a join, not a subtraction of two metrics:

```promql
sum by (pod, namespace) (container_memory_working_set_bytes{container!=''})
  / sum by (pod, namespace) (kube_pod_container_resource_limits{resource="memory"}) * 100
```

### `kube_*_status_phase` / `_condition` are label-encoded

`kube_pod_status_phase` is 1/0 per phase, with the phase in a label — so counting
running pods means selecting the label and de-duplicating series:

```promql
count(max by (pod, namespace, clusterId) (kube_pod_status_phase{phase="Running"}) > 0)
```

Same shape for nodes: `kube_node_status_condition{condition="Ready",status="true"}`.
The `max by (...)` de-dup matters — duplicate label sets otherwise inflate the count.

## MetricsQL Extensions

The backend is VictoriaMetrics, so MetricsQL is available on top of PromQL. Two
extensions KubeSense itself relies on:

| Extension | Use |
|---|---|
| `default 0` | Substitute a value where the series is absent: `sum(...) default 0` |
| `drop_empty_series(...)` | Discard series that are entirely empty after filtering |
| `[1h:60s]` subqueries | Rollup-over-rollup, e.g. `max_over_time(rate(x[5m])[1h:60s])` |

These will not work against a stock Prometheus, but they are correct here.

## Common Patterns

| Goal | Query |
|---|---|
| Per-second counter rate | `rate(metric[$__rate_interval])` |
| Aggregate across series | `sum(...) by (namespace)` |
| Histogram percentile | `histogram_quantile(0.99, sum(rate(metric_bucket[5m])) by (le))` |
| Total over a window | `increase(metric[$__time_filter])` |
| Top N | `topk(10, ...)` — pair with `query_type: "instant"` |
| Regex label match | `metric{namespace=~"prod-.*"}` |
| Ratio as a percentage | `sum(a) / sum(b) * 100` |

For a histogram percentile, always `sum(rate(...)) by (le)` **before**
`histogram_quantile` — passing raw buckets grouped by other labels produces nonsense.

## Cloud Resource Metrics

Metrics pulled from cloud providers' own monitoring APIs — AWS CloudWatch, Google Cloud
Monitoring, Azure Monitor, MongoDB Atlas, Confluent Cloud, Kong — are in the same
VictoriaMetrics instance but follow a **different convention entirely**.

> [!IMPORTANT]
> Every cloud datapoint, for every provider and resource type, is stored under one
> series name: **`kubesense_cloud_resource_metric`**. The provider's own metric name is
> the **`metric_name` label**, not part of the series name. `get-available-metrics`
> therefore returns exactly one name no matter how many cloud series exist, and
> searching it for `CPUUtilization` finds nothing.

```promql
kubesense_cloud_resource_metric{provider="aws",resource_type="Ec2Instance",metric_name="CPUUtilization"}
```

Fixed labels: `provider` (`aws` | `gcp` | `azure` | `mongodbatlas` | `confluent` |
`kong`), `account_id`, `resource_id`, `resource_type`, `metric_name`, `unit` — plus
collector dimensions such as `region`. There is **no `clusterId`, `namespace` or `pod`**,
so a selector copied from a Kubernetes query matches nothing.

Discovery is a PromQL step, not a tool call, because the values live in labels:

```promql
count by (resource_type) (kubesense_cloud_resource_metric{provider="aws"})
count by (metric_name, unit) (kubesense_cloud_resource_metric{resource_type="RdsInstance"})
```

Three rules that decide whether a cloud query is right or silently wrong:

1. **Never `rate()` them.** The provider's aggregation (CloudWatch `Sum`/`Average`, the
   Cloud Monitoring aligner, the Azure Monitor aggregation) is already applied at
   collection time. Use the raw value, or `sum_over_time`/`avg_over_time`/`max_over_time`
   to roll up buckets.
2. **Always pin `resource_type` alongside `metric_name`.** `CPUUtilization` alone mixes
   EC2, RDS, ECS, ElastiCache, DocumentDB, Neptune, OpenSearch and Redshift into one
   aggregate.
3. **Collection is a 5-minute tick with a 15-minute forward-fill.** Instant queries work
   because the newest sample is re-stamped; a series silent for more than 15 minutes is
   genuinely absent, not zero. Keep windows at or above 10m.

Full label contract, per-provider resource types and their metrics, the AWS types that
roll up onto a parent (there is no `PerformanceInsights` or `NetworkLoadBalancer`
resource type), and worked queries:
**[references/cloud-metric-catalog.md](./references/cloud-metric-catalog.md)**.

## Choosing Metrics vs Traces vs Infra Tools

- **Resource pressure, saturation, capacity** (CPU, memory, disk, GPU) → metrics.
- **Request rate, latency percentiles, error rate per service/endpoint** → traces
  (`analyze-traces`). Metrics have no per-request detail.
- **"Is this pod restarting / why" or "what's running"** →
  [kubesense-infra](../kubesense-infra/SKILL.md) tools; they return the same facts
  already joined and labelled, in one call.

Use metrics to *quantify and confirm* a hypothesis the cheaper tools surfaced.

## Metric Catalog

For the metric families KubeSense collects — exact names for pods, containers, nodes,
workloads, PVCs, network, GPU, JVM, and process metrics — read
**[references/metric-catalog.md](./references/metric-catalog.md)**. For AWS, GCP, Azure,
MongoDB Atlas, Confluent Cloud and Kong resource metrics, read
**[references/cloud-metric-catalog.md](./references/cloud-metric-catalog.md)**.

Treat the catalog as *what to expect*, not a substitute for discovery: which families
are present depends on the cluster's collectors, and application metrics are entirely
deployment-specific. Always confirm with `get-available-metrics`.

## Rules

1. `get-available-metrics` before writing PromQL. Never invent a metric name.
2. `get-metric-labels` before writing a label selector — and remember the cluster label
   is **`clusterId`**.
3. Filter `container!=''` on every `container_*` metric.
4. `rate()` windows must be ≥ the auto-computed step (`max(window/30, 15)`s). Prefer
   `$__rate_interval`, which guarantees it at any window size; `[5m]` is a safe literal.
5. `kube_pod_container_resource_limits`/`_requests` need a `resource="cpu"|"memory"`
   selector — they are one metric, not two.
6. `kube_*_status_phase`/`_condition` encode the state in a label; select it and de-dup
   with `max by (...)` before counting.
7. `query_type: "instant"` for totals/current state/top-N; `"range"` for trends.
8. An empty result means "no matching series", which is NOT the same as zero — verify
   the metric exists and the labels match before reporting a value of 0.
9. `sum(rate(...)) by (le)` before `histogram_quantile`.
10. Widen the discovery window for sparse metrics; `get-available-metrics` only looks
    back 1 hour by default.
11. Cloud-provider metrics are all one series — `kubesense_cloud_resource_metric` — with
    the provider's metric name in the `metric_name` label. Discover them with
    `count by (metric_name) (...)`, never `get-available-metrics`.
12. Never `rate()` a cloud metric, and always pin `resource_type` next to `metric_name`.
