---
name: exploring-github
description: "Explore and understand GitHub repositories using the gh CLI. Use when asked to browse repos, read files, search code, analyze issues/PRs/commits/releases, or understand codebases on GitHub. Replaces MCP-based GitHub tools with zero dependencies beyond gh."
---

# Exploring GitHub

Explore and understand GitHub repositories using the `gh` CLI — a zero-dependency alternative to MCP-based GitHub context servers like gitctx.

## Prerequisites

- `gh` CLI installed and authenticated
- Works with any MCP client: Claude Code, Amp, Pi, or any agent with shell access

If `gh` is not found or not authenticated, stop and ask the user to install/authenticate it. If a command fails for a non-blocking reason (e.g., rate limit on a non-critical call), skip it and continue.

## Context State

Maintain a mental "current repo" context. Once the user specifies a repo (e.g., `rust-lang/rust`), use `-R owner/repo` on all subsequent `gh` commands. Track:

- **Repo**: `OWNER/REPO` — always pass via `-R`
- **Branch**: default branch unless user switches — pass via `--branch` or `@ref` where applicable
- **Path prefix**: for scoped file navigation

## Tool Reference

### 1. Repository Discovery & Metadata

**Find/search repos:**
```bash
gh search repos "<query>" --sort stars --limit 10 --json fullName,description,stargazersCount,language,updatedAt
```

**View repo metadata:**
```bash
gh repo view OWNER/REPO --json name,description,defaultBranchRef,isPrivate,diskUsage,forkCount,stargazerCount,languages,homepageUrl
```

**List branches:**
```bash
gh api repos/OWNER/REPO/branches --paginate --jq '.[].name'
```

### 2. Code Navigation

**List directory contents (root or subdir):**
```bash
gh api repos/OWNER/REPO/contents/PATH --jq '.[] | "\(.type)\t\(.name)\t\(.size // "")"' -H "Accept: application/vnd.github.v3+json"
```
For a specific branch:
```bash
gh api "repos/OWNER/REPO/contents/PATH?ref=BRANCH" --jq '.[] | "\(.type)\t\(.name)\t\(.size // "")"'
```

**Read a file:**
```bash
gh api repos/OWNER/REPO/contents/PATH -H "Accept: application/vnd.github.v3.raw" 2>&1 | head -500
```
For a specific branch:
```bash
gh api "repos/OWNER/REPO/contents/PATH?ref=BRANCH" -H "Accept: application/vnd.github.v3.raw" 2>&1 | head -500
```

**Read multiple files (run in parallel):**
Read each file with the command above. Run multiple Bash calls in parallel for efficiency.

**Get full repo tree (recursive):**
```bash
gh api repos/OWNER/REPO/git/trees/BRANCH?recursive=1 --jq '.tree[] | select(.type=="blob") | .path' | head -200
```

**Search code in a repo:**
```bash
gh search code "<query>" --repo OWNER/REPO --limit 20 --json path,textMatches
```

**Search code globally:**
```bash
gh search code "<query>" --language LANG --limit 20 --json repository,path,textMatches
```

### 3. Issues

**List/search issues:**
```bash
gh issue list -R OWNER/REPO --state all --search "<query>" --limit 20 --json number,title,state,author,labels,createdAt,updatedAt
```

**Get issue details:**
```bash
gh issue view NUMBER -R OWNER/REPO --json number,title,state,body,author,labels,assignees,comments,createdAt,closedAt
```

**List issue comments:**
```bash
gh issue view NUMBER -R OWNER/REPO --json comments --jq '.comments[] | "[\(.author.login) \(.createdAt)]\n\(.body)\n---"'
```

### 4. Pull Requests

**List/search PRs:**
```bash
gh pr list -R OWNER/REPO --state all --search "<query>" --limit 20 --json number,title,state,author,labels,baseRefName,headRefName,createdAt,mergedAt
```

**Get PR details:**
```bash
gh pr view NUMBER -R OWNER/REPO --json number,title,state,body,author,labels,assignees,comments,reviews,additions,deletions,changedFiles,baseRefName,headRefName,mergedAt,mergedBy
```

**Get PR diff:**
```bash
gh pr diff NUMBER -R OWNER/REPO
```

**List PR review comments:**
```bash
gh api repos/OWNER/REPO/pulls/NUMBER/comments --jq '.[] | "[\(.user.login) \(.created_at) \(.path):\(.line // .original_line)]\n\(.body)\n---"'
```

### 5. Commits

**List commits:**
```bash
gh api repos/OWNER/REPO/commits --paginate -f sha=BRANCH -f per_page=20 --jq '.[] | "\(.sha[:8]) \(.commit.author.date) \(.commit.author.name): \(.commit.message | split("\n")[0])"'
```

With path filter:
```bash
gh api repos/OWNER/REPO/commits -f sha=BRANCH -f path=PATH -f per_page=20 --jq '.[] | "\(.sha[:8]) \(.commit.author.date) \(.commit.author.name): \(.commit.message | split("\n")[0])"'
```

With author filter:
```bash
gh api repos/OWNER/REPO/commits -f sha=BRANCH -f author=USERNAME -f per_page=20 --jq '.[] | "\(.sha[:8]) \(.commit.author.date): \(.commit.message | split("\n")[0])"'
```

**Get commit details:**
```bash
gh api repos/OWNER/REPO/commits/SHA --jq '{sha: .sha, message: .commit.message, author: .commit.author, files: [.files[] | {filename, status, additions, deletions, patch}]}'
```

**Compare commits/refs:**
```bash
gh api repos/OWNER/REPO/compare/BASE...HEAD --jq '{ahead_by, behind_by, total_commits: .total_commits, files: [.files[] | {filename, status, additions, deletions}], commits: [.commits[] | {sha: .sha[:8], message: .commit.message | split("\n")[0]}]}'
```

**Blame a file:**
```bash
gh api graphql -f query='
  query {
    repository(owner: "OWNER", name: "REPO") {
      object(expression: "BRANCH:PATH") {
        ... on Blob {
          blame {
            ranges {
              startingLine
              endingLine
              commit {
                abbreviatedOid
                message
                author { name date }
              }
            }
          }
        }
      }
    }
  }
' --jq '.data.repository.object.blame.ranges[] | "L\(.startingLine)-\(.endingLine) \(.commit.abbreviatedOid) \(.commit.author.name) (\(.commit.author.date)): \(.commit.message | split("\n")[0])"'
```

### 6. Releases

**List releases:**
```bash
gh release list -R OWNER/REPO --limit 20 --json tagName,name,publishedAt,isPrerelease,isDraft,isLatest
```

**Get release details:**
```bash
gh release view TAG -R OWNER/REPO --json tagName,name,body,publishedAt,author,assets,isPrerelease,isDraft
```

**Compare releases (commits between two tags):**
```bash
gh api repos/OWNER/REPO/compare/TAG1...TAG2 --jq '{total_commits: .total_commits, commits: [.commits[] | {sha: .sha[:8], message: .commit.message | split("\n")[0]}], files_changed: [.files[] | .filename]}'
```

### 7. Repository Insights

**Top contributors:**
```bash
gh api repos/OWNER/REPO/contributors -f per_page=20 --jq '.[] | "\(.login): \(.contributions) commits"'
```

**Repository stats (commit activity):**
```bash
gh api repos/OWNER/REPO/stats/participation --jq '"Owner commits (last 52 weeks): \(.owner | add)\nAll commits (last 52 weeks): \(.all | add)"'
```

**Language breakdown:**
```bash
gh api repos/OWNER/REPO/languages
```

**Dependency graph (if available):**
```bash
gh api repos/OWNER/REPO/dependency-graph/sbom --jq '.sbom.packages[:30][] | "\(.name) \(.versionInfo // "unknown")"'
```

## Usage Recommendation

This skill is best used via a **subagent** (e.g. Claude Code's Task tool, or any agent that supports delegated subtasks). GitHub exploration generates a lot of intermediate output — file trees, code snippets, API responses — that is useful for answering the question but clutters the main conversation. Delegating to a subagent keeps that noise isolated and returns only the synthesized answer.

## Exploration Strategy

Follow a **broad-then-narrow** approach:

1. **Orient** — start with repo metadata (`gh repo view`) and file tree to understand project shape
2. **Survey** — read key entry points: README, config files (package.json, Cargo.toml, go.mod), main entry files
3. **Target** — use code search and directory listing to locate the specific area asked about
4. **Deep-read** — read the relevant files thoroughly; do not skim or summarize code you have not actually read
5. **Cross-reference** — connect findings across concerns (trace a function from definition to usage to tests to related PRs/issues)

Run independent operations in parallel whenever possible. For example, read multiple files at once, or search code while listing a directory. When exploring unfamiliar territory, adjust your investigation based on what you discover — do not follow a rigid script.

### Codebase Understanding

1. `gh repo view` — get overview, default branch, languages
2. `gh api .../git/trees/BRANCH?recursive=1` — get file tree
3. Read key files: README, config files, entry points
4. `gh search code` — find specific patterns or implementations
5. Synthesize architecture understanding

### Issue/PR Triage

1. `gh issue list` / `gh pr list` with filters
2. `gh issue view` / `gh pr view` for details
3. `gh pr diff` for code changes
4. Cross-reference with commits and blame

### Release Analysis

1. `gh release list` — recent releases
2. `gh api .../compare/TAG1...TAG2` — diff between releases
3. Check linked issues/PRs for changelog context

## Output Guidelines

- Always use `--json` + `--jq` for structured, token-efficient output
- Pipe large outputs through `head -N` to avoid flooding context
- For file contents, limit to 500 lines unless the user requests more
- Lead with the answer — state the key finding first, then support with details
- Include evidence — reference specific files, line ranges, commit SHAs, issue/PR numbers
- Use Mermaid diagrams when explaining architecture, data flow, or component relationships
- Quantify when possible — "47 files changed across 3 packages" not "many files changed"
- When mentioning files, link to them on GitHub: `[src/auth.rs](https://github.com/OWNER/REPO/blob/BRANCH/src/auth.rs#L10-L25)`

## Error Handling

- Rate-limited? Use `gh api -H "Accept: ..." --cache 1h` for cacheable requests
- 404 errors likely mean private repo without access or wrong path — verify repo name
- Large repos: use tree + targeted reads instead of recursive listing
