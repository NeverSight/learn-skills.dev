---
name: cloud-cost-optimization
description: Optimize cloud spend for fullstack workloads with rightsizing, autoscaling tuning, and waste elimination.
disable-model-invocation: true
---

# Cloud Cost Optimization

## Use When

- Cloud bills growing faster than usage
- Need cost accountability per team

## Workflow

1. Establish cost allocation tags and dashboards
2. Rightsize compute and storage resources
3. Tune autoscaling min/max and schedules
4. Review idle resources and retention policies
5. Set budget alerts with action owners

## Required Checks

- Top cost drivers identified and owned
- Savings changes validated against SLOs
- Budget alerts tested
- Monthly review cadence established

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
