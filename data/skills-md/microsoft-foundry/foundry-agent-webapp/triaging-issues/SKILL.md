---
name: triaging-issues
description: >
  Provides issue triage workflow, priority definitions, and report format.
  Use when analyzing GitHub issues and PRs, assessing priority,
  or generating triage reports.
---

# Issue Triage Guidance

Gather open issues and PRs, analyze them, and recommend next steps. Search the codebase to identify affected components — don't rely on hardcoded file mappings.

## Priority Definitions

| Priority | Criteria |
|----------|----------|
| 🔴 **Critical** | Production broken, security issue, data loss |
| 🟠 **High** | Major feature broken, blocking users |
| 🟡 **Medium** | Feature degraded, workaround exists |
| 🟢 **Low** | Minor issue, cosmetic, nice-to-have |

## Complexity Scale

| Size | Estimate |
|------|----------|
| **S** | Hours |
| **M** | 1-2 days |
| **L** | 3-5 days |
| **XL** | 1+ week |

## Label Taxonomy

| Prefix | Values |
|--------|--------|
| `area:` | `backend`, `frontend`, `auth`, `streaming`, `infra`, `docs` |
| `type:` | `bug`, `feature`, `enhancement`, `chore`, `docs` |
| `priority:` | `critical`, `high`, `medium`, `low` |

## Triage Report Format

### Open Issues Summary

| # | Title | Priority | Type | Complexity |
|---|-------|----------|------|------------|

### Per Issue — #[number]: [title]

- **Priority** / **Type** / **Complexity**
- **Affected Areas**: checklist of areas
- **Relevant Files**: table with file + reason
- **Suggested Labels**: using taxonomy above
- **Recommended Next Steps**: numbered list

### Open PRs Summary

| # | Title | Author | Status | Files Changed |
|---|-------|--------|--------|---------------|

### Per PR — #[number]: [title]

- **Status**: Draft | Ready for review | Changes requested | Approved
- **Review Notes**: concerns or things to check

## gh CLI Commands for Read-Only Analysis

```bash
# List open issues
gh issue list --state open

# Search for potential duplicates
gh issue list --search "keyword"

# View issue details
gh issue view <number>

# List open PRs
gh pr list --state open

# View PR details and diff
gh pr view <number>
gh pr diff <number>
```

## Duplicate Detection

Before deep-diving into an issue, search for duplicates:

1. Use `gh issue list --search "<keywords>"` with key terms from the issue title and body.
2. Check closed issues too: `gh issue list --state closed --search "<keywords>"`.
3. If a duplicate exists, note it in the triage report with a cross-reference.

## Constraints

- ❌ **Read-only** — do NOT modify issues or PRs
- ❌ No `gh issue edit`, `gh issue close`, `gh issue label`
- ❌ No `gh pr merge`, `gh pr close`, `gh pr review --approve`
- ✅ Only use read commands: `list`, `view`, `search`, `diff`
