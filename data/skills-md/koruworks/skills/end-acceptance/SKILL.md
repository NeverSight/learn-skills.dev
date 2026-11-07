---
name: end-acceptance
description: Close out acceptance testing. Finds the open docs/acceptances/ATTENTION.<feature>.md candidate files that start-acceptance left, compares each candidate with docs/acceptances/ATTENTION.md, and for every one not already there asks the user, one at a time, whether it is systematic and settles the exact wording with them before it is moved; then retires the feature file. Runs the project's full test suite, lint and typecheck once first, since the acceptance session skipped them. Use when the user says acceptance is finished, asks to promote or review the acceptance lessons, or invokes /end-acceptance [feature]. Never promotes a lesson in its own wording.
---

# End acceptance testing

`docs/acceptances/ATTENTION.md` is read first by every skill that shapes,
plans, builds or reviews. It stays useful only while everything in it is a
real pattern, said precisely enough that an agent at the right stage knows
what to check. That is why nothing is written to it during an acceptance
session: candidates wait in `docs/acceptances/ATTENTION.<feature>.md`, and
this is where each one is settled with the user, including the words.

**The user decides, and the user words it.** You recommend; you never
promote a candidate on your own wording. If the user leaves mid-way, the
undecided candidates stay in the feature file with your proposal beside
them, and the session stops there.

## Find what is open

1. List `docs/acceptances/ATTENTION.*.md` — every open candidate file, or
   the one the user named. If there is none, say so and stop.
2. For each, say which feature it is, when its candidates were written, and
   whether that feature's acceptance is finished: read the results beside the
   checks in `docs/<feature>/ACCEPTANCE.md`. If checks are still not run,
   say so and ask whether to settle its candidates now or leave the file open
   for the rest of the session.
3. **Read `ATTENTION.md` in full first**, if it exists. You are matching
   against it, and the new entries must use its grouping and its voice. If it
   does not exist yet, you will create it with a two-line header: what it is,
   and that every shaping, planning, building and reviewing skill reads it.

## Run the full tests, once

The acceptance session ran no suite — it is too slow to run while a person
waits — so the tree as the session left it is unverified. Run the project's
full test suite, lint and typecheck now, once, before anything is settled.
A failure is a finding: fix it with [fix-bug](../fix-bug/SKILL.md) when the
cause is small and clear, otherwise carry it to the questions log or the V2
rev with what was seen. The report says what ran and what came back, and a
lesson is not promoted on a red tree without the report saying it is red.

## Compare

Before asking anything, go through every candidate and give it one of three
readings, so the user sees the shape of the session before the questions
start — one line each, in one table:

- **Already covered** — an existing entry says it. The entry's *seen in*
  grows; if the candidate sharpens the entry's wording, that is a proposal.
- **New** — nothing in `ATTENTION.md` covers it. Say which of the systematic
  tests it passes (happened before, more than one place, a class not an
  instance, a stage skipped it) and which stage should catch it.
- **Not systematic**, in your view — an incident, not a pattern — with the
  reason. The user may disagree.

Search before you say "new": the same lesson is often already there under
different words, and two entries for one pattern is how the file stops being
read.

## Ask, one at a time

For each candidate that is *new* or *not systematic*, and for each *already
covered* one whose wording you want to change, one question:

- the candidate, in the record's words, and the check ids it came from;
- why it looks systematic, or why not;
- your recommendation — promote, extend an entry, or drop — first;
- **the exact wording as it would appear in `ATTENTION.md`**: the stage it
  sits under, the heading naming the pattern, *what to do instead* in one or
  two sentences, and *seen in*.

The user approves the wording or changes it. Write what was settled, word
for word — not a paraphrase. One decision per question; never bundle two
candidates, and never move past a question that is still open. Growing an
existing entry's *seen in* without changing its words needs no question;
say that you did it.

## Write and retire

- **Update `ATTENTION.md`**: new entries under their stage, extended entries
  in place. Merge, never duplicate. If the session showed an entry to be
  obsolete — it became a principle, a skill check or a test, or it has not
  bitten in a long time — propose retiring it, as its own question.
- **Delete `ATTENTION.<feature>.md`** once every candidate in it is settled.
  Git keeps it. Dropped candidates are not carried anywhere else; the
  verdicts beside the checks already hold them. If any candidate is still
  undecided, the file stays, holding only those, each with the proposal that
  was made.
- **Commit** with [commit-changes](../commit-changes/SKILL.md): what was
  promoted, extended, dropped and retired, and which feature files were
  closed. Show the message, commit on approval, never push.
- Report in one screen: per feature file, the candidates and what became of
  each, and what `ATTENTION.md` now holds that it did not before.
