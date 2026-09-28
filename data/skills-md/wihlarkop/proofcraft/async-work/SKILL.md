---
name: async-work
description: >-
  Design, implement, or review background jobs, queues, events, workers, and concurrent workflows.
  Use for durable work ownership, enqueue/publish boundaries, acknowledgement, retries, idempotency,
  duplicate delivery, ordering, replay, cancellation, restart recovery, poison work, and
  backpressure. Stay broker/vendor neutral and derive semantics from the application's guarantees.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Async Work

Make progress, ownership, acknowledgement, and recovery explicit.

## Workflow

1. Identify the authoritative state and the unit of work/event.
2. Define when work becomes durable and who owns it after enqueue/publish.
3. Define acknowledgement/commit timing and what happens if the process crashes before or after that point.
4. State duplicate, ordering, concurrency, and idempotency semantics at the smallest scope that matters.
5. Define retry classification, poison-work handling, replay, and reconciliation.
6. Define cancellation/timeouts/restart recovery for long-running work.
7. Define backpressure and overload behavior when producers can outpace consumers.
8. Use broker-specific features only after the project transport is known. Do not choose Kafka/PubSub/SQS/etc. because a specialist happens to be installed.

## Stop

Stop when normal progress plus the material crash/retry/duplicate/cancellation paths are explicit and can be verified.
## Reference Guide

Load only the references needed for the current task:

- [cancellation replay backpressure](references/cancellation-replay-backpressure.md)
- [idempotency ordering](references/idempotency-ordering.md)
- [jobs messaging](references/jobs-messaging.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [authority](references/_shared/state/authority.md)
- [lifecycle](references/_shared/state/lifecycle.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
