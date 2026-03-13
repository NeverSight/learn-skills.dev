---
name: fetch-meta-from-kb
description: Fetch recent `journals` rows directly from PostgreSQL and return a JSON array containing `doi`, `title`, `abstract`, and `date` (filtered by rolling `DAYS` on `created_at`). Use when users need raw paper payloads for downstream processing without LLM filtering or hotspot report generation.
---

# Fetch Meta from KB

## Workflow

1. Read DB env vars from `.env` or process env: `KB_DB_HOST`, `KB_DB_PORT`, `KB_DB_NAME`, `KB_DB_USER`, `KB_DB_PASSWORD`.
2. Query `journals` where `created_at >= now_utc - DAYS`, ordered by `created_at DESC`, selecting only `doi`, `title`, `abstract`, `date`.
3. Return/write JSON array records with exactly these fields: `doi`, `title`, `abstract`, `date`.

## Script

Run:

```bash
cd fetch-meta-from-kb
python3 scripts/fetch_meta_from_kb.py --days 7 --output selected-abstract.json
```

Env example:

```dotenv
KB_DB_HOST=<HOST>
KB_DB_PORT=5432
KB_DB_NAME=<DATABASE>
KB_DB_USER=<USER>
KB_DB_PASSWORD=<PASSWORD>
```

## Output Rules

- Return UTF-8 JSON.
- Keep each item as: `doi`, `title`, `abstract`, `date`.
- Do not output DB credentials.
