---
name: table-creation
description: >
  Create an Extruct company table from user-provided data, upload rows, and
  optionally add enrichment columns. Handles the full flow: parse input (CSV,
  pasted list, or structured data), create or reuse a table, upload domains in
  batches, add agent columns, and trigger enrichment. Triggers on: "create table",
  "upload companies", "add to extruct", "new extruct table", "import companies",
  "upload list to extruct".
---

# Create Table

End-to-end workflow: parse company data → create/reuse Extruct table → upload rows → add columns → run enrichment.

## Environment

| Variable | Service |
|----------|---------|
| `EXTRUCT_API_TOKEN` | Extruct API |

Before making API calls, check that `EXTRUCT_API_TOKEN` is set by running `test -n "$EXTRUCT_API_TOKEN" && echo "set" || echo "missing"`. If missing, ask the user to provide their Extruct API token and set it via `export EXTRUCT_API_TOKEN=<value>`. Do not proceed until confirmed.

Base URL: `https://api.extruct.ai/v1`

## Official API Reference

- https://www.extruct.ai/docs

## Workflow

### Step 0: Verify API reference

1. Read local reference: [../list-enrichment/references/api_reference.md](../list-enrichment/references/api_reference.md)
2. Fetch live docs: https://www.extruct.ai/docs
3. Compare endpoints, params, and response fields (especially `POST /tables`, `POST /tables/{id}/rows`, `POST /tables/{id}/columns`)
4. If discrepancies found:
   - Update the local reference file
   - Flag changes to the user before proceeding
5. Proceed with the skill workflow

### 1. Parse input data

Accept data in any of these formats:

**Pasted list** (most common): User pastes company names, URLs, and metadata as freeform text. Parse into structured records. Extract domains by stripping protocol, `www.`, and trailing slashes.

**CSV file**: Read CSV, map columns to find the URL/domain column.

**Extruct table URL**: Fetch data from existing table via API.

Key rules:
- Skip entries with no URL (e.g., "Stealth" companies)
- Deduplicate by domain
- Ask which metadata fields to preserve (country, stage, industry, etc.)

### 2. Decide: create new table or add to existing

Ask the user:
- **New table**: Create via `POST /tables`
- **Existing table**: User provides table ID or URL (`https://app.extruct.ai/tables/{id}`)

To create a new company table, use `POST /tables` with `kind: "company"` and a single input column (`kind: "input"`, `key: "input"`). The `company` kind auto-enriches each domain with Company Profile, Company Name, and Company Website columns.

### 3. Upload rows in batches

Upload domains via `POST /tables/{table_id}/rows` in batches of 50. Each row: `{ "data": { "input": "domain.com" } }`. Add 0.5s delay between batches.

Report progress: "Batch 1: uploaded 50 rows OK"

### 4. Add agent columns (optional)

If the user wants enrichment columns (industry, funding, etc.), add them after upload via `POST /tables/{table_id}/columns`.

**Column types by use case:**

| User says | Agent type | Output format | Notes |
|-----------|------------|---------------|-------|
| "add industry" | `llm` | `select` with labels | Classification from profile, no web research needed |
| "add funding" | `research_pro` | `text` | Needs web research |
| "classify by vertical" | `llm` | `select` with labels | Classification |
| "find their tech stack" | `research_pro` | `text` | Needs web research |
| "score fit 1-5" | `llm` or `research_reasoning` | `grade` | Assessment |
| "tag multiple categories" | `llm` | `multiselect` with labels | Multiple tags |

See the [list-enrichment skill](../list-enrichment/SKILL.md) for full column types and output formats.

### 5. Trigger enrichment

Run via `POST /tables/{table_id}/run` with `{ "mode": "new", "columns": [new_column_ids] }`, scoped to only the newly added agent columns.

If no agent columns were added, skip this step.

### 6. Report to user

Provide:
- Table URL: `https://app.extruct.ai/tables/{table_id}`
- Row count uploaded
- Columns added
- Cells queued for enrichment
- Any rows skipped (stealth, duplicates, invalid URLs)

## Input Parsing Patterns

### Freeform pasted list (5-line groups)

```
Company Name
URL (or "Stealth")
Country
Industry
Funding Stage
```

Parse by splitting into 5-line chunks. Filter where URL == "Stealth".

### CSV

Map columns: look for "website", "url", "domain", "Company Website". Extract domain from whichever column contains URLs.

### Single-column domain list

```
example.com
startup.io
company.ai
```

Direct upload — each line is a domain.

## Common Pitfalls

- **Domain format**: Strip protocol and trailing slash. `https://www.example.com/` → `example.com`
- **Stealth companies**: Skip — no domain to enrich
- **Duplicates**: Deduplicate by domain before upload
- **Batch limits**: Max 50 rows per API call
- **Column labels**: For `select`/`multiselect`, collect unique values from user data to build the label list
- **Run timing**: Trigger run AFTER all rows and columns are added
