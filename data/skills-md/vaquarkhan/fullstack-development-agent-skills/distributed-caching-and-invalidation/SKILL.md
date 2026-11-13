---
name: distributed-caching-and-invalidation
description: Design distributed caching with reliable invalidation and consistency controls across UI and backend services. Use when optimizing latency-sensitive fullstack workloads.
disable-model-invocation: true
---

# Distributed Caching And Invalidation

## Use When

- Read-heavy paths need lower latency
- Cache coherence issues are causing stale user data

## Workflow

1. Classify cacheable data and staleness tolerance.
2. Define cache keys, TTL, and ownership.
3. Implement write-through or invalidation strategy.
4. Add fallback behavior for cache misses and outages.
5. Observe hit ratio, stale reads, and stampede risk.

## Required Checks

- Invalidation path exists for every mutating action
- Cache outage does not break core user flows
- Metrics include hit rate, miss rate, and stale-read incidents

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

- Performance improves without correctness regressions
- Cache behavior is predictable under failure conditions
