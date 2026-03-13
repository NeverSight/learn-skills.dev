---
name: gh-search
description: Use when searching GitHub via CLI for issues, PRs, repos, code, or commits - provides correct syntax for exclusions, qualifiers, quoting, and platform-specific handling to avoid command failures
---

# GitHub CLI Search

## Overview

Search GitHub from the command line using `gh search` subcommands. The key principle: **Always use `--` before queries with exclusions** to prevent shell interpretation of `-` prefixes.

## When to Use

Use this skill when:
- Searching GitHub via `gh` CLI for issues, PRs, repos, code, or commits
- User requests searches with exclusions (NOT, minus prefix)
- Constructing complex queries with multiple qualifiers
- Queries contain spaces or special characters

## Subcommands Quick Reference

| Subcommand | Use For | Common Flags |
|------------|---------|--------------|
| `gh search issues` | Issues (add `--include-prs` for PRs too) | `--label`, `--state`, `--author`, `--assignee` |
| `gh search prs` | Pull requests only | `--label`, `--state`, `--author`, `--draft`, `--merged` |
| `gh search repos` | Repositories | `--language`, `--stars`, `--topic`, `--owner` |
| `gh search code` | Code within files | `--repo`, `--language`, `--filename` |
| `gh search commits` | Commit messages | `--repo`, `--author`, `--committer` |

## Critical Syntax Rules

### 1. Exclusions Require `--` Flag

**Unix/Linux/Mac:**
```bash
gh search issues -- "bug -label:duplicate"
```

**PowerShell:**
```powershell
gh --% search issues -- "bug -label:duplicate"
```

**Why:** The `-` prefix gets interpreted as a command flag without `--`. PowerShell needs `--% ` to stop parsing.

### 2. Quoting Rules

**Multi-word queries need quotes:**
```bash
gh search issues "memory leak"
```

**Entire query with spaces should be quoted:**
```bash
gh search issues "bug label:urgent created:>2024-01-01"
```

**Qualifier values with spaces need inner quotes:**
```bash
gh search prs -- 'security label:"bug fix"'
```

### 3. Qualifier Syntax

**Inline qualifiers** (use within search query):
```bash
gh search repos "react stars:>1000 language:typescript"
```

**Flag-based** (use as separate flags):
```bash
gh search repos "react" --language typescript --stars ">1000"
```

**Can mix both:**
```bash
gh search issues "crash" --label bug created:>2024-01-01
```

## Common Qualifiers

### Comparison Operators
- `>`, `>=`, `<`, `<=` - Numeric: `stars:>100`, `comments:>=5`
- `..` - Ranges: `stars:10..50`, `created:2024-01-01..2024-12-31`

### Special Values
- `@me` - Current user: `author:@me`, `assignee:@me`, `owner:@me`
- Dates use ISO8601: `created:>2024-01-01` or `created:2024-01-01..2024-12-31`

### Field-Specific Search
- `in:title` - Search in title only
- `in:body` - Search in body only
- `in:comments` - Search in comments only

### Exclusions
- `-qualifier:value` - Exclude: `-label:bug`, `-language:javascript`
- `NOT` keyword - For words only: `"hello NOT world"`

## Examples

**Find your open issues without bug label:**
```bash
gh search issues -- "is:open author:@me -label:bug"
```

**Find popular Python ML repos updated recently:**
```bash
gh search repos "machine learning" --language python --stars ">1000" --updated ">2024-01-01"
```

**Find PRs with specific label and text:**
```bash
gh search prs -- 'security label:"bug fix" created:>2024-01-01'
```

**Search code in organization repos:**
```bash
gh search code "TODO" --owner myorg --language javascript
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `gh search issues -label:bug` | `-label` interpreted as flag | Add `--`: `gh search issues -- "-label:bug"` |
| `gh search repos machine learning` | Searches "machine" OR "learning" | Quote it: `"machine learning"` |
| `in:title` outside quotes | Shell interprets `:` oddly | Include in query: `"crash in:title"` |
| Mixing `@` with value | Invalid syntax | Use `@me` or username, not both: `author:@me` ✓, `author:@username` ✗ (drop @) |
| PowerShell without `--%` | Parsing breaks with exclusions | Add `gh --%` before command |

## Output Options

All subcommands support:
- `--limit <n>` - Max results (default: 30, max: 1000)
- `--json <fields>` - JSON output for scripting
- `--web` - Open results in browser
- `--sort <field>` - Sort by: comments, created, reactions, updated, stars, etc.
- `--order asc|desc` - Sort direction (default: desc)

## Real-World Impact

Correct syntax prevents:
- Command failures from misinterpreted flags
- Missing results from incorrect exclusions
- Errors from unquoted spaces
- Platform-specific parsing issues
