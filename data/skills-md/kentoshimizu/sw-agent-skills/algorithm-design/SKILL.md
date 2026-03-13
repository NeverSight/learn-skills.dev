---
name: algorithm-design
description: "Design algorithms by modeling constraints, enumerating candidate strategies, proving correctness, and selecting data structures with explicit tradeoffs. Use when implementation success depends on algorithm choice or decomposition under unclear constraints, from vague outcome requests to concrete directives; do not use for persistence schema or deployment topology decisions."
---

# Algorithm Design

## Overview
Use this skill to produce an implementable algorithm decision with explicit correctness reasoning and tradeoff analysis.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Objective, required outputs, and correctness conditions.
- Input constraints (size ranges, distribution, adversarial cases, update/query patterns).
- Resource budgets (latency, throughput, memory) and operational constraints.
- Mutation/concurrency requirements and ordering guarantees.

## Deliverables
- Problem model with assumptions, invariants, and edge-case catalog.
- Candidate strategy comparison (pros/cons and applicability bounds).
- Selected algorithm and data-structure decision with correctness argument.
- Risk list and follow-up verification plan.

## Quality Standard
- Assumptions are explicit, measurable, and linked to requirement context.
- Correctness argument includes invariant/termination reasoning or equivalent proof sketch.
- Selected and rejected options include complexity and operability tradeoffs.
- Data-structure choices are justified by access/mutation patterns.
- Edge cases and failure modes are identified before implementation.

## Workflow
1. Formalize the problem, constraints, and success criteria.
2. Enumerate candidate strategies at the same abstraction level.
3. Evaluate correctness risk, complexity, and implementation/operational tradeoffs.
4. Select algorithm and data structures with explicit rationale.
5. Define edge-case tests and evidence needed to validate the decision.

## Failure Conditions
- Stop when constraints are unknown or contradictory.
- Stop when no candidate has a defensible correctness argument.
- Escalate when feasible options conflict with mandatory resource budgets.
