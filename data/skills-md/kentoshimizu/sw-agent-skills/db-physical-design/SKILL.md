---
name: db-physical-design
description: "Physical database design workflow for storage layout, partitioning, engine settings, and hardware-aware performance behavior. Use when sustained workload efficiency depends on physical data organization; do not use for conceptual modeling tasks."
---

# DB Physical Design

## Overview
Use this skill to align storage structures with workload shape, growth patterns, and operational constraints.

## Scope Boundaries
- Data volume or access distribution creates storage and latency pressure.
- Partitioning or table layout decisions affect manageability.
- Engine-specific behavior requires deliberate configuration.

## Core Judgments
- Partitioning strategy (range/hash/list/hybrid) and key choice.
- Hot/cold data tiering and archival layout.
- Table/index storage parameters by engine characteristics.
- Maintenance strategy for bloat, vacuum/reorg, and statistics.

## Practitioner Heuristics
- Partition by access and lifecycle behavior, not by calendar habit.
- Keep partition count operationally manageable.
- Co-locate frequently joined data only when it materially improves hot paths.
- Engine tuning must follow measured workload and failure history, not defaults folklore.

## Workflow
1. Profile data growth, access skew, and latency bottlenecks.
2. Evaluate physical layout options against workload and operations cost.
3. Select partition and storage strategies with explicit trade-offs.
4. Define maintenance cadence for statistics and storage health.
5. Document scaling and re-partitioning triggers.

## Common Failure Modes
- Partition key chosen without considering future rebalance complexity.
- Excessive small partitions degrade planner and maintenance performance.
- Storage tuning changes applied without workload baseline.

## Failure Conditions
- Stop when physical layout has no clear workload rationale.
- Stop when partition strategy cannot support retention/archival requirements.
- Escalate when operational maintenance burden exceeds team capacity.
