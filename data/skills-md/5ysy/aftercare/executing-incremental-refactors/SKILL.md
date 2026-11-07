---
name: executing-incremental-refactors
description: execute an approved aftercare refactor plan in small safe slices while preserving behavior and re-validating frequently. use only after a clear refactor plan exists or a human has explicitly approved the refactor direction — never as an autonomous cleanup pass.
---

# Executing Incremental Refactors

Announce at the start: "I'm using executing-incremental-refactors to apply the approved plan one verifiable slice at a time."

## Core idea

Aftercare execution is conservative. A refactor is a sequence of small behavior-preserving moves, each independently verifiable, each stoppable. The job is not to reach the endpoint in one sweep; it is to leave the repo materially better without surprising anyone.

## Workflow

1. Re-state the approved goal in one sentence. If it takes more, the plan is not ready to execute.
2. Re-state the constraints: what must not change (external behavior, public API, performance envelope, dependency direction).
3. Pick the next slice from the plan. Apply exactly that slice — no adjacent tidying, no "while I'm here" edits.
4. Verify: run the tests hardened in the prior phase; run any manual checks the plan specifies.
5. Walk [`checklist.md`](./checklist.md) for the slice you just completed.
6. Consult [`decision-tree.md`](./decision-tree.md) to decide whether to continue to the next slice, pause for review, or revert.
7. Stop when the repo is materially better, not when every theoretical cleanup is complete.

## Heuristics

- Commit (or at least checkpoint) after every slice; a slice that cannot stand alone is too big.
- When confidence drops mid-slice, revert the slice and re-plan; do not push through.
- Prefer moves that are reversible over moves that are "almost right."

## Do not

- sneak in unrelated redesigns, renames, or formatting passes
- rewrite broad areas because the plan "suggested it"
- keep changing structure after confidence has dropped
- skip verification between slices because "this one is obvious"

## Supporting files

- [`checklist.md`](./checklist.md) — per-slice safety checks covering behavior preservation, test status, scope discipline, and commit hygiene.
- [`decision-tree.md`](./decision-tree.md) — continue / pause / revert decision logic based on slice outcomes.

## Output

Maintain a running log of completed slices, remaining slices, and any risks surfaced during execution. When stopping (whether complete or paused), state the current state of the repo against the original goal and what remains.
