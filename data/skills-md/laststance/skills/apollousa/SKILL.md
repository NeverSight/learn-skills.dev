---
name: apollousa
description: "Create a GitHub PR for completed work, then run coderabbit-resolver through review, CI, merge, and cleanup. Pass `cli` to put `@coderabbitai ignore` in the PR body and review with the CodeRabbit CLI instead of the GitHub bot. Use when: the user asks for PR creation followed by CodeRabbit resolution. Keywords: create PR, CodeRabbit, merge, CLI, @coderabbitai ignore."
argument-hint: "[base-branch] [cli]"
---

# Apollousa

Create the PR, then hand it directly to `coderabbit-resolver`.

Parse arguments: `cli` / `--cli` is the CLI-mode flag; any other token is the base branch (`/apollousa`, `/apollousa cli`, `/apollousa develop`, `/apollousa develop cli`). `cli` is never a branch name.

1. Read the repository instructions and verify `pwd`, Git status, current branch, default branch, remote, and existing PR state.
2. Run the repository's required validation before pushing. Never push a broken or dirty result.
3. If currently on the default branch, create a descriptive feature branch at the completed commit. Otherwise reuse the current feature branch.
4. Push the feature branch and create a non-draft PR with a concise summary and test plan. Reuse an existing PR for the branch instead of duplicating it.
   - **`cli` mode:** put `@coderabbitai ignore` on its own line in the PR **description** (create body, or `ensure-cli-ignore.sh` / `gh pr edit` when reusing a PR). A comment does not disable the bot. Keep the line.
5. Invoke the installed `coderabbit-resolver` skill with the PR number and follow its single-PR workflow through CodeRabbit findings, CI, merge, and branch cleanup.
   - **`cli` mode:** pass `cli` as well (`/coderabbit-resolver <n> cli`) so the resolver reviews with the CodeRabbit CLI and does not trigger the GitHub bot.
6. Report the PR URL, merge result, final checks, and clean local branch state.

Do not stop after PR creation. Completion means the invoked `coderabbit-resolver` workflow has reached its own success criteria or reported a genuine blocker.
