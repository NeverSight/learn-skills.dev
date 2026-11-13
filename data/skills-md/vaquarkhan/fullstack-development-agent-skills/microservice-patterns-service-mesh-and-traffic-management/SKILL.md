---
name: microservice-patterns-service-mesh-and-traffic-management
description: Manage service-to-service traffic with mesh policies for retries, timeouts, mTLS, canary, and fault isolation. Use when platform-level network controls are needed across many services.
disable-model-invocation: true
---

# Microservice Patterns Service Mesh And Traffic Management

## Use When

- Fleet-wide traffic policies need consistency
- Teams require canary and security controls without app rewrites

## Workflow

1. Define baseline traffic policy: timeout, retry budget, circuit behavior.
2. Enforce mTLS identity and authorization between services.
3. Configure canary, blue-green, or weighted routing rules.
4. Apply outlier detection and connection pool limits.
5. Monitor policy impact on latency and error budgets.

## Required Checks

- Retry policy does not amplify downstream outages
- Service identity and policy scopes are explicit
- Canary rollback can be triggered quickly

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

- Traffic behavior is controllable and observable at platform layer
- Security and release routing are repeatable across services
