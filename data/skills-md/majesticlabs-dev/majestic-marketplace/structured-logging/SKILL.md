---
name: structured-logging
description: Production logging patterns for observability and incident debugging. Structured JSON logging, correlation IDs, context propagation, log levels, and performance. Use when implementing logging, adding observability, or debugging production systems. Triggers on logging setup, logger configuration, observability, distributed tracing, or incident response workflows.
---

# Structured Logging

## Core Philosophy

- Logs are optimized for **querying**, not writing — design with debugging in mind
- A log without correlation IDs is useless in distributed systems
- If you can't answer "Who was affected? What failed? When? Why?" within 5 minutes, logging needs work

## Structured Format

Always use key-value pairs (JSON), never string interpolation.

```json
{
  "event": "payment_failed",
  "user_id": "123",
  "reason": "insufficient_funds",
  "amount": 99.99,
  "timestamp": "2025-01-24T20:00:00Z",
  "level": "error",
  "service": "billing",
  "request_id": "req_abc123"
}
```

## Required Fields

Every log event MUST include:

| Field | Format | Example |
|-------|--------|---------|
| `timestamp` | ISO 8601 with timezone | `2025-01-24T20:00:00Z` |
| `level` | debug, info, warn, error | `info` |
| `event` | snake_case, past tense | `user_login_succeeded` |
| `request_id` or `trace_id` | UUID or prefixed ID | `req_abc123` |
| `service` | Service/app name | `api-gateway` |
| `environment` | prod, staging, dev | `prod` |

## High-Cardinality Fields

Include these when available — they make logs queryable during incidents:

| Category | Fields |
|----------|--------|
| Identity | `user_id`, `org_id`, `account_id` |
| Tracing | `request_id`, `trace_id`, `span_id` |
| Domain | `order_id`, `transaction_id`, `job_id` |

**Rule:** Look for domain-specific identifiers that help isolate issues to specific entities.

## Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| `debug` | Verbose local dev details, disabled in prod | Variable values, loop iterations |
| `info` | Normal operations worth recording | User actions, job completions, deploys |
| `warn` | Unexpected but handled | Retries triggered, fallbacks activated |
| `error` | Failed, needs attention | Exceptions, failed requests, timeouts |

**Anti-pattern:** Don't log errors for expected conditions (wrong password = info, not error).

## Context Propagation

For distributed systems:

1. **Inherit IDs** — Downstream services must receive correlation IDs from upstream
2. **Pass through boundaries** — HTTP headers, message queues, async jobs
3. **Middleware injection** — Auto-inject context into every log via middleware/interceptor

```
[Client] --request_id--> [API Gateway] --request_id--> [Service A] --request_id--> [Service B]
                              |                              |                          |
                           (logs)                         (logs)                     (logs)
                              ↓                              ↓                          ↓
                     All queryable by single request_id
```

**Async jobs:** Store and restore original request context when processing background work.

## What to Log

| Log These | Skip These |
|-----------|------------|
| Request entry/exit with duration | Sensitive data (passwords, tokens, PII, cards) |
| State transitions (created → paid → shipped) | Inside tight loops |
| External service calls with latency + status | Success cases with no debug value |
| Auth/authz events | Redundant infra logs (LB already captures) |
| Job starts, completions, failures | |
| Retry attempts, circuit breaker changes | |

## Naming Conventions

| Pattern | Example |
|---------|---------|
| Field names: `snake_case` | `user_id`, not `userId` or `user-id` |
| Events: past tense verbs | `payment_completed`, not `complete_payment` |
| Domain prefixes when helpful | `auth.login_failed`, `billing.invoice_created` |

**Team agreement:** Define field names once, use consistently across all services.

## Performance

| Concern | Solution |
|---------|----------|
| High-volume debug logs | Sampling in production |
| Hot path logging | Avoid or use async appenders |
| I/O overhead | Buffer and batch writes |
| Dynamic verbosity | Runtime-configurable log levels |

## Language-Specific Implementations

| Language | Library | Notes |
|----------|---------|-------|
| Python | `structlog` | See `majestic-data/etl-core-patterns` |
| Ruby/Rails | `Rails.event` (8.1+), `semantic_logger` | See `majestic-rails/dhh-coder/structured-events` |
| Node.js | `pino`, `winston` with JSON formatter | |
| Go | `slog` (stdlib), `zerolog` | |
| Java | `logback` with JSON encoder | |

## Decision Table: Log or Not?

| Scenario | Decision | Reason |
|----------|----------|--------|
| User enters wrong password | `info` | Expected behavior, not an error |
| Payment gateway timeout | `error` + retry | Needs attention, affects user |
| Cache miss | `debug` | Only useful for performance analysis |
| User created account | `info` | Business event worth recording |
| Loop iteration 5000 of 10000 | Don't log | Creates noise, no debug value |
| External API returns 500 | `warn` or `error` | Depends on retry/fallback behavior |
| Background job started | `info` | Useful for job debugging |
| Background job failed after retries | `error` | Needs investigation |

## Incident Debugging Checklist

When designing logs, verify you can answer:

- [ ] **Who** — Can filter to specific user/org/account?
- [ ] **What** — Can identify the exact operation that failed?
- [ ] **When** — Can narrow to specific time window?
- [ ] **Why** — Is error context captured (reason, upstream cause)?
- [ ] **Where** — Can trace across services via correlation ID?

**Post-incident:** Add the logs you wished you had.
