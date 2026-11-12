---
name: revise-draft
description: Coordinate an existing manuscript through nine evidence-gated revision operations without requiring a full-book outline, structure, or ending.
disable-model-invocation: true
---

# Revise Draft

Coordinate revision of existing manuscript from the same shared project evidence as `revise-fiction`. This skill mirrors its guided sequence while allowing an unfinished manuscript and undecided future plot. Resolve the installed `setup-author-toolkit` skill's root as `<setup-skill-root>` and use the controlled workflow terminology in `<setup-skill-root>/assets/references/terminology.md` for shared terms and exact contract values.

## Start or resume

1. Locate `.author-toolkit/project.json`. If it is absent, display the host command for user-invoked `setup-author-toolkit` and stop. Use the same setup command forms as `revise-fiction`. Setup is identical for all five workflow entries. If the manifest has any schema version other than `3.1.0`, report that it is unsupported and stop without changing it.
2. Read each needed callee's installed `SKILL.md` and applicable references. Execute its procedure directly. A user-invoked entry starts only through its author-facing command, never as an internal callee.
3. Run the `author-project` procedures separately with `read`, `validate`, and `status --digest`. These use the shared contracts and validator installed with setup. If they report an incomplete toolkit installation, stop and report the missing installed files; do not deploy contracts into the project. Read `PROJECT_STATE.md` first, then read only the tracker sections, sessions, current plan, current scope, pending action, and relevant evidence needed for the requested work. Do not read the full tracker or backup index for routine navigation. For routine navigation, use `PROJECT_STATE.md` pointers, targeted artifact reads, or aggregate counts rather than emitting complete file listings of the registered session or backup directories. Switching from `revise-fiction` preserves the shared project state and changes no scope or status.
4. On the first run for a new scope, complete the read-only `intake` inventory and a proposed `draft-baseline`, then stop at the first item in the author decision loop, normally confirmation of the proposed scope. Show the proposed baseline as context without requesting its confirmation in the same turn. On later runs, select the author-requested operation or the earliest missing, partial, or stale evidence in the sequence below. Read only the relevant section in [`references/stage-gates.md`](references/stage-gates.md).
5. Record the operation through `author-project` with `set-pending`. Run one operation and stop at its gate with `awaiting_author` or `blocked`. When the author says to continue, advance to the next applicable operation whose evidence is not current. Do not require an outline, total chapter count, planned ending, or full-book structure audit at any gate.

The current-draft sequence is `intake`, `draft-baseline`, `diagnostics`, `characters`, `revision-plan`, `chapter-revision`, `prose`, `ai-cleanup`, and `current-scope-review`.

## Author interaction

At every author gate, follow the [Author decision loop](../revise-fiction/references/state-and-findings.md#author-decision-loop) before presenting questions or approval requests. This applies within an operation as well as at its final gate.

## Operation routing

For each diagnostic callee, supply the operation identifier, destination report path, named inputs and versions, `scope_id`, BCP 47 language, tracker path, and resolved `<setup-skill-root>`. Require `<setup-skill-root>/assets/references/workflow-reporting.md` and finding v2, and supply `../revise-fiction/references/state-and-findings.md` resolved from the callee's installed skill directory as the shared state reference. Record actual operation coverage and subchecks; unknown future story is not a finding by itself.

| Operation | Delegation |
|---|---|
| `intake` | `author-project` plus manuscript inventory |
| `draft-baseline` | `fiction-workshop`, current-text summary using the local baseline template |
| `diagnostics` | `fiction-workshop` Developmental Editor, scene and chapter scope only |
| `characters` | Character Consultant and Continuity Tracker; `character-archetypes` when requested or when profiles already exist |
| `revision-plan` | Consolidate accepted findings using the shared plan template |
| `chapter-revision` | `fiction-workshop`, scoped to the approved plan |
| `prose` | `prose-mechanics`, audits 1-18 in upstream order |
| `ai-cleanup` | Follow `<setup-skill-root>/assets/references/avoid-ai-writing-adapter.md` |
| `current-scope-review` | `author-review` with `review_mode=current-scope` |

`diagnostics` excludes full-book act-level landmark placement, percentage timing, ending completeness, and missing future beats. It may diagnose observable scene causality, chapter function, information release, local pacing, chapter transitions, and current climactic turns. Local split, merge, reorder, cut, or scene rewrite proposals are allowed after approval; describe their local purpose and uncertainty rather than claiming an optimal whole-book structure.

`characters` uses the same character and continuity capabilities as `revise-fiction`, evaluated against current text. Motivation, voice, choices, current arc trends, timeline, relationships, knowledge states, and world facts are in scope. Future arc resolution and full-cast readiness are not prerequisites. Reports list actual subchecks so their evidence is not mistaken for full-book character coverage.

## Direct entry and skips

The author may request diagnosis-only work, direct `prose` or `ai-cleanup`, or a limited review. These entries require current intake evidence, a confirmed scope, and language metadata; chapter revision still requires an approved plan and batch. Record skipped operations in the session and tracker rather than manufacturing evidence. When no accepted finding requires edits, `revision-plan` and `chapter-revision` may be skipped for the current scope. A direct entry or narrowed requested pass does not by itself establish current-draft revision convergence.

Before prose over text with approved but unexecuted changes, explain the rework risk. If the author continues, record a `prose-risk` approval for that exact scope. Unknown future structure and issues outside the target scope do not block prose.

## Approval and backup gate

For manuscript changes, first diagnose without editing. Read `<setup-skill-root>/assets/references/context-fit.md` and complete its check before presenting an edit proposal. Then show affected paths, exact intended changes, and checked local context. Record explicit author approval in the shared tracker, then run `author-project` with `record-backup` for every affected file and the approval ID. Apply only the approved batch after every backup succeeds. After the exact batch completes, verify its output hashes and run `author-project` with `record-execution`; an interrupted batch has no execution receipt and remains unverified. Restore requires separate explicit approval and a safety backup.

Baseline writes distinguish text-established facts, interpretations, and unknowns. Interpretations remain labeled until the author turns them into creative decisions. Only affected baseline differences are presented after an edit; unknowns never become automatic blockers.

## Strategy switching and evidence reuse

`write-fiction`, `revise-fiction`, `revise-increment`, and `revise-request` use this same manifest and state. At any stable operation gate, show the exact command for the author's selected strategy and wait; do not switch automatically or require the other strategy's sequence to finish. Preserve scope, evidence, approvals, staged drafts, and backups. Reconcile an interrupted write or commit before dependent work. After shared creation adds or affects chapters, offer `revise-increment` when the author wants to preserve reusable unchanged-chapter evidence and bring the expanded target scope to current-draft revision convergence. When the current scope is a full-manuscript scope that has reached current-draft revision convergence and the author requests another revision of existing content, offer `revise-request`.

Reuse full local coverage units only when source-report identity, operation, paths and hashes, subchecks, and dependencies match. Keep the unit's original scope for provenance and use the target scope for the composed index and synthesis. Reevaluate every applicable whole-book synthesis after changed text, membership, reading order, or dependencies, even when some local units remain reusable. Creation evidence does not satisfy `chapter-revision`. Review jobs and fresh-reader continuity retain their same-scope and actual-reading requirements.

## Current-draft revision convergence and reports

Use the shared [Current-draft revision convergence](../revise-fiction/references/state-and-findings.md#current-draft-revision-convergence) definition before claiming that state for a requested pass. Persist full local coverage units for independently covered paths so later `revise-increment` or `revise-request` work can reuse them. After current-scope review, process every finding; accepted edits return to the affected planning and revision operations and require new downstream coverage and review. A completed current-scope review with open findings does not establish current-draft revision convergence.

Before writing any report or changing finding or approval status, read [`../revise-fiction/references/state-and-findings.md`](../revise-fiction/references/state-and-findings.md). Reports use the shared `reports/` directories and report v2; there is no separate `revise-draft` state tree. Record `scope_id`, `operation_coverage`, and applicable `subchecks` in `engine.notes`.

Do not repeatedly recommend outlining, choosing an ending, or switching to `revise-fiction`. Mention that path only when the author asks for full-book structure or final review. Do not auto-write future scenes or run `story-structure` Map as a substitute for current-draft revision.

Finish each invocation with the current operation and scope, actual coverage, stale evidence, artifact paths, approvals or backups, unknowns, current-draft revision convergence status and blockers, and the exact next action. Use `author-handoff` for session transfer after shared state is current.
