---
name: java-spring-boot-microservices
description: Design and implement Java Spring Boot microservices with contract-first APIs, resilience controls, observability, and production-safe delivery. Use when users request Java backend services, Spring APIs, or microservice reliability improvements.
disable-model-invocation: true
---

# Java Spring Boot Microservices

## Use When

- Building Java Spring Boot services or APIs
- Contract-first delivery or production reliability improvements are needed

## Workflow

1. Define bounded context and service ownership.
2. Define API contract and DTO compatibility policy.
3. Implement resilience with timeout, retry, and fallback.
4. Add structured logs, metrics, and tracing.
5. Verify with contract, integration, and load tests.

## Required Checks

- Clear separation of controller, service, and persistence layers
- Idempotency for write endpoints
- Migration-safe database versioning
- Deployment and rollback readiness documented

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

