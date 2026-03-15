---
name: github-skill
description: Read and manage GitHub PRs, issues, and notifications. Use when the user asks to check PRs, view code reviews, find review requests, or check CI status. Helps inform daily standups and code review workflows.
allowed-tools: Bash, Read
---

# GitHub Skill - PRs & Code Review

Read, search, and manage GitHub pull requests and issues. View reviews, check CI status, track notifications.

## No Setup Required

This skill uses the `gh` CLI which should already be authenticated. Verify with:

```bash
gh auth status
```

## Commands

### List Open PRs

```bash
python3 ~/.claude/skills/github-skill/github_skill.py prs [--repo OWNER/REPO] [--mine] [--limit N] [--state STATE]
```

**Arguments:**
- `--repo` / `-r` - Repository in `owner/repo` format (optional if in git repo)
- `--mine` / `-m` - Only show your PRs
- `--limit` / `-l` - Number of results (default: 20)
- `--state` / `-s` - Filter: `open`, `closed`, `merged`, `all` (default: open)

### Get PR Details

```bash
python3 ~/.claude/skills/github-skill/github_skill.py pr NUMBER [--repo OWNER/REPO] [--format FORMAT]
```

**Arguments:**
- `NUMBER` - PR number
- `--repo` / `-r` - Repository
- `--format` / `-f` - Output format: `json` (default) or `vault` (markdown for notes)

### Get PR Review Comments

```bash
python3 ~/.claude/skills/github-skill/github_skill.py pr-comments NUMBER [--repo OWNER/REPO]
```

### Get PR Reviews

```bash
python3 ~/.claude/skills/github-skill/github_skill.py pr-reviews NUMBER [--repo OWNER/REPO]
```

### PRs Awaiting Your Review

```bash
python3 ~/.claude/skills/github-skill/github_skill.py review-requests [--repo OWNER/REPO] [--limit N]
```

Perfect for morning standup prep - shows all PRs where your review is requested.

### List Issues

```bash
python3 ~/.claude/skills/github-skill/github_skill.py issues [--repo OWNER/REPO] [--mine] [--limit N] [--state STATE]
```

### Get Issue Details

```bash
python3 ~/.claude/skills/github-skill/github_skill.py issue NUMBER [--repo OWNER/REPO]
```

### List Your Repos

```bash
python3 ~/.claude/skills/github-skill/github_skill.py repos [--limit N]
```

### Unread Notifications

```bash
python3 ~/.claude/skills/github-skill/github_skill.py notifications [--limit N]
```

## Workflow Examples

### Morning Standup Prep

```bash
# See what PRs need your review
python3 ~/.claude/skills/github-skill/github_skill.py review-requests

# Check status of your open PRs
python3 ~/.claude/skills/github-skill/github_skill.py prs --mine
```

This gives you:
- PRs awaiting your review (with CI status)
- Your open PRs (with review decisions)

Format for standup: "Review Andre's PR (EPO-428) - CI passing, needs approval"

### Check Specific PR

```bash
# Get full details
python3 ~/.claude/skills/github-skill/github_skill.py pr 123 --repo epochml/epoch

# See review comments
python3 ~/.claude/skills/github-skill/github_skill.py pr-comments 123 --repo epochml/epoch

# Get vault-formatted markdown
python3 ~/.claude/skills/github-skill/github_skill.py pr 123 --repo epochml/epoch --format vault
```

### Cross-Reference with Linear

PR titles often include Linear issue IDs (e.g., "EPO-428: Fix manifest flattening"). The skill extracts these automatically in output:

```json
{
  "number": 123,
  "title": "EPO-428: Fix manifest flattening",
  "linear_id": "EPO-428",
  ...
}
```

Use with Linear skill:
```bash
# Get PR details
python3 ~/.claude/skills/github-skill/github_skill.py pr 123 --repo epochml/epoch

# Get Linear issue details
python3 ~/.claude/skills/linear-skill/linear_skill.py issue EPO-428
```

## Output

All commands output JSON by default. The `--format vault` option (for `pr` command) outputs markdown suitable for Obsidian notes:

```markdown
## PR #123: EPO-428: Fix manifest flattening

**Status:** OPEN, Changes Requested
**Author:** @andre
**Linear:** EPO-428
**Link:** [epochml/epoch#123](https://github.com/epochml/epoch/pull/123)

### Checks
- CI: OK
- lint: OK

### Reviews
- @idan: CHANGES_REQUESTED - "Need to handle edge case..."
```

## Output Fields

### PR List Output

```json
{
  "number": 123,
  "title": "EPO-428: Fix manifest flattening",
  "author": {"login": "andre"},
  "state": "OPEN",
  "reviewDecision": "CHANGES_REQUESTED",
  "linear_id": "EPO-428",
  "checks_summary": "5 passed, 1 pending",
  "url": "https://github.com/epochml/epoch/pull/123"
}
```

### Review Decision Values

- `APPROVED` - Ready to merge
- `CHANGES_REQUESTED` - Needs work
- `REVIEW_REQUIRED` - Waiting for review
- `null` - No reviews yet

## Requirements

- `gh` CLI installed and authenticated
- Python 3.9+

## Security Notes

- Uses existing `gh` CLI authentication
- No credentials stored in this skill
- Inherits permissions from `gh auth status`
