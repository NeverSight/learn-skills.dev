---
name: otel-collector
description: Expert guidance for configuring and deploying the OpenTelemetry Collector. Use when setting up a Collector pipeline, configuring receivers, exporters, or processors, deploying a Collector to Kubernetes or Docker, or forwarding telemetry to Dash0. Triggers on requests involving collector, pipeline, OTLP receiver, exporter, or Dash0 collector setup.
license: MIT
metadata:
  author: dash0
  version: '1.0.0'
  workflow_type: 'advisory'
  signals:
    - traces
    - metrics
    - logs
---

# OpenTelemetry Collector configuration guide

Expert guidance for configuring and deploying the OpenTelemetry Collector to receive, process, and export telemetry.

## Rules

| Rule | Description |
|------|-------------|
| [receivers](./rules/receivers.md) | Receivers — OTLP, Prometheus, filelog, hostmetrics |
| [exporters](./rules/exporters.md) | Exporters — OTLP/gRPC to Dash0, debug, authentication |
| [processors](./rules/processors.md) | Processors — memory limiter, resource detection, ordering, sending queue |
| [pipelines](./rules/pipelines.md) | Pipelines — service section, per-signal configuration, connectors |
| [deployment](./rules/deployment.md) | Deployment — agent vs gateway patterns, deployment method selection |
| [dash0-operator](./rules/deployment/dash0-operator.md) | Dash0 Kubernetes Operator — automated instrumentation, Collector management, Dash0 export |
| [collector-helm-chart](./rules/deployment/collector-helm-chart.md) | Collector Helm chart — presets, modes, image selection |
| [opentelemetry-operator](./rules/deployment/opentelemetry-operator.md) | OpenTelemetry Operator — Collector CRD, auto-instrumentation, sidecar |
| [raw-manifests](./rules/deployment/raw-manifests.md) | Raw Kubernetes manifests — DaemonSet, Deployment, RBAC, Docker Compose |
| [sampling](./rules/sampling.md) | Sampling — head, tail, load balancing |
| [red-metrics](./rules/red-metrics.md) | RED metrics — span-derived request rate, error rate, duration histograms |

## Key principles

- **Processor ordering matters.**
  Place `memory_limiter` first in every pipeline.
  Use the exporter's `sending_queue` with `file_storage` instead of the `batch` processor.
  Incorrect ordering causes memory exhaustion or data loss.
- **One pipeline per signal type.**
  Define separate pipelines for traces, metrics, and logs.
  Mixing signals in a single pipeline breaks processing and causes runtime errors.
- **Every declared component must appear in a pipeline.**
  The Collector rejects configurations that declare receivers, processors, or exporters not referenced by any pipeline.
- **Consistent resource enrichment across pipelines.**
  Apply processors that enrich resource attributes like `resourcedetection` and `k8sattributes` to every signal pipeline (traces, metrics, and logs), not just one.
  If one pipeline enriches telemetry with `k8s.namespace.name` or `host.name` but another does not, correlation between signals is compromised by incomplete metadata.
- **Memory safety is non-negotiable.**
  Always configure `memory_limiter` in production.
  Without it, a burst of telemetry can cause the Collector to OOM and crash.

## Quick reference

| What do you need? | Rule |
|--------------------|------|
| Accept OTLP telemetry from applications | [receivers](./rules/receivers.md) |
| Scrape Prometheus endpoints | [receivers](./rules/receivers.md) |
| Collect log files or host metrics | [receivers](./rules/receivers.md) |
| Send telemetry to Dash0 | [exporters](./rules/exporters.md) |
| Configure retry, queue, or compression | [exporters](./rules/exporters.md) |
| Set processor ordering | [processors](./rules/processors.md) |
| Add Kubernetes or cloud metadata | [processors](./rules/processors.md) |
| Wire receivers → processors → exporters | [pipelines](./rules/pipelines.md) |
| Complete working configuration | [pipelines](./rules/pipelines.md) |
| Validate the pipeline with the debug exporter | [collector-helm-chart](./rules/deployment/collector-helm-chart.md), [opentelemetry-operator](./rules/deployment/opentelemetry-operator.md), [raw-manifests](./rules/deployment/raw-manifests.md), or [dash0-operator](./rules/deployment/dash0-operator.md) |
| Deploy as DaemonSet or Deployment | [raw-manifests](./rules/deployment/raw-manifests.md) |
| Deploy with Helm | [collector-helm-chart](./rules/deployment/collector-helm-chart.md) |
| Deploy with the OTel Operator | [opentelemetry-operator](./rules/deployment/opentelemetry-operator.md) |
| Deploy with the Dash0 Operator | [dash0-operator](./rules/deployment/dash0-operator.md) |
| Auto-instrument applications in Kubernetes | [opentelemetry-operator](./rules/deployment/opentelemetry-operator.md) or [dash0-operator](./rules/deployment/dash0-operator.md) |
| Local development with Docker Compose | [raw-manifests](./rules/deployment/raw-manifests.md) |
| Reduce trace volume | [sampling](./rules/sampling.md) |
| Keep errors and slow traces, drop the rest | [sampling](./rules/sampling.md) |
| Generate RED metrics from traces | [red-metrics](./rules/red-metrics.md) |

## Official documentation

- [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/)
- [Collector configuration](https://opentelemetry.io/docs/collector/configuration/)
- [Collector contrib components](https://github.com/open-telemetry/opentelemetry-collector-contrib)
- [Dash0 Integration Hub](https://www.dash0.com/hub/integrations)
