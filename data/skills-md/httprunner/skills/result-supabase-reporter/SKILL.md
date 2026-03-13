---
name: result-supabase-reporter
description: "Filter rows from sqlite capture_results and upsert to Supabase with retry-safe sqlite writeback. Use for stat/filter/report/retry-reset workflows, especially task-scoped reporting with --task-id."
---

# Result Supabase Reporter

Use this skill to run a deterministic `sqlite -> Supabase` pipeline around `capture_results`.

## Workflow

1) Select rows
- `stat`: print total sqlite row count for one `--task-id`.
- `filter`: preview upload candidates from `capture_results`.
- Default status filter is `reported IN (0,-1)`.

2) Report rows
- `report`: batch upsert to Supabase and write back sqlite status.
- `--max-rows <n>` sets total cap for one report run.
- For per-task workflows, always pass `--task-id <TASK_ID>` to avoid cross-task uploads.
- Success writeback: `reported=1`, `reported_at=now_ms`, `report_error=NULL`.
- Failure writeback: `reported=-1`, `reported_at=now_ms`, `report_error=<truncated error>`.

3) Retry failures
- `retry-reset`: move failed rows (`reported=-1`) back to pending (`reported=0`), then rerun `report`.

## Run

```bash
npx tsx scripts/result_reporter.ts <subcommand> [flags]
```

Use `npx tsx scripts/result_reporter.ts --help` as the CLI source of truth.

Hotlist commands:

```bash
npx tsx scripts/hotlist_reporter.ts <subcommand> [flags]
```

Use `npx tsx scripts/hotlist_reporter.ts --help` as the CLI source of truth.

## Environment Variables

Required for `report`:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

Optional overrides:
- `TRACKING_STORAGE_DB_PATH` (default `$HOME/.eval/records.sqlite`)
- `RESULT_SQLITE_TABLE` (default `capture_results`)
- `SUPABASE_RESULT_TABLE` (default `capture_results`)
- `SUPABASE_HOTLIST_TABLE` (default `hotlist_catalogs`)

## Recommended Command Patterns

Task-scoped preview:

```bash
npx tsx scripts/result_reporter.ts filter --task-id <TASK_ID> --status 0,-1 --limit 20
```

Task-scoped report:

```bash
export SUPABASE_URL=https://<project>.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=<service_role_key>
npx tsx scripts/result_reporter.ts report --task-id <TASK_ID> --batch-size 100 --max-rows 500
```

Retry failed rows:

```bash
npx tsx scripts/result_reporter.ts retry-reset --app com.tencent.mm --scene onSearch
npx tsx scripts/result_reporter.ts report --task-id <TASK_ID> --status 0,-1
```

## Hotlist Usage

Schema fields:
- `platform_name`
- `rank`
- `catalog_name`
- `catalog_type`
- `release_date` (`date`)
- `collected_date` (`date`)
- `created_at` (`timestamptz`, default `now()`)

Unique constraint:
- `(platform_name, collected_date, rank)`

Initialize hotlist table (Supabase SQL Editor):

```sql
-- references/hotlist_init.sql
```

Insert one row:

```bash
npx tsx scripts/hotlist_reporter.ts insert \
  --platform-name "腾讯视频" \
  --rank 1 \
  --catalog-name "太平年" \
  --catalog-type "电视剧" \
  --release-date "2026-01-01" \
  --collected-date "2026-02-28"
```

Batch insert from JSONL:

```bash
npx tsx scripts/hotlist_reporter.ts insert --input hotlist.jsonl
```

JSONL line example:

```json
{"platform_name":"腾讯视频","rank":1,"catalog_name":"太平年","catalog_type":"电视剧","release_date":"2026-01-01","collected_date":"2026-02-28"}
```

Query by platform and recent days:

```bash
npx tsx scripts/hotlist_reporter.ts query --platform-name "腾讯视频" --last-days 7 --limit 200
```

Query by explicit date range:

```bash
npx tsx scripts/hotlist_reporter.ts query --platform-name "腾讯视频" --from "2026-02-22" --to "2026-02-28"
```

## Failure Handling

- Use `report --dry-run` to validate selection before network writes.
- Check sqlite `report_error` for root cause when `reported=-1`.
- Fix root cause, then rerun `retry-reset` and `report`.

## Resources

- `scripts/result_reporter.ts`: CLI behavior and flags.
- `scripts/hotlist_reporter.ts`: hotlist insert/query behavior and flags.
- `references/sqlite-and-field-mapping.md`: sqlite schema and field mapping.
- `references/supabase-api-and-errors.md`: Supabase upsert contract and error triage.
- `references/init.sql`: Supabase DDL with required unique constraint `(task_id, item_id)`.
- `references/hotlist_init.sql`: Supabase DDL for `hotlist_catalogs`.
- `references/hotlist_http_api.md`: shareable HTTP API doc for external callers.
