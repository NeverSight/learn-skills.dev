---
name: create-github-release
description: >
  Create a GitHub release with proper tagging, release notes,
  and optional build artifacts. Covers semantic versioning,
  changelog generation, and GitHub CLI usage. Use when marking a stable
  version of software for distribution, publishing a new library or
  application version, creating release notes for stakeholders, or
  distributing build artifacts (binaries, tarballs).
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: git
  complexity: basic
  language: multi
  tags: github, release, git-tags, changelog, versioning
---

# Create GitHub Release

Create a tagged GitHub release with release notes and optional artifacts.

## When to Use

- Marking a stable version of software for distribution
- Publishing a new version of a library or application
- Creating release notes for stakeholders
- Distributing build artifacts (binaries, tarballs)

## Inputs

- **Required**: Version number (semantic versioning)
- **Required**: Summary of changes since last release
- **Optional**: Build artifacts to attach
- **Optional**: Whether this is a pre-release

## Procedure

### Step 1: Determine Version Number

Follow semantic versioning (`MAJOR.MINOR.PATCH`):

| Change | Example | When |
|--------|---------|------|
| MAJOR | 1.0.0 -> 2.0.0 | Breaking changes |
| MINOR | 1.0.0 -> 1.1.0 | New features, backward compatible |
| PATCH | 1.0.0 -> 1.0.1 | Bug fixes only |

**Expected:** A version number is chosen that accurately reflects the scope of changes since the last release.

**On failure:** If unsure whether changes are breaking, review the public API diff. Any removal or signature change of an exported function is a breaking change requiring a MAJOR bump.

### Step 2: Update Version in Project Files

- `DESCRIPTION` (R packages)
- `package.json` (Node.js)
- `Cargo.toml` (Rust)
- `pyproject.toml` (Python)

**Expected:** The version number is updated in the appropriate project file and committed to version control.

**On failure:** If the version was already updated in a previous step (e.g., via `usethis::use_version()` in R), verify it matches the intended release version.

### Step 3: Write Release Notes

Create or update changelog. Organize by category:

```markdown
## What's Changed

### New Features
- Added user authentication (#42)
- Support for custom themes (#45)

### Bug Fixes
- Fixed crash on empty input (#38)
- Corrected date parsing in UTC (#41)

### Improvements
- Improved error messages
- Updated dependencies

### Breaking Changes
- `old_function()` renamed to `new_function()` (#50)

**Full Changelog**: https://github.com/user/repo/compare/v1.0.0...v1.1.0
```

**Expected:** Release notes are organized by category (features, fixes, breaking changes) with issue/PR references for traceability.

**On failure:** If changes are hard to categorize, review `git log v1.0.0..HEAD --oneline` to reconstruct the list of changes since the last release.

### Step 4: Create Git Tag

```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

**Expected:** An annotated tag `v1.1.0` exists locally and on the remote. `git tag -l` shows the tag.

**On failure:** If the tag already exists, delete it with `git tag -d v1.1.0 && git push origin :refs/tags/v1.1.0` and recreate it. If push is rejected, ensure you have write access to the remote.

### Step 5: Create GitHub Release

**Using GitHub CLI (recommended)**:

```bash
gh release create v1.1.0 \
  --title "v1.1.0" \
  --notes-file CHANGELOG.md
```

With artifacts:

```bash
gh release create v1.1.0 \
  --title "v1.1.0" \
  --notes "Release notes here" \
  build/app-v1.1.0.tar.gz \
  build/app-v1.1.0.zip
```

Pre-release:

```bash
gh release create v2.0.0-beta.1 \
  --title "v2.0.0 Beta 1" \
  --prerelease \
  --notes "Beta release for testing"
```

**Expected:** Release visible on GitHub with tag, notes, and attached artifacts (if any).

**On failure:** If `gh` is not authenticated, run `gh auth login`. If the tag does not exist on the remote, push it first with `git push origin v1.1.0`.

### Step 6: Auto-Generate Release Notes

GitHub can auto-generate notes from merged PRs:

```bash
gh release create v1.1.0 \
  --title "v1.1.0" \
  --generate-notes
```

Configure categories in `.github/release.yml`:

```yaml
changelog:
  categories:
    - title: New Features
      labels:
        - enhancement
    - title: Bug Fixes
      labels:
        - bug
    - title: Documentation
      labels:
        - documentation
    - title: Other Changes
      labels:
        - "*"
```

**Expected:** Release notes are auto-generated from merged PR titles, categorized by label. `.github/release.yml` controls the categories.

**On failure:** If auto-generated notes are empty, ensure PRs were merged (not closed) and had labels assigned. Manually write notes as a fallback.

### Step 7: Verify Release

```bash
# List releases
gh release list

# View specific release
gh release view v1.1.0
```

**Expected:** `gh release list` shows the new release. `gh release view` displays the correct title, tag, notes, and assets.

**On failure:** If the release is missing, check the Actions tab for any release workflows that may have failed. Verify the tag exists with `git tag -l`.

## Validation

- [ ] Version tag follows semantic versioning
- [ ] Git tag points to the correct commit
- [ ] Release notes accurately describe changes
- [ ] Artifacts (if any) are attached and downloadable
- [ ] Release is visible on the GitHub repository page
- [ ] Pre-release flag is set correctly

## Common Pitfalls

- **Tagging wrong commit**: Always verify `git log` before tagging. Tag after version-bump commit.
- **Forgetting to push tags**: `git push` doesn't push tags. Use `git push --tags` or `git push origin v1.1.0`.
- **Inconsistent version format**: Decide on `v1.0.0` vs `1.0.0` and stick with it.
- **Empty release notes**: Always provide meaningful notes. Users need to know what changed.
- **Deleting and recreating tags**: Avoid changing tags after push. If needed, create a new version instead.

## Related Skills

- `commit-changes` - staging and committing workflow
- `manage-git-branches` - branch management for release prep
- `release-package-version` - R-specific release workflow
- `configure-git-repository` - Git setup prerequisite
- `setup-github-actions-ci` - automate releases via CI
