---
name: close-roadmap
description: Close out a finished roadmap or feature execution by retiring its planning docs into canonical documentation and carrying what is still owed into the next roadmap — you are the archivist and the architect of the next round, not the coder. Use when the user invokes /close-roadmap <feature>, or asks to clean up a feature's docs, retire a roadmap, prepare for the next roadmap, or tidy docs/<feature>/ after execute-roadmap or build-feature has finished. Reviews ACCEPTANCE.md check by check, triages every item of ROADMAP.final.md or PLAN.final.md as landed, pending, deferred or dropped; moves pending work into ROADMAP-V2.rev1.md; turns landed work into decision records, architecture, data-model and product docs; writes the folder's README.md; deletes revs and execution artifacts the tree no longer needs; and fixes every inbound link. Nothing disappears unaccounted for; the user settles anything that would be dropped. For a small plan whose landed work folds into pages that already exist, use close-plan instead.
---

# Close a roadmap

You are closing the loop on a feature for the user. Execution is over:
`ROADMAP.final.md` or `PLAN.final.md` was signed off and built, and
`docs/<feature>/` (the project's planning folder, unless it uses another) now
holds the planning documents, review notes and execution artifacts that got
it there. Left alone, that folder becomes the thing the next agent reads
first and trusts most, and most of it is no longer true. Your job is to leave
behind **what exists** (canonical, current, one hop from the project's agent
orientation) and **what is still owed** (the next roadmap's rev1), and
nothing else.

You are judged on whether a fresh agent, reading only the tree, learns the
truth about this feature in the fewest hops — and on whether every item that
was ever promised in the final doc can still be found: landed, carried
forward, deferred, or dropped by the user's decision.

**Never drop work on your own.** A plan the final doc promised is a product
commitment. If it did not land, it goes to the next roadmap unless the user
says otherwise; if the user says otherwise, it goes to the project's
deferred-work record (if it has none, a "Deferred" section in the folder's
README) with the reason, so it is not silently re-decided later.

**Never take a decision while recording one.** Writing a decision record for
a decision that was already made is your job; making a new one is not. Where
the record is ambiguous — an execution deviation with no stated reason, a
logged question the user never answered — ask, in simple terms, one decision
per question.

## Inputs

The feature name comes from the argument (e.g. `/close-roadmap notifications`).
Read all of `docs/<feature>/` and then, in this order:

1. **The final doc** — `ROADMAP.final.md` or `PLAN.final.md` (and
   `TECHNICAL.final.md` or `EXPERIENCE.final.md`, if the feature has them).
   If only revs exist, stop: nothing was signed off, so there is nothing to
   close.
2. **The execution record** — `EXECUTION.md` (what landed, with commit
   hashes), the questions log (deviations and unanswered questions, wherever
   the project keeps them), `ACCEPTANCE.md` (what a person was asked to
   verify by hand), `HANDOFF.md` (the briefing to the next agent), and any
   list of untested items or test plan. These are claims, not facts; the
   next step checks them, and `ACCEPTANCE.md` gets a review of its own before
   the triage.
3. **The code and the history.** `git log` for the branch and the commits
   EXECUTION.md cites; then the code itself for every plan the doc marks
   done. **A plan is landed when the code does what the plan's verification
   step says, not when a document says it did.** A plan that landed in a
   different shape from the one planned is a decision (see "Landed work"),
   not a discrepancy to smooth over.
4. **The canonical docs this feature touches** — wherever the project's doc
   map (e.g. a table in `AGENTS.md` or `CONTRIBUTING.md` saying where each
   kind of doc lives) sends architecture, data model, operations, user guide
   and product status, and the feature's own entry in the docs index if
   there is one. Read them before writing into them, so an addition lands
   beside its neighbours rather than as a second copy.
5. **Any already-closed feature folder** in the project, so the result has
   the same shape.

Check against the main integration branch as the sibling skills do
(`git fetch`, then `git log --oneline <branch>..<main>`, where `<main>` is
e.g. `main` or `dev`). Closing a roadmap against a tree that has since
changed writes documentation of a state that no longer exists; say so and ask
before merging (see [merge-branch](../merge-branch/SKILL.md)).

## The acceptance review — settle this before the triage

`ACCEPTANCE.md` is the checklist a person was asked to work through by hand
(see [write-acceptance](../write-acceptance/SKILL.md)). It exists because
those checks are the ones no machine could run, which makes it the one part
of the record you cannot confirm by reading the code. **Go through it check
by check** and give each a result:

| Result | What it means | What you do |
| --- | --- | --- |
| **passed** | the user or tester reported the named observable | cite it as the evidence for that plan's *landed* fate |
| **failed** | they reported something else | the plan is not landed — it is pending, and the V2 rev1 says what was seen |
| **never run** | no result was ever reported back | ask; it is not landed until it is answered |

**A never-run check is unverified work, not landed work** — the same
standing as a plan whose verification step never ran. Do not quietly promote
it because the code looks right: it was on that list precisely because
reading the code could not settle it. Ask the user, in one question per
check, whether to run it now or accept the work unverified; if they accept it
unverified, it is marked as partial wherever the project records what works
today, and the verification becomes a plan in the V2 rev1.

Bring the results into the ledger below as the evidence column, and say in
your report which plans are landed on a person's confirmation rather than on
a green suite. If a check is still worth running after this feature closes —
a regression, not a one-time acceptance — it moves to the feature's live test
plan before `ACCEPTANCE.md` is deleted.

## The triage — echo it back before touching a file

Every milestone and plan in the final doc, and every entry in the questions
log, any untested list and the test plan, gets exactly one of four fates:

| Fate | Meaning | Where it goes |
| --- | --- | --- |
| **landed** | verified in the code, with the commit — and its acceptance check passed, where it had one | canonical docs; the plan text is deleted |
| **pending** | promised and not built, or partly built | `ROADMAP-V2.rev1.md`, with its original id in parentheses |
| **deferred** | the user has decided not to build it for now | the deferred-work record — what, why, and what would change the answer |
| **dropped** | the user has decided it will not be built | a line in the V2 rev1's "Not carried forward" section, with the reason |

Only the user can assign *deferred* or *dropped*. Present the ledger as a
table — id, title, fate, evidence (commit hash or file) — with the questions
that need an answer marked, **and wait for the user before deleting
anything.** The ledger is the one output of this skill that cannot be
reconstructed from the tree afterwards, so it also goes into the commit
message.

## What is still owed — `docs/<feature>/ROADMAP-V2.rev1.md`

It is a **rev1** because it re-enters the
[draft-roadmap](../draft-roadmap/SKILL.md) review cycle: rev2, rev3,
`ROADMAP-V2.final.md`, then [execute-roadmap](../execute-roadmap/SKILL.md).
Write it as draft-roadmap would, and it inherits that skill's standing
requirements for every plan.

- **Open with "Where this picks up"**: one paragraph on what the previous
  roadmap delivered, pointing at the README rather than repeating it, and
  what remains — ordered by urgency, with the reason for the order. A debt
  (a promise made to users that is not yet kept) comes before a feature.
- **Carry the invariants forward.** The final doc's execution contract,
  standing requirements and invariants survive; the new plans are reviewed
  against them. Copy them, do not link to a file you are about to delete.
- **Every pending plan keeps its inputs, outputs and verification step**,
  rewritten against the code as it is now — a plan that named a seam that has
  since moved must name the new one. A partly-built plan says what exists and
  what is left, with the file where the existing half lives.
- **Open questions from the log** that the user has not answered become the
  rev1's open product questions, each with the options and the
  recommendation that was logged. Answered ones are decisions, and go to a
  decision record, not here.
- **"Not carried forward"** lists what the user dropped, with the reason, so
  the reviewer can see the roadmap shrank on purpose.

Do not restate what was built. The rev1 assumes the README.

## Landed work — write it where it will be read

Route each piece of landed work by the project's doc map. The feature folder
holds only what is *about this feature and nothing else*; anything a reader
of another area needs goes to the shared page.

- **Decisions → decision records (ADRs), one each, if the project keeps
  them.** The execution deviations in the questions log and EXECUTION.md are
  decisions that were made under pressure and usually never got a record;
  write them now, with the alternative that lost, while the reasoning is
  still in the tree. Check for decisions the final doc settled during review
  ("Responses to revN notes") that the code now embodies. Take numbers from
  the project's register; if another branch has already published a number,
  it wins — the newcomer renumbers, and its cross-references move with it.
  **Do not start a per-feature decisions file** when the project has a shared
  register.
- **Model → the project's data-model documentation**, linking the decision
  record. A feature with a model of its own that the shared page should not
  carry (a schema, a wire format) gets its own data-model page in the folder.
- **Code shape and data flow → the shared architecture docs** when it crosses
  modules; a folder `ARCHITECTURE.md` when it is the feature's own internals.
  Each file says what is normative — usually the code's types — and that
  where prose and code disagree, the code is right and the prose is a bug.
- **Operations, APIs, events, configuration and environment variables** —
  wherever the project documents them. If any of those docs are generated,
  run the generator and commit what it produces rather than editing by hand.
- **What a person does → the user guide. What works today → the project's
  product status page**, honest about done versus partial: a plan that
  landed with untested items is partial until someone verifies it, and the
  verification is a plan in the V2 rev1.
- **Code walked past → the project's tech-debt record**, with what, why not
  yet, and what would make it safe. A worker's "I did not touch X because" in
  EXECUTION.md is usually one of these.
- **A manual test plan stays** if it is still the manual pass for the
  feature, with its known gaps current.

Do not write a summary document that repeats what the shared pages say. The
README's job is to point; the shared pages' job is to hold.

## The folder's README.md

Write or rewrite `docs/<feature>/README.md`:

1. **One sentence of what the feature is**, the sentence everything else
   follows from, then a navigation table: *you want to know … → read …*,
   pointing at the shared pages for everything that lives there and at the
   folder's own files for the rest. The next roadmap is one row.
2. **What is in this folder**, one line per file, and what each is *for* —
   including what is historical and what is normative.
3. **Where new work goes**, the table that keeps the folder from silting up
   again: decisions to a decision record, model changes to the data-model
   page, deferred work to the roadmap, and so on.
4. **The shortest possible summary of what exists**, for a reader who will
   not click through. Not a second architecture document.

Mark `notes/` historical with its own README: what each note was, what
overtook it, where it was right and where it was not. The notes stay — they
are the reasoning the roadmap started from — but nothing in them is normative
and nobody implements from them.

## Delete what the tree no longer needs

Once the user has approved the ledger and the canonical docs are written:

- **Delete the final doc, every `.revN.md` and `.revN.notes.md`, and
  `EXECUTION.md`, the feature's questions log, `ACCEPTANCE.md`, `HANDOFF.md`
  and any untested list** — carrying any acceptance check still worth
  re-running into the feature's live test plan first, since a check nobody
  will run again is spent but a regression check is not. They were committed
  when each round closed, so git holds the iteration history; a copy in the
  tree is the copy an agent will mistake for current. Do not move them to an
  `archive/` folder — that is a delete with a longer path, and the folder
  silts up in its turn. The commit message names each deleted file and where
  its content went.
- **Keep** the README, the V2 rev1, `notes/`, a live test plan, designs and
  assets that plans still cite, and any file a citation depends on — grep
  first, because source code sometimes cites docs by name.
- **Fix every inbound link.** Grep the docs, the agent orientation files, the
  READMEs and the source tree for each deleted or renamed path. The feature's
  entry in any docs index points at `docs/<feature>/README.md`, never at a
  roadmap.
- **Run any tests that enforce generated docs**, and the standing checks the
  final doc named. If there is no link checker, the grep above is the link
  check, so do it after the last rename, not before.

## Finishing

- **Commit the closure as one change** following
  [commit-changes](../commit-changes/SKILL.md): the ledger, what was written
  where, what was deleted and where its content went. Never push unless
  asked. The V2 rev1 is part of the same commit; its review rounds are
  separate commits, as draft-roadmap specifies.
- **Report to the user in product language**: what the feature does now,
  what is still owed and in what order, what they decided during the closure,
  and what the reviewer should look at first in the V2 rev1.
