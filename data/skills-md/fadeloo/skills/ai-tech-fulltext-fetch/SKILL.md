---
name: ai-tech-fulltext-fetch
description: Fetch and persist article full text for RSS entries already stored in SQLite by ai-tech-rss-fetch. Use when backfilling or incrementally syncing body text from entries.url or entries.canonical_url into a companion table for downstream indexing, retrieval, or summarization.
---

# AI Tech Fulltext Fetch

## Core Goal
- Reuse the same SQLite database populated by `ai-tech-rss-fetch`.
- Fetch article body text from each RSS entry URL.
- Persist extraction status and text in a companion table (`entry_content`).
- Support incremental runs and safe retries without creating duplicate fulltext rows.

## Triggering Conditions
- Receive a request to fetch article body/full text for entries already in `ai_rss.db`.
- Receive a request to build a second-stage pipeline after RSS metadata sync.
- Need a stable, resumable queue over existing `entries` rows.
- Need URL-based fulltext persistence before chunking, indexing, or summarization.

## Workflow
1. Ensure metadata table exists first.
- Run `ai-tech-rss-fetch` and populate `entries` in SQLite before using this skill.
- This skill requires the `entries` table to exist.
- In multi-agent runtimes, pin DB to the same absolute path used by `ai-tech-rss-fetch`:

```bash
export AI_RSS_DB_PATH="/absolute/path/to/workspace-rss-bot/ai_rss.db"
```

2. Initialize fulltext table.

```bash
python3 scripts/fulltext_fetch.py init-db --db "$AI_RSS_DB_PATH"
```

3. Run incremental fulltext sync.
- Default behavior fetches rows that are missing full text or currently failed.

```bash
python3 scripts/fulltext_fetch.py sync \
  --db "$AI_RSS_DB_PATH" \
  --limit 50 \
  --timeout 20 \
  --min-chars 300
```

4. Fetch one entry on demand.

```bash
python3 scripts/fulltext_fetch.py fetch-entry \
  --db "$AI_RSS_DB_PATH" \
  --entry-id 1234
```

5. Inspect extracted content state.

```bash
python3 scripts/fulltext_fetch.py list-content \
  --db "$AI_RSS_DB_PATH" \
  --status ready \
  --limit 100
```

## Data Contract
- Reads from existing `entries` table:
  - `id`, `canonical_url`, `url`, `title`.
- Writes to `entry_content` table:
  - `entry_id` (unique, one row per entry)
  - `source_url`, `final_url`, `http_status`
  - `extractor` (`trafilatura`, `html-parser`, or `none`)
  - `content_text`, `content_hash`, `content_length`
  - `status` (`ready` or `failed`)
  - `retry_count`, `last_error`, timestamps.

## Extraction and Update Rules
- URL source priority: `canonical_url` first, fallback to `url`.
- Attempt `trafilatura` extraction when dependency is available, fallback to built-in HTML parser.
- Upsert by `entry_id`:
  - Success: write/update full text and reset `retry_count` to `0`.
  - Failure with existing `ready` content: keep old text, keep status `ready`, record `last_error`.
  - Failure without ready content: status becomes `failed`, increment `retry_count`, set `next_retry_at`.
- Failed retries are capped by `--max-retries` (default `3`) and paced by `--retry-backoff-minutes`.
- `--force` allows refetching already `ready` rows.
- `--refetch-days N` allows refreshing rows older than `N` days.

## Configurable Parameters
- `--db`
- `AI_RSS_DB_PATH` (recommended absolute path in multi-agent runtime)
- `--limit`
- `--force`
- `--only-failed`
- `--refetch-days`
- `--oldest-first`
- `--timeout`
- `--max-bytes`
- `--min-chars`
- `--max-retries`
- `--retry-backoff-minutes`
- `--user-agent`
- `--disable-trafilatura`
- `--fail-on-errors`

## Error Handling
- Missing `entries` table: return actionable error and stop.
- Network/HTTP/parse errors: store failure state and continue processing other entries.
- Non-text content types (PDF/image/audio/video/zip): mark as failed for that entry.
- Extraction too short (`--min-chars`): treat as failure to avoid low-quality body text.

## References
- `references/schema.md`
- `references/fetch-rules.md`

## Assets
- `assets/config.example.json`

## Scripts
- `scripts/fulltext_fetch.py`
