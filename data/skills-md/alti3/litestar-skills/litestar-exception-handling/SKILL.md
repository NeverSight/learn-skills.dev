---
name: litestar-exception-handling
description: Implement Litestar exception handling with HTTPException, built-in exception subclasses, custom exception handlers, layered overrides, status-code mappings, and stable API error contracts. Use when translating domain failures, validation errors, middleware/dependency failures, or router-generated HTTP errors into deterministic Litestar responses. Do not use for authentication or authorization policy design that belongs in security layers.
---

# Exception Handling

## Execution Workflow

1. Separate startup and configuration failures from request-time failures.
2. Decide whether the failure should be represented by raising `HTTPException` or by mapping another exception type through an exception handler.
3. Choose the narrowest layer that should own the handler: app, router, controller, or route handler.
4. Keep the outbound error contract stable: status code, payload shape, media type, and safe detail level.
5. Register app-level handlers for `404 Not Found` and `405 Method Not Allowed` when those responses must be customized.
6. Verify validation and server-failure paths separately so sensitive details do not leak unintentionally.

## Core Rules

- Distinguish configuration/startup exceptions from request-handling exceptions.
- Use `HTTPException` or its subclasses when the handler should raise an HTTP-aware error directly.
- Use exception handlers to translate domain or library exceptions into transport-safe responses.
- Keep error payload schemas stable across handlers and layers.
- Keep documented error behavior aligned with `litestar-openapi` route metadata and security docs.
- Redact or replace validation and internal error details when exposing raw messages would leak implementation details.
- Prefer specific exception mappings over broad catch-alls that hide root causes.
- Keep handler registration close to the layer that owns the behavior, except for `404` and `405`, which must be handled at app scope.

## Decision Guide

- Raise `HTTPException` subclasses directly for clear HTTP semantics such as `401`, `403`, `404`, `429`, or `503`.
- Map domain exceptions with `exception_handlers` when business logic should stay transport-agnostic.
- Map by exception class when the exception type is the stable contract.
- Map by status code when multiple exceptions should share one response format for the same HTTP status.
- Use app-level defaults for generic `500` handling and lower-level overrides only where behavior genuinely differs.

## Reference Files

Read only the sections you need:

- For exception taxonomy, built-in subclasses, `HTTPException` constructor behavior, validation warnings, headers, `extra`, and websocket-related exceptions, read [references/built-in-exceptions.md](references/built-in-exceptions.md).
- For handler registration patterns, plain-text vs JSON responses, status-code mappings, layered overrides, and the app-only `404`/`405` rule, read [references/handler-patterns.md](references/handler-patterns.md).

## Recommended Defaults

- Standardize one JSON error envelope unless a route intentionally serves another media type.
- Treat `ValidationException.extra` as potentially user-visible diagnostic data.
- Keep `500` responses generic for clients and detailed in logs.
- Prefer class-based mappings for business exceptions and app-level status-code mappings for generic fallback behavior.
- Keep middleware and dependency failures covered by the same top-level error strategy as route handlers.

## Anti-Patterns

- Returning raw exception text for internal server errors in production APIs.
- Exposing validation internals or stack-trace-like details to clients without intent.
- Registering a catch-all handler that collapses every failure into the same `400` response.
- Splitting identical error envelopes across many handlers without a clear reason.
- Trying to customize `404` or `405` below the app layer.
- Encoding authorization policy inside generic exception handlers instead of security layers.

## Validation Checklist

- Confirm expected exception classes map to the intended status codes.
- Confirm app startup and configuration errors are not treated as request-time API responses.
- Confirm `404` and `405` customization is registered on the `Litestar` app instance.
- Confirm payload shape is consistent across handlers, routes, and layers.
- Confirm documented error responses and raised exceptions match the real contract.
- Confirm validation failures do not leak more detail than intended.
- Confirm unhandled exceptions still surface as `500` responses and remain observable in logs.
- Confirm route-specific overrides do not accidentally shadow broader app policy.
- Confirm middleware and dependency exceptions follow the same contract as handler-raised exceptions.

## Cross-Skill Handoffs

- Use `litestar-authentication` or `litestar-security` for auth-specific `401` and `403` strategy.
- Use `litestar-responses` when the main task is response formatting rather than exception mapping.
- Use `litestar-testing` for exhaustive failure-path assertions and override coverage.
- Use `litestar-openapi` when documented error responses or security-related failure docs need to match runtime behavior.
- Use `litestar-logging` when exception observability, redaction, or structured logging is part of the task.

## Litestar References

- https://docs.litestar.dev/latest/usage/exceptions.html
- https://docs.litestar.dev/latest/reference/exceptions.html
- https://docs.litestar.dev/latest/usage/middleware/using-middleware.html
