---
name: compliance-gdpr-and-data-privacy-fullstack
description: Implement GDPR-oriented privacy controls including consent, retention, export, and deletion across UI and backend.
disable-model-invocation: true
---

# Compliance Gdpr And Data Privacy Fullstack

## Use When

- EU users or privacy-regulated data
- Data subject rights must be supported

## Workflow

1. Map personal data flows end-to-end
2. Implement consent and preference management
3. Define retention and deletion workflows
4. Support export and erasure requests
5. Document lawful basis and processors

## Required Checks

- Deletion propagates to downstream systems
- Consent changes reflected in processing
- Audit trail exists for privacy operations
- DPIA or equivalent review completed where required

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
