---
name: answer-notes-loop
description: Run the author's half of the document review loop without the user relaying each round — wait for the reviewer's <DOC>.revN.notes.md, answer it with <DOC>.rev(N+1).md, and repeat until the reviewer says ready for final, a round cap is hit, or only the user can move it forward. Use after rev1 exists, when the user invokes /answer-notes-loop <feature> [max-rounds] in the session that authored the plan, roadmap, technical or experience document. Its counterpart is review-doc-loop in a fresh session.
---

# Author's side of the review loop

You are the author of `docs/<feature>/<STEM>.rev1.md` — the architect from
[draft-roadmap](../draft-roadmap/SKILL.md), [build-feature](../build-feature/SKILL.md),
[draft-technical](../draft-technical/SKILL.md) or
[draft-experience](../draft-experience/SKILL.md). (`docs/<feature>/` is the
project's planning folder, unless it uses another.) Without this loop the user
carries each round by hand: "review notes 1", "review 2", "review notes 2".
This skill replaces the carrying, and nothing else. **The rules of the author
skill still apply in full** — read its "review round" section before the
first wait — and so do these:

**Never assume or take a product decision.** A reviewer's open question that
turns on what the customer sees, or on anything expensive to reverse, is not
yours to answer in the next rev. Carry it forward in an explicit **Open
questions for the user** section — one decision per question, what each
option means, your recommendation — and write the plan under the
recommendation as a stated assumption, so the user's answer changes one
section rather than the whole document. Two agents converging on a product
choice between themselves is the failure this loop must not produce.

**The reviewer's file is never yours to touch.** Your answer to
`<STEM>.revN.notes.md` is `<STEM>.rev(N+1).md`; you do not annotate, correct
or tidy the notes, even for a typo.

**Only the next rev is written during the loop.** Nothing else in the tree
changes while this runs — not the notes, not code, not other docs — because
the reviewer commits each closed round from the same checkout and must find
only the two files it expects.

## Inputs

`/answer-notes-loop <feature> [max-rounds]`. `max-rounds` is how many review
rounds the loop may run before stopping to report; the default is **3**, so
the loop never writes past rev4 on its own.

1. Find the stem and the current round in `docs/<feature>/`: the highest
   `<STEM>.revN.md`, and whether `<STEM>.revN.notes.md` exists beside it. If a
   `<STEM>.final.md` exists, stop — there is nothing to iterate.
2. If this session did not write the current rev, read every rev and every
   notes file, `docs/<feature>/notes/*` and the project's stated principles
   (a `PRINCIPLES.md`, `AGENTS.md`, `CONTRIBUTING.md` or similar), if it has
   them, before acting. You are taking over the author's voice, and the
   reviewer will check that each finding was resolved rather than restated.
3. Tell the user in one line what you found and that you are entering the
   loop: the feature, the stem, the rev you are waiting on notes for, and the
   round cap.

## The loop

Each turn is: **wait for the notes → read the verdict → answer or stop.**

### Wait

Watch for `docs/<feature>/<STEM>.revN.notes.md`. If your agent runtime has a
background watcher (a monitor or background-task tool), use it with a poll
that exits once the file exists and its size has been stable across two polls
— the reviewer writes it in one go, but the check costs nothing. Let the watch
outlive any per-call timeout, and give the poll its own deadline, because a
watch that can only report success is silence when the reviewer's session
dies:

```sh
f="docs/<feature>/<STEM>.rev<N>.notes.md"; prev=-1; n=0
while [ "$n" -lt 960 ]; do
  if [ -f "$f" ]; then
    size=$(wc -c < "$f")
    if [ "$size" = "$prev" ] && [ "$size" -gt 0 ]; then echo "notes ready: $f"; exit 0; fi
    prev=$size
  fi
  sleep 15; n=$((n + 1))
done
echo "gave up: no $f after four hours"; exit 1
```

Do nothing else while waiting. When the "gave up" line arrives, report to the
user and stop; do not restart the watch on your own.

### Read the verdict

The notes begin with one line the loop branches on:

- `Verdict: needs rev<N+1>` — write the next rev (below).
- `Verdict: ready for final` — stop and report. The user signs off; only then
  does [finalize-doc](../finalize-doc/SKILL.md) run, and never from inside
  this loop.
- `Verdict: blocked on the user` — stop and report. The reviewer found
  something neither side may settle: a finding that survived two rounds, a
  product or blast-radius decision the plan cannot be written around, or a
  persisted schema/format change with no recorded approval.

If the first line is none of these, treat it as `needs rev`, and say so in the
new rev's responses section so the reviewer fixes the header next round.

### Answer

Write `docs/<feature>/<STEM>.rev(N+1).md` exactly as the author skill's review
round requires: the full document, plus a **Responses to rev<N> notes**
section answering every finding explicitly — *fixed* (and how), *disagree*
(and why; the user settles it), or *needs a decision from the user* (moved to
the open questions section with your recommendation). Never silently drop a
finding. Do not commit; the reviewer commits the pair when it closes the
round.

Then count the rounds. If the rev you just wrote is rev(1 + max-rounds), stop
and report rather than waiting again. Otherwise wait for the next notes file.

## Reporting and stopping

The loop ends in one message to the user that stands alone:

- **The outcome first**: ready for sign-off, blocked, or the round cap
  reached — and which rev is current.
- **Every open question**, one decision per bullet in plain language, with
  your recommendation and what each option means for the product. These are
  the decisions the user came to make; do not bury them under mechanism.
- **What changed across the rounds** in a few lines: the findings that
  reshaped the plan, and anything you disagreed with that the user now
  settles.

The user answers in *this* session, because the answers become the next rev
or, on sign-off, the final. The reviewer's session stands by for a re-review.

Stop the loop early if the user interrupts; when they do, say which rev and
which notes exist so nothing is lost.
