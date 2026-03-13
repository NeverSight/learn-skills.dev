---
name: Ops Enrichment Manager
description: |
  Configure and run AI enrichment on Ops table columns, and check enrichment job progress.
  Use when a user asks "enrich this column", "check enrichment status", "how's enrichment going",
  "enrich the company data", or needs to run AI-powered data enrichment on their prospect tables.
  Returns enrichment job status, progress percentage, and completion results.
metadata:
  author: sixty-ai
  version: "2"
  category: enrichment
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - prospecting
  triggers:
    - pattern: "enrich column"
      intent: "enrich_table_column"
      confidence: 0.90
      examples:
        - "enrich this column"
        - "enrich the company column"
        - "run enrichment on this column"
        - "fill in the missing data"
    - pattern: "check enrichment"
      intent: "get_enrichment_status"
      confidence: 0.85
      examples:
        - "check enrichment status"
        - "how's the enrichment going"
        - "is enrichment done yet"
        - "enrichment progress"
    - pattern: "enrich my table"
      intent: "enrich_table_column"
      confidence: 0.85
      examples:
        - "enrich this table"
        - "run enrichment"
        - "enrich the data"
        - "fill in the blanks"
    - pattern: "start enrichment"
      intent: "enrich_table_column"
      confidence: 0.85
      examples:
        - "start enriching"
        - "kick off enrichment"
        - "begin enrichment on this column"
        - "enrich all rows"
  keywords:
    - "enrich"
    - "enrichment"
    - "status"
    - "progress"
    - "fill"
    - "populate"
    - "data"
    - "column"
    - "AI"
    - "generate"
  required_context: []
  optional_context:
    - table_id
    - column_id
  inputs:
    - name: table_id
      type: string
      description: "ID of the ops table to enrich"
      required: false
    - name: column_id
      type: string
      description: "ID of the column to enrich"
      required: false
    - name: prompt
      type: string
      description: "Custom AI prompt for enrichment (what to generate or look up)"
      required: false
  outputs:
    - name: enrichment_job
      type: object
      description: "Enrichment job details with ID, status, and progress"
    - name: enrichment_status
      type: object
      description: "Current enrichment progress with completion percentage and row counts"
  requires_capabilities:
    - ops_tables
  execution_mode: sync
  timeout_ms: 30000
  priority: high
  tags:
    - ops
    - enrichment
    - prospecting
    - AI
---

## Available Context
@_platform-references/org-variables.md

# Ops Enrichment Manager

## Goal

Run AI-powered enrichment on Ops table columns and monitor enrichment job progress. Enrichment transforms empty or sparse columns into rich, AI-generated data -- company summaries, personalized intros, lead scores, industry classifications, and more.

Enrichment is the step that turns a raw list of names and emails into an actionable prospect database. Without it, reps are stuck doing manual research. With it, every row gets AI-analyzed data in minutes.

## Required Capabilities
- **Ops Tables**: Access to enrichment APIs for ops tables

## Inputs
- `table_id`: ID of the ops table containing the column to enrich
- `column_id`: ID of the specific column to enrich
- `prompt`: Custom AI prompt that describes what to generate (e.g., "Write a one-line personalized intro based on the lead's title and company")

## Instructions

### Starting Enrichment

When the user wants to enrich a column:

1. Identify the table and column. If the user says "enrich the company summary column", resolve the table and column IDs.
2. If no column is specified, ask which column to enrich. Show the table's columns and suggest candidates:
   - Columns of type `ai_generate` are natural enrichment targets
   - Empty or sparse columns benefit most from enrichment
3. If the column has a built-in enrichment type (e.g., company data lookup, email finder), no custom prompt is needed.
4. For AI-generated columns, check if a prompt is configured. If not, ask the user:
   - "What should the AI generate for this column? For example: 'Write a personalized outreach opener based on the lead's role and company.'"
5. Call `execute_action("enrich_table_column", { table_id: "<id>", column_id: "<col_id>", prompt: "<prompt>" })`
6. Report that enrichment has started: "Enrichment started for [Column Name] in [Table Name]. Processing X rows -- I'll check progress for you."

### Checking Enrichment Status

When the user asks about enrichment progress:

1. Call `execute_action("get_enrichment_status", { table_id: "<id>" })`
2. Present a clear status report:
   - Overall progress percentage
   - Rows completed vs total
   - Estimated time remaining (if available)
   - Any errors or failures
3. If enrichment is complete, congratulate and suggest next steps: "Enrichment complete! All 142 rows now have [column name] data. Want to view the results?"

### Suggesting Enrichment

When viewing a table with empty columns, proactively suggest enrichment:
- "I notice the [Column Name] column is mostly empty (12% filled). Want me to run enrichment on it?"
- For `ai_generate` columns without data, suggest a prompt based on the column name

## Available Actions

| Action | Parameters | Returns |
|--------|-----------|---------|
| `enrich_table_column` | `{ table_id: string, column_id: string, prompt?: string }` | Enrichment job with ID and status |
| `get_enrichment_status` | `{ table_id: string }` | Progress with completion %, row counts, errors |

## Output Format

### Enrichment Started
```
ENRICHMENT STARTED
  Table: Lead Prospects
  Column: Company Summary
  Rows to process: 142
  Prompt: "Write a 2-sentence company overview based on the company name and domain"

I'll check back on progress. You can ask me "how's enrichment going?" anytime.
```

### Enrichment Status
```
ENRICHMENT PROGRESS
  Table: Lead Prospects
  Column: Company Summary

  [=========>          ] 67% complete
  95 of 142 rows processed
  3 errors (missing company data)
  Est. remaining: ~2 minutes
```

### Enrichment Complete
```
ENRICHMENT COMPLETE
  Table: Lead Prospects
  Column: Company Summary

  142 rows processed
  139 successful
  3 skipped (insufficient source data)

Want to view the enriched data?
```

## Error Handling

### No enrichable columns
If the table has no columns suitable for enrichment: "This table doesn't have any AI-generated or enrichable columns. Want me to add one? For example, I can add a 'Company Summary' column that AI will populate."

### Enrichment already running
If enrichment is already in progress for the requested column: "Enrichment is already running on [Column Name] -- currently at X%. Want me to check back when it's done?"

### Missing source data
If enrichment fails for some rows because required source columns are empty: "Enrichment completed for 95% of rows. 7 rows were skipped because they're missing [Source Column] data. Want to fill those in first?"

### Prompt not provided for AI column
If the user starts enrichment on an `ai_generate` column without a prompt: "This is an AI-generated column -- I need to know what to generate. What should each cell contain? For example: 'A personalized outreach opening line based on the lead's role and recent company news.'"

## Guidelines
- Always show which table and column are being enriched -- avoid ambiguity
- For large tables (500+ rows), set expectations: "This will take a few minutes for 500 rows"
- Suggest checking status after starting rather than waiting: "Ask me 'how's enrichment going?' in a couple minutes"
- When enrichment finishes, suggest viewing the results or running a follow-up action (like querying the enriched data)
- If multiple columns need enrichment, suggest running them sequentially to avoid overwhelming the system
- Always explain what the AI will generate before starting -- no surprises
