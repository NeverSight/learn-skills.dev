---
name: commit-without-issue
description: Commit changes without an issue reference.
metadata:
  type: command
  invocation: skill-callable
  applies-to: [commits, git, no-issue-tracker]
---

# Commit Without Issue

Commit the changes. Follow the [`git-and-github`](https://github.com/mtngtools/agents/blob/main/rules/git-and-github.md) rule for commit message conventions, but omit the issue reference since this repo doesn't track issues:

- **Format:** `type(scope): subject` — Conventional Commits (no `#issue-number`)
- **Body:** Describe the change and its rationale
- **Breaking changes:** Use `BREAKING CHANGE` or `!` after type/scope if applicable

Example:
```
refactor: simplify config loading

Streamline the configuration parsing to reduce dependencies
and improve startup time.
```

Since there's no issue to close or reference, focus the commit message on clearly explaining what changed and why.
