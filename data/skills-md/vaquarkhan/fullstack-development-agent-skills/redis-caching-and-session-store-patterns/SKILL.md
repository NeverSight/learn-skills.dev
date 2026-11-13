---
name: redis-caching-and-session-store-patterns
description: Use Redis for caching, session storage, rate limiting, and pub/sub with clear TTL and invalidation policies.
disable-model-invocation: true
---

# Redis Caching And Session Store Patterns

## Use When

- Need low-latency session or cache layer
- Traffic spikes require shared ephemeral state

## Workflow

1. Define key naming and TTL conventions
2. Choose data structures per access pattern
3. Implement invalidation on mutating operations
4. Configure persistence and eviction policies
5. Monitor memory, hit rate, and connection saturation

## Required Checks

- Cache invalidation is defined for each write path
- Session storage is encrypted or scoped appropriately
- Failover behavior documented for cache outage
- Hot keys and memory limits reviewed

## Decision Framework

- Prefer explicit contracts and compatibility rules before implementation.
- If dependency risk is high, require timeout, retry, and fallback strategy per call path.
- If async messaging is used, require idempotency, replay, and dead-letter handling.
- If traffic patterns are volatile, require load, failover, and scaling validation before ship.

## Common Rationalizations And Rebuttals

- "Retries will handle failures automatically." -> Unbounded retries can amplify outages; use budgets.
- "We can skip runbooks for now." -> Operational ambiguity delays incident recovery.
- "Contract changes are minor." -> Small breaking changes cause broad downstream regressions.

## Evidence Pack

- Contract compatibility note and migration strategy (if applicable)
- Failure-mode test evidence for dependency degradation and recovery
- Observability snapshot (latency, error, saturation, or queue health)
- Rollout and rollback steps with clear trigger thresholds

## Exit Criteria

- Workflow is production-ready with verified evidence
- Operational and security guardrails are in place
- Release and rollback expectations are documented
