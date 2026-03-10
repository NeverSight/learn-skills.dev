---
name: docs-changelog
description: Write changelog entries for open source documentation sites using Keep a Changelog format. Use when asked to "write a changelog", "update the changelog", "add changelog entry", "document recent changes", or after a release/set of changes that should be recorded. Reviews git commits since the last changelog entry and produces a categorized, human-readable entry.
---

# Docs Changelog

Write a new changelog entry by reviewing commits since the last documented entry, categorizing changes, and appending a well-written entry in Keep a Changelog format.

## Workflow

### 1. Find the changelog file

Search for the changelog in common locations:

```
CHANGELOG.md
changelog.md
docs/changelog.md
docs/CHANGELOG.md
src/pages/changelog.md
src/content/changelog.mdx
content/changelog.md
```

Use `glob` with patterns like `**/changelog.{md,mdx}` and `**/CHANGELOG.{md,mdx}` if not found in standard locations. If multiple candidates exist, ask the user which one to use.

### 2. Parse the last entry

Read the changelog file and extract the most recent version header. The header format is:

```
## [X.Y.Z] - YYYY-MM-DD
```

Extract:
- **Version number** (e.g., `1.2.0`) — for determining the next version
- **Date** (e.g., `2025-01-15`) — for scoping the git log

If the changelog is empty or has only an `[Unreleased]` header, use the repo's earliest tag or first commit as the boundary.

### 3. Gather commits

Run:

```bash
git log --oneline --no-merges --after="YYYY-MM-DD" HEAD
```

Where `YYYY-MM-DD` is the date from the last changelog entry. Also check tags:

```bash
git tag -l --sort=-creatordate | head -5
```

If there's a tag newer than the last changelog entry, use that as the new version number. Otherwise, ask the user what version this entry should be.

### 4. Categorize changes

Review each commit and assign it to one Keep a Changelog category:

| Category | What belongs here |
|---|---|
| **Added** | New features, new pages, new API endpoints |
| **Changed** | Updates to existing functionality, behavior changes, dependency updates |
| **Deprecated** | Features marked for future removal |
| **Removed** | Deleted features, removed pages, dropped support |
| **Fixed** | Bug fixes, typo corrections, broken link repairs |
| **Security** | Vulnerability patches, security improvements |

**Categorization rules:**
- Read the diff when a commit message is ambiguous — the code tells the truth
- Group related commits into a single bullet (e.g., three typo-fix commits become one "Fixed typos across documentation" entry)
- Skip commits that are purely internal (CI config, linting, formatting-only) unless they affect user-visible behavior
- Skip merge commits and version bump commits

### 5. Write the entry

Insert the new entry directly below the `# Changelog` header (or below `## [Unreleased]` if present). Use this exact structure — omit any category section that has no items:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added

- Brief, human-readable description of what was added

### Changed

- Brief description of what changed

### Fixed

- Brief description of what was fixed
```

**Writing rules:**
- Each bullet is one sentence, starting with a past-tense verb (Added, Updated, Fixed, Removed)
- Write for the end user of the documentation site, not for developers
- Link to relevant pages or PRs where helpful: `Fixed broken link on [Getting Started](/docs/getting-started) page`
- Keep entries scannable — no paragraphs, no sub-bullets
- Use the project's existing tone (scan prior entries to match)
- Today's date for the entry date unless the user specifies otherwise

### 6. Verify

After writing the entry:
- Confirm the entry is in reverse chronological order (newest first)
- Check that version link references at the bottom of the file are updated if the project uses them (e.g., `[1.3.0]: https://github.com/org/repo/compare/v1.2.0...v1.3.0`)
- Read the final file to ensure formatting is clean

Present the new entry to the user for review before considering the task complete.
