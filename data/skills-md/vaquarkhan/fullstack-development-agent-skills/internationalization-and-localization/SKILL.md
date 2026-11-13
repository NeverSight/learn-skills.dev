---
name: internationalization-and-localization
description: Deliver multilingual products with locale-aware formatting, RTL support, and translation workflows.
disable-model-invocation: true
---

# Internationalization And Localization

## Use When

- Global user base with multiple locales
- Regulatory or market-specific content

## Workflow

1. Externalize strings and locale resources
2. Implement date, number, and currency formatting
3. Support RTL layouts where required
4. Define translation review and release process
5. Validate fallback locale behavior

## Required Checks

- Critical journeys tested in target locales
- RTL layouts verified for key screens
- Translation keys versioned with releases
- Locale detection and override behavior documented

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
