---
name: commit
description: Use when the user wants to commit changes. Stages files, updates CHANGELOG.md, and creates a commit following project conventions.
---

You are making a git commit for this project. Follow these steps carefully.

## Setup

This skill includes a `commit-msg` git hook that enforces CHANGELOG.md updates on `feat:` and `fix:` commits. Run the setup script from the project root to check status and get install instructions:

```bash
scripts/setup.sh
```

## 1. Review changes

Run `git status` and `git diff` to understand what has changed.

## 2. Update CHANGELOG.md

The commit hook **requires** `CHANGELOG.md` to be staged for any `feat:` or `fix:` commit. Add a concise entry under `## [Unreleased]` describing the changes.

Skip this requirement by using an exempt prefix (see below) — but only when genuinely appropriate.

## 3. Write the commit message

Use the **Conventional Commits** format:

```
<type>(<optional scope>): <short description>

<optional body>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Types

| Type | When to use | Requires CHANGELOG? |
|------|-------------|-------------------|
| `feat:` | New feature or user-visible change | **Yes** |
| `fix:` | Bug fix | **Yes** |
| `chore:` | Maintenance, deps, config, tooling | No |
| `docs:` | Documentation only | No |
| `style:` | Formatting, whitespace | No |
| `test:` | Tests only | No |
| `ci:` | CI/CD changes | No |
| `build:` | Build system changes | No |
| `revert:` | Reverting a commit | No |

### Message rules
- Subject line: imperative mood, ≤72 chars, no period
- Be specific: describe *what* and *why*, not just *what*
- Use body for additional context if needed

## 4. Stage and commit

- Stage relevant files explicitly (avoid `git add -A` or `git add .` unless all changes should be included)
- Always include `CHANGELOG.md` in the staged files for `feat:`/`fix:` commits
- Pass the commit message via heredoc to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
feat: short description

Longer explanation if needed.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

## 5. Verify

Run `git status` after committing to confirm success.
