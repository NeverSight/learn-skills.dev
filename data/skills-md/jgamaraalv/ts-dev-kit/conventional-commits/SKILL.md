---
name: conventional-commits
description: "Write, review, and validate commit messages following the Conventional Commits v1.0.0 specification. Use when: (1) crafting a git commit message for any change, (2) reviewing or correcting an existing commit message, (3) choosing the right commit type for a change, (4) deciding how to mark a breaking change, (5) writing multi-line commits with body and footers, or (6) understanding how commits map to SemVer bumps (PATCH/MINOR/MAJOR). Covers all standard types: feat, fix, docs, chore, refactor, perf, test, build, ci, style, revert."
---

## Table of Contents

- [Format](#format)
- [Types and SemVer impact](#types-and-semver-impact)
- [Breaking changes](#breaking-changes)
- [Examples](#examples)
- [Non-obvious rules](#non-obvious-rules)
- [Choosing the right type](#choosing-the-right-type)
- [SemVer cheatsheet](#semver-cheatsheet)

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

- **type**: lowercase noun (see table below)
- **scope**: optional noun in parentheses describing the affected section, e.g. `feat(auth):`
- **description**: imperative, present tense, no period at end, immediately after `": "`
- **body**: free-form; begins one blank line after description
- **footers**: one blank line after body; follow git trailer format (`Token: value` or `Token #value`)

## Types and SemVer impact

| Type       | Use for                                      | SemVer |
| ---------- | -------------------------------------------- | ------ |
| `feat`     | New feature                                  | MINOR  |
| `fix`      | Bug fix                                      | PATCH  |
| `docs`     | Documentation only                           | none   |
| `style`    | Formatting, whitespace (no logic change)     | none   |
| `refactor` | Code restructure (not a fix or feature)      | none   |
| `perf`     | Performance improvement                      | none   |
| `test`     | Adding or fixing tests                       | none   |
| `build`    | Build system, dependencies (npm, gradle…)    | none   |
| `ci`       | CI configuration (GitHub Actions, CircleCI…) | none   |
| `chore`    | Maintenance not fitting above types          | none   |
| `revert`   | Reverts a previous commit                    | none   |

Any type + `BREAKING CHANGE` → **MAJOR**.

## Breaking changes

Two ways to signal a breaking change (can combine both):

**1. `!` after type/scope** (visible at a glance):

```
feat(api)!: remove deprecated v1 endpoints
```

**2. `BREAKING CHANGE:` footer** (required if you need a description):

```
feat: allow config object to extend other configs

BREAKING CHANGE: `extends` key now used for extending config files
```

Both together:

```
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

## Examples

**Simple fix:**

```
fix: prevent racing of requests
```

**Feature with scope:**

```
feat(lang): add Polish language
```

**Fix with body and footers:**

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

**Revert with footer references:**

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

**Docs with no body:**

```
docs: correct spelling of CHANGELOG
```

## Non-obvious rules

- **NEVER** add `Co-Authored-By` trailers to commit messages. This project does not use authorship footers.
- Types are **case-insensitive** in parsing, but `BREAKING CHANGE` footer token **must be uppercase**.
- `BREAKING-CHANGE` (hyphen) is a valid synonym for `BREAKING CHANGE` in footers.
- Footer tokens use `-` instead of spaces (e.g. `Reviewed-by`), **except** `BREAKING CHANGE`.
- Footer separator is either `": "` (colon-space) or `" #"` (space-hash for issue refs): `Refs #123`.
- A footer value may span multiple lines; parsing stops at the next valid `Token: ` or `Token #` pair.
- When a commit fits multiple types, split into multiple commits instead of picking one.
- Wrong type used before merge? Ask the developer to fix manually with an interactive rebase. Claude Code cannot run interactive commands. After release, the commit is simply missed by automation tools — not catastrophic.
- Squash workflows: lead maintainer can rewrite messages at merge time; contributors don't need to follow the spec perfectly on every WIP commit.

## Choosing the right type

```
Is it a new user-facing capability?         → feat
Is it fixing incorrect behavior?            → fix
Is it changing docs/comments only?          → docs
Is it improving speed/memory?               → perf
Is it reorganizing code (no behavior Δ)?    → refactor
Is it adding/fixing tests only?             → test
Is it CI pipeline config?                   → ci
Is it build tooling or dependency updates?  → build
Is it undoing a previous commit?            → revert
Everything else (scripts, config, etc.)?    → chore
```

## SemVer cheatsheet

`fix`→PATCH, `feat`→MINOR, `BREAKING CHANGE`→MAJOR
