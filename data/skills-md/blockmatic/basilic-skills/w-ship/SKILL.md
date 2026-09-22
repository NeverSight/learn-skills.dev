---
name: w-ship
description: Implement the requested change, validate, commit, push, and create its PR.
disable-model-invocation: true
---

Invocation requests the complete implementation-to-PR path, not a lone commit (`/w-commit`) and not merge or deploy. Read the task or plan, repository instructions, branch state, affected docs, and scripts. Follow [git publish](references/git-publish.md). Do not open a child SKILL.md unless that Git step is blocked.

1. Follow git-publish branch rules. Dirty tree stops (no stash). Every new branch: `git fetch origin` then `git switch -c <name> --no-track origin/main` — never skip fetch, never a stale local `main`.
2. Implement in complete slices. Docs as `/w-build`: matching MDX and nearest README when behavior/commands/conventions changed, or one line why not.
3. Run the repository's full pre-push gate (`pnpm qa` in Basilic, or the consuming repo's documented equivalent). This is the only playbook that requires that gate. Diagnose failures before publishing.
4. Commit task-owned changes, then push the inspected upstream.
5. Create or update the PR. Return commit, branch, PR link, and checks. If a gate fails, report the blocker and completed local work; do not present an unpublished change as shipped.
