---
name: gh-cli
description: GitHub CLI for remote repository analysis, file fetching, codebase comparison, and discovering trending code/repos. Use when analyzing repos without cloning, comparing codebases, or searching for popular GitHub projects.
---

# GitHub CLI - Remote Analysis & Discovery

Remote repository operations, codebase comparison, and code discovery without cloning.

## When to Use

- Analyze repositories without cloning
- Compare codebases side-by-side
- Fetch specific files from any repo
- Find trending repositories and code patterns
- Search code across GitHub

## Quick Operations

### Fetch a file remotely

```bash
gh api repos/OWNER/REPO/contents/path/file.ts | jq -r '.content' | base64 -d
```

### Get directory listing

```bash
gh api repos/OWNER/REPO/contents/PATH
```

### Search code

```bash
gh search code "pattern" --language=typescript
```

### Find trending repos

```bash
gh search repos --language=rust --sort stars --order desc
```

## Compare Two Codebases

Systematic workflow for comparing repositories to identify similarities and differences.

**Example use**: "Compare solana-fm/explorer-kit and tenequm/solana-idls"

### Step 1: Fetch directory structures

```bash
gh api repos/OWNER-A/REPO-A/contents/PATH > repo1.json
gh api repos/OWNER-B/REPO-B/contents/PATH > repo2.json
```

If comparing a monorepo package, specify the path (e.g., `packages/explorerkit-idls`).

### Step 2: Compare file lists

```bash
jq -r '.[].name' repo1.json > repo1-files.txt
jq -r '.[].name' repo2.json > repo2-files.txt
diff repo1-files.txt repo2-files.txt
```

Shows files unique to each repo and common files.

### Step 3: Fetch key files for comparison

Compare package dependencies:

```bash
gh api repos/OWNER-A/REPO-A/contents/package.json | jq -r '.content' | base64 -d > repo1-pkg.json
gh api repos/OWNER-B/REPO-B/contents/package.json | jq -r '.content' | base64 -d > repo2-pkg.json
```

Compare main entry points:

```bash
gh api repos/OWNER-A/REPO-A/contents/src/index.ts | jq -r '.content' | base64 -d > repo1-index.ts
gh api repos/OWNER-B/REPO-B/contents/src/index.ts | jq -r '.content' | base64 -d > repo2-index.ts
```

### Step 4: Analyze differences

Compare the fetched files to identify:

**API Surface**
- What functions/classes are exported?
- Are the APIs similar or completely different?

**Dependencies**
- Shared dependencies (same approach)
- Different dependencies (different implementation)

**Unique Features**
- Features only in repo1
- Features only in repo2

For detailed comparison strategies, see [references/comparison.md](references/comparison.md).

## Discover Trending Content

### Find trending repositories

```bash
# Most starred repos
gh search repos --sort stars --order desc --limit 20

# Trending in specific language
gh search repos --language=rust --sort stars --order desc

# Recently popular (created in last month)
gh search repos "created:>2024-10-01" --sort stars --order desc

# Trending in specific topic
gh search repos "topic:machine-learning" --sort stars --order desc
```

### Discover popular code patterns

```bash
# Find popular implementations
gh search code "function useWallet" --language=typescript --sort indexed

# Find code in popular repos only
gh search code "implementation" "stars:>1000"

# Search specific organization
gh search code "authentication" --owner=anthropics
```

For complete discovery queries and patterns, see [references/discovery.md](references/discovery.md).

## Search Basics

### Code search

```bash
# Search across all repositories
gh search code "API endpoint" --language=python

# Search in specific organization
gh search code "auth" --owner=anthropics

# Exclude results with negative qualifiers
gh search issues -- "bug report -label:wontfix"
```

### Issue & PR search

```bash
# Find open bugs
gh search issues --label=bug --state=open

# Search assigned issues
gh search issues --assignee=@me --state=open
```

For advanced search syntax, see [references/search.md](references/search.md).

## Special Syntax

### Field name inconsistencies

**IMPORTANT:** GitHub CLI uses inconsistent field names across commands:

| Field | `gh repo view` | `gh search repos` |
|-------|----------------|-------------------|
| Stars | `stargazerCount` | `stargazersCount` |
| Forks | `forkCount` | `forksCount` |

**Examples:**

```bash
# ✅ Correct for gh repo view
gh repo view owner/repo --json stargazerCount,forkCount

# ✅ Correct for gh search repos
gh search repos "query" --json stargazersCount,forksCount
```

### Excluding search results

When using negative qualifiers (like `-label:bug`), use `--` to prevent the hyphen from being interpreted as a flag:

```bash
gh search issues -- "query -label:bug"
```

For more syntax gotchas, see [references/syntax.md](references/syntax.md).

## Advanced Workflows

For detailed documentation on specific workflows:

**Core Workflows:**
- [remote-analysis.md](references/remote-analysis.md) - Advanced file fetching patterns
- [comparison.md](references/comparison.md) - Complete codebase comparison guide
- [discovery.md](references/discovery.md) - All trending and discovery queries
- [search.md](references/search.md) - Advanced search syntax
- [syntax.md](references/syntax.md) - Special syntax and command quirks

**GitHub Operations:**
- [repositories.md](references/repositories.md) - Repository operations
- [pull_requests.md](references/pull_requests.md) - PR workflows
- [issues.md](references/issues.md) - Issue management
- [actions.md](references/actions.md) - GitHub Actions
- [releases.md](references/releases.md) - Release management

**Setup & Configuration:**
- [getting_started.md](references/getting_started.md) - Installation and auth
- [other.md](references/other.md) - Environment variables, aliases, config
- [extensions.md](references/extensions.md) - CLI extensions

## Resources

- Official docs: https://cli.github.com/manual/
- GitHub CLI: https://github.com/cli/cli
- Search syntax: https://docs.github.com/en/search-github
