---
name: mobile-api-and-offline-sync-patterns
description: Design mobile-friendly APIs with pagination, sync, conflict resolution, and resilient offline-first behavior.
disable-model-invocation: true
---

# Mobile Api And Offline Sync Patterns

## Use When

- Mobile clients consume backend APIs
- Intermittent connectivity is common

## Workflow

1. Define sync protocol and conflict rules
2. Use cursor-based pagination for large datasets
3. Implement optimistic UI with server reconciliation
4. Add push notification hooks for sync completion
5. Load test mobile-specific API patterns

## Required Checks

- Conflict resolution behavior is deterministic
- Auth tokens refreshed safely on mobile
- Payload sizes optimized for mobile networks
- Offline queue replay tested

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
