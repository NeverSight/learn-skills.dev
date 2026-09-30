---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets on a separate worktree, based off of the current branch.

## Claim the issue first

Before editing any files, claim the issue you are implementing so a colliding agent skips it (see `docs/agents/triage-labels.md`). If the work maps to an issue number `N`:

**First, check for an existing claim** with `gh issue view N --json labels,comments`. If `in-progress` is already set, another agent may be on it: read the latest `🤖 in-progress` comment, inspect *that branch's* real state (open PR? commits? or an empty/abandoned branch?), and skip or coordinate instead of duplicating. Claim only if the issue is free, or the prior claim is clearly abandoned (no open linked PR, the reaper's rule).

Then claim:

```
gh issue edit N --add-label in-progress --remove-label ready-for-agent
gh issue comment N --body "🤖 in-progress: <branch> (<session>) <date>"
```

Idempotent: re-running `/implement` on the same issue must not error: adding a present label, dropping an absent `ready-for-agent`, and re-commenting are all tolerated. The claim comment must name the working branch (a colliding agent inspects that branch's state, not a lingering worktree).

## Release the claim

When you open the PR (work handed to review), release the claim: `gh issue edit N --remove-label in-progress`. If the flow ends without opening a PR, leave the label; the `cleanup-merged-branches` reaper releases abandoned claims. Do not restore `ready-for-agent` on success; the issue closes on merge.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.

Close any Chrome tabs you opened during this session before creating the PR.
