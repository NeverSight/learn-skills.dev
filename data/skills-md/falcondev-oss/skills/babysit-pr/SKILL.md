---
name: babysit-pr
description: Monitor a pull request through review and CI. Use when the user asks you to monitor, watch or babysit a PR.
---

# Babysit PR

Wait on events, not the clock. In T3 Code, call its `watch_pull_request` tool on the PR and end your turn: it wakes you when checks finish, comments arrive, or the branch falls behind. Only outside T3 Code, use your harness's own PR watcher the same way. Watcher events and subagent completion notifications are your only wake signals; schedule no timers, sleeps, wakeups or polling loops. Reserve a bare status read for the first look and the final confirmation.

When the PR is merge-ready or you hand back, stop the watcher: `unwatch_pull_request` in T3 Code, the harness's equivalent elsewhere.

Only act on checks and comments newer than the latest push. Verify every bot finding against the source before changing code. Fix real findings and CI failures, distinguish repository failures from infrastructure flakes, and reply with a written reason when dismissing false positives.

When the PR falls behind its base branch or conflicts with it, run `git fetch origin <base>` and merge `origin/<base>` into the PR branch (a local base branch can lag the remote), re-run the checks the merge affects, and push. Merging keeps every push a fast-forward; rewriting the pushed history needs the user's go-ahead.

If a review bot leaves feedback you believe is not worth addressing, reply and resolve the comment. Format comments left on the user's behalf as:

```
[MODEL-SLUG] RESPONDING ON BEHALF OF [USER NAME]

[actual reply]
```

Do not let review feedback expand the PR beyond the user's original goal.
Address real shortcomings, but avoid scope creep.

If nothing has changed, stay quiet rather than posting filler comments. Stop when the review bots and required checks are green on the latest commit.
Merge only when the user explicitly requested it; otherwise report that the PR is ready.
