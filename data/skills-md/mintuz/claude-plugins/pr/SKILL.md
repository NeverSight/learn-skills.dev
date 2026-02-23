---
name: pr
description: WHEN drafting PR descriptions or sizing/splitting work; NOT for commit messages; provides reviewer-first templates and gh pr steps.
---

# Pull Request Skills

Guidelines for creating comprehensive pull request descriptions and submitting PRs efficiently.

## Philosophy

- **Reviewer-first** - Optimize for the person reviewing, not the author
- **Context over detail** - Explain why, link to how
- **Scannable** - Busy reviewers skim; make it easy
- **Actionable** - Clear testing steps, obvious risks
- **Honest** - Flag complexity, don't hide it

## Gathering Context

Before creating a PR, gather information about the changes:

```bash
# Compare branch changes against main
git diff main...HEAD

# List modified files
git diff main...HEAD --name-only

# Review commit history
git log main..HEAD --oneline

# Get detailed commit messages
git log main..HEAD --format="%B---"

# Get files changed with stats
git diff main...HEAD --stat
```

## Quick Reference

| Task | Guide |
| ---- | ----- |
| Sizing and splitting PRs | [pr-sizing.md](pr-sizing.md) |
| Writing PR descriptions | [pr-description.md](pr-description.md) |
| Creating PRs with `gh` CLI | [pr-creation.md](pr-creation.md) |

## When to Use Each Guide

### PR Sizing

Use [pr-sizing.md](pr-sizing.md) when you need:

- Size category definitions (small/medium/large)
- Signs a PR should be split
- Strategies for splitting large PRs
- Guidance on when large PRs are acceptable

### PR Description Writing

Use [pr-description.md](pr-description.md) when you need:

- Templates for small, medium, or large PRs
- Section writing guidelines (summary, changes, testing, etc.)
- Commands to gather context from git history

### PR Creation

Use [pr-creation.md](pr-creation.md) when you need:

- `gh pr create` command syntax and options
- HEREDOC pattern for multi-line bodies
- Draft PRs, reviewers, labels, and milestones
- Troubleshooting common errors
