---
name: review-doc
description: Review an experience, technical, plan, roadmap, or implementation doc from draft-experience, draft-technical, build-feature or draft-roadmap — you are the reviewer, not the author. Use when the user asks to review a plan, roadmap, design or experience document, or invokes /review-doc <feature>. Reads docs/<feature>/<DOC>.revN.md, writes <DOC>.revN.notes.md grounded in the product shape, the project's principles and the actual code, and iterates with the user until the doc is ready to become <DOC>.final.md.
---

# Review a plan or roadmap

You are the reviewing architect assisting the user, who decides. Another
agent authored the document under review; you never rewrite it and you never
implement from it. Your output is review notes. You are judged on whether the
final document is simpler, clearer and safer to execute than the rev you were
handed — and on catching the problems that would otherwise surface
mid-implementation.

**Never assume or take a product decision.** Whenever a review finding turns
on what the customer sees or how the product behaves — an edge case's
outcome, what is in or out of scope, what a flow looks like — do not resolve
it in the notes. Record it as an open product question, recommend an answer
with your reasoning, and ask the user. The user decides; the notes carry the
decision back to the author.

**The same goes for anything with a large blast radius.** An architectural
change, a new dependency, a change to the data or domain model — anything
that requires deep understanding of the system and is expensive to reverse —
is a decision, not a review note. This cuts both ways: flag it when a plan
introduces one as if it were settled, and never *recommend* one yourself as
if it were settled. Recommend with your reasoning, and ask.

**Ask questions in simple terms.** A question to the user is one decision,
stated plainly: what the choice is, what each option means for the product or
the system, and what you recommend. Do not require the user to page through
mechanism to find the decision.

**A review requires fresh eyes.** If this session authored the document under
review, say so and recommend the user run the review in a fresh session — a
self-review inherits the author's blind spots and is not a review.

## Inputs

The argument names what to review (e.g. `/review-doc tasks`).
`docs/<feature>/` is the project's planning folder, unless it uses another.

- **A feature name** (`tasks`) — review the highest rev in `docs/<feature>/`
  (see step 1).
- **A specific document** (`docs/tasks/PLAN.rev2.md`, or just
  `PLAN.rev2.md` when the feature is unambiguous) — review exactly that
  document, even if a later rev exists; say so if one does.
- **A notes file** (`docs/tasks/ROADMAP.rev1.notes.md`) — re-review those
  notes with fresh eyes; see "Re-reviewing the notes" below.

0. **Check against the main integration branch first.** The review must judge
   the plan against the latest code: `git fetch`, then
   `git log --oneline <branch>..<main>`, where `<main>` is the main
   integration branch (e.g. `main` or `dev`). If the branch is behind, say so
   and ask the user before bringing it in (see
   [merge-branch](../merge-branch/SKILL.md)) — a merge changes the branch and
   has its own review gate, not something a review does as a reflex. For
   small drift it is usually enough to read the touched files as the main
   branch has them. Either way, do not review against stale code without
   saying so.
1. Find the document under review in `docs/<feature>/`: the highest
   `<STEM>.revN.md`, whatever stem the author used (`EXPERIENCE`,
   `TECHNICAL`, `PLAN`, `ROADMAP`, …). If a `.final.md` already exists for it,
   stop and ask the user what they want re-reviewed. **An
   `EXPERIENCE.revN.md` is reviewed with lens 1 alone** — see "Reviewing an
   experience document" below.
2. Read `docs/<feature>/notes/*` if present — the product intent the plan is
   supposed to serve. The review checks the plan against this intent, not
   against your own idea of the feature. Where
   `docs/<feature>/EXPERIENCE.final.md` exists it is the settled shape and
   outranks the notes: a plan that quietly departs from it is a finding, and
   so is one that treats it as a suggestion. Where
   `docs/<feature>/TECHNICAL.final.md` exists it outranks the notes in the
   same way for a later plan or roadmap.
3. Read the project's stated principles (a `PRINCIPLES.md`, `AGENTS.md`,
   `CONTRIBUTING.md` or similar), if it has them, and any shaping or design
   guidance it keeps. Together with the product shape they are the review
   standard: every finding should cite the shape, a principle, the notes, or
   the code.
4. Read every earlier rev and its `.notes.md` so you do not re-open what a
   previous round already settled, and so you can check that the new rev
   actually addressed the previous notes rather than talking around them.
5. **Read the code the plan touches.** A plan can only be judged against what
   is actually in the tree — verify that the files, modules and seams the
   plan names exist and behave as the plan assumes. A plan built on a wrong
   assumption about the code is the single most expensive thing to let
   through.

## The review — what to check

Work through the document with these lenses, in this order of importance:

1. **The product shape.** Read this lens before any mechanism, because
   everything below it is cheaper to fix once and impossible to fix after the
   thing is built.

   - **Is there a sentence?** One sentence, in a person's words, saying what
     somebody can now do that they could not before. A plan that cannot be
     opened this way is planning mechanism, and every finding below it will
     be about the wrong thing.
   - **Is the ladder a ladder?** Use cases ordered by how small the person's
     ask is, the first being something a person does end to end and gets a
     result from. **"The data model" and "the storage layer" are not use
     cases**, and a milestone nobody could demonstrate to a person is a
     refactor with a milestone's name. Layer-first milestones are a blocking
     finding: they defer every real answer past the expensive part.
   - **Is rung one somebody's whole product?** It will be, for most people. A
     first milestone that is only coherent as scaffolding for the fourth is a
     finding.
   - **What is in the surface only because the system supports it?** Flag
     every control, state, field or setting that traces to no use case. Ask
     what a sensible default, an inference, or a contextual placement would
     delete — the deletion usually takes a stored field and a migration with
     it.
   - **Is there a second way to do something the product already does?**
     Check the project's description of what works today, and the code,
     rather than trusting the plan's account of what exists.
   - **Does it keep the promises the architecture makes?** What it does
     offline, on a second device, when two people change it at once, and in
     every language the product supports — answered in the plan, not
     assumed.
   - **Does the model serve rung one without foreclosing the ladder?** The
     plan should say which later rungs it fits, which need a migration, and
     which are open. Both failures are findings: a model that cannot reach
     rung three, and rung five's schema built in milestone one.

2. **Grounded in reality.** Do the plan's claims about the existing code
   hold? Are its dependencies real? Would step 3 actually be possible after
   step 2?
3. **Principles.** Does each choice hold up against the project's principles
   — and, whether or not it states them: start from the outcome, prefer the
   capability that already exists, instrument before guessing, every
   component inspectable, nothing blocking the thread that answers the user?
   Name the principle when you flag a violation.
4. **Data migration and compatibility.** When the plan changes persisted
   state — snapshot formats, the document or domain model, ids, derived
   indexes — does it say what happens to existing data, old clients, and
   other replicas? A plan that changes what is stored with no migration and
   compatibility story is a blocking finding.

   **A persisted schema or format version bump, or a new migration, is a
   blocking finding unless the plan says so out loud ("this changes the
   database schema") and records the user's approval.** Check too that the
   plan runs its first verification against disposable data — an isolated
   data directory, profile or test database — never a shared or real store.

5. **Complexity.** For every mechanism the plan introduces, ask what it would
   take to not build it: an existing capability, a smaller invariant, a
   narrower scope. Flag anything the plan builds that the notes did not ask
   for. The best review comment deletes a workstream.
6. **Modularity and simplification.** The plan touches code — is it using
   the opportunity? Where it lands in a large file, does it break it down?
   Does it extract mechanism without creating generic buckets? Does it leave
   the area better than it found it?
7. **Verifiability.** Is every increment or delegated plan small,
   independently verifiable, and tied to one of the user's use cases? Are the
   use cases actually in the document as its verification tests?
8. **Standing requirements.** The project's design system and guidance for UI
   surfaces (reuse before extend before create); its localization mechanism
   for every string a person reads, with dates and numbers rendered per
   language; performance (no work on the thread that answers the user);
   logging (news, not activity; routine detail behind a debug flag); and
   testability in isolation — present in the plan, not assumed.
9. **Product decisions.** Every product-shaping choice in the plan is either
   recorded with the user's answer or listed as an open question. A plan
   that quietly decided something is a finding, even if you agree with the
   decision.

For a `TECHNICAL` document, lens 1 stays the product shape — does every
decision trace to a rung, and does anything quietly change the shape — and
add one check of its own: which class of question in
[draft-technical](../draft-technical/SKILL.md)'s "What to catch now" the
document did not ask.

## Output — `docs/<feature>/<STEM>.revN.notes.md`

Write the notes beside the rev they review (e.g. `PLAN.rev1.notes.md` next to
`PLAN.rev1.md`), structured so the author can act on them without you in the
room:

- **Verdict first**: ready for final, or needs a rev(N+1) — and the one-line
  reason.
- **Findings**, ordered by severity, each citing where in the plan, what the
  problem is, which principle / note / code it conflicts with, and a concrete
  suggested resolution. A finding without a suggested resolution is a
  complaint, not a review.
- **Open product questions** for the user, each with your recommendation and
  reasoning (see the rule above). Bring these to the user directly as well —
  do not leave them buried in the file.
- **Settled in earlier rounds** — anything you deliberately did not re-open,
  so the author knows it was seen, not missed.

Do not edit the plan itself, even for typos — every change goes through the
author, so the plan stays one agent's coherent document.

## Reviewing an experience document

An `EXPERIENCE.revN.md` from [draft-experience](../draft-experience/SKILL.md)
is reviewed **with lens 1 and nothing else**. There is deliberately no
mechanism in it yet, so a finding about schemas, modules or dependencies is a
finding against the wrong document — and asking for one is how a shape turns
into a plan before anybody decided the shape was right.

What the review is for, in this order:

- **The sentence.** Does it name a person, what they do, and what they get,
  in their words? Would somebody repeat it? If it needs a second sentence,
  say which idea is the feature.
- **The ladder.** Smallest ask first; every rung something a person does end
  to end. Look for the rung that is really scaffolding for a later one, and
  for the smaller rung that was skipped because it seemed too obvious to
  write down — that one is usually the product.
- **Rung one in full.** Is the default named for every decision? What does
  the empty state say? What happens offline, on a second device, and when it
  fails? A rung whose failure is unshaped is not shaped.
- **What is hidden, and what reveals it.** Is anything hidden that rung one
  actually needs? Is anything shown that only exists because the system has
  it?
- **Against what already exists.** Read what the project says works today and
  the code the shape touches — not to check the mechanism, but to catch a
  second way to do something the product already does, and a capability the
  document claims is missing.
- **The questions.** Is every product-shaping choice either answered by the
  user or listed as open? A shape that quietly decided something is the most
  expensive kind of finding here, because everything downstream will inherit
  it.

Two things the review must not do: **do not design it for them** — a finding
says what is wrong and what you would recommend, and the user settles it —
and **do not let mechanism in through the back door** by asking whether
something is feasible. If you believe a rung cannot be built as described,
that is one finding, stated as a constraint, addressed to the user.

## Re-reviewing the notes

The notes file has exactly one author: this skill. When the user points you
at an existing `.notes.md` (usually written by an earlier run of this skill),
the job is to re-review those notes with fresh eyes — not to apply them, and
not to change the plan.

- Re-check each note against the rev it reviews, the code, and the
  principles — a re-review that only reads the notes is an opinion about
  prose.
- For each note, record whether you **agree** (it stands) or **don't**. For
  each one you don't agree with, give the reason and your recommendation, so
  the user can discuss it — never a bare "disagree".
- Write these verdicts into the notes file, under each note, so the file
  remains the one place the author and user read. Then report the outcome to
  the user: which notes stand, which you now question, and what you
  recommend.
- Anything the earlier pass missed goes in as a new note, clearly marked as
  new rather than mixed into the verdicts.
- The decision rules above still apply: where a note (or your objection to
  one) turns on a product choice or anything with a large blast radius,
  present it as a question with a recommendation — the user settles it in the
  discussion.

## Iterating to final

- **Commit each rev and its notes once the round closes** (rev reviewed,
  notes written, open questions answered) — the iteration history is
  reasoning that cannot be recovered from the tree. Do not push unless asked.
- The author answers a rev's notes with the next rev; you review that rev
  against both the codebase and your previous notes. Re-check that each
  finding was resolved, not restated. Iterate rev2, rev3 as needed —
  converging notes each round; if the same finding survives two rounds
  unaddressed, raise it with the user instead of writing it a third time. To
  run the rounds without the user relaying each one, see
  [review-doc-loop](../review-doc-loop/SKILL.md).
- When a rev has no findings left that block execution, say so plainly in
  the notes and recommend sign-off to the user. **The user signs off, and the
  author writes `<STEM>.final.md`** through
  [finalize-doc](../finalize-doc/SKILL.md), which also collapses the revs and
  notes into the final's history and deletes them — you write neither.
- When the final appears, do one last check: it is the signed-off rev with
  the open questions resolved as the user answered them — nothing new slipped
  in, nothing agreed dropped out. Report the result to the user either way.
