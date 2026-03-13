---
name: algorithm-complexity-analysis
description: "Analyze candidate algorithms for time/space complexity, scalability limits, and resource-budget fit (CPU, memory, I/O, concurrency). Use when feasibility depends on input growth or latency/memory constraints and quantitative bounds are required before implementation; do not use for persistence schema or deployment topology decisions."
---

# Algorithm Complexity Analysis

## Overview
Use this skill to quantify whether candidate approaches can meet performance and resource constraints at expected scale.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Candidate algorithms and dominant operations.
- Input-scale assumptions (current, expected, and stress ranges).
- Resource budgets (latency targets, throughput targets, memory limits).
- Runtime context (I/O patterns, cache behavior, concurrency contention).

## Deliverables
- Complexity report with worst-case, average-case, and amortized bounds (as applicable).
- Memory and auxiliary-space analysis, including peak usage assumptions.
- Budget-fit assessment and scalability breakpoints.
- Recommendation with residual risk and monitoring triggers.

## Quality Standard
- Complexity claims are tied to explicit assumptions and units.
- Dominant operations and constants relevant at target scale are identified.
- CPU, memory, I/O, and contention effects are addressed where applicable.
- Analysis states confidence level and uncertainty sources.
- Decision includes conditions that would invalidate the current choice.

## Workflow
1. Define workload model, scale assumptions, and performance budgets.
2. Derive formal bounds for each candidate's critical operations.
3. Evaluate real-world cost drivers (constants, I/O, cache, contention).
4. Compare candidates against budgets and identify breakpoints.
5. Publish recommendation, residual risks, and re-evaluation triggers.

## Failure Conditions
- Stop when workload/scale assumptions are missing.
- Stop when dominant cost drivers are unmodeled.
- Escalate when no candidate can satisfy mandatory budgets.
