---
name: software-engineering-workflow-skill
description: "Create software-engineering planning artifacts with triaged depth: future-state runtime call stacks, future-state runtime call stack review, and implementation planning/progress for all sizes, plus proposed design docs for medium/large scope. Includes requirement clarification, call-stack review, and iterative refinement."
---

# Software Engineering Workflow Skill

## Overview

Produce a structured planning workflow for software changes: triage scope, build future-state runtime call stacks per use case, verify those call stacks with a dedicated review artifact, and drive implementation with plan + real-time progress tracking. For medium/large scope, include a full proposed design document organized by architecture direction plus separation of concerns.
This workflow is stage-gated. Do not batch-generate all artifacts by default.
In this skill, future-state runtime call stacks are future-state (`to-be`) execution models. They are not traces of current (`as-is`) implementation behavior.

## Workflow

### Ticket Folder Convention (Project-Local)

- For each task, create/use one ticket folder under `tickets/in-progress/`.
- Folder naming: use a clear, short kebab-case name (no date prefix required).
- Write all task planning artifacts into the `in-progress` ticket folder while work is active.
- Standard states:
  - active work path: `tickets/in-progress/<ticket-name>/`
  - completed archive path: `tickets/done/<ticket-name>/`
- Move rule (mandatory): move a ticket from `in-progress` to `done` only when the user explicitly confirms completion (for example: "done", "finished", or "verified") or explicitly asks to move it.
- Reopen rule (mandatory): if the user asks to continue/reopen a completed ticket, move it from `tickets/done/<ticket-name>/` back to `tickets/in-progress/<ticket-name>/` before making new updates.
- Never auto-move a ticket to `done` based only on internal assessment.
- If the user specifies a different location, follow the user-specified path.

### Ticket + Worktree Bootstrap (Mandatory First Action)

- Before investigation, bootstrap work context in this order:
  - create/use `tickets/in-progress/<ticket-name>/`,
  - if the project is a git repository, create/switch to a dedicated worktree/branch for the ticket before writing artifacts (`codex/<ticket-name>` branch naming),
  - create/update `requirements.md` with status `Draft` from user-provided requirement intent.
- Investigation must not start before the ticket bootstrap and `requirements.md` `Draft` are physically written.
- If a dedicated worktree already exists for the ticket, reuse it instead of creating a new one.
- If the environment is not a git repository, continue without worktree setup and still enforce ticket-folder + `Draft` requirement capture.

### Workflow State File (Mandatory Enforcement Artifact)

- Create and maintain `tickets/in-progress/<ticket-name>/workflow-state.md` as the canonical stage-control artifact.
- Initialize it during Stage 0 immediately after ticket bootstrap with:
  - `Current Stage = 0`,
  - `Code Edit Permission = Locked`,
  - stage gate rows in `Not Started`/`In Progress` state.
- Update model (mandatory):
  - rewrite `Current Snapshot` in place on every stage transition,
  - append one row to `Transition Log` for every transition/re-entry,
  - keep `Stage Gates` rows current with evidence links/paths.
- Source-code edit lock (hard rule):
  - no source code edits are allowed unless `workflow-state.md` explicitly shows `Code Edit Permission = Unlocked`,
  - default state is `Locked`; unlock source-code edits only when Stage 6 prerequisites are satisfied.
- Re-entry lock rule:
  - on any Stage 7/8 failure, set `Code Edit Permission = Locked` before re-entry actions,
  - record trigger/classification/return path in `workflow-state.md` before proceeding.
- Violation protocol:
  - if source code is edited while `Code Edit Permission = Locked`, record a violation entry in `workflow-state.md`,
  - pause further source edits, declare re-entry, and return to the required upstream stage path.

### Audible Notifications (Speak Tool, Required)

- Use the `Speak` tool for workflow-state transition updates so the user can follow where execution is and what is next.
- Playback rule (mandatory): for required audible notifications, call `Speak` with `play=true` explicitly.
- Do not set `play=false` by default for required transition notifications.
- Exception: set `play=false` only when the user explicitly requests silent mode.
- Transition-driven speak rule (mandatory):
  - speak only when `workflow-state.md` is updated for a stage transition, gate decision, re-entry decision, or code-edit lock/unlock change,
  - do not speak for low-level command execution, intermediate analysis notes, or partial drafts.
- Required audible events:
  - workflow kickoff (`task accepted`, `next stage`),
  - every stage transition (`From Stage -> To Stage`) after `workflow-state.md` transition log is appended,
  - every gate decision (`Pass`/`Fail`/`Blocked`) after gate evidence is written,
  - every re-entry declaration (classification + return path) after `workflow-state.md` re-entry section is updated,
  - every `Code Edit Permission` change (`Locked`/`Unlocked`) after snapshot update.
- Speak ordering rule:
  - update `workflow-state.md` first,
  - then emit audible notification reflecting the persisted state.
- Spoken message content (mandatory):
  - current stage,
  - what just completed/changed (transition or gate result),
  - next stage/action,
  - code-edit lock state when it changed.
- If multiple transitions happen close together, batch them into one short message after the final persisted update.
- Keep each spoken message short (1-2 sentences), status-first, and action-oriented.
- If the `Speak` tool fails or is unavailable, continue the workflow and provide the same update in text.
- Do not speak secrets, tokens, or full sensitive payloads.

### Execution Model (Strict Stage Gates)

- Work in explicit stages and complete each gate before producing downstream artifacts.
- Before every stage transition, update `workflow-state.md` first (snapshot + transition log + gate statuses), then proceed.
- Treat `workflow-state.md` as an execution lock controller, not optional documentation.
- Transition authority rule (mandatory): stage movement is controlled by the Stage Transition Contract + Transition Matrix. When a trigger condition is met, transition immediately to the mapped path; do not continue in the current stage by preference.
- Requirements can start as rough `Draft` from user input/bug report artifacts before deep analysis.
- Do not start investigation until ticket/worktree bootstrap is complete and `requirements.md` status `Draft` is physically written.
- Do not mark understanding pass complete until `investigation-notes.md` is physically written and current for the ticket.
- Do not draft design artifacts (`proposed-design.md` or small-scope design basis in `implementation-plan.md`) until deep understanding pass is complete and `requirements.md` reaches `Design-ready`.
- Do not finalize `implementation-plan.md` or generate `implementation-progress.md` until the future-state runtime call stack review gate is fully satisfied for the current scope.
- Do not start implementation execution until `implementation-plan.md` is finalized and `implementation-progress.md` is initialized.
- Do not start source-code edits until all of the following are true in `workflow-state.md`:
  - `Current Stage = 6`,
  - `Code Edit Permission = Unlocked`,
  - Stage 5 gate is `Go Confirmed`,
  - required upstream artifacts are marked `Pass` with evidence.
- Do not start API/E2E test implementation and execution until implementation execution is complete with required unit/integration verification and Stage 6 modernization/decoupling checks are satisfied.
- Do not start code review until API/E2E test gate is `Pass`.
- Do not start post-testing `docs/` synchronization until code review is complete (for infeasible acceptance criteria in Stage 7, explicit user waiver + constraints + compensating evidence + residual risk must be recorded).
- Do not close the task until post-testing `docs/` synchronization is completed (or explicit no-impact decision is recorded with rationale).
- Keep the ticket folder under `tickets/in-progress/` until explicit user completion confirmation is received.
- Treat technical completion and ticket archival as separate gates: technical completion ends at implementation + API/E2E test gate + code review + docs sync; archival to `tickets/done/` requires explicit user confirmation.
- `Small` scope exception: drafting `implementation-plan.md` (solution sketch only) before review is allowed as design input, but this draft does not unlock implementation kickoff.
- Future-state runtime call stack review must run as iterative deep-review rounds (not one-pass review).
- `Go Confirmed` cannot be declared immediately after required upstream artifact updates from a blocking round.
- Stability rule (mandatory): unlock `Go Confirmed` only after two consecutive deep-review rounds report no blockers, no required persisted artifact updates, and no newly discovered use cases.
- First clean round is provisional (`Candidate Go`), second consecutive clean round is confirmation (`Go Confirmed`).
- Missing-use-case discovery rule (mandatory): every Stage 5 round must run a dedicated missing-use-case discovery sweep (requirement coverage, boundary crossings, fallback/error branches, and design-risk scenarios).
- A Stage 5 round is not clean if it discovers new use cases, requires persisted artifact updates, or finds blockers.
- Any review finding with a required design/call-stack update is blocking; regenerate affected artifacts and re-review before proceeding.
- If design/review reveals missing understanding or requirement ambiguity, return to understanding + requirements stages, update `requirements.md`, then continue design/review.
- Stage 5 classified re-entry mapping (mandatory):
  - `Design Impact` (clear boundary/layer/naming/architecture issue with high confidence): return to `Stage 3 -> Stage 4 -> Stage 5`.
  - `Requirement Gap` (missing/ambiguous requirement or acceptance criterion): return to `Stage 2 -> Stage 3 -> Stage 4 -> Stage 5`.
  - `Unclear` (cross-cutting scope or low root-cause confidence): return to `Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5`.
- For any Stage 5 blocking round, record classification + return path in `future-state-runtime-call-stack-review.md` and `workflow-state.md` before starting the next round.
- Stage 6 non-local re-entry rule (mandatory): if a Stage 6 issue is classified as `Design Impact`, `Requirement Gap`, or `Unclear`, record classification + return path in `workflow-state.md`, set `Code Edit Permission = Locked`, and transition to the mapped upstream stage path before further source edits.
- Re-entry declaration rule (mandatory): when a post-implementation gate (`Stage 7` API/E2E testing or `Stage 8` code review) finds issues, explicitly record:
  - trigger stage (`7`/`8`),
  - classification (`Local Fix`/`Design Impact`/`Requirement Gap`/`Unclear`),
  - required return stage path before any code edit.
- Re-entry declaration must be recorded in `workflow-state.md` before any artifact/code update work begins.
- No-direct-patch rule (mandatory): for post-implementation gate findings, do not edit source code first. Update required upstream artifacts first based on classification path.
- Re-entry mapping (mandatory):
  - `Local Fix`: update implementation artifacts (`implementation-plan.md` / `implementation-progress.md` / `api-e2e-testing.md` / `code-review.md` as applicable), then implement fix, then rerun `Stage 6 -> Stage 7`; once Stage 7 passes, continue to `Stage 8`.
  - `Design Impact`: return to `Stage 1 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7`; once Stage 7 passes, continue to `Stage 8`.
  - `Requirement Gap`: return to `Stage 2 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7`; once Stage 7 passes, continue to `Stage 8`.
  - `Unclear` (or cross-cutting root cause): return to `Stage 0 -> Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7`; once Stage 7 passes, continue to `Stage 8`.
- Stage 0 in a re-entry path means re-open bootstrap controls in the same ticket/worktree (`workflow-state.md`, lock state, artifact baselines); do not create a new ticket folder.
- If the user asks for all artifacts in one turn, still enforce stage gates within that turn (iterate review rounds first; only then produce implementation artifacts).
- Stage-first persistence rule: if a Stage 5 round finds issues, first record classification + return path and transition to the required upstream stage in `workflow-state.md`, then persist required artifact updates in that stage.
- No mental-only review refinements: do not carry unresolved updates in memory across rounds.
- For each review round, record explicit persisted artifact updates in `future-state-runtime-call-stack-review.md`:
  - updated files,
  - new artifact versions,
  - changed sections,
  - which findings were resolved.
- A review round cannot be considered complete until its required file updates are physically written.
- If announcing review-round status, do it only after the round record + required staged artifact updates are physically written and the related Stage 5 gate status is persisted in `workflow-state.md`.

### Canonical Stage Sequence (Quick Map)

| Stage | Name | Core Deliverable/Gate | Code Edit Permission |
| --- | --- | --- | --- |
| 0 | Bootstrap + Draft Requirement | Ticket/worktree bootstrap complete + `requirements.md` = `Draft` | Locked |
| 1 | Investigation + Triage | `investigation-notes.md` current + scope triage complete | Locked |
| 2 | Requirements Refinement | `requirements.md` reaches `Design-ready`/`Refined` | Locked |
| 3 | Design Basis | `implementation-plan.md` sketch (`Small`) or `proposed-design.md` (`Medium/Large`) | Locked |
| 4 | Runtime Modeling | `future-state-runtime-call-stack.md` current | Locked |
| 5 | Runtime Review Gate | `Go Confirmed` (two consecutive clean rounds with no blockers/persisted updates/new use cases) | Locked |
| 6 | Source Implementation + Unit/Integration | Source code + required unit/integration checks complete + no backward-compat/legacy retention + decoupling preserved + touched files correctly placed | Unlocked |
| 7 | API/E2E Test Implementation + Gate | API/E2E scenarios implemented and acceptance criteria closure complete | Unlocked |
| 8 | Code Review Gate | Code review decision recorded (`Pass`/`Fail`) with `<=500` effective-line hard-limit + required `>220` delta-gate assessments + shared-principles/layering + decoupling + module/file placement + no-backward-compat/no-legacy checks | Locked |
| 9 | Docs Sync | `docs/` updates complete or no-impact rationale recorded | Locked |
| 10 | Final Handoff | Delivery summary + ticket state decision recorded | Locked |

### Stage Transition Contract (Enforcement)

| Stage | Exit Condition (Must Be True To Transition) | On Fail/Blocked | Next Stage On Pass |
| --- | --- | --- | --- |
| 0 Bootstrap + Draft Requirement | Ticket/worktree bootstrap complete and `requirements.md` status is `Draft` | Stay in `0` until bootstrap is complete | `1` |
| 1 Investigation + Triage | `investigation-notes.md` is current and scope triage (`Small`/`Medium`/`Large`) is recorded | Stay in `1` until investigation evidence is complete | `2` |
| 2 Requirements | `requirements.md` is `Design-ready` (or `Refined`) with requirement/acceptance-criteria coverage maps | Stay in `2` until requirements are design-ready | `3` |
| 3 Design Basis | Design basis artifact is current (`implementation-plan.md` sketch for `Small`, `proposed-design.md` for `Medium/Large`) | Stay in `3` and revise design basis | `4` |
| 4 Runtime Modeling | `future-state-runtime-call-stack.md` is current for in-scope use cases | Stay in `4` and regenerate runtime model | `5` |
| 5 Review Gate | Runtime review reaches `Go Confirmed` (two consecutive clean rounds with no blockers, no required persisted artifact updates, and no newly discovered use cases) | Classified re-entry before next review round (`Design Impact`: `3 -> 4 -> 5`, `Requirement Gap`: `2 -> 3 -> 4 -> 5`, `Unclear`: `1 -> 2 -> 3 -> 4 -> 5`) | `6` |
| 6 Source + Unit/Integration | Source implementation complete, required unit/integration checks pass, no backward-compatibility/legacy-retention paths remain in scope, decoupling boundaries stay intact (no new unjustified cycles/tight coupling), and touched files have correct module/file placement | Local issues: stay in `6`; classified re-entry for non-local issues (`Design Impact`: `1 -> 3 -> 4 -> 5 -> 6`, `Requirement Gap`: `2 -> 3 -> 4 -> 5 -> 6`, `Unclear`: `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6`) | `7` |
| 7 API/E2E Gate | API/E2E scenarios implemented and all executable mapped acceptance criteria are `Passed` (or explicitly `Waived` by user for infeasible cases) | `Blocked` on infeasible/no waiver; otherwise re-enter by classification (`Local Fix`: `6 -> 7`, `Design Impact`: `1 -> 3 -> 4 -> 5 -> 6 -> 7`, `Requirement Gap`: `2 -> 3 -> 4 -> 5 -> 6 -> 7`, `Unclear`: `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7`) | `8` |
| 8 Code Review Gate | Code review decision is `Pass` with all mandatory review checks satisfied (including `<=500` effective-line hard-limit + required `>220` delta-gate assessments + shared-principles/layering + decoupling + module/file placement + no-backward-compat/no-legacy) | Re-enter by classification (`Local Fix`: `6 -> 7 -> 8`, `Design Impact`: `1 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8`, `Requirement Gap`: `2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8`, `Unclear`: `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8`) | `9` |
| 9 Docs Sync | Docs updates are completed, or explicit no-impact rationale is recorded | Stay in `9` until docs gate is satisfied | `10` |
| 10 Final Handoff | Handoff summary complete; ticket move to `done` only on explicit user confirmation | Stay in `10`/`in-progress` until explicit user completion instruction | End |

### Transition Matrix (Pass/Fail/Blocked)

| Trigger | Required Transition Path | Notes |
| --- | --- | --- |
| Normal forward pass | `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10` | Use only when each stage gate is `Pass`. |
| Stage 5 blocker classified `Design Impact` | `3 -> 4 -> 5` | Use when issue is clearly in architecture/layering/boundary/naming decisions. |
| Stage 5 blocker classified `Requirement Gap` | `2 -> 3 -> 4 -> 5` | Use when missing/ambiguous requirement or acceptance criteria is discovered. |
| Stage 5 blocker classified `Unclear` | `1 -> 2 -> 3 -> 4 -> 5` | Use when root cause is uncertain or cross-cutting and investigation must be refreshed first. |
| Stage 6 failure classified `Local Fix` | stay in `Stage 6` | Fix implementation/tests within Stage 6; do not advance to Stage 7. |
| Stage 6 failure classified `Design Impact` | `1 -> 3 -> 4 -> 5 -> 6` | Re-open investigation checkpoint, then re-enter design/runtime chain before continuing implementation. |
| Stage 6 failure classified `Requirement Gap` | `2 -> 3 -> 4 -> 5 -> 6` | Update requirements first, then rerun downstream chain before continuing implementation. |
| Stage 6 failure (`Unclear`/cross-cutting root cause) | `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6` | Re-open Stage 0 controls in the same ticket context, then rerun full chain before continuing implementation. |
| Stage 7 failure classified `Local Fix` | `6 -> 7` | Update artifacts first, then code fix, then rerun Stage 7 scenarios. |
| Stage 7 failure classified `Design Impact` | `1 -> 3 -> 4 -> 5 -> 6 -> 7` | Re-open investigation, then re-enter design/runtime chain before retrying Stage 7. |
| Stage 7 failure classified `Requirement Gap` | `2 -> 3 -> 4 -> 5 -> 6 -> 7` | Update requirements first, then rerun downstream chain. |
| Stage 7 failure (`Unclear`/cross-cutting root cause) | `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7` | Re-open Stage 0 controls in the same ticket context, then rerun full chain. |
| Stage 7 infeasible scenario without user waiver | stay in `Stage 7 (Blocked)` | Record constraints + compensating evidence; wait for explicit user waiver or environment fix. |
| Stage 8 fail classified `Local Fix` | `6 -> 7 -> 8` | Apply fix and rerun test gate before re-review. |
| Stage 8 fail classified `Design Impact` | `1 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8` | Re-open investigation, then return to design chain before re-review. |
| Stage 8 fail classified `Requirement Gap` | `2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8` | Return to requirements then rerun full downstream chain. |
| Stage 8 failure (`Unclear`/cross-cutting root cause) | `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8` | Re-open Stage 0 controls in the same ticket context, then rerun full chain before re-review. |

### 0) Bootstrap Ticket + Capture Draft Requirement

- Run mandatory first-action sequence:
  - create/use `tickets/in-progress/<ticket-name>/`,
  - if git repo, create/switch ticket worktree/branch,
  - create/update `tickets/in-progress/<ticket-name>/workflow-state.md` from `assets/workflow-state-template.md` and set `Current Stage = 0`, `Code Edit Permission = Locked`,
  - capture initial requirement snapshot (`requirements.md` status `Draft`) from user input/bug report evidence first (text, images, logs, repro notes, constraints).
- Do not run deep investigation before Stage 0 bootstrap and `requirements.md` `Draft` are physically written.
- Before transitioning to Stage 1, update `workflow-state.md` snapshot + transition log + stage gate evidence.

### 1) Investigation + Understanding Pass + Triage

- Create/update `tickets/in-progress/<ticket-name>/investigation-notes.md` continuously during investigation. Do not keep investigation results only in memory.
- Minimum codebase understanding pass before design:
  - identify entrypoints and execution boundaries for in-scope flows,
  - identify touched modules/files and owning concerns,
  - identify expected canonical file locations/folder owners for touched concerns (for example: platform-specific vs shared),
  - identify current naming conventions (file/module/API style),
  - identify unknowns that could invalidate design assumptions.
- In `investigation-notes.md`, record at minimum:
  - sources consulted (`local file paths`, `web links`, `open-source references`, `papers` when used),
  - key findings and constraints,
  - module/file placement observations (which files are already under the right owning folder, which are misplaced, and what the canonical location should be),
  - open unknowns/questions,
  - implications for requirements/design.
- Re-entry rule: when later implementation/testing uncovers large or unclear issues, reopen this understanding stage and append new evidence, unknowns, and implications before changing requirements/design artifacts.
- Do not draft design artifacts or runtime call stacks until this understanding pass is complete and `requirements.md` reaches `Design-ready`.
- Classify as `Small`, `Medium`, or `Large` using practical signals:
  - Estimated files touched (roughly <= 3 is usually `Small` if not cross-cutting).
  - New/changed public APIs, schema/storage changes, or cross-cutting behavior.
  - Multi-layer impact (API + service + persistence + runtime flow) or architectural impact.
- Choose workflow depth:
  - `Small`: create a draft implementation plan (with a short solution sketch), build per-use-case future-state runtime call stacks from that plan, review them, then refine until stability gate `Go Confirmed` and track progress in real time.
  - `Medium`: create proposed design doc first, build future-state runtime call stacks from the proposed design doc, run iterative deep-review rounds until stability gate `Go Confirmed`, and only then create implementation plan and track progress in real time.
  - `Large`: create proposed design doc first, build future-state runtime call stacks from the proposed design doc, run iterative deep-review rounds until stability gate `Go Confirmed`, and only then create implementation plan and track progress in real time.
- Re-evaluate during implementation; if scope expands or smells appear, escalate from `Small` to full workflow.
- Before transitioning to Stage 2, update `workflow-state.md` snapshot + transition log + stage gate evidence.
- After triage depth is finalized (`Small`/`Medium`/`Large`) and `investigation-notes.md` is current, announce only with the persisted `workflow-state.md` transition/gate update.

### 2) Refine Requirements Document To Design-Ready (Mandatory)

- Create/update `tickets/in-progress/<ticket-name>/requirements.md` for all sizes (`Small`, `Medium`, `Large`).
- Requirement writing is mandatory even for small tasks (small can be concise).
- Use one canonical file path only: update `requirements.md` in place. Do not create versioned duplicates such as `requirements-v2.md`.
- Requirements maturity flow:
  - `Draft`: rough capture from report/input evidence,
  - `Design-ready`: refined after deep understanding pass,
  - `Refined`: further updates when design/review/implementation feedback reveals gaps.
- Minimum required sections in `requirements.md`:
  - status (`Draft`/`Design-ready`/`Refined`),
  - goal/problem statement,
  - in-scope use cases,
  - acceptance criteria,
  - constraints/dependencies,
  - assumptions,
  - open questions/risks.
- Requirements quality rule (mandatory): requirements must be verifiable behavior specifications, not only descriptive narratives.
- For each requirement, include a stable `requirement_id` and explicit expected outcome.
- For each acceptance criterion, include a stable `acceptance_criteria_id` (for example: `AC-001`) and an explicit measurable expected outcome.
- Acceptance criteria must be testable and cover primary behavior plus relevant edge/error behavior.
- Include a requirement coverage map to call-stack use cases (all requirements must map to at least one use case).
- Include an acceptance-criteria coverage map to Stage 7 scenarios (all acceptance criteria must map to at least one API/E2E scenario).
- Confirm the triage result (`Small` vs `Medium` vs `Large`) and rationale in the requirements doc.
- Refine requirements from the latest `investigation-notes.md`; do not derive requirements from memory-only investigation.
- Design-ready requirement gate must make expected behavior clear enough to draft design and runtime call stacks.
- If understanding is not sufficient to reach `Design-ready`, continue understanding pass and refine requirements first.
- After `requirements.md` reaches `Design-ready` and is confirmed as design input, announce only with the persisted `workflow-state.md` transition/gate update.

### Core Modernization Policy (Mandatory)

- Mandatory stance: no backward compatibility and no legacy code retention.
- Do not preserve legacy behavior, legacy APIs, compatibility wrappers, dual-write paths, or fallback branches kept only for old flows.
- Prefer clean replacement and explicit deletion of obsolete code, files, tests, flags, and adapters in the same ticket.
- Do not add compatibility exceptions in this workflow.

### Shared Architecture Principles (Design + Review, Mandatory)

- Design and review must use the same principles and vocabulary. Review is a check of design quality, not a different rule system.
- Separation of concerns (SoC) is the cause: responsibilities are split so each module/file/component owns one clear concern.
- Layering is usually an emergent result of strong SoC plus clear dependency direction; layering is not a fixed tier taxonomy by default.
- Decoupling is the dependency-quality rule: boundaries are replaceable, dependencies stay one-way, and unjustified cycles are rejected.
- Module/file placement is the physical-code-organization rule: each file lives in the folder/boundary/platform that owns its concern; if ownership changes, rename/move/split the file instead of leaving it in an arbitrary location.
- Layering/extraction trigger rule (mandatory): if coordination policy is repeated across callers (provider selection, fallback, retry, aggregation, routing, fan-out), extract that policy into an orchestration/registry/manager boundary.
- Responsibility-overload trigger rule (mandatory): if one file/module starts owning multiple concerns, split concerns and lift coordination into a higher-order boundary.
- Anti-overlayering rule (mandatory): do not add a layer that only pass-throughs and owns no coordination policy or boundary concern.
- Shared-folder rule (mandatory): place code in a shared/common folder only when it is genuinely cross-cutting and concern-agnostic; do not hide platform-specific code in shared or unrelated directories.
- `Keep` is valid when current layers/boundaries are already coherent for in-scope behavior and expected evolution.

### 3) Draft The Proposed Design Document

- Required for `Medium/Large`. Optional for `Small`.
- Prerequisite: `requirements.md` is `Design-ready` (or `Refined`) and current for this ticket.
- For `Small`, do not require a full proposed design doc; use the draft implementation plan solution sketch as the lightweight design basis for runtime call stacks.
- Architecture-first rule: define the target architecture shape before mapping work onto existing files.
- Do not anchor design to current file layout when the layout is structurally wrong for the target behavior.
- Module/file placement rule (mandatory): target file paths must match owning concern/boundary/platform; if a file is codex-specific, cloud-specific, UI-specific, infra-specific, or otherwise scope-bound, place it in that canonical area instead of near whichever caller currently imports it.
- Layering fitness check (mandatory): assess whether current layering and cross-layer interactions are coherent for the target behavior; treat layering as emergent architecture structure, not fixed tier labels.
- Explicitly evaluate whether new layers, modules, boundary interfaces, or orchestration shells should be introduced.
- Explicitly evaluate whether existing layers/modules should be split, merged, moved, or removed.
- Apply layering/extraction trigger checks explicitly: when provider choice/fallback/retry/aggregation/routing logic repeats across callers, extract orchestration/registry/manager responsibilities into a higher-order boundary.
- Reject overlayering: if a proposed layer is only a pass-through with no owned policy/boundary, keep structure flatter.
- Record the architecture direction decision and rationale (`complexity`, `testability`, `operability`, `evolution cost`).
- For straightforward local changes, one concise decision is enough; alternatives are optional.
- For non-trivial or uncertain architecture changes, include a small alternatives comparison before deciding.
- Choose the proper structural change for the problem (`Keep`, `Add`, `Split`, `Merge`, `Move`, `Remove`) without bias toward minimal edits.
- `Keep` is a valid outcome when layering and boundary interactions are already coherent.
- If a file's concern and folder disagree, `Keep` is usually invalid; prefer explicit `Move`, `Split`, or justified `Promote Shared`.
- Functional/local correctness is not sufficient: if a bug fix "works" but degrades layering or responsibility boundaries, redesign the structure instead of accepting the patch.
- Reject patch-on-patch hacks that bypass clear boundaries just to make a local change compile.
- Follow separation of concerns after the target architecture direction is chosen: each file/module owns a clear responsibility.
- Explicit decoupling rule (mandatory): define and preserve clear module/service/component boundaries so dependencies are one-directional and replaceable.
- For `Small`, the solution sketch in `implementation-plan.md` must still include a concise architecture sketch (target layers/boundaries and any new modules/files).
- Apply separation-of-concerns at the correct technical boundary for the stack:
  - frontend/UI scope: evaluate responsibility at view/component level (each component should own a clear concern),
  - non-UI scope (backend/service/worker/domain): evaluate responsibility at file/module/service level,
  - integration/infrastructure scope: each adapter/module should own one integration concern with clear contracts.
- Make the proposed design doc delta-aware, not only target-state:
  - include current-state summary (as-is),
  - include target-state summary (to-be),
  - include explicit change inventory rows for `Add`, `Modify`, `Rename/Move`, `Remove`.
- List files/modules and their public APIs.
- For each file/module, state target layer/boundary placement, responsibility, key APIs, inputs/outputs, dependencies, and change type.
- For each file/module, state whether its target path matches the owning concern and record the move/split rationale when placement changes are required.
- Include a naming decisions section:
  - proposed file/module/API names,
  - rationale for each naming choice,
  - mapping from old names to new names when renaming.
- Use natural, unsurprising, implementation-friendly names; naming choices should be understandable without domain-specific insider context.
- Add a naming-drift check section in the design doc:
  - verify each file/module name still matches its current responsibility after scope expansion,
  - identify drifted names (name no longer represents real behavior),
  - choose corrective action per drifted item (`Rename`, `Split`, `Move`, or `N/A` with rationale),
  - map each corrective action to change inventory rows and implementation tasks.
- Document dependency flow and cross-reference risk explicitly (including how cycles are avoided or temporarily tolerated).
- Document allowed dependency directions between layers/boundaries and note any temporary violations with removal plan.
- For `Rename/Move` and `Remove`, include decommission/cleanup intent (import cleanup and dead-code removal).
- Capture data models and error-handling expectations if relevant.
- Add a use-case coverage matrix in the design doc with at least:
  - `use_case_id`,
  - primary path covered (`Yes`/`No`),
  - fallback path covered (`Yes`/`No`/`N/A`),
  - error path covered (`Yes`/`No`/`N/A`),
  - mapped sections in runtime call stack doc.
- Version the design during review loops (`v1`, `v2`, ...) and record what changed between rounds.
- Use the template in `assets/proposed-design-template.md` as a starting point.
- No-backward-compat design gate (mandatory): proposed design must not introduce compatibility wrappers, dual-read/dual-write flows, legacy adapters, or fallback branches kept only for old behavior.
- If backward-compatibility or legacy-retention mechanisms are required to make the design work, classify as `Fail` and redesign the architecture direction before continuing.
- Do not speak solely because `proposed-design.md` changed; announce only when the related `workflow-state.md` transition/gate update is persisted.

### 4) Build Future-State Runtime Call Stacks Per Use Case

- Required for all sizes (`Small`, `Medium`, `Large`).
- For `Small`, keep it concise but still cover each in-scope use case with primary path plus key fallback/error branch when relevant.
- Basis by scope:
  - `Small`: use the draft implementation plan solution sketch as the design basis.
  - `Medium/Large`: use the proposed design document as the design basis.
- For each use case, write a future-state runtime call stack from entry point to completion in a debug-trace format.
- Use stable `use_case_id` values and ensure IDs match the design coverage matrix and review artifact.
- Use two allowed use-case source types:
  - `Requirement`: derived from explicit requirement behavior.
  - `Design-Risk`: derived from architecture or technical risk that must be validated.
- Coverage rule (mandatory): every in-scope requirement must be covered by at least one `Requirement` use case.
- For each `Design-Risk` use case, record the technical objective/risk justification and expected observable outcome.
- Treat this artifact as `to-be` architecture behavior derived from the proposed design (or small-scope solution sketch), not as-is code tracing.
- If current code differs from target design, model the target design behavior and record migration/transition notes separately.
- Include file and function names at every frame using `path/to/file.ts:functionName(...)`.
- Show architectural boundaries explicitly (e.g., controller -> service -> repository -> external API).
- Include primary path and fallback/error paths, not only happy path.
- Include explicit use-case coverage status per use case (primary/fallback/error) and mark intentional `N/A` branches.
- Mark async/event boundaries (`await`, queue enqueue/dequeue, worker loop handoff).
- Mark state mutations and persistence points (`in-memory state`, `cache write`, `DB/file write`).
- Capture decision gates and conditions that choose one branch over another.
- Note key data transformations (input schema -> domain model -> output payload).
- Version call stacks to match design revisions from review loops (`v1`, `v2`, ...).
- Use the template in `assets/future-state-runtime-call-stack-template.md`.
- Do not speak solely because `future-state-runtime-call-stack.md` changed; announce only when the related `workflow-state.md` transition/gate update is persisted.

### 5) Review Future-State Runtime Call Stacks (Future-State + Architecture + Naming + Cleanliness Gate)

- Create `future-state-runtime-call-stack-review.md` as a mandatory review artifact.
- Review focus is future-state correctness and implementability against the target design basis (`proposed-design.md` for `Medium/Large`, small-scope solution sketch in `implementation-plan.md` for `Small`), not parity with current code structure.
- Review must challenge architecture choice itself (layering/boundaries/allocation), not only file-level separation of concerns.
- Review must explicitly evaluate decoupling quality, not only local correctness.
- Review must reuse the same shared architecture principles from Stage 3 (SoC cause, layering emergent result, decoupling dependency quality); do not apply a different principle set in review.
- Review must explicitly verify module/file placement against the Stage 3 design basis; wrong folder placement is a structural defect, not a cosmetic nit.
- Run review in explicit rounds and record each round in the same review artifact.
- In every round, run a dedicated missing-use-case discovery sweep before verdicting the round.
- Review each use case against these criteria:
  - architecture fit check (`Pass`/`Fail`): chosen architecture shape is appropriate for this use case and expected growth,
  - shared-principles alignment check (`Pass`/`Fail`): SoC is treated as cause, layering as emergent result, and decoupling directionality is preserved consistently with Stage 3 design basis,
  - layering fitness check (`Pass`/`Fail`): layering and interactions are logical and maintainable, with layering treated as emergent from SoC/coordination needs (no fixed-tier requirement, no required layer-count change when current layering is already coherent),
  - boundary placement check (`Pass`/`Fail`): responsibilities are assigned to the right layer/module boundary,
  - decoupling check (`Pass`/`Fail`): dependency directions stay one-way, avoid tight cross-module coupling, and avoid cyclic cross-references,
  - module/file placement alignment check (`Pass`/`Fail`): file/module path matches owning concern/boundary/platform, and any shared placement is explicitly justified,
  - existing-structure bias check (`Pass`/`Fail`): design is not forced to mirror current files when that harms target architecture,
  - anti-hack check (`Pass`/`Fail`): no patch-on-patch tricks that hide architecture issues behind local fixes,
  - local-fix degradation check (`Pass`/`Fail`): a functionally working fix does not degrade architecture or separation of concerns,
  - terminology and concept vocabulary is natural and intuitive (`Pass`/`Fail`),
  - file/API naming is clear and unsurprising for implementation mapping (`Pass`/`Fail`),
  - name-to-responsibility alignment under scope drift (`Pass`/`Fail`),
  - future-state alignment with target design basis (`Pass`/`Fail`),
  - use-case coverage completeness (primary/fallback/error coverage) (`Pass`/`Fail`),
  - use-case source traceability (`Pass`/`Fail`) (`Requirement` or `Design-Risk`, with source reference),
  - requirement coverage closure (`Pass`/`Fail`) (all requirements mapped to at least one use case),
  - design-risk use-case justification quality (`Pass`/`Fail`) (clear objective/risk and expected outcome),
  - business flow completeness (`Pass`/`Fail`),
  - gap findings,
  - layer-appropriate structure and separation-of-concerns check (`Pass`/`Fail`) (frontend/UI: view/component boundary; non-UI: file/module/service boundary),
  - dependency flow smells,
  - redundancy/duplication check (`Pass`/`Fail`),
  - simplification opportunity check (`Pass`/`Fail`),
  - remove/decommission and obsolete/deprecated/dead-path cleanup completeness for impacted changes (`Pass`/`Fail`),
  - legacy-retention cleanup check (`Pass`/`Fail`) (obsolete old-behavior/deprecated/dead paths are removed for impacted scope),
  - backward-compatibility mechanism check (`Pass`/`Fail`) (no compatibility wrappers, dual-path behavior, or legacy fallback branches retained),
  - overall verdict (`Pass`/`Fail`).
- Round policy:
  - use deep review for every round (challenge assumptions, edge cases, and cleanup quality),
  - if a round finds blockers, requires persisted artifact updates, or discovers new use cases, classify the round (`Design Impact`/`Requirement Gap`/`Unclear`), apply required upstream updates through the classified stage path, and reset clean-review streak to 0,
  - if a round finds no blockers, no required persisted artifact updates, and no newly discovered use cases, mark `Candidate Go` and increment clean-review streak,
  - open `Go` only when clean-review streak reaches 2 consecutive deep-review rounds.
- Across rounds, track trend quality: issues should decline in count/severity or become more localized; otherwise escalate design refinement before proceeding.
- Round staged re-entry discipline (mandatory):
  - Step A: run review + missing-use-case discovery and record findings in the current round.
  - Step B: classify blockers as exactly one of `Design Impact`/`Requirement Gap`/`Unclear`.
  - Step C: if findings require updates, transition to the classified upstream stage path first, then modify required artifacts there and bump versions (`vN -> vN+1`).
  - Step D: record an "Applied Updates" entry in the review artifact (what changed, where, and why), including classification + return path.
  - Step E: start the next round from updated files only; do not carry unresolved edits in memory.
  - Step F: record clean-review streak state in the review artifact (`Reset`, `Candidate Go`, or `Go Confirmed`).
- Gate `Go` criteria (all required):
  - architecture fit check is `Pass` for all in-scope use cases,
  - shared-principles alignment check is `Pass` for all in-scope use cases,
  - layering fitness check is `Pass` for all in-scope use cases,
  - boundary placement check is `Pass` for all in-scope use cases,
  - decoupling check is `Pass` for all in-scope use cases,
  - module/file placement alignment check is `Pass` for all in-scope use cases,
  - existing-structure bias check is `Pass` for all in-scope use cases,
  - anti-hack check is `Pass` for all in-scope use cases,
  - local-fix degradation check is `Pass` for all in-scope use cases,
  - terminology/concept vocabulary is `Pass` for all in-scope use cases,
  - file/API naming clarity is `Pass` for all in-scope use cases,
  - name-to-responsibility alignment under scope drift is `Pass` for all in-scope use cases,
  - future-state behavior is consistent with target design basis across all in-scope use cases,
  - layer-appropriate structure and separation-of-concerns check is `Pass` for all in-scope use cases,
  - use-case coverage completeness is `Pass` for all in-scope use cases,
  - use-case source traceability is `Pass` for all in-scope use cases,
  - requirement coverage closure is `Pass` for the full in-scope requirement set,
  - design-risk use-case justification quality is `Pass` for all design-risk use cases,
  - redundancy/duplication check is `Pass` for all in-scope use cases,
  - simplification opportunity check is `Pass` for all in-scope use cases,
  - all in-scope use cases have overall verdict `Pass`,
  - no unresolved blocking findings (including any required design/call-stack updates),
  - for any impacted `Add`/`Modify`/`Rename/Move`/`Remove` scope items, decommission/cleanup and obsolete/deprecated/dead-path checks are `Pass`,
  - no new use cases are discovered in either of the two clean rounds,
  - legacy-retention cleanup check is `Pass` for all in-scope use cases,
  - backward-compatibility mechanism check is `Pass` for all in-scope use cases,
  - two consecutive deep-review rounds have no blockers, no required persisted artifact updates, and no newly discovered use cases.
- If issues are found:
  - classify each blocking round as exactly one of `Design Impact`/`Requirement Gap`/`Unclear` and record it in `future-state-runtime-call-stack-review.md` and `workflow-state.md`.
  - `Design Impact` (clear and high-confidence design issue): update design basis in Stage 3 (`Medium/Large`: `proposed-design.md`; `Small`: design section in `implementation-plan.md`), regenerate call stacks in Stage 4, then return to Stage 5.
  - `Requirement Gap`: update `requirements.md` first in Stage 2 (status `Refined`), then update design basis in Stage 3, regenerate call stacks in Stage 4, then return to Stage 5.
  - `Unclear` (cross-cutting/low-confidence): update `investigation-notes.md` in Stage 1 first, then proceed through `2 -> 3 -> 4 -> 5`.
- If naming drift is found, prefer explicit rename/split/move updates in the same review loop instead of carrying stale names forward.
- Even when a round reports no findings, still complete the round record in-file and run another deep-review round until the two-consecutive-clean stability rule is satisfied.
- Repeat until all gate `Go Confirmed` criteria are satisfied.
- Use the template in `assets/future-state-runtime-call-stack-review-template.md`.

### 6) Implement Source + Unit/Integration And Track Progress

- Use a bottom-up, test-driven approach: implement foundational dependencies first.
- Sequence is mandatory:
  - first ensure `implementation-plan.md` is finalized,
  - then initialize/update `implementation-progress.md`,
  - then execute source implementation with required unit/integration verification.
- Stage separation rule (mandatory):
  - Stage 6 implements source code and verifies file/module/service boundaries with unit/integration tests.
  - Stage 7 implements API/E2E tests and runs API/E2E test scenarios against acceptance criteria.
  - Stage 8 runs the code review gate after Stage 7 passes.
- Include requirement traceability in plan/progress (`requirement -> design section -> call stack/use_case -> implementation tasks/tests`).
- Integration test coverage is required for behavior that crosses module boundaries, process boundaries, storage boundaries, or external API boundaries. If any such behavior is not covered, record a concrete rationale.
- Finalize planning artifacts before kickoff:
  - `Small`: refine the draft implementation plan until future-state runtime call stack review passes final stability gate (`Go Confirmed`).
  - `Medium/Large`: create implementation plan only after future-state runtime call stack review passes final stability gate (`Go Confirmed`).
- Create the implementation progress document at implementation kickoff, after required pre-implementation artifacts are ready (including the proposed design document for Medium/Large).
- Implementation plan + real-time progress tracking are required for all sizes (`Small`, `Medium`, `Large`).
- Treat future-state runtime call stack + review as a pre-implementation verification gate: ensure each use case is represented and reviewed before coding starts.
- Start implementation only after the review gate says implementation can start and all in-scope use cases are `Pass`.
- Before first source-code edit in Stage 6, update `workflow-state.md`:
  - set `Current Stage = 6`,
  - set `Code Edit Permission = Unlocked`,
  - record transition evidence that Stage 5 gate is `Go Confirmed` and pre-edit checklist is satisfied.
- Ensure traceability when a proposed design doc exists: every design change-inventory row (especially `Rename/Move` and `Remove`) maps to implementation tasks and verification steps.
- Enforce clean-cut implementation: do not keep legacy compatibility paths.
- No-backward-compat implementation rule (mandatory): reject compatibility wrappers, dual-path reads/writes, and old-behavior fallback branches even if they make rollout easier.
- Decoupling-preservation implementation rule (mandatory): implementation must not introduce new tight coupling or cyclic dependencies across layers/modules.
- Module/file placement preservation rule (mandatory): do not leave touched files in the wrong concern folder just to minimize edits; move/split them when the current path no longer matches ownership.
- Implementation completeness rule (mandatory): implementation is not complete until obsolete code paths and compatibility shims in scope are removed.
- Stage 6 failure classification rule (mandatory):
  - `Local Fix`: issue is bounded and does not require requirement/design/call-stack updates; remain in Stage 6.
  - `Design Impact`: issue indicates architecture/decoupling or compatibility-policy breach requiring upstream design/runtime updates; re-enter `Stage 1 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6`.
  - `Requirement Gap`: missing/ambiguous requirement or acceptance criteria discovered during implementation; re-enter `Stage 2 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6`.
  - `Unclear`: cross-cutting/low-confidence root cause; re-enter `Stage 0 -> Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6`.
- If a change only "works" by leaving a file in the wrong folder or adding new misplaced files, do not classify it as `Local Fix`; treat it as `Design Impact` unless the real issue is missing requirements.
- Use "one file at a time" as the default execution strategy, not an absolute rule.
- When rare cross-referencing is unavoidable, allow limited parallel/incomplete implementation, but explicitly record:
  - the cross-reference smell,
  - the blocked dependency edge,
  - the condition to unblock,
  - the required proposed-design-document update.
- Update progress in real time during implementation (immediately after file status changes, test runs, blocker discoveries, and design-feedback-loop updates).
- Track change IDs and change types in progress (`Add`/`Modify`/`Rename/Move`/`Remove`) so refactor deltas remain explicit through execution.
- Track file build state explicitly (`Pending`, `In Progress`, `Blocked`, `Completed`, `N/A`).
- Track unit/integration test state separately (`Not Started`, `In Progress`, `Passed`, `Failed`, `Blocked`, `N/A`).
- If a file is blocked by unfinished dependencies, mark it `Blocked` and record the dependency and unblock condition.
- Mark a file `Completed` only when implementation is done and required tests are passing.
- Mark Stage 6 complete only when:
  - implementation plan scope is delivered (or deviations are explicitly documented),
  - required unit/integration tests pass,
  - no backward-compatibility shims or legacy old-behavior branches remain in scope,
  - decoupling boundaries remain valid (no newly introduced unjustified tight coupling/cyclic dependencies),
  - touched files either already have correct placement or are moved/split so their paths match owning concerns.
- Use `assets/implementation-plan-template.md` and `assets/implementation-progress-template.md`.
- Do not speak for routine `implementation-plan.md`/`implementation-progress.md` edits. Announce only for persisted `workflow-state.md` events (Stage 6 entry, lock/unlock change, gate/transition outcomes).

### 7) Implement API/E2E Tests And Run API/E2E Test Gate (Mandatory)

- Run this stage immediately after `Stage 6` completes.
- At Stage 7 entry, update `workflow-state.md` and keep `Code Edit Permission = Unlocked` while API/E2E test artifacts are being implemented/executed.
- Create/update `tickets/in-progress/<ticket-name>/api-e2e-testing.md` as the canonical scenario + result artifact.
- Stage 7 scope includes:
  - implementing API test files/harness as needed,
  - implementing E2E test files/harness as needed,
  - executing API/E2E scenarios mapped from acceptance criteria.
- If Stage 7 failures require source-code changes, declare re-entry and return to Stage 6 first.
- Scenario sources (mandatory):
  - requirement-driven scenarios (must cover all critical requirements and flows),
  - design-risk-driven scenarios (must cover technical risks introduced by architecture/design choices).
- Acceptance-criteria closure loop (mandatory):
  - build and maintain an explicit Stage 7 acceptance-criteria matrix sourced from `requirements.md` (`acceptance_criteria_id` -> mapped scenario IDs -> execution status),
  - every in-scope acceptance criterion must map to at least one executable API/E2E scenario before execution starts,
  - any acceptance criterion with status `Unmapped`, `Not Run`, `Failed`, or `Blocked` keeps Stage 7 open and requires re-entry unless explicitly marked `Waived` by user decision for infeasible cases,
  - rerun the required re-entry chain and return to Stage 7 until all in-scope acceptance criteria are `Passed` or explicitly `Waived`.
- For each scenario, record at minimum:
  - `scenario_id`,
  - mapped `acceptance_criteria_id` values,
  - mapped `requirement_id` and `use_case_id` values,
  - source type (`Requirement`/`Design-Risk`),
  - test level (`API`/`E2E`),
  - expected outcome,
  - execution command/harness,
  - result (`Passed`/`Failed`/`Blocked`/`N/A`).
- API test depth rule (mandatory): when scenario level is `API`, validate contract-level behavior including required fields/schema shape, status codes, and error payload behavior for mapped acceptance criteria.
- Cross-boundary test rule (mandatory): for client/server or multi-service scope, include API/E2E scenarios that validate cross-boundary interaction behavior (request -> boundary handoff -> downstream effect -> returned state).
- Manual testing policy: do not include manual testing in the default workflow.
- Feasibility policy:
  - if a scenario is not executable in current environment (missing secrets/tokens, unavailable partner system, infra limit), record concrete infeasibility reasons and constraints in `api-e2e-testing.md` and `implementation-progress.md`,
  - record compensating automated evidence and residual risk notes for each infeasible critical scenario,
  - mark Stage 7 as `Blocked` unless the user explicitly accepts a waiver for the infeasible acceptance criteria.
- Test feedback escalation policy (mandatory):
  - classify each failing Stage 7 scenario as exactly one of `Local Fix`, `Design Impact`, `Requirement Gap`, or `Unclear`,
  - before final classification, run an investigation screen:
    - if issue scope is cross-cutting, touches unknown runtime paths, or root-cause confidence is low, mark `Investigation Required` and reopen understanding stage first (`investigation-notes.md` must be updated before design/requirements artifact updates),
    - if issue is clearly bounded with high root-cause confidence, continue classification directly.
  - `Local Fix` is allowed only when responsibility boundaries stay intact, no new use case/acceptance criterion is needed, and no requirement/design changes are needed.
  - if a fix works functionally but degrades layering/separation-of-concerns, it is **not** `Local Fix`; classify as `Design Impact`.
  - if a fix only works by leaving a file in the wrong folder or adding a new misplaced file, it is **not** `Local Fix`; classify as `Design Impact`.
  - classify as `Requirement Gap` when failing behavior reveals missing functionality/use case or missing/ambiguous acceptance criteria.
  - apply re-entry declaration before source code edits when source/design/requirement updates are needed.
  - `Local Fix` path: update artifacts first, then rerun `Stage 6 -> Stage 7`.
  - `Design Impact` path: `Stage 1 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7`.
  - `Requirement Gap` path: `Stage 2 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7`.
  - `Unclear`/cross-cutting root cause path: `Stage 0 -> Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7`.
- Stage completion gate:
  - all in-scope acceptance criteria from `requirements.md` are mapped to Stage 7 scenarios,
  - all executable in-scope acceptance criteria have execution status `Passed`,
  - all executable mapped API/E2E scenarios are resolved (`Passed`), with no unresolved failures/blockers,
  - if any acceptance criterion is infeasible due to environment constraints, Stage 7 remains `Blocked` until explicit user waiver is recorded with constraints + compensating evidence + residual risk.
- Before transitioning to Stage 8, update `workflow-state.md` with Stage 7 gate result and transition evidence.
- Use `assets/api-e2e-testing-template.md`.
- Do not speak for `api-e2e-testing.md` edits alone. Announce when `workflow-state.md` records Stage 7 entry, gate result, and any re-entry declaration/lock-state change.

### 8) Run Code Review Gate (Mandatory, Post-Testing)

- Run this stage only after `Stage 7` API/E2E test gate is `Pass`.
- At Stage 8 entry, update `workflow-state.md` and set `Code Edit Permission = Locked`.
- Create/update `tickets/in-progress/<ticket-name>/code-review.md` as the canonical code review artifact.
- Scope:
  - source files and test files,
  - include changed files and directly impacted related files when structural risk exists.
- Mandatory review checks:
  - separation-of-concerns and responsibility boundaries,
  - layering quality under shared principles (layering emerges from SoC and coordination needs; reject both missing orchestration extraction and unjustified pass-through layers),
  - explicit decoupling quality (low coupling, clear dependency direction, no unjustified cycles),
  - architecture/layer boundary consistency with design basis,
  - module/file placement and folder ownership consistency with design basis,
  - naming-to-responsibility alignment and drift,
  - duplication and patch-on-patch complexity smells,
  - no backward-compatibility mechanisms and no legacy code retention,
  - test quality and test maintainability.
- Source file size policy (mandatory):
  - measure line counts explicitly per changed source file:
    - effective non-empty line count command: `rg -n "\\S" <file-path> | wc -l`
    - per-file changed-line delta command: `git diff --numstat <base-ref>...HEAD -- <file-path>`
  - enforcement baseline uses effective non-empty line count.
  - for changed source files with effective non-empty line count `<= 500`, run normal review checks.
  - hard limit rule: if any changed source file has effective non-empty line count `> 500`, default classification is `Design Impact` and Stage 8 decision is `Fail`.
  - for `> 500` hard-limit cases, do not continue by default; trigger re-entry with investigation checkpoint first (`Stage 1 -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7 -> Stage 8`).
  - no soft middle band (`501-700`) and no default exception path in this workflow.
  - delta gate (mandatory): if a single changed source file has `> 220` changed lines in the current diff, record a design-impact assessment even when file size is `<= 500`.
- Gate decision:
  - `Pass`: continue to `Stage 9` only when all mandatory review checks (including `<=500` hard-limit + required `>220` delta-gate assessments + shared-principles/layering + decoupling + module/file placement + no-backward-compat/no-legacy checks) are `Pass`.
  - `Fail`: apply re-entry declaration and follow re-entry mapping before any source code edits.
- Treat wrong-location files as review failures when the path obscures ownership (for example, platform-specific code outside its platform folder without explicit shared-boundary rationale).
- If code review requires source changes, rerun `Stage 6 -> Stage 7 -> Stage 8`.
- Use `assets/code-review-template.md`.
- Do not speak for `code-review.md` edits alone. Announce when `workflow-state.md` records Stage 8 entry, gate result, and any re-entry declaration.

### 9) Synchronize Project Documentation (Mandatory Post-Testing + Review)

- After Stage 7 API/E2E testing and Stage 8 code review are complete, update project documentation under the project `docs/` folder (and other canonical architecture docs such as `ARCHITECTURE.md` when impacted) so docs reflect the latest codebase behavior.
- Treat `docs/` as the long-lived canonical source of truth for the current codebase.
- Treat ticket artifacts under `tickets/` as task-local, time-bound records; they are not the long-term source of truth.
- If relevant docs do not exist yet, create new docs in `docs/` with clear natural names that match current functionality.
- If relevant docs already exist, update them in place instead of creating duplicate overlapping docs.
- Update docs for:
  - new modules/files/APIs,
  - changed runtime flows,
  - renamed/moved/removed components,
  - updated operational or testing procedures when behavior changed.
- If there is no docs impact, record an explicit "No docs impact" decision with rationale in `implementation-progress.md`.
- Docs synchronization is complete only when docs content aligns with the final implemented behavior.
- After docs synchronization result is recorded (`Updated`/`No impact`), announce only with the persisted `workflow-state.md` transition/gate update.

### 10) Final Handoff

- Complete handoff only after implementation execution, Stage 7 API/E2E testing, Stage 8 code review, and docs synchronization are complete.
- Handoff summary must include:
  - delivered scope vs planned scope,
  - verification summary (unit/integration plus API/E2E testing, acceptance-criteria closure status, and for infeasible criteria documented constraints + compensating automated evidence + explicit user waiver reference),
  - docs files updated (or explicit no-impact rationale).
- Ticket state transition:
  - keep ticket under `tickets/in-progress/<ticket-name>/` by default after handoff,
  - move ticket to `tickets/done/<ticket-name>/` only after explicit user confirmation that the ticket is finished/verified or explicit user move instruction.
  - if the user reopens a completed ticket, move it back to `tickets/in-progress/<ticket-name>/` before any additional artifact updates.
- Speak final handoff completion only after all required artifacts/docs outputs are written and the final `workflow-state.md` transition/gate state is persisted.

## Output Defaults

If the user does not specify file paths, write to a project-local ticket folder in stage order:
These defaults list file-producing stages; gating and handoff rules still follow the full workflow above.

- Stage 0 (bootstrap + draft requirement):
  - create/use `tickets/in-progress/<ticket-name>/`
  - if git repo, create/switch ticket worktree/branch
  - create/update `tickets/in-progress/<ticket-name>/workflow-state.md` (`Current Stage = 0`, `Code Edit Permission = Locked`)
  - `tickets/in-progress/<ticket-name>/requirements.md` (`Draft`)
- Stage 1 (investigation + understanding + triage):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` transition (`0 -> 1`)
  - `tickets/in-progress/<ticket-name>/investigation-notes.md`
- Stage 2 (requirements refinement to `Design-ready`):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` transition (`1 -> 2`)
  - update `tickets/in-progress/<ticket-name>/requirements.md` in place
- Stage 3 (design basis):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` transition (`2 -> 3`)
  - `Small`: start/refine `tickets/in-progress/<ticket-name>/implementation-plan.md` (solution sketch section only for design basis).
  - `Medium/Large`: create/refine `tickets/in-progress/<ticket-name>/proposed-design.md`.
- Stage 4 (runtime modeling):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` transition (`3 -> 4`)
  - `tickets/in-progress/<ticket-name>/future-state-runtime-call-stack.md`
- Stage 5 (review gate, iterative):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` transition (`4 -> 5`)
  - `tickets/in-progress/<ticket-name>/future-state-runtime-call-stack-review.md`
- Stage 6 (only after gate `Go Confirmed`):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` (`Current Stage = 6`, `Code Edit Permission = Unlocked` only when pre-edit checklist is `Pass`)
  - finalize/update `tickets/in-progress/<ticket-name>/implementation-plan.md`
  - `tickets/in-progress/<ticket-name>/implementation-progress.md`
  - execute source implementation plus required unit/integration verification and log progress in real time
  - close Stage 6 only when no backward-compatibility/legacy-retention paths remain in scope, decoupling boundaries remain valid, and touched files have correct module/file placement
- Stage 7 (API/E2E test implementation + API/E2E test gate):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` (`Current Stage = 7`, `Code Edit Permission = Unlocked`)
  - create/update `tickets/in-progress/<ticket-name>/api-e2e-testing.md`
  - maintain acceptance-criteria matrix (`acceptance_criteria_id` -> scenario coverage -> pass status)
  - record scenario execution results and any escalation decisions in `tickets/in-progress/<ticket-name>/implementation-progress.md`
- Stage 8 (code review gate, only after `Stage 7 = Pass`):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` (`Current Stage = 8`, `Code Edit Permission = Locked`)
  - create/update `tickets/in-progress/<ticket-name>/code-review.md`
  - record gate result (`Pass`/`Fail`) and any re-entry declaration before `Stage 9`
- Stage 9 (post-testing documentation sync):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` transition (`8 -> 9`)
  - update existing impacted docs in place (for example `docs/**/*.md`, `ARCHITECTURE.md`)
  - create missing relevant docs in `docs/` when no existing doc covers the implemented functionality
  - record docs sync result in `tickets/in-progress/<ticket-name>/implementation-progress.md` (`Updated`/`No impact` + rationale)
- Stage 10 (ticket state transition):
  - update `tickets/in-progress/<ticket-name>/workflow-state.md` transition (`9 -> 10`) and final state record
  - keep ticket in `tickets/in-progress/<ticket-name>/` unless user explicitly confirms completion/verification or asks to move it
  - on explicit user completion/verification instruction, move ticket folder to `tickets/done/<ticket-name>/`
  - if user reopens later, move it back to `tickets/in-progress/<ticket-name>/` before new updates

## Templates

- `assets/proposed-design-template.md`
- `assets/future-state-runtime-call-stack-template.md`
- `assets/future-state-runtime-call-stack-review-template.md`
- `assets/implementation-plan-template.md`
- `assets/implementation-progress-template.md`
- `assets/code-review-template.md`
- `assets/api-e2e-testing-template.md`
- `assets/workflow-state-template.md`
