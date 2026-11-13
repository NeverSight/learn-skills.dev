---
name: kafka-event-backbone-patterns
description: Build Kafka-based event backbones with partitioning, schema evolution, consumer groups, and replay-safe processing.
disable-model-invocation: true
---

# Kafka Event Backbone Patterns

## Use When

- Domain events drive cross-service workflows
- High-throughput async integration is required

## Workflow

1. Define topic contracts and versioning
2. Choose partitioning keys for ordering needs
3. Implement idempotent consumers and DLQ topics
4. Configure retention and compaction policies
5. Run replay and lag recovery drills

## Required Checks

- Consumers handle duplicates safely
- Schema changes are compatible
- Lag alerts exist with actionable thresholds
- Replay procedures tested in non-production

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
