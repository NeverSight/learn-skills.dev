---
name: spec-workflow
description: Drives a spec-first, phased execution workflow for feature work. Use when the user wants a feature spec, an implementation plan, or an iterative "next task only" loop where requirements stay locked in `docs/specs/*.spec.md` and execution lives in one or more mutable `docs/specs/plans/*.plan.md` files.
---

# Spec Workflow Skill

## Purpose

This skill keeps one stable spec per feature as the source of truth and drives implementation through one or more mutable phased plan files.

Use this model:

- **Spec = what**
- **Plan = how**

The spec should remain mostly locked after approval. The plan evolves as tasks are completed.

## When to Use

Use this skill when the user wants any of the following:

- a spec-first workflow for a feature
- a stable requirements document plus an execution plan
- phased implementation with explicit task tracking
- a "do only the next task" loop
- an agent workflow that updates plan progress after each implementation step

Typical trigger phrases:

- `Spec: build ...`
- "create a spec and plan for this feature"
- "turn this into a phased implementation plan"
- "implement the next task from the plan"
- "use the spec as locked requirements"

Do not use this skill for trivial one-off edits unless the user explicitly asks for the workflow.

## Canonical Layout

Prefer this repository layout unless the user or repo already has an equivalent convention:

```text
AGENTS.md
CLAUDE.md

docs/
  specs/
    010_task-management.spec.md
    plans/
      010_task-management.plan.md
```

Use a shared numeric prefix and stable slug for the feature across the spec and plan files.

If `CLAUDE.md` exists in the repository, treat it as an additional instruction source alongside `AGENTS.md`.

## Naming Guidance

Use clear, stable file names:

- `<id>_<slug>.spec.md`
- `<id>_<slug>.plan.md`

Prefer readable slugs such as:

- `010_task-management`
- `011_user-invitations`
- `012_billing-webhooks`

Do not use vague slugs such as `stuff`, `misc`, or `new-feature`.

## Core Model

### 1) Spec = source of truth

The spec defines:

- overview
- scope and non-scope
- requirements
- contracts, invariants, and rules
- acceptance criteria
- references to the plan file or files

The spec should not track task checkboxes or step-by-step execution status.

### 2) Plan = phased execution

The plan defines:

- phases
- atomic task IDs
- task checkboxes
- expected files to change
- validation commands to run after the phase's tasks are complete
- phase gates and acceptance checks

The plan is the primary mutable document during implementation.

## Required File Contents

### Spec File

`docs/specs/<id>_<slug>.spec.md` should contain:

1. `Overview`
2. `Scope / Non-Scope`
3. `Requirements`
4. `Acceptance Criteria`
5. `Plan References`

The `Plan References` section should point to one or more files in `docs/specs/plans/`.

### Plan File

`docs/specs/plans/<id>_<slug>.plan.md` should contain phased execution such as:

- `Phase 1 - Skeleton + Types`
- `Phase 2 - Validation + Errors`
- `Phase 3 - Core Logic`
- `Phase 4 - Adapters`
- `Phase 5 - Hardening`

Within each phase, include:

- atomic tasks with stable IDs such as `P1.T1`
- checkboxes
- expected files to change
- validation commands to run after the phase's tasks are complete
- a gate describing what must be true before the phase is considered complete

The final phase must include a task to update `README.md` to reflect any user-visible changes introduced by the feature. This update must integrate the new content into the existing README — preserve all sections that are unaffected by the feature. Do not rewrite or replace the README wholesale. Read the current README first, identify which sections need to change, and edit only those sections.

## Holistic Validation Pass

Before approving, revising, or executing a spec/plan pair, perform these checks against the repository:

1. Surface audit
   - search for every renamed or removed symbol, config key, route, UI string, contract, and behavior named in the spec
   - identify all impacted layers, not just the files already named in the docs
   - include any relevant application, UI, API, data, infrastructure, automation, test, and documentation surfaces

2. Scope consistency
   - check for contradictions between Overview, Scope, Out of Scope, Requirements, Contracts, Acceptance Criteria, and Plan References
   - if an acceptance criterion requires changing an out-of-scope layer, either narrow the acceptance criterion or bring that layer into scope

3. Phase executability
   - verify each phase can pass its listed validation commands using only work completed in that phase and earlier phases
   - reorder phases when build, type, test, validation, deployment, migration, or integration steps depend on later-phase changes

4. Explicit ownership
   - if a requirement says to update callers, consumers, adapters, views, handlers, controllers, services, tests, docs, configs, or similar downstream surfaces, name them explicitly in the plan tasks and expected-file summary
   - do not leave high-risk coupling as implied cleanup

5. Contract boundaries
   - distinguish product behavior, application/runtime behavior, storage/schema behavior, integration behavior, and infrastructure behavior
   - state clearly when a cleanup changes one boundary but intentionally leaves another unchanged

When reviewing, present findings in this order:

1. contradictions
2. missing implementation surface
3. phase or ordering risks
4. test or verification gaps
5. suggested doc fixes

## Choosing the Active Spec and Plan

When multiple feature specs or plans exist, determine the active files in this order:

1. explicit user-provided file or feature ID
2. files referenced in the current task context
3. files matching the current branch or active feature name
4. the only matching spec/plan pair in the repository

If multiple candidates still remain, do not guess. Ask the user which feature ID or file pair to use.

## Single Plan vs Multiple Plans

Use one plan file by default.

Use multiple plan files only when the feature has clearly separate execution tracks, such as:

- backend and frontend work that can progress independently
- application work plus infrastructure or migration work
- a large feature with separate rollout streams

If multiple plans exist:

- the spec must reference all of them
- each plan must own a distinct scope
- the current run should operate on only one active plan unless the user explicitly asks otherwise

## Workflow

### Phase A: Create or refine the spec

When no spec exists yet:

1. Gather context from the repo and the user request.
2. Run the holistic validation pass for the known feature surface so the draft spec reflects actual repo coupling.
3. Draft the spec file in `docs/specs/`.
4. Include plan references in the spec.
5. Ask the user to review and lock the spec before implementation.

When a spec already exists:

1. Treat it as the source of truth.
2. Do not modify it unless the user explicitly asks to revise requirements.
3. Still run the holistic validation pass before accepting the spec as execution-ready.

### Phase B: Generate the phased plan

Once the spec is approved or already locked:

1. Create or revise the plan file in `docs/specs/plans/`.
2. Run the holistic validation pass against the locked spec and current repo state before finalizing phase boundaries.
3. Break execution into phases.
4. Write atomic tasks with IDs and checkboxes.
5. Add expected files, validation commands, and gates.
6. Keep plan steps concrete enough that one run can complete exactly one task.

### Phase C: Implementation loop

For each execution run:

1. Read `AGENTS.md`.
2. Read `CLAUDE.md` if it exists.
3. Read the locked spec in `docs/specs/`.
4. Read the active plan in `docs/specs/plans/`.
5. Identify the active phase: the first phase that still has unchecked tasks.
6. If any task in the phase is underspecified, refine those plan tasks before coding.
7. Implement all unchecked tasks in the active phase, one at a time, in order.
8. Update each task checkbox as its implementation work is completed.
9. After all tasks in the phase are complete, run the phase's validation commands.
10. Verify the phase gate.
11. Present a phase review to the user (see Phase Boundary Rule).
12. Stop. Wait for the user to either provide feedback or explicitly approve moving to the next phase.

## Task Design Rules

Each task should usually fit in one focused implementation run and produce one reviewable diff.

Good task shapes:

- add domain types for task entity
- add request validation for create-task route
- implement repository method for task lookup

Bad task shapes:

- build backend
- implement entire feature
- finish API and UI

If a plan contains oversized tasks, split them before implementation.

## Execution Rules

When operating in the implementation loop:

- execute all unchecked tasks within the active phase, in order
- do not pull in tasks from a later phase
- keep diffs minimal and scoped to each task
- use the spec as locked requirements
- prefer updating the plan over rewriting the spec
- run validation after all tasks in the active phase are complete, not after each individual task
- stop at the phase boundary and wait for explicit user instruction before starting the next phase

If a task within the active phase is blocked:

- do not silently skip to a later task
- record the blocker in the plan
- ask the user for direction if the blocker changes requirements or ordering
- do not advance to the next phase while a blocker is unresolved

## Phase Boundary Rule

A phase is complete when all of its tasks are checked off and its gate condition is satisfied.

When a phase is complete:

1. Run phase-scoped validation commands.
2. Run the full test suite. If any previously passing tests now fail, fix the regression in the implementation — do not modify tests, the spec, or phase boundaries to work around it. Surface to the user if the regression is out of scope.
3. Verify the phase gate (all listed acceptance checks pass).
4. Update the plan to reflect phase completion.
5. Present a phase review to the user in this format:

   ```
   ## Phase <N> Complete

   **Tasks completed:** <list with task IDs>
   **Files changed:** <list>
   **Gate:** <pass / fail with details>

   ---
   Provide feedback to adjust this phase, or reply "proceed" to start Phase <N+1>.
   ```

6. Stop. Do not begin the next phase.

The user may respond with:

- **Feedback** — corrections, additional changes, or questions about the phase just completed. Apply the feedback within the current phase before asking again.
- **Explicit continuation** — any clear instruction to move forward, such as "proceed", "continue to phase 2", or "next phase".

If the user provides feedback, address it and re-present the phase review prompt when done. Do not advance until the user explicitly approves.

## Validation Rules

Each phase should include explicit validation commands that run after all tasks in the phase are complete.

Examples:

- `npm test -- task.validation`
- `npm run typecheck`
- `cargo test task_service`
- `pytest tests/tasks/test_create_task.py`

If a phase does not list validation commands, add appropriate ones to the plan before implementation begins.

Do not run validation after individual tasks. Run it once when all tasks in the active phase are done.

### Full Suite Requirement

After running phase-scoped validation, always run the full test suite. A phase is not complete if the full suite is broken, even if the phase's own validation commands pass.

If the full suite has failures:

- Fix the regression by correcting the implementation — do not delete, skip, or modify failing tests to make them pass.
- Do not modify the spec or restructure plan phases to work around the failure.
- If the regression cannot be fixed within the current phase's scope, surface it to the user before proceeding.

## Plan Refinement Rule

If the next unchecked task is underspecified, ambiguous, or too large, refine the plan first.

Allowed refinements include:

- clarifying the task wording
- splitting the task into smaller tasks
- adding expected files
- adding validation commands
- clarifying the phase gate

Do not hide major design changes inside plan refinement. If the requirements change, that is a spec issue.

## Spec Lock Rule

Treat the spec as locked once the user approves it or clearly treats it as the accepted requirements baseline.

Do not modify a locked spec unless:

- the user explicitly asks to change requirements
- implementation reveals a true contradiction or impossibility that requires spec revision

If the spec must change, update the spec deliberately, then reconcile the plan to match it.

## Spec Change Escalation

During planning or implementation, if the agent discovers that the spec likely needs to change, it must say so explicitly before proceeding.

Examples:

- the spec conflicts with the actual repository constraints
- the spec is missing a requirement needed to complete the next task
- the spec contains an invalid assumption
- the accepted scope should be split, reduced, or expanded to remain coherent
- the current plan cannot continue without changing a locked requirement

When this happens, present the issue in this format:

1. `Affected section`
2. `Problem`
3. `Why discovered now`
4. `Proposed revision`
5. `Plan impact`

Wait for user approval before editing the spec.

Do not silently edit the spec just because implementation uncovered new information.

## Plan Mutation Rule

The plan is expected to change during the work.

Allowed plan updates include:

- checking off completed tasks
- clarifying task wording
- splitting a task into smaller tasks
- adding acceptance notes
- updating commands or file lists
- recording blockers

Do not convert the plan into a narrative status document. Keep it execution-oriented.

## Drift Reconciliation Rule

If the codebase has already drifted from the plan but not from the spec:

1. reconcile the plan to reflect reality
2. mark already completed work accurately
3. add or revise tasks so the remaining plan still matches the spec
4. then continue with the next unchecked task

Do not force implementation to follow an outdated plan when the spec remains correct.

## Blocker Handling

When the next task is blocked, update the plan with a concise blocker note such as:

```md
- Blocked: waiting on schema decision for `status` enum
- Blocked: task depends on `P2.T3` requirement clarification
```

State:

- what is blocked
- why it is blocked
- whether the blocker is a plan issue or a spec issue

Do not skip forward unless the user explicitly approves resequencing.

## Completion Rule

When all tasks in the active plan are complete:

1. verify the implemented work against the spec acceptance criteria
2. identify any remaining gaps or follow-up work
3. update the plan to reflect completion accurately
4. report whether the feature appears ready for review, rollout, or another planning pass

Completion is defined by the spec and acceptance criteria, not just by checked boxes.

## Standard Operating Prompt

Use this instruction pattern when the user wants the loop:

> Use `@AGENTS.md` for constraints.
> Use `@CLAUDE.md` for additional constraints if it exists.
> Use `@docs/specs/<id>_<slug>.spec.md` as LOCKED requirements and do not modify it unless explicitly instructed.
> Use `@docs/specs/plans/<id>_<slug>.plan.md` to identify the active phase (first phase with unchecked tasks).
> Implement all unchecked tasks in that phase, in order.
> After completing all tasks in the phase, run the phase's validation commands.
> When the phase is complete, verify the phase gate, present the phase review, and invite feedback or a proceed instruction.
> Do not advance to the next phase until the user explicitly approves.

## Output Expectations

When drafting the workflow artifacts:

- clearly state which spec and plan files are being used
- identify whether you are creating the spec, generating the plan, refining the plan, or executing the next task
- when implementing, name the selected task ID before making edits

When finishing an implementation run:

- report the phase and each task completed within it
- summarize files changed
- list commands run and results
- state whether the phase gate was satisfied
- confirm the plan was updated
- present the phase review prompt and explicitly invite feedback or a proceed instruction before stopping

## Guardrails

- Do not treat the spec and plan as interchangeable.
- Do not store execution checkboxes in the spec.
- Do not advance past the current phase without explicit user instruction.
- Do not implement tasks from a later phase in the same run as the active phase.
- Do not silently change locked requirements by editing the spec during implementation.
- Do not guess which spec or plan is active when multiple candidates exist.
- Prefer one spec per feature, with one or more plan files referenced from that spec only when needed.
