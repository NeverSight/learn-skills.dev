---
name: git-commit
description: "Commit changes with an emphasis on tidiness and reviewability: small, focused commits, with clear rationale in messages."
---

# Git Commit

Use this skill as the playbook for producing reviewable commits and a clean, consistent commit history.

## Phase 1: Review changes

1. Check what files have changed
2. If there are no changes to commit, inform the user and stop
3. If there are unstaged changes, stage them with `git add`

Rules:

- Keep commits small, focused, and atomic
- Avoid commits that mix unrelated changes (e.g., "Address feedback")
- Never stage or commit files that look like secrets (e.g. `.env`, credentials, API keys)

## Phase 2: Generate commit message

1. Remember commit messages best practices
2. Write a short subject line:
   - Up to 50 chars
   - Start subject with a capital letter, don’t end with a period
   - Use imperative mood (e.g. "Fix memory leak while scrolling widget")
3. Leave a blank line between subject and body
4. Only when needed (don’t force it for trivial changes), write a body:
   - Wrap lines at 72 chars
   - Focus on "what" and "why", not the "how"
     - Explain the motivation
     - Mention side effects, trade-offs, or alternatives considered
     - Reference relevant issue IDs / tickets at the bottom if known
5. Check style of recent commits in the repo (tone, structure, capitalization, length, etc): `git log -10 --oneline`
6. Generate a message that adheres to the style in the repo while following best practices

Rules:

- Never stage files that look like secrets (e.g. `.env`, credentials, API keys)
- Do not add yourself as an author or contributor
- Do not include "Generated with ...", "Co-Authored-By: ...", or any AI attribution

## Phase 3: Commit

1. Commit staged changes with `git commit`

Rules:

- Avoid `git commit --amend` unless explicitly requested
- Do not bypass hooks with `git commit --no-verify`
  - If `git commit` fails due to hooks, fix issues and retry
- Use `git commit -F` (or heredoc) when there is a body, never newline escapes in `-m`.
- Never push to remotes unless explicitly requested
