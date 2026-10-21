---
name: review-walkthrough
description: Mentor a reviewer through a pull request step by step, teaching the code as it goes, and post the agreed findings as one GitHub review in their name.
disable-model-invocation: true
---

# Review walkthrough

Review a pull request the way a senior developer **mentors** a peer through it. Teach each part of
the change and the code around it until the reviewer could change that code themselves, put each
decision to them, and finish with one GitHub review the reviewer posts as their own. The code
stays as the author left it: every change you want becomes a finding.

Write everything with `writing-lean`. The findings, the summary and how to post them are in
[REVIEW.md](REVIEW.md); every GitHub call is in [GITHUB.md](GITHUB.md).

**The reviewer sets the pace.** From step 3 on, a step ends when its **Done when** holds and the
reviewer says to move on. Answering a round settles its findings, not the step: ask if they're
ready.

## 1. Pin the pull request

The argument is a pull request number or URL. A pull request is required, because the walkthrough
reads its linked issue, description, checks and earlier reviews. With none, stop and suggest
`open-pr`.

Record its number, repository, base, head SHA, author, and the issue it closes. Check whether an
agent wrote it: a `copilot/` branch, a bot author, or agent co-authors on its commits.

When the reviewer has reviewed this pull request before, this is a **follow-up review**: record the
commit their last review covered ([GITHUB.md](GITHUB.md#the-last-reviewed-commit)). **The diff under
review** runs from that commit to the head, or from the base when there is none.

**Done when** each of those is recorded, and the diff under review is known.

## 2. Start the background work

Dispatch these as background subagents, so they run while the reviewer answers step 3:

- **`code-review`** over the diff under review. Its requirements are the closing issue and its agent
  brief, plus the earlier review's findings in a follow-up review. Add `house-rules` and
  `writing-lean` to its Standards sources as documented standards; they override its smell
  baseline. When `code-review` isn't
  installed, the subagent instead checks the closing issue and every acceptance criterion in its
  agent brief against the diff under review, and reports each as met, partly met or missing.
- **Checks.** Read the pull request's checks. Cite passing ones as they are. Run locally only the
  checks that failed and the documented checks CI doesn't run, using the commands in the repo's
  `AGENTS.md`.
- **Earlier threads.** Fetch every review thread, from any reviewer, and read every reply. Classify
  each unresolved thread against the commits since: addressed (with the commit), partly addressed,
  not addressed, or no longer applies. For each resolved thread, note whether a reply confirms the
  fix.

**Done when** all three are running.

## 3. Meet the reviewer

Work out who is invoking the skill from `gh` and git, then confirm in one round:

- how well they know this codebase,
- what the review is for: general, correctness, security, performance, or learning the area,
- whether they are the pull request's author.

When the reviewer is the author, tell them now how that limits the review's event; see
[REVIEW.md](REVIEW.md#the-event).

When the diff under review runs past about 400 changed lines or touches many files, recommend
asking for a split before going further. In a follow-up review, recommend carrying on instead:
commits answering a review rarely split well.

Their answers set how deep each step teaches and which findings rank first: a security review leads
with leaks.

**Done when** the reviewer has answered, and has decided on a split if you recommended one.

## 4. Plan the steps

Wait for the `code-review` findings and the earlier threads, then build the step plan from them and
the diff under review. Where `code-review` and a thread disagree on an earlier finding, the thread's
replies win: they hold the reviewer's later decisions. Order the plan from the shared foundation
(helpers, contracts, data shapes) out to the edges and interfaces, so each step builds on the last.
Give the most time to steps holding serious findings, and fold quiet areas into their neighbours.

Show the plan as a numbered list, one line per step naming its files, and let the reviewer reorder,
merge or skip steps. Then add the closing steps: remaining specs, local testing, and draft and
post.

**Done when** the reviewer accepts the plan and every file in the diff under review sits in a step
or on the not-reviewed list.

## 5. Walk each step

Teach each step in this order:

1. **Purpose**: why this code exists and what problem it solves.
2. **How it works**: show the code itself, not just links. Quote each block you discuss verbatim
   in a fenced code block, under a heading or link to its exact lines, with `// ←` markers on the
   lines a finding or point refers to; condense only boilerplate, and say so. Links alone are hard
   to follow. Give enough of the surrounding system for the reviewer to change this code afterwards.
3. **What's significant**: risks, traps, and problems that predate the pull request.
4. **Coverage**: which specs exercise it, and the specific gaps.
5. **Try it locally**: a short way to see it work. When the step changes something a user sees,
   kick the tires with the reviewer now, unless running the app is costly and the requested changes
   will touch the same path; then recommend deferring it. Put everything else on the local-testing
   checklist in the draft.

Raise each earlier thread in the step that covers its code. Note it when it's addressed, propose
carrying it when it isn't (see [REVIEW.md](REVIEW.md#a-finding)), and let the reviewer decide when
it no longer applies.

End the step with a **round**: every proposed finding, numbered as in
[REVIEW.md](REVIEW.md#a-finding), each with your recommendation and worded so that "yes" accepts it,
then "Questions, or ready for the next step?":

```
❓ **F3** - **<finding title>**: <the problem, and why it matters>

➡️ <your recommended fix, and its label and blocking status>
```

Add each agreed finding to the draft as soon as it's agreed.

**Done when** the reviewer's questions are answered and every finding is agreed or rejected.

## 6. Remaining specs

Cover the spec files no step discussed, and the gaps that cut across steps, such as a path that
only runs on reconnect or failure. End with a round.

**Done when** every spec file in the diff under review has been discussed and every finding is
agreed or rejected.

## 7. Local testing

Show the local-testing checklist and offer to run it with the reviewer now, or to leave it until the
requested changes land.

**Done when** the reviewer has run the checklist or chosen to defer it.

## 8. Draft and post

Follow [REVIEW.md](REVIEW.md) to draft the summary and comments, recommend an event, and post.

**Done when** the review is posted, or left pending for the reviewer to submit, and its URL is shown
to the reviewer.

## 9. Recap

In chat, recap the codebase concepts the session taught, one line each, so the reviewer leaves with
a map of the area. Offer to reply "Addressed in `<sha>`" to each earlier thread found addressed and
still unresolved, and resolve it, confirming each with the reviewer.

**Done when** the reviewer has the recap and has answered any offer.
