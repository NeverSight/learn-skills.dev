---
name: fetch-meta-to-kb
description: Fetch journal articles from Crossref published after a user-specified date and insert them into PostgreSQL `journals` with DOI deduplication. Use when incrementally ingesting journal metadata from `journals_issn` into `journals`.
---

# Fetch Meta to KB

## Core Goal
- Pull `journal-article` records from Crossref after a given `--from-date`.
- Read ISSN seed rows from `journals_issn` (`journal`, `issn1`).
- Insert rows into `journals` with `ON CONFLICT (doi) DO NOTHING`.
- Keep the implementation aligned with `fetch_meta_to_kb.py`.

## Run Workflow
1. Set database connection env vars (user-managed keys prefixed with `KB_`):
- `KB_DB_HOST`
- `KB_DB_PORT`
- `KB_DB_NAME`
- `KB_DB_USER`
- `KB_DB_PASSWORD`
- `KB_LOG_DIR` (required, log output directory)

2. Run incremental fetch with a required date:

```bash
python3 scripts/fetch_meta_to_kb.py --from-date 2024-05-01
```

- If executing through an `exec` tool call, set timeout to **1800 seconds (30 minutes)**.

3. Check logs in:
- `${KB_LOG_DIR}/fetch-meta-to-kb-YYYYMMDD-HHMMSS.log` (UTC timestamp, one file per run)

4. Build user-facing summary strictly from the current run output:
- Prefer `RUN_SUMMARY_JSON` emitted by `fetch_meta_to_kb.py`.
- If JSON is unavailable, parse only this run's `${KB_LOG_DIR}/fetch-meta-to-kb-YYYYMMDD-HHMMSS.log`.
- `total_inserted` must mean rows inserted in this run (after DOI dedup), not cumulative rows in table.

## Behavior Contract
- Query Crossref endpoint: `https://api.crossref.org/journals/{issn}/works`.
- Filter with `type:journal-article,from-pub-date:<from-date>`.
- Keep only items whose `container-title` equals target journal title (case-insensitive).
- Continue pagination with cursor until no matching items remain.
- Store fields in `journals`: `title`, `doi`, `journal`, `authors`, `date`, `abstract` (nullable when Crossref has no abstract).
- Reporting/announcement metrics must use current-run log/summary only.
- Do **not** compute announcement counts via database-wide or time-window SQL such as `WHERE date >= ...`.

## Scope Boundary
- Implement only Crossref incremental fetch + insert into `journals`.

## Script
- `scripts/fetch_meta_to_kb.py`
