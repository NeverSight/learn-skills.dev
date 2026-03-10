---
name: apply-semantic-versioning
description: >
  Apply semantic versioning (SemVer 2.0.0) to determine the correct
  version bump based on change analysis. Covers major/minor/patch
  classification, pre-release identifiers, build metadata, and
  breaking change detection. Use when preparing a new release to determine
  the correct version number, after merging changes before tagging, evaluating
  whether a change constitutes a breaking change, adding pre-release identifiers,
  or resolving disagreement about what version bump is appropriate.
license: MIT
allowed-tools: Read Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: versioning
  complexity: intermediate
  language: multi
  tags: versioning, semver, version-bump, breaking-changes
---

# Apply Semantic Versioning

Determine and apply the correct semantic version bump by analyzing changes since the last release. This skill reads version files, classifies changes as breaking (major), feature (minor), or fix (patch), computes the new version number, and updates the appropriate files. Follows [SemVer 2.0.0](https://semver.org/) specification.

## When to Use

- Preparing a new release and need to determine the correct version number
- After merging a set of changes and before tagging a release
- Evaluating whether a change constitutes a breaking change
- Adding pre-release identifiers (alpha, beta, rc) to a version
- Resolving disagreement about what version bump is appropriate

## Inputs

- **Required**: Project root directory containing a version file (DESCRIPTION, package.json, Cargo.toml, pyproject.toml, or VERSION)
- **Required**: Git history since the last release (tag or commit)
- **Optional**: Commit convention in use (Conventional Commits, free-form)
- **Optional**: Pre-release label to apply (alpha, beta, rc)
- **Optional**: Previous version if not readable from files

## Procedure

### Step 1: Read Current Version

Locate and read the version file in the project root.

```bash
# R packages
grep "^Version:" DESCRIPTION

# Node.js
grep '"version"' package.json

# Rust
grep '^version' Cargo.toml

# Python
grep 'version' pyproject.toml

# Plain file
cat VERSION
```

Parse the current version into major.minor.patch components. If the version contains a pre-release suffix (e.g., `1.2.0-beta.1`), note it separately.

**Expected:** Current version identified as `MAJOR.MINOR.PATCH[-PRERELEASE]`.

**On failure:** If no version file is found, check for a VERSION file or git tags (`git describe --tags --abbrev=0`). If no version exists at all, start at `0.1.0` for initial development or `1.0.0` if the project has a stable public API.

### Step 2: Analyze Changes Since Last Release

Retrieve the list of changes since the last tagged release.

```bash
# Find the last version tag
git describe --tags --abbrev=0

# List commits since that tag
git log --oneline v1.2.3..HEAD

# If using Conventional Commits, filter by type
git log --oneline v1.2.3..HEAD | grep -E "^[a-f0-9]+ (feat|fix|BREAKING)"
```

If no tags exist, compare against the initial commit or a known baseline.

**Expected:** A list of commits with messages that can be classified by change type.

**On failure:** If git history is unavailable or tags are missing, ask the developer to describe the changes manually. Classify based on their description.

### Step 3: Classify Changes

Apply the SemVer classification rules:

| Change Type | Version Bump | Examples |
|---|---|---|
| **Breaking** (incompatible API change) | MAJOR | Renamed/removed public function, changed return type, removed parameter, changed default behavior |
| **Feature** (new backwards-compatible functionality) | MINOR | New exported function, new parameter with default, new file format support |
| **Fix** (backwards-compatible bug fix) | PATCH | Bug fix, documentation correction, performance improvement with same API |

Classification rules:
1. If ANY change is breaking, the bump is MAJOR (resets minor and patch to 0)
2. If no breaking changes but ANY new features, the bump is MINOR (resets patch to 0)
3. If only fixes, the bump is PATCH

Special cases:
- **Pre-1.0.0**: During initial development (`0.x.y`), minor bumps may contain breaking changes. Document clearly.
- **Deprecation**: Deprecating a function is a MINOR change (it still works). Removing it is MAJOR.
- **Internal changes**: Refactoring that does not change the public API is PATCH.

**Expected:** Each change classified as breaking/feature/fix, and the overall bump level determined.

**On failure:** If changes are ambiguous, err on the side of a higher bump. A conservative major bump is better than a minor bump that breaks downstream code.

### Step 4: Compute New Version

Apply the bump to the current version:

| Current | Bump | New Version |
|---|---|---|
| 1.2.3 | MAJOR | 2.0.0 |
| 1.2.3 | MINOR | 1.3.0 |
| 1.2.3 | PATCH | 1.2.4 |
| 0.9.5 | MINOR | 0.10.0 |
| 2.0.0-rc.1 | (release) | 2.0.0 |

If a pre-release label is requested:
- `1.3.0-alpha.1` for first alpha of upcoming 1.3.0
- `1.3.0-beta.1` for first beta
- `1.3.0-rc.1` for first release candidate

Pre-release precedence: `alpha < beta < rc < (release)`.

**Expected:** New version number computed following SemVer rules.

**On failure:** If the current version is malformed or non-SemVer, normalize it first. For example, `1.2` becomes `1.2.0`.

### Step 5: Update Version Files

Write the new version to the appropriate file(s).

```r
# R: Update DESCRIPTION
# Change "Version: 1.2.3" to "Version: 1.3.0"
```

```json
// Node.js: Update package.json
// Change "version": "1.2.3" to "version": "1.3.0"
// Also update package-lock.json if present
```

```toml
# Rust: Update Cargo.toml
# Change version = "1.2.3" to version = "1.3.0"
```

If the project has multiple files that reference the version (e.g., `_pkgdown.yml`, `CITATION`, `codemeta.json`), update all of them.

**Expected:** All version files updated consistently to the new version number.

**On failure:** If a file update fails, revert all changes to maintain consistency. Never leave version files in a partially updated state.

### Step 6: Create Version Tag

After committing the version bump, create a git tag.

```bash
# Annotated tag (preferred)
git tag -a v1.3.0 -m "Release v1.3.0"

# Lightweight tag (acceptable)
git tag v1.3.0
```

Use the project's established tag format:
- `v1.3.0` (most common)
- `1.3.0` (no prefix)
- `package-name@1.3.0` (monorepo)

**Expected:** Git tag created matching the new version.

**On failure:** If the tag already exists, the version was not properly bumped. Check for duplicate tags with `git tag -l "v1.3*"` and resolve before proceeding.

## Validation

- [ ] Current version was read from the correct version file
- [ ] All commits since the last release were analyzed
- [ ] Each change is classified as breaking, feature, or fix
- [ ] The bump level matches the highest-severity change (breaking > feature > fix)
- [ ] New version follows SemVer 2.0.0 format: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`
- [ ] All version files in the project are updated consistently
- [ ] No version was skipped (e.g., 1.2.3 to 1.4.0 without 1.3.0 being released)
- [ ] Git tag matches the new version and project's tag format convention
- [ ] Pre-release suffix, if used, follows correct precedence (alpha < beta < rc)

## Common Pitfalls

- **Skipping minor versions**: Going from 1.2.3 directly to 1.4.0 because "we added two features." Each release gets one bump; the number of features does not determine the version.
- **Treating deprecation as breaking**: Deprecating a function (adding a warning) is a minor change. Only removing it is a breaking change.
- **Forgetting pre-1.0.0 rules**: Before 1.0.0, the API is considered unstable. Some projects bump minor for breaking changes during this phase, but it should be documented.
- **Inconsistent version files**: Updating package.json but not package-lock.json, or updating DESCRIPTION but not CITATION. All version references must stay in sync.
- **Build metadata confusion**: Build metadata (`+build.123`) does not affect version precedence. `1.0.0+build.1` and `1.0.0+build.2` have the same precedence.
- **Not tagging releases**: Without git tags, future version bumps cannot determine the baseline for change analysis.

## Related Skills

- `manage-changelog` -- Maintain changelog entries that pair with version bumps
- `plan-release-cycle` -- Plan release milestones that determine when version bumps occur
- `release-package-version` -- R-specific release workflow that includes version bumping
- `commit-changes` -- Commit the version bump with a proper message
- `create-github-release` -- Create a GitHub release from the version tag
