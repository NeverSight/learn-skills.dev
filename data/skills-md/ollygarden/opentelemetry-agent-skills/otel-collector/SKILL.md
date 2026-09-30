---
name: otel-collector
description: OpenTelemetry Collector component configuration. Use when authoring, reviewing, or debugging Collector YAML for a specific receiver, processor, exporter, connector, or extension — config keys, defaults, validation rules, signal support, stability levels, and component-level gotchas. Triggers on Collector component questions including receivers, processors, exporters, connectors, extensions, component renames, signal support, and pipeline wiring.
---

# OpenTelemetry Collector

This skill covers the configuration surface of individual OpenTelemetry Collector components. It targets [opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector) and [opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib).

It does **not** cover OTTL expressions (see `otel-ottl`), declarative SDK configuration (`otel-declarative-config`), or end-to-end pipeline design choices. Reach for those skills when the question is about transformation language, SDK setup, or pipeline composition.

## Workflow

1. **Identify the component.** Find the `type` in the user's config or question (`log_dedup`, `interval`, `otlp`, …). Note that several components were renamed to snake_case across v0.146.0–v0.154.0 with deprecated aliases preserved — see [Recent renames](#recent-renames).
2. **Load the component page before answering.** If the component is in the [Component index](#component-index), always read `components/<type>/README.md` first — the top-level index is only a routing aid, not enough evidence for an answer. Follow its **Details** index to the smallest relevant file: read `configuration.md` for versioned keys, defaults, or validation; `quirks.md` for stability, availability, failure behavior, or migration traps; and the other detail files only as the question requires. Do not infer exact configuration or status from the summary row or memory.
3. **If the component is not indexed**, say so explicitly and fall back to the upstream README under `processor/<name>/`, `receiver/<name>/`, `exporter/<name>/`, `connector/<name>/`, or `extension/<name>/` in [opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib). Don't invent config keys from memory — Collector components evolve quickly.
4. **Apply Collector-wide conventions.** Named instances (`type/name`), stability levels, and pipeline placement rules in [Collector-wide conventions](#collector-wide-conventions) apply to every component.
5. **Verify.** Run the component page's **Verification** recipe — `telemetrygen` (see the `otel-telemetrygen` skill) plus a `debug` or `file` exporter — to confirm the component behaves as the docs claim. Alpha- and Development-stability components are common here, and behavior changes between releases. See [Verification harness](#verification-harness) for how to run a recipe end-to-end.

## Component index

Each component is a directory under `components/<type>/`. The `File` column points at the lean `README.md` (metadata, description, main use-cases, and a **Details** index); the full config reference, verification recipe, advanced use-cases, and quirks live in on-demand detail files linked from that README.

Coverage is intentionally selective. If a component is not indexed here, fall back to the upstream component README for the user's Collector version.

| Type | File | Kind | Signals | Stability | Summary |
|------|------|------|---------|-----------|---------|
| `log_dedup` | `components/log_dedup/README.md` | processor | logs | Alpha | Deduplicates identical log records over a time window; emits one aggregated log with a count. Renamed from `logdedup` in v0.151.0; alias preserved. |
| `interval` | `components/interval/README.md` | processor | metrics | Alpha | Buffers cumulative monotonic metrics (and optionally gauges/summaries) and emits the latest value once per interval. Delta and non-monotonic sums pass through unchanged. |
| `tail_sampling` | `components/tail_sampling/README.md` | processor | traces | Beta | Buffers whole traces and makes a single keep/drop decision after a wait window via policies. Supports in-process concurrency through `num_shards`; scaling across Collector instances still requires a `load_balancing` layer. v0.160 adds tracestate-aware thresholds for rate/bytes limiting. |
| `drain` | `components/drain/README.md` | processor | logs | Alpha | Clusters log bodies and annotates each record with a template. v0.158 replaced `extract_parameters` / `params_attribute` with `masking_rules` + `parameter_key_prefix` for named values and `emit_wildcards` + `wildcards_attribute` for remaining `<*>` positions. |
| `redaction` | `components/redaction/README.md` | processor | traces, logs, metrics | Beta (traces), Alpha (logs/metrics) | Allow/block-list masking or removal of sensitive attribute keys and values, with hashing and URL/DB sanitizers. |
| `filter` | `components/filter/README.md` | processor | traces, metrics, logs, profiles | Alpha (traces/metrics/logs), Development (profiles) | Drops spans, metric data points, log records, and profiles that match OTTL conditions (or legacy metric-name / severity filters). The most direct telemetry-volume lever. |
| `transform` | `components/transform/README.md` | processor | traces, metrics, logs, profiles | Beta (traces/metrics/logs), Development (profiles) | Applies OTTL statements to mutate spans, metric data points, log records, and profiles in place (rename/redact/convert/aggregate attributes). The OTTL language itself lives in the `otel-ottl` skill. |
| `probabilistic_sampler` | `components/probabilistic_sampler/README.md` | processor | traces, logs | Beta (traces), Alpha (logs) | Head sampling — deterministically keeps a configured percentage of traces/logs by hashing the trace ID (or an attribute). The cheaper, stateless counterpart to `tail_sampling`. |
| `attributes` | `components/attributes/README.md` | processor | traces, metrics, logs | Beta | Modifies span/log/datapoint **attributes** via an ordered action list (insert/update/upsert/delete/hash/extract/convert), scoped by include/exclude matching. |
| `resource` | `components/resource/README.md` | processor | traces, metrics, logs, profiles | Beta (traces/metrics/logs), Development (profiles) | Modifies the **resource** attributes of telemetry via the same action grammar as `attributes` (e.g. set `service.name`, drop noisy resource keys). No include/exclude matching. |
| `k8s_attributes` | `components/k8s_attributes/README.md` | processor | traces, metrics, logs, profiles | Beta (traces/metrics/logs), Development (profiles) | Enriches telemetry with Kubernetes pod/namespace/node/workload metadata, associating each record to a pod by IP or resource attribute. v0.160 removes `deployment_name_from_replicaset` and adds ReplicaSet/CronJob label and annotation extraction. |
| `routing` | `components/routing/README.md` | connector | traces, metrics, logs | Alpha | Routes same-signal telemetry to different pipelines by OTTL `condition`/`statement` per context; ordered table, first match wins, `default_pipelines` fallback. Replaces the deprecated `routingprocessor`. |
| `memory_limiter` | `components/memory_limiter/README.md` | processor | traces, metrics, logs, profiles | Beta (traces/metrics/logs), Alpha (profiles) | Safety valve against OOM: refuses data with backpressure when Go heap exceeds a soft/hard limit. Its receiver-middleware **extension** reached Beta in v0.158 but is absent from stock distributions; the bundled processor remains the standard form. |
| `load_balancing` | `components/load_balancing/README.md` | exporter | traces, logs, metrics | Beta (traces/logs), Alpha (metrics) | Distributes telemetry across downstream Collectors via a consistent-hash ring keyed on trace ID / `service.name` (etc.), pinning related records to one backend. The standard way to scale `tail_sampling`/`span_metrics`. Renamed from `loadbalancing` in v0.153.0; alias preserved. |
| `otlp` (receiver) | `components/otlp/README.md` | receiver | traces, metrics, logs, profiles | Stable (traces/metrics/logs), Alpha (profiles) | The canonical OTLP ingress over gRPC (`4317`) and/or HTTP (`4318`, protobuf + JSON). `protocols:` block, at least one required. Default endpoint is `localhost`, not `0.0.0.0` — must be set explicitly to receive containerized traffic. |
| `otlp_grpc` (exporter) | `components/otlp_exporter/README.md` | exporter | traces, metrics, logs, profiles | Stable (traces/metrics/logs), Alpha (profiles) | Sends OTLP over gRPC to a downstream endpoint; gzip, sending queue, and retry are enabled by default. Exporter-side `sending_queue.batch` is opt-in unless the `pkg.exporterhelper.queueBatchEnabled` gate is enabled. Renamed from `otlp` in core v1.50.0; alias preserved. |
| `file_log` (receiver) | `components/file_log/README.md` | receiver | logs | Beta | Tails log files (glob `include`), turns each line/entry into a log record, and parses it via a stanza `operators` pipeline. Fingerprint + offset tracking across rotation; `storage` for durable offsets. v0.160 adds opt-in `skip_unmodified_files`. |
| `resource_detection` | `components/resource_detection/README.md` | processor | traces, metrics, logs, profiles | Beta (traces/metrics/logs), Development (profiles) | Auto-detects resource attributes via an ordered `detectors` list with global retry settings. Includes Azure Container Apps and, since v0.160, Azure App Service detectors. Renamed from `resourcedetection` in v0.153.0; alias preserved. |
| `file_storage` | `components/file_storage/README.md` | extension | — (not pipeline-scoped) | Beta | Persists component state to local disk (bbolt) so it survives a Collector restart: receiver read offsets (`storage:`), exporter persistent send queues (`sending_queue.storage:`), and stateful-processor decision caches. One bbolt file per consumer; `directory` must exist unless `create_directory: true`. Not placed in a pipeline — listed under `service.extensions:` and referenced by other components. |
| `prometheus` (receiver) | `components/prometheus/README.md` | receiver | metrics | Beta | Scrapes Prometheus-format HTTP endpoints and converts them to OTLP metrics, embedding `prometheus/prometheus`'s scrape manager — the `config:` block is the same YAML as `prometheus.yml` (`global`, `scrape_configs`, `scrape_config_files`, service discovery, relabeling). Extra keys: `trim_metric_suffixes`, `target_allocator` (sharded targets from the OTel Operator), `api_server` (debug API). Scrape-only: rejects `remote_write`/`remote_read`/`rule_files`/alerting. Stateful, does not auto-shard across replicas. |
| `prometheus` (exporter) | `components/prometheus_exporter/README.md` | exporter | metrics | Beta | Exposes pipeline metrics for Prometheus to scrape. In-memory accumulator expires stale series after 5m. v0.160 adds `resource_constant_labels` and deprecates `resource_to_telemetry_conversion`; `add_metric_suffixes` remains deprecated in favor of `translation_strategy`. |
| `prometheus_remote_write` (exporter) | `components/prometheus_remote_write/README.md` | exporter | metrics | Beta | Pushes OTLP metrics as Prometheus Remote Write. Nests HTTP client settings under `http`; uses `remote_write_queue` (not `sending_queue`). v0.160 adds `resource_constant_labels` and deprecates `resource_to_telemetry_conversion`; RW2 remains gated and in development. |

## Collector-wide conventions

### Named instances

Every component type supports the `type/name` pattern so the same type can be configured more than once. The pipeline references the named form:

```yaml
processors:
  log_dedup/health-checks:
    interval: 30s
    conditions:
      - 'log.attributes["log.type"] == "health_check"'
  log_dedup/access-logs:
    interval: 10s

service:
  pipelines:
    logs/health:
      processors: [log_dedup/health-checks]
    logs/access:
      processors: [log_dedup/access-logs]
```

### Stability levels

Components publish a stability level per signal. Treat these as load-bearing when recommending production use:

| Level | Use in |
|-------|--------|
| Development | Tests and prototypes only — breaking changes expected. |
| Alpha | Limited, non-critical workloads — config keys can still change. |
| Beta | Production viable — breaking changes rare. |
| Stable | Production — backward compatibility guaranteed. |

Stability now varies per component — and per signal for multi-signal components (e.g. `redaction` is Beta for traces but Alpha for logs/metrics). Don't assume a single level for the indexed set: check each component's README header metadata table for the authoritative stability and surface it when the user asks about production readiness.

### Recent renames

Many components were renamed to snake_case across v0.146.0–v0.154.0. The legacy names remain as deprecated aliases — old configs keep working but new configs should use the new names. Check the upstream component README for the exact rename version before flagging a config as broken.

Examples: `logdedup` → `log_dedup`, `hostmetrics` → `host_metrics`, `spanmetrics` → `span_metrics`, `servicegraph` → `service_graph`, `k8sattributes` → `k8s_attributes`, plus several `_log` and `_check` receivers.

### Pipeline placement

Two rules of thumb that apply across components:

- `memory_limiter` belongs first in any processor list, before anything that allocates buffers (`log_dedup`, `transform`, `tail_sampling`, …).
- The `otlp_grpc` exporter's sending queue is enabled by default, but its `sending_queue.batch` sub-block is opt-in. Enable exporter-side batching explicitly (or with the alpha `pkg.exporterhelper.queueBatchEnabled` migration gate). The separate `batch` processor remains Beta and supported; use it when pipeline-level batching is needed and place it after data-dropping processors.

### Verification harness

Each component page's **Verification** section gives a config, a `telemetrygen` command, and the expected output. To run any of them:

1. Save the YAML to a file and start a collector that bundles the component — for components in the `contrib`/`k8s` distributions, `otelcol-contrib --config <file>.yaml`; for components not in any distribution, build a custom collector with the [OpenTelemetry Collector Builder (OCB)](https://github.com/open-telemetry/opentelemetry-collector/tree/main/cmd/builder) first.
2. Send telemetry with `telemetrygen` (see the `otel-telemetrygen` skill).
3. Watch the `debug` exporter's stdout (or the `file` exporter's output) for the expected result.

The Verification configs are **minimal repros**: they omit `memory_limiter` and other production scaffolding on purpose, to isolate the component under test. Don't copy them verbatim into production.

## Adding a new component to this skill

When extending coverage:

1. **Create the directory `components/<type>/`.** Files carry no frontmatter — only `SKILL.md` has frontmatter.
2. **Write a lean `README.md`** — always loaded, kept small:
   - **Header metadata table** — kind, `type` name, signals, per-signal stability, distributions, Go module, upstream README link, and a rename note if the component was renamed.
   - **Description** — what the component does and the mechanism, in 1–2 tight paragraphs (push detailed mechanism/reference into `configuration.md`).
   - **Main use-cases** — "Use when" / "Avoid when".
   - **Related components** — cross-links.
   - **Details index** — a bullet list where each item links a detail file followed by an em dash and a short description of its contents (e.g. `- [Configuration](configuration.md) — config keys, defaults, validation`), so the reader loads only what a question needs.
3. **Split the rest into on-demand detail files** under the same directory:
   - **`configuration.md`** — full config-reference table (key, type, default, validation) plus any mechanism/reference tables.
   - **`verification.md`** — a `telemetrygen` + `debug`/`file` exporter recipe that proves the documented behavior; cross-reference the `otel-telemetrygen` skill. **Verify every `telemetrygen` flag against that skill — never assert a flag that doesn't exist.** If `telemetrygen` can't produce the input the component needs, say so and point to an alternative (OTTL/`transform`, a custom emitter). Keep the config a minimal repro (see [Verification harness](#verification-harness)).
   - **`advanced.md`** — named instances, multi-pipeline setups, combinations, and edge configs.
   - **`quirks.md`** — gotchas, stability caveats, memory model, a validation-error→fix table, anti-patterns, and troubleshooting.
   - Split a heavy section into its own file when it's large (e.g. `policies.md` for a big policy catalog); merge trivial sections into a sibling rather than create a stub. Repoint any in-page anchor links that now cross files.
4. **Use `components/log_dedup/` and `components/interval/` as reference implementations** of this structure.
5. **Add a row to the [Component index](#component-index)** above (the `File` column points at `components/<type>/README.md`).
6. **Update the description trigger phrases** in this file's frontmatter if the new component introduces a clearly distinct user-facing keyword.
