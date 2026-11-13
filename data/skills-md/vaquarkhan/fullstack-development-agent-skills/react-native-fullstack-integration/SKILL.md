---
name: react-native-fullstack-integration
description: Integrate React Native apps with backend APIs, auth, push notifications, and release pipelines.
disable-model-invocation: true
---

# React Native Fullstack Integration

## Use When

- Mobile app shares backend with web
- Need consistent auth and API contracts

## Workflow

1. Align API contracts with web clients
2. Implement secure token storage on device
3. Configure deep links and push notification flows
4. Add over-the-air update strategy if used
5. Validate store release and rollback process

## Required Checks

- Auth flows tested on iOS and Android
- API compatibility verified against contract
- Crash and performance monitoring enabled
- Release checklist completed per store

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
