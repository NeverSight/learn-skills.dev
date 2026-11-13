---
name: performance-and-load-testing-fullstack
description: Run performance and load tests across UI-critical APIs with realistic traffic models and SLO validation.
disable-model-invocation: true
---

# Performance And Load Testing Fullstack

## Use When

- Latency or scale issues under peak load
- Major release affects critical journeys

## Workflow

1. Define workload models per persona
2. Script API and browser-level tests
3. Run baseline and regression comparisons
4. Identify bottlenecks and tune autoscaling
5. Document capacity headroom and limits

## Required Checks

- SLO targets met under expected peak
- Error rate within budget during test
- Autoscaling responds within target time
- Results attached to release decision

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
