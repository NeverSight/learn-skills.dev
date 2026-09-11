---
name: conventionalcommits
description: How to write Conventional Commits (v1.0.0 spec, https://www.conventionalcommits.org/en/v1.0.0/) - project-agnostic. Covers the type(scope) message grammar, the type vocabulary, how BREAKING CHANGE is expressed, and how this maps directly to SemVer bumps. Use when writing a commit message, setting up commit-lint tooling, or reviewing commit history for a release.
---

# Conventional Commits

A commit message that a machine (and a future human) can actually parse
— the spec at
[conventionalcommits.org/en/v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## The grammar

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

```
feat(auth): add OAuth2 refresh-token support

Refresh tokens are now requested alongside the access token and
persisted so a session survives past the access token's expiry
without forcing a re-login.

Refs: #482
```

## The load-bearing types

Only two types carry spec-mandated meaning — everything else is
convention, not requirement:

| Type | Meaning | SemVer bump |
|---|---|---|
| `fix` | A bug patch | `PATCH` |
| `feat` | A new feature | `MINOR` |

A `!` right before the `:` (or a `BREAKING CHANGE:` footer, below) on
**any** type — `fix!`, `feat!`, `refactor!` — forces `MAJOR`, regardless
of which type it's attached to.

**Other widely-used types** (not spec-mandated, but standard
enough to treat as one vocabulary, not invent your own per-project):
`build`, `chore`, `ci`, `docs`, `perf`, `refactor`, `revert`, `style`,
`test`. None of these bump the version on their own.

## Scope

Optional, in parentheses right after the type — names the part of
the codebase affected: `feat(parser): ...`, `fix(cli): ...`. Keep it to
an existing subsystem name, not a made-up one per commit.

## Breaking changes — two ways to say it

```
feat!: remove support for Node 16
```
or
```
feat: add streaming response support

BREAKING CHANGE: the `onData` callback signature changed from
`(chunk: string) => void` to `(chunk: Buffer) => void`.
```
`BREAKING CHANGE` (or the synonym `BREAKING-CHANGE`) is the one footer
token that **must** be uppercase — everything else in the spec is
case-insensitive. State the concrete thing that breaks (a
signature, a removed flag, a changed default) — "various breaking
changes" tells a reader nothing they can act on.

## Footers

One blank line after the body, `Token: value` or `Token #value` per
line — the same shape git already uses for `Signed-off-by:`:
```
Reviewed-by: jane-doe
Refs: #482
```

## Rules worth remembering

- The description must immediately follow `type(scope):` on the same
  line, and should read as a present-tense instruction ("add X",
  not "added X" or "adds X") — matches how `git log --oneline` reads
  best.
- A body, if present, starts one blank line after the description
  — free-form prose explaining *why*, not restating *what* the diff
  already shows.
- This only constrains the **commit message**, not commit granularity —
  one logical change per commit is still a separate, good practice
  this spec doesn't itself enforce.

## Why this matters beyond readability

`feat`/`fix`/`!` map directly onto [SemVer](../semver/SKILL.md)'s
MAJOR/MINOR/PATCH — a changelog-generation or release-automation
tool can compute the next version number **from commit history
alone**, and a [Keep a Changelog](../keepachangelog/SKILL.md) entry can
be drafted from the same commit messages, if they're written this
way consistently. The payoff only shows up with consistency — a
history that's half-conventional, half-freeform gives tooling nothing
reliable to parse.
