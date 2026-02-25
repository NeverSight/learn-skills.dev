---
name: gh
description: Use the GitHub CLI (`gh`) for repository operations including PR and issue inspection, GitHub search, checks, and API calls. Use when a user asks for GitHub URLs, PR metadata, issue details, checks, or repository automation.
---

# Gh

Use `gh` for GitHub-related tasks.

```bash
gh pr view 123 --json number,title,body,commits,files,headRefName,url
```

## Inspect PRs And Issues

View one PR as JSON:

```bash
gh pr view 123 --json number,title,body,commits,files,headRefName,url
```

List open PRs:

```bash
gh pr list --state open --json number,title,headRefName,url
```

View one issue as JSON:

```bash
gh issue view 456 --json number,title,body,comments,url
```

## Search GitHub

Prefer `gh search` for code/repo/issue/PR discovery.

Code search:

```bash
gh search code "TODO repo:owner/repo path:src" --limit 20
```

Repository search:

```bash
gh search repos "topic:cli language:go" --limit 20 --json name,description,url
```

Issue search:

```bash
gh search issues "repo:owner/repo is:issue is:open label:bug" --limit 50 --json number,title,url,state,updatedAt
```

PR search:

```bash
gh search prs "repo:owner/repo is:pr is:open author:alice" --limit 50 --json number,title,url,state,updatedAt
```

Search tips:

- Use qualifiers to reduce noise: `repo:`, `path:`, `language:`, `is:open`, `author:`, `label:`
- Start broad, then refine filters
- Combine with local search (`rg`) in checked-out repos when validating context

## Checks And CI

View checks for a PR branch:

```bash
gh pr checks 123
```

View run details with links:

```bash
gh run list --limit 20
```

## API And Automation

Use `gh api` when subcommands do not expose required fields.

```bash
gh api repos/:owner/:repo/pulls --method POST -f title='My PR' -f head='feature-branch' -f base='main'
```

Prefer machine-readable output for automation:

- Use `--json` where available
- Use `gh api` output with `jq` for deterministic extraction of fields like `number`, `title`, `body`, and `url`

## URL Handling

When the user provides a GitHub URL, parse owner/repo/number and fetch details with `gh` commands instead of browser scraping.

Examples:

- PR URL -> `gh pr view <number> --repo <owner>/<repo> ...`
- Issue URL -> `gh issue view <number> --repo <owner>/<repo> ...`

## Guardrails

Default to read-only operations unless the user explicitly requests mutation.

Read-only examples:

- `gh pr view`, `gh pr list`, `gh pr checks`
- `gh issue view`, `gh search ...`, `gh run list`, `gh api` GET calls

Mutating examples (require explicit user intent):

- `gh pr create`, `gh pr merge`, `gh pr close`
- `gh issue create`, `gh issue edit`, `gh issue close`
- `gh api` POST/PATCH/DELETE calls
