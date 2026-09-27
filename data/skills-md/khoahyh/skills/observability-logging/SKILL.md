---
name: observability-logging
description: Design, add, or review production logs, traces, and metrics for operational questions, safe fields, and error ownership.
---

# Observability Logging

Use the least production telemetry that answers a defined operational question. If existing signals answer it, add nothing. Use `motel-debug` for temporary diagnostic probes rather than retaining them as production instrumentation.

## Signal And Scope

| Operational need | Signal |
| --- | --- |
| Duration and causal operation boundary | Span |
| Meaningful occurrence or state transition | Named event or structured log |
| Aggregate rate, count, or distribution | Metric |

A context-rich completion event can answer several known queries; it does not replace useful spans or point-in-time events by default.

Use static names such as `checkout.completed` or HTTP route templates. Put dynamic values in attributes, with bounded metric dimensions. Resource attributes describe the service and deployment, not individual requests. Use SDK trace/span correlation; an application request ID complements it.

Inbound middleware owns request lifecycle fields; application modules own business outcomes; outbound adapters classify dependency failures. Configure resources, exporters, sampling, and structured logging at the composition root. For Effect programs, use the installed version's span and scoped logging APIs rather than ad hoc global loggers.

## Safe Fields

Allowlist fields by operational need. Prefer operation, route template, state or typed error tag, dependency, retry count, and bounded numeric summaries. Opaque non-PII domain IDs belong only where an established allowlist permits them and incident lookup requires them.

Keep secrets, credentials, tokens, cookies, sessions, raw PII, payment data, bodies, SQL parameters, prompts/completions, arbitrary objects, and raw signed URLs out of telemetry. Capture headers or sanitized URL components only through an explicit allowlist. Bound and sanitize untrusted strings; preserve `Redacted` values through adapters without recording them.

## Error Ownership

Record a terminal failure once at the outermost owning boundary that classifies the final operational outcome, correlated with the active span. Include a stable typed error tag and safe context. Lower adapters translate failures rather than duplicating the terminal record at every catch and rethrow.

Handled retries and fallbacks do not make a successful enclosing operation fail. Intentional cancellation is an outcome, not an error. Use `WARN` for conditions needing operational attention and fatal severity only for process-ending failures.

## Completion

For a design or review, identify the operational question, needed signal or existing coverage, ownership, safe fields, and any evidence gaps. For implementation, continue through focused checks of emitted telemetry and fix attributable issues within scope.

The relevant boundary should demonstrate stable names, trace correlation, one terminal error record, accurate handled outcomes, safe fields, and bounded metric dimensions. Use an existing test collector or runtime query that can answer the original question; avoid building a telemetry test framework for a small edit. Report unavailable runtime evidence instead of claiming emission was verified. Repeat or broaden checks only when changes, failures, or unresolved risks warrant it.

## Conditional References

Consult version-matched SDK documentation when API behavior is uncertain, and the relevant standard when deciding schema, error, or data-handling policy:

- [OpenTelemetry logs data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)
- [OpenTelemetry events](https://opentelemetry.io/docs/specs/semconv/general/events/)
- [OpenTelemetry error recording](https://opentelemetry.io/docs/specs/semconv/general/recording-errors/)
- [OpenTelemetry sensitive data](https://opentelemetry.io/docs/security/handling-sensitive-data/)
- [OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
