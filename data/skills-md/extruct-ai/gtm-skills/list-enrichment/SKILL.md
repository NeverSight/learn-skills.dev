---
name: list-enrichment
description: >
  Add research-powered enrichment columns to Extruct company tables via the API.
  Use when the user wants to add enrichment columns (e.g. funding, verticals,
  tech stack) to an existing Extruct table, run column configs from
  enrichment-design, or monitor enrichment progress. Triggers on: "enrich",
  "add column", "add data point", "research column", "enrich table",
  "enrichment", "add a field", "run enrichment", "monitor enrichment".
---

# Table Enrichment

Add research-powered enrichment columns to Extruct company tables.

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

1. Read local reference: [references/api_reference.md](references/api_reference.md)
2. Fetch live docs: https://www.extruct.ai/docs
3. Compare endpoints, params, and response fields
4. If discrepancies found:
   - Update the local reference file
   - Flag changes to the user before proceeding
5. Proceed with the skill workflow

### 1. Confirm the table

Get the table ID from the user (URL or ID). Fetch table metadata via `GET /tables/{table_id}`. Show the user: table name, row count, existing columns.

### 2. Get column configs

Two paths:

**Path A: From enrichment-design** — User has `column_configs` ready. Confirm and proceed.

**Path B: Design on the fly** — Confirm with the user:

1. **What data point?** — what to research (e.g. "funding stage", "primary vertical", "tech stack")
2. **Output format** — pick the right format:

| Format | When to use | Extra params |
|---|---|---|
| `text` | Free-form research output | — |
| `number` / `money` | Numeric data (revenue, headcount) | — |
| `select` | Single choice from known categories | `labels: [...]` |
| `multiselect` | Multiple tags from known categories | `labels: [...]` |
| `json` | Structured multi-field data | `output_schema: {...}` |
| `grade` | 1-5 score | — |
| `label` | Single tag from list | `labels: [...]` |
| `date` | Date values | — |
| `url` / `email` / `phone` | Contact info | — |

3. **Agent type** — default `research_pro`. Use `llm` when no web research needed (classification from existing profile data).

### 3. Write the prompt

Craft a clear prompt using `{input}` for the row's domain value. Prompt guidelines:

- Be specific about what to find
- Specify the exact output format in the prompt (e.g. "Return ONLY a number in millions USD")
- Include fallback instruction (e.g. "If not found, return N/A")
- For `select`/`multiselect`, the labels constrain the output — the prompt should guide which label to pick

### 4. Create the column(s)

Create columns via `POST /tables/{table_id}/columns` with the `column_configs` array.

### 5. Trigger enrichment (only the new columns)

Run via `POST /tables/{table_id}/run` with `{ "mode": "new", "columns": [new_column_ids] }`.

**Important:** Always scope the run to the newly created column(s) only. Avoid broad or implicit run payloads when you only intend to enrich specific columns.

Report: run ID, rows queued, and table URL.

### 6. Monitor progress

Poll the table data via `GET /tables/{table_id}/data` every 30 seconds. For each row, check the `status` field of the relevant column cells (`done`, `pending`, `failed`).

Show the user:
- Current % complete (done cells / total cells)
- Number of failed cells (if any)
- Estimated time remaining (based on rate so far)

Stop polling when all cells are done or failed.

### 7. Quality spot-check

After enrichment completes (or after 50%+ is done), fetch a sample of 5-10 enriched rows and display for review.

**Present to user as a table.** Ask:
- "Does the data quality look right?"
- "Any columns returning garbage or N/A too often?"
- "Should we adjust any prompts and re-run?"

If quality issues are found:
1. Delete the problematic column
2. Adjust the prompt
3. Re-create and re-run

## API Reference

See [references/api_reference.md](references/api_reference.md) for full API spec: all output formats, agent types, prompt variables, and endpoints.
