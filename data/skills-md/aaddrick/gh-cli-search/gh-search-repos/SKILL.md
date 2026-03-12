---
name: gh-search-repos
description: Use when searching for repositories across GitHub - provides syntax for filtering by stars, forks, language, topics, license, archived status, and all repository attributes
---

# GitHub CLI: Search Repositories

## Overview

Search for repositories **across GitHub** using `gh search repos`. Filter by stars, forks, language, topics, license, and more.

## When to Use This Skill

Use this skill when searching for repositories across GitHub:
- Finding repositories by popularity (stars/forks)
- Searching by programming language or topics
- Finding repos with good first issues
- Filtering by license or archived status
- Searching in specific organizations or by owner
- Need to exclude certain results (requires `--` flag)

## Syntax

```bash
gh search repos [<query>] [flags]
```

## Key Flags Reference

### Repository Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--language <string>` | Programming language | `--language python` |
| `--topic <strings>` | Repository topics | `--topic machine-learning` |
| `--license <strings>` | License type | `--license mit` |
| `--archived {true\|false}` | Archived state | `--archived false` |
| `--owner <strings>` | Repository owner | `--owner github` |
| `--visibility <string>` | Visibility: public, private, internal | `--visibility public` |

### Popularity Metrics

| Flag | Purpose | Example |
|------|---------|---------|
| `--stars <number>` | Star count | `--stars ">1000"` |
| `--forks <number>` | Fork count | `--forks ">100"` |
| `--followers <number>` | Follower count | `--followers ">50"` |
| `--size <string>` | Size in KB | `--size "100..1000"` |

### Issue Counts

| Flag | Purpose | Example |
|------|---------|---------|
| `--good-first-issues <number>` | "Good first issue" label count | `--good-first-issues ">=5"` |
| `--help-wanted-issues <number>` | "Help wanted" label count | `--help-wanted-issues ">=3"` |

### Date Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--created <date>` | Creation date | `--created ">2024-01-01"` |
| `--updated <date>` | Last update date | `--updated ">2024-06-01"` |

### Search Scope

| Flag | Purpose | Example |
|------|---------|---------|
| `--match <strings>` | Search in: name, description, readme | `--match name` |
| `--include-forks {false\|true\|only}` | Include/exclude forks | `--include-forks false` |

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by: stars, forks, updated, etc. | `--sort stars` |
| `--order <string>` | Sort direction: asc or desc | `--order desc` |
| `--json <fields>` | JSON output | `--json name,stargazersCount,language` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

`createdAt`, `defaultBranch`, `description`, `forksCount`, `fullName`, `hasDownloads`, `hasIssues`, `hasPages`, `hasProjects`, `hasWiki`, `homepage`, `id`, `isArchived`, `isDisabled`, `isFork`, `isPrivate`, `language`, `license`, `name`, `openIssuesCount`, `owner`, `pushedAt`, `size`, `stargazersCount`, `updatedAt`, `url`, `visibility`, `watchersCount`

## Exclusion Syntax (Critical!)

When using inline query exclusions (negations with `-`), you MUST use the `--` separator:

✅ Correct: `gh search repos -- "search-terms -qualifier:value"`
❌ Wrong: `gh search repos "search-terms" --flag=-value`
❌ Wrong: `gh search repos "search-terms" --flag=!value`
❌ Wrong: `gh search repos --language=-Go`

**Examples:**
- `gh search repos -- "cli -language:go"` (exclude language)
- `gh search repos -- "starter -archived:true"` (exclude archived)
- `gh search repos -- "web -topic:deprecated"` (exclude topic)
- `gh search repos -- "library -license:gpl-3.0"` (exclude license)

**Why the `--` separator is required:**
The `--` tells the shell to stop parsing flags and treat everything after it as arguments. Without it, `-qualifier:value` inside quotes may be misinterpreted.

## Critical Syntax Rules

### When to Use Flag Syntax vs Query Syntax

**Decision Tree:**
```
Does your search include:
  - Any exclusions (NOT, minus, without, except)?  → Use Query Syntax with `--`
  - Complex boolean logic (OR, AND)?              → Use Query Syntax with `--`

Otherwise:
  - Simple positive filters only?                  → Use Flag Syntax
```

**Flag Syntax** (for positive filters):
```bash
gh search repos "cli" --language go --stars ">100"
```

**Query Syntax with `--`** (required for exclusions):
```bash
gh search repos -- "cli -language:javascript -archived:true"
```

**⚠️ NEVER mix both syntaxes in a single command!**

### 1. Exclusions and Negations

**CRITICAL:** When excluding results, you MUST use query syntax with the `--` separator.

#### Exclusion Syntax Rules:
1. Use the `--` separator before your query
2. Use `-qualifier:value` format (dash prefix for negation)
3. Quote the entire query string

#### Examples:

**Single exclusion:**
```bash
# Exclude specific language
gh search repos -- "web framework -language:javascript"

# Exclude archived repos
gh search repos -- "cli tool -archived:true"
```

**Multiple exclusions:**
```bash
# Exclude multiple languages
gh search repos -- "game engine -language:javascript -language:python"

# Exclude archived and small repos
gh search repos -- "starter -archived:true -stars:<10"
```

**Combine with positive filters using flags:**
```bash
# Wrong - mixing syntaxes:
gh search repos "cli" --language go -archived:true  # ❌

# Correct - use query syntax for everything when excluding:
gh search repos -- "cli language:go -archived:true"  # ✅
```

**PowerShell exclusions:**
```powershell
# Use --% to prevent PowerShell parsing
gh --% search repos -- "cli -language:javascript"
```

#### Common Exclusion Patterns:

| User Request | Command |
|--------------|---------|
| "Find repos but not archived" | `gh search repos -- "starter -archived:true"` |
| "Repos excluding specific language" | `gh search repos -- "web framework -language:php"` |
| "Repos not in specific topic" | `gh search repos -- "cli -topic:deprecated"` |
| "Repos excluding multiple languages" | `gh search repos -- "game -language:javascript -language:css"` |
| "Repos not forks" | `gh search repos -- "template -is:fork"` (or use `--include-forks false`) |
| "Repos excluding low stars" | `gh search repos -- "framework -stars:<100"` |
| "Repos not with specific license" | `gh search repos -- "library -license:gpl-3.0"` |

### 2. Special Values

- Multiple topics: `--topic unix,terminal`
- Boolean flags: `--archived false` or `--archived true`
- Fork inclusion: `--include-forks false|true|only`

### 3. Quoting Rules

**Multi-word search:**
```bash
gh search repos "machine learning"
```

**Comparison operators need quotes:**
```bash
gh search repos "python" --stars ">1000"
```

**Ranges use quotes:**
```bash
gh search repos "cli" --stars "100..500"
```

## Common Use Cases

**Find popular Python repos:**
```bash
gh search repos "data science" --language python --stars ">5000"
```

**Find repos with good first issues:**
```bash
gh search repos --language javascript --good-first-issues ">=10"
```

**Find recently updated repos:**
```bash
gh search repos "react" --updated ">2024-01-01" --stars ">100"
```

**Find repos by topic:**
```bash
gh search repos --topic machine-learning --language python
```

**Find repos by license:**
```bash
gh search repos "web framework" --license mit,apache-2.0
```

**Exclude archived repos:**
```bash
gh search repos "cli tool" --archived false
```

**Find repos by organization:**
```bash
gh search repos --owner microsoft --visibility public
```

**Exclude forks:**
```bash
gh search repos "starter" --include-forks false
```

**Find only forks:**
```bash
gh search repos "template" --include-forks only
```

**Find repos in star range:**
```bash
gh search repos "game engine" --stars "100..1000"
```

**Exclude specific language:**
```bash
gh search repos -- "cli -language:go"
```

**Search in name only:**
```bash
gh search repos "awesome" --match name
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `--language="NOT javascript"` or `--archived=-true` | Flag syntax doesn't support negation | Use query: `-- "-language:javascript"` or `-- "-archived:true"` |
| `gh search repos cli -language:js` | `-language` interpreted as flag | Use `--`: `-- "cli -language:js"` |
| `"cli NOT language:js"` | `NOT` keyword doesn't work | Use `-`: `-- "cli -language:js"` |
| Mixing syntaxes: `--stars ">100" "cli -language:js"` | Can't mix flags with query qualifiers | Use query for all: `-- "cli stars:>100 -language:js"` |
| Not quoting comparisons | Shell interprets `>` | Quote: `--stars ">1000"` |
| `--archived archived` | Invalid value | Use boolean: `--archived true` or `false` |
| Not quoting multi-word search | Searches separately | Quote: `"machine learning"` |
| Using `@` with owner | Invalid syntax | Drop `@`: `--owner github` |
| PowerShell without `--%` | Breaks with exclusions | Add: `gh --%` |

## Installation Check

If `gh` command not found:
```bash
# Check if gh is installed
which gh

# Install: https://cli.github.com/manual/installation
```

If not authenticated:
```bash
# Authenticate with GitHub
gh auth login
```

## Comparison Operators

- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal
- `..` - Range: `100..1000` or `2024-01-01..2024-12-31`

## Common Licenses

- `mit` - MIT License
- `apache-2.0` - Apache License 2.0
- `gpl-3.0` - GNU GPL v3
- `bsd-2-clause` - BSD 2-Clause
- `bsd-3-clause` - BSD 3-Clause
- `mpl-2.0` - Mozilla Public License 2.0
- `isc` - ISC License

## Match Field Options

- `name` - Search repository names only
- `description` - Search descriptions only
- `readme` - Search README files only

Example: `gh search repos "documentation" --match readme`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-for-repositories
- For searching other resources: `gh-search-code`, `gh-search-commits`, `gh-search-issues`, `gh-search-prs`
