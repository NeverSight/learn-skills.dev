---
name: releasing
description: Use when publishing a new version — bumping version numbers, creating git tags, and publishing GitHub Releases with changelogs.
---

# Releasing a New Version

## Overview

Bump versions, tag, and publish a GitHub Release with an auto-generated changelog. All version sources must stay in sync.

## Version Sources (must match)

| File | Field |
|------|-------|
| `.claude-plugin/plugin.json` | `version` |
| `.claude-plugin/marketplace.json` | `plugins[0].version` |
| Git tag | `vX.Y.Z` |

## Steps

### 1. Determine version bump

Check commits since last tag:
```bash
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```

Apply semver: **patch** for fixes, **minor** for features, **major** for breaking changes.

### 2. Update version in both JSON files

Edit `plugin.json` and `marketplace.json` to the new version string. Both must match exactly.

### 3. Commit version bump

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "chore: bump version to X.Y.Z"
```

### 4. Create tag and push

```bash
git tag vX.Y.Z
git push origin main --tags
```

### 5. Create GitHub Release

Generate changelog from commits since previous tag, then publish:

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes "$(cat <<'EOF'
## Changes

<changelog from git log>
EOF
)"
```

Group commits by type when there are enough to justify it:
- **Features** (`feat:`)
- **Fixes** (`fix:`)
- **Refactors** (`refactor:`)
- **Other** (everything else)

For small releases (< 5 commits), a flat list is fine.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| marketplace.json version not updated | Always update both JSON files together |
| Tag created before commit pushed | Push commit first, then tag, or use `--tags` |
| Changelog missing commits | Use `prev_tag..HEAD`, not `prev_tag..new_tag` before tagging |
