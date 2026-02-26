---
name: sustainability-rss-fetch
description: Ingest all sustainability journal RSS entries into a dedicated RSS SQLite database first, keyed by DOI, then mark relevance and prune non-relevant rows to DOI-only. Use when building a DOI-first ingestion pipeline with mandatory full ingestion before topic filtering.
---

# Sustainability RSS Fetch

## Core Goal
- Ingest all RSS/Atom items into SQLite before topic filtering.
- Use `doi` as the primary key in `entries`.
- Keep RSS metadata isolated in its own DB file.
- After semantic screening, keep relevant rows and prune non-relevant rows to DOI-only.

## Triggering Conditions
- Receive a request to import sustainability feeds and persist all fetched records first.
- Receive a request to do prompt-based topic screening after DB ingestion.
- Receive a request to convert irrelevant rows into lightweight DOI-only records.
- Need stable DOI-keyed storage for downstream API/fulltext/summarization.

## Mandatory Workflow
1. Prepare runtime and RSS metadata DB path.

```bash
python3 -m pip install feedparser
export SUSTAIN_RSS_DB_PATH="/absolute/path/to/workspace-rss-bot/sustainability_rss.db"
python3 scripts/rss_subscribe.py init-db --db "$SUSTAIN_RSS_DB_PATH"
```

2. Collect RSS window and ingest all fetched items first.

```bash
python3 scripts/rss_subscribe.py collect-window \
  --db "$SUSTAIN_RSS_DB_PATH" \
  --opml assets/journal.opml \
  --start 2026-02-01 \
  --end 2026-02-10 \
  --max-items-per-feed 150 \
  --topic-prompt "筛选与可持续主题相关的文章：生命周期评价、物质流分析、绿色供应链、绿电、绿色设计、减污降碳" \
  --output /tmp/sustainability-candidates.json \
  --pretty
```

3. Screen candidates in agent context (semantic, not regex-only).
- Use `topic_prompt` + user instructions.
- Produce selected `candidate_id` list.

4. Mark selected rows as relevant and prune unselected rows.

```bash
python3 scripts/rss_subscribe.py insert-selected \
  --db "$SUSTAIN_RSS_DB_PATH" \
  --candidates /tmp/sustainability-candidates.json \
  --selected-ids 3,7,12,21
```

Result:
- selected candidates: `is_relevant=1`, keep metadata.
- unselected candidates: clear metadata fields, keep DOI-only row (`is_relevant=0`).

## Optional Maintenance Sync
```bash
python3 scripts/rss_subscribe.py sync --db "$SUSTAIN_RSS_DB_PATH" --max-feeds 20 --max-items-per-feed 100
```

## Source Management
```bash
python3 scripts/rss_subscribe.py add-feed --db "$SUSTAIN_RSS_DB_PATH" --url "https://example.com/feed.xml"
python3 scripts/rss_subscribe.py import-opml --db "$SUSTAIN_RSS_DB_PATH" --opml assets/journal.opml
```

## Query Data
```bash
python3 scripts/rss_subscribe.py list-feeds --db "$SUSTAIN_RSS_DB_PATH" --limit 50
python3 scripts/rss_subscribe.py list-entries --db "$SUSTAIN_RSS_DB_PATH" --limit 100
```

## Data Contract
- `feeds` table: subscription and fetch state.
- `entries` table (`doi` PK):
  - metadata fields (`title/url/summary/categories/...`)
  - `doi_is_surrogate` (when no DOI is present in source)
  - `is_relevant` (`1` relevant, `0` pruned non-relevant, `NULL` not labeled yet)
- Non-relevant rows are pruned to DOI-only payload for storage efficiency.

## Configurable Parameters
- `--db`
- `SUSTAIN_RSS_DB_PATH`
- `--opml`
- `--feed-url`
- `--use-subscribed-feeds`
- `--topic-prompt`
- `--start/--end`
- `--max-feeds`
- `--max-items-per-feed`
- `--user-agent`
- `--cleanup-ttl-days`

## Error and Boundary Handling
- Feed/network failure: continue other feeds and keep errors in feed state.
- Missing `feedparser`: return install guidance.
- Missing DOI in RSS item: create deterministic surrogate DOI key to keep full-ingestion guarantee.
- Invalid selected IDs: fail fast before label/prune write.

## References
- `references/input-model.md`
- `references/output-rules.md`
- `references/time-range-rules.md`

## Assets
- `assets/journal.opml`
- `assets/config.example.json`

## Scripts
- `scripts/rss_subscribe.py`
