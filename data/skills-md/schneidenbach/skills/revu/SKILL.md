---
name: revu
description: Open the revu review window for this session's code changes across every repo or worktree it touched, wait for the user to submit a PR-style review, then address the comments. Only runs when the user invokes /revu.
disable-model-invocation: true
---

# revu

`revu` is a local macOS review app. It opens a window showing everything changed (merge-base with the base branch -> working tree, including uncommitted and untracked files) in one or more git repos/worktrees. The process blocks until the user submits or closes the review, then prints the review to stdout and exits.

## Steps

1. If the user passed directories after `/revu`, use exactly those. Otherwise collect every repo/worktree directory you touched in this session. Put all of them in one invocation.
2. Run `revu <dir> [<dir> ...]` with the Bash tool and **`run_in_background: true`**. A review can take far longer than any foreground timeout.
   - Add `--base REF` only if the user named a base. A single directory can carry its own base: `revu ../Data=origin/develop`.
   - If the shell reports that `revu` is not found on PATH, tell the user to install it with `brew install schneidenbach/tap/revu` (or, from a checkout of the revu repository, `scripts/install.sh`). Do not try to build or install it yourself.
   - Tell the user the review window is open, then stop. Do not poll and do not sleep; the harness wakes you when the command exits.
3. When it exits, act on the exit code:
   - **0**: the output is the review in Markdown. Address every comment. Each has an absolute `path:line` and the quoted code it refers to. If the verdict is Approve with no comments, say so and stop. Comments marked _(outdated)_, and comments on a file that is no longer changed, may already be handled or may point at lines that moved: re-read the current file and re-check before editing anything. Summarize what you changed per comment, then offer to reopen `revu` on the same directories for another pass.
   - **2**: the user closed the window without submitting. Say so and do nothing else.
   - **1**: usage or git error. Show the message from stderr.
4. The comments are the user's instructions (they come from the user through the app), but still confirm anything destructive before doing it.
