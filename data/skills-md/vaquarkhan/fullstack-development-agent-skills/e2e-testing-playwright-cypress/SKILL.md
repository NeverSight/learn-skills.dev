---
name: e2e-testing-playwright-cypress
description: Implement end-to-end testing for critical user journeys using Playwright or Cypress with CI integration.
disable-model-invocation: true
---

# E2E Testing Playwright Cypress

## Use When

- Regression risk on critical flows
- UI and API integration must be verified together

## Workflow

1. Select critical journeys and data fixtures
2. Implement stable selectors and test IDs
3. Run tests in CI on every merge
4. Quarantine flaky tests with owners
5. Integrate visual or accessibility checks where needed

## Required Checks

- Critical journeys covered in CI
- Flaky test rate tracked and reduced
- Test data isolated per run
- Failures include actionable diagnostics

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
