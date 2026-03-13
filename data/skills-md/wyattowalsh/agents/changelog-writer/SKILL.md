---
name: changelog-writer
description: >-
  Generate changelogs, release notes, and migration guides from git history.
  Parse conventional commits. Use for releases. NOT for git ops (git-workflow)
  or doc sites (docs-steward).
argument-hint: "<mode> [version]"
license: MIT
model: sonnet
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Changelog Writer

Generate changelogs, release notes, breaking change summaries, migration guides, and version bump recommendations from git history.

**Scope:** Changelog and release documentation only. NOT for git operations (git-workflow), documentation sites (docs-steward), or code review (honest-review).

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| Empty / `generate` | Generate changelog from recent commits |
| `release <version>` | User-facing release notes for specific version |
| `breaking` | Breaking change detection and summary |
| `migration <from> <to>` | Migration guide between two versions |
| `bump` | Semantic version recommendation based on changes |
| Unrecognized input | Ask for clarification, show mode menu |

## Canonical Vocabulary

| Term | Definition |
|------|-----------|
| **conventional commit** | Commit following `type(scope): description` format |
| **change type** | Classification: feat, fix, refactor, perf, docs, chore, test, ci, build, style |
| **breaking change** | Backward-incompatible change, marked by `!` or `BREAKING CHANGE:` footer |
| **scope** | Component affected, in parentheses after type |
| **changelog entry** | Formatted line item in a changelog section |
| **release notes** | User-facing summary of changes for a version |
| **migration guide** | Step-by-step instructions to upgrade between versions |
| **semver bump** | major (breaking), minor (feat), patch (fix) recommendation |
| **unreleased** | Changes since the last tagged version |

## Mode 1: Generate Changelog

Default mode. Produces a Keep a Changelog formatted document.

### Step 1: Classify Commits

Run the commit classifier script:

```
uv run python skills/changelog-writer/scripts/commit-classifier.py [--since <tag-or-date>] [--until <ref>] [--path <dir>]
```

Parse the JSON output. The script classifies each commit by conventional type and detects breaking changes.

### Step 2: Format Changelog

Run the changelog formatter script:

```
uv run python skills/changelog-writer/scripts/changelog-formatter.py --input <classified-json> [--format keepachangelog|github|simple]
```

The script converts classified commits to formatted markdown. Default format: Keep a Changelog.

### Step 3: Review and Refine

- Group entries by section (Added, Changed, Deprecated, Removed, Fixed, Security)
- Rewrite terse commit messages into user-readable descriptions
- Merge related commits into single entries where appropriate
- Ensure breaking changes are prominently called out

Format reference: read references/changelog-conventions.md

## Mode 2: Release Notes

`release <version>` produces polished, user-facing release notes.

### Step 1: Identify Scope

Determine the range: last tag to HEAD (or between two tags if version already tagged).

```bash
git log --oneline <previous-tag>..<version-or-HEAD>
```

### Step 2: Classify and Group

Run `commit-classifier.py` with the appropriate `--since` and `--until` flags. Group by user impact, not commit type:

- **Highlights** — headline features (top 3-5)
- **Improvements** — enhancements, performance gains
- **Bug Fixes** — resolved issues
- **Breaking Changes** — migration-required items (link to migration mode)
- **Contributors** — credit contributors from git log

### Step 3: Write Release Notes

Rewrite technical commit messages into user-facing language. Reference: read references/changelog-conventions.md, section "Release Note Style."

## Mode 3: Breaking Changes

`breaking` scans for backward-incompatible changes.

### Step 1: Detect

Run the commit classifier with breaking-change focus:

```
uv run python skills/changelog-writer/scripts/commit-classifier.py --breaking-only [--since <tag>]
```

### Step 2: Enrich

For each breaking change:

1. Identify the affected API/interface
2. Describe what changed and why
3. Provide the before/after code pattern
4. Assess blast radius (how many consumers affected)

Use patterns from `data/breaking-change-patterns.json` for language-specific detection.

### Step 3: Summarize

Output a breaking changes report with severity ranking (high/medium/low) based on blast radius and migration effort.

## Mode 4: Migration Guide

`migration <from> <to>` generates step-by-step upgrade instructions.

### Step 1: Collect Breaking Changes

Run commit classifier between the two versions:

```
uv run python skills/changelog-writer/scripts/commit-classifier.py --breaking-only --since <from> --until <to>
```

### Step 2: Generate Migration Steps

For each breaking change, produce:

1. **What changed** — old behavior vs new behavior
2. **Action required** — exact steps to migrate
3. **Code example** — before/after snippets
4. **Verification** — how to confirm the migration worked

Order steps by dependency (changes that must happen first go first).

### Step 3: Compile Guide

Structure as a numbered checklist. Include a pre-migration checklist (backup, test suite green) and post-migration verification steps.

Reference: read references/changelog-conventions.md, section "Migration Guide Structure."

## Mode 5: Version Bump

`bump` recommends the next semantic version.

### Step 1: Analyze

Run the commit classifier:

```
uv run python skills/changelog-writer/scripts/commit-classifier.py --since <last-tag>
```

Read the `suggested_bump` field from the JSON output.

### Step 2: Report

Present the recommendation with evidence:

| Bump | Reason |
|------|--------|
| **major** | Breaking changes detected: list them |
| **minor** | New features without breaking changes |
| **patch** | Bug fixes and non-functional changes only |

Show the commit evidence supporting the recommendation. If commits are ambiguous (non-conventional format), flag uncertainty and ask for confirmation.

## Reference Files

Load ONE reference at a time.

| File | Content | Read When |
|------|---------|-----------|
| `references/changelog-conventions.md` | Keep a Changelog format, release note style, migration guide structure, semver decision tree | Formatting output in any mode |
| `references/commit-parsing.md` | Conventional commits parsing rules, breaking change detection heuristics | Understanding classifier output or edge cases |

| Data File | Content | Used By |
|-----------|---------|---------|
| `data/changelog-formats.json` | Format templates (Keep a Changelog, GitHub Releases, simple) | `changelog-formatter.py` |
| `data/breaking-change-patterns.json` | Language-specific breaking change detection patterns | `commit-classifier.py`, Mode 3 enrichment |

| Script | Purpose |
|--------|---------|
| `scripts/commit-classifier.py` | Parse git log, classify by conventional type, detect breaking changes |
| `scripts/changelog-formatter.py` | Convert classified commits JSON to formatted changelog markdown |

## Critical Rules

1. Never modify git history or run git operations beyond `git log` and `git tag` — this skill reads only
2. Always run `commit-classifier.py` before formatting — do not manually parse git log
3. Breaking changes must be prominently called out in every output format
4. Rewrite commit messages into user-readable language — raw commit text is not a changelog
5. Migration guides must include before/after code examples for every breaking change
6. Version bump recommendations must cite specific commits as evidence
7. When commits are non-conventional, classify by best-effort heuristics and flag uncertainty
8. Do not generate changelogs for uncommitted changes — only committed history
9. Always identify the previous tag as the baseline unless the user specifies otherwise
10. Credit contributors in release notes — extract from git log author fields
