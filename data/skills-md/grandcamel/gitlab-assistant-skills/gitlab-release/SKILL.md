---
name: "gitlab-release"
description: "GitLab release operations. ALWAYS use this skill when user wants to: (1) list releases, (2) view release details, (3) create new releases, (4) upload assets, (5) delete releases."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Release Skill

Release operations for GitLab using the `glab` CLI.

## Quick Reference

| Operation | Command | Risk |
|-----------|---------|:----:|
| List releases | `glab release list` | - |
| View release | `glab release view <tag>` | - |
| Create release | `glab release create <tag>` | ⚠️ |
| Upload assets | `glab release upload <tag> <files>` | ⚠️ |
| Download assets | `glab release download <tag>` | - |
| Delete release | `glab release delete <tag>` | ⚠️⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to work with releases
- User mentions "release", "version", "changelog", "tag" (for releases)
- User wants to publish or distribute software versions

**NEVER use when:**
- User wants to manage git tags directly (use git commands)
- User wants CI/CD operations (use gitlab-ci instead)

## Available Commands

### List Releases

```bash
glab release list [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-P, --per-page=<n>` | Results per page |
| `--all` | Get all releases |

**Examples:**
```bash
# List all releases
glab release list

# List with more results
glab release list --per-page=50
```

### View Release Details

```bash
glab release view <tag> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-w, --web` | Open release in browser |

**Examples:**
```bash
# View release details
glab release view v1.0.0

# Open release in browser
glab release view v1.0.0 --web
```

### Create Release

```bash
glab release create <tag> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-n, --notes=<notes>` | Release notes |
| `-F, --notes-file=<file>` | Read release notes from file |
| `-N, --name=<name>` | Release name (defaults to tag) |
| `-r, --ref=<ref>` | Git ref to create tag from (if tag doesn't exist) |
| `-a, --assets-links=<json>` | JSON array of asset links |
| `--milestone=<titles>` | Milestone titles to associate |

**Examples:**
```bash
# Create simple release
glab release create v1.0.0

# Create with release notes
glab release create v1.0.0 -n "## What's New
- Feature A
- Bug fix B"

# Create with notes from file
glab release create v1.0.0 -F CHANGELOG.md

# Create with name and milestone
glab release create v1.0.0 -N "Version 1.0.0" --milestone="Sprint 5"

# Create from specific commit
glab release create v1.0.0 -r abc123def
```

### Upload Assets

```bash
glab release upload <tag> <file>... [options]
```

Upload files as release assets.

**Examples:**
```bash
# Upload single file
glab release upload v1.0.0 ./dist/app.zip

# Upload multiple files
glab release upload v1.0.0 ./dist/*.tar.gz

# Upload with custom name
glab release upload v1.0.0 ./build/app.exe#windows-binary
```

### Download Assets

```bash
glab release download <tag> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-D, --dir=<dir>` | Download directory |
| `-n, --asset-name=<name>` | Download specific asset by name |

**Examples:**
```bash
# Download all assets
glab release download v1.0.0

# Download to specific directory
glab release download v1.0.0 -D ./downloads/

# Download specific asset
glab release download v1.0.0 -n "app.zip"
```

### Delete Release

```bash
glab release delete <tag> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-y, --yes` | Skip confirmation |
| `--with-tag` | Also delete the associated tag |

**Warning:** This permanently deletes the release.

**Examples:**
```bash
# Delete release (prompts for confirmation)
glab release delete v1.0.0

# Delete release and tag
glab release delete v1.0.0 --with-tag

# Delete without confirmation
glab release delete v1.0.0 --yes
```

## Common Workflows

### Workflow 1: Standard Release

```bash
# 1. Ensure all changes are merged
glab mr list --state=opened

# 2. Verify CI passes
glab ci status --branch=main

# 3. Create release with changelog
glab release create v1.2.0 -F CHANGELOG.md -N "Version 1.2.0"

# 4. Upload binaries
glab release upload v1.2.0 ./dist/*
```

### Workflow 2: Pre-release

```bash
# Create pre-release version
glab release create v2.0.0-beta.1 \
  -n "Beta release for testing. Not for production use."
```

### Workflow 3: Hotfix Release

```bash
# 1. Create release from hotfix branch
glab release create v1.0.1 -r hotfix/critical-fix \
  -n "Hotfix release:
- Fixed critical security issue"

# 2. Upload patched binaries
glab release upload v1.0.1 ./dist/*
```

## Release Notes Best Practices

Structure your release notes:

```markdown
## What's New
- Feature descriptions

## Bug Fixes
- Fix descriptions

## Breaking Changes
- Migration notes

## Contributors
- @username
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid/expired token | Run `glab auth login` |
| Tag already exists | Duplicate release | Use different tag or delete existing |
| Release not found | Invalid tag | Verify tag with `glab release list` |
| Upload failed | File not found | Check file path exists |

## Related Documentation

- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
