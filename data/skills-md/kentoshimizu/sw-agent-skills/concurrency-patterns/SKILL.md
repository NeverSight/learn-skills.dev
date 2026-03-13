---
name: concurrency-patterns
description: "Design and review concurrency strategy for shared state, coordination, and contention control. Use when parallel execution or async coordination introduces race/deadlock/liveness risk and explicit pattern selection is required; do not use for persistence schema or deployment topology decisions."
---

# Concurrency Patterns

## Overview
Use this skill to choose concurrency mechanisms that preserve correctness under load and failure.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Shared state model and mutation frequency.
- Read/write patterns and contention expectations.
- Ordering, consistency, and latency requirements.
- Failure/timeout/retry semantics in concurrent flows.

## Deliverables
- Selected concurrency pattern with rationale.
- Invariant and liveness assumptions.
- Risk list (race, deadlock, starvation, contention collapse).
- Verification plan (stress, race, soak, failure-injection tests).

## Pattern Selection Cheatsheet
- `single-writer queue/actor`: high contention mutable state.
- `fine-grained lock`: moderate contention with strict in-process consistency.
- `lock-free/CAS`: low-latency hot path with careful ABA/memory-ordering handling.
- `immutable snapshot + swap`: read-heavy workloads.
- `idempotent async workflow`: distributed coordination with retries.

## Quick Example
- Problem: concurrent balance updates causing lost writes.
- Anti-pattern: read-modify-write without serialization.
- Safer options:
  - single-writer actor per account,
  - optimistic concurrency with version check + bounded retry.

## Quality Standard
- Correctness invariants are explicit and testable.
- Deadlock/starvation prevention strategy is defined.
- Contention behavior is characterized at expected scale.
- Timeout/retry/cancellation behavior is deterministic.
- Selected pattern includes clear operational monitoring signals.

## Workflow
1. Define correctness invariants and liveness constraints.
2. Map workload and contention profile.
3. Compare candidate patterns with tradeoffs.
4. Select pattern and define failure/timeout semantics.
5. Define targeted stress/race test strategy.

## Failure Conditions
- Stop when invariants cannot be preserved by selected pattern.
- Stop when deadlock or starvation risk is unbounded.
- Escalate when required throughput conflicts with safe coordination model.
