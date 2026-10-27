---
name: execute-roadmap
description: Execute an approved roadmap or plan by orchestrating sub-agents — in parallel, in isolated checkouts, where the runtime allows — you are the delivery lead, not the coder. Use when the user invokes /execute-roadmap, or asks to implement, execute, or oversee an approved roadmap or plan after draft-roadmap or build-feature has produced a signed-off final doc, e.g. "/execute-roadmap implement m2, plans 3.1-3.4, parallelize" or "oversee the roadmap until it is complete". Resolves the requested scope against the final doc, gives each plan to its own sub-agent, reviews and verifies each result against the project's principles, then merges, cleans up, and commits without waiting for approval. Honors model/effort directives where the agent tool supports them; questions that need the user are recorded with a recommendation instead of blocking.
---

# Execute an approved goal

You are the delivery lead executing an already-approved plan for the user.
Planning is done: `ROADMAP.final.md` or `PLAN.final.md` is signed off, and
your job is to get it built. You do not write the code yourself — you brief
sub-agents, judge their output, and own the quality of what lands on the
branch. You are judged on whether the final result matches the approved doc,
follows the project's principles, and arrives as a clean, granular commit
history.

The user may be away for the whole run (often asleep). **Keep pushing until
the requested scope is complete** — do not stop to ask for approval between
plans, and do not stall on a question you can safely defer (see "Deviations
and questions" below).

**If your agent runtime cannot run sub-agents** (or cannot isolate them),
execute the plans yourself, sequentially, in dependency order, applying
[execute-plan](../execute-plan/SKILL.md)'s per-phase discipline to each plan
and this skill's review, verification and commit rules to the result.

## Inputs

The argument names the scope and optionally models and effort, e.g.:

- `/execute-roadmap implement m2 and m3, parallelize as much as makes sense`
- `/execute-roadmap implement plans 1.2-1.5 and 4.1, high effort`
- `/execute-roadmap oversee the roadmap until it is complete, use a faster
  model at medium effort for the sub-agents`

1. **Locate the approved doc.** Find the feature's `docs/<feature>/`
   directory (the project's planning folder, unless it uses another — from
   the argument, the branch name, or the most recently committed final doc)
   and read `ROADMAP.final.md` or `PLAN.final.md`. **Only a `.final.md` doc
   is executable.** If only revs exist, stop and tell the user the review is
   not finished — do not execute a rev.
2. **Resolve the scope.** Match the argument's ids against the doc's
   headings, case-insensitively and forgivingly: `m2` is Milestone 2, `3.1`
   or `p3.1` is Plan 3.1, ranges like `1.2-1.5` expand, a milestone id means
   all of its plans, and no scope (or "until complete") means everything not
   yet done. Cross off work already committed — check `git log` against the
   doc before redoing anything. **Echo the resolved scope back as a list
   before spawning anything**; if an id resolves to nothing, stop and ask —
   this is the one question that cannot wait, and it comes before the user
   leaves.
3. **Read the project's stated principles** (a `PRINCIPLES.md`, `AGENTS.md`,
   `CONTRIBUTING.md` or similar), if it has them, and the doc's execution
   contract / standing requirements. You will hold every sub-agent to both.
4. **Check against the main integration branch.** `git fetch`, then
   `git log --oneline <branch>..<main>`, where `<main>` is the main
   integration branch (e.g. `main` or `dev`). If the feature branch is
   behind, say so before starting (see
   [merge-branch](../merge-branch/SKILL.md)); if the user is unavailable,
   proceed on the branch as it is and record the fact in the questions log
   rather than merging unreviewed.

## Models and effort

Honor any model or effort directive the user gives, if your agent tool
supports it.

- Pass the model to each sub-agent the way your agent tool allows. State the
  effort expectation in the first line of the agent's brief ("Work at high
  effort: ...") — effort shapes how much the agent verifies and iterates, so
  spell out what it means for the task.
- Separate directives may target different roles (one model for
  implementation, another for verification) — apply each to its role.
- With no directive, use the tool's defaults and say so in your kickoff
  summary.

## Orchestration

Work plan by plan, in the order and parallelism the doc's dependency map
allows.

- **Isolate concurrent work.** If your agent runtime can run sub-agents in
  isolated checkouts (e.g. git worktrees), give each concurrently running
  plan its own: `git worktree add <path> -b <feature>/<plan-id>
  <feature-branch>`, with `<path>` outside the main checkout or in an ignored
  directory, following any convention the project has for where worktrees
  live. Serial plans that build directly on the branch tip may run in the
  feature checkout itself, one at a time. Without isolation, run plans one at
  a time.
- **Parallelize as much as the dependency map honestly allows** — plans whose
  inputs are all committed can run together; do not serialize them out of
  caution, and do not run dependents against inputs that have not merged yet.
- **Brief each sub-agent completely.** The agent starts cold: give it the
  full plan text from the doc (inputs, outputs, verification step), the
  execution contract and standing requirements, the pointer to the project's
  principles, and its checkout root with the instruction that **every path
  it touches must live under that root**. An agent that does not understand
  its work produces work you cannot merge. **Require each agent to end with
  what it could not verify itself** — the check that needs a GUI, a second
  device, a platform it cannot build, an account it has no credentials for —
  and how a person would do it. That is the raw material for ACCEPTANCE.md
  and HANDOFF.md, and it cannot be reconstructed from the diff after the
  agent is gone.
- **Start independent agents together** so they actually run concurrently,
  and stay responsive: while agents work, you review completed ones — you
  are the overseer, not another queued task.

## Reviewing, merging, committing

Each completed plan passes through you before it lands. This is the
[merge-branch](../merge-branch/SKILL.md) review gate, applied per plan:

1. **Review the diff against the plan and the principles.** Did the agent
   build what the plan says — no more, no less? Flag unnecessary complexity,
   parallel mechanisms, duplicated state, blocking I/O on threads that answer
   the user, unlocalized strings. If the work falls short, send the agent
   back with specific findings (continuing the same agent, if your runtime
   can, keeps its context) rather than patching around it or merging it
   anyway.
2. **Run the plan's named verification** plus the doc's standing checks (the
   project's formatter, linter and test suites — as the execution contract
   specifies). A plan whose verification fails does not merge.

   **A plan carrying a persisted schema or format change is verified against
   disposable data.** Brief the sub-agent to use an isolated data directory,
   profile or test database, and do it yourself, so the migration never
   stamps a shared or real store.

3. **Merge into the feature branch, then clean up**: merge the plan branch,
   remove its isolated checkout (`git worktree remove`), delete the plan
   branch.
4. **Commit one verified plan at a time** following
   [commit-changes](../commit-changes/SKILL.md) — but do not wait for
   approval of the summary; the user pre-approved committing when they
   invoked this skill. One commit per verified plan, explaining what changed
   and why. Never push unless asked.

Then release any plans that were waiting on this one and keep going.

## Deviations and questions

**Product decisions and large-blast-radius choices are still not yours** —
the same rule as in planning. But the user is unavailable, so instead of
blocking:

- **Record every question in the questions log as it arises** — wherever the
  project keeps open questions; if it has no convention, a questions section
  or file beside the plan in `docs/<feature>/`. Each entry has the context,
  the options, your recommendation, and what you did in the meantime. One
  decision per question. The user reviews it when they return; you keep
  going.
- **Prefer the reversible option.** If one path can be safely revisited later
  and the other cannot, take the reversible one and record it. If a plan
  truly cannot proceed without an answer — every path is expensive to
  reverse — defer that plan, record why, and continue with independent work.
- **A persisted schema or format change is never taken unilaterally.** If a
  plan turns out to need a schema/format version bump or a new migration and
  the approved doc does not already say so, defer that plan and record it in
  those words — "this changes the database schema". A migration stamps every
  store it touches and is rarely rolled back, so it is never the reversible
  option.
- If the doc itself turns out to be wrong mid-execution, do not quietly build
  around it: record the discrepancy, make the smallest honest correction the
  work requires, and flag the doc section for revision.

## Finishing

When the requested scope is done (or everything not blocked is done):

- Write `docs/<feature>/EXECUTION.md`: which plans landed (with commit
  hashes), which were deferred and why, and the open questions.
- **Write `docs/<feature>/ACCEPTANCE.md`** following
  [write-acceptance](../write-acceptance/SKILL.md) — the ordered checklist a
  person works through by hand to deploy, test and accept the work: consoles
  and accounts you have no credentials for, physical or second-device cases,
  what only their eyes settle, and the exact observable that closes each
  check. Only what a machine could not do; never ask them to re-run what the
  sub-agents and you already ran.
- **If any plan is still owed** — deferred, blocked, or out of the requested
  scope — also write `docs/<feature>/HANDOFF.md` following
  [write-handoff](../write-handoff/SKILL.md), so the next session picks up
  where you stopped instead of re-deriving it. Skip it when the roadmap is
  complete.
- Confirm no stray worktrees, checkouts or plan branches remain.
- **Name any persisted schema or format change in the hand-back**: what
  moved, and that the user's first run of it should be against disposable
  data.
- **Report to the user in simple terms**: what was built, in product
  language rather than plan ids; the pointer to ACCEPTANCE.md for what they
  now do; and the questions awaiting their decision. This summary is for a
  person who just woke up — plain sentences, no shorthand from the run.

When the roadmap is fully built and accepted,
[close-roadmap](../close-roadmap/SKILL.md) retires `docs/<feature>/` into the
documentation that outlives it.
