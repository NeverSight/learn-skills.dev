---
name: manage-changelog
description: >
  Maintain a changelog following Keep a Changelog format. Covers
  entry categorization (Added, Changed, Deprecated, Removed, Fixed,
  Security), version section management, and unreleased tracking. Use when
  starting a new project that needs a changelog, adding entries after
  completing features or fixes, preparing a release by promoting Unreleased
  entries to a versioned section, or converting a free-form changelog to
  Keep a Changelog format.
license: MIT
allowed-tools: Read Write Edit Grep
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: versioning
  complexity: basic
  language: multi
  tags: versioning, changelog, documentation, keep-a-changelog
---

# Manage Changelog

Maintain a project changelog following the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. This skill covers creating a new changelog, categorizing entries, managing the `[Unreleased]` section, and promoting entries to versioned sections upon release. Adapts to R convention (`NEWS.md`) when detected.

## When to Use

- Starting a new project that needs a changelog
- Adding entries after completing features, fixes, or other changes
- Preparing a release by moving Unreleased entries to a versioned section
- Reviewing changelog completeness before publishing
- Converting a free-form changelog to Keep a Changelog format

## Inputs

- **Required**: Project root directory
- **Required**: Description of changes to document (or git log to extract from)
- **Optional**: Target version number (for release promotion)
- **Optional**: Release date (defaults to today)
- **Optional**: Changelog format preference (Keep a Changelog or R NEWS.md)

## Procedure

### Step 1: Locate or Create Changelog

Search for an existing changelog in the project root.

```bash
# Check for common changelog filenames
ls -1 CHANGELOG.md CHANGELOG NEWS.md CHANGES.md HISTORY.md 2>/dev/null
```

If no changelog exists, create one with the standard header:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
```

For R packages, use `NEWS.md` with R convention formatting:

```markdown
# packagename (development version)

## New features

## Bug fixes

## Minor improvements and fixes
```

**Expected:** Changelog file located or created with proper header and an Unreleased section.

**On failure:** If a changelog exists in a non-standard format, do not overwrite it. Instead, note the format difference and adapt entries to match the existing style.

### Step 2: Parse Existing Entries

Read the changelog and identify its structure:

1. Header/preamble (project name, format description)
2. `[Unreleased]` section with pending changes
3. Versioned sections in reverse chronological order (`[1.2.0]` before `[1.1.0]`)
4. Comparison links at the bottom (optional)

For each section, identify the categories present:
- **Added** -- new features
- **Changed** -- changes in existing functionality
- **Deprecated** -- soon-to-be removed features
- **Removed** -- now removed features
- **Fixed** -- bug fixes
- **Security** -- vulnerability fixes

**Expected:** Changelog structure understood, existing entries inventoried.

**On failure:** If the changelog is malformed (missing sections, wrong order), note the issues but do not restructure without confirmation. Add new entries correctly and flag structural issues for manual review.

### Step 3: Categorize New Changes

For each change to be documented, classify it into one of the six categories:

| Category | When to Use | Example Entry |
|---|---|---|
| Added | New feature or capability | `- Add CSV export for summary reports` |
| Changed | Modification to existing feature | `- Change default timeout from 30s to 60s` |
| Deprecated | Feature marked for future removal | `- Deprecate `old_function()` in favor of `new_function()`` |
| Removed | Feature or capability removed | `- Remove legacy XML parser` |
| Fixed | Bug fix | `- Fix off-by-one error in pagination` |
| Security | Vulnerability fix | `- Fix SQL injection in user search (CVE-2026-1234)` |

Entry writing guidelines:
- Start each entry with a verb in imperative mood (Add, Change, Fix, Remove)
- Be specific enough that a user can understand the impact without reading code
- Reference issue numbers or CVEs where applicable
- Keep entries to one line; use sub-bullets only for complex changes

**Expected:** Each change assigned to exactly one category with a well-written entry.

**On failure:** If a change spans multiple categories (e.g., both adds a feature and fixes a bug), create separate entries in each relevant category. If the category is unclear, default to "Changed."

### Step 4: Add Entries to Unreleased Section

Insert categorized entries under the `[Unreleased]` section. Maintain category order: Added, Changed, Deprecated, Removed, Fixed, Security.

```markdown
## [Unreleased]

### Added

- Add batch processing mode for large datasets
- Add `--dry-run` flag to preview changes without applying

### Fixed

- Fix memory leak when processing files over 1GB
- Fix incorrect timezone handling in date parsing
```

Only add categories that have entries; do not include empty category headings.

**Expected:** New entries added under `[Unreleased]` in the correct categories, maintaining consistent formatting.

**On failure:** If the Unreleased section does not exist, create it immediately below the header/preamble and above the first versioned section.

### Step 5: Promote to Versioned Section on Release

When cutting a release, move all Unreleased entries to a new versioned section:

1. Create a new section heading: `## [1.3.0] - 2026-02-17`
2. Move all entries from `[Unreleased]` to the new section
3. Leave `[Unreleased]` empty (but keep the heading)
4. Update comparison links at the bottom of the file

```markdown
## [Unreleased]

## [1.3.0] - 2026-02-17

### Added

- Add batch processing mode for large datasets

### Fixed

- Fix memory leak when processing files over 1GB

## [1.2.0] - 2026-01-15

### Added

- Add CSV export for summary reports
```

Update comparison links (if present at bottom):

```markdown
[Unreleased]: https://github.com/user/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/user/repo/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

For R `NEWS.md`, use the R convention:

```markdown
# packagename 1.3.0

## New features

- Add batch processing mode for large datasets

## Bug fixes

- Fix memory leak when processing files over 1GB

# packagename 1.2.0
...
```

**Expected:** Unreleased entries moved to a dated versioned section; Unreleased section cleared; comparison links updated.

**On failure:** If the version number conflicts with an existing section, the version was already released. Check with `apply-semantic-versioning` to determine the correct version.

### Step 6: Validate Changelog Format

Verify the changelog meets format requirements:

1. Versions are in reverse chronological order (newest first)
2. Dates follow ISO 8601 format (YYYY-MM-DD)
3. Each versioned section has at least one categorized entry
4. No duplicate version sections
5. Comparison links (if present) match the version sections

```bash
# Check for duplicate version sections
grep "^## \[" CHANGELOG.md | sort | uniq -d

# Verify date format
grep "^## \[" CHANGELOG.md | grep -v "Unreleased" | grep -vE "\d{4}-\d{2}-\d{2}"
```

**Expected:** Changelog passes all format checks with no warnings.

**On failure:** Fix any format issues found: reorder sections, correct date formats, remove duplicates. Report issues that require human judgment (e.g., missing entries for known changes).

## Validation

- [ ] Changelog file exists with proper header referencing Keep a Changelog and SemVer
- [ ] `[Unreleased]` section exists at the top (below header)
- [ ] All new entries are categorized into Added/Changed/Deprecated/Removed/Fixed/Security
- [ ] Entries start with imperative verb and describe user-facing impact
- [ ] Versioned sections are in reverse chronological order
- [ ] Dates use ISO 8601 format (YYYY-MM-DD)
- [ ] No duplicate version sections exist
- [ ] Comparison links (if used) are correct and up to date
- [ ] Empty categories are not included (no heading without entries)

## Common Pitfalls

- **Internal-only entries**: "Refactored database module" is not useful to users. Focus on user-facing changes. Internal refactors go in commit messages, not changelogs.
- **Vague entries**: "Various bug fixes" tells the user nothing. Each fix should be a specific, descriptive entry.
- **Forgetting Unreleased**: Adding entries directly to a versioned section instead of Unreleased means changes are documented as already released when they are not.
- **Wrong category**: "Fix" that actually adds a new feature. A fix restores expected behavior; a new capability is "Added" even if it was requested as a bug report.
- **Missing Security entries**: Security fixes should always be documented with CVE identifiers when available. Users need to know if they should upgrade urgently.
- **Changelog drift**: Not updating the changelog at the time of the change. Batch-writing entries before release leads to missed or poorly described changes. Write entries alongside code changes.

## Related Skills

- `apply-semantic-versioning` -- Determine the version number that pairs with changelog entries
- `plan-release-cycle` -- Define when changelog entries get promoted to versioned sections
- `commit-changes` -- Commit changelog updates with proper messages
- `release-package-version` -- R-specific release workflow including NEWS.md updates
- `create-github-release` -- Use changelog content as GitHub release notes
