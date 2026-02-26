---
name: sustainability-summary
description: Retrieve time-windowed relevant sustainability RSS evidence from the RSS metadata SQLite database and optionally join DOI-keyed enriched content from a separate fulltext SQLite database. Use when generating grounded daily, weekly, monthly, or custom-range digests after relevance labeling.
---

# Sustainability Summary

## Core Goal
- Read only relevant (`is_relevant=1`) records from RSS DB.
- Build compact RAG context from DOI-keyed entries.
- Include optional enriched content from separate fulltext DB `entry_content` when available.
- Let the agent synthesize final summary text with evidence anchors.

## Triggering Conditions
- Receive requests for daily/weekly/monthly sustainability digests.
- Receive requests for custom date-range summaries.
- Need evidence-grounded output from labeled RSS entries and enriched content.

## Input Requirements
- Required tables: `feeds`, `entries` (from `sustainability-rss-fetch`).
- `entries` must be DOI-keyed and relevance-labeled.
- Optional fulltext DB table: `entry_content` (from `sustainability-fulltext-fetch`).
- RSS DB and fulltext DB must be different files.

## Workflow
1. Build retrieval context by time window.

```bash
export SUSTAIN_RSS_DB_PATH="/absolute/path/to/workspace-rss-bot/sustainability_rss.db"
export SUSTAIN_FULLTEXT_DB_PATH="/absolute/path/to/workspace-rss-bot/sustainability_fulltext.db"

python3 scripts/time_report.py \
  --rss-db "$SUSTAIN_RSS_DB_PATH" \
  --content-db "$SUSTAIN_FULLTEXT_DB_PATH" \
  --period weekly \
  --date 2026-02-10 \
  --max-records 120 \
  --max-per-feed 20 \
  --summary-chars 8192 \
  --fulltext-chars 8192 \
  --pretty \
  --output /tmp/sustainability-weekly-context.json
```

2. Generate final summary from returned `records` + `aggregates`.

3. Cite evidence using DOI + URL for key claims.

## Time Window Modes
- `--period daily --date YYYY-MM-DD`
- `--period weekly --date YYYY-MM-DD`
- `--period monthly --date YYYY-MM-DD`
- `--period custom --start ... --end ...`

## Default Fields
- `doi,timestamp_utc,timestamp_source,feed_title,feed_url,title,url,summary,fulltext_status,fulltext_length,fulltext_excerpt`

## Configurable Parameters
- `--rss-db`
- `--content-db`
- `SUSTAIN_RSS_DB_PATH`
- `SUSTAIN_FULLTEXT_DB_PATH`
- `--period`
- `--date`
- `--start`
- `--end`
- `--max-records`
- `--max-per-feed`
- `--summary-chars`
- `--fulltext-chars`
- `--top-feeds`
- `--top-keywords`
- `--fields`
- `--output`
- `--pretty`
- `--fail-on-empty`

## Error Handling
- Missing required DOI-based tables: fail fast with setup guidance.
- RSS DB and fulltext DB path collision: fail fast and require separate files.
- Invalid date/time/field list: return parse errors.
- Missing `entry_content`: continue in metadata-only mode.
- Empty relevant set: return empty context; optional failure with `--fail-on-empty`.

## References
- `references/time-window-rules.md`
- `references/report-format.md`

## Assets
- `assets/config.example.json`

## Scripts
- `scripts/time_report.py`
