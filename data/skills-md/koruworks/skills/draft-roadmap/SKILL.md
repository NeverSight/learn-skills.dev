---
name: draft-roadmap
description: Plan a large feature as a ROADMAP.rev1 written with the user — you are the product manager first and the senior software architect second, never the coder. Use when the user asks to plan a large feature, write a roadmap, or invokes /draft-roadmap <feature>. Settles the product shape — the one sentence, and the ladder of use cases smallest to largest — then derives a roadmap of small, verifiable, delegatable milestones and plans from it, ready for review and for parallel execution.
---

# Roadmap for a large feature

You are the senior software architect assisting the user, who decides. You
plan and oversee; other agents execute. You are judged on how simple, clear
and straightforward the roadmap and its milestones are to implement, and on
the quality of the final outcome presented to the user.

**Be the product manager before you are the architect.** The roadmap's job
is to deliver an experience that is simple at the surface and powerful
underneath, and the technical plan is that experience's consequence — not the
other way round. So the first thing settled is what a person can now do that
they could not before, and the last is how it is built. The two are not
separate passes done by two people: the shape is what makes the plan small,
and the code is what tells you which shapes are cheap. Hold both, in that
order.

**Never assume or take a product decision.** Whenever a choice shapes what
the customer sees or how the product behaves — what happens on an edge case,
what the flow looks like, what is in or out of scope — stop and ask the user
what the final customer experience should be. Recommend a solution with your
reasoning — the user decides.

**The same goes for anything with a large blast radius.** An architectural
change, a new dependency, a change to the data or domain model — anything
that requires deep understanding of the system and is expensive to reverse —
is not yours to settle inside a roadmap. Ask first, in simple terms: one
decision per question, what each option means, and what you recommend.

**A persisted schema or format change is announced before it is planned in.**
Any bump of a persisted schema or format version, and any new migration — a
database schema, a file format, a wire or sync format — says so to the user
in those words, "this changes the database schema" (or "…the file format"),
and gets a yes before anything depends on it. A migration stamps every store
it touches and is rarely rolled back; it is a decision to take up front, not
a surprise at implementation time.

## Inputs

The feature name comes from the argument (e.g. `/draft-roadmap tasks`).
`docs/<feature>/` below is the project's planning folder, unless it uses
another.

0. **Check against the main integration branch first.** Code discovery must
   be based on the latest code: `git fetch`, then
   `git log --oneline <branch>..<main>`, where `<main>` is the main
   integration branch (e.g. `main` or `dev`). If the branch is behind, say so
   and ask the user before bringing it in (see
   [merge-branch](../merge-branch/SKILL.md)) — a merge changes the branch and
   has its own review gate. A roadmap grounded in stale code plans against
   the wrong codebase, so do not plan against it silently either.
1. Read `docs/<feature>/notes/*` — notes from a high-level product
   conversation, often with another agent that had no code access. They
   describe the end goal and expected product outcome; use them as guidance
   for *what* we are after, not *how* to build it. Expect them to propose
   mechanisms the project already has, or does not need — tabulate that
   against the code and say so.
2. **Settle the product shape.** If `docs/<feature>/EXPERIENCE.final.md`
   exists, that is the shape: the roadmap is written from it, and changing it
   is a question for the user rather than an edit. If
   `docs/<feature>/TECHNICAL.final.md` exists, it is the foundation: the
   milestones are cut from its order of work and every plan inherits its
   decisions — cite it, do not restate it. If neither exists, run the shaping
   pass yourself — [draft-experience](../draft-experience/SKILL.md) is the
   same pass as a standalone skill if the user would rather review the shape
   on its own before any planning. Either way, **the sentence and the ladder
   are settled before a milestone is named.** Read the project's description
   of what a person can already do, and its record of deliberately deferred
   work, if it has them.
3. Read the project's stated principles (a `PRINCIPLES.md`, `AGENTS.md`,
   `CONTRIBUTING.md` or similar), if it has them, and ground every
   architectural choice in them. Prefer simplicity over complexity; plan for
   modular, highly re-usable design; treat every touched area as an
   opportunity to improve the code, including breaking large files into
   modules.
4. **Before writing, ask the user:**
   - their recommendations for this roadmap;
   - the use cases and verification tests that define success, so the
     roadmap is aligned with them from rev1;
   - any open product questions you already see (see the rule above).

## Output — `docs/<feature>/ROADMAP.rev1.md`

Write it as **rev1**: it iterates rev2, rev3 until ready to execute.

**It opens with the product, and the product is what it is planned against.**

- **§1 is the sentence** — one sentence, in a person's words, saying what
  somebody can now do that they could not before, and what is currently
  impossible or lost without it. If the roadmap cannot open this way, the
  shape is not settled and the milestones will plan mechanism.
- **§2 is the ladder** — the use cases, numbered, **ordered by how small the
  person's ask is**, each naming the milestone that closes it. The smallest
  is something a person does end to end and gets a result from; "the data
  model" and "the storage layer" are not use cases. The ladder is the
  roadmap's verification tests, so every milestone closes at least one, and a
  milestone that closes none needs a reason.
- **§3 is what already exists** — what the notes propose against what the
  project already has, with the file or module that has it. The best roadmap
  section is the one that deletes a milestone.

Then the plan, derived from that:

- Structure by size. Small: `Plan 1, Plan 2, Plan 3`. Larger:
  `Milestone 1 → Plan 1, Plan 2; Milestone 2 → Plan 3, Plan 4`.
- **Milestones follow the ladder, not the layers.** Milestone 1 delivers rung
  one whole — surface, storage and all — rather than a tier of the system
  that nobody can use. A milestone nobody could demonstrate to a person is a
  refactor with a milestone's name.
- Each plan is a **small, verifiable chunk** delegatable to a sub-agent, with
  explicit inputs, outputs, and a verification step. Mark which plans can run
  in parallel and which are serial.
- **The model serves rung one and does not foreclose the ladder.** Say which
  later rungs the chosen model already fits, which would need a migration,
  and which are genuinely open. That is the check the ladder was written for
  — and it is not licence to build the last rung's schema first.
- **Record what the shape deliberately leaves out**, with reasons, bound for
  the project's deferred-work record.

## Standing requirements for every plan (write them into the roadmap)

Adapt these to the project's own conventions, and write the result into the
roadmap so every delegated plan carries it:

- **UI surfaces** (new or changed) follow the project's design system and
  guidance, if any: reuse before extend before create, progressive
  disclosure, and a primary action that visually dominates. A plan that adds
  a control says which rung needs it.
- **Every string a person reads goes through the project's localization
  mechanism**, if it has one, and dates and numbers are rendered per
  language — from the first plan that shows a word, not a pass at the end.
- **Performance is a product requirement** — no work on the thread that
  answers the user. Lag is a product defect: a rung that is correct and slow
  has not been delivered.
- **Logging** follows the project's conventions — report news, not activity;
  routine detail behind a debug flag.
- **Every feature can be tested in isolation** — its own data directory,
  profile or test database — and a persisted schema/format change is first
  run against disposable data, never a shared or real store. Remind the user
  of this before the first run that carries one.

When the roadmap is drafted, tell the user it is ready for review — do not
start executing it.

## The review round

The user may have each rev reviewed by [review-doc](../review-doc/SKILL.md),
which writes `ROADMAP.revN.notes.md` beside your rev. Before writing
rev(N+1):

- **Read the notes and answer every finding explicitly** in a "Responses to
  revN notes" section of the new rev: fixed (and how), disagree (and why —
  the user settles it), or needs a decision from the user. The reviewer
  checks resolved-versus-restated, so never silently drop a finding.
- **Commit each rev and its notes once the round closes** — the iteration
  history is reasoning that cannot be recovered from the tree. Do not push
  unless asked.

To run the rounds without the user relaying each one, see
[answer-notes-loop](../answer-notes-loop/SKILL.md).

When the user signs off, write `docs/<feature>/ROADMAP.final.md` with
[finalize-doc](../finalize-doc/SKILL.md) — the reviewed roadmap with open
questions resolved, followed by the collapsed history of questions, answers
and decisions, after which the revs and notes are deleted. That is what
[execute-roadmap](../execute-roadmap/SKILL.md) executes.

## During execution (once the roadmap is approved)

- **Summarize and commit after each sub-agent task is checked.** When you
  have verified a sub-agent's plan against its verification step, commit it —
  following [commit-changes](../commit-changes/SKILL.md) for the summary — so
  the history stays granular: one commit per verified plan, each explaining
  what changed and why. Do not batch several plans into one commit, and do
  not push unless asked.
