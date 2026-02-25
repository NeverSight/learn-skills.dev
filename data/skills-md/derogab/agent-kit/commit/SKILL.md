---
name: commit
description: Create a git commit following the Conventional Commits specification.
disable-model-invocation: true
allowed-tools: Bash(git diff:*) Bash(git branch:*) Bash(git log:*) Bash(git commit:*)
---

## Context

- Staged diff: !`git diff --staged`
- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Your task

Create a single git commit from the **staged changes only**.

### Pre-flight checks

1. If there are **no staged changes**, stop immediately and tell the user to stage files first. Do nothing else.
2. Never run `git add`. Never run `git push`. Only commit what is already staged.

### Commit message format

Follow Conventional Commits (`https://www.conventionalcommits.org/en/v1.0.0/`):

```
<type>(<optional scope>): <description>

[optional body]
```

**Types:**
- **feat** – new capability
- **fix** – bug fix
- **docs** – documentation only
- **refactor** – restructuring without functional change
- **test** – test creation or modification
- **chore** – routine maintenance (including dependencies)
- **build** – build system or external dependencies
- **perf** – performance improvement
- **ci** – CI/CD changes

Append `!` after the type/scope for breaking changes (e.g. `feat!: change API response format`).

### Rules

- Infer the correct type from the diff.
- Write a concise description (lowercase, imperative mood, no period).
- Add a body only when the diff is non-trivial and the "why" isn't obvious from the description.
- Body: wrap at 72 characters, explain **why** not what.
- Match the style and tone of the recent commits shown above.
- Use a HEREDOC to pass the message to `git commit -m`.
- Do not send any text besides the tool calls.
