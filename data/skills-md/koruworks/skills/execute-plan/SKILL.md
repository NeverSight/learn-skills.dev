---
name: execute-plan
description: Execute a signed-off PLAN.final.md for a single feature yourself, phase by phase, on the current branch — you are the engineer, not a delivery lead. Use when the user invokes /execute-plan, or asks to implement, build or continue an approved plan that is small enough for one person, e.g. "/execute-plan spell-check", "/execute-plan spell-check p1-p3", "build the rest of the plan while I sleep". Resolves the requested phases against the final doc, builds each as its own verified increment, runs its verification before the next begins, and commits each landed phase without waiting for approval. Questions that need the user are recorded with a recommendation instead of blocking. For a roadmap large enough to want parallel sub-agents, use execute-roadmap instead.
---

# Execute an approved plan

You are the engineer building an already-approved plan for the user.
Planning is done: `PLAN.final.md` is signed off, and your job is to get it
built. Unlike [execute-roadmap](../execute-roadmap/SKILL.md), the plan is
small enough that **you write the code yourself** — there is no fan-out to
review, so the quality of every line is yours directly.

You are judged on whether the result matches the approved plan, follows the
project's principles, and arrives as a clean, granular commit history — one
commit per verified phase, each of which builds and runs on its own.

The user may be away for the whole run (often asleep). **Keep going until the
requested scope is complete** — do not stop for approval between phases, and
do not stall on a question you can safely defer (see "Deviations and
questions").

## Which skill this is

- **This skill** — one signed-off `PLAN.final.md`, phases that mostly build
  on each other, all of it landing on the current branch. You code it.
- **[execute-roadmap](../execute-roadmap/SKILL.md)** — a roadmap of
  milestones and plans with real parallelism, one sub-agent per plan. You
  brief and review; you do not code.
- **[build-feature](../build-feature/SKILL.md)** — planning is *not* done. Go
  there first; come back here once the user signs off the final doc.

If you start here and find the plan actually wants three agents working in
parallel, say so and switch to execute-roadmap rather than improvising a
fan-out.

## Inputs

The argument names the feature, optionally the phases, and optionally a
model or effort directive, e.g.:

- `/execute-plan spell-check`
- `/execute-plan spell-check p1-p3`
- `/execute-plan finish the plan, high effort`

1. **Locate the approved doc.** Find `docs/<feature>/` (the project's
   planning folder, unless it uses another — from the argument, the branch
   name, or the most recently committed final doc) and read `PLAN.final.md`
   in full — including the product decisions, the standing requirements and
   the verification tests, not only the phase list. **Only a `.final.md` doc
   is executable.** If only revs exist, stop and tell the user the review is
   not finished — do not execute a rev.
2. **Resolve the scope.** Match the argument's ids against the plan's phase
   headings, case-insensitively and forgivingly: `p1` or `1` is Phase 1,
   ranges like `p2-p5` expand, and no scope (or "finish the plan") means
   everything not yet done. Cross off work already committed — check
   `git log` and the code against the plan before redoing anything; a phase
   is done when the code does what its verification step says, not when a
   document says so. **Echo the resolved phase list back before starting.**
   If an id resolves to nothing, stop and ask — this is the one question that
   cannot wait, and it comes before the user leaves.
3. **Read the project's stated principles and agent orientation** (a
   `PRINCIPLES.md`, `AGENTS.md`, `CONTRIBUTING.md` or similar), if it has
   them, plus the area docs for the code this plan touches. Ground every
   implementation choice in them.
4. **Check against the main integration branch.** `git fetch`, then
   `git log --oneline <branch>..<main>`, where `<main>` is the main
   integration branch (e.g. `main` or `dev`). If the branch is behind, say so
   before starting (see [merge-branch](../merge-branch/SKILL.md) — a merge is
   a review gate, not a mechanical step). If the user is unavailable, proceed
   on the branch as it is and record the fact in the questions log rather
   than merging unreviewed.

## Models and effort

Honor any model or effort directive the user gives, if your agent tool
supports it. You are doing the work in this session, so a model directive
applies to any sub-agent you spawn and an effort directive applies to you: it
says how much you verify and iterate before calling a phase done. With no
directive, use the defaults and say so in your kickoff summary.

**Spawn a sub-agent only for work that is genuinely independent and
self-contained** — a fixture set, a one-off migration script, a mechanical
sweep across many files. Brief it completely (the phase text, the principles
pointer, and the checkout root with the instruction that every path it
touches lives under that root), and review its diff as strictly as you would
review your own. Never hand it a phase whose design decisions are still open.

## Building each phase

Take the phases in the plan's order, one at a time. Each is its own
reviewable increment that builds, runs, and demonstrates something before the
next begins.

1. **Re-read the phase and its verification step**, and name out loud what
   "done" means for it before writing code.
2. **Build the smallest honest version of what the phase says** — no more, no
   less. A phase is not a licence to also fix the things you noticed next to
   it; note those instead.
3. **Improve what you touch.** When an increment lands in a large file, look
   for the natural break: extract the reusable mechanism, keep domain
   behaviour with its domain. Do not create generic buckets.
4. **Watch for what the plan cannot see.** Unnecessary complexity, a second
   mechanism parallel to one that exists, duplicated state, blocking work on
   the thread that answers the user, unlocalized strings — these are the
   findings you would raise if you were reviewing someone else. Raise them on
   yourself before committing.

## Verifying and committing

Each phase passes its own gate before it lands.

1. **Run the phase's named verification** plus the plan's standing checks and
   the repo's own (its formatter, linter and test suite), and whatever else
   the plan's contract specifies. A phase whose verification fails does not
   get committed — fix it or defer it, and never report it as landed.
2. **Say what you actually ran.** If a check could not run in this
   environment (a GUI path, a platform-specific build, an asset that is not
   installed), say so plainly and record it — an unrun check is not a passed
   check.
3. **Commit the verified phase** following
   [commit-changes](../commit-changes/SKILL.md) — but do not wait for
   approval of the summary; the user pre-approved committing when they
   invoked this skill. One commit per verified phase, explaining what changed
   and why the decisions were taken. Never push unless asked.

Then move to the next phase.

## Deviations and questions

**Product decisions and large-blast-radius choices are still not yours** —
the same rule as in planning. A change to what the customer sees, the data or
domain model, a new dependency, an architectural turn: not yours to settle
inside a phase. But the user is unavailable, so instead of blocking:

- **Record every question in the questions log as it arises** — wherever the
  project keeps open questions; if it has no convention, a questions section
  or file beside the plan in `docs/<feature>/`. Each entry has the context,
  the options, your recommendation, and what you did in the meantime. One
  decision per question. Then keep going.
- **Prefer the reversible option.** If one path can be safely revisited later
  and the other cannot, take the reversible one and record it. If a phase
  truly cannot proceed without an answer — every path is expensive to reverse
  — defer that phase, record why, and continue with the phases that do not
  depend on it.
- **A persisted schema or format change is never taken unilaterally.** If a
  phase turns out to need a schema/format version bump or a new migration and
  the approved plan does not already say so, defer that phase and record it
  in those words — "this changes the database schema". A migration stamps
  every store it touches and is rarely rolled back, so it is never the
  reversible option.
- If `PLAN.final.md` turns out to be wrong mid-execution, do not quietly build
  around it: record the discrepancy, make the smallest honest correction the
  work requires, and flag the plan section for revision. A plan that no
  longer matches the code is worse than no plan.

## Finishing

When the requested scope is done (or everything not blocked is done):

- Write `docs/<feature>/EXECUTION.md`: which phases landed (with commit
  hashes), which were deferred and why, what was verified and what could not
  be, and the open questions.
- **Write `docs/<feature>/ACCEPTANCE.md`** following
  [write-acceptance](../write-acceptance/SKILL.md) — the ordered checklist a
  person works through by hand to see the work running and accept it: what
  to run and open, what to install, what needs a second device or their own
  eyes, and the exact observable that closes each check. Only what a machine
  could not do; never ask them to re-run what you already ran.
- **If any phase is still owed** — deferred, blocked, or stopped short — also
  write `docs/<feature>/HANDOFF.md` following
  [write-handoff](../write-handoff/SKILL.md), so the next session picks up
  where you stopped instead of re-deriving it. Skip it when the scope is
  complete.
- **Name any persisted schema or format change in the hand-back**: what moved,
  and that the user's first run of it should be against disposable data.
- Leave the tree clean — no stray branches, checkouts or scratch files.
- **Report to the user in simple terms**: what was built, in product language
  rather than phase ids; the pointer to ACCEPTANCE.md for what they now do;
  and the questions awaiting their decision. This summary is for a person who
  just woke up — plain sentences, no shorthand from the run.

When the plan is fully built and the user has worked through ACCEPTANCE.md,
[close-plan](../close-plan/SKILL.md) retires `docs/<feature>/` into the
documentation that outlives it.
