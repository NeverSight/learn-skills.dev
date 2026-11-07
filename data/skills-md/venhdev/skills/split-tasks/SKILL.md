---
name: split-tasks
description: "Decompose complex features or settled designs into an acyclic directed graph of independently verifiable vertical slices with explicit parent provenance."
---

# split-tasks — Task DAG Decomposition & Provenance Slicing

## Operating Invariants

- **Zero-Persistence Boundary**: Never write task files to disk or issues to remote trackers; produce only an in-memory or reviewable Task DAG manifest.
- **Vertical Slice Mandate**: Partition work strictly into end-to-end vertical slices (1–4 files, 50–150 LOC) with observable acceptance criteria; forbid horizontal technical layering (DB-only or API-only slices).
- **Parent Provenance Rigor**: Every slice must explicitly trace to its origin (`Parent Trace`: ADR ID, Feature Slug, or Frozen Contract coordinate); forbid orphan slices.
- **Acyclic Dependency Enforcement**: Slices must form a directed acyclic graph (DAG); forbid circular dependencies.
- **Atomic Bypass**: Retain a single unified slice when the input scope already fits within one verification turn (≤ 3 files, single criterion).
- **Adaptive Invocation Output**: Render the full Markdown table for human review; output a compact JSON DAG when dispatched by an autonomous runner.

## Domain Rubric

### 1. Slicing Sizing & Blast Radius
A slice must be verifiable within one turn of `/forge`. If a slice spans more than 4 files or touches disparate domain contexts, split it further along independent caller or scenario boundaries.

### 2. Topological Phasing
Sequence slices topologically:
1. *Contract / Seam Anchor*: Type declarations, interfaces, characterization tests.
2. *Core Vertical Flow*: Minimal end-to-end happy path.
3. *Edge / Resiliency Slices*: Validations, error boundaries, concurrency safeguards.
4. *Pruning / Deprecation*: Removal of obsolete shims, flags, or legacy paths.

### 3. State & Dispatch Lifecycle
- `READY`: All predecessor dependencies are `DONE`; ready for immediate `/forge` execution.
- `BLOCKED`: Awaiting completion of prerequisite upstream slices.

## Canonical Output Contract

```markdown
# Task DAG: <Feature / Scope> · <STAGED | UNRESOLVED>

Basis: <Root intent, architecture anchor, or ADR link>

| Slice ID | Title & Scope | Dependencies | Parent Trace | Acceptance & Verification Criteria | Dispatch State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| S-01 | <Vertical deliverable> | None | <ADR / Spec Anchor> | <Automated test command or invariant> | READY |
| S-02 | <Dependent deliverable>| S-01 | <ADR / Spec Anchor> | <Automated test command or invariant> | BLOCKED |

Summary: <N> slices (Max depth <K>, <D> direct dependencies).
*(omit if clean)* Gap: <Unresolved dependency or ambiguous boundary requiring decision.>
```

*Autonomous JSON Contract (for Model Runner)*:
```json
{
  "basis": "<anchor>",
  "slices": [
    {"id": "S-01", "scope": "<title>", "deps": [], "parent": "<trace>", "verify": "<cmd>", "state": "READY"},
    {"id": "S-02", "scope": "<title>", "deps": ["S-01"], "parent": "<trace>", "verify": "<cmd>", "state": "BLOCKED"}
  ]
}
```

### Routing

- Immediate in-session execution -> Take first READY slice to (via /changeset) -> (via /forge).
- Deferred execution or team backlog tracking -> (via /track-tasks).
- Long-running automated pipeline execution -> Autonomous Runner (/goal).
- Ambiguous scope or conflicting dependencies -> (via /clarify).

## Execution Protocol

1. Ingest settled changeset, frozen contracts, or architectural directions.
2. If scope is atomic (≤ 3 files), yield a single READY slice without partitioning.
3. Otherwise, derive vertical slices, establish parent traces, and verify acyclic dependencies.
4. Output Markdown DAG (for human caller) or JSON DAG (for autonomous runner).
