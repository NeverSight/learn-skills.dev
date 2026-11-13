---
name: cqrs-and-event-sourcing-patterns
description: Apply CQRS and event sourcing for complex domains that require auditability, temporal queries, and scalable read models. Use when write and read concerns diverge significantly.
disable-model-invocation: true
---

# CQRS And Event Sourcing Patterns

## Use When

- Domain behavior requires immutable event history
- Query shapes differ heavily from command workflows

## Workflow

1. Define command model invariants and event schema strategy.
2. Persist domain events as source of truth.
3. Build projections for query-optimized read models.
4. Design replay, snapshot, and projection catch-up operations.
5. Implement versioning and backward-compatible event evolution.

## Required Checks

- Event schemas include versioning and migration policy
- Projection rebuild process is tested and bounded
- Command-side validation prevents invalid state transitions

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

- System can replay history to restore consistent state
- Query performance improves without compromising write integrity
