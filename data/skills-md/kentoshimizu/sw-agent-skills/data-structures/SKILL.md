---
name: data-structures
description: "Select data structures using explicit access patterns, mutation behavior, memory limits, and concurrency constraints. Use when implementation correctness or performance depends on choosing between alternatives (array/map/heap/tree/queue/set) under real workload assumptions; do not use for persistence schema or deployment topology decisions."
---

# Data Structures

## Overview
Use this skill to choose data structures with explicit tradeoffs, then justify the choice with workload assumptions and failure modes.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Required operations (`lookup`, `insert`, `delete`, `scan`, `range`, `top-k`).
- Read/write ratio and mutation frequency.
- Data volume now and forecast at peak.
- Latency/memory constraints and concurrency model.

## Deliverables
- Candidate structure comparison with tradeoffs.
- Selected structure and rationale tied to workload.
- Risk list (memory blowup, contention, degeneration cases).
- Verification plan (microbenchmarks and edge-case tests).

## Quick Decision Examples
- Frequent key lookup + updates: `hash map` (+ collision strategy).
- Sorted range queries: `balanced tree` or ordered index.
- Top-N / priority scheduling: `heap`.
- FIFO work pipeline: `queue` (bounded if backpressure is needed).
- Membership checks with low memory: `bitset`/Bloom filter (with false-positive caveat).

## Quality Standard
- Choice is tied to actual operation mix, not preference.
- Complexity claims include worst/average behavior assumptions.
- Memory growth and peak usage are estimated.
- Concurrency implications are explicit (lock scope, contention hotspots).

## Workflow
1. Define workload model and required guarantees.
2. Enumerate feasible structures at the same abstraction level.
3. Compare complexity, memory, and concurrency behavior.
4. Select one and document rejection reasons for others.
5. Define benchmark and edge-case validation plan.

## Failure Conditions
- Stop when workload assumptions are missing or contradictory.
- Stop when chosen structure cannot satisfy mandatory operations.
- Escalate when memory or contention risk is unbounded at target scale.
