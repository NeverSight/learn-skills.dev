---
name: multi-tenant-data-isolation-patterns
description: Enforce tenant isolation across database, cache, APIs, and observability for SaaS platforms.
disable-model-invocation: true
---

# Multi Tenant Data Isolation Patterns

## Use When

- Multi-tenant SaaS with strict isolation needs
- Risk of cross-tenant data exposure

## Workflow

1. Choose isolation model per tier (row, schema, database)
2. Enforce tenant context in every data path
3. Add automated tests for cross-tenant access
4. Audit logs include tenant identifiers
5. Plan migration between isolation models

## Required Checks

- Negative tests prove isolation
- Tenant context cannot be spoofed from client
- Operational tools respect tenant boundaries
- Isolation model documented per data store

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
