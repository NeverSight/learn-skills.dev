---
name: 'otel-instrumentation'
description: Expert guidance for emitting high-quality, cost-efficient OpenTelemetry telemetry. Use when instrumenting applications with traces, metrics, or logs. Triggers on requests for observability, telemetry, tracing, metrics collection, logging integration, or OTel setup.
license: MIT
metadata:
  author: dash0
  version: '2.0.0'
  workflow_type: 'advisory'
  signals:
    - traces
    - metrics
    - logs
---

# OpenTelemetry Instrumentation Guide

Expert guidance for implementing high-quality, cost-efficient OpenTelemetry telemetry.

## Rules

| Rule | Description |
|------|-------------|
| [telemetry](./rules/telemetry.md) | **Entrypoint** - signal types, correlation, and navigation |
| [resolve-values](./rules/resolve-values.md) | Resolving configuration values from the codebase |
| [resources](./rules/resources.md) | Resource attributes - service identity and environment |
| [k8s](./rules/platforms/k8s.md) | Kubernetes deployment - downward API, pod spec |
| [spans](./rules/spans.md) | Spans - naming, kind, status, and hygiene |
| [logs](./rules/logs.md) | Logs - structured logging, severity, trace correlation |
| [metrics](./rules/metrics.md) | Metrics - instrument types, naming, units, cardinality |
| [nodejs](./rules/sdks/nodejs.md) | Node.js instrumentation setup |
| [go](./rules/sdks/go.md) | Go instrumentation setup |
| [python](./rules/sdks/python.md) | Python instrumentation setup |
| [java](./rules/sdks/java.md) | Java instrumentation setup |
| [scala](./rules/sdks/scala.md) | Scala instrumentation setup |
| [dotnet](./rules/sdks/dotnet.md) | .NET instrumentation setup |
| [ruby](./rules/sdks/ruby.md) | Ruby instrumentation setup |
| [php](./rules/sdks/php.md) | PHP instrumentation setup |
| [browser](./rules/sdks/browser.md) | Browser instrumentation setup |
| [nextjs](./rules/sdks/nextjs.md) | Next.js full-stack instrumentation (App Router) |

## Official documentation

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [Dash0 Integration Hub](https://www.dash0.com/hub/integrations)

## Key principles

### Signal density over volume

Every telemetry item should serve one of three purposes:
- **Detect** - Help identify that something is wrong
- **Localize** - Help pinpoint where the problem is
- **Explain** - Help understand why it happened

If it doesn't serve one of these purposes, don't emit it.

### Sample in the pipeline, not the SDK

Use the `AlwaysOn` sampler (the default) in every SDK.
Do not configure SDK-side samplers — they make irreversible decisions before the outcome of a request is known.
Defer all sampling to the [Collector](../otel-collector/rules/sampling.md), where policies can be changed centrally without redeploying applications.

```
SDK (AlwaysOn)  →  Collector (sampling)  →  Backend (retention)
     ↓                    ↓                       ↓
  All spans         Head or tail            Storage policies
  exported          sampling applied
```

## Quick reference

| Use Case | Rule |
|----------|------|
| Node.js backend | [nodejs](./rules/sdks/nodejs.md) |
| Go backend | [go](./rules/sdks/go.md) |
| Python backend | [python](./rules/sdks/python.md) |
| Java backend | [java](./rules/sdks/java.md) |
| Scala backend | [scala](./rules/sdks/scala.md) |
| .NET backend | [dotnet](./rules/sdks/dotnet.md) |
| Ruby backend | [ruby](./rules/sdks/ruby.md) |
| PHP backend | [php](./rules/sdks/php.md) |
| Browser frontend | [browser](./rules/sdks/browser.md) |
| Next.js (App Router) | [nextjs](./rules/sdks/nextjs.md) |
| Kubernetes pod spec | [k8s](./rules/platforms/k8s.md) |
| Resolve config values | [resolve-values](./rules/resolve-values.md) |
| Resource attributes | [resources](./rules/resources.md) |
| Writing metrics | [metrics](./rules/metrics.md) |
| Cardinality management | [metrics](./rules/metrics.md) |
| Span naming, kind, status | [spans](./rules/spans.md) |
| Writing logs | [logs](./rules/logs.md) |
| Signal overview | [telemetry](./rules/telemetry.md) |
