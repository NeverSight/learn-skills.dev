---
name: review-doc-loop
description: Run the reviewer's half of the document review loop without the user relaying each round — review the current <DOC>.revN.md into <DOC>.revN.notes.md, commit the closed round, wait for the author's rev(N+1), and repeat until the document is ready for final, a round cap is hit, or only the user can move it forward. Use after rev1 exists, when the user invokes /review-doc-loop <feature> [max-rounds] in a fresh session that did not write the document. Its counterpart is answer-notes-loop in the author's session.
---

# Reviewer's side of the review loop

You are the reviewing architect from [review-doc](../review-doc/SKILL.md).
Without this loop the user carries each round by hand: "review 1", then
"review notes 1" to the author, then "review 2". This skill replaces the
carrying, and nothing else. **Every rule and every lens in review-doc still
applies in full** — read it before the first review — and so do these:

**A review requires fresh eyes.** If this session authored the document under
review, stop and say so; the loop's whole value is that the two voices belong
to two sessions.

**Never assume or take a product decision.** A finding that turns on what the
customer sees, or on anything expensive to reverse, is recorded as an open
question with your recommendation — never resolved in the notes, and never
treated as resolved because the author wrote the next rev under your
recommendation. Two agents converging on a product choice between themselves
is the failure this loop must not produce. Open questions ride along in the
notes each round; the review continues on everything else.

**The rev is never yours to touch.** You write `<STEM>.revN.notes.md` and
nothing else, not even a typo in the plan.

## Inputs

`/review-doc-loop <feature> [max-rounds]`. `max-rounds` is how many review
rounds the loop may run before stopping to report; the default is **3**.

1. Find the stem and the current round in `docs/<feature>/` (the project's
   planning folder, unless it uses another): the highest `<STEM>.revN.md` and
   whether its `.notes.md` already exists. If a `<STEM>.final.md` exists,
   stop — there is nothing to iterate.
2. Do review-doc's inputs once, up front: the notes folder, the project's
   stated principles, every earlier rev and notes file, and the code the plan
   touches. Check the branch against the main integration branch (e.g. `main`
   or `dev`): `git fetch`, then `git log --oneline <branch>..<main>`. **Do not
   merge inside the loop** — a merge has its own review gate. Record the drift
   in the first notes file and review touched files as the main branch has
   them.
3. Tell the user in one line what you found and that you are entering the
   loop: the feature, the stem, the rev you are reviewing first, and the round
   cap.

## The loop

Each turn is: **review the rev → write the notes → commit the round → wait
for the next rev, or stop.**

### Review and write

Review `<STEM>.revN.md` exactly as review-doc describes, checking for N > 1
that each finding from your previous notes was resolved rather than restated.
Write `docs/<feature>/<STEM>.revN.notes.md` in review-doc's shape, with **one
addition**: the first line after the title is the verdict the author's loop
branches on, in one of exactly three forms:

- `Verdict: needs rev<N+1>` — findings remain that block execution.
- `Verdict: ready for final` — nothing left blocks execution. Open product
  questions may still be listed; they go to the user with the sign-off.
- `Verdict: blocked on the user` — the loop cannot usefully continue: the
  same finding has survived two rounds unaddressed, a product or blast-radius
  decision determines the shape of the plan itself, or the plan carries a
  persisted schema/format change with no recorded approval.

### Commit the round

The round closes when the notes exist. Commit **exactly** the rev and its
notes — `git add docs/<feature>/<STEM>.rev<N>.md docs/<feature>/<STEM>.rev<N>.notes.md`,
never `-A` — with a message that says which round closed and its verdict.
The author's session shares this checkout and writes nothing else during the
loop, so anything else that is dirty is not yours to stage. Do not push.

### Wait or stop

Stop and report if the verdict was `ready for final` or `blocked on the user`,
or if N equals max-rounds. Otherwise watch for
`docs/<feature>/<STEM>.rev(N+1).md` — with your runtime's background watcher
if it has one — using a poll that exits once the file exists and its size has
been stable across two polls, outliving any per-call timeout and with its own
deadline, because a watch that can only report success is silence when the
author's session dies:

```sh
f="docs/<feature>/<STEM>.rev<N+1>.md"; prev=-1; n=0
while [ "$n" -lt 960 ]; do
  if [ -f "$f" ]; then
    size=$(wc -c < "$f")
    if [ "$size" = "$prev" ] && [ "$size" -gt 0 ]; then echo "rev ready: $f"; exit 0; fi
    prev=$size
  fi
  sleep 15; n=$((n + 1))
done
echo "gave up: no $f after four hours"; exit 1
```

Do nothing else while waiting. When the "gave up" line arrives, report to the
user and stop; do not restart the watch on your own.

## Reporting and stopping

The loop ends in one message to the user that stands alone:

- **The verdict first**, and which rev it is about: recommend sign-off,
  blocked, or the round cap reached with what still blocks.
- **Every open question**, one decision per bullet in plain language, with
  your recommendation and what each option means for the product — the same
  list the notes carry, so the user reads them here and not in the file.
- **What this review changed** in a few lines: the findings that reshaped the
  plan, and anything the author disagreed with that the user now settles.

The user answers in the **author's** session, because the answers become the
next rev or the final; you stand by for a re-review of the final when it
appears, as review-doc's last step describes.

Stop the loop early if the user interrupts; when they do, say which rev and
which notes exist and whether the last round was committed.
