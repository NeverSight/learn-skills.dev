---
name: monolith-to-microservices-migration-strategy
description: Plan and execute safe migration from monolith to microservices using strangler patterns, anti-corruption layers, and phased cutover controls. Use when modernizing large legacy systems.
disable-model-invocation: true
---

# Monolith To Microservices Migration Strategy

## Use When

- Legacy systems block release speed and scalability
- Teams need phased modernization with low business risk

## Workflow

1. Baseline current architecture, hotspots, and release bottlenecks.
2. Prioritize extraction candidates by business value and coupling.
3. Use strangler facade and anti-corruption layer for safe coexistence.
4. Migrate data and traffic incrementally with rollback guards.
5. Retire monolith paths only after parity and reliability proof.

## Required Checks

- Coexistence model between legacy and new services is explicit
- Migration slices are reversible with clear rollback triggers
- Consumer-facing behavior parity is validated continuously

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

- Migration advances in measurable low-risk increments
- Legacy footprint decreases without service disruption
