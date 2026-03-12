---
name: fetch-abstract-to-kb
description: "Fetch DOI candidates from PostgreSQL `journals` and batch write `abstract` by DOI. Use when you need DB-only backfill workflow: (1) select newest rows where doi is not empty, author is not empty, and abstract is empty (default limit 10), then (2) write prepared abstract values back in batch by DOI."
---

# Fetch Abstract to KB

## Core Goal
- Provide only two DB operations:
  1. Fetch DOI candidates from `journals`.
  2. Batch update `abstract` by DOI.

## Required Environment
- `KB_DB_HOST`
- `KB_DB_PORT`
- `KB_DB_NAME`
- `KB_DB_USER`
- `KB_DB_PASSWORD`

## Workflow
1. Fetch DOI list (default 10 rows):

```bash
python3 scripts/fetch_abstract_to_kb.py fetch-doi
```

2. Optionally override row limit:

```bash
python3 scripts/fetch_abstract_to_kb.py fetch-doi --limit 10
```

3. Prepare JSON input for batch update (one of the two formats):

```json
[
  {"doi": "10.1000/a", "abstract": "text A"},
  {"doi": "10.1000/b", "abstract": "text B"}
]
```

or

```json
{
  "10.1000/a": "text A",
  "10.1000/b": "text B"
}
```

4. Batch write abstract by DOI:

```bash
python3 scripts/fetch_abstract_to_kb.py write-abstracts --input abstracts.json
```

## Query/Write Contract
- Fetch filter:
  - `doi` not empty
  - `author` not empty (fall back to `authors` when `author` is unavailable)
  - `abstract` empty (`NULL` or blank)
- Fetch order:
  - `ORDER BY created_at DESC NULLS LAST`
- Fetch default limit:
  - `10`
- Write guard:
  - Update only when target row `abstract` is still empty.

## Script
- `scripts/fetch_abstract_to_kb.py`
