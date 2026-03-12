---
name: litestar-testing
description: Test Litestar applications with TestClient, AsyncTestClient, create_test_client, websocket test helpers, dependency overrides, mocked dependencies, lifecycle-aware fixtures, and deterministic success and failure assertions. Use when adding or fixing Litestar test coverage, including exception contracts, override precedence, websocket behavior, event-bus side effects, or live-server-only response patterns. Do not use as a substitute for production observability or runtime debugging strategy.
---

# Testing

## Execution Workflow

1. Choose the right client shape first: `TestClient`, `AsyncTestClient`, `create_test_client`, or subprocess live-server helpers.
2. Build fixtures with deterministic configuration, dependencies, and lifecycle boundaries.
3. Isolate external I/O with injected fakes or mocked dependencies instead of monkeypatching internals.
4. Assert full contracts: status code, body, headers, cookies, side effects, and failure payload shape.
5. Cover error paths deliberately, including validation failures, app-level exception mappings, event-listener failures, layered override precedence, and schema/docs regressions.

## Core Rules

- Keep tests deterministic in time, randomness, and I/O.
- Use `AsyncTestClient` when tests, fixtures, and app resources must share the same event loop.
- Use `create_test_client` for isolated handler tests or small app subsets.
- Prefer dependency injection and fake services over patching transport-layer code.
- Assert stable error contracts, not just that an exception occurred.
- Reset overrides and fixture state between tests.
- Use live-server subprocess helpers when the in-process client cannot emulate the transport correctly.

## Decision Guide

- Use `TestClient` for synchronous tests that do not need to share async resources with the app.
- Use `AsyncTestClient` when async fixtures or resources are involved.
- Use `create_test_client` when you want a disposable app assembled inline for one test.
- Use `websocket_connect()` for websocket contract tests.
- Use subprocess clients for infinite SSE streams or other cases where HTTPX's in-process transport is insufficient.

## Reference Files

Read only the sections you need:

- For client selection, fixtures, async event-loop behavior, websocket tests, blocking-portal usage, and subprocess live-server helpers, read [references/client-patterns.md](references/client-patterns.md).
- For dependency overrides, mocked dependencies, exception-contract assertions, event-emission tests, listener-failure tests, schema/docs regressions, `404`/`405` testing, and layered precedence tests, read [references/failure-patterns.md](references/failure-patterns.md).

## Recommended Defaults

- Turn on `app.debug` only when a test needs it; otherwise keep tests aligned with production-facing behavior.
- Keep app assembly near the test when only one handler or one contract is under test.
- Assert response payloads and headers fully for custom exception handlers.
- Use one fake implementation per dependency boundary instead of broad monkeypatching.
- Prefer explicit fixtures over hidden global state.

## Anti-Patterns

- Using `TestClient` with async fixtures that create loop-bound resources.
- Asserting only status codes for custom error handlers.
- Letting dependency overrides leak across tests.
- Treating websocket tests like plain HTTP tests and ignoring handshake or frame behavior.
- Using in-process clients for transport patterns the docs call out as poor fits, such as infinite SSE streams.
- Relying on debug-only stack traces as part of the tested contract.

## Validation Checklist

- Confirm client choice matches the event-loop and resource model.
- Confirm startup and shutdown behavior are exercised where relevant.
- Confirm dependency overrides and mocked services are scoped to the test.
- Confirm expected failures produce stable payloads, headers, and status codes.
- Confirm emitted events and listener side effects are asserted when the feature depends on the event bus.
- Confirm app-level `404` and `405` handlers are tested at app scope.
- Confirm layered overrides behave as expected at app, router, controller, and handler scope.
- Confirm websocket tests assert both send and receive behavior.
- Confirm live-server helpers are used for scenarios the in-process client cannot model correctly.
- Confirm generated schema/docs regressions are covered when response or error contracts change.

## Cross-Skill Handoffs

- Use `litestar-dependency-injection` to design override-friendly providers and scope rules.
- Use `litestar-exception-handling` to standardize failure envelopes before locking tests.
- Use `litestar-events` when tests depend on event IDs, listeners, and custom emitter behavior.
- Use `litestar-responses` for stream, redirect, file, and SSE contract details.
- Use `litestar-openapi` when tests must lock down schema or docs behavior.
- Use `litestar-websockets` when the main challenge is websocket endpoint design rather than test harness setup.

## Litestar References

- https://docs.litestar.dev/latest/usage/testing.html
- https://docs.litestar.dev/latest/usage/exceptions.html
- https://docs.litestar.dev/latest/usage/websockets.html
