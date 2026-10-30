---
name: end-pr-review
description: Close a pull-request review session — summarize what was found, decided and changed, for the original author who was not in the room, and check that every change made during the review is documented with its reason before the summary is posted. Then runs end-acceptance to settle the acceptance lessons. Use when the user says the PR review is finished, asks to wrap up or write up a review, or invokes /end-pr-review <pr or branch>. Recommends a verdict; never merges and never pushes unasked.
---

# End a pull-request review

The author of this change was not in the session. They will open the PR and
find comments, new commits and an acceptance record they did not write.
This skill makes sure what they find tells the whole story: what was looked
at, what was decided, what changed in their work and why — in a tone that
teaches rather than scolds, because the point is that the next PR does not
need the same review.

## Gather the record

1. **The PR itself**: the review comments posted during the session and
   their decisions, the description, and the spec the review was done
   against (see [start-pr-review](../start-pr-review/SKILL.md)).
2. **The commits since the author's last one**:
   `git log --oneline <author's last commit>..<branch>`, with their
   messages. Every one of them was made in this session.
3. **The acceptance results** beside the checks in
   `docs/<feature>/ACCEPTANCE.md`, and the candidate file
   `docs/acceptances/ATTENTION.<feature>.md`, if
   [start-acceptance](../start-acceptance/SKILL.md) ran.

## Check that every change is documented

Walk the commit list against the record. For each commit, the author must be
able to find: which finding or acceptance result it answers, and why that
change rather than another. A commit that answers nothing on the record is
a gap — write the missing comment now, before the summary, rather than
letting the change appear unexplained. Then check the other direction: a
finding the user asked to have fixed with no commit answering it is still
open, and the summary must say so.

If a change altered behaviour the project's docs describe, confirm the docs
changed too, or record it as follow-up work.

## The summary

One comment on the PR, written for the author:

- **What was reviewed and against what** — the spec, the principles, the
  acceptance checklist.
- **The findings**, each in one line with its outcome: fixed (and the
  commit), accepted as follow-up work (and where it is recorded), or
  dismissed (and why). Where a finding came from a principle or an
  `ATTENTION.md` entry, say so — that is the part that transfers to the next
  PR.
- **What changed in the author's work and why**, commit by commit, in plain
  language. The reason matters more than the diff; they can read the diff.
- **What acceptance showed**: checks passed, failed and not run, and what a
  person saw that a test could not.
- **What is still owed** and by whom, if anything.

Post it when you can; otherwise give it to the user to post, and say so. It
is a summary of the record, not a replacement for it: the line comments and
the commits stay where they are.

## Close the acceptance

Run [end-acceptance](../end-acceptance/SKILL.md): the candidates this review
raised are settled with the user, in the user's words, and the feature's
candidate file is retired. A review that found a systematic lesson and did
not promote it will find the same lesson in the next PR.

## The verdict

Recommend one — approve, request changes, or back to the author with the
open items — with your reasoning in two sentences. The user decides.
Merging is [merge-branch](../merge-branch/SKILL.md)'s gate, not this
skill's; pushing the session's commits so the author can see them is the
user's call, asked once.
