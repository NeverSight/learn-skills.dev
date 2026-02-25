---
name: conventional-commits
description: "Writes and reviews Conventional Commits commit messages (v1.0.0) to support semantic versioning and automated changelogs. Use when drafting git commit messages, PR titles, release notes, or when enforcing a conventional commit format (type(scope): subject, BREAKING CHANGE, footers, revert)."
---

# Conventional Commits (v1.0.0)

Use the Conventional Commits spec to produce consistent commit messages that are easy to parse for changelogs and semantic versioning.

## Commit message format (canonical)

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

Rules:

- Separate **header**, **body**, **footers** with a blank line.
- Keep the **header** on one line.
- Put `!` immediately before `:` to mark a breaking change (e.g. `feat!: ...`, `refactor(api)!: ...`).

## Choose a type

The spec allows any type, but these are common and widely supported by tooling:

- `feat`: introduce a new feature (user-facing)
- `fix`: bug fix (user-facing)
- `docs`: documentation-only changes
- `refactor`: refactor that neither fixes a bug nor adds a feature
- `perf`: performance improvement
- `test`: add or adjust tests
- `build`: build system/dependencies
- `ci`: CI configuration/scripts
- `chore`: maintenance tasks
- `style`: formatting (whitespace, missing semicolons, etc.)
- `revert`: revert a previous commit

Default choice when unsure:

- If users see new behavior → `feat`
- If users see corrected behavior → `fix`
- Otherwise → `chore` or a more specific maintenance type (`refactor`, `build`, `ci`)

## Optional scope

Use scope to clarify the area impacted.

Format:

```text
type(scope): description
```

Guidelines:

- Use a short noun: `api`, `auth`, `ui`, `db`, `cli`, `deps`, `docs`.
- Use repo/module/package name when working in a monorepo.
- If scope adds no clarity, omit it.

## Description (subject)

Write the description as a short summary of what the change does.

Guidelines:

- Use **imperative** mood: “add”, “fix”, “remove”, “update”.
- Avoid ending punctuation.
- Be specific; avoid “stuff”, “changes”, “update things”.

Examples:

```text
feat(auth): add passwordless login
fix(api): handle empty pagination cursor
chore(deps): bump react to 18.3.0
```

## Body (optional)

Use the body to explain motivation, constraints, or high-level implementation notes.

Guidelines:

- Prefer complete sentences.
- If helpful, include:
  - why the change was needed
  - what approach was chosen
  - notable trade-offs

Example:

```text
refactor(parser): simplify tokenization

Replace the regex pipeline with a small state machine to reduce backtracking.
```

## Footers (optional)

Footers are key/value-like lines at the end. Use them for:

- breaking change details
- issue references
- metadata used by tooling

Examples:

```text
Refs: #123
Closes: #456
Co-authored-by: Name <email@example.com>
```

## Breaking changes

Mark breaking changes in one (or both) of these ways:

1. Add `!` in the header:

```text
feat(api)!: remove deprecated v1 endpoints
```

2. Add a `BREAKING CHANGE:` footer (recommended when you need an explanation):

```text
feat(api): remove deprecated v1 endpoints

BREAKING CHANGE: /v1/* endpoints are removed; migrate to /v2/*.
```

## Reverts

Use the `revert` type when undoing a previous change.

Example:

```text
revert: feat(auth): add passwordless login

This reverts commit 1a2b3c4.
```

## Semantic versioning mapping (typical)

Common mapping for automated version bumps:

- `fix` → patch
- `feat` → minor
- any breaking change (`!` or `BREAKING CHANGE:`) → major

## When asked to “write a commit message”

Collect missing inputs quickly:

- What changed? (1–2 sentences)
- Scope/module? (optional)
- User-facing? (feature vs fix vs chore)
- Breaking? (yes/no; migration note if yes)
- Any issue IDs to reference?

Then produce:

1. A conventional header
2. Optional body (only if it adds clarity)
3. Optional footers (`Refs:`, `Closes:`, `BREAKING CHANGE:`)

## Ready-to-use templates

Minimal:

```text
<type>: <description>
```

With scope:

```text
<type>(<scope>): <description>
```

Breaking change with explanation:

```text
<type>(<scope>): <description>

BREAKING CHANGE: <what breaks and how to migrate>
```
