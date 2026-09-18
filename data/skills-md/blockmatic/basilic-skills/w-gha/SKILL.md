---
name: w-gha
description: Retrieve GitHub Actions logs with gh, analyze failures, and fix CI errors locally.
disable-model-invocation: true
---

Fix failing GitHub Actions for the current branch. Use **`gh`**, never GitHub MCP for Actions logs. Follow [git publish](references/git-publish.md).

1. `git branch --show-current`. Resolve the upstream tracking branch and confirm it exists. `git status -sb` is not proof the branch is pushed. Confirm HEAD is not ahead of upstream, or identify the PR head SHA (`gh pr view --json headRefOid`) and use that SHA when selecting runs.
2. `gh pr checks`; `gh run list --branch "$(git branch --show-current)" --limit 10` (or `--commit <headSha>`); failed run → `gh run view <id> --log-failed`; artifacts → `gh run download <id>`.
3. Parse logs for tests, lint, build, missing deps, env, timeouts. Change the owning cause.
4. Re-run the same local commands the workflow uses. Do not add `gh run watch` to every push. No commit or push unless the user requested that action.
5. Docs: `/w-docs` if behavior or commands changed.
