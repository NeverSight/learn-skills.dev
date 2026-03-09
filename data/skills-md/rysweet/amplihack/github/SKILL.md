---
name: github
description: Expert guidance for GitHub CLI (gh) - issues, PRs, repos, releases, and GitHub API. Use when working with GitHub, managing issues/PRs, or when user mentions GitHub, PRs, issues, or repos. Preferred over GitHub MCP server for context efficiency.
---

# GitHub CLI Skill

## Quick Start

### Authentication

```bash
# Interactive authentication (recommended)
gh auth login

# Check authentication status
gh auth status

# Login with token
gh auth login --with-token < token.txt

# Login to enterprise
gh auth login --hostname github.example.com
```

### Configuration

```bash
# Set default editor
gh config set editor "code --wait"

# Set default browser
gh config set browser "firefox"

# Set default git protocol
gh config set git_protocol ssh

# View all settings
gh config list
```

## Essential Commands (Most Common First)

### 1. Issues

```bash
# Create issue
gh issue create --title "Bug: something broken" --body "Description here"

# Create with labels
gh issue create --title "Feature request" --label "enhancement,priority:high"

# List issues
gh issue list                    # Open issues
gh issue list --state all        # All issues
gh issue list --assignee @me     # Assigned to me
gh issue list --label "bug"      # By label

# View issue
gh issue view 123                # By number
gh issue view 123 --comments     # With comments

# Edit issue
gh issue edit 123 --title "New title"
gh issue edit 123 --add-label "in-progress"
gh issue edit 123 --assignee username

# Close/reopen
gh issue close 123
gh issue close 123 --comment "Fixed in PR #456"
gh issue reopen 123

# Comment
gh issue comment 123 --body "This is a comment"
```

### 2. Pull Requests

```bash
# Create PR
gh pr create --title "Feature: new thing" --body "Description"
gh pr create --draft                       # Create as draft
gh pr create --fill                        # Auto-fill from commits

# List PRs
gh pr list                        # Open PRs
gh pr list --state merged         # Merged PRs
gh pr list --author @me           # My PRs
gh pr list --search "review:required"

# View PR
gh pr view 123                    # By number
gh pr view                        # Current branch PR
gh pr diff 123                    # View diff
gh pr checks 123                  # View CI status

# Review PRs
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix X"
gh pr review 123 --comment --body "Looks good overall"

# Merge
gh pr merge 123                   # Interactive
gh pr merge 123 --squash          # Squash merge
gh pr merge 123 --rebase          # Rebase merge
gh pr merge 123 --auto            # Auto-merge when checks pass

# Mark ready
gh pr ready 123                   # Convert draft to ready

# Comment
gh pr comment 123 --body "Comment text"

# Close
gh pr close 123
```

### 3. Repository

```bash
# Clone
gh repo clone owner/repo
gh repo clone owner/repo -- --depth 1   # Shallow clone

# Create
gh repo create my-repo --public
gh repo create my-repo --private --clone

# View
gh repo view                      # Current repo
gh repo view owner/repo           # Specific repo
gh repo view --web                # Open in browser

# Fork
gh repo fork owner/repo
gh repo fork owner/repo --clone   # Fork and clone

# Sync fork
gh repo sync                      # Sync fork with upstream

# List repos
gh repo list                      # Your repos
gh repo list owner                # Organization repos
```

### 4. Workflow (GitHub Actions)

```bash
# List workflows
gh workflow list

# View workflow runs
gh run list                       # Recent runs
gh run list --workflow ci.yml     # By workflow
gh run list --status failure      # Failed runs

# View run details
gh run view 123456                # By run ID
gh run view 123456 --log          # With logs
gh run view 123456 --log-failed   # Only failed logs

# Trigger workflow
gh workflow run ci.yml
gh workflow run ci.yml -f param=value

# Watch run
gh run watch                      # Watch current branch run
gh run watch 123456               # Watch specific run

# Cancel/rerun
gh run cancel 123456
gh run rerun 123456
gh run rerun 123456 --failed      # Rerun only failed jobs
```

### 5. Search

```bash
# Search issues/PRs
gh search issues "bug in:title"
gh search issues "label:bug state:open"
gh search prs "author:username is:merged"

# Search repos
gh search repos "language:python stars:>1000"

# Search code
gh search code "function handleError"
gh search code "filename:config.json org:myorg"
```

## Advanced Commands

### Releases

```bash
# Create release
gh release create v1.0.0 --title "Version 1.0" --notes "Release notes"
gh release create v1.0.0 --generate-notes   # Auto-generate notes
gh release create v1.0.0 ./dist/*           # Upload assets

# List/view
gh release list
gh release view v1.0.0

# Download assets
gh release download v1.0.0
gh release download v1.0.0 --pattern "*.zip"
```

### Gists

```bash
# Create gist
gh gist create file.txt
gh gist create --public file.txt
gh gist create -d "Description" file1.txt file2.txt

# List/view
gh gist list
gh gist view gist_id

# Edit
gh gist edit gist_id
```

### API Access

```bash
# GraphQL query
gh api graphql -f query='{ viewer { login } }'

# REST API
gh api repos/owner/repo/issues
gh api repos/owner/repo/issues --method POST -f title="Issue title"

# Paginate
gh api repos/owner/repo/issues --paginate
```

### SSH Keys & GPG

```bash
# SSH keys
gh ssh-key add ~/.ssh/id_ed25519.pub --title "My laptop"
gh ssh-key list

# GPG keys
gh gpg-key add key.asc
gh gpg-key list
```

## Common Patterns

### Issue-to-PR Workflow

```bash
# 1. Create issue
gh issue create --title "Feature: X" --label "enhancement"
# Returns issue #123

# 2. Create branch and work
git checkout -b feat/issue-123-x

# 3. Create PR linking to issue
gh pr create --title "Feature: X" --body "Closes #123"
```

### Code Review Flow

```bash
# Check out PR locally
gh pr checkout 456

# Run tests, review code...

# Approve or request changes
gh pr review 456 --approve --body "LGTM!"
```

### CI Failure Investigation

```bash
# List failed runs
gh run list --status failure

# Get logs
gh run view RUN_ID --log-failed

# Rerun after fix
gh run rerun RUN_ID
```

## Re-enabling GitHub MCP Server

If you need the full GitHub MCP server for advanced operations (e.g., complex GraphQL queries, bulk operations), you can ask:

> "Please use the GitHub MCP server" or "Re-enable GitHub MCP"

To re-enable manually:

1. Edit `~/.copilot/github-copilot/mcp.json`
2. Remove or set `"disabled": false` for github-mcp-server:

```json
{
  "mcpServers": {
    "github-mcp-server": {
      "disabled": false
    }
  }
}
```

3. Restart the Copilot CLI session

**When to use MCP vs gh CLI:**

| Use gh CLI                         | Use GitHub MCP                            |
| ---------------------------------- | ----------------------------------------- |
| Standard issue/PR operations       | Complex multi-step GitHub operations      |
| CI/CD workflow management          | Bulk operations across many repos         |
| Quick lookups and status checks    | Advanced GraphQL queries                  |
| Script automation                  | Operations requiring persistent state     |
| **Most daily GitHub interactions** | **Rare, specialized GitHub integrations** |

## Troubleshooting

```bash
# Check auth
gh auth status

# Refresh token
gh auth refresh

# Clear cache
gh cache delete --all

# Debug mode
GH_DEBUG=api gh issue list
```

## Environment Variables

```bash
GH_TOKEN           # Auth token (alternative to gh auth)
GH_HOST            # Default host (for enterprise)
GH_REPO            # Default repo (owner/repo format)
GH_EDITOR          # Editor for interactive commands
GH_BROWSER         # Browser for --web commands
GH_DEBUG           # Enable debug output (api, oauth)
NO_COLOR           # Disable colored output
```
