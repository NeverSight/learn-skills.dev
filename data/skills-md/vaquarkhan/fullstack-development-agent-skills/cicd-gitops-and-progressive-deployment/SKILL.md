---
name: cicd-gitops-and-progressive-deployment
description: Deliver fullstack changes with CI/CD pipelines, GitOps promotion, and progressive deployment strategies.
disable-model-invocation: true
---

# Cicd Gitops And Progressive Deployment

## Use When

- Teams need repeatable release automation
- Manual deploys cause drift and risk

## Workflow

1. Define pipeline stages and quality gates
2. Use infrastructure and app GitOps repos
3. Implement canary or blue-green where needed
4. Automate smoke tests after promotion
5. Document rollback automation

## Required Checks

- Pipeline blocks on failed gates
- Environment promotion is auditable
- Rollback executed successfully in drill
- Deployment artifacts immutable and traceable

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
