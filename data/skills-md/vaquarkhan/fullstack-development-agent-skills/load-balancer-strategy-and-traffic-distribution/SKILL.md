---
name: load-balancer-strategy-and-traffic-distribution
description: Design load balancer strategy across L4 and L7 layers with health probes, weighted routing, stickiness policy, and failover behavior. Use when scaling service traffic and controlling reliability.
disable-model-invocation: true
---

# Load Balancer Strategy And Traffic Distribution

## Use When

- Traffic growth requires multi-instance distribution
- Release safety needs canary or weighted traffic control

## Workflow

1. Choose LB layer (L4 or L7) and routing algorithm by workload profile.
2. Configure health checks, failover thresholds, and connection draining.
3. Define session affinity strategy only where required.
4. Implement weighted routing for canary and blue-green rollouts.
5. Validate latency and error impact across normal and degraded scenarios.

## Required Checks

- Health checks represent real service readiness
- Failover does not route traffic to unhealthy pools
- Sticky session policy does not block horizontal scale

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

- Traffic distribution is balanced, reliable, and controllable
- Release routing is safe and reversible
