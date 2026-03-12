---
name: litestar-responses
description: Build Litestar responses with typed return values, explicit Response containers, layered response classes, headers, cookies, status-code control, redirects, files, streams, server-sent events, ASGI app returns, and background tasks. Use when shaping outbound HTTP behavior, correcting response contracts, or choosing the right Litestar response primitive. Do not use for request parsing, validation, or authentication policy design.
---

# Responses

## Execution Workflow

1. Start with the simplest return form that matches the contract: plain typed data, `Response[T]`, or a specialized response container.
2. Set status code, media type, headers, and cookies explicitly when defaults are not enough.
3. Choose specialized response types for redirects, files, streams, SSE, templates, or third-party ASGI responses.
4. Apply response-class layering only when serialization or envelope behavior should be shared across many handlers.
5. Verify OpenAPI accuracy for typed responses, documentation-only headers/cookies, empty-body statuses, and specialized response containers.

## Core Rules

- Prefer plain typed returns for standard JSON responses.
- Use `Response[T]` when you need runtime control over headers, cookies, background tasks, or status code.
- Keep generic arguments on response classes precise so schema generation stays accurate.
- Document runtime headers and cookies when clients depend on them, especially if values are set dynamically.
- Treat `204`, `304`, and other no-body responses as `None`-returning contracts.
- Keep success envelopes consistent with exception-handling envelopes where the API uses a shared contract.
- Use specialized response containers instead of reimplementing file, redirect, stream, or SSE behavior manually.
- Keep layered `response_class`, `response_headers`, and `response_cookies` overrides intentional and local.

## Decision Guide

- Return plain data when Litestar defaults already match the contract.
- Return `Response[T]` when the payload is normal but metadata is dynamic.
- Use `response_class=` when many endpoints need the same serialization strategy.
- Return `ASGIApp` when wrapping third-party ASGI response objects or custom low-level behavior.
- Use `File`, `Stream`, `ServerSentEvent`, or redirect responses when the transport semantics are special.
- Use subprocess test clients for live-server scenarios the in-process client cannot emulate well, especially infinite SSE streams.

## Reference Files

Read only the sections you need:

- For plain typed returns, `Response[T]`, status codes, layered `response_class`, custom response classes, and background tasks, read [references/response-basics.md](references/response-basics.md).
- For headers, cookies, redirects, files, streams, SSE, templates, and ASGI app returns, read [references/response-containers.md](references/response-containers.md).

## Recommended Defaults

- Let Litestar serialize normal JSON returns unless you need transport-level control.
- Use status-code constants from `litestar.status_codes` in both code and tests.
- Document dynamic headers and cookies with `documentation_only=True` metadata and set the runtime value in the response or hook.
- Keep stream and SSE generators cancellation-safe and bounded by disconnect behavior.
- Keep file delivery and redirect behavior explicit so intermediaries and clients behave predictably.

## Anti-Patterns

- Returning `Response[Any]` everywhere and losing schema precision.
- Using custom response classes when a normal `Response[T]` or built-in container is enough.
- Returning bodies for `204 No Content` endpoints.
- Setting dynamic headers or cookies without documenting them for OpenAPI when clients depend on them.
- Testing infinite stream or SSE behavior only with the in-process client.
- Reimplementing file serving manually instead of using `File`.

## Validation Checklist

- Confirm return annotations match the actual response body and status code.
- Confirm empty-body responses use `None` annotations and bodies.
- Confirm layered `response_class`, `response_headers`, and `response_cookies` precedence is intentional.
- Confirm dynamic headers and cookies are documented if clients depend on them.
- Confirm stream, SSE, redirect, and file responses have the intended media type and transport behavior.
- Confirm background tasks run only after the response body has been sent.
- Confirm OpenAPI output remains accurate after custom response-class or container changes.
- Confirm response documentation stays aligned with `litestar-openapi` metadata and examples.

## Cross-Skill Handoffs

- Use `litestar-exception-handling` for error-envelope and failure-response design.
- Use `litestar-openapi` when response changes materially affect schema output.
- Use `litestar-templating` for deeper template-engine concerns.
- Use `litestar-testing` for assertions on status, headers, cookies, streams, redirects, and SSE behavior.

## Litestar References

- https://docs.litestar.dev/latest/usage/responses.html
- https://docs.litestar.dev/latest/reference/response/index.html
- https://docs.litestar.dev/latest/usage/testing.html
