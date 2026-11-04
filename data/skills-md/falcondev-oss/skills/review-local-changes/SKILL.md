---
name: review-local-changes
description: Review the local changes cold and report the findings to the user.
disable-model-invocation: true
---

# Review Local Changes

Review the local changes and report to the user. Completion is the report.

The **local changes** are everything in the working tree that the default branch lacks: commits since the merge-base with the default branch, plus staged, unstaged, and untracked files. Review them all, whichever session made them.

## 1. Review cold

Dispatch `$code-review`, `$simplicity-review` and `$bug-review` in parallel as subagents, each handed the diff of the local changes and nothing else.

One cold round. Treat findings as hypotheses:

1. Verify each finding against the diff and current code.
2. Fix every valid, in-scope finding.
3. Record false positives and out-of-scope findings, leaving the change as it stands.
4. Re-run the checks your fixes touched, and re-review the fixes alone.

## 2. Report to the user

Open with a simple explanation of the problem the local changes solve, then briefly explain the solution. Do not lead with an implementation inventory:

BAD

> ❌ Removed implicit workspace carry-over from every "new thread" entry point (cmd+n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads inherit only the project from context; branch, worktree, and env mode always come from the configured defaults. Delete buildContextualThreadOptions, startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.

GOOD

> ✅ My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

Use the applicable sections from this structure in this exact order. Replace every placeholder and omit sections that have no content:

```markdown
## 📝 Summary

<Explain the problem, then the solution in plain language. This should be short, concise, and human-readable.>

## 📦 Changes

- <Name user visible and main area changes>

## ✅ Verification

- `<command>`: <result>

## 🔍 Reviews

| Review   | Found   | Fixed   |
| -------- | ------- | ------- |
| <review> | <count> | <count> |

<Tell the user what you changed during the review loop>

- <Every finding with its verdict: fixed, false positive, or out of scope, and why.>

## ⚠️ Needs attention

<List follow-up work, known limitations, or other issues that need the user's attention.>
```

List every review that ran, including reviews that found nothing. Never claim a check or review ran unless it did.
