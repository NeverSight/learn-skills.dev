---
name: continue
description: >-
  Resume software work after a context switch by reconstructing current repository reality from
  git, code, canonical artifacts, handoff notes, and remote CI/PR evidence when available. Use for
  “continue/resume/what is next?” requests. Treat handoffs as hints that may be stale, reconcile
  contradictions, identify the first eligible work item, then route to the appropriate workflow
  stage.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Continue

Reconstruct reality before resuming work.

## Workflow

1. Read the latest relevant handoff if one exists, but do not trust it blindly.
2. Inspect branch, HEAD, base, working tree, canonical project/spec/plan/ADR/roadmap state, and the actual implementation.
3. Inspect PR/CI/remote evidence when accessible and material to eligibility.
4. Reconcile differences between the previous checkpoint and current reality.
5. Determine the first eligible unfinished work item and the correct workflow stage: shape, architect, plan, implement, debug, accept/review, or finish.
6. If the user's instruction is simply to continue and no genuine human decision blocks progress, proceed through the appropriate owner instead of asking the user to restate known context.

## Outputs

Reconstructed state, contradictions or stale assumptions, current blockers, and next eligible work. A substantial resume may immediately hand execution to another core workflow.

## Stop

Stop reconstruction when the current state and next eligible work are evidenced. If proceeding is safe and requested, transition to that workflow rather than stopping merely to report status.
## Reference Guide

Load only the references needed for the current task:

- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [gate](references/_shared/orchestration/gate.md)
- [reconcile](references/_shared/orchestration/reconcile.md)
- [handoff](references/_shared/orchestration/handoff.md)
- [artifact model](references/_shared/artifacts/artifact-model.md)
- [diff discipline](references/_shared/engineering/diff-discipline.md)
- [evidence](references/_shared/verification/evidence.md)
