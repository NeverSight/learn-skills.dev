---
name: approve-plan
description: Turns an approved plan into a spec (.plans/{task}/plan.md) and a task list (tasks.md), sized by the change's tier, then picks the task loop, model and effort and starts an unattended run with ship-plan in this checkout, which ends in the configured delivery (a pull request by default). Use right after the user approves a plan from forge or a fix plan from diagnose-bug, or says "approve", "ship it" or "go".
---

<instructions>

The user has approved the plan discussed previously. Your task is to size the work, create the specification, create the implementation task list, and start the run. After that, the user's part is done: the run ends in the configured delivery, a pull request by default.

## Instructions

0.  **Size the work first.** Settings come from the workflow config (`pick-tier/CONFIG.md`); only `tier.mjs` reads it, and everything below reads the resolved values from `tier.md`. Run the **pick-tier** skill in estimate mode on the approved plan: the files it would touch, the lines it would change, whether it touches authentication, routing or a server API, and whether a person can see the difference. Write `.plans/<task>/tier.md`. If the user declared a tier, pass `--tier <X>` to `tier.mjs`.

    - **Tier S** — skip the specification. Write a one-line note into `.plans/<task>/plan.md` saying the change is Tier S and is implemented directly, write a `tasks.md` with a single build task, and go to step 5. No spec, no dialogue replay, no review, no browser walkthrough.
    - **Tier M** — write a short spec (see the tier budget below).
    - **Tier L** — write the full spec (see the mandatory elements below).

1.  **Synthesize History:** Review the Socratic dialogue and the approved plan. Extract all technical decisions, code references, and algorithms discussed.
2.  **Generate Specification:** Write the spec with `Write` to `.plans/<task>/plan.md` (where `<task>` is a slugified version of the task name). The specification is the "spec" — the authoritative reference for what to implement.
    - **A fix plan from diagnose-bug:** write the spec and task list into its notes folder, `.plans/<bug>/`, next to `diagnosis.md`, the repro and `fix.patch`. The fix starts from `fix.patch`. The repro becomes a test in the repo where one fits; otherwise rerunning it is an acceptance criterion.
    - **A plan from design-forge** (it has a `## Design` section): use the plan folder that section names instead of a new slug. Write the section verbatim to `.plans/<task>/design.md`. Leave `.plans/<task>/taste/` as it is.
    - **The tier budget:** Tier M specs are at most 120 lines and carry only: Problem, Solution, the files to change, the acceptance criteria, the risks, and the test plan. Tier L specs carry the full mandatory elements.
3.  **Review Specification:** Re-read the generated spec end-to-end. Verify that every phase from the approved plan is covered, that the sections the tier requires are present, and that a fresh agent could implement the feature using only this document. Fix any gaps, inconsistencies, or ambiguities you find.
4.  **Create Task List:** `Write` `.plans/<task>/tasks.md` with every task from the approved plan, in phase order — one `##` header per phase, one `- [ ]` line per task:

    ```markdown
    ## Research
    - [ ] Map the existing call sites

    ## Build
    - [ ] Add the parser
    ```

    Use the same phases that appear in the spec. The task-loop skills read and tick this file; it is the progress tracker, the spec is not. **Append a final phase called "Verification"** with each acceptance criterion from the approved plan as a separate task in that phase. This ensures the agent verifies all acceptance criteria before declaring the task complete.
    - **Manual criteria stay out of the automated list.** A criterion that can only be checked against a real backend, a real account or a real device is written in the spec as `manual: <criterion>` — with what a human must do to check it. Put those in a separate **Manual checks** section of `tasks.md`, not in the Verification phase. The automated run must not spend turns trying to check them.
    - **Design plans:** when `design.md` exists, native flow-walk steps, and captures marked manual in `design.md`, go to **Manual checks**.
    - The "Verification" phase must include "Record Updates" at the end iff the approved plan contains a "Record Updates" section. The task description must encode this two-part logic: (1) review the complete implementation; (2a) if the implementation matches the planned Record Updates, write those exact entries into `.agents/RECORD.md`; (2b) if the implementation **diverged** from the planned entries, **do not write a wrong entry** — instead surface the divergence in your final implementation summary so the user can resolve it.
5.  **Pick the loop by rule.** Once `tasks.md` exists, count its `##` phases, leaving out `Verification` and `Manual checks`, and re-run `node <pick-tier>/tier.mjs` with the same files plus `--phases N`, `--tier <X>` if the user declared a tier, and `--out .plans/<task>/tier.md`. The loop is the `LOOP:` line in that file: tier S or M is `micro`; tier L with a sensitive path, or more than 3 phases, is `phased`; every other tier L is `simple`; a `loop` set in the config (marked `(config)`) counts as chosen. If the user's approval names a loop, write `LOOP: <loop> (user)` in `tier.md` in place of that line. Nothing else may set a loop the rule didn't pick. Give the `LOOP:` line as the reason.
6.  **Pick the model and effort,** with a one-line reason. The orchestrator runs as the `ORCHESTRATOR:` line of `tier.md` says (`inherit` means the model you are on); the helpers it spawns run on the models in the `## Steps` list of `tier.md`. If the user's approval named a model or effort ("opus, high"), use those instead. If it named a model for a specific step ("build on haiku"), rewrite that step's line in the `## Steps` list of `tier.md` as `<step> — <model> (user)`, e.g. `Build — haiku (user)`; a model named without a step still sets the orchestrator.
7.  **The browser walkthrough needs a fixture.** The walkthrough runs against the repo's committed fixture, the `FIXTURE:` path in `tier.md` (default `.harness/`) — a fake backend the repo ships, which never contacts a real backend. If the repo has no fixture, the walkthrough is skipped and reported as "no fixture at `<path>` — run `make-fixture` in this repo". Never write a recipe, and never point the app at a real backend.
8.  **Start the run.** Don't wait for another OK: the plan's approval covers it.
    - Create a branch in this checkout, named `BRANCH_PREFIX:` (when not `none`) followed by the task slug, from `BASE_BRANCH:` (`auto` means the repo's default branch), then run the command yourself with the chosen model and effort: `/ship-plan <absolute path to .plans/<task>> <loop>`, where `<loop>` is the `LOOP:` line of `tier.md` (`micro`, `simple` or `phased`, without the `(user)` mark).
    - The run happens here, on that branch, unattended. It never commits to the default branch, never merges, and never touches files outside the repo. A killed run resumes from its `run-state.md` checkpoint, so the same command is safe to run again.
9.  **Report** in three lines: the tier and what it means; where the spec and task list are; the loop (from `LOOP:` in `tier.md`), model and effort, each with its reason; and that the run continues here, unattended, and ends as `DELIVERY:` says. Say "pull request" only when `DELIVERY:` is `pr` or `draft-pr`; for `push` say the branch is pushed, for `local` say it stays on a local branch, not pushed.

## The tier budget (Tier M)

A Tier M spec is at most 120 lines and has these sections, in this order:

1. **Problem** — one paragraph: what is wrong or missing today.
2. **Solution** — the approach, in bullets.
3. **Files** — the files to create or change, full paths, one line each on what changes in them.
4. **Acceptance criteria** — numbered, each checkable, with the check named. A criterion that needs a real backend, a real account or a real device is written as `manual: <criterion>` with the human steps.
5. **Risks** — the ways this can go wrong, and what happens then.
6. **Test plan** — which test file covers what, and the command that runs them.

Nothing else. A Tier M spec that needs more than 120 lines is a Tier L change wearing a Tier M hat: raise the tier and write the full spec.

## Mandatory Elements (Tier L)

The specification must be a **standalone technical document**. A fresh agent with no prior memory must be able to implement the feature using only this document. It MUST include the following sections explicitly:

1.  **Dialectical Outcomes (Why):** Reasoning for key decisions based on the Socratic dialogue. Document trade-offs and alternatives rejected.
2.  **Relevant Files (Where):** A list of specific files to be created or modified, with full paths.
3.  **Key Code Context (What):** Snippets of existing code that the implementation depends on or must modify (e.g., struct definitions, function signatures). Do not just reference them; include the code blocks.
4.  **Implementation Algorithm (How):** The explicit logic for implementation. Detail state machines, logic flows, or data transformations.
5.  **Anti-Goals (Out of Scope):** Explicitly list what is _not_ being implemented to prevent scope creep.
6.  **Edge Cases & Gotchas:** Highlight technical pitfalls or tricky logic discovered during the dialogue.
7.  **Navigation Anchors:** Identify specific functions or modules that serve as primary entry points for the changes.
8.  **Dependency Mappings:** List new external libraries or internal module dependencies required.
9.  **Test Strategies:** Specific guidance on _how_ to verify each phase (e.g., "Update unit test X", "Add test for edge case Y").

## Structure

- The document **must** begin with the "Problem" and "Solution" from the approved plan.
- The document **must** include the "Acceptance Criteria" from the approved plan, with the manual ones marked `manual:`.
- The document **must** include the "Phases" from the approved plan, expanded with implementation specifics describing what each phase covers. Do not use checkboxes for status tracking — the task list handles that.
- The document **must** have dedicated headers for all Mandatory Elements listed above (Tier L only).

</instructions>
