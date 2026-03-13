---
name: graph-algorithms
description: "Graph algorithm workflow for modeling entities/relations and selecting traversal, path, ordering, or flow strategies. Use when correctness or performance depends on graph representation and algorithm choice; do not use for schema-only modeling or deployment topology planning."
---

# Graph Algorithms

## Overview
Use this skill to choose and validate graph approaches that are correct for the domain and efficient for expected scale.

## Scope Boundaries
- The problem involves reachability, shortest paths, dependencies, connectivity, matching, or flow.
- Algorithm choice materially affects correctness guarantees or runtime cost.
- Teams need explicit trade-off rationale between multiple graph approaches.

## Shared References
- Algorithm selection rules:
  - `references/graph-algorithm-selection-rules.md`

## Templates And Assets
- Problem framing template:
  - `assets/graph-problem-framing-template.md`
- Algorithm comparison template:
  - `assets/graph-algorithm-comparison-template.md`

## Inputs To Gather
- Entity/relationship model and graph directionality assumptions.
- Constraints (weighted/unweighted, cyclic/acyclic, static/dynamic updates).
- Scale expectations (nodes, edges, update/query ratio, latency budget).
- Correctness requirements and acceptable approximation/error policy.

## Deliverables
- Graph representation choice with invariants and assumptions.
- Candidate algorithm comparison with complexity and fit rationale.
- Validation plan for correctness, complexity, and edge-case handling.
- Residual risk list for scaling or approximation trade-offs.

## Workflow
1. Frame the problem using `assets/graph-problem-framing-template.md`.
2. Determine representation (adjacency list/matrix/edge list) based on scale and operations.
3. Compare candidate algorithms using `assets/graph-algorithm-comparison-template.md`.
4. Select an approach using `references/graph-algorithm-selection-rules.md`.
5. Validate with correctness tests (cycles, disconnected components, degenerate cases).
6. Measure complexity behavior under representative and worst-case workloads.
7. Publish decision rationale, constraints, and follow-up optimization actions.

## Quality Standard
- Representation and algorithm assumptions are explicit and testable.
- Complexity claims are tied to real workload characteristics.
- Edge and failure cases are validated, not inferred.
- Trade-offs between accuracy, latency, and memory are documented.

## Failure Conditions
- Stop when representation assumptions conflict with domain behavior.
- Stop when chosen algorithm fails required correctness guarantees.
- Escalate when performance requirements cannot be met with current constraints.
