---
name: ai-tech-rss-fetch
description: Subscribe to AI and tech RSS feeds and persist normalized metadata into SQLite using mature Python tooling (feedparser + sqlite3). Use when adding feed URLs/OPML sources, running incremental sync with deduplication, and storing entry metadata without full-text extraction or summarization.
---

# AI Tech RSS Fetch

## Core Goal
- Subscribe to RSS/Atom sources.
- Persist feed and entry metadata to SQLite.
- Deduplicate entries with stable keys across runs.
- Keep only metadata; do not fetch full article bodies and do not summarize.

## Triggering Conditions
- Receive a request to subscribe RSS feeds from URLs or OPML.
- Receive a request to run incremental RSS sync reliably.
- Need stable metadata persistence for downstream processing.
- Need dedupe-safe storage of feed items over repeated runs.

## Workflow
1. Prepare runtime and database.
- Ensure dependency is installed: `python3 -m pip install feedparser`.
- In multi-agent runtimes, pin DB to an absolute path before any command:

```bash
export AI_RSS_DB_PATH="/absolute/path/to/workspace-rss-bot/ai_rss.db"
```

- Initialize SQLite schema once:

```bash
python3 scripts/rss_subscribe.py init-db --db "$AI_RSS_DB_PATH"
```

2. Add feed subscriptions.
- Add one feed URL:

```bash
python3 scripts/rss_subscribe.py add-feed --db "$AI_RSS_DB_PATH" --url "https://example.com/feed.xml"
```

- Import feeds from OPML:

```bash
python3 scripts/rss_subscribe.py import-opml --db "$AI_RSS_DB_PATH" --opml assets/hn-popular-blogs-2025.opml
```

3. Run incremental sync.
- Fetch active feeds and store metadata:

```bash
python3 scripts/rss_subscribe.py sync --db "$AI_RSS_DB_PATH" --max-feeds 20 --max-items-per-feed 100
```

- Optional one-feed sync:

```bash
python3 scripts/rss_subscribe.py sync --db "$AI_RSS_DB_PATH" --feed-url "https://example.com/feed.xml"
```

4. Query persisted metadata.
- List feeds:

```bash
python3 scripts/rss_subscribe.py list-feeds --db "$AI_RSS_DB_PATH" --limit 50
```

- List recent entries:

```bash
python3 scripts/rss_subscribe.py list-entries --db "$AI_RSS_DB_PATH" --limit 100
```

## Input Requirements
- Supported inputs:
  - RSS XML feed URLs.
  - OPML feed list files.

## Output Contract (Metadata Only)
- Persist `feeds` metadata to SQLite:
  - `feed_url`, `feed_title`, `site_url`, `etag`, `last_modified`, status fields.
- Persist `entries` metadata to SQLite:
  - `dedupe_key`, `guid`, `url`, `canonical_url`, `title`, `author`,
    `published_at`, `updated_at`, `summary`, `categories`, timestamps.
- Do not store generated summaries and do not create archive markdown files.

## Configurable Parameters
- `db_path`
- `AI_RSS_DB_PATH` (recommended absolute path in multi-agent runtime)
- `opml_path`
- `feed_urls`
- `max_feeds_per_run`
- `max_items_per_feed`
- `user_agent`
- `seen_ttl_days`
- `enable_conditional_get`
- Example config: `assets/config.example.json`

## Error and Boundary Handling
- Feed HTTP/network failure: keep syncing other feeds and record `last_error`.
- Feed `304 Not Modified`: skip entry parsing and keep state.
- Missing `guid` and `link`: use hashed fallback dedupe key.
- Dependency missing (`feedparser`): return install guidance.

## Final Output Checklist (Required)
- core goal
- trigger conditions
- input requirements
- metadata schema
- dedupe and sync rules
- command workflow
- configurable parameters
- error handling

Use the following simplified checklist verbatim when the user requests it:

```text
核心目标
输入需求
触发条件
元数据模型
去重与同步规则
命令流程
可配置参数
错误处理
```

## References
- `references/input-model.md`
- `references/output-rules.md`
- `references/time-range-rules.md`

## Assets
- `assets/hn-popular-blogs-2025.opml` (candidate feed pool)
- `assets/config.example.json`

## Scripts
- `scripts/rss_subscribe.py`
