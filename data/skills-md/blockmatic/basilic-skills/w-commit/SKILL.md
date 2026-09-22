---
name: w-commit
description: Review and commit the task's intended changes using repository conventions.
disable-model-invocation: true
---

Invocation requests a commit. Inspect staged and unstaged changes and the authorized task scope before staging anything. Follow [git publish](references/git-publish.md).

1. If creating a new branch, `git fetch origin` then `git switch -c <name> --no-track origin/main` first — never skip fetch, never a stale local `main`. Inspect the diff and distinguish task-owned changes from unrelated work, including pre-staged files. If the intended commit cannot be separated safely, clarify the file scope.
2. Before staging: if behavior, commands, or conventions changed, matching MDX and nearest README must be in the diff; otherwise one line why not. Rely on commit hooks. Never the full pre-push suite.
3. Stage explicit task-owned paths or hunks. Do not sweep unrelated or untracked work into the commit with a blanket add. Never `git add -A`. Never stage `.env`, credentials, or secrets.
4. Write a Conventional Commit: lowercase type/scope, imperative summary of at most 60 characters, no period. Follow repository-specific scope conventions. Pass the message via a heredoc; commit with hooks enabled.
5. Inspect the result and remaining working tree. Return commit ID and scope. A commit request alone does not authorize pushing.
