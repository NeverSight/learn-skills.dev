---
name: commit
description: Use this skill when an agent needs to prepare a focused commit, follow repository commit-message conventions, write a clear commit message, and create the git commit cleanly.
---

# Commit Skill

Use this skill when the work is already implemented and the next step is to create a clean git commit.

## Goals

- Keep the commit scoped to the intended change
- Write a concise, descriptive commit message
- Avoid including unrelated modified files

## Workflow

1. Inspect the working tree before committing.
2. Confirm which files belong to the requested change.
3. Detect the repository's commit-message rules and style.
4. Stage only the relevant files.
5. Write a commit message that follows the detected style and summarizes the
   user-visible change.
6. Create the commit without rewriting unrelated history.

## Commit Message Style

Before writing the message, check for explicit rules in repository instructions
such as `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, pull request templates,
package scripts, or commitlint configuration. Explicit project or user rules
override history.

If no explicit rule exists, inspect recent commits:

```bash
git log --format=%s -n 20
git log --format=%B -n 5
```

Use the dominant style from relevant recent history:

- **Conventional commits:** use `type(scope): subject` or `type: subject` when
  recent history uses prefixes such as `feat:`, `fix:`, `docs:`, `chore:`,
  `ci:`, `refactor:`, or scoped variants.
- **Simple subjects:** use a concise imperative subject such as
  `Update skill validation workflow` when history uses plain sentence-style
  commit subjects.
- **Multiline commits:** include a blank line and body when recent non-merge
  commits commonly include bodies, when the change needs context, or when the
  user asks for references/explanations. Keep the subject aligned with the
  detected subject style.
- **Mixed history:** prefer the style used by recent commits touching the same
  area. Do not imitate merge commits.

## Guidelines

- Respect what the user already staged: inspect `git diff --cached` before staging anything, treat pre-staged content as intentional, and do not unstage it unless it clearly does not belong to the requested change — call that out instead.
- If a pre-commit hook fails, fix the reported problem and retry the commit. If a hook rewrites files, restage only the hook-modified files and commit again. Do not bypass hooks with `--no-verify` unless the user explicitly asks.
- Do not stage unrelated files just to make the tree clean.
- Prefer one focused commit over a mixed commit.
- Use imperative subjects unless the repository's explicit rules or dominant
  history use another style.
- If the tree contains unexpected changes, call them out before committing.
- Do not amend existing commits unless explicitly requested.
