---
name: commit-messages
description: WHEN writing git/conventional commits; NOT for PR text; returns concise, why-first commit lines with proper type/scope.
---

# Commit Messages

Use this skill to generate clear, conventional commit messages that explain the "why" not just the "what". Follow this guide when writing commit messages or helping users structure their commits.

## When to Use

- User asks for help writing a commit message
- User wants to understand conventional commit format
- User needs to split a large commit into smaller ones
- User asks about commit best practices

## Philosophy

- **Why > What** - The diff shows what changed; the message explains why
- **Atomic commits** - One logical change per commit
- **Future readers** - Write for someone debugging at 2am in 6 months
- **Searchable** - Make it easy to find with `git log --grep`

## Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): subject

body (optional)

footer (optional)
```

## Types

| Type       | When to Use                                    | Example                               |
| ---------- | ---------------------------------------------- | ------------------------------------- |
| `feat`     | New feature for the user                       | `feat(auth): add password reset flow` |
| `fix`      | Bug fix for the user                           | `fix(cart): correct quantity calc`    |
| `docs`     | Documentation only changes                     | `docs: update API examples`           |
| `style`    | Formatting, white-space (not CSS)              | `style: format with biome`            |
| `refactor` | Code change that neither fixes nor adds        | `refactor: extract validation utils`  |
| `perf`     | Performance improvement                        | `perf: memoize expensive calculation` |
| `test`     | Adding or updating tests                       | `test: add auth integration tests`    |
| `build`    | Build system or dependencies                   | `build: upgrade to node 22`           |
| `ci`       | CI configuration                               | `ci: add playwright to pipeline`      |
| `chore`    | Other changes that don't modify src/test files | `chore: update .gitignore`            |

## Rules

### Subject Line

| Rule                         | Good                                  | Bad                  |
| ---------------------------- | ------------------------------------- | -------------------- |
| Imperative mood              | `add user profile`                    | `added user profile` |
| No capitalization            | `fix login bug`                       | `Fix login bug`      |
| No period                    | `update readme`                       | `update readme.`     |
| Be specific                  | `fix redirect loop on session expiry` | `fix bug`            |
| Max 50 chars (72 hard limit) | Keep it concise                       | Don't write essays   |

### Scope (optional)

- Component or area: `feat(auth):`, `fix(api):`, `test(cart):`
- Keep consistent within project
- Omit if change spans multiple areas

### Body (when needed)

- Wrap at 72 characters
- Explain **why** this change was necessary
- Include context that isn't obvious from the diff
- Reference issues: `Fixes #123` or `Relates to #456`

### Breaking Changes

```
feat(api)!: change authentication endpoint

BREAKING CHANGE: /auth/login now requires email instead of username.
Migration: Update all clients to send email field.
```

## Commit Scope Assessment

Before writing the message, assess whether the staged changes should be one commit or multiple.

### Signs to Split

| Signal                      | Action                       |
| --------------------------- | ---------------------------- |
| Changes to unrelated files  | Split by feature/area        |
| Multiple types (feat + fix) | Separate commits             |
| "and" in your subject line  | Probably two commits         |
| > 10 files changed          | Consider splitting           |
| Mix of refactor + feature   | Refactor first, then feature |

### Good Split Example

Instead of:

```
feat: add user profile and fix login redirect and update tests
```

Split into:

```
fix(auth): prevent redirect loop on session expiry
feat(profile): add user profile page
test(auth): add session expiry tests
```

## Examples

### Good

```
feat(cart): add quantity selector to cart items

Allow users to update item quantities directly from the cart
instead of navigating back to the product page.

Closes #234
```

```
fix(auth): prevent redirect loop on expired session

Session expiry was triggering a redirect to login, which then
redirected back to the protected route, causing an infinite loop.

Now we clear the redirect URL when session expires.
```

```
refactor: extract validation logic to shared utilities

Consolidates duplicate Zod schemas from three API routes into
a single source of truth in lib/validation.

No behavior changes.
```

```
perf(search): debounce search input to reduce API calls

Search was firing on every keystroke, causing 10+ requests
for a typical query. Now waits 300ms after typing stops.

Reduces search API calls by ~80% based on local testing.
```

### Bad

| Message                 | Problem                 |
| ----------------------- | ----------------------- |
| `fixed stuff`           | Too vague - what stuff? |
| `Updated the code`      | Obvious - adds no value |
| `WIP`                   | Not ready to commit     |
| `fix: Fix the bug`      | Redundant, no detail    |
| `misc changes`          | Meaningless             |
| `feat: add new feature` | What feature?           |
| `refactor code`         | What code? Why?         |

## Output Format

When generating commit messages, provide the complete message ready to use:

```
type(scope): clear subject line

Optional body explaining the motivation for this change.
Include context that helps future readers understand why
this was done, not just what was done.

Fixes #123
```

If the commit should be split, recommend splitting with specific guidance:

```markdown
**Recommendation: Split this commit**

The staged changes include multiple unrelated changes:

1. [Change type 1] - [files affected]
2. [Change type 2] - [files affected]

**Suggested commits:**

1. First commit:
```

type(scope): first change

```

2. Second commit:
```

type(scope): second change

```

**To split:** Use `git reset HEAD` then stage files for each commit separately.
```
