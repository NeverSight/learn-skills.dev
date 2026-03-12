---
name: litestar-logging
description: Configure Litestar logging with `LoggingConfig`, `queue_listener`, exception logging policy, selective stack-trace suppression, standard logging, picologging, Structlog, and custom logging config subclasses. Use when establishing or refactoring application logging behavior, request-level logs, or production-safe error logging in Litestar. Do not use for metrics/tracing instrumentation or exception-response contract design.
---

# Logging

## Execution Workflow

1. Choose the logging backend first: stdlib logging, picologging, Structlog, or a custom config subclass.
2. Configure logging once at app setup with `logging_config` or the Structlog plugin.
3. Use Litestar's non-blocking `queue_listener` handler unless a concrete reason requires otherwise.
4. Decide when exceptions should be logged and which stack traces should be suppressed.
5. Standardize request and app logger usage so fields, levels, and redaction rules stay consistent.
6. Validate that logs remain actionable without leaking sensitive data.

## Core Rules

- Keep logging configuration centralized at app construction.
- Prefer the built-in non-blocking `queue_listener` handler for async applications.
- Treat exception logging policy as an explicit decision; Litestar does not log exceptions by default outside debug mode.
- Use `disable_stack_trace` for expected exception types or status codes that should not spam traces.
- Keep secrets, auth material, and sensitive request data out of logs.
- Avoid duplicate logging across middleware, exception handlers, and business code.
- Keep logging concerns separate from metrics and tracing.

## Decision Guide

- Use `LoggingConfig` for standard logging or picologging-based setups.
- Use `logging_module="picologging"` when picologging is the desired backend.
- Use `StructlogPlugin` when structured logging with Structlog is the project standard.
- Use `log_exceptions="always"` when production incidents require exception logs even outside debug mode.
- Use `disable_stack_trace` for common expected errors such as `404` or domain-level validation problems.
- Subclass `BaseLoggingConfig` only when the built-in configs cannot express the needed behavior.

## Reference Files

Read only the sections you need:

- For stdlib logging, picologging, logger access, and custom config subclassing, read [references/configuration-patterns.md](references/configuration-patterns.md).
- For exception logging, stack-trace suppression, Structlog, and redaction-oriented guidance, read [references/exception-and-structlog-patterns.md](references/exception-and-structlog-patterns.md).

## Recommended Defaults

- Keep root level, handler choice, and formatter shape explicit.
- Use `request.logger` for request-scoped logs and one shared app logger for app-level events.
- Log exceptions intentionally instead of assuming Litestar will do it for you.
- Suppress traces only for expected, high-volume failures.
- Keep message fields and key names stable for searchability.

## Anti-Patterns

- Writing blocking log handlers into async request paths when `queue_listener` would suffice.
- Logging secrets, tokens, or raw sensitive payloads.
- Logging the same failure at multiple layers without adding new context.
- Enabling stack traces for high-volume expected failures that operators already understand.
- Subclassing logging config before exhausting built-in options.

## Validation Checklist

- Confirm logging is configured exactly once.
- Confirm request and app loggers emit at the intended levels.
- Confirm `log_exceptions` and `disable_stack_trace` match the incident policy.
- Confirm secrets and sensitive request fields are absent or redacted.
- Confirm queue-based handlers or equivalent non-blocking behavior are in place.
- Confirm structured logging output matches downstream log ingestion expectations.

## Cross-Skill Handoffs

- Use `litestar-metrics` for quantitative observability and scrape/export concerns.
- Use `litestar-exception-handling` for client-facing error contracts separate from logging behavior.
- Use `litestar-debugging` for incident-driven troubleshooting workflows.
- Use `litestar-security` when logging policy intersects with secrets, auth context, or redaction requirements.

## Litestar References

- https://docs.litestar.dev/latest/usage/logging.html
