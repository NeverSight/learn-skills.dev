---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

# Git Release Skill

Create consistent releases and changelogs from merged PRs.

## What I do

- Draft release notes from merged PRs
- Propose a version bump based on semantic versioning
- Provide a copy-pasteable `gh release create` command
- Generate changelog entries

## When to use me

Use this when you are preparing a tagged release.

Ask clarifying questions if the target versioning scheme is unclear.

## Steps

1. Analyze recent commits and merged PRs since last tag
2. Categorize changes (feat, fix, chore, docs, etc.)
3. Generate proposed version bump (major, minor, patch)
4. Draft release notes in markdown format
5. Provide ready-to-use GitHub CLI command

## Example output

```
## Release Notes v1.2.3

### New Features
- Added user profile page (#123)
- Implemented dark mode toggle (#145)

### Bug Fixes
- Fixed login timeout issue (#156)
- Resolved mobile layout overflow (#167)

### Other Changes
- Updated dependencies (#189)
- Improved test coverage (#192)

To create this release:

```bash
gh release create v1.2.3 --title "v1.2.3" --notes-file CHANGELOG.md
```