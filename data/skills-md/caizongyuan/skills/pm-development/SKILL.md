---
name: pm-development
description: Coordinate approved multi-issue or long-running development, owning scope, agent capacity, risk decisions, and evidence for actual integration and delivery.
---

# PM Development

The PM receives a defined task and owns scope, scheduling, risk decisions, and delivery verification. Independent Developers implement. Follow the runtime configuration, host repository rules, and existing authorization; reuse approved requirements and experiences.

Matt owns clarification, specs, and tickets; Developers use its implementation/TDD methods, Reviewers use Standards + Spec, and `pr` / `retro` handle PRs and environment improvements. PM dispatches directly; `implement-spec` is an alternative scheduling entrypoint. Keep imported skills unchanged and host overrides in owned files. When a method is unavailable, use the host's equivalent and report the limitation.

Check independent implementer/reviewer capacity before dispatch; limited capacity permits preparation, not claims of independent implementation or review. At the start, use installed [development-timeline](../development-timeline/SKILL.md) for stage changes and waits, or the host's existing journal/report when unavailable.

## Dispatch and Schedule

- Reconcile parent/child acceptance, accepted experience, and latest corrections before dispatch. List key failure states and known verification risks; settle contradictions using existing decisions or a concrete user decision when needed. Desktop web is the default unless mobile is already included. Preserve commitments and record which criteria a later explicit scope correction supersedes.
- Read the tracker, actual blockers, agents, and Git. Claim ready, unowned implementation issues. Keep one owner, branch, and worktree per issue; give the Developer the baseline, approved artifacts, public verification entrypoints, deliverable, authorization, and evidence locations.
- Schedule source implementation, heavy execution, and review as separate capacities, based on actual contract/path overlap and available slots. Lightweight preparation may continue during serialized builds; path overlap alone does not serialize an entire issue.
- Isolate databases, migration identifiers, accounts, ports, build directories, and evidence as well as worktrees. Declare shared services, quotas, and consumers with an owner; assign an integration owner for coordinated registration or generation changes. Follow the host's resource ledger and cleanup policy.
- Record readiness, last progress, next stage, and a continuation plan before borrowing an implementer. Reuse non-author review roles by phase; frozen candidates and CI waits need not keep their authors in active turns. On recovery reconcile actual state, resume the original implementer, and confirm writes have stopped before transfer.
- Give maintenance, diagnosis, and review a phase goal and exit condition. Reserve heavy resources for execution and cleanup, release them promptly, and let independent ready issues proceed while diagnosis is reconsidered.

## Select Methods When Needed

An existing Developer or Reviewer can apply an installed thin skill in their task. Reuse valid evidence; a skill needs neither another Agent nor a new gate. Use host equivalents if unavailable.

- Shared API, schema, dependency, or resource-ownership changes: use [change-impact](../change-impact/SKILL.md) to identify real consumers and prove the facts the change relies on.
- Performance claims or comparisons: use [check-benchmark](../check-benchmark/SKILL.md) to check that measurement represents correct, comparable work.
- Unfamiliar or repeatedly rediscovered verification entrypoints: use [verification-guide](../verification-guide/SKILL.md) to validate and document the existing harness, then reuse the guide.
- Consequential unresolved designs, repeated failure without new evidence, or review conflicts: read [Advisor consultation](references/advisor.md) and ask a read-only second opinion. PM evaluates the evidence and decides.

## Stabilize and Integrate

For verification, review, or difficult diagnosis, read [delivery and rework control](references/delivery.md). It governs early high-risk checks, reviewer independence, valid evidence, and bounded diagnosis; reuse already read rules.

Complete bounded [reduce-complexity](../reduce-complexity/SKILL.md) or the host's equivalent before final validation and independent review. Refresh affected coverage after repairs/baseline movement from the semantic delta. Stable-candidate CI and review may overlap.

For GitHub CI, read [the observer contract](references/ci-observer.md) before using `scripts/ci-observer.mjs`; act on changes and failures. The observer reports facts; PM determines required checks from host policy and verifies the final head. When unavailable, use the host's observation process.

Before an authorized merge, verify the complete candidate, simplification, applicable independent review, and required CI on the final head. WIP commits and authorized Draft PRs preserve progress. Completion requires the authorized delivery goal and actual integration: read back the merge, then update the tracker; pending integration stays unfinished.

## Report and Improve

Keep the checkpoint to authorization/scope, roles/issues, revisions, resource owners, results, and next steps; link history/evidence. Reuse runner/observer facts through installed timeline projections. At delivery, task end, pause, or handoff, report completed/pending work, evidence, blockers, rework, and limitations. Reports add no merge gate; retain unknown intervals.

Verify approved real user journeys and the usable application address. At milestone completion, review and survey simplification from the entire milestone baseline to the integrated revision, including consumers. Optional cleanup remains a proposal. Feed the same factual record to Matt `retro` for environment improvements; publication and release follow existing authorization.
