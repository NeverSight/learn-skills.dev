---
name: github-contribution-period-analysis
description: Analyze one GitHub user's code contribution activity in a specified UTC time window and generate a Markdown report focused on practical contributions (authored merged PRs, PRs merged by the target user, and authored commits) across accessible public and private repositories. Use when users ask to evaluate real engineering contribution over a period and want evidence links.
---

# GitHub Contribution Period Analysis

## Core Goal
- Build an evidence-based Markdown report for one target GitHub user in a UTC time window.
- Focus on practical code contribution signals: merged PR and commit activity.
- Cover both own repositories and other repositories, limited by credential access.

## Workflow
1. Prepare authentication for GitHub API access.
2. Run `scripts/github_contribution_report.py` with target user and time window.
3. Review the generated Markdown report and inspect evidence links.

## Command

```bash
python3 scripts/github_contribution_report.py \
  --user <github-login> \
  --start 2026-03-01 \
  --end 2026-03-08 \
  --output /tmp/github-contribution-report.md
```

## Output Semantics
- Included contribution types:
  - Authored merged PRs.
  - PRs merged by the target user (maintainer merge work).
  - Authored commits.
- Excluded activity types:
  - Comments, reviews, stars, watches, forks.
- The report contains:
  - Scope and coverage notes.
  - Summary metrics.
  - Substantive work categories inferred from PR/commit evidence.
  - Work content highlights with representative evidence links.
  - Repository breakdown.
  - Per-repository concrete change details (for every changed repository).
  - Contribution timeline.
  - Top contribution tables.
  - Evidence appendix with PR/commit URLs.

## Important Constraints
- SSH key alone is for `git` transport and does not directly authorize GitHub REST API calls.
- Private repository coverage needs authenticated API access, typically via `GITHUB_TOKEN`/`GH_TOKEN` or `gh auth token`.
- GitHub Search API has a 1000-item cap per query. For very active users, split the time range and run multiple reports.

## References
- `references/env.md`
- `references/data-model.md`
- `references/markdown-template.md`

## Scripts
- `scripts/github_contribution_report.py`
