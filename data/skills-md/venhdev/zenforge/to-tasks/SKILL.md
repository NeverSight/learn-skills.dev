---
name: to-tasks
description: "Decompose settled changesets into a verifiable DAG and persist tasks to the configured tracker via split-tasks and track-tasks."
disable-model-invocation: true
---

# to-tasks — Task Decomposition & Persistence Pipeline

Pipeline wrapper chaining task decomposition `(via /split-tasks)` and tracker persistence `(via /track-tasks)`.

## Operating Invariants

- **Delegation Exclusivity**: Delegate DAG derivation exclusively to `/split-tasks` and persistence operations exclusively to `/track-tasks`; never calculate DAG topology or mutate files directly.
- **Lean Authorization Gate**: Present the derived Task DAG and halt for authorization before persistence, unless task publication is already explicitly pre-authorized by the caller.
- **Zero-Implementation Boundary**: Task creation never authorizes code implementation; implementation remains a separate `/forge` invocation.

## Execution Protocol

1. **Decompose**: Invoke `/split-tasks` with the input changeset, architectural directions, or acceptance criteria to derive the in-memory Task DAG.
2. **Authorize**:
   - If task persistence is unauthorized: Output the Task DAG from `/split-tasks` as `STAGED` and halt the turn.
   - If persistence is authorized: Forward the Task DAG manifest directly to `/track-tasks`.
3. **Persist & Verify**: Execute `/track-tasks` to sync records to the configured tracker (`.agents/task-tracker.md`), verify IDs/paths, and report the persistence contract.

### Routing

- Immediate in-turn execution of the first ready slice without tracker persistence → (via /split-tasks) → (via /forge).
- Syncing or state updates on pre-existing tasks → (via /track-tasks).
- Unresolved scope or conflicting dependencies discovered during slicing → (via /clarify).
- Ready, authorized task ready for implementation → (via /forge).
