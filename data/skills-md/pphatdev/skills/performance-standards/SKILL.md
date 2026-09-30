---
name: performance-standards
description: Load this skill when performance matters - optimization work, suspected regressions, resource-sensitive code paths, or capacity planning.
user-invocable: true
---

# Performance Standards

Category: Rules (Governance)

## Purpose

Keep the system inside its performance budgets, and make every optimization
an evidence-driven decision rather than an instinct.

## The prime directive

**Measure before optimizing.** Identify the actual hot path with a
profiler or tracing before changing a line. Most code is cold; optimizing
cold code trades readability for nothing observable. "It feels slow" is a
hypothesis, not a measurement.

## Workflow

1. **Define the budget.** Latency (p50 and p95 - p95 is the contract,
   p50 is vanity), memory, payload size, bundle size, query count per
   request. Without a number, "faster" cannot be verified.
2. **Measure the baseline.** Under realistic data volume - a query plan
   with 10 rows proves nothing about 10 million.
3. **Find the hot path.** Profile; do not guess. Common real culprits:
   N+1 query patterns, synchronous I/O inside loops, loading entire
   collections to filter in memory, missing indexes on the actual query
   shape, repeated parsing/serialization, unbounded caches.
4. **Optimize in order of leverage:** algorithm/data-model change >
   query/index fix > caching (with explicit invalidation rules) >
   batch or parallelize I/O > micro-optimization (last resort).
5. **Re-measure and report** before/after numbers against the budget, in
   the same conditions as the baseline. An optimization without a measured
   win is complexity added for free.

## Regression protocol

- Suspected regression: bisect to the change (recent `git log` first),
  measure before and after the offending commit, then decide fix-forward
  or revert. Reverting a regression is not a defeat; shipping p95
  degradation to users is.
- Where feasible, add a guard: a benchmark or test that fails if the
  budget is exceeded again.

## Standards

- Caching requires a written invalidation rule; a cache without one is a
  future correctness bug.
- Changes that trade correctness, security, or readability for
  unmeasured speed are rejected on review.
- Allocations and abstractions in hot loops must justify themselves; the
  justification is a measurement, not an opinion.
