---
name: release-notes
description: Generate release notes from commits since last tag
disable-model-invocation: true
---

Generate release notes for arcfetch:

1. Get the latest tag: `git describe --tags --abbrev=0`
2. List commits since that tag: `git log <tag>..HEAD --oneline`
3. Categorize by conventional commit type:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `chore:` - Maintenance
   - `docs:` - Documentation
   - `refactor:` - Code improvements
4. Summarize user-facing changes
5. Note: per releaseRules in package.json, breaking changes trigger a minor bump (not major)
6. Output a formatted summary suitable for a GitHub release
