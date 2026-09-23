---
name: opentelemetry
description: "OpenTelemetry — vendor-neutral observability framework for generating and collecting traces, metrics, and logs. Use when building with OpenTelemetry or asking about its JavaScript/Node.js SDK setup, auto-instrumentation, manual spans, exporters, context propagation, sampling, or integration with Jaeger, Zipkin, or OTLP collectors. Fetch live documentation for up-to-date details."
---

# OpenTelemetry

> **CRITICAL: Your training data for OpenTelemetry is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://opentelemetry.io/docs/languages/js/")`**
>
> Do not proceed without fetching this URL first. Never assume package names or initialization patterns — verify against current docs.

OpenTelemetry is a vendor-neutral observability framework for generating, collecting, and exporting traces, metrics, and logs.

## Key Capabilities

OpenTelemetry JS bundles capabilities that developers often reach for separate tools to cover:

- **Auto-instrumentation**: `@opentelemetry/auto-instrumentations-node` automatically instruments popular frameworks and libraries (Express, HTTP, gRPC, database clients) with zero code changes — no manual span creation needed for common libraries
- **Resource detection**: built-in detectors for cloud providers, containers, and process info via `OTEL_NODE_RESOURCE_DETECTORS` — no need for custom resource-tagging middleware
- **Context propagation**: W3C TraceContext and Baggage propagated automatically across async boundaries when using `tracer.startActiveSpan` — no manual context threading required

## Best Practices

- **Instrumentation must load before application code** — For ESM projects, use `node --import ./instrumentation.mjs`. For CommonJS projects or the zero-code package (`@opentelemetry/auto-instrumentations-node`), use `node --require @opentelemetry/auto-instrumentations-node/register` (or `--require ./instrumentation.js`). Loading instrumentation after app code silently produces no-op spans with no errors thrown.
- **Use `BatchSpanProcessor` in production, never `SimpleSpanProcessor`** — the simple processor exports synchronously on every span end, adding latency to every request. `BatchSpanProcessor` is the correct choice for production; `SimpleSpanProcessor` is only appropriate for debugging.
- **SDK initialization failure is silent** — if the SDK is initialized too late or fails to initialize, OpenTelemetry returns no-op implementations and emits no errors. Always verify spans appear in your exporter before deploying.
- **Always call `span.end()`** — spans that are never ended are never exported. Wrap span bodies in try/finally to guarantee `span.end()` is called even on exceptions.
- **Lower the default sample rate for production** — the getting-started default captures 100% of traces. Set `OTEL_TRACES_SAMPLER=parentbased_traceidratio` and `OTEL_TRACES_SAMPLER_ARG=0.1` (or equivalent SDK config) before going to production to avoid excessive collector and backend costs.
