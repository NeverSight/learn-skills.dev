---
name: changelog
description: Generate a changelog from git history between two refs, grouped by type (features, fixes, chores).
allowed-tools: Bash, Read, Grep
argument-hint: "<from-ref>..<to-ref> [--format md|plain] [--repo owner/repo]"
---

Generate a structured changelog from git commit history between two refs.

## Process

Parse `$ARGUMENTS`:
- Required: ref range like `v1.0..v1.1`, `main..HEAD`, `abc123..def456`, or a single ref (implies `<ref>..HEAD`)
- `--format md|plain`: output format (default: `md`)
- `--repo owner/repo`: if specified, link to GitHub commits/PRs

1. **Get the commit log**:
   ```bash
   git log <from>..<to> --pretty=format:"%H|%s|%an|%aI" --no-merges
   ```

   Also get merge commits separately to extract PR numbers:
   ```bash
   git log <from>..<to> --pretty=format:"%H|%s|%an|%aI" --merges
   ```

2. **Categorize commits** by their prefix or content:

   | Category | Patterns |
   |---|---|
   | Features | `feat:`, `add:`, `new:`, commits that add new files/capabilities |
   | Fixes | `fix:`, `bugfix:`, `hotfix:`, `patch:` |
   | Breaking | `BREAKING:`, `breaking:`, `!:` suffix in conventional commits |
   | Chores | `chore:`, `ci:`, `build:`, `deps:`, `bump:` |
   | Docs | `doc:`, `docs:` |
   | Refactor | `refactor:`, `refact:`, `cleanup:` |
   | Other | anything that doesn't match above |

   If commits don't follow conventional commit format, do best-effort categorization based on the message content.

3. **Extract PR references** from merge commit messages (e.g., `Merge pull request #123`) and link them if `--repo` is specified.

4. **Output format** (markdown):

```markdown
# Changelog: <from> → <to>

**Period:** <earliest date> to <latest date>
**Commits:** <count> (excluding merges)

## Breaking Changes
- <description> — <author> (<hash short>) [#PR]

## Features
- <description> — <author> (<hash short>) [#PR]

## Fixes
- <description> — <author> (<hash short>) [#PR]

## Chores
- <description> — <author> (<hash short>) [#PR]

## Other
- <description> — <author> (<hash short>) [#PR]
```

5. Omit empty categories. If `--repo` is specified, make commit hashes and PR numbers into GitHub links.

## Notes

- If the ref range produces more than 200 commits, summarize instead of listing each one.
- If `--repo` is not specified, try to detect from `git remote get-url origin`.
- Strip conventional commit prefixes from the description for cleaner output.
