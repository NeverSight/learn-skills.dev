---
name: writing-plans
description: Write self-contained implementation plan files that a fresh, possibly weaker executor can run without the author's context — splitting work into PR-sized plans, with verification gates, STOP conditions, and a memo protocol for design forks. Use when asked to write/create a plan, turn a decided design or ticket into plans, or when another skill hands off plan-writing. Not for deciding what to build or executing plans.
---

# Writing Plans

You are writing plans for an executor that has not seen this conversation, this codebase exploration, or any sibling plan — and may be a smaller, cheaper model. Write for that executor even when you expect to execute the plan yourself: context dies at the session boundary, and an over-specified plan costs a little reading while an under-specified one fails the whole execution.

Plans are **intent-based: outcomes over prescriptions**. Specify what must be true, name exact files and symbols, point at exemplars to imitate, and gate every step with a verification command. Leave the executor room to play jazz on the implementation itself.

This skill starts when the *what* is decided, at least roughly — a request, a ticket, a settled design discussion, or another skill's handoff. It does not own ideation, auditing, or design debate. If a decision needed for planning is genuinely missing, first try to resolve it from the codebase; only what remains becomes questions to the user — asked one at a time, each with your recommended answer.

While planning, write only under the plans destination. Don't edit source, even trivially — a plan's current-state excerpts must describe the tree as it exists.

## Where plans go

Resolve the destination in this order; take the first that applies:

1. The project's demonstrated convention — an existing directory with plans in it, or a location named in `CLAUDE.md`/`AGENTS.md` or similar agent docs.
2. `$AGENTS_PLANS_DIR`, if set.
3. `./docs/plans/`, if `./docs/` exists.
4. `./plans/` (create it).
5. Not obviously in a project? Ask.

## Recon

Before writing anything, learn what every plan must carry:

- **Exact build / test / lint / typecheck commands** — verified from the repo's config (justfile, package.json, noxfile, CI), not guessed. These become each plan's verification gates.
- **Conventions and exemplars** — error handling, naming, test structure, with one concrete exemplar file per pattern the plan will tell the executor to match.
- **The VCS in use and the current revision.** Every plan carries concrete commands for the repo's actual VCS — a planned-at revision stamp and a drift check (diff the in-scope paths from that revision).

If the repo has no working verification command, say so — establishing one may need to be the first plan.

## Decomposition

**One plan = one independently-landable, reviewable change** — roughly one PR, codebase green after it lands. If the decided work can't honestly fit that unit, split it into multiple numbered plans and surface the dependency ordering (preparatory "make the change easy" plans before the change itself).

You decide how the work cleaves into landable units; you do not decide which work to do.

## Layout

Scale the structure to the work:

- **Single plan**: one file, `<destination>/<slug>.md`. No index, no numbering.
- **Multi-plan effort**: its own subdirectory — `<destination>/<effort-slug>/NNN-<step-slug>.md` plus an effort-local `README.md` index. Numbering is local to the effort, monotonic, and never reused or renumbered; execution order lives in the index and may diverge from numeric order.
- Memos (see below) sit alongside the plans as `memo-<slug>.md`.

## Writing

Read [references/plan-template.md](references/plan-template.md) before writing the first plan. For a multi-plan effort, write the index last using [references/index-template.md](references/index-template.md).

Code in plans: **sketches over implementations**. Pseudocode, signatures, type shapes, and idea sketches communicate intent without pretending to be the final code. Full prose-written implementations look plausible but are never compiled, rot before the work is done, and get copied verbatim even when wrong — write code out in full only when something genuinely must be done one specific way, or the executor plausibly won't get there from intent alone, and anchor it with an exemplar `file:line` pointer where one exists.

## Memos: design forks during execution

Less-prescriptive plans occasionally hit forks the plan didn't anticipate. The protocol has two halves:

- **The executor's half is embedded in every plan you write** (the template's STOP conditions): at a design fork, stop and write a *handback* — current state, desired outcome, lingering questions. Descriptive, not prescriptive.
- **Your half**: when a handback comes in (often pasted into your session), research the question against the codebase, write `memo-<slug>.md` next to the plans using [references/memo-template.md](references/memo-template.md) — verdict first, evidence with `file:line`, rejected alternatives — then spawn or amend the affected plans and log the round-trip in the index.

## Re-entry

Before writing, read the destination. If plans for this effort already exist, reconcile rather than duplicate: amend plans in place when the change is additive, mark superseded ones in the index, give new work the next number, and append a terse reconciliation-log entry.
