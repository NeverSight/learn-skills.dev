---
name: oneplan
description: Run one planning turn — review the previous build, plan the next build and its atomic patches, and present both for author approval in one turn.
---

# Build

Builds are steps in the implementation of a change spec. Builds work well together with OneSpec skills but don't require them.

A **build** is a unit of work from the change spec's backlog. Its core is a statement of **what materially improved over the current state** — user-inspectable change in product, or (rarely) an internal outcome expressed as a significant change in codebase metrics (all warnings eliminated, a module removed, …). Build should include a one-sentence title that summarizes the build statement.

Builds have names: <TAG><Build-number> where TAG is 2 (or more if necessary) letters matching the name of the change spec.

## Change spec record

A change spec is arranged in this order, and a new section goes where it belongs, not at the end:

1. Goal and design — what the change is and how it works.
2. Facts — what was verified, with dates.
3. `Builds` — one record per build, in order: executed builds, then the one planned build.
4. `Backlog` — always last.

An implementation line (for example, `--- Implemented / Next ---`) splits current state from planned deltas:

1. Text above the line is historical and may be inconsistent with later changes. This doesn't need fixing: the later version, and ultimately, code, wins.
2. Below the line, milestones are delta-only; they do not restate full behavior.

When reviewing a change spec:

1. Keep one canonical statement per behavior/default; later sections should reference it.
2. If duplicated rules disagree, flag drift; for current-state checks, code wins.

### Builds and numbers

The spec grows one build at a time. A build is numbered `<TAG><n>` when it is planned, never earlier, so only executed builds and the one planned build carry numbers. The backlog is a flat, unordered list of one-line items. Backlog items carry no build numbers. They have no acceptance checks, patches or ordering; anything beyond a one-line item is planned only when it becomes the next build. Outside a planning turn, add open questions and backlog items, never draft future builds.

Each build record begins with a `Status:` line:

- `Status: planned, awaiting author checkpoint`
- `Status: planned, approved <date>` — the author approved the plan at the checkpoint, by saying so or by invoking `onebuild` on it; the first patch lands it
- `Status: executed, pending author verification` — every patch is committed, but acceptance has a clause only the author can discharge
- `Status: implemented <date> (commits <TAG><n>.*)`

A patch is one coherent, verified change; inside a build it lands as exactly one commit named `<TAG><n>.<k>`, the same string as its commit subject. Patch numbers restart at 1 for each build.

A finished change spec is a record of what was built, not a plan: plan from this layout, never from a finished spec. Retiring a change spec keeps its `Status:` lines.


# Build Cycle

One cycle turn covers Steps 1–3 below and ends at the author checkpoint. Execution (`onebuild`) runs between checkpoints, possibly by a different agent, so both the build record and the approved plan must be self-contained in the change spec.

## Step 1: Review the previous build

Skip if this is the first build of the change spec. The previous build may have been executed by a different agent — review from the record (the change spec and commits tagged `<tag><build>.*`), not from conversation memory.

- Check the commits against the build's planned patches by comparing each commit subject to the patch name literally; note drift.
- Check that the previous build record has a valid `Status:` line and set it from what the record shows. Any of the four statuses the record layout lists is valid, including `planned, approved`. Flag a fully specified build record without a valid `Status:` line as a defect.
- Check the previous build's "Author action required at completion" items. An outstanding one blocks the next build: present it instead of planning past it.
- Run the build's acceptance check. Acceptance inherits the live/external rule: green suite alone does not pass a live claim — observe the real effect; missing or denied proof is a block, not a pass. Fix issues and re-verify until it passes, keeping all fixes **uncommitted**.
- For patches that claimed a live/external effect, confirm the record shows that effect was observed (not only a green suite or synthetic stand-in). A blocked live step that was marked done or skipped is drift.
- Reflect: if the build seriously drifted from its plan, propose a process change.

## Step 2: Plan the next build

- State the title and material improvement.
- Verify every assumption the plan makes about anything outside the repo before
  the checkpoint, and record what proved it. The test: if learning the true
  answer would change the plan, check it now. Unchecked, it surfaces
  mid-execution, when the plan is already committed.
- Declare an **acceptance check**: how the improvement is verified. It asserts
  exactly what the build changes — no stricter. If the improvement is a live or
  external effect, the check must observe that effect (not only a suite or
  synthetic stand-in). Do not extend the build's scope without explicit
  approval.
- Script every clause a script can reproduce, and put it where something
  already runs it — a gate or tier the harness composes, not a bespoke check
  beside it. The per-build delta carries only what no tier reaches; an empty
  delta is a good result, a duplicated one is not.
- Name the clauses a script cannot reproduce — live and external effects — in
  the harness itself, so the executor records them rather than discovers them.
  A script never substitutes for observing a live effect; Step 1's rule is not
  relaxed by this one.
- Place each check of an external contract on the patch that introduces it;
  final acceptance re-checks it, it does not discover it.
- Edit the acceptance harness during this turn. The per-build delta is part of
  the plan the checkpoint presents, not something execution improvises.
- For each acceptance clause, ask who can execute it. A clause only the author can discharge (a write to a personal account, a production change, a physical observation, a paid call, a credential the agent does not hold) goes in an "Author action required at completion" section of the build, beside the patches rather than inside the acceptance prose. Name each action, who does it, and the clause it discharges. Shape it for a human: one reviewable file beats many interactive prompts.
- Assign the next sequential build number under the change spec's tag, e.g. `LC1`, at planning time only; backlog items carry no numbers. The number stays with the build.

## Step 3: Plan the patches

Break the build into ordered atomic patches named `<TAG><n>.1…`, the same string their commit subjects carry. Re-plan until every patch is atomic and verifiable:

- A patch is coherent: it changes one invariant and does not combine multiple
  change streams. Exception: it may bundle several changes of the same nature
  when each is too small to call out independently.
- One-off mutations of live state (such as statement run by hand against
  production, a DNS or provider change made outside code) — are declared when
  planned, kept separate from the code change motivating them, and approved at
  the checkpoint rather than mid-execution. 
    - Migrations and maintenance routines are exempt: they are code the author
  reviews in the patch, replayed identically in every environment and exercised
  by the gate. 
- Patch numbers restart at 1 for each build. Within a build, an executed patch
  freezes its number; unexecuted patches may be renumbered until the checkpoint
  approves the plan.


## Step 4: Author checkpoint

Make proposed changes to the change spec: append the new build record after the existing ones, with `Status: planned, awaiting author checkpoint`; the backlog stays last. When the author approves the plan, set `Status: planned, approved <date>`.

Present in one message: 
- the previous-build review (acceptance result, any uncommitted fix diff with its verification and a proposed commit message, reflection)
- the summary of the next-build plan (improvement, acceptance check, patch list). The plan will be either committed manually, or by `onebuild`.

- Let author request commit of the fixes. If requested, tag commit with the build tag (e.g. `LC1: <description>`).
- Let author explicitly invoke execution with the `onebuild` skill.

## Closing the change spec

When no backlog items remain, skip Steps 2–3: the checkpoint presents the final build's review together with a proposal to fold the change spec into its parent spec and retire it by handing off to `onewrap`, which folds only after the author confirms.

When abandoning a branch of development, take inventory of the spec changes and developments that die with it.
