---
name: conventional-commits
description: Write git commit messages following Conventional Commits v1.0.0. Use when committing changes, choosing commit types, or indicating breaking changes.
---

# Conventional Commits

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | When to use | SemVer |
|------|-------------|--------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation only | — |
| `refactor` | Code change, no feature/fix | — |
| `test` | Adding or updating tests | — |
| `chore` | Maintenance, config, dependencies | — |
| `perf` | Performance improvement | — |
| `ci` | CI/CD changes | — |
| `build` | Build system changes | — |
| `style` | Formatting, whitespace | — |
| `revert` | Reverts a previous commit | — |

## Scope

Use the **slice name** as scope: `feat(user): add user CRUD functionality`

Common scopes: slice names (`user`, `auth`, `project`), infrastructure (`api`, `prisma`, `theme`), or omit for cross-cutting changes.

## Rules

- Description: imperative, present tense ("add" not "added")
- No capital first letter
- No period at end
- Keep header under 72 characters
- Body starts with blank line after description
- Footers start with blank line after body

## Breaking Changes

Add `!` before the colon, or use a `BREAKING CHANGE:` footer (or both):

```
feat!: remove support for Node 6
```

```
feat: change config format

BREAKING CHANGE: `extends` key now works differently
```

Breaking changes always trigger a MAJOR version bump.

## Examples

```
feat(user): add user CRUD functionality
```

```
fix(auth): handle token expiration correctly
```

```
refactor(project): extract validation into service
```

```
feat(api): add pagination to list endpoints

Support cursor-based pagination for all collection endpoints.
Default page size is 20 items.

Refs: #123
```

```
chore: update dependencies
```
