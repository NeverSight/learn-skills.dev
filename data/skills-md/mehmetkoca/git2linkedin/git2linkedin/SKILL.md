---
name: git2linkedin
description: Generate feature-based and confidentiality-safe English LinkedIn Experience drafts directly from commit messages. Use when asked to write LinkedIn experience text from real commit activity for all-time or a specific date range (`since`/`until` in YYYY-MM-DD), while avoiding repository statistics and internal/confidential implementation details.
---

# Git2LinkedIn

## Overview

Generate a LinkedIn Experience draft from git history by directly reading commit messages and converting them into feature-focused, business-relevant, and confidentiality-safe bullets.

## Workflow

1. Collect required inputs:
- `role` (required)
- `company` (required)

2. Collect optional inputs:
- `repo` (default `.`)
- `since` (`YYYY-MM-DD`)
- `until` (`YYYY-MM-DD`)
- `author` (default: current git user)
- `out` (optional markdown output path)
- `max-commits` (default `400`)

3. Run the extractor:

```bash
# All-time
python3 skills/git2linkedin/scripts/git_history_extract.py \
  --role "Senior Software Engineer" \
  --company "Acme"

# Date range
python3 skills/git2linkedin/scripts/git_history_extract.py \
  --role "Senior Software Engineer" \
  --company "Acme" \
  --since 2025-01-01 \
  --until 2025-12-31
```

4. Convert JSON output into final LinkedIn text:
- Write one short English summary sentence.
- Write 4-6 impact bullets.
- Focus on end-user value and business relevance.
- Avoid repository metrics, commit hashes, file paths, and internal identifiers.

5. Handle empty ranges explicitly:
- If commit list is empty, explain that no commits were found and suggest widening the date range or changing `author`.

## Output Contract

Use these JSON fields:
- `summary`: baseline sentence for LinkedIn experience
- `feature_highlights`: feature-oriented bullet candidates
- `end_user_outcomes`: user-facing outcomes
- `business_relevance`: why this work matters for role/business goals
- `source_mode`: extraction mode metadata (`direct-commit-messages`)
- `guidance`: fallback suggestion when history is empty

## Guardrails

- Keep output in English unless user asks otherwise.
- Keep bullets concise and outcome-focused.
- Keep sentence style mostly passive and neutral; avoid first-person phrasing (`I improved`, `I enhanced`, etc.).
- Do not include repository statistics.
- Do not expose commit hashes, file paths, issue IDs, URLs, or raw commit messages.
- Do not invent confidential product details; keep language high-level and safe for public profiles.
