---
name: start-acceptance
description: Open an acceptance-testing session — the user is about to try finished work by hand. Points them at the feature's ACCEPTANCE.md, or writes one from what actually changed when there is none, then takes their notes, screenshots and corrections one at a time, recording each verdict beside its check and fixing or carrying what it finds. Anything that looks like a pattern rather than an incident — a missed requirement, a recurring bug, a design error — is written as a candidate to docs/acceptances/ATTENTION.<feature>.md for end-acceptance to promote, with the user, into docs/acceptances/ATTENTION.md. Runs no test suite during the session, because it is too slow while a person waits; end-acceptance runs it once. Use when the user says they are starting acceptance, about to test or try the feature, or invokes /start-acceptance <feature>.
---

# Start acceptance testing

The user is sitting down to try the work. You owe them two things: a list to
work through, and a memory of what they find that outlives this session.
The list is `docs/<feature>/ACCEPTANCE.md`. The memory is in two places with
two different filters: the verdicts beside the checks, which keep
everything, and `docs/acceptances/ATTENTION.<feature>.md`, which keeps only
what might be systematic. That second file is a holding pen —
[end-acceptance](../end-acceptance/SKILL.md) is where its candidates are
promoted, with the user and in the user's wording, into
`docs/acceptances/ATTENTION.md`, the project-wide watchlist every shaping,
planning, building and reviewing skill reads. Never write to `ATTENTION.md`
from this session.

**The user decides.** They are the acceptance. A correction is not a
disagreement to settle; it is evidence about the plan or the build, and your
job is to find out which. Recommend, record, and let them choose what is
fixed now, carried, or dropped.

## Find or write the checklist

1. **Work out which feature.** From the argument, the branch, the newest
   `EXECUTION.md` or plan folder in the planning folder (`docs/<feature>/`
   unless the project uses another). If it is not obvious, ask — one
   question, with your best guess first.
2. **If `ACCEPTANCE.md` exists**, read it and check it against the tree:
   `git log` since it was written. Work that landed after it is work it may
   not cover — say which checks are affected and append a section rather than
   rewriting what they may already have worked through. Then point the user
   at it: one line per section with its time cost, and where to start.
3. **If there is none, write one** with
   [write-acceptance](../write-acceptance/SKILL.md), from what actually
   changed: the branch's `git log` and diff against the main integration
   branch (or since the release or commit the user names), `EXECUTION.md` and
   the final doc if they exist. Open it by saying what you think the scope
   is — what a person can now do that they could not — and how it should be
   tested, and **ask the user to confirm the scope before they start**. A
   checklist for the wrong scope wastes their session. Keep it as short as
   honesty allows.
4. **Read `docs/acceptances/ATTENTION.md`**, if it exists, and any
   `ATTENTION.<other>.md` still open from an earlier feature. Every entry
   that applies to this feature is a check to add if the list does not
   already have one — the things acceptance has caught before are the first
   things to re-check.
5. Tell them you are ready: send notes, screenshots and corrections as they
   go; you keep the record.

## The record — beside the checks

Keep the verdicts in `ACCEPTANCE.md` itself, under a dated `## Results`
heading (or a results column, if the project's checklists have one), so the
close skills find each verdict beside its check. For each thing the user
sends:

- **Match it to a check.** If it matches none, that is a finding about the
  list — add the check, then record against it.
- **Look at screenshots yourself.** Say what you see against the expected
  observable. Never ask the user to describe what they just showed you.
- **Classify it**, in one word the record can be sorted by: *pass*; *bug*
  (built as planned, does not work); *missed requirement* (nobody planned it,
  a person expects it); *design error* (built as planned, planned wrong);
  *polish* (wording, spacing, a default); or *question* (only the user can
  settle it).
- **Record it**: the check id, the verdict, the user's words, your reading,
  the platform or device it was seen on, and what you did about it.
- **Act on it.** A small bug with a clear cause: fix it now with
  [fix-bug](../fix-bug/SKILL.md), say so, and put the commit hash in the
  record. Anything that is a product decision or has a large blast radius:
  ask, one question, your recommendation first — never decide it inside the
  session. Anything larger than the session: carry it to the questions log or
  the V2 rev the close skills write, with enough context to pick up cold.
  Nothing lives only in chat.
- **Never argue a correction away.** If it is wrong for the user, it is
  wrong. Find out whether the shape, the plan, the build or the review let it
  through — that is what the candidate file needs.
- **Do not run the test suite.** It takes too long, and the user is sitting
  there with the app open. A fix made in the session gets the one targeted
  test for what it touched, if that runs in seconds, and nothing more; the
  full suite, lint and typecheck run once, in
  [end-acceptance](../end-acceptance/SKILL.md). Say in the record that a fix
  is unverified beyond that, so nobody reads it as tested.

## Candidates — `docs/acceptances/ATTENTION.<feature>.md`

Every little thing belongs beside its check. This file is for what might
bite the next feature too: **patterns, not incidents.** Write a candidate as
soon as a finding looks like one — do not wait for the end of the session,
when the reasoning is gone. A finding is a candidate when at least one of
these holds:

- It has happened before — search this feature's record and earlier
  features' records before deciding.
- It happened in more than one place in this feature.
- It is a class, not an instance: "empty states are never specified", "the
  second-device case is never tested", "shortcuts are spelled for Windows" —
  not "the Save button was grey".
- It got through because a stage skipped something: the shape never covered
  failure, the plan had no acceptance for it, the review did not check it.

When unsure, write it as a candidate and say what the doubt is. It is cheap
for end-acceptance to drop one and expensive for a lesson to be lost.

Each candidate is a short entry: the pattern in one line as a heading; which
of the tests above it passes, in a sentence; the check ids and dates it came
from; the stage that should have caught it (shaping, design, planning,
execution, review, acceptance); and a first draft of *what to do instead* —
the check or question that would catch it. Ten lines is long. Create the
file on the first candidate, with a one-line header saying it is the
candidate list for this feature and that end-acceptance retires it.

Candidates that match an existing `ATTENTION.md` entry still go here, noted
as "extends: <entry>", so end-acceptance can grow that entry's record.

## Ending the session

When the user says they are done, or stops sending:

- Report in one screen: checks passed, failed and not run; fixes committed,
  with hashes; what was carried and where; the candidates written.
- Checks that were not run stay on the list, marked as such.
  [close-plan](../close-plan/SKILL.md) and
  [close-roadmap](../close-roadmap/SKILL.md) retire the list, check by
  check; do not retire it here.
- The suite has not run. Say so; end-acceptance runs it.
- Commit the record and the candidate file with
  [commit-changes](../commit-changes/SKILL.md): show the message, commit on
  approval, never push.
- Say that [end-acceptance](../end-acceptance/SKILL.md) is the next step,
  and offer to run it now if the user has the time. The candidates are not
  lessons until it has.
