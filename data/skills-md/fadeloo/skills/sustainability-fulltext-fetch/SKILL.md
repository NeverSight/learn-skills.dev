---
name: sustainability-fulltext-fetch
description: Fetch and persist content for DOI-keyed sustainability RSS entries from a separate fulltext SQLite DB, using OpenAlex/Semantic Scholar API metadata first and webpage fulltext extraction as fallback. Use when building resilient DOI-first content enrichment after relevance labeling.
---

# Sustainability Fulltext Fetch

## Core Goal
- Read relevant DOI entries from RSS metadata DB.
- Write fetched content into a separate fulltext DB.
- Process only relevant entries (`is_relevant=1`).
- Prefer API metadata retrieval by DOI (OpenAlex first, Semantic Scholar fallback).
- Fallback to webpage fulltext extraction when API metadata is unavailable.
- Persist one content row per DOI in `entry_content`.

## Triggering Conditions
- Receive a request to enrich relevant DOI records with abstract/fulltext content.
- Receive a request to replace webpage-first crawling with API-first enrichment.
- Need retry-safe incremental updates without duplicate rows.

## Workflow
1. Ensure upstream DOI/relevance data exists.

```bash
export SUSTAIN_RSS_DB_PATH="/absolute/path/to/workspace-rss-bot/sustainability_rss.db"
export SUSTAIN_FULLTEXT_DB_PATH="/absolute/path/to/workspace-rss-bot/sustainability_fulltext.db"
python3 scripts/fulltext_fetch.py init-db --content-db "$SUSTAIN_FULLTEXT_DB_PATH"
```

2. Run incremental sync (API first, webpage fallback).

```bash
python3 scripts/fulltext_fetch.py sync \
  --rss-db "$SUSTAIN_RSS_DB_PATH" \
  --content-db "$SUSTAIN_FULLTEXT_DB_PATH" \
  --limit 50 \
  --openalex-email "you@example.com" \
  --api-min-chars 80 \
  --min-chars 300
```

3. Fetch one DOI on demand.

```bash
python3 scripts/fulltext_fetch.py fetch-entry \
  --rss-db "$SUSTAIN_RSS_DB_PATH" \
  --content-db "$SUSTAIN_FULLTEXT_DB_PATH" \
  --doi "10.1038/nature12373"
```

4. Inspect stored content state.

```bash
python3 scripts/fulltext_fetch.py list-content \
  --rss-db "$SUSTAIN_RSS_DB_PATH" \
  --content-db "$SUSTAIN_FULLTEXT_DB_PATH" \
  --status ready \
  --limit 100
```

## Data Contract
- Reads from RSS DB `entries`:
  - `doi`, `doi_is_surrogate`, `is_relevant`, `canonical_url`, `url`, `title`.
- Writes to fulltext DB `entry_content` (primary key `doi`):
  - source URL/status/extractor
  - `content_kind` (`abstract` or `fulltext`)
  - `content_text`, `content_hash`, `content_length`
  - retry fields and timestamps.

## Extraction Priority
1. API metadata path:
- OpenAlex by DOI.
- Semantic Scholar fallback by DOI.
- If accepted (`--api-min-chars`), persist as `content_kind=abstract`.

2. Webpage fallback path:
- Use `canonical_url` then `url`.
- Extract with `trafilatura` when available, else built-in HTML parser.
- Persist as `content_kind=fulltext`.

## Update Semantics
- Upsert key: `doi`.
- Success: status `ready`, reset retry counters.
- Failure with existing ready row: keep old content, record latest error.
- Failure without ready row: set `status=failed`, increment retry state.

## Configurable Parameters
- `--rss-db`
- `--content-db`
- `SUSTAIN_RSS_DB_PATH`
- `SUSTAIN_FULLTEXT_DB_PATH`
- `--limit`
- `--force`
- `--only-failed`
- `--refetch-days`
- `--timeout`
- `--max-bytes`
- `--min-chars`
- `--openalex-email` / `OPENALEX_EMAIL`
- `--s2-api-key` / `S2_API_KEY`
- `--api-timeout`
- `--api-min-chars`
- `--disable-api-metadata`
- `--max-retries`
- `--retry-backoff-minutes`
- `--user-agent`
- `--disable-trafilatura`
- `--fail-on-errors`

## Error Handling
- Missing DOI-keyed `entries` table: stop with actionable message.
- RSS DB and fulltext DB path collision: fail fast and require separate files.
- API/network/HTTP failures: record failures and continue queue.
- Webpage non-text content: mark failed for that DOI.
- Short extraction: fail by threshold to avoid low-quality content.

## References
- `references/schema.md`
- `references/fetch-rules.md`

## Assets
- `assets/config.example.json`

## Scripts
- `scripts/fulltext_fetch.py`
