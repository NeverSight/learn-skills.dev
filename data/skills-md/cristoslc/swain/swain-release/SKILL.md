---
name: swain-release
description: Cut a release — detect versioning context, generate a changelog from conventional commits, bump versions, and create a git tag. Use when the user says "release", "cut a release", "tag a release", "bump the version", "create a changelog", or any variation of shipping/publishing a version. This skill is intentionally generic and works across any repo — it infers context from git history and project structure rather than assuming a specific setup.
license: UNLICENSED
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion
metadata:
  short-description: Version bump, changelog, and git tag
  version: 1.0.0
  author: cristos
---

# Release

Cut a release by detecting the project's versioning context, generating a changelog, bumping versions, and tagging. Works across any repo by reading context from git history and project structure rather than hardcoding assumptions.

## Override file

Before starting, read `.agents/release.override.skill.md` if it exists. This is a freeform markdown file authored by the project owner whose instructions layer on top of this skill — its contents take precedence where they conflict. It can narrow defaults, specify version file locations, set tag formats, add pre/post-release steps, or anything else.

If no override exists, proceed with context detection alone.

## Workflow

### 1. Gather context

Infer the project's release conventions from what already exists. Do all of these checks up front before proposing anything to the user.

**Tag history:**
```bash
git tag --sort=-v:refname | head -20
```
From existing tags, infer:
- **Tag format** — `v1.2.3`, `1.2.3`, `name-v1.2.3`, or something else
- **Versioning scheme** — semver, calver, or custom
- **Current version** — the most recent tag that matches the detected pattern

If there are no tags at all, note that this is the first release and ask the user what format they want.

**Commits since last release:**
```bash
git log <last-tag>..HEAD --oneline --no-decorate
```
If no tags exist, use all commits (or a reasonable window — ask the user if there are hundreds).

**Version files** — scan for files that commonly hold version numbers:
```bash
# Look for common version carriers
grep -rl 'version' --include='*.json' --include='*.toml' --include='*.yaml' --include='*.yml' -l . 2>/dev/null | head -20
```
Also check for `VERSION` files, `version:` in SKILL.md frontmatter, `version` fields in `package.json`, `pyproject.toml`, `Cargo.toml`, etc. Don't modify anything yet — just catalog what exists.

### 2. Determine the bump

Parse commits since the last tag using conventional-commit prefixes to suggest a bump level:

| Commit prefix | Suggests |
|---------------|----------|
| `feat` | minor bump |
| `fix` | patch bump |
| `docs`, `chore`, `refactor`, `test`, `ci` | patch bump |
| `BREAKING CHANGE` in body, or `!` after type | major bump |

The highest-level signal wins (any breaking change = major, any feat = at least minor, otherwise patch).

If commits don't follow conventional-commit format, fall back to listing them and asking the user what bump level feels right.

### 3. Propose the release

Present the user with a release plan before executing anything. Include:

- **Current version** (from latest tag, or "first release")
- **Proposed version** (with the detected bump applied)
- **Changelog preview** (grouped by type — see below)
- **Files to update** (version files found in step 1, if any)
- **Tag to create** (using the detected format)

Wait for the user to confirm, adjust the version, or abort. If the user wants a different version than what was suggested, use theirs — the suggestion is a starting point, not a mandate.

### 4. Generate the changelog

Group commits by conventional-commit type. Use clear, human-readable headings:

```markdown
## [1.5.0] - 2026-03-06

### New Features
- Add superpowers plan ingestion script (#SPEC-003)
- Add superpowers detection and routing to swain-design (#SPEC-004)

### Bug Fixes
- Fix specwatch false positives on cross-directory refs

### Documentation
- Complete SPIKE-008 superpowers evaluation
- Transition EPIC-009 to Complete

### Other Changes
- Update list-epics.md and list-specs.md indexes
```

Conventions:
- Strip the conventional-commit prefix from the summary line (readers don't need `feat:` when it's already under "New Features")
- Keep entries concise — one line per commit, imperative mood
- If a commit references an artifact ID (SPEC-003, EPIC-009, etc.), keep it
- Commits that are purely mechanical (merge commits, hash stamps, index refreshes) can be grouped under "Other Changes" or omitted if the changelog would be cleaner without them — use judgment

**Where to put the changelog:**
- If a `CHANGELOG.md` exists, prepend the new section at the top (below any header)
- If no changelog exists, ask the user whether they want one created, and where
- If the user doesn't want a file, just output it to the conversation

### 5. Bump versions

Update version strings in the files identified in step 1. Be surgical — only change the version value, not surrounding content. For each file type:

- **package.json / composer.json**: update the `"version"` field
- **pyproject.toml / Cargo.toml**: update `version = "..."`
- **SKILL.md frontmatter**: update `version:` in YAML header
- **VERSION file**: replace contents

If a file has multiple version-like strings and it's ambiguous which one to update, ask the user rather than guessing.

### 6. Commit and tag

Stage the changed files (changelog + version bumps) and commit:

```bash
git add <changed-files>
git commit -m "release: v1.5.0"
```

Then create an annotated tag:

```bash
git tag -a <tag> -m "Release <tag>"
```

Use the tag format detected in step 1 (or what the user specified).

### 7. Offer to push

Ask the user if they want to push the commit and tag:

```bash
git push && git push --tags
```

Don't push without asking — the user may want to review first, or they may have a CI pipeline that triggers on tags.

## Edge cases

**Monorepo with multiple version streams:** If the tag history suggests per-package tags (e.g., `frontend-v1.2.0`, `api-v3.1.0`), ask the user which package they're releasing rather than assuming.

**Pre-release versions:** If the user asks for a pre-release (alpha, beta, rc), append the pre-release suffix to the version: `1.5.0-alpha.1`. Follow the existing convention if prior pre-release tags exist.

**No conventional commits:** If the commit history doesn't use conventional prefixes, don't force the grouping. Present a flat list and let the changelog be a simple bullet list of changes.

**Dirty working tree:** If there are uncommitted changes when `/swain-release` is invoked, warn the user and ask whether to proceed (changes won't be included in the release) or abort so they can commit first.
