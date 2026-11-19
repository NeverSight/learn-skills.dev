---
name: development-loop
description: "Use to build one feature's tasks, from an approved task list to landed, verified, reviewed code. The goal is to own the loop [implement -> verify -> review] per unit — usually one task, or a batch of small same-shape tasks: dispatch a fresh implementer subagent (which writes tests first and proves them green), then a fresh reviewer subagent, cap the cycles, and run a final whole-branch review. You are not allowed to let a unit skip verify or review, to waive a Critical/Important finding, or to exceed the cycle cap without asking the human. Trigger phrases: build the feature, run the loop, implement the tasks, start development, work through tasks.md, dev loop, batch small tasks."
argument-hint: "Point at the feature, e.g. specs/001-auth/ (its tasks.md)"
---

# Development Loop

`planning` cuts a feature into tasks; `test-strategy` settles how they are tested. This skill takes those tasks and drives them to landed code — one **unit** at a time, each built test-first, verified green, and reviewed by a fresh session. It is the loop that sits between Plan and Deploy in the spine.

**Self-contained.** Use it to build any feature with an approved task list, whether or not `fight` is driving; `fight` simply calls it when it's active. It is the loop's single source of truth: the cycle cap, the transitions, and the dispatch rules live here, not in `fight` and not in the steps below.

**The loop runs per unit, not per feature.** One cycle = one unit taken through `implement -> verify -> review`. A **unit** is what one dispatch covers: a single task, or a batch of small same-shape tasks (see _Batching_). A feature with eight tasks runs the loop up to eight times, fewer when tasks batch.

## The Model

| Thing      | What it is                                                            | Where it lives                              |
| ---------- | --------------------------------------------------------------------- | ------------------------------------------- |
| **Step**   | One of the loop's three stages: `implement`, `verify`, `review`.      | this skill, below                           |
| **Task**   | One reviewable change (~300 lines).                                   | `specs/NNN-slug/tasks.md`                   |
| **Batch**  | Several small same-shape tasks dispatched as one unit.                | `specs/NNN-slug/tasks.md`                   |
| **Unit**   | What one dispatch covers: a single task, or a batch. The loop's unit. | `specs/NNN-slug/status.md` (`current_unit`) |
| **Cycle**  | One unit's round through `implement -> verify -> review`.             | `specs/NNN-slug/status.md` (`cycle`)        |
| **Brief**  | The unit's requirements, extracted to a file for the implementer.     | see `references/brief-and-report.md`        |
| **Report** | The implementer's full account, written to a file.                    | see `references/brief-and-report.md`        |
| **Branch** | One feature = one branch = one PR.                                    | `feat/NNN-slug`                             |

One unit = **one** implementer dispatch and **one** reviewer dispatch. For a single task that is one task; for a batch it is the whole batch, reviewed as one diff.

### The three steps

The step names are the shared vocabulary across the pack. Other skills say "back to `implement`" or "`review` judges the diff" — they mean these:

| Step          | What it does                                                         | Reference                        |
| ------------- | -------------------------------------------------------------------- | -------------------------------- |
| **implement** | Builds one task test-first and proves it green (RED-GREEN-REFACTOR). | `references/implement.md`        |
| **verify**    | Proves the work runs green with fresh evidence, before any claim.    | `references/implement.md` (part) |
| **review**    | Judges the diff against intent, in a fresh session.                  | `references/review.md`           |

**`verify` is not a separate subagent.** The **implementer** writes the test first, watches it fail, makes it pass, and runs the full suite — its report carries the fresh evidence (see `references/implementer-prompt.md`). There is no "trust me" step: the controller reads that evidence and re-runs anything it doubts. This keeps the loop to **two subagents per unit** — one implementer, one reviewer — while still holding the fresh-evidence bar.

## When to Use

- An approved task list exists (`specs/NNN-slug/tasks.md`), the design is agreed, and there is at least one unbuilt task.
- You are about to build a feature's tasks and want the loop run honestly.

**Do NOT use** to decide what to build (`brainstorming`), slice features into phases (`roadmap`), design the system (`system-design`), cut a feature into tasks (`planning`), settle the test strategy (`test-strategy`), or land the branch (`finishing-a-development-branch` — the loop exits into it). Do not use it for a single task with no feature context; that is still the loop, but say so and run one cycle.

## Core Rules

The loop's rules live here — one source of truth for the gate.

- **Cycle cap: 3, per unit.** One cycle = that unit (a task, or a batch) through `implement -> verify -> review`. On the third cycle without a clean exit, **STOP and ask the human** (`AGENTS.md`). The cap is per unit, so a stuck unit does not starve the rest of the feature.
- **Each cycle changes the approach, it doesn't repeat it.** Re-running the same fix with a tweak burns the cap without progress. Before starting cycle _n_, name what was wrong with cycle _n−1_ and what is different this time — a new hypothesis, a different layer, a fresh diagnosis. No new hypothesis means STOP and ask.
- **No unit skips a step.** Every unit goes through all three: built test-first, proven green, reviewed in a fresh session. "It's trivial" is not an exemption — a run of trivial tasks is a batch, which is dispatched once and reviewed once (see _Batching_).
- **The reviewer is a fresh session**, never the one that wrote the code, and **never a subagent the implementer spawned**.
- **Never pre-judge a finding.** Do not tell a reviewer to ignore an issue, treat it as Minor, or accept "the plan chose this." Let it raise the finding and adjudicate it in the loop. A prompt containing "do not flag" is pre-judging. A batch buys one review, never a weaker one.
- **Review is bounded and read-only.** Diff-scoped, one pass, stop rule, no mutation of the checkout, no suite runs on it, no recursive dispatch. An oversized or out-of-scope diff is sent back to `implement`, not reviewed.
- **A blocked unit is not a stalled feature.** If a unit trips the cap, park it with a written ruling, note it, and continue with the next unit rather than stopping the whole feature.
- **Artifacts are files, not pasted text.** Hand the implementer a brief file and take back a report file. Never paste the session's history into a dispatch.
- **No branch without approval to land.** The loop ends at a clean, reviewed, verified branch; `finishing-a-development-branch` raises the MR/PR, and merging needs explicit human approval.

## Batching

Some task lists contain runs of small, same-shape work: the same one-line fix, constant rename, or field addition repeated across files. Those do not each need their own dispatch, cycle, and review — that is ceremony, not gate. Dispatch them as **one unit**.

**A batch is allowed only when every member is all of these:**

- **Same shape** — the same kind of mechanical edit, repeated. A mixed batch is not a batch.
- **Independent** — no `depends_on` between members, and no two members touching the same file.
- **Behavior-free** — no member adds or changes behavior, so no member needs its own RED. The existing suite proves the batch.
- **One review surface** — no member needs its own judgment call.
- **Small together** — the whole batch fits one brief and stays under ~300 lines.

To form one: put every member's file and its change in **one brief** (see `references/brief-and-report.md`), record `BASE` once, dispatch **one** implementer, and review the whole diff as one unit.

**Guards — batching is a concession, not a shortcut:**

- **One member too big, risky, or ambiguous → pull it out** and dispatch it on its own. A batch must never let a hard task hide among easy ones.
- **The whole batch goes back together.** A Critical/Important finding on any member sends the batch back to `implement`; you do not half-review it.
- **A batch is a symptom of a plan cut too fine.** Note it in `status.md` notes so `planning` can tighten `task-sizing` next time. Batching absorbs an over-split plan; it does not excuse one.
- **The cap is per unit.** Batching a run of six tasks buys three cycles for the batch, not eighteen. That is the point: the cap exists to stop thrashing on _one_ piece of work.

This does not replace `dispatching-parallel-agents`: a batch is **one** agent on **one** branch taking several files; parallel dispatch is **several** agents on **several** branches. They compose — a parallel agent can itself receive a batch.

## Procedure

### 1. Load the feature and its tasks

Read `specs/_state.md` (current phase/feature) and the feature's `specs/NNN-slug/status.md` (`status`, `current_unit`, `cycle`, `cycle_cap`, `next`, `notes`). Read `specs/NNN-slug/tasks.md` — the task list, each task's `Verify:` line, and the feature's `## Test strategy` section. Read the newest spec revision and the parts of `docs/architecture/architecture.md` the tasks touch.

If a task has no outcome or nothing to verify against, it is not sized: send it back to `planning` before building anything.

Then group the pending tasks into units: keep every task that needs its own judgment, tests, or review surface as a unit of one, and batch the runs of small same-shape work (see _Batching_).

### 2. Set up the branch

Work on `feat/NNN-slug`. Start from a clean tree and a green baseline; if the baseline is red for a reason you did not cause, name it before you begin.

### 3. Run the loop, one unit at a time

For each unit, in `depends_on` order (a batch is ready only when every member is):

1. **Record `BASE`** — `git rev-parse HEAD` — **before** dispatching. The review diff and any fix round need it. Never use `HEAD~1`: it silently drops all but the last commit of a multi-commit unit.
2. **Build the brief and dispatch the implementer.** Extract the unit's requirements to a brief file (see `references/brief-and-report.md`) and dispatch **one** fresh implementer subagent with `references/implementer-prompt.md`. Give it the brief, the interfaces earlier units created, the global constraints, and the report-file path. Never the session's history, never the whole plan.
3. **Read the report.** The implementer returns a short status (`DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`) and a report file. On `BLOCKED` or `NEEDS_CONTEXT`, answer the question and re-dispatch rather than guessing. Treat the report as claims: check the diff and re-run anything you doubt.
4. **Verify the evidence.** Confirm the report's test evidence is fresh and complete (RED seen for the right reason, GREEN, full suite, pristine output). This is the `verify` step — it is held by the implementer's evidence and your reading of it, not a separate dispatch. Red, or evidence missing → back to `implement` (cycle).
5. **Review the unit.** Generate the diff for `BASE..HEAD` and dispatch **one** fresh reviewer subagent with `references/reviewer-prompt.md` and `references/review.md`. For a batch, the reviewer sees every member's files — the review is looser on nothing, only fewer in number. Never the author's session.
6. **Route the outcome.** Findings in the code → `implement`. Findings in the task list → `planning`. Findings in the design → `system-design`. Findings in the requirement → `system-design` (revise the spec), or `brainstorming` if the PRD is wrong.
7. **Close the unit.** Clean verify and a clean review (or only Minor findings) → the unit is done. Tick **each member's** checkbox in `tasks.md`, record it in `specs/NNN-slug/status.md` (`next`, `notes`), and move to the next unit. The **branch** is not landed here — it lands once per feature, after the final review (step 5).

### 4. Track the cycle

Increment `cycle` in `specs/NNN-slug/status.md` **only when a unit is sent back** (a red verify or a Critical/Important review finding). Set `next` to the return target and add a one-line note. When `cycle` reaches `cycle_cap`:

- Park the open findings with a one-line ruling each (what you decided, why, what it costs if wrong).
- Set the feature's `status` to `blocked` only if the whole feature is stuck; otherwise note the parked unit and move on.
- Tell the human, and stop asking the loop to converge — past the cap, rounds do not converge; the failure is structural.

### 5. Run the final review

After **every** unit is done, run the whole-branch review (`references/final-review.md`). Per-unit reviews judge each diff in isolation; the final review judges the branch as a whole — the seams between units, the feature against its spec, and anything that only shows up once the units sit together. Fix what it finds in a single wave, then hand to `finishing-a-development-branch`.

### 6. Exit the loop

The loop is done when every unit is done or parked-with-ruling and the final review is clean. Then `finishing-a-development-branch` lands the branch: it raises the MR/PR for the human — merging needs explicit human approval — appends the ledger row, and cleans up the worktree. Then `deploy`, at the milestone.

One feature = one branch = one PR, so there is exactly **one** landing per feature, after the final review — not one per unit.

Update the feature's `specs/NNN-slug/status.md` (`next`, `notes`) as you go, and the project ledger `specs/_status.md` on each landing.

## Red Flags

| Thought                                              | Reality                                                                                |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------- |
| "This unit is trivial, skip verify and review"       | Every unit goes through all three steps. Trivial is where the shortcut ships.          |
| "Tests pass, so the unit is done"                    | Verify is evidence; review is intent. Both, or it's not done.                          |
| "I'll paste the whole plan into the dispatch"        | Send the brief file. A fresh subagent needs its unit, not your history.                |
| "The implementer said it worked"                     | Agent reports are claims. Check the diff; re-run what you doubt.                       |
| "Cycle 4 is fine, we're close"                       | The cap is 3 per unit. Park with a ruling and ask the human.                           |
| "Same fix, one more try"                             | Each cycle changes the approach. No new hypothesis means STOP.                         |
| "I'll just tell the reviewer to ignore that one"     | Never pre-judge a finding. Let it surface, then adjudicate.                            |
| "Per-unit reviews caught everything, skip the final" | Unit reviews are diff-scoped. The final review judges the branch as a whole.           |
| "The implementer spawned its own reviewer"           | A duplicate seat at full cost. Flag it; the controller owns review.                    |
| "One unit is stuck, the feature is doomed"           | Park it with a ruling and move to the next unit. The cap is per unit.                  |
| "I'll fix it myself, dispatching is overhead"        | Controller fixes skip review and pollute your context. Resume the implementer.         |
| "These 6 tiny tasks need 6 dispatches to be safe"    | Same-shape, independent, behavior-free → one batch, one review. That is the safe path. |
| "I'll batch these 4 — the reviewer can be lenient"   | A batch buys one review, not a weaker one. It sees every member's files.               |
| "I'll tuck this big task in with the tiny ones"      | Pull it out. A batch must not let a hard task hide among easy ones.                    |

## Completion Check

The loop is trustworthy when ALL are true:

- [ ] Every unit went through all three steps — built test-first, verified with fresh evidence, reviewed in a fresh session.
- [ ] The cycle cap (3, per unit) was honored; any unit past it is parked with a written ruling and the human was told.
- [ ] Each unit was handed over as a brief file and came back as a report file; no session history was pasted into a dispatch.
- [ ] Any batch met every guard (same shape, independent, behavior-free, one review surface, small together); no big or ambiguous member was hidden in one.
- [ ] The final whole-branch review ran after the last unit, and its findings were fixed or parked-with-ruling.
- [ ] `specs/NNN-slug/status.md` reflects the current unit, cycle, and next pointer; the ledger row was appended on landing.
- [ ] The loop exited into `finishing-a-development-branch` once, for the whole feature; nothing merged or deployed without explicit human approval.
