---
name: bug-review
description: Cold review of a diff for merge-blocking bugs, each with a way to demonstrate the failure. Use when asked to find bugs in a branch, PR or local changes, or when another skill dispatches a correctness review.
---

# Bug review

Review the diff you were handed, with its contract or ticket if one came along. When you compute the diff yourself, run `git fetch origin <base>` and diff against `origin/<base>`: a local base branch can lag the remote and pull unrelated commits in.

Correctness is your only axis. Read the changed code, its callers and its tests; coding standards and style docs belong to the other reviews. Report only issues that block merging: wrong behavior, data loss, permission or tenant holes, races, broken error paths, type holes that reach runtime.

For each issue:

- `file:line`
- why it is wrong, in one or two sentences
- how to demonstrate the failure: the input and steps, or a sketch of a test that goes red

Mark every issue you suspect but couldn't confirm, and say where you looked. If nothing blocks merging, say so in one line.

Leave the working tree as you found it: someone else is building in it. Write any repro or demo test outside the repo (under `$TMPDIR`), or delete it before reporting. The report carries the test sketch.

Completion: every changed hunk read, every reported issue carries all three parts, and `git status` matches what it showed when you started.
