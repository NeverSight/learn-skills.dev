---
name: litestar-events
description: Use Litestar's event emitter and listener system with `@listener`, `request.app.emit()`, multiple listeners per event, multi-event listeners, shared argument contracts, and custom event emitter backends. Use when decoupling async side effects, fanout-style in-process notifications, or transport-triggered domain events inside a Litestar app. Do not use for startup/shutdown lifecycle hooks, request/response interception, or broker-backed pub-sub systems that belong in app setup, lifecycle hooks, or channels.
---

# Events

## Execution Workflow

1. Decide whether the event bus is the right tool: decoupled in-process side effects, not app lifecycle or broker-backed messaging.
2. Define stable event IDs and argument contracts before wiring emitters and listeners.
3. Register listeners on the `Litestar` app with `listeners=[...]`.
4. Emit events from handlers or services through `request.app.emit(...)` or another app reference.
5. Keep listeners independent so multiple listeners can react to the same event safely.
6. Replace the default emitter backend only when retry, persistence, or external infrastructure requirements justify it.

## Core Rules

- Treat event IDs as stable contracts, not ad hoc strings scattered through the codebase.
- Make every listener for an event compatible with the full emitted `*args` and `**kwargs` set.
- Use `**kwargs` defensively when multiple listeners consume different subsets of the same event payload.
- Keep listener bodies side-effect focused and small; delegate heavy domain logic to services.
- Use the built-in in-memory emitter for simple in-process async fanout.
- Implement a custom emitter backend only when persistence, retry, scheduling, or external transport is required.
- Do not confuse the event bus with `on_startup` / `on_shutdown`; those are different Litestar mechanisms.

## Decision Guide

- Use events when one action should trigger one or more async side effects without coupling the route handler to each implementation.
- Use multiple listeners when several side effects should react to the same event independently.
- Use one listener with multiple event IDs only when the argument contract and behavior are genuinely shared.
- Use a custom backend when event delivery must survive process boundaries or support retry/history semantics.
- Use `litestar-channels` instead when the problem is real pub-sub or cross-process fanout.
- Use `litestar-app-setup` instead when the task is startup/shutdown initialization.

## Reference Files

Read only the sections you need:

- For listener registration, multi-event listeners, multiple listeners, argument-shape rules, emission patterns, and service-layer design, read [references/listener-patterns.md](references/listener-patterns.md).
- For backend selection, `SimpleEventEmitter`, custom backend requirements, async context manager behavior, and failure semantics, read [references/emitter-backends.md](references/emitter-backends.md).

## Recommended Defaults

- Centralize event ID constants or naming rules.
- Emit keyword arguments instead of positional arguments when contracts may evolve.
- Keep listener signatures tolerant of extra kwargs when multiple listeners share an event.
- Prefer the default `SimpleEventEmitter` unless concrete requirements force a custom backend.
- Keep emitted payloads domain-oriented and free of request-specific transport details where possible.

## Anti-Patterns

- Using events for startup/shutdown resource management.
- Emitting inconsistent argument shapes for the same event ID.
- Writing listeners that break as soon as another listener needs an extra kwarg.
- Hiding critical synchronous business steps behind fire-and-forget event listeners.
- Reaching for a custom backend before the in-process emitter's limits are real.
- Using events as a substitute for channels when cross-process delivery is required.

## Validation Checklist

- Confirm each emitted event ID has an intentional contract and owner.
- Confirm every listener can accept the full emitted arg/kwarg shape.
- Confirm multiple listeners for the same event remain independent and idempotent enough for the use case.
- Confirm event emission is placed after the authoritative state change that should trigger it.
- Confirm the default emitter backend is sufficient, or document why a custom backend is required.
- Confirm listener failures do not accidentally cancel sibling listeners.
- Confirm tests cover both emission side effects and listener argument compatibility.

## Cross-Skill Handoffs

- Use `litestar-app-setup` for startup/shutdown hooks and lifespan ownership.
- Use `litestar-lifecycle-hooks` for request/response interception and instrumentation.
- Use `litestar-channels` for broker-backed or cross-process publish-subscribe flows.
- Use `litestar-testing` for event-emission assertions and listener-failure tests.

## Litestar References

- https://docs.litestar.dev/2/usage/events.html
- https://docs.litestar.dev/2/reference/events.html
- https://docs.litestar.dev/2/reference/config.html
