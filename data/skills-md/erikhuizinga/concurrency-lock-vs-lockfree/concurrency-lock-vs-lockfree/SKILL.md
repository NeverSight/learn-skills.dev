---
name: concurrency-lock-vs-lockfree
description: Language-agnostic guidance for lock-vs-lock-free (lockfree/lockless) concurrency decisions, atomic primitives, and memory-ordering risk evaluation. Use when tasks mention atomics, CAS/compare-and-swap, lock-free queues/stacks/pools, memory ordering or memory fences, ABA, weak-memory behavior, or replacing mutexes/locks for performance. Also use when designing custom synchronization primitives or debugging rare concurrency bugs caused by thread interleavings.
---

# Concurrency: Lock vs Lock-Free

Prefer higher-level concurrency primitives and lock-based designs unless there
is strong evidence they are insufficient.

Use this playbook to make explicit, auditable decisions.

## Related Terminology

The following terms are closely related to this skill's scope and intent:

- lockfree
- lock free
- lockless
- compare-and-swap
- CAS loop
- atomic operations
- mutex vs lock-free
- synchronization strategy
- memory ordering
- ABA problem
- linearizability
- hazard pointers

## Decision Process

1. Identify the shared state and required invariants.
2. Start from existing high-level components in the target language/runtime.
3. Evaluate lock-based designs first.
4. Escalate to lock-free atomics only when all lock-based options are proven
   inadequate for the target throughput/latency/concurrency profile.
5. If lock-free is chosen, require explicit handling of memory ordering,
   lifetime/reclamation, ABA, and interleavings.

## Default Recommendation

- Prefer existing concurrency libraries and runtime primitives.
- Prefer mutexes/locks over custom lock-free algorithms.
- Prefer partitioning/sharding, batching, and thread-local buffering before
  introducing lock-free shared structures.

## Lock-Free Escalation Gate

Do not recommend custom lock-free algorithms unless all are true:

1. Performance evidence shows lock contention is the bottleneck.
2. Simpler alternatives (sharding, batching, lock scope reduction, library
   data structures) were evaluated and rejected with evidence.
3. The team has memory-model expertise for the target language and hardware.
4. A correctness plan exists: formal reasoning/tools + stress/fuzz strategy.
5. Ownership/lifetime and reclamation strategy is explicit.

## Required Risk Checklist (When Atomics Are Involved)

- Memory ordering:
  - Specify why each atomic operation uses that ordering.
  - Avoid relaxed ordering unless a proof/explanation exists.
- Cross-platform behavior:
  - Do not assume x86 behavior represents ARM/POWER behavior.
- Non-atomic sequences:
  - Treat multi-step atomic sequences as interruptible.
- Lifetime and reclamation:
  - Define safe reclamation (hazard pointers, epochs/RCU-like patterns, etc.).
- ABA exposure:
  - Detect and mitigate ABA risks in CAS loops.
- Progress guarantees:
  - State lock-free/wait-free/obstruction-free claim precisely.
- Maintainability:
  - Keep algorithm and invariants understandable to non-authors.

## Performance Guidance

Before recommending lock-free structures, prioritize:

1. Data layout and cache locality improvements.
2. Lock partitioning (shard by key/hash/core).
3. Reduced critical section scope.
4. Batched updates and per-thread/local aggregation.
5. Existing concurrent containers in mature libraries.

## Testing and Verification Guidance

Do not treat unit tests as sufficient for lock-free correctness.

Require:

1. Stress testing under heavy concurrency and long runs.
2. Race detection tooling where applicable.
3. Variation across compilers, optimization levels, and architectures.
4. Invariant assertions and linearizability reasoning where feasible.
5. Formal/specialized checkers for non-trivial lock-free algorithms.

## Response Format

When advising, produce:

1. Decision:
   - `Use locks/high-level primitives` or `Lock-free justified`.
2. Rationale:
   - Evidence-backed tradeoffs, not preferences.
3. Safer alternative:
   - Concrete lock-based/library-based option first.
4. If lock-free:
   - Required ordering model, reclamation plan, ABA mitigation, and test plan.
5. Validation:
   - Benchmarks + correctness checks needed before adoption.

## Language-Specific Mapping

For concrete primitive choices by language, use
`references/language-mapping.md`.

## Source Credit

Primary source guidance adapted from Abseil:
`https://abseil.io/docs/cpp/atomic_danger`
