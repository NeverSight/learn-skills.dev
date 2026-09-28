---
name: finish
description: >-
  Close software work with risk-appropriate verification, relevant review, diff hygiene, artifact
  reconciliation, readiness evidence, and a factual handoff. Use when implementation is considered
  complete, a PR/milestone should be ready, or release readiness must be assessed. Keep finish as
  the single core workflow owner, compose only material domain specialists, and scale closure to
  the work rather than replaying every earlier workflow.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.1"
---


# Finish

Close the work with enough evidence to make the completion claim credible, but no more ceremony than the risk requires.

## Workflow

1. Start from project-local current state, accepted artifacts, existing acceptance evidence, and source-control/CI state when those capabilities actually exist. Treat non-Git workspaces as normal.
2. Reconstruct the work depth and material concern set; do not blindly reuse stale plan metadata.
3. Load only the material domain skill contracts needed to interpret final evidence or review touched risk domains. Keep `finish` as the sole core workflow owner: do not invoke `accept`, `review`, `implement`, or other core skills as sibling workflows merely to close the milestone.
4. Reuse existing acceptance/review evidence when it is current and sufficient. Rerun only the verification needed to support the final readiness claim or to resolve stale/uncertain evidence; do not mechanically replay the full acceptance phase.
5. Perform a bounded final review of the delivered scope, check diff/working-tree hygiene when source control exists, and preserve unrelated changes.
6. Reconcile durable artifacts according to ownership. Product/design/ADR/spec change only when their durable truth changed. Project context should orient and point. PLAN remains the implementation approach; at most add a concise status/pointer when useful. HANDOFF/READINESS owns the exact final execution state, verification evidence, blockers, and next eligible work. Do not duplicate the same evidence ledger across artifacts.
7. For production/high-assurance changes, include the relevant migration, security, recovery, rollback, or readiness evidence. Do not run these modes for ordinary small changes.
8. Record blocked or missing evidence explicitly. A milestone may be implementation-complete while a required readiness/acceptance gate remains BLOCKED; never turn that into a full-verification claim.
9. Produce a factual handoff/readiness record when future continuation or PR review benefits from it.

## Release mode

When explicitly used for release readiness, verify artifact/version/compatibility/rollback and production-intended configuration appropriate to the project. A feature flag can stop future code paths but cannot reverse already-committed data or external side effects.

## Stop

Stop when required criteria are evidenced or explicitly marked blocked/gap, the intended delivered scope is understood, durable artifacts are reconciled without duplication, and the next state is unambiguous.
## Reference Guide

Load only the references needed for the current task:

- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [bounded work](references/_shared/constitution/bounded-work.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [depth](references/_shared/orchestration/depth.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [reconcile](references/_shared/orchestration/reconcile.md)
- [handoff](references/_shared/orchestration/handoff.md)
- [artifact model](references/_shared/artifacts/artifact-model.md)
- [acceptance](references/_shared/artifacts/acceptance.md)
- [diff discipline](references/_shared/engineering/diff-discipline.md)
- [evidence](references/_shared/verification/evidence.md)
- [verdicts](references/_shared/verification/verdicts.md)
- [risk depth](references/_shared/verification/risk-depth.md)
- [regression scope](references/_shared/verification/regression-scope.md)
