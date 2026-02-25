---
name: sm-bigquery-analyst
description: Query SourceMedium-hosted BigQuery safely. Emits SQL receipts. SELECT-only, cost-guarded. Use when users need help with BigQuery setup, access verification, or analytical questions against SourceMedium datasets.
compatibility: Requires gcloud CLI, bq CLI, and network access to BigQuery.
metadata:
  author: sourcemedium
  version: "1.0"
---

# SourceMedium BigQuery Analyst

Use this skill to help end users work with SourceMedium BigQuery data from setup to analysis.

## Workflow

1. **Verify environment** (run these before any analysis)
2. Confirm project and dataset/table visibility
3. Use docs-first guidance for definitions and table discovery
4. Answer analytical questions with reproducible SQL receipts
5. Call out assumptions and caveats explicitly

## Setup Verification

Run these commands in order before writing analysis SQL:

```bash
# 1. Check CLI tools are installed
gcloud --version && bq version

# 2. Check authenticated account
gcloud auth list

# 3. Check active project
gcloud config get-value project

# 4. Validate BigQuery API access (dry-run)
bq query --use_legacy_sql=false --dry_run 'SELECT 1 AS ok'

# 5. Test table access (your project is named sm-<tenant_id>)
#    Example: if your tenant is "acme-corp", your project is sm-acme-corp
bq query --use_legacy_sql=false --dry_run "
  SELECT 1 
  FROM \`sm-<tenant_id>.sm_transformed_v2.obt_orders\` 
  LIMIT 1
"

# 6. Confirm you can actually read data (not just dry-run)
bq query --use_legacy_sql=false "
  SELECT 1
  FROM \`sm-<tenant_id>.sm_transformed_v2.obt_orders\`
  WHERE is_order_sm_valid = TRUE
  LIMIT 1
"
```

If any step fails, see `references/TROUBLESHOOTING.md` and guide the user to request access.

## Safety Rules

These are hard constraints. Do not bypass.

### Query Safety

1. **SELECT-only** — deny: INSERT, UPDATE, DELETE, MERGE, CREATE, DROP, EXPORT, COPY
2. **Dry-run first** when iterating on new queries:
   ```bash
   bq query --use_legacy_sql=false --dry_run '<SQL>'
   ```
3. **Enforce cost limit** with maximum bytes billed:
   ```bash
   bq query --use_legacy_sql=false --maximum_bytes_billed=1073741824 '<SQL>'
   ```
   (1GB = 1073741824 bytes. If it fails due to bytes billed, tighten filters or ask for approval.)
4. **Always bound queries**:
   - Add `LIMIT` clause (max 100 rows for exploratory)
   - Use date/partition filters when querying partitioned tables
   - Prefer `WHERE` filters on partition columns

### Data Safety

1. **Default to aggregates** — avoid outputting raw rows unless explicitly requested
2. **PII handling**:
   - Do not output columns likely containing PII (email, phone, address, name) without explicit confirmation
   - If PII is requested, confirm scope and purpose before proceeding
   - Prefer anonymization. Example:
     ```sql
     -- Hash PII instead of exposing raw values
     SELECT TO_HEX(SHA256(LOWER(email))) AS email_hash, ...
     ```

### Cost Guardrails

```sql
-- Good: bounded scan
SELECT ... FROM `sm-<tenant_id>.sm_transformed_v2.obt_orders`
WHERE DATE(order_processed_at_local_datetime) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
LIMIT 100

-- Bad: full table scan
SELECT ... FROM `sm-<tenant_id>.sm_transformed_v2.obt_orders`  -- no filters
```

## Output Contract

For analytical questions, always return:

1. **Answer** — concise plain-English conclusion
2. **SQL (copy/paste)** — BigQuery Standard SQL used for the result
3. **Notes** — timeframe, metric definitions, grain, scope, timezone, attribution lens
4. **Verify** — `bq query --use_legacy_sql=false --dry_run '<SQL>'` command
5. **Bytes scanned** — if >1GB, note this and ask for approval before running

If access/setup fails, do not fabricate results. Return:

1. Exact failing step
2. Exact project/dataset that failed
3. Direct user to `assets/BIGQUERY_ACCESS_REQUEST_TEMPLATE.md`

## Query Guardrails

1. Fully qualify tables as `` `sm-<tenant_id>.dataset.table` ``
2. For order analyses, default to `WHERE is_order_sm_valid = TRUE`
3. Use `sm_store_id` (not `smcid` — that name does not exist in customer tables)
4. Use `SAFE_DIVIDE` for ratio math
5. Handle DATE/TIMESTAMP typing explicitly (`DATE(ts_col)` when comparing to dates)
6. Use `order_net_revenue` for revenue metrics (not `order_gross_revenue` unless explicitly asked)
7. **Prefer `*_local_datetime` columns** when available for date-based reporting; otherwise be explicit about UTC vs local
8. **For enumerations** (channel, platform, status), discover values with `SELECT DISTINCT` first, then use exact match. Reserve `LIKE`/`REGEXP` for free-text fields (`utm_campaign`, `product_title`, `page_path`)
9. **LTV tables (`rpt_cohort_ltv_*`)**: always filter `sm_order_line_type` to exactly ONE value

## References

- `references/SCHEMA.md` — key tables, grains, columns, and naming conventions
- `references/QUERY_PATTERNS.md` — common SQL patterns and LTV/cohort rules
- `references/TROUBLESHOOTING.md` — auth, permission, and API issues
- `assets/BIGQUERY_ACCESS_REQUEST_TEMPLATE.md` — copy/paste request for users without access
