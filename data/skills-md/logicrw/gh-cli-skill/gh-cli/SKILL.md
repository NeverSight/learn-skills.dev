---
name: gh-cli
description: >
  GitHub CLI operations via `gh` command. Use when working with GitHub
  repositories, pull requests, issues, code search, releases, or any
  GitHub API operation. This skill replaces the GitHub MCP server with
  direct CLI calls. Triggers on: GitHub, PR, pull request, issue, repo,
  branch, release, tag, commit, fork, merge, review, gh.
---

# GitHub CLI (`gh`) — Agent Skill

Use the `gh` CLI for ALL GitHub operations. Always use `--json` for structured output and `--jq` for field selection to minimize token usage.

## Authentication

Already configured via `gh auth`. Verify with:

```bash
gh auth status
```

## Core Principle

**Always request only the fields you need** to minimize output tokens:

```bash
# ❌ Bad — returns everything
gh pr view 123

# ✅ Good — returns only what's needed
gh pr view 123 --json title,state,body,url --jq '{title,state,body,url}'
```

---

## Quick Reference

### Pull Requests

```bash
# List open PRs
gh pr list --json number,title,author,updatedAt --jq '.[] | {number,title,author:.author.login}'

# View PR details
gh pr view <number> --json title,state,body,headRefName,baseRefName,additions,deletions,changedFiles

# View PR diff
gh pr diff <number>

# View PR files changed
gh pr diff <number> --name-only

# Create PR
gh pr create --title "title" --body "description" --base main --head feature-branch

# Create draft PR
gh pr create --title "title" --body "description" --draft

# Merge PR
gh pr merge <number> --squash --delete-branch

# Review PR
gh pr review <number> --approve
gh pr review <number> --request-changes --body "feedback"
gh pr review <number> --comment --body "looks good"

# PR review comments
gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[].body'

# Add review comment on specific line
gh api repos/{owner}/{repo}/pulls/{number}/comments \
  -f body="comment" -f path="file.py" -F line=42 -f side="RIGHT" \
  -f commit_id="$(gh pr view <number> --json headRefOid --jq .headRefOid)"

# Check PR CI status
gh pr checks <number>

# Update PR branch
gh pr update-branch <number>
```

### Issues

```bash
# List issues
gh issue list --json number,title,labels,assignees --jq '.[] | {number,title,labels:[.labels[].name]}'

# View issue
gh issue view <number> --json title,body,state,labels,assignees,comments

# Create issue
gh issue create --title "title" --body "description" --label "bug"

# Comment on issue
gh issue comment <number> --body "comment text"

# Close issue
gh issue close <number> --reason completed

# Edit issue
gh issue edit <number> --title "new title" --add-label "priority"

# Search issues
gh issue list --search "keyword in:title,body" --json number,title
```

### Repository & Files

```bash
# View repo info
gh repo view --json name,description,defaultBranchRef --jq '{name,description,branch:.defaultBranchRef.name}'

# Get file contents (use gh api to avoid raw output issues)
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
# Or with ref:
gh api repos/{owner}/{repo}/contents/{path}?ref={branch} --jq '.content' | base64 -d

# List directory
gh api repos/{owner}/{repo}/contents/{path} --jq '.[].name'

# Create/update file
gh api repos/{owner}/{repo}/contents/{path} \
  -X PUT \
  -f message="commit message" \
  -f content="$(echo -n 'file content' | base64)" \
  -f branch="branch-name"
# For update, include sha:
  -f sha="<blob_sha>"

# Delete file
gh api repos/{owner}/{repo}/contents/{path} \
  -X DELETE \
  -f message="delete file" \
  -f sha="<blob_sha>" \
  -f branch="branch-name"

# Push multiple files — use git directly
git add file1 file2 && git commit -m "message" && git push

# Create branch
gh api repos/{owner}/{repo}/git/refs \
  -f ref="refs/heads/new-branch" \
  -f sha="$(gh api repos/{owner}/{repo}/git/ref/heads/main --jq '.object.sha')"

# List branches
gh api repos/{owner}/{repo}/branches --jq '.[].name'

# Fork repo
gh repo fork {owner}/{repo}

# Create repo
gh repo create {name} --public --description "desc"
```

### Search

```bash
# Search code
gh search code "query" --repo {owner}/{repo} --json path,repository,textMatches
gh search code "query language:python" --json path,repository

# Search repos
gh search repos "query" --json fullName,description,stargazersCount --jq '.[] | {name:.fullName,stars:.stargazersCount}'

# Search issues across GitHub
gh search issues "query" --json number,title,repository

# Search PRs
gh search prs "query" --json number,title,repository
```

### Commits & History

```bash
# List commits
gh api repos/{owner}/{repo}/commits --jq '.[].commit.message' | head -20
gh api repos/{owner}/{repo}/commits?sha={branch}\&per_page=10 --jq '.[] | {sha: .sha[:7], message: .commit.message}'

# View specific commit
gh api repos/{owner}/{repo}/commits/{sha} --jq '{message:.commit.message,files:[.files[].filename],stats:.stats}'

# Get commit diff
gh api repos/{owner}/{repo}/commits/{sha} -H "Accept: application/vnd.github.diff"
```

### Releases & Tags

```bash
# List releases
gh release list --json tagName,name,publishedAt

# View latest release
gh release view --json tagName,name,body

# View specific release
gh release view {tag} --json tagName,name,body

# List tags
gh api repos/{owner}/{repo}/tags --jq '.[].name'

# Create release
gh release create {tag} --title "title" --notes "release notes"
```

### Advanced API Access

For any operation not covered above, use `gh api` directly:

```bash
# GET request
gh api repos/{owner}/{repo}/actions/runs --jq '.workflow_runs[:3] | .[].conclusion'

# POST request
gh api repos/{owner}/{repo}/issues/{number}/comments -f body="comment"

# With pagination
gh api repos/{owner}/{repo}/issues --paginate --jq '.[].number'

# Get authenticated user
gh api user --jq '{login,name,email}'

# Team members
gh api orgs/{org}/teams/{team}/members --jq '.[].login'
```

## Output Optimization

Always minimize output for agent consumption:

1. **Use `--json` + `--jq`** for structured, minimal output
2. **Limit results** with `--limit` or API `per_page` parameter
3. **Select fields** — never dump full objects
4. **Pipe to `head`** for long outputs: `| head -50`

## Error Handling

```bash
# Check if command succeeded
gh pr view 999 --json state 2>/dev/null && echo "exists" || echo "not found"

# Safe API call with error handling
gh api repos/{owner}/{repo}/contents/{path} 2>/dev/null || echo "file not found"
```
