---
name: pr-review
description: Review a PR the way a senior teammate does — prior threads re-verified, ticket AC checked, catches separated from concerns, then drafted as inline comments.
disable-model-invocation: true
---

A review is a message to a person, not a report about a diff. It is read by someone who wrote this code yesterday, knows it better than you, and has limited patience. Everything below serves that.

The highest-yield finding is rarely something nobody saw. It is something a human or a bot already flagged that **is still open** in the current code. Reviewers assume a commit named "address review feedback" addressed the feedback; often it addressed two of five. So the review starts in the existing threads and the ticket, not in the diff.

## Steps

1. **Gather the context around the diff.**
   - `gh pr view <n> --json title,body,headRefName,state,reviews,comments`
   - `gh api repos/{owner}/{repo}/pulls/<n>/comments` — the inline threads, bots included
   - `gh pr diff <n>`, plus the neighbouring PRs if the title or body says "1 of N" or "stack"
   - The ticket, when the title, branch, or body names one: pull it from the tracker if one is connected, otherwise ask for the acceptance criteria to be pasted rather than guessing at them.

   Done when you can name the PR's position in its stack, every prior reviewer and what each asked for, and the ticket's acceptance criteria — or which of those does not exist.

2. **Re-verify every prior comment against the code on disk.** Not against the author's reply, not against a later commit message. Open the file and look.

   Done when each prior comment is sorted into fixed or still open, with the `file:line` you checked. A comment you cannot locate in the current code is still open, not resolved.

3. **Check each acceptance criterion against the diff**, one at a time. Grep for the thing the criterion requires — a gate, a state, an awareness of some input — and record what you found.

   Done when every criterion is met, missing, or explicitly deferred to a named later PR in the stack.

4. **Read the diff for what nobody flagged**, with the lenses below.

   Done when each lens has a verdict on the diff, "clear" included.

5. **Verify by reading.** This is a code review, not a QA pass — the evidence for every claim is the source, reached by opening the file, following the definition, and grepping the other callers. Leave the tests, the dev server, the build, and the emulators alone; the author can run those, and a review that waits on a green run is a review that arrives late.

   Existing tests are read as evidence of intent, not run as proof of behaviour: a test asserting the surprising branch tells you it was chosen, and a changed path with no test at all is itself a finding.

   Done when every claim traces to a `file:line` you opened, and anything you could only infer is downgraded to a concern.

6. **Write the review in the shape GitHub takes it**, and nothing else. There is no separate prose report — the review *is* the output, and every part of it must be postable without editing.

   **The summary comment** — what goes in the top review box. Three to five sentences: what the PR does and where it sits in its stack, which prior rounds you re-checked, what came back still open, and the one thing that has to happen before merge. Prior feedback you verified is fixed goes here in a single line so the author is not re-litigated on finished work.

   **The inline comments** — one per `file:line`, each in its own fenced block so it can be copied straight into the review box. Catches and concerns both become comments; a concern says it is not a blocker in its own words.

   Done when every still-open item from steps 2–4 is either an inline comment or a clause in the summary, nothing in the review needs rewriting before it is posted, and nothing appears as a blocking comment that you did not open the file to confirm.

7. **Offer to post it.** `gh pr review <n> --comment --body-file <f>` for the summary, `gh api ... /pulls/<n>/comments` for the inline ones. Wait for a yes — a posted review pings every subscriber and cannot be quietly undone.

## Voice

Write like a teammate who knows the codebase and is typing quickly. Plain words, contractions, short sentences, no section scaffolding inside a finding.

- **Name the mechanism, then the consequence.** "The transition fires before the existence check on line 251. That transition is reachable from three terminal states too. So a duplicate webhook reopens something that was already approved." Three sentences and the author can act.
- **Show what you checked.** "Confirmed via grep — nothing under that directory references entity type." A claim you verified reads differently from one you assumed, and the author can tell which is which.
- **Credit whoever raised it first.** "Flagged in round 1; untouched since." Reviewers stop repeating themselves once they see their comment landed.
- **Hedge only where you are actually unsure**, and say what would settle it: "there's a test asserting this is intentional, so it may be deliberate — worth confirming with whoever made that call."
- **Concede before you object.** "Not a bug, but a future-maintainer trap."
- **Quote the source you are holding the code against** — the acceptance criterion, the prior comment — in its own words, so the author can argue with the source rather than with you.

Delete on sight: severity tables and priority labels; **Issue: / Impact: / Recommendation:** scaffolding repeated per finding; an opening line grading the PR; a list of every changed file; praise for code that works; and any sentence that restates what the diff plainly does.

## Writing a comment

- Lead with `file:line`, then the comment, in a fenced block on its own.
- **Ask, don't assert.** Name the mechanism in a clause, then end on a question the author can answer: "doesn't that mean a replayed webhook can flip an approved record back?", "intentional?", "deferred to a later PR, or should it happen here?"
- Two or three sentences. If it needs a paragraph, the paragraph is you thinking out loud — cut it down to the question that survives.
- **Propose the fix as a question too** — "can we check for the existing record first?" — so disagreeing is cheap.
- **Point at the pattern already in the tree** when one exists: "the sibling service two files over wraps this in `with_lock` — same reason?" An author copies a local precedent faster than they take advice.
- Say "flagged in round 1, still open" when a bot or a human raised it first. It changes how the comment reads from a fresh opinion to an unclosed loop.
- Write nothing about work that is already fixed, and nothing that restates what the diff plainly does.

## Lenses

**Replay.** Every write and every state transition must survive running twice — a redelivered webhook, a retried job, a double-clicked button. Check what makes it idempotent and whether the key is genuinely unique. A transition that fires before the existence check, or that is reachable from a terminal state, undoes settled work on the second run.

**Silent fallback.** An unrecognised input degrading into a benign state — unknown status becomes pending, missing config becomes a default, a failed lookup becomes an empty list. It hides the upstream contract change it should have surfaced. Ask whether the quiet path was chosen or discovered.

**Trust boundary.** Anything reachable from outside: confirm the authorization check is present, that signatures are verified before the body is acted on, that input is validated, and that a new resource a client can touch has a matching rule wherever access is declared.

**Blast radius.** A script, migration, deploy task, or scheduled job named for one narrow change should not touch anything beyond it. Read what it actually loads or sweeps, not what its filename claims.

**Contract drift.** A validation or required field added here that a sibling PR in the stack must now satisfy; the same field name meaning two different things on two related models; a shared helper whose signature changed for one caller. Grep the other callers before believing the diff is self-contained.
