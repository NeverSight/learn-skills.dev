---
name: local-code-review
description: Use when user wants local code review with GitHub-like PR interface, or when reviewing branches before merge using Gitea
---

# Local Code Review

Ephemeral GitHub-like PR review via a throwaway local Gitea instance. User reviews in the web UI (line comments, suggestions, squash merge). Agent manages PRs via CLI. Nothing persists after `done`.

## Quick Reference

| Command | Description |
|---------|-------------|
| `gitea-review start <branch> [...]` | Spin up Gitea, push branches, create PRs, open browser |
| `gitea-review comments <pr#> [--hide-resolved]` | Fetch review comments with resolved status |
| `gitea-review push <branch>` | Push fixes to existing PR |
| `gitea-review reply <pr#> <path> <line> <msg>` | Reply to a comment |
| `gitea-review merge <pr#>` | Squash merge PR |
| `gitea-review list` | List open PRs |
| `gitea-review open [pr#]` | Open in browser |
| `gitea-review status` | Check if Gitea is running |
| `gitea-review done` | Tear down Gitea, remove remote, clean up |

**AI assistants:** Use full path `~/.claude/skills/local-code-review/bin/gitea-review`.

## When to Use

- User wants to review branches with line comments before merging
- User asks for "local code review" or "local PR review"
- User wants GitHub-like review without pushing to GitHub
- User says "create a PR for review" and context is local/private work

## How It Works

Gitea runs as an ephemeral Docker container with a Caddy reverse proxy that auto-logs the user in (no password needed). The script adds a `gitea` remote alongside `origin`, pushes branches there, and creates PRs with auto-generated descriptions. The user reviews at the auto-assigned port (override with `GITEA_PORT`). When done, `gitea-review done` removes the container, the remote, and all temp state.

Each repository gets its own isolated instance (container, port, state file), so multiple sessions can run concurrently without interfering with each other.

### PR Descriptions

PRs are automatically created with thorough descriptions that include:
- **Summary** - Conventional commit type breakdown (feat, fix, test, etc.)
- **Changes** - Files modified count and line change statistics
- **File list** - Up to 10 changed files with paths
- **Commit list** - Up to 10 commits with hashes and messages

This gives reviewers immediate context about what changed and why.

## Workflow

```
gitea-review start branch1 branch2   # Launch Gitea, create PRs, open browser
  [user reviews in browser, leaves line comments]
gitea-review comments 1               # Agent reads comments
  [agent makes code fixes]
gitea-review push branch1             # Push fixes
  [user resolves threads in browser]
gitea-review merge 1                  # Squash merge when approved
gitea-review done                     # Tear down
```

## Responding to Review Comments

When the user says "address review comments" or "check PR comments":

1. `gitea-review comments <pr#>` -- each comment shows `[id] reviewer: message` at `file:line` with diff context. Resolved comments are marked with `[RESOLVED]`. Use `--hide-resolved` to filter them out.
2. Make the requested code changes
3. `gitea-review push <branch>`
4. `gitea-review reply <pr#> <path> <line> "Fixed -- <what you did>"`
5. User resolves threads in the browser UI

## Requirements

- Docker
- curl, python3, git

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GITEA_PORT` | Auto-assigned (3000-3999) | Port for the Gitea web UI |
