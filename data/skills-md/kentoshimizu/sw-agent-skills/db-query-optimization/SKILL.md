---
name: db-query-optimization
description: "Query optimization workflow for reducing latency and resource cost through plan-aware rewrites and access-path improvements. Use when hot-path query behavior is the bottleneck; do not use for conceptual schema redesign without workload evidence."
---

# DB Query Optimization

## Overview
Use this skill to improve query performance based on execution evidence, not intuition.

## Scope Boundaries
- Hot-path latency or database CPU/IO usage is query-bound.
- Query plans are unstable across parameter distributions.
- Workload changes expose previously acceptable query anti-patterns.

## Core Judgments
- Dominant bottleneck: scan cost, join explosion, sort spill, lock wait, network round trips.
- Rewrite scope: query shape, index changes, schema adjustment, or materialization.
- Plan stability and parameter-sensitivity risk.
- Correctness risk from aggressive rewrite or approximation.

## Practitioner Heuristics
- Start from actual execution plans and runtime metrics.
- Optimize the highest-impact query families, not one-off outliers.
- Sargability and predicate selectivity usually dominate early wins.
- Keep optimization readable; opaque SQL hacks create long-term maintenance debt.

## Workflow
1. Identify high-impact queries by frequency and user/business impact.
2. Capture plan/runtime evidence under representative parameters.
3. Propose rewrites and access-path changes with expected effects.
4. Compare candidates for latency gain versus complexity and risk.
5. Roll selected change and monitor plan stability and resource usage.
6. Record conditions that should trigger re-optimization.

## Common Failure Modes
- Tuning for small dev datasets misleads production behavior.
- Index-only fixes mask poor query shape.
- Query changes improve p50 while degrading tail latency.

## Failure Conditions
- Stop when no representative workload evidence is available.
- Stop when optimization changes correctness semantics.
- Escalate when required performance target is unattainable without model changes.
