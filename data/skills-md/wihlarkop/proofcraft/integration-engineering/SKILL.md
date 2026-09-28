---
name: integration-engineering
description: >-
  Design, implement, or review safe integration with external systems and third-party APIs. Use
  for external contracts, data mapping, anti-corruption boundaries, credentials/auth handoff,
  rate limits, retries/timeouts, webhooks/polling, reconciliation, and partial failure. Keep the
  external provider model from leaking into the application's domain and report sibling concerns
  instead of taking over orchestration.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Integration Engineering

Treat an external system as an unreliable boundary with somebody else's domain model.

## Workflow

1. Inspect the external contract, ownership, authentication mechanism, quotas/rate limits, and actual business job.
2. Map external identifiers/statuses/objects into an internal boundary model. Avoid allowing vendor-specific DTOs or lifecycle semantics to become the application's domain by accident.
3. Define timeout, retry, idempotency, duplicate, and partial-failure behavior for each operation that can repeat.
4. Choose webhook, polling, callback, or async/event mechanisms from the provider's actual guarantees and product latency needs.
5. Define reconciliation: how the application detects and repairs missed callbacks, stale local state, or ambiguous outcomes.
6. Identify observability needed to answer integration-specific questions without logging secrets/sensitive payloads unnecessarily.
7. Report supporting security, async-work, database, privacy, or reliability concerns to the active core workflow when they materially apply.

## Stop

Stop when mapping, ownership, failure/retry, reconciliation, and evidence are explicit enough to implement or review the integration safely.
## Reference Guide

Load only the references needed for the current task:

- [boundary mapping](references/boundary-mapping.md)
- [failure rate limits](references/failure-rate-limits.md)
- [webhooks reconciliation](references/webhooks-reconciliation.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
