---
name: distributed-systems-basics
description: "Distributed-systems workflow for failure-mode analysis, consistency choices, and reliability primitive selection across networked components. Use when correctness depends on partitions, retries, timeouts, ordering, or partial failures; do not use for single-process implementation details only."
---

# Distributed Systems Basics

## Overview
Use this skill to reason about correctness and reliability in systems where network faults and partial failures are normal.

## Scope Boundaries
- Multi-service workflows require explicit consistency and ordering guarantees.
- Retry/timeout/duplicate-message behavior can change business correctness.
- Teams need to define reliability primitives before implementation or rollout.

## Shared References
- Failure mode and consistency rules:
  - `references/failure-mode-consistency-rules.md`

## Templates And Assets
- Distributed flow risk template:
  - `assets/distributed-flow-risk-template.md`

## Inputs To Gather
- Component boundaries and communication patterns.
- Consistency and ordering requirements per workflow.
- Failure scenarios (partition, timeout, duplicate, out-of-order, stale read).
- Recovery and observability capabilities.

## Deliverables
- Failure-mode map and risk ranking.
- Consistency decision record per critical flow.
- Reliability mechanism selection (retry, idempotency, backoff, timeout).
- Validation plan (fault injection and invariant checks).

## Workflow
1. Capture critical flows with `assets/distributed-flow-risk-template.md`.
2. Map failure assumptions and consistency requirements per flow.
3. Select reliability primitives using `references/failure-mode-consistency-rules.md`.
4. Define observability and recovery behavior.
5. Validate assumptions with targeted failure tests and invariant checks.

## Quality Standard
- Critical flows have explicit consistency and ordering rules.
- Retry/timeout semantics are bounded and intentional.
- Idempotency strategy exists where at-least-once delivery is possible.
- Failure handling is observable and testable.

## Failure Conditions
- Stop when consistency assumptions are implicit or contradictory.
- Stop when retries/timeouts can amplify failure unboundedly.
- Escalate when critical failure modes have no mitigation path.
