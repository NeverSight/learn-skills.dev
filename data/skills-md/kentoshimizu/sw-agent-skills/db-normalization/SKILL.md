---
name: db-normalization
description: "Normalization workflow for reducing update anomalies while balancing query practicality and domain invariants. Use when schema redundancy and inconsistency risk need deliberate trade-off decisions; do not use for physical indexing-only tasks."
---

# DB Normalization

## Overview
Use this skill to decide normalization depth intentionally, preserving integrity without ignoring workload realities.

## Scope Boundaries
- Duplicate mutable data causes inconsistency bugs.
- Schema design needs explicit normalization versus denormalization trade-offs.
- Teams are preparing for domain growth and evolving query patterns.

## Core Judgments
- Normal form target per entity group (3NF/BCNF and justified deviations).
- Redundancy acceptance criteria and ownership.
- Denormalization scope and refresh semantics.
- Constraint placement for anomaly prevention.

## Practitioner Heuristics
- Normalize data that changes frequently or has strict consistency needs.
- Denormalize only for measured read-path benefit with explicit maintenance strategy.
- Prefer derived data pipelines over ad hoc duplicated writable columns.
- Document who repairs divergence when denormalized copies drift.

## Workflow
1. Identify update anomalies and redundancy hotspots.
2. Model normalized alternatives and expected consistency behavior.
3. Evaluate read/write trade-offs for selective denormalization.
4. Define synchronization semantics for intentional redundancy.
5. Document accepted anomalies and mitigation mechanisms.

## Common Failure Modes
- Denormalization introduced without ownership of refresh logic.
- Over-normalization creates excessive joins for latency-critical paths.
- Hidden duplicated columns diverge silently over time.

## Failure Conditions
- Stop when anomaly prevention responsibilities are undefined.
- Stop when denormalization has no measurable performance rationale.
- Escalate when required consistency cannot be maintained at chosen form.
