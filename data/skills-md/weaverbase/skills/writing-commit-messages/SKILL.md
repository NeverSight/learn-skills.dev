---
name: writing-commit-messages
description: Use when writing, amending, or reviewing git commit messages, including before running git commit.
---

# Writing Commit Messages

## Overview

Write commit messages that explain one coherent change and why it was needed.

**Core principle:** Follow repository conventions first; use these defaults when the repository does not specify its own.

## Format

Use this format:

```text
<type>(<optional scope>): <short description>

[optional body]

[optional footer(s)]
```

## Types

| Type | Use for |
| --- | --- |
| `feat` | Add a feature. |
| `fix` | Fix a bug. |
| `refactor` | Restructure code without changing behavior. |
| `perf` | Improve performance. |
| `docs` | Change documentation. |
| `test` | Add or change tests. |
| `build` | Change the build system or dependencies. |
| `ci` | Change continuous integration configuration or scripts. |
| `chore` | Perform maintenance not covered by the other types. |
| `revert` | Revert an earlier commit. |

## Subject

- Use imperative mood: "add", "fix", or "remove", not "added" or "fixed".
- Use lowercase after the colon.
- Do not add a trailing period.
- Keep the subject to about 72 characters or fewer.

## Scope

The scope is optional. Use a short module or area name taken from the repository, such as a directory, package, or scope already used in its history; do not invent one. Omit it when no single area applies.

## Body

Separate the body from the subject with a blank line. Explain why the change was needed and what changed, wrapping lines at about 72 characters.

## Breaking Changes

Put `!` after the type or scope, such as `feat!:` or `feat(api)!:`, and add a `BREAKING CHANGE:` footer describing the impact on callers.

```text
feat(api)!: remove v1 order endpoints

BREAKING CHANGE: clients must use the v2 order endpoints instead of v1.
```

## Precedence

Repository conventions win over these defaults. Check existing history, `CONTRIBUTING`, and commitlint configuration before writing a message.

## Example

Good:

```text
fix(auth): reject expired refresh tokens

Compare the current time with the expiry claim instead of the issue
time. This prevents expired refresh tokens from creating new sessions.
```

Bad:

```text
fix: Fixed bugs and updated docs.
```

The subject is vague, uses past tense and a capital letter, ends with a period, and bundles unrelated changes.

## Red Flags

Stop and rewrite the message if you see:

- A vague subject such as `fix: stuff`.
- A past tense subject.
- Several unrelated changes in one commit.
- An invented scope rather than a repository module or area.
- A breaking change without `!` or a `BREAKING CHANGE:` footer.
- A body that repeats the diff without explaining why.
- Repository conventions ignored in favor of these defaults.
