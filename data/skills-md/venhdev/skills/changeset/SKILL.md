---
name: changeset
description: "Map affected files and dependency cascades for a settled solution into a reviewable changeset before implementation or task tracking."
disable-model-invocation: true
---

# changeset — File Impact & Cascade Planning

## Domain Rubric

### Input & Boundary

Receive a settled direction or solution with outcome, constraints, and available evidence. Ground it against the current checkout and governing contracts; keep planning read-only and preserve the supplied direction.

Trace direct and indirect callers, implementations, imports, schemas, and tests. Inspect only the target and load-bearing cascades; exclude cosmetic churn, speculative files, and unaffected backward-compatible callers. Prune superseded logic: stage explicit removal of dead helpers, obsolete branches, and tests invalidated by the solution. Stop if the input plan is stale or contradictory rather than silently redesigning it.

### File Actions

- `[CREATE]`: New file required by the solution.
- `[MOVE]`: Relocation or rename, including affected references.
- `[UPDATE]`: Existing logic, contract, test, or necessary cascade.
- `[DELETE]`: Obsolete file whose removal is required by the solution.

### State

- `STAGED`: The Changeset Tree identifies concrete operations and necessary cascades for the settled direction.
- `UNRESOLVED`: Missing, stale, or conflicting direction prevents a reliable changeset; cite the blocker and decision required.

## Canonical Output Contract

````markdown
# Changeset: <Scope> · STAGED

Basis: <Settled solution and supporting proof/reference.>
Acceptance: <Observable criteria and constraints to carry downstream.>

```text
|-- <subsystem>/
|   |-- <file>
|   |   `-- [UPDATE] <Load-bearing change and invariant>.
|   `-- <new-file>
|       `-- [CREATE] <Required component or regression check>.
`-- <deep/path/to/caller>
    `-- [UPDATE] <Necessary cascade>.

Summary: <N> files affected (<C> created, <U> updated, <M> moved, <D> deleted).
```
````

For `UNRESOLVED`, replace the tree with a concise blocker, evidence, and required redesign decision; omit invented file operations.

### Routing

- An outdated plan exposes unresolved requirements → (via /clarify).
- An outdated plan requires a new design direction → (via /architect-decision).
- The supported changeset is authorized for implementation → (via /forge).
- The caller wants task decomposition into verifiable slices → (via /split-tasks).
- The caller wants backlog persistence or issue tracking → (via /track-tasks).

## Execution Protocol

1. Inspect the supplied direction and current code/contracts. Stop on an outdated plan or foundational contradiction and report `UNRESOLVED` with the required redesign decision.
2. Build the tree with file actions, direct cascades, acceptance criteria, and evidence provenance. Collapse redundant directories while preserving file hierarchy.
3. Present `STAGED` and halt without filesystem mutations. An embedded changeset produced elsewhere uses the same handoff obligations without requiring this skill.
