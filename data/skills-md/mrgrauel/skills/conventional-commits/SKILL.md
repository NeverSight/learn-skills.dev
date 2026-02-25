---
name: conventional-commits
description: Draft and validate Git commit messages that follow Conventional Commits v1.0.0. Use when creating, rewriting, or reviewing commit messages for `git commit`, `git commit --amend`, PR cleanup, or release/changelog automation that depends on conventional commit types.
---

# Conventional Commits

## Goal

Produce commit messages in this canonical shape:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Workflow

1. Inspect staged changes with `git status --short` and `git diff --staged`.
2. Summarize the change in one sentence before writing the message.
3. Choose exactly one primary type:
   - `feat`: add user-facing behavior
   - `fix`: correct a bug
   - `docs`: change documentation only
   - `style`: change formatting only, no behavior
   - `refactor`: change structure without feature or bug fix
   - `perf`: improve performance
   - `test`: add or update tests only
   - `build`: change build system or dependencies
   - `ci`: change CI/CD config
   - `chore`: maintenance work with no user-facing behavior
   - `revert`: revert a previous commit
4. Add optional scope when it improves precision (`auth`, `api`, `ui`, `deps`).
5. Write the description as an imperative phrase (`add`, `fix`, `remove`), concise and specific, with no trailing period.
6. Mark breaking changes by adding `!` and a footer:
   - Header example: `feat(api)!: rename session token field`
   - Footer: `BREAKING CHANGE: sessionToken was renamed to authToken`
7. Add body only when useful to explain intent, constraints, or tradeoffs.
8. Add footer trailers for references when needed (`Refs: #123`, `Closes: #456`).

## Validation Rules

Reject and rewrite any message that:

- misses the `type: description` shape
- omits the required `: ` separator
- uses vague descriptions (`update stuff`, `misc changes`)
- mixes multiple unrelated changes in one commit
- declares a breaking change without `!` and `BREAKING CHANGE:`

## Output Contract

When asked to draft a commit message:

1. Return a final, copy-ready commit message block.
2. Return one short line explaining the selected type (and scope, if used).
3. Ask one focused clarification only when the change intent is ambiguous.
