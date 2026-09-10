---
name: draft-commit-message
description: Draft a commit message following the organization's git and commit message guidelines.
metadata:
  type: command
  invocation: skill-callable
  applies-to: [commits, git, messages]
---

# Draft Commit Message

Draft a commit message for the current changes. Follow the commit message conventions in [`git-and-github`](https://github.com/mtngtools/agents/blob/main/rules/git-and-github.md) rule:

- **Format:** `type(scope): subject (#issue-number)` — Conventional Commits
- **Always include issue reference** on first line
- **Body:** Use GitHub keywords (`closes`, `addresses`, `refs`) with issue details
- **Breaking changes:** Use `BREAKING CHANGE` or `!` after type/scope
- **Multiple issues:** Comma-separated on first line, detailed at bottom

If drafting interactively with a human, ask clarifying questions about which issues are addressed, whether the change is breaking, and what type of commit this is (feat, fix, refactor, etc.).
