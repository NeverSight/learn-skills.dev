---
name: github
description: Interact with GitHub repositories, issues, pull requests, and code via the GitHub MCP server. This skill should be used when managing repositories, creating/updating files, working with issues and PRs, searching code/repos/users, creating branches, and performing code reviews. Supports all major GitHub API operations.
---

# GitHub

Base directory for this skill: C:\Users\lyf1143312445\.agents\skills\github

Interact with GitHub repositories through the Model Context Protocol (MCP) server for GitHub.

## When to Use

- Managing repository files (create, update, get contents)
- Working with issues (create, update, list, comment)
- Managing pull requests (create, review, merge, get status)
- Searching GitHub (repositories, code, issues, users)
- Creating and managing branches
- Forking repositories

## Quick Start

Run the CLI script with bun from this skill directory:

```bash
bun ./scripts/github.ts <command> [options]
```

## Available Commands

### Repository Operations

| Command | Description |
|---------|-------------|
| `create-repository` | Create a new GitHub repository |
| `fork-repository` | Fork a repository to your account |
| `search-repositories` | Search for repositories |

### File Operations

| Command | Description |
|---------|-------------|
| `get-file-contents` | Get file or directory contents |
| `create-or-update-file` | Create or update a single file |
| `push-files` | Push multiple files in a single commit |

### Branch Operations

| Command | Description |
|---------|-------------|
| `create-branch` | Create a new branch |
| `list-commits` | List commits in a repository |

### Issue Operations

| Command | Description |
|---------|-------------|
| `create-issue` | Create a new issue |
| `get-issue` | Get issue details |
| `list-issues` | List repository issues |
| `update-issue` | Update an existing issue |
| `add-issue-comment` | Add a comment to an issue |

### Pull Request Operations

| Command | Description |
|---------|-------------|
| `create-pull-request` | Create a new PR |
| `get-pull-request` | Get PR details |
| `list-pull-requests` | List repository PRs |
| `get-pull-request-files` | Get files changed in PR |
| `get-pull-request-status` | Get PR status checks |
| `get-pull-request-comments` | Get PR review comments |
| `get-pull-request-reviews` | Get PR reviews |
| `create-pull-request-review` | Create a PR review |
| `merge-pull-request` | Merge a PR |
| `update-pull-request-branch` | Update PR branch from base |

### Search Operations

| Command | Description |
|---------|-------------|
| `search-repositories` | Search repositories |
| `search-code` | Search code across GitHub |
| `search-issues` | Search issues and PRs |
| `search-users` | Search GitHub users |

## Global Options

- `-t, --timeout <ms>`: Call timeout (default: 30000)
- `-o, --output <format>`: Output format: `text` | `markdown` | `json` | `raw`

## Common Examples

```bash
# Get file contents
bun ./scripts/github.ts get-file-contents \
  --owner facebook --repo react --path README.md

# Create an issue
bun ./scripts/github.ts create-issue \
  --owner myorg --repo myrepo --title "Bug report" --body "Description here"

# List open PRs
bun ./scripts/github.ts list-pull-requests \
  --owner facebook --repo react --state open

# Search code
bun ./scripts/github.ts search-code \
  --q "useState filename:*.tsx"

# Create a PR review
bun ./scripts/github.ts create-pull-request-review \
  --owner myorg --repo myrepo --pull-number 123 \
  --body "LGTM!" --event APPROVE
```

## Requirements

- [Bun](https://bun.sh) runtime
- `mcporter` package (embedded in script)
- `GITHUB_TOKEN` environment variable for authentication

## Resources

- `scripts/github.ts` - Main CLI tool wrapping GitHub MCP server
- `references/api_reference.md` - Detailed parameter documentation for all commands
