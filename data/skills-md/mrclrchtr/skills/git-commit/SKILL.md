---
name: git-commit
description: "Create safe, repo-convention commits: inspect and stage changes, write a clear subject, add a body when useful, and commit."
---

# Git Commit

## Goal

Make one logical, reviewable commit using the repo's existing message style.

## Quick Workflow

1) Inspect repo state:

```bash
git branch --show-current
git status --porcelain=v1
git --no-pager diff
git --no-pager diff --staged
git --no-pager log --oneline -20 --graph
```

2) Do a quick safety scan:

```bash
rg -n "(AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key\\s*=|secret\\s*=|password\\s*=)" -S .
```

If anything looks sensitive, stop and ask the user what to do.

3) Stage changes intentionally (one logical change per commit):

```bash
git add path/to/file1 path/to/file2

git add -p
```

Use `git add -A` only when everything belongs in this commit.

4) Write the commit message:
- If the repo uses Conventional Commits, use `<type>(<scope>): <summary>`.
- Otherwise match the repo's existing format.
- Add a body when the diff is large or reviewer context matters.
- If you include literal backticks in a `git commit -m "..."` message, escape them as `\`` (otherwise zsh/bash will treat them as command substitution).

```text
type(scope): summary

Why this change was needed.
Key tradeoffs or constraints.
Notable side effects or follow-ups.
```

5) Commit and verify:

```bash
git commit -m "type(scope): summary"
git commit \
  -m "type(scope): summary" \
  -m "Why this change was needed and what constraints shaped it."
git --no-pager show --stat
```

## Guardrails

- Do not bypass hooks with `--no-verify` unless the user asks.
- Do not use history rewrite (`--amend`, rebase, force push) unless requested.
- If checks fail, fix and re-run the normal flow.
