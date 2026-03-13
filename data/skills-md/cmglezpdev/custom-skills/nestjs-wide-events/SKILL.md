---
name: nestjs-wide-events
description: Implement structured, wide-event logging in NestJS applications following the canonical log line / wide event pattern. Use this skill whenever the user asks about logging, observability, debugging, or tracing in a NestJS app. Also trigger when the user mentions log lines, structured logging, canonical log lines, wide events, request context, observability, or asks how to improve their NestJS logging setup. Use this even if the user just says "add logging" to a NestJS project, since the wide event pattern should be the default, not scattered console.log calls.
---

# NestJS Wide Events Logging

Emit ONE context-rich structured JSON event per request per service, instead of scattering dozens of log lines across the codebase.

## Core Principles

1. **One event per request per service.** Build context throughout the lifecycle; emit once at the end.
2. **Business context is mandatory.** Include subscription tier, account age, feature flags, cart value -- anything needed at 2am during an incident.
3. **High cardinality is the point.** Fields like `user_id`, `request_id`, `order_id` with millions of unique values make debugging possible.
4. **High dimensionality wins.** 50 fields on one event beats 5 fields across 10 events.
5. **Structured JSON only.** Every field is a queryable key-value pair.
6. **Tail sampling controls cost.** Always keep errors, slow requests, VIP users. Sample the rest.
7. **No log-level abuse.** The wide event IS the log. Level indicates outcome severity only.

## Architecture Overview

### Components

- **`WideEventInterceptor`** (global): Creates context at request start, emits the single event at request end.
- **`WideEventService`** (request-scoped): Holds the mutable event context. Any service/guard/pipe injects it to enrich the event.
- **`WideEventModule`**: Wires everything together. Import at root level.
- **`TailSampler`**: Decides whether to persist the event (always keeps errors, slow requests, VIP users).
- **`WideEventExceptionFilter`** (global): Enriches the event with error details before the interceptor emits.
- **`WideEventMiddleware`**: Resolves the request-scoped service and attaches it to the request object for the singleton interceptor.

### Request Lifecycle

```
Request arrives
  -> Middleware resolves request-scoped WideEventService, attaches to req
    -> Interceptor seeds event with HTTP metadata, starts timer
      -> Guards/pipes inject WideEventService, add user context
        -> Controller/services inject WideEventService, add business context
      -> Response or exception
    -> ExceptionFilter catches errors, enriches event
  -> Interceptor finalizes: duration, status, outcome
  -> TailSampler decides: persist or drop
  -> Single JSON event emitted
```

### Wide Event Field Groups

- **Request envelope** (auto): `timestamp`, `request_id`, `trace_id`, `method`, `path`, `status_code`, `duration_ms`, `ip`, `user_agent`, `service`, `version`
- **User context** (auth guard/controller): `user.id`, `user.subscription`, `user.role`, `user.org_id`
- **Business context** (controller/service): domain-specific fields like `cart.*`, `payment.*`
- **Error context** (exception filter): `error.type`, `error.code`, `error.message`, `error.retriable`
- **Performance** (services doing I/O): `db.query_count`, `db.total_ms`, `cache.hit`, `external_calls[]`
- **Feature flags**: `feature_flags.*` as flat booleans
- **Outcome** (interceptor): `outcome` (`success`|`error`|`client_error`), `level` (`info`|`warn`|`error`)

### Key Rules

1. Use `REQUEST` scope for `WideEventService` -- each request gets its own instance.
2. Only the interceptor calls `logger.info(event)`. Services only enrich.
3. Sanitize sensitive fields with an allowlist, not a denylist.
4. Use `AsyncLocalStorage` when request-scoped DI is unavailable (queues, event handlers).
5. Nest fields under namespaces: `user.id` not `userId`, `payment.latency_ms` not `paymentLatencyMs`.
6. Timings use `_ms` suffix, always integers.
7. For queue/cron jobs: emit one wide event per job execution, same pattern.

### Tail Sampling

- **Always keep (100%):** status >= 500, error field present, duration > p99 threshold, VIP users, monitored feature flags
- **Sample the rest:** configurable rate, default 5%

### Anti-Patterns

- Do NOT scatter `console.log()` / `this.logger.log()` through services.
- Do NOT use log levels to categorize request stages.
- Do NOT put high-volume debug tracing in the wide event.
- Do NOT log request/response bodies wholesale -- extract only needed fields.
- Do NOT treat OpenTelemetry as a substitute; your wide event IS your enriched OTel span.

## Reference Documents

Read these only when you need implementation details for a specific area:

- **`core-setup.md`** -- Full code for WideEventService, WideEventInterceptor, WideEventExceptionFilter, TailSampler, WideEventMiddleware, WideEventModule, and app bootstrap. Read this when setting up wide events from scratch.
- **`usage-examples.md`** -- How to enrich events from controllers, services, and auth guards. Read this when adding wide event enrichment to existing code.
- **`advanced-patterns.md`** -- AsyncLocalStorage bridge, queue/cron job pattern, and Pino integration. Read this for non-HTTP contexts or production logger setup.
- **`testing.md`** -- Unit tests for WideEventService and TailSampler. Read this when writing tests.

## Quick Start

1. Read `core-setup.md` for full component code.
2. Create `WideEventModule` with all components, register at app root.
3. In controllers/services, inject `WideEventService` and call `event.enrich({...})`.
4. Configure `TailSampler` sampling rules.
5. Remove all scattered log statements -- replace with event enrichments.
