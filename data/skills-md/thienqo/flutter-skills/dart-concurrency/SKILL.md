---
name: dart-concurrency
description: Design and debug Dart asynchronous infrastructure with Future, Stream, isolates, cancellation, and lifecycle-safe ownership. Use for races, stale results, background CPU work, stream leaks, or async error handling; not for routine form-local validation or submission unless its underlying ordering mechanism is the task.
---

# Dart Concurrency

Make ownership, ordering, cancellation, and error propagation explicit.

## Diagnose first

Identify the producer, consumer, lifecycle owner, ordering requirement, and desired behavior when work becomes obsolete. Reproduce the race or leak before adding synchronization-like machinery.

## Decision rules

- Use `Future` for one result and `Stream` for a sequence over time.
- Avoid unawaited work unless independence and error handling are intentional.
- Cancel subscriptions and controllers according to the owning object's lifecycle.
- Guard UI updates after async gaps with the lifecycle mechanism appropriate to the project.
- Prevent stale requests from overwriting newer state through cancellation, tokens, sequencing, or latest-wins logic.
- Use isolates for measured CPU-bound work or isolation needs, not ordinary network I/O.
- Send transferable values across isolate boundaries and surface failures to the caller.
- Preserve stack traces when translating errors.

Do not hide async ownership inside global helpers. Keep retry and timeout policy at a boundary that understands idempotency and user intent.

## Verification

Test success, failure, cancellation/disposal, and out-of-order completion. Run static analysis; add a focused stress or fake-time test when timing is central to the bug.

## References

- Read [isolate communication and worker pools](references/isolate-communication-and-worker-pools.md) when handling heavy CPU computations, port messaging, or background worker threads.
- Read [stream cancellation and debouncing](references/stream-cancellation-and-debouncing.md) when managing subscription lifecycles, race conditions, debounce/throttle, or latest-wins semantics.

## Sources

- [Dart concurrency](https://dart.dev/language/concurrency)
- [Asynchronous programming](https://dart.dev/libraries/async/async-await)
