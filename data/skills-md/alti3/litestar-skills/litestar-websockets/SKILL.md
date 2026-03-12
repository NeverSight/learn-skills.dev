---
name: litestar-websockets
description: Build Litestar WebSocket endpoints with low-level websocket handlers, websocket listeners, websocket streams, dependency injection, custom websocket classes, transport-mode control, and graceful connection lifecycle handling. Use when implementing bidirectional real-time communication, reactive websocket message handling, or proactive server push over WebSockets. Do not use for server-side pub/sub fanout that is better expressed with channels alone.
---

# WebSockets

## Execution Workflow

1. Choose the interface first: low-level `@websocket`, reactive `@websocket_listener`, or proactive `@websocket_stream` / `send_websocket_stream()`.
2. Decide how data should be received and sent: text vs binary transport, raw socket methods vs typed serialization.
3. Keep connection acceptance, disconnect handling, and cleanup explicit.
4. Add DI, guards, DTOs, or custom websocket classes only where they simplify the endpoint contract.
5. Test both nominal message flow and disconnect or invalid-payload behavior.

## Core Rules

- Use low-level websocket handlers when you need full control over receive loops and socket operations.
- Use websocket listeners when a callback-style, typed receive-return-send flow matches the problem.
- Use websocket streams for proactive push from an async generator.
- Use `send_websocket_stream()` when you need to combine streaming with receiving data concurrently.
- Treat send and receive transport modes as protocol-level choices, not direct proxies for Python types.
- Keep disconnect handling explicit so loops and background tasks terminate cleanly.
- Avoid reading from the same socket in multiple places unless the flow is intentionally coordinated.

## Decision Guide

- Choose `@websocket` for manual accept, receive, send, and task orchestration.
- Choose `@websocket_listener` or `WebsocketListener` for event-driven typed messages and simpler business logic.
- Choose `@websocket_stream` for one-way push from server to client.
- Choose `send_websocket_stream()` with a low-level handler or listener when you must send a stream and receive messages concurrently.
- Use a custom `websocket_class` only when connection-level behavior must be extended consistently.

## Reference Files

Read only the sections you need:

- For low-level handlers, DI, connection lifecycle hooks, transport modes, custom websocket classes, and manual stream coordination, read [references/low-level-patterns.md](references/low-level-patterns.md).
- For websocket listeners, `WebsocketListener`, typed send and receive behavior, websocket streams, and stream/listener combinations, read [references/listener-and-stream-patterns.md](references/listener-and-stream-patterns.md).

## Recommended Defaults

- Default to text transport unless binary transfer is materially required.
- Keep message schemas explicit and narrow.
- Let typed listeners and DTO-capable handlers own serialization when message contracts are stable.
- Stop background tasks and generators on disconnect promptly.
- Treat websocket tests as protocol tests, not just function tests.

## Anti-Patterns

- Hand-writing receive loops when a listener already matches the problem.
- Mixing streaming and manual receives without coordinating disconnect handling.
- Assuming binary mode means Python `bytes` values only, or text mode means Python `str` values only.
- Leaving infinite loops running after disconnect.
- Packing large domain logic directly into websocket callbacks instead of delegating to services.

## Validation Checklist

- Confirm the chosen websocket interface matches the interaction pattern.
- Confirm accept, receive, send, and close behavior are explicit and testable.
- Confirm send and receive modes match the protocol and client expectations.
- Confirm DI, DTO, and custom websocket-class behavior work under real connection flow.
- Confirm disconnects stop background tasks, generators, and receive loops.
- Confirm stream endpoints do not accidentally lose data when disconnect listening is enabled.
- Confirm websocket tests assert both inbound and outbound frames.

## Cross-Skill Handoffs

- Use `litestar-channels` for server-side event fanout and broker-backed subscriptions.
- Use `litestar-authentication` or `litestar-security` for connection auth and authorization rules.
- Use `litestar-testing` for websocket client patterns and disconnect assertions.
- Use `litestar-dependency-injection` when websocket handlers depend on services or scoped resources.

## Litestar References

- https://docs.litestar.dev/latest/usage/websockets.html
- https://docs.litestar.dev/latest/reference/handlers.html
- https://docs.litestar.dev/latest/usage/testing.html
