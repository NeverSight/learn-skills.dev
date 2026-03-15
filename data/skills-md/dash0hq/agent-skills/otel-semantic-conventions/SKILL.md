---
name: otel-semantic-conventions
description: OpenTelemetry Semantic Conventions expert. Use when selecting, applying, or reviewing telemetry attributes, span names, span kinds, or span status codes. Triggers on tasks involving attribute selection, naming telemetry, semantic convention compliance, attribute migration, or custom attribute decisions. Covers the attribute registry, naming patterns, status mapping, attribute placement, and versioning.
metadata:
  author: dash0
  version: '1.0.0'
---

# OpenTelemetry Semantic Conventions

Semantic conventions define standardized names, types, and semantics for telemetry attributes, span names, metric instruments, and log fields. They ensure that telemetry from different libraries, frameworks, and services describes the same concepts in the same way — enabling correlation, querying, and tooling across the entire stack.

The [Attribute Registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/) is the single source of truth for all defined attributes.

## Rules

| Rule                                | Description                                                           |
|-------------------------------------|-----------------------------------------------------------------------|
| [attributes](./rules/attributes.md) | Attribute registry, selection, placement, common attributes by domain |
| [versioning](./rules/versioning.md) | Semconv versioning, stability, migration                              |
| [dash0](./rules/dash0.md)           | Dash0 derived attributes and feature dependencies                     |

## Official documentation

- [Attribute Registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/)
- [Semantic Conventions Specification](https://opentelemetry.io/docs/specs/semconv/)
- [Semantic Conventions Repository](https://github.com/open-telemetry/semantic-conventions)
- [Dash0 Semantic Conventions](https://www.dash0.com/documentation/dash0/semantic-conventions)
- [Dash0 Semantic Conventions Explainer](https://www.dash0.com/knowledge/otel-semantic-conventions-explainer)

## Key principles

- **Registry first** — Search the [Attribute Registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/) before creating any custom attribute
- **No custom attributes unless necessary** — Custom names fragment querying and break tooling
- **Low cardinality in names** — Span names and metric attribute values must be bounded; variable data goes in attributes
- **Right level, every time** — Place attributes at the correct telemetry level (resource, scope, span, log, metric)
- **Consistent placement** — Once an attribute is at a level, keep it there across all services

## Quick reference

| Use Case                               | Rule                                |
|----------------------------------------|-------------------------------------|
| Choosing or reviewing attributes       | [attributes](./rules/attributes.md) |
| HTTP/DB/messaging/RPC attributes       | [attributes](./rules/attributes.md) |
| Attribute placement (resource vs span) | [attributes](./rules/attributes.md) |
| Naming a span or choosing span kind    | [spans](../otel-instrumentation/rules/spans.md) |
| Span status code mapping               | [spans](../otel-instrumentation/rules/spans.md) |
| Semconv version migration              | [versioning](./rules/versioning.md) |
| Dash0 derived attributes               | [dash0](./rules/dash0.md)           |
