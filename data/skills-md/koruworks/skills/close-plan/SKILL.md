---
name: close-plan
description: Close out a finished <DOC>.final.md — fold what landed into the docs that already exist, carry what is still owed into <DOC>-V2.rev1.md, and delete the planning artifacts the tree no longer needs. Use when the user invokes /close-plan <feature>, or asks to clean up or retire a small feature's docs after execute-plan or build-feature has finished. Reviews ACCEPTANCE.md check by check before calling anything landed, then triages every phase as landed, pending, deferred or dropped. The smaller sibling of close-roadmap — works for any stem (PLAN, TECHNICAL, …); a plan usually does not earn its own folder of permanent documentation, so the default is to add a paragraph to a page that exists rather than create a new one.
---

# Close a plan

You are closing the loop on a small feature for the user. `PLAN.final.md`
was signed off and built, and `docs/<feature>/` (the project's planning
folder, unless it uses another) now holds the revs, notes and execution
artifacts that got it there. Left alone, that folder becomes the thing the
next agent reads first and trusts most, and most of it is no longer true.

You are judged on whether a fresh agent, reading only the tree, learns the
truth about this feature in the fewest hops — and on whether every phase the
plan promised can still be found: landed, carried forward, deferred, or
dropped by the user's decision.

**Never drop work on your own.** A phase the final doc promised is a product
commitment. If it did not land, it is carried forward unless the user says
otherwise; if they say otherwise, it goes to the project's deferred-work
record with the reason.

**Never take a decision while recording one.** Writing up a decision that
was already made is your job; making a new one is not.

## Which skill this is

- **This skill** — one `PLAN.final.md`, a handful of phases, a feature that
  touches a few areas. Most of what landed belongs in pages that already
  exist.
- **[close-roadmap](../close-roadmap/SKILL.md)** — a roadmap of milestones, a
  feature large enough to own a docs folder, a README that is a navigation
  table, and a V2 roadmap that re-enters the roadmap review cycle.

The line is not the number of phases, it is **whether the feature earns
permanent documentation of its own**. If closing this plan would create a
folder README, an architecture page and three decision records, you are
closing a roadmap — switch. If it would add a section to an existing area
page and one decision record, you are here.

## Inputs

The feature name comes from the argument (e.g. `/close-plan spell-check`).
Read all of `docs/<feature>/`, then:

1. **`PLAN.final.md`** (and `TECHNICAL.final.md`, if there is one). If only
   revs exist, stop: nothing was signed off, so there is nothing to close.
2. **The execution record** — `EXECUTION.md`, the questions log (wherever the
   project keeps open questions), `ACCEPTANCE.md`, `HANDOFF.md`, and any list
   of untested items. Claims, not facts.
3. **The code and the history.** `git log` for the branch and the commits
   EXECUTION.md cites, then the code for every phase the doc marks done. **A
   phase is landed when the code does what its verification step says, not
   when a document says it did.**
4. **The pages this feature touches** — wherever the project's doc map (e.g.
   a table in `AGENTS.md` or `CONTRIBUTING.md`) sends each kind of content.
   Read them before writing into them, so an addition lands beside its
   neighbours rather than as a second copy.

Check against the main integration branch as the sibling skills do
(`git fetch`, then `git log --oneline <branch>..<main>`, where `<main>` is
e.g. `main` or `dev`); closing against a tree that has since changed
documents a state that no longer exists.

## The acceptance review

Go through `ACCEPTANCE.md` check by check exactly as
[close-roadmap](../close-roadmap/SKILL.md) specifies: each one is **passed**
(cite it as evidence), **failed** (the phase is not landed), or **never run**
(ask — it is not landed until it is answered). A never-run check is
unverified work; it was on that list because reading the code could not
settle it, so reading the code cannot settle it now either.

## The triage — echo it back before touching a file

Every phase in the plan, and every entry in the questions log and any
untested list, gets one of the four fates in close-roadmap's table —
**landed**, **pending**, **deferred**, **dropped** — under the same rule that
only the user assigns the last two. Present it as a table (phase, title,
fate, evidence), mark the questions that need an answer, and **wait for the
user before deleting anything.** The ledger goes into the commit message; it
is the one output that cannot be reconstructed from the tree.

Being smaller, this ledger is usually short enough to sit in the report
itself rather than in a document.

## What is still owed

- **A coherent body of remaining work → `docs/<feature>/<STEM>-V2.rev1.md`**,
  named for the stem the final document carried — `PLAN.final.md` closes into
  `PLAN-V2.rev1.md` — written as [build-feature](../build-feature/SKILL.md)
  would write a rev1 and re-entering the [review-doc](../review-doc/SKILL.md)
  cycle before [execute-plan](../execute-plan/SKILL.md) builds it. Open with
  "Where this picks up", carry the final doc's standing requirements and
  invariants forward by copying them (never link to a file you are about to
  delete), and give every pending phase its inputs, outputs and verification
  step rewritten against the code as it is now.
- **One or two loose ends → the project's tech-debt record or backlog**, or
  the area page's "where new work goes" note. A V2 rev1 holding a single
  leftover is ceremony that will be read as a roadmap; do not create one for
  it.
- **Unanswered questions from the log** become the rev1's open product
  questions, with the options and recommendation that were logged. Answered
  ones are decisions and go to a decision record, if the project keeps them.

## Landed work — fold it in, do not build a wing

Route each piece by the project's doc map, with close-roadmap's rules for
each destination (decisions to decision records, model to the data-model
page, what a person does to the user guide, what works today to the product
status page — honest about done versus partial, where a phase accepted
unverified stays partial). Run any doc generators rather than editing
generated files by hand.

**The difference at this size is the default.** A plan's landed work is a
paragraph in a page that exists, not a new page — a new file for every small
feature is how a docs tree silts up, and each one costs every future reader a
hop. Create a `docs/<feature>/` file only when the content is about this
feature *and nothing else* and is too long for the shared page to carry.

**A feature that needs no folder should not keep one.** If everything landed
in shared pages and nothing is owed, delete `docs/<feature>/` entirely
(keeping `notes/` only if it holds reasoning worth preserving, marked
historical) and let the shared pages be the record. Say so in the ledger, so
the user sees the folder go.

If the folder does stay, it needs a `README.md` — one sentence of what the
feature is, a short navigation table, and where new work goes. Not the full
close-roadmap README; a plan-sized folder does not need four sections.

## Delete what the tree no longer needs

Once the user has approved the ledger and the docs are written: **delete
`PLAN.final.md`, every `.revN.md` and `.revN.notes.md`, and `EXECUTION.md`,
the feature's questions log, `ACCEPTANCE.md`, `HANDOFF.md` and any untested
list** — carrying any acceptance check still worth re-running into the
feature's live test plan first. They were committed as each round closed, so
git holds the history; a copy in the tree is the copy an agent will mistake
for current. No `archive/` folder — that is a delete with a longer path. The
commit message names each deleted file and where its content went.

**Fix every inbound link.** Grep the docs, the agent orientation files, the
READMEs and the source tree for each deleted or renamed path — source files
sometimes cite docs by name. If there is no link checker, the grep is the
link check, so do it after the last rename.

## Finishing

- **Commit the closure as one change** following
  [commit-changes](../commit-changes/SKILL.md): the ledger, what was written
  where, what was deleted and where its content went. Never push unless
  asked.
- **Report to the user in product language**: what the feature does now,
  what is still owed, what they decided during the closure, and — if any
  phase landed on a person's confirmation rather than a green suite — which
  ones.
