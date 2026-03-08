---
name: github-automation
description: Automate GitHub operations using gh CLI - manage repositories, issues, pull requests, releases, and workflows. Use when working with GitHub, managing repos, creating issues/PRs, or when users mention GitHub operations, gh CLI, or repository management.
vm0_secrets:
  - GH_TOKEN
---

# GitHub Automation

This Skill helps you manage GitHub operations using the `gh` CLI, including repositories, issues, pull requests, releases, and GitHub Actions workflows.

## Capabilities

- **Repositories**: Create, clone, fork, view, and manage repos
- **Issues**: Create, list, view, close, comment, and label issues
- **Pull Requests**: Create, review, merge, list, and comment on PRs
- **Releases**: Create releases and manage tags
- **Workflows**: View and manage GitHub Actions
- **Gists**: Create and manage gists
- **Search**: Search repos, issues, PRs, code, and users

## Authentication

Go to [vm0.ai](https://vm0.ai) **Settings → Connectors** and connect **GitHub**. vm0 will automatically inject the required token.

Verify with:
```bash
gh auth status
```

## Instructions

### Phase 1: Understand the Request
1. Clarify what GitHub operation the user needs
2. Identify the target repository (if not specified, ask)
3. Confirm any destructive operations before executing

### Phase 2: Execute the Operation
Use `gh` CLI commands. Common patterns:

**Repository Operations**
```bash
gh repo view <owner>/<repo>
gh repo clone <owner>/<repo>
gh repo create <name> --public/--private
gh repo list <owner>
```

**Issue Operations**
```bash
gh issue list --repo <owner>/<repo>
gh issue create --repo <owner>/<repo> --title "Title" --body "Body"
gh issue view <number> --repo <owner>/<repo>
gh issue close <number> --repo <owner>/<repo>
gh issue comment <number> --repo <owner>/<repo> --body "Comment"
```

**Pull Request Operations**
```bash
gh pr list --repo <owner>/<repo>
gh pr create --repo <owner>/<repo> --title "Title" --body "Body"
gh pr view <number> --repo <owner>/<repo>
gh pr merge <number> --repo <owner>/<repo>
gh pr review <number> --repo <owner>/<repo> --approve/--comment/--request-changes
gh pr checks <number> --repo <owner>/<repo>
```

**Search Operations**
```bash
gh search repos <query>
gh search issues <query>
gh search prs <query>
gh search code <query>
```

**GitHub Actions**
```bash
gh run list --repo <owner>/<repo>
gh run view <run-id> --repo <owner>/<repo>
gh workflow list --repo <owner>/<repo>
```

**Releases**
```bash
gh release list --repo <owner>/<repo>
gh release create <tag> --repo <owner>/<repo> --title "Title" --notes "Notes"
```

## Guidelines

- Always specify `--repo <owner>/<repo>` when not in a cloned repository
- For destructive operations (delete, close, merge), confirm with user first
- Use `--json` flag when you need to parse output programmatically
- Handle errors gracefully and suggest fixes
- When creating issues/PRs, use clear titles and descriptive bodies

### Phase 3: Report Results
- Summarize what was done
- Provide relevant links (PR URLs, issue numbers, etc.)
- Suggest next steps if applicable

## Output Format

When listing items, format clearly:
```
#123 - Issue title (open/closed) - @author
#456 - PR title (open/merged/closed) - @author
```

When creating items, always report:
- The created item's number/ID
- Direct URL to the item
- Any relevant status information

## Examples

**Create an issue:**
```bash
gh issue create --repo <owner>/<repo> --title "Bug: Login fails" --body "Steps to reproduce..."
```

**List open PRs awaiting review:**
```bash
gh pr list --repo <owner>/<repo> --state open --search "review:required"
```

**Get PR details as JSON:**
```bash
gh pr view <number> --repo <owner>/<repo> --json title,state,reviews,checks
```

## Prerequisites

This Skill requires the GitHub CLI (`gh`) to be installed. Token is automatically provided by vm0 — connect GitHub in [vm0.ai](https://vm0.ai) **Settings → Connectors**.

**Important:** When using environment variables in commands with pipes, wrap the command in `bash -c '...'` to avoid variable substitution issues:
```bash
bash -c 'gh pr view <number> --repo $OWNER/$REPO --json title,state' | jq '.title'
```

Without environment variables, the pipe is fine:
```bash
gh pr view <number> --repo <owner>/<repo> --json title,state | jq '.title'
```
