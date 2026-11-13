---
name: microservice-patterns-outbox-and-cdc
description: Publish reliable domain events using outbox and CDC patterns to avoid dual-write failures. Use when transactional updates must trigger downstream processing.
disable-model-invocation: true
---

# Microservice Patterns Outbox And CDC

## Use When

- Service writes to database and emits events
- Event delivery reliability is critical for downstream systems

## Workflow

1. Store domain event in outbox table in same transaction as data change.
2. Relay outbox entries through CDC or polling worker.
3. Publish to broker with ordering and partition strategy.
4. Track delivery state and retries with poison-message handling.
5. Add replay and reconciliation jobs for missed events.

## Required Checks

- No dual-write path bypasses outbox transaction
- Relay worker is idempotent and restart-safe
- Backlog metrics and alert thresholds are configured

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

- Event publishing survives process and network failures
- Consumers can recover using replay-safe semantics
