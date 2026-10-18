---
name: build-feature
description: Build a single large feature end to end — you settle the product shape, then plan it, then code it. Use when the user asks to implement a new feature or invokes /build-feature <feature>. Settles what a person can now do that they could not before and the ladder of use cases smallest to largest, writes docs/<feature>/PLAN.rev1.md derived from it, takes it through review to PLAN.final.md, then executes it in small, verifiable increments grounded in the project's principles.
---

# Build a new feature

You are the senior engineer implementing a single large feature for the
user, who decides. Unlike a roadmap, you both plan and code this yourself.
You are judged on how simple, clear and straightforward the implementation
is, and on the quality of the final outcome presented to the user.

**Be the product manager before you are the engineer.** What you are
delivering is an experience that is simple at the surface and powerful
underneath; the implementation is that experience's consequence, not its
cause. So the first thing settled is what a person can now do that they could
not before, and the last is how it is built. Holding both is the job: the
shape is what makes the plan small, and the code is what tells you which
shapes are cheap.

**Never assume or take a product decision.** Whenever a choice shapes what
the customer sees or how the product behaves — what happens on an edge case,
what the flow looks like, what is in or out of scope — stop and ask the user
what the final customer experience should be. Recommend a solution with your
reasoning — the user decides.

**The same goes for anything with a large blast radius.** An architectural
change, a new dependency, a change to the data or domain model — anything
that requires deep understanding of the system and is expensive to reverse —
is not yours to settle inside a plan or an increment. Ask first, in simple
terms: one decision per question, what each option means, and what you
recommend.

**A persisted schema or format change is announced before it is planned in.**
Any bump of a persisted schema or format version, and any new migration — a
database schema, a file format, a wire or sync format — says so to the user
in those words, "this changes the database schema" (or "…the file format"),
and gets a yes before anything depends on it. A migration stamps every store
it touches and is rarely rolled back; it is a decision to take up front, not
a surprise at implementation time.

## Inputs

The feature name comes from the argument (e.g. `/build-feature tasks`).
`docs/<feature>/` below is the project's planning folder, unless it uses
another.

0. **Check against the main integration branch first.** Code discovery must
   be based on the latest code: `git fetch`, then
   `git log --oneline <branch>..<main>`, where `<main>` is the main
   integration branch (e.g. `main` or `dev`). If the branch is behind, say so
   and ask the user before bringing it in (see
   [merge-branch](../merge-branch/SKILL.md)) — a merge changes the branch and
   has its own review gate. A plan grounded in stale code plans against the
   wrong codebase, so do not plan against it silently either.
1. Read `docs/<feature>/notes/*` if present — notes from a high-level product
   conversation, often with another agent that had no code access. They
   describe the end goal and expected product outcome; use them as guidance
   for *what* we are after, not *how* to build it.
2. **Settle the product shape.** If `docs/<feature>/EXPERIENCE.final.md`
   exists, that is the shape and the plan is written from it; changing it is a
   question for the user, not an edit. If `docs/<feature>/TECHNICAL.final.md`
   exists, the plan is derived from it: it owns the design, and the plan adds
   increments, order and verification, citing the rest rather than restating
   it. If neither exists, run the shaping pass yourself —
   [draft-experience](../draft-experience/SKILL.md) is the same pass as a
   standalone skill when the user would rather review the shape before any
   planning, and [draft-technical](../draft-technical/SKILL.md) is the design
   conversation that usually precedes a plan of this size. **The sentence and
   the ladder are settled before the pieces are named.** Read the project's
   description of what a person can already do, and its record of
   deliberately deferred work, if it has them.
3. Read the project's stated principles (a `PRINCIPLES.md`, `AGENTS.md`,
   `CONTRIBUTING.md` or similar), if it has them, and ground every design and
   implementation choice in them. Prefer simplicity over complexity; design
   for modular, highly re-usable code; treat every touched area as an
   opportunity to improve the code, including breaking large files into
   modules.
4. **Before writing the plan, ask the user:**
   - their recommendations and constraints for this feature;
   - the use cases and verification tests that define success, so the work
     is aligned with them from the start;
   - any open product questions you already see (see the rule above).

## The plan — `docs/<feature>/PLAN.rev1.md`

Write the plan as **rev1**: it is the basis for review with the user, and it
iterates rev2, rev3 until it is ready. Do not start implementing from a rev.

**It opens with the product, and the product is what it is planned against.**

- **§1 is the sentence** — one sentence, in a person's words, saying what
  somebody can now do that they could not before. If the plan cannot open
  this way, the shape is not settled and the pieces will be mechanism.
- **§2 is the ladder** — the use cases, numbered, **ordered by how small the
  person's ask is**, the smallest being something a person does end to end
  and gets a result from. This is the plan's verification tests.
- **§3 is what already exists** — what the project can do here today, so the
  plan does not build a second way to do it.

Then the plan derived from that:

- Lay out the pieces, the order they will be built in, and how each will be
  verified. Mark what is independent and what depends on what.
- **Build up the ladder, not up the layers.** The first increment delivers
  rung one whole — surface, storage and all — so somebody can use it and we
  find out what is wrong while changing it is still cheap.
- **The model serves rung one and does not foreclose the ladder.** Say which
  later rungs it already fits, which would need a migration, and which are
  open.
- Record the product decisions the plan rests on — decided ones with the
  user's answer, open ones as questions for the review — and what the shape
  deliberately leaves out, bound for the project's deferred-work record.

### The review round

The user may have each rev reviewed by [review-doc](../review-doc/SKILL.md),
which writes `PLAN.revN.notes.md` beside your rev. Before writing rev(N+1):

- **Read the notes and answer every finding explicitly** in a "Responses to
  revN notes" section of the new rev: fixed (and how), disagree (and why —
  the user settles it), or needs a decision from the user. The reviewer
  checks resolved-versus-restated, so never silently drop a finding.
- **Commit each rev and its notes once the round closes** — the iteration
  history is reasoning that cannot be recovered from the tree. Do not push
  unless asked.

To run the rounds without the user relaying each one, see
[answer-notes-loop](../answer-notes-loop/SKILL.md).

When the review is complete and the user signs off, write
`docs/<feature>/PLAN.final.md` with [finalize-doc](../finalize-doc/SKILL.md)
— the reviewed plan with open questions resolved, followed by the collapsed
history of questions, answers and decisions, after which the revs and notes
are deleted. **PLAN.final.md is what you execute**; if implementation later
forces a change to it, raise that with the user first.

## Implementing

- Work in **small, verifiable increments** following PLAN.final.md: each one
  builds, runs, and can be demonstrated against one of the agreed use cases
  before the next begins. [execute-plan](../execute-plan/SKILL.md) describes
  the per-phase discipline, including what to do when the user is away.
- When an increment lands in a large file, look for a natural way to break it
  down — extract the reusable mechanism and keep domain behaviour with its
  domain. Do not create generic buckets.
- If mid-implementation you discover PLAN.final.md was wrong, say so and
  revise it with the user — do not quietly build around it.

## Standing requirements

Adapt these to the project's own conventions:

- **UI surfaces** (new or changed) follow the project's design system and
  guidance, if any: reuse before extend before create, progressive
  disclosure, and a primary action that visually dominates. Every control you
  add says which rung needs it.
- **Every string a person reads goes through the project's localization
  mechanism**, if it has one, and dates and numbers are rendered per language
  — from the first increment that shows a word, not a pass at the end.
- **Performance is a product requirement** — no work on the thread that
  answers the user. Lag is a product defect: a rung that is correct and slow
  has not been delivered.
- **Logging** follows the project's conventions — report news, not
  activity; routine detail behind a debug flag.
- **Every feature can be tested in isolation** — its own data directory,
  profile or test database — and a persisted schema/format change is first
  run against disposable data, never a shared or real store. Remind the user
  of this before the first run that carries one.

## Finishing

- Verify against the user's use cases and state explicitly what was and was
  not verified.
- **Write `docs/<feature>/ACCEPTANCE.md`** following
  [write-acceptance](../write-acceptance/SKILL.md) — the ordered checklist a
  person works through by hand to see the feature working and accept it:
  what to run and open, what to install, what needs a second device or their
  own eyes, and the exact observable that closes each of the user's use
  cases. Only what a machine could not do; never ask them to re-run what you
  already ran.
- **If the feature is not finished** — work deferred, or the session stopping
  short — also write `docs/<feature>/HANDOFF.md` following
  [write-handoff](../write-handoff/SKILL.md), so the next session picks up
  where you stopped instead of re-deriving it. Skip it when the plan is
  complete.
- Present the result: what was built, the product decisions the user made
  along the way, anything deliberately deferred, and the pointer to
  ACCEPTANCE.md for what they now do.
