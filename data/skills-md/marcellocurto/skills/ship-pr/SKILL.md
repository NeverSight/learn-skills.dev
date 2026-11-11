---
name: ship-pr
description: Implement a GitHub issue or the work agreed in the conversation as a pull request, then review it with independent agents, settle every review comment, and check each round of fixes before it is pushed. Use when the user asks to ship an issue or change end to end, or to build it and then babysit the PR. To only open the PR, use `implement-to-pr`.
---

# Ship PR

Run the `implement-to-pr` skill, then the `babysit-pr` skill, to build, open, independently review, and settle a PR, checking fixes before each push. Never force-push or merge.

## 1. Build and open the PR

Follow `implement-to-pr` through opening the PR. Save its final response for the combined report. Wait if it needs a user answer.

## 2. Babysit

Run `babysit-pr` on the new PR. Supply the linked issue or full agreed request, all subsequent user-approved requirements, decisions, and exceptions (quoting user decisions verbatim), and validation results. It handles the first review, reviewer briefs, and agent and human feedback.

## Report

When `babysit-pr` finishes or stops, combine both skills' reports in this order, omitting empty parts:

```markdown
**PR:** the link, and one sentence on what it does.

**Status:** done, or why babysitting stopped, with the head commit and the number of rounds.

**Screenshots:** for UI changes, embed checked screenshots as Markdown images with absolute local paths and captions. Show the head version after UI fixes.

**Couldn't verify:** each check or tool that didn't run, what it would have caught, what you did instead, and what to install to run it; each review lens that didn't cover part of the diff, with the files; and each finding no verifier answered.

**Judgment calls:** assumptions and decisions the issue or conversation didn't settle, and anywhere the work differs from what was asked.

**Review focus:** the one to three places in the final diff that need careful reading, and which parts are mechanical.

**Feedback:** each review finding, labeled with its lens, each fix-check finding, and each human comment, with its outcome: fixed (with the commit), rejected (with the reason), dropped before posting or fixing (with the reason), limit accepted (with where it is written down), or left open (with the decision needed). Quote any user decision used as counterevidence. For an architectural problem, name the root cause and the change you recommend.

**Noticed, not done:** the problems from `implement-to-pr`'s final response and `babysit-pr`'s follow-ups and noticed problems, as one list written the way the `code-review` skill writes Noticed items.

**Proposed rules:** the policy lines `babysit-pr` proposes for the repository's instructions, each as the line to add.
```

Never say all checks pass when some didn't run. Name what passed and what didn't run.
