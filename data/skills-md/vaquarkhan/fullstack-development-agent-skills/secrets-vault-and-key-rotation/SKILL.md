---
name: secrets-vault-and-key-rotation
description: Manage secrets with vaults, rotation, and least-privilege access across environments.
disable-model-invocation: true
---

# Secrets Vault And Key Rotation

## Use When

- Credentials rotate on schedule or incident
- Multiple services share sensitive config

## Workflow

1. Centralize secrets in vault or cloud secret manager
2. Eliminate secrets from repos and images
3. Automate rotation with compatibility windows
4. Audit secret access and emergency revocation
5. Validate break-glass procedures

## Required Checks

- No plaintext secrets in source control
- Rotation drill completed successfully
- Access logs retained per policy
- Emergency revocation path tested

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
