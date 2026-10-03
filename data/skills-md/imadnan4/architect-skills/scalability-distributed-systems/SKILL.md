---
name: scalability-distributed-systems
description: How to build systems that survive PRODUCTION. Use when designing horizontal scaling, statelessness, caching, queues, event-driven architecture, CQRS, sagas, outbox, circuit breakers, bulkheads, graceful degradation, multi-region, zero-downtime deploys.
when_to_use: |
  - horizontal scaling, statelessness, caching strategies
  - queues, event-driven architecture, CQRS, saga, outbox
  - circuit breakers, bulkheads, graceful degradation, multi-region, zero-downtime deploys
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Scalability & Distributed Systems

A scalable system is not one that handles a million users — it is one that **keeps operating
correctly as demand grows**. Optimize for survivability, not just speed. Assume success *and*
failure; design for both.

## Vertical vs horizontal

| | Vertical | Horizontal |
|---|---|---|
| Pros | simple, fast, cheap initially | fault-tolerant, elastic, unlimited |
| Cons | hard limit, SPOF | complexity, sync, networking |

Default MVP = vertical. Move to horizontal (stateless) when vertical hits its limit.

## Stateless services (default)

App servers remember **nothing**. State lives in DB / cache / object storage / queue / session
store — never local memory. Benefits: horizontal scale, rolling deploys, crash recovery, LB.

## Caching

Never cache first — measure first. Layers: browser → CDN → reverse proxy → Redis → app → DB.

- **Cache-aside** (default): miss → DB → store → return.
- **Write-through:** DB + cache together (consistency matters).
- **Write-back:** cache → async DB (perf, more complexity).
- **Invalidation** (hardest problem): every cache needs TTL + invalidation + ownership + fallback.

## Queues & resilience

- **Queues** absorb pressure and isolate failures; slow work is always async (email, encoding,
  indexing, AI, imports). Producer → Queue → Worker → Retry → **Dead Letter Queue** (never lose work).
- **Retries:** exponential backoff + jitter + limits + circuit breaker. Never retry immediately.
- **Idempotent workers:** same job twice = same result (payments, invoices, emails…).
- **Workflow engines** (Temporal, Trigger.dev, Inngest) for tasks spanning minutes/hours with
  retries, checkpoints, human approval.
- **Circuit breaker:** stop calling a failing dependency, recover later.
- **Bulkhead:** isolate critical workloads (payments must not compete with image processing).

## Event-driven & distributed patterns

- **Event-driven:** one event, many consumers (`OrderPlaced` → Inventory, Email, Analytics, Fraud…).
  Publisher knows nothing about consumers.
- **CQRS:** split commands (write) from queries (read) only when patterns differ significantly.
- **Event sourcing:** store events, not state (finance/audit/compliance). Avoid for ordinary SaaS.
- **Saga:** distributed transaction via compensation, not rollback.
- **Outbox:** write the event *inside* the DB transaction, then a worker publishes — guarantees
  consistency (no "DB written, publish failed").

## Distributed fundamentals

- **CAP:** can't maximize consistency + availability + partition tolerance. Choose deliberately.
- **Eventual consistency** is fine for search/analytics/notifications/feeds — **not** for payments/
  wallets/inventory/auth.
- **Multi-region** only for global users / DR / compliance / latency. **DB replication:** primary →
  read replicas (never write to replicas).

## Deployment & ops

- **Zero-downtime:** rolling / blue-green / canary + feature flags (deploy ≠ release).
- **Health checks:** readiness, liveness, startup. **Observability:** logs, metrics, traces, events.
- **SLOs:** availability, latency, error rate, RTO, RPO — measured continuously.
- **Failure philosophy:** servers restart, containers die, networks partition, caches vanish, clouds
  fail. Every component must recover automatically.

## Architecture review (pre-launch)

- [ ] Stateless · horizontally scalable · queue isolation · retry strategy · DLQ
- [ ] Circuit breaker · timeouts · health checks · observability · autoscaling
- [ ] Graceful degradation · backup strategy · DR · capacity & cost estimate · rollback plan

## Architecture decision tree

```
Load increasing?
  ↓
Vertical limit reached? → YES → Horizontal (stateless)
Need shared state? → DB / Cache / Queue (never local memory)
Slow work? → Queue (async) → Dead Letter Queue
Cross-service transaction? → Saga + Outbox
Task needs retries/checkpoints/minutes? → Workflow engine
Dependency flaky? → Circuit breaker
```

## Anti-patterns

- ❌ Stateful app servers (local memory)
- ❌ Synchronous slow work
- ❌ Distributed transactions across services
- ❌ Caching without invalidation strategy
- ❌ No Dead Letter Queue (losing work)
- ❌ Immediate retries (retry storms) · requiring downtime for deploys

## Architecture prompts

- Can this scale / recover / fail independently?
- Should this be async / event / queue / workflow?
- What is the cache invalidation strategy?
- What happens when a dependency dies?
- Is critical work isolated (bulkhead)?
