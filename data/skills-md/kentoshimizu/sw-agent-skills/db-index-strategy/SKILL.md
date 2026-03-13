---
name: db-index-strategy
description: "Index strategy workflow for balancing read latency, write amplification, and plan stability on critical query paths. Use when query performance depends on index design trade-offs; do not use for high-level conceptual modeling."
---

# DB Index Strategy

## Overview
Use this skill to choose indexes that improve real workloads while controlling write and storage costs.

## Scope Boundaries
- Query latency hotspots are driven by access-path inefficiency.
- New query patterns or sort requirements are introduced.
- Existing indexes show redundancy, bloat, or unstable plans.

## Core Judgments
- Query-path priority by business impact and frequency.
- Composite key order by filter selectivity and sort usage.
- Covering/partial/functional index suitability by engine capability.
- Write amplification and maintenance cost tolerance.

## Practitioner Heuristics
- Indexes should be justified by concrete query families, not single ad hoc queries.
- Composite index order follows filter-first then sort semantics.
- Prefer fewer high-value indexes over broad index proliferation.
- Consider plan stability across parameter distribution, not one explain sample.

## Workflow
1. Rank critical queries by frequency, latency impact, and SLA relevance.
2. Inspect current plans and identify scans, misestimation, and sort spills.
3. Propose candidate indexes with expected plan effects.
4. Evaluate write/maintenance/storage impact for each candidate.
5. Decide new, modified, and removable indexes as one portfolio.
6. Record assumptions that require re-evaluation as data distribution changes.

## Common Failure Modes
- Indexes tuned for one tenant or parameter pattern only.
- Redundant indexes remain after query evolution.
- Index design ignores heavy write paths and causes throughput collapse.

## Failure Conditions
- Stop when index choices are not tied to prioritized workload.
- Stop when write amplification risk is unbounded.
- Escalate when plan stability remains poor after viable candidates.
