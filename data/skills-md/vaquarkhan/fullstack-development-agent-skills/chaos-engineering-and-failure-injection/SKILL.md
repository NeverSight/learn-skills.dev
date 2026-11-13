---
name: chaos-engineering-and-failure-injection
description: Validate fullstack resilience with controlled failure injection across services, data, and edge layers.
disable-model-invocation: true
---

# Chaos Engineering And Failure Injection

## Use When

- Production incidents recur under dependency failure
- SLOs require proven recovery behavior

## Workflow

1. Define failure hypotheses and blast radius
2. Run game days in staging with guardrails
3. Inject latency, error, and resource pressure
4. Measure recovery time and user impact
5. Track remediations with owners

## Required Checks

- Rollback tested during injected failures
- Alerts fire before SLO breach where possible
- Runbooks updated from experiment outcomes
- Critical paths have passing chaos scenarios

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
