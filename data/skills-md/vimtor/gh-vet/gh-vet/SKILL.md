---
name: gh-vet
description: Check a GitHub user's open source merge rate and contribution score. Use when reviewing a PR from an unknown contributor, asked to "check merge rate", "check contributor quality", "vet this PR author", or "run gh-vet".
metadata:
  author: vimtor
  version: "1.0.0"
---

# gh-vet

Check a GitHub contributor's open source merge rate before reviewing their PR. Helps identify low-quality LLM-generated pull requests.

## How It Works

1. Fetches all public PRs (and optionally issues) by the user via GitHub GraphQL API
2. Excludes the user's own repos — only external contributions count
3. Calculates a **score score**: % of merged PR stars out of total PR stars (star-weighted merge rate)
4. Breaks down stats per repository

## Prerequisites

Requires [GitHub CLI](https://cli.github.com/) (`gh`) authenticated.

## Usage

```bash
# Check a specific user
gh vet <username>

# Auto-detect PR author (when run inside a PR branch)
gh vet

# JSON output (for programmatic use)
gh vet <username> --json

# Include issue stats
gh vet <username> --issues

# Highlight a specific repo in output
gh vet <username> --repo owner/name
```

## When to Use

- **Reviewing a PR from an external contributor** — run `gh vet <author>` to check their track record
- **Triaging incoming PRs** — quickly assess if a contributor has a history of merged contributions
- **Comparing contributors** — use `--json` to programmatically compare multiple users

## Output

The tool outputs:
- **Score**: star-weighted merge rate (green ≥70%, yellow ≥40%, red <40%)
- **Pull Requests**: total merged/opened with per-repo breakdown
- **Issues** (with `--issues`): total closed/opened with per-repo breakdown

## Present Results to User

When presenting gh-vet output, summarize:
- The user's score score and what it indicates
- Their overall merge rate
- Notable repos they've contributed to
- Whether this suggests the contributor is trustworthy for the current PR
