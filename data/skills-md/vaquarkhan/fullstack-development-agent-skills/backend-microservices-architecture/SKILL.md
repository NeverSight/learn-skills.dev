---
name: backend-microservices-architecture
description: Design and implement backend microservices with explicit boundaries, resilience, observability, and safe deployment patterns. Use when the user asks for service design, microservice APIs, reliability, scaling, or incident-hardening.
disable-model-invocation: true
---

# Backend Microservices Architecture

## Use When

- Creating a new microservice
- Refactoring monolith logic into services
- Adding reliability and operability controls

## Workflow

1. Define service boundary, ownership, and data responsibilities.
2. Define API contracts and compatibility policy.
3. Implement idempotency and failure handling.
4. Add telemetry: logs, metrics, traces.
5. Prove readiness with load/error tests and rollback plan.

## Required Checks

- API and event contracts are versioned
- Timeouts, retries, and circuit breakers are explicit
- Dead-letter handling exists for async failures
- Health checks and SLOs are documented
- Rollout strategy includes canary or phased release

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

- Workflow decisions are documented and implementation-ready
- Validation evidence exists for quality, reliability, and compatibility
- Operational readiness and rollback expectations are explicit

