---
name: bagisto-git-workflow
description: Use when branching, committing, writing a CHANGELOG entry or opening a pull request against a Bagisto repository. Trigger phrases include "branch", "commit", "commit message", "PR", "pull request", "changelog", "merge", "conventional commits", "release notes".
license: MIT
---

# Git Workflow

The conventions this repository actually follows, read from its history rather
than from a generic Git guide.

## Branches

`<author>/<topic>` or `<author>/<type>/<topic>`, lowercase and hyphenated:

```
devansh-webkul/themes-improvements
kartikeywebkul9260/v2.4_file_attribute_required_validation
Vansh-Sharmaa/fix/duplicate-product-customizable-options
```

Branch from the release line you are targeting — `2.4` for 2.4 work, `master`
for the next major — and open the pull request against that same branch. Never
commit directly to `2.4` or `master`.

## Commits

Conventional Commits, lowercase subject, imperative or descriptive. Across the
last 200 commits: `fix:` 66, `feat:` 21, `chore:` 9, `chore(deps):` 5,
`test:` 3, `refactor(shop):` 1, `docs:` 1.

```
fix: grouped themes into two parts my theme and buy themes
feat: playwight testcases updated and draft issue fixed
test: playwright testcases added
chore: changelog and version updated
```

A scope is optional and used sparingly — `refactor(shop):`, `chore(deps):`.

Write a body only when the subject cannot carry the reason — 12 of the last 100
non-merge commits have one. The body explains **why**, not what the diff shows —
and it is the right home for anything you were tempted to write as a comment in
the code, since this codebase does not take comments inside method bodies.

**Never add AI or tool attribution.** No `Co-Authored-By` for an assistant, no
"Generated with", no robot emoji. There are none in this repository's history
and none should appear.

## CHANGELOG

`CHANGELOG.md` opens with `## Unreleased`, then one section per release:

```markdown
## Unreleased

- Entry.

## **v2.4.9 (5th of August 2026)** - *Release*

- Entry.
```

Entries are `-` prefixed with a blank line between them, and are **prose written
for the person upgrading**: the user-visible effect, in full sentences. Not a
commit subject, not a diff summary.

> Fixed the mega search leaving you on an empty tab when another tab had
> results, which read as nothing being found. It now opens the first tab that
> matched.

**Every entry is at most two lines — clear and to the point.** This is a hard
ceiling, and it applies to both shapes:

| Shape | When |
|---|---|
| `- <prose>` | A feature or a change with no reported issue |
| `- #11432 [fixed] - <prose>` | A fix for a reported issue |

State the user-visible effect and stop. The cause, the internal mechanism and
the history are **not** CHANGELOG material — they belong in the commit message
or the pull request, which is where anyone investigating the change will look.
If an entry does not fit in two lines, it is carrying explanation that should
move there.

```markdown
- Fixed the admin product listing repeating a product once for every channel it is carried by.
```

```markdown
- Fixed the admin product listing repeating a product once for every channel it is carried by, so a
  store with three channels listed it three times. The PostgreSQL work had widened the grouping from
  the product to every selected column, which made the channel part of the group; it now picks one
  row per product.        ← the cause belongs in the commit message, not here
```

Add the entry under `## Unreleased`. Do not invent a version heading or a date —
releases are cut separately.

## Pull requests

Merged with GitHub's default subject, which is what the history shows:

```
Merge pull request #11426 from devansh-webkul/themes-improvements
```

The description states what changed and why, and names anything a reviewer
cannot see in the diff — a config default, a migration, a follow-up left out.
Run the verification gates before opening it, and say in the description which
ran and which were skipped.

## Rules

- **Do not commit, push, or open a PR unless asked.** Leave the work in the
  tree and say what is ready.
- **Never `--force` onto a shared branch**, and never rewrite published history.
- **Never commit `.env`, credentials, `vendor/`, `node_modules/`, or build
  output under `public/themes/*/build/`.**
- **One logical change per commit.** A fix and an unrelated refactor are two
  commits, so either can be reverted alone.
- **Do not add or remove a Composer or npm dependency without approval**, and
  never commit a lockfile change you did not intend.
- **Run the gates first.** A commit that fails Pint or the tests is a commit
  that fails CI.

**REQUIRED SUB-SKILL:** Use bagisto-change-verification before calling any change done.
