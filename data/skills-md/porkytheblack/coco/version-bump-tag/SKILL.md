---
name: version-bump-tag
description: Expert guide for bumping versions, creating git tags, and managing releases for Tauri and Node.js projects.
---

# Version Bump & Tag Management — Development Guide

You are an expert on semantic versioning and release management. Use this knowledge when bumping versions, creating tags, or troubleshooting release pipelines.

## What It Is

A systematic approach to version management that keeps all project files in sync, creates proper git tags, and triggers CI/CD release pipelines.

**This project's scripts**:
- `./app/scripts/bump-version.sh` — Version bumping
- `./app/scripts/redeploy.sh` — Re-trigger failed releases

## Quick Reference (This Project)

```bash
# Bump and release
./app/scripts/bump-version.sh patch    # 0.1.0 → 0.1.1
./app/scripts/bump-version.sh minor    # 0.1.0 → 0.2.0
./app/scripts/bump-version.sh major    # 0.1.0 → 1.0.0
git push && git push --tags

# Other options
./app/scripts/bump-version.sh --set 2.0.0    # Explicit version
./app/scripts/bump-version.sh patch --dry-run # Preview changes
./app/scripts/bump-version.sh patch --no-git  # Skip commit/tag

# Re-deploy failed release
./app/scripts/redeploy.sh              # Current version
./app/scripts/redeploy.sh v0.1.5       # Specific version
```

## Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes (backward compatible)
  │     └──────── New features (backward compatible)
  └────────────── Breaking changes (incompatible API)
```

| Bump | When | Example |
|------|------|---------|
| `patch` | Bug fixes, minor tweaks | 1.0.0 → 1.0.1 |
| `minor` | New features, no breaking changes | 1.0.0 → 1.1.0 |
| `major` | Breaking changes, major rewrites | 1.0.0 → 2.0.0 |

### Pre-release Versions

```
1.0.0-alpha.1    # Early development
1.0.0-beta.1     # Feature complete, testing
1.0.0-rc.1       # Release candidate
```

## Version Files by Project Type

### Tauri Applications (This Project)

| File | Format |
|------|--------|
| `package.json` | `"version": "X.Y.Z"` |
| `src-tauri/tauri.conf.json` | `"version": "X.Y.Z"` |
| `src-tauri/Cargo.toml` | `version = "X.Y.Z"` |
| `src-tauri/Cargo.lock` | Auto-updated |
| UI status bar | Display string |

### Node.js Projects

| File | Format |
|------|--------|
| `package.json` | `"version": "X.Y.Z"` |
| `package-lock.json` | Auto-updated |

### Rust Projects

| File | Format |
|------|--------|
| `Cargo.toml` | `version = "X.Y.Z"` |
| `Cargo.lock` | Auto-updated |

## Pre-Push Validation

**Always validate before releasing:**

```bash
# Quick check
git status --porcelain | grep -q . && echo "UNCOMMITTED CHANGES" && exit 1
git fetch origin
git log @{u}..HEAD --oneline | grep -q . && echo "UNPUSHED COMMITS" && exit 1
echo "Ready to release"
```

### Full Validation Function

```bash
validate_ready_to_release() {
    # Check for uncommitted changes
    if [[ -n "$(git status --porcelain)" ]]; then
        echo "ERROR: Uncommitted changes"
        git status --short
        return 1
    fi

    # Check for unpushed commits
    git fetch origin --quiet
    local AHEAD=$(git log @{u}..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$AHEAD" -gt 0 ]]; then
        echo "ERROR: $AHEAD unpushed commit(s)"
        return 1
    fi

    echo "Ready to release"
    return 0
}
```

## Git Tag Operations

### Creating Tags

```bash
# Annotated tag (recommended)
git tag -a v1.0.0 -m "Release v1.0.0"

# With release notes
git tag -a v1.0.0 -m "Release v1.0.0

- Feature: Added user auth
- Fix: Memory leak resolved
- Chore: Updated deps"
```

### Pushing Tags

```bash
git push origin v1.0.0      # Single tag
git push --tags             # All tags
git push && git push --tags # Commits + tags
```

### Listing Tags

```bash
git tag -l                  # All tags
git tag -l "v1.*"           # Pattern match
git show v1.0.0             # Tag details
git describe --tags --abbrev=0  # Latest tag
```

### Deleting Tags

```bash
git tag -d v1.0.0                    # Local
git push origin :refs/tags/v1.0.0    # Remote
```

### Recreating Tags (Re-release)

```bash
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## Redeployment

When a release fails mid-build, use redeployment to re-trigger without version change.

### What Redeploy Does

1. Deletes tag locally (if exists)
2. Deletes tag on remote (if exists)
3. Recreates annotated tag at HEAD
4. Pushes new tag
5. CI/CD workflow re-triggers

### Manual Redeployment

```bash
VERSION="v0.1.5"

# Validate first
git status --porcelain | grep -q . && echo "Uncommitted changes!" && exit 1

# Delete and recreate
git tag -d "$VERSION" 2>/dev/null || true
git push origin ":refs/tags/$VERSION" 2>/dev/null || true
git tag -a "$VERSION" -m "Release $VERSION"
git push origin "refs/tags/$VERSION"
```

### When to Redeploy

- CI/CD workflow failed mid-build
- Build artifacts corrupted
- Code signing failed
- Secrets/environment updated
- Artifact upload failed

## Complete Release Workflow

### Manual Steps

```bash
# 1. Ensure clean state
git status  # No uncommitted changes

# 2. Get current version
CURRENT=$(jq -r '.version' package.json)

# 3. Calculate new version
IFS='.' read -r major minor patch <<< "$CURRENT"
NEW="${major}.${minor}.$((patch + 1))"

# 4. Update all version files
# (Use bump script or edit manually)

# 5. Commit
git add -A
git commit -m "chore: bump version to v${NEW}"

# 6. Tag
git tag -a "v${NEW}" -m "Release v${NEW}"

# 7. Push
git push && git push --tags
```

### Using This Project's Script

```bash
./app/scripts/bump-version.sh patch
git push && git push --tags
```

The script handles steps 2-6 automatically.

## Version Comparison in Bash

```bash
VERSION="1.2.3"
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Patch bump
PATCH=$((PATCH + 1))
NEW="${MAJOR}.${MINOR}.${PATCH}"  # 1.2.4

# Minor bump
MINOR=$((MINOR + 1)); PATCH=0
NEW="${MAJOR}.${MINOR}.${PATCH}"  # 1.3.0

# Major bump
MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0
NEW="${MAJOR}.${MINOR}.${PATCH}"  # 2.0.0
```

## Useful Commands

| Action | Command |
|--------|---------|
| Current version | `jq -r '.version' app/package.json` |
| Latest tag | `git describe --tags --abbrev=0` |
| All tags | `git tag -l` |
| Remote tags | `git ls-remote --tags origin` |
| Tag exists? | `git rev-parse v1.0.0 >/dev/null 2>&1 && echo "exists"` |
| Commits since tag | `git log v1.0.0..HEAD --oneline` |

## Common Gotchas

1. **Tag format must match workflow trigger** — If workflow triggers on `v*`, use `v0.1.0` not `0.1.0`.
2. **Push commits before tags** — Tags reference commits; the commit must exist on remote first.
3. **Version files must all match** — Mismatch causes build failures. Use the bump script.
4. **Cargo.lock needs regeneration** — After editing Cargo.toml, run `cargo update -p <pkg>`.
5. **Don't amend tagged commits** — Creates divergent history. Create new commit + tag instead.
6. **Annotated tags for releases** — Lightweight tags (`git tag v1.0.0`) lack metadata. Use `-a`.
7. **Tag deletion is not instant** — GitHub may cache tags briefly. Wait a moment before recreating.
8. **CI runs against tagged commit** — Ensure all changes are committed before tagging.
9. **Pre-release versions sort correctly** — `1.0.0-alpha.1 < 1.0.0-beta.1 < 1.0.0-rc.1 < 1.0.0`
10. **Conventional commits for bumps** — Use `chore: bump version to vX.Y.Z` or `release: vX.Y.Z`.
