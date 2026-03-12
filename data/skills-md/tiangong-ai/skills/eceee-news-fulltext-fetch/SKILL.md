---
name: eceee-news-fulltext-fetch
description: Discover article URLs from https://www.eceee.org/all-news/ and extract/persist full article text into SQLite with retry-safe incremental sync. Use when building or maintaining an eceee news fulltext corpus for downstream search, indexing, or summarization.
---

# eceee News Fulltext Fetch

## Core Goal
- Discover news article URLs from `https://www.eceee.org/all-news/`.
- Persist discovered entry metadata into SQLite.
- Fetch and extract article body text from each entry page.
- Persist status and text in a companion table (`entry_content`) with retry-safe updates.

## Triggering Conditions
- Receive a request to extract full text from eceee news archive pages.
- Receive a request to run incremental fulltext sync for eceee news links.
- Need a resilient local SQLite queue for discovery + extraction + retries.

## Workflow
1. Initialize database.

```bash
export ECEEE_NEWS_DB_PATH="/absolute/path/to/eceee_news.db"
python3 scripts/fulltext_fetch.py init-db --db "$ECEEE_NEWS_DB_PATH"
```

2. Discover links and fetch fulltext incrementally.

```bash
python3 scripts/fulltext_fetch.py sync \
  --db "$ECEEE_NEWS_DB_PATH" \
  --index-url "https://www.eceee.org/all-news/" \
  --limit 50 \
  --min-chars 180
```

3. Discover only (refresh URL catalog without fetching bodies).

```bash
python3 scripts/fulltext_fetch.py sync \
  --db "$ECEEE_NEWS_DB_PATH" \
  --discover-only
```

4. Fetch one entry on demand.

```bash
python3 scripts/fulltext_fetch.py fetch-entry \
  --db "$ECEEE_NEWS_DB_PATH" \
  --entry-id 123
```

Or by URL:

```bash
python3 scripts/fulltext_fetch.py fetch-entry \
  --db "$ECEEE_NEWS_DB_PATH" \
  --url "https://www.eceee.org/all-news/news/example-slug/"
```

5. Inspect stored state.

```bash
python3 scripts/fulltext_fetch.py list-entries --db "$ECEEE_NEWS_DB_PATH" --limit 100
python3 scripts/fulltext_fetch.py list-content --db "$ECEEE_NEWS_DB_PATH" --status ready --limit 100
```

## Data Contract
- `entries` table stores discovery metadata:
  - `url`, `title`, `published_at`
  - `discovered_at`, `last_seen_at`
- `entry_content` table stores extraction result (one row per `entry_id`):
  - `source_url`, `final_url`, `http_status`
  - `extractor` (`trafilatura`, `html-parser`, or `none`)
  - `content_text`, `content_hash`, `content_length`
  - `status` (`ready` or `failed`)
  - retry fields + timestamps

## Extraction and Update Rules
- Discovery source is `https://www.eceee.org/all-news/`, extracting anchor tags with class `newslink` under `/all-news/news/`.
- Fulltext extraction uses article main content region (`mainContentColumn`) and removes related-news/share blocks.
- Extraction path:
  1. `trafilatura` (if installed and not disabled)
  2. built-in HTML parser fallback
- Upsert by `entry_id`:
  - Success: set `ready`, write text/hash/length, reset retry counters.
  - Failure with existing `ready` content: keep old content, update error/retry metadata.
  - Failure without ready content: set `failed`, increment retries, set `next_retry_at`.

## Configurable Parameters
- `--db`
- `ECEEE_NEWS_DB_PATH`
- `--index-url`
- `--discover-only`
- `--limit`
- `--force`
- `--only-failed`
- `--since-date`
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
- Index fetch/parse failure returns actionable error.
- HTTP/network/content-type failures are recorded per entry and do not stop the whole sync batch.
- Short extracted text (`< --min-chars`) is treated as failed to avoid low-quality bodies.
- Retry queue is controlled via `max_retries` + exponential backoff.

## References
- `references/schema.md`
- `references/fetch-rules.md`

## Assets
- `assets/config.example.json`

## Scripts
- `scripts/fulltext_fetch.py`
