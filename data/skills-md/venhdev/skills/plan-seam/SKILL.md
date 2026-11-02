---
name: plan-seam
description: "Formulate safe multi-phase migration strategies using seams, expand-contract patterns, and feature flags to eliminate regression cascades during large-scale refactors."
disable-model-invocation: true
---

# plan-seam — Seam-Driven Refactoring & Expand-Contract Strategy

## Domain Rubric

### 1. Seam Coordinates & Isolation Mechanism
Identify interception seams at interface, dependency injection, or package boundaries. Select a zero-downtime isolation mechanism: *Interface Adapter*, *Feature Flag*, *Shadow Proxy*, or *Branch by Abstraction*.

### 2. Expand-Contract Triad Invariants
1. **Phase 1: Expand (Additive Non-Breaking)**: Introduce new interfaces, schemas, or shadow services alongside legacy code. Caller signatures and legacy test suites remain unmodified and GREEN.
2. **Phase 2: Migrate (Progressive Cutover)**: Reroute callers individually to the new abstraction via feature flags or adapters. Rollback to legacy path must execute instantly via flag toggle without code redeployment.
3. **Phase 3: Contract (Pruning & Cleanup)**: Remove legacy implementations, delete temporary flags, and purge obsolete branches and shims once full regression tests pass.

### 3. State
- `STAGED`: The 3-phase migration strategy and rollback coordinates are staged for human review.
- `UNRESOLVED`: Tightly coupled code prevents seam identification without a foundational redesign.

## Canonical Output Contract

```markdown
# Seam Migration Plan: <Refactor Target> · <STAGED | UNRESOLVED>

Basis: <Frozen contract, architectural direction, or structural audit>
Seam Coordinate: <Repo-relative file and symbol representing the interception point>
Isolation Mechanism: <Interface Adapter | Feature Flag | Shadow Proxy | Branch by Abstraction>

## Phase 1: Expand (Additive Non-Breaking)
- Operations: [CREATE] <New interfaces, adapters, or shadow implementations>
- Invariant: Zero modifications to existing caller signatures; legacy tests remain unmodified and GREEN.

## Phase 2: Migrate (Progressive Cutover)
- Migration Steps:
  1. `<Caller A>`: Rerouted via `<Flag / Seam>` -> Verified via `<Parity Check>`.
  2. `<Caller B>`: Rerouted via `<Flag / Seam>` -> Verified via `<Parity Check>`.
- Fallback Gate: <Observable condition triggering instant rollback to legacy seam>

## Phase 3: Contract (Pruning & Cleanup)
- Operations:
  - [DELETE] `<Legacy implementation files or obsolete branches>`
  - [UPDATE] `<Remove temporary flags, adapters, and redundant shims>`
- Final Verification: <Full regression test suite execution without legacy paths>

Summary: 3 atomic phases planned, rollback exposure confined to Phase 2 flag.
*(omit if clean)* Gap: <Coupling blocker preventing clean seam extraction.>
```

### Routing

- Migration strategy ready for multi-phase living plan packaging → (via /plan-dossier).
- Migration strategy staged, proceed to slice each phase into a DAG → (via /split-tasks).
- Single phase ready for immediate file-impact planning → (via /changeset).
- Cannot isolate a seam without a major architectural pivot → (via /architect-decision).

## Execution Protocol

1. Inspect target refactoring scope, locate interception seams, and formulate the 3-phase progression (Expand -> Migrate -> Contract).
2. Stage the Seam Migration Plan with explicit rollback gates. Report `STAGED` (or `UNRESOLVED` if coupling prevents seam isolation).
