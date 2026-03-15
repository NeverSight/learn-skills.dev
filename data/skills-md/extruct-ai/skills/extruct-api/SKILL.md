---
name: extruct-api
description: Run explicit Extruct API tasks through the bundled Extruct CLI. Covers Deep Search, semantic search, lookalike search, company and people tables, column operations, enrichment, and contact finding.
---

# Extruct API

Use `<extruct_api_cli>` for supported Extruct operations. Do not construct raw HTTP requests for operations the CLI already supports.

Extruct AI is a company discovery and research platform for finding, enriching, and evaluating companies. Its core workflows are semantic search, lookalike search, and Deep Search for company discovery, plus AI Tables for repeatable company and people enrichment, scoring, and contact-finding workflows.

## Source Of Truth

Use the bundled CLI and the instructions in this skill as the default path.

When behavior is unclear, when the user asks for a capability that may not be covered here, or when the request may depend on recently changed API behavior, consult the official Extruct API reference as the source of truth:

- https://www.extruct.ai/docs/api-reference/introduction

Decision rule:
- if the CLI already supports the operation, use the CLI
- if the CLI does not cover the operation or the documented behavior here conflicts with the live API, defer to the official API docs

## Resolve The Bundled CLI First

`<extruct_api_cli>` means the absolute path to the bundled CLI script for this skill.

- Resolve it from the directory that contains this `SKILL.md`.
- In shell or Bash tool calls, prefer the resolved absolute path, not `scripts/extruct-api` relative to the workspace root.
- All command examples below use `<extruct_api_cli>` as shorthand for that resolved absolute path.

Example:

```bash
/absolute/path/to/skills/extruct-api/scripts/extruct-api auth user
```

## Core Workflow

This section covers the default operating intent of the skill: identify the Extruct object the user is working with, choose the right execution path, inspect before mutating, and use the CLI to carry the task through to completion.

1. Resolve `<extruct_api_cli>` first, then establish API access. Before the first authenticated CLI call in a conversation, run `<extruct_api_cli> auth user`. If it fails, run `<extruct_api_cli> healthcheck` to distinguish credential problems from connectivity issues.
2. Classify the request into the right Extruct path:
   - if the user provides an Extruct table URL or a raw table UUID, treat it as an existing table operation first
   - if the user provides an Extruct task URL or a raw task UUID, treat it as an existing Deep Search task first
   - company discovery: semantic search, lookalike search, or Deep Search
   - existing table operation: inspect, add/update rows or columns, run, poll, read
   - company-table workflow: enrich or score companies in a reusable table
   - people workflow: find people at companies or enrich existing people rows
3. If the user already has a table or task, inspect it before mutating it. Default inspection is `tables get`, `columns list`, and a small `tables data` page. When you only need a surgical read, add `--columns` on the first `tables data` call instead of fetching the full row payload.
4. Start from the inline command and payload examples in this file. If a payload spans more than a few lines, prefer `--payload-file`. Read `references/column-guide.md` before designing or changing columns.
5. Carry async work through to completion with `tables poll` or `deep-search poll`, then summarize the final result or API error in plain language, including IDs, counts, and the next relevant object when it matters.

If any request shape, field name, response contract, or endpoint capability is uncertain while executing this workflow, re-check the official API reference before proceeding:

- https://www.extruct.ai/docs/api-reference/introduction

## Resolve Extruct Identifiers

Users may provide Extruct objects as raw IDs or as dashboard URLs.

Interpret them as follows:

- if the user provides an Extruct table URL such as `https://app.extruct.ai/tables/<table_id>` or `http://app.extruct.ai/tables/<table_id>`, treat the path segment after `/tables/` as the table id
- if the user provides an Extruct task URL such as `https://app.extruct.ai/tasks/<task_id>` or `http://app.extruct.ai/tasks/<task_id>`, treat the path segment after `/tasks/` as the Deep Search task id
- if the URL includes extra path segments, query params, or fragments, still extract the id from the `/tables/<table_id>` or `/tasks/<task_id>` segment
- if the user provides a raw table UUID, use it directly as the table id
- if the user provides a raw task UUID, use it directly as the task id
- do not ask the user to restate an id that is already present in the URL
- when a table URL is present, default to the existing-table workflow unless the user explicitly asks for a new table or a search workflow
- when a task URL is present, default to the Deep Search task workflow unless the user explicitly asks to start a new search task

Example:

User request:

```text
Add a funding column to http://app.extruct.ai/tables/0a1a669a-9a40-497c-bb00-d49dd8ee5b74
```

Resulting table id:

```text
0a1a669a-9a40-497c-bb00-d49dd8ee5b74
```

First CLI reads:

```bash
<extruct_api_cli> tables get 0a1a669a-9a40-497c-bb00-d49dd8ee5b74
<extruct_api_cli> columns list 0a1a669a-9a40-497c-bb00-d49dd8ee5b74
<extruct_api_cli> tables data 0a1a669a-9a40-497c-bb00-d49dd8ee5b74 --limit 20 --offset 0
```

User request:

```text
Check results for https://app.extruct.ai/tasks/d530c3ad-626c-4d7b-ab15-181d4058e4f8
```

Resulting task id:

```text
d530c3ad-626c-4d7b-ab15-181d4058e4f8
```

First CLI reads:

```bash
<extruct_api_cli> deep-search get d530c3ad-626c-4d7b-ab15-181d4058e4f8
<extruct_api_cli> deep-search results d530c3ad-626c-4d7b-ab15-181d4058e4f8 --limit 20 --offset 0
```

## Choose The Right Company-Finding Path

### Semantic Search

Use semantic search when the user describes a market, ICP, category, product, or use case in natural language.

Typical asks:

- "search Extruct for AI procurement startups"
- "find German fintech companies in Extruct"
- "show me B2B treasury automation companies"

Commands:

```bash
<extruct_api_cli> companies search --query "vertical SaaS for logistics procurement" --limit 20

<extruct_api_cli> companies search --query "enterprise sales AI" \
  --filters '{"include":{"country":["United States"]},"range":{"founded":{"min":2018}}}' \
  --offset 20 --limit 20
```

Use `--filters` when the user specifies geography, city, company size, or founded range. Pass a JSON object like one of these as the `--filters` value.

```json
{
  "include": {
    "country": ["United States"],
    "size": ["51-200", "201-500"]
  }
}
```

```json
{
  "range": {
    "founded": {
      "min": 2018,
      "max": 2024
    }
  }
}
```

If search filters or pagination behavior appear different from the guidance here, verify current request and response details in the official API reference before guessing.

### Lookalike Search

Use lookalike search when the user already has a reference company and wants similar companies. Prefer domains or URLs for `--company-identifier` unless a prior Extruct response already gives you a UUID.

Typical asks:

- "find companies similar to Stripe in Extruct"
- "lookalike search from ramp.com"

Commands:

```bash
<extruct_api_cli> companies similar --company-identifier extruct.ai --limit 20

<extruct_api_cli> companies similar --company-identifier stripe.com \
  --filters '{"include":{"country":["United Kingdom"]}}'
```

Pagination uses the same `--offset` and `--limit` behavior as semantic search.

If identifier handling is unclear for a specific seed company or the live API behavior differs, verify the current lookalike-search request contract in the official API reference.

### Deep Search

Use Deep Search when the user wants a higher-precision asynchronous company search, wants explicit criteria, or is comfortable waiting for a task.

Typical asks:

- "run Deep Search for B2B revenue intelligence vendors"
- "find high-conviction AI procurement startups and show me the first result"

Create a task:

```bash
<extruct_api_cli> deep-search create --payload '{"query":"AI procurement startups serving enterprise finance teams","desired_num_results":25}'
```

Create a task with explicit criteria:

```bash
<extruct_api_cli> deep-search create --payload-file criteria.json
```

`criteria.json`:

```json
{
  "query": "vertical SaaS companies serving freight forwarding",
  "desired_num_results": 25,
  "criteria": [
    {
      "key": "has_logistics_focus",
      "name": "Logistics Focus",
      "criterion": "Company serves freight forwarding or logistics operations."
    },
    {
      "key": "b2b_fit",
      "name": "B2B Fit",
      "criterion": "Company sells primarily to business buyers."
    }
  ]
}
```

Inspect, poll, read results, or request more:

```bash
<extruct_api_cli> deep-search list --limit 20
<extruct_api_cli> deep-search get <task_id>
<extruct_api_cli> deep-search poll <task_id>
<extruct_api_cli> deep-search results <task_id> --limit 20 --offset 0
<extruct_api_cli> deep-search resume <task_id> --payload '{"desired_new_results":25}'
```

Deep Search notes:

- `deep-search results` can be read while the task is still running
- `deep-search poll` completes when `status == "done"` or `is_exhausted == true`
- if the user wants follow-on enrichment, move shortlisted domains into a company table
- if the payload spans more than a few lines or includes `criteria`, prefer `--payload-file` over inline `--payload`

If Deep Search payload fields, task states, or resume behavior are unclear, verify them against the official API reference before constructing raw fallback requests.

Read `references/finding-companies.md` when the task is a fuller company-discovery workflow instead of a single search command.

## Operate Existing Tables

Use these commands when the user already has a table and wants to inspect it, change rows or columns, run new work, or read results.

Typical asks:

- "add a funding column to this Extruct table"
- "poll this Extruct table until it finishes"
- "show me the first 20 rows from this table"
- "rerun only the new columns on this table"

If table payload shape, row schema, or run behavior is unclear, check the official API reference before mutating live tables:

- https://www.extruct.ai/docs/api-reference/introduction

### Create A Table

Use this when the user needs a new table before doing anything else.

```bash
<extruct_api_cli> tables create --payload '{
  "name":"Target Accounts",
  "kind":"company"
}'
```

### Inspect Before Mutating

If the user supplied a table URL, extract the table id first and use that id for all CLI commands below.

```bash
<extruct_api_cli> tables list --limit 20
<extruct_api_cli> tables get <table_id>
<extruct_api_cli> columns list <table_id>
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0 --columns company_name,company_website
<extruct_api_cli> rows get <table_id> <row_id>
```

### Update, Clone, Or Delete A Table

Update metadata:

```bash
<extruct_api_cli> tables update <table_id> --payload '{
  "name":"Target Accounts - Updated",
  "description":"High-priority accounts for enrichment"
}'
```

Clone or delete:

```bash
<extruct_api_cli> tables clone <table_id> --schema-only
<extruct_api_cli> tables delete <table_id> --yes
```

`--schema-only` clones the columns and structure without copying row data.
Without `--schema-only`, clone copies both schema and rows.

### Add, Update, Or Delete Rows

Use company domains or URLs as the safest `input` on company tables.
Default to `"run": false` while iterating so you can inspect rows and columns before spending more work. Only switch to `"run": true` when the user explicitly wants add-and-run in one step.
Before deleting, inspect either the specific row with `rows get` or a small `tables data` page so you only remove the intended records.

Create rows:

```bash
<extruct_api_cli> rows create <table_id> --payload '{
  "rows":[
    {"data":{"input":"extruct.ai"}},
    {"data":{"input":"stripe.com"}}
  ],
  "run":false
}'
```

Update rows:

```bash
<extruct_api_cli> rows update <table_id> --payload '{
  "rows":[
    {
      "id":"<row_id>",
      "data":{"input":"https://extruct.ai"}
    }
  ],
  "run":false
}'
```

Delete rows:

```bash
<extruct_api_cli> rows delete <table_id> --yes --payload '{
  "rows":[
    "<row_id_1>",
    "<row_id_2>"
  ]
}'
```

Row-deletion notes:

- deletion is bulk and row-ID based
- `rows delete` requires `--yes`
- a successful response returns the deleted row IDs

### Add, Update, Or Delete Columns

Read `references/column-guide.md` before designing or changing columns. Prefer built-in column kinds before custom prompts.

If a column kind, payload field, or validation rule in this skill looks stale, verify the current table and column contract in the official API reference before retrying.

Add a simple research column:

```bash
<extruct_api_cli> columns add <table_id> --payload '{
  "column_configs":[
    {
      "kind":"agent",
      "name":"Latest Funding",
      "key":"latest_funding",
      "value":{
        "agent_type":"research_pro",
        "prompt":"What is the latest funding round for the company? Return round type, amount, date, and lead investors when available.",
        "output_format":"text"
      }
    }
  ]
}'
```

Update a column:

```bash
<extruct_api_cli> columns update <table_id> <column_id> --payload '{
  "kind":"agent",
  "name":"Latest Funding",
  "key":"latest_funding",
  "value":{
    "agent_type":"research_pro",
    "prompt":"What is the latest funding round for the company? Return round type, amount, date, and lead investors when available.",
    "output_format":"text"
  }
}'
```

Delete a column:

```bash
<extruct_api_cli> columns delete <table_id> <column_id> --yes
```

### Run And Poll

Default incremental run:

```bash
<extruct_api_cli> tables run <table_id>

<extruct_api_cli> tables run <table_id> --payload '{
  "mode":"new",
  "columns":["<column_id_1>","<column_id_2>"]
}'
```

Poll and then read a small result page:

```bash
<extruct_api_cli> tables poll <table_id>
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0 --columns company_name,latest_funding
```

Table-operation defaults:

- prefer `mode: "new"` when iterating on an existing table
- bare `tables run <table_id>` is shorthand for `{"mode":"new"}`
- supported run modes are `new`, `all`, and `failed`
- pass explicit column ids when the user only wants new work
- inspect a small result page before scaling out, and use `--columns` whenever you only need a surgical slice of the data
- do not rerun the whole table unless the user explicitly wants that

### Choose The Right Table Kind

When creating a table, choose the kind from the entity the rows represent:

- `company`: use when rows are companies and the user wants company research, enrichment, scoring, or company-to-people branching
- `people`: use when rows are people or contacts and the user wants email, phone, LinkedIn, or derived people fields
- `generic`: use only when rows are neither companies nor people

For `generic` tables:

- the CLI fully supports create, update, run, and read operations
- this skill gives less prescriptive guidance because there are no company/people built-ins to lean on
- use `references/column-guide.md` more directly and design prompts, dependencies, and output formats explicitly

## Research Companies With Tables

Use company tables when the user wants custom enrichment over a set of companies or wants to run repeatable company research workflows.

Company table notes:

- `company` tables automatically include `input`, `company_profile`, `company_name`, and `company_website`
- use domains or URLs as row inputs whenever possible
- built-in company columns usually remove the need to create basic identity fields yourself

If the user needs a fresh company table, create one:

```bash
<extruct_api_cli> tables create --payload '{
  "name":"Target Accounts",
  "kind":"company"
}'
```

Then use the existing-table commands above to:

1. add company rows
2. add custom research columns from `references/column-guide.md`
3. run only the new column ids with `mode: "new"`
4. poll and inspect a small results page

Read `references/researching-companies.md` when the task is a full company-research workflow instead of a single table operation.

## Find People At Companies

Use this path when the user starts from companies and wants decision-makers, leadership, or contactable people.

If child-table behavior, finder output shape, or workflow handoff details differ from what this skill expects, verify the current API behavior in the official API reference.

Start from a `company` table, then add a `company_people_finder` column:

```bash
<extruct_api_cli> columns add <company_table_id> --payload '{
  "column_configs":[
    {
      "kind":"company_people_finder",
      "name":"Decision Makers",
      "key":"decision_makers",
      "value":{
        "roles":["VP Sales","sales leadership","revenue operations"]
      }
    }
  ]
}'
```

Run only the new finder column and poll:

```bash
<extruct_api_cli> tables run <company_table_id> --payload '{
  "mode":"new",
  "columns":["<people_finder_column_id>"]
}'
<extruct_api_cli> tables poll <company_table_id>
```

Then inspect the parent table to find the generated child `people` table in `child_relationships`, and continue there:

```bash
<extruct_api_cli> tables get <company_table_id>
```

The parent company table will also show the people-finder cell result, but the child `people` table is the place to continue downstream enrichment.

Use broader role families for coverage, such as `sales leadership`, and exact titles for narrower targeting, such as `VP Sales`. Read `references/finding-people-at-companies.md` when the task is a full company-to-people workflow.

## Research People

Use this path when the user already has people rows or already has a generated child `people` table and now wants enrichment, contact data, or derived fields.

Typical asks:

- "find work emails for these people"
- "add phone numbers to this people table"
- "classify these contacts by department and seniority"

People-table notes:

- `people` tables automatically include `input`, `full_name`, `role`, and `profile_url`
- full name, current role, and LinkedIn URL is the safest `input`
- include current role when available
- for `email_finder` or `phone_finder`, `company_website` must exist under the exact key `company_website`
- on `people` tables, custom `agent` columns can use `llm`, `research_reasoning`, and `linkedin`; `research_pro` is not allowed

If people-table capabilities, supported column kinds, or enrichment requirements appear to have changed, verify them in the official API reference before proceeding.

Create a standalone people table with local website context:

```bash
<extruct_api_cli> tables create --payload '{
  "name":"Target Contacts",
  "kind":"people",
  "column_configs":[
    {
      "kind":"input",
      "name":"Company Website",
      "key":"company_website"
    }
  ]
}'
```

Add people rows:

```bash
<extruct_api_cli> rows create <people_table_id> --payload '{
  "rows":[
    {
      "data":{
        "input":"Jane Doe, VP Sales, https://linkedin.com/in/jane-doe",
        "company_website":"extruct.ai"
      }
    }
  ],
  "run":false
}'
```

Add contact or derived columns:

```bash
<extruct_api_cli> columns add <people_table_id> --payload '{
  "column_configs":[
    {
      "kind":"email_finder",
      "name":"Work Email",
      "key":"work_email"
    },
    {
      "kind":"phone_finder",
      "name":"Direct Phone",
      "key":"direct_phone"
    }
  ]
}'
```

Run, poll, and inspect:

```bash
<extruct_api_cli> tables run <people_table_id> --payload '{
  "mode":"new",
  "columns":["<column_id_1>","<column_id_2>"]
}'
<extruct_api_cli> tables poll <people_table_id>
<extruct_api_cli> tables data <people_table_id> --limit 20 --offset 0
```

Read `references/researching-people.md` when the task is a full people-research workflow.

## Troubleshooting And Recovery

### Auth Or Connectivity Fails

Run:

```bash
<extruct_api_cli> auth user
<extruct_api_cli> healthcheck
```

If `auth user` fails, the token or account context is wrong. If `healthcheck` fails too, treat it as connectivity or service health.

If the auth flow, expected status codes, or healthcheck contract has changed, defer to the official API reference.

### Search Results Are Too Broad

- add `--filters` for country, city, size, or founded range
- switch from semantic search to lookalike if a reference company exists
- switch from semantic search or lookalike to Deep Search if the user wants a tighter, higher-conviction shortlist

### Lookalike Results Feel Wrong

- use a domain or URL instead of a company name when possible
- confirm the seed company is the correct one before judging the output

### Column Creation Fails

Common causes:

- unresolved prompt references such as `{pricing_notes}` pointing at a missing key
- wrong table kind for the column kind
- invalid `json` columns without an `output_schema`

Check `references/column-guide.md` before retrying.

### Cells Never Start Or Stay Idle

Common causes:

- upstream dependency cells are not done yet
- the table is missing required context
- the run targeted the wrong columns

Checks:

- inspect the table header and current columns
- verify the same rows have `done` cells in any upstream dependency columns
- keep dependency chains short
- rerun only the intended new columns with `mode: "new"`

### Email Or Phone Enrichment Fails On People Tables

Check that:

- the row has strong person context in `input`
- `company_website` exists under the exact key `company_website`
- the row belongs to the intended company

### Results Are Hard To Use Downstream

- split multi-job prompts into separate columns
- use `select`, `multiselect`, `numeric`, `money`, `date`, `grade`, or `json` instead of defaulting to `text`
- use the simplest format that captures the business value; do not pack Extruct explanation or source metadata into `json` unless the user explicitly wants those fields as table data
- derive downstream classifications with `llm` after researching the source fact once

### Retry Behavior

- if the CLI returns `429`, treat it as billing or quota rejection, not a tight-loop retry signal
- if the CLI returns a `5xx`, wait 5-10 seconds and retry once

## Global Flags

- `--pretty` for human-readable JSON
- `--timeout <seconds>` to override request timeout
- `--base-url <url>` to override the API base URL
- these flags can be placed before the resource, after the resource, or after the final action; for example: `<extruct_api_cli> tables list --limit 20 --pretty`

## References

- `references/column-guide.md`: column design rules plus a comprehensive library of good column configs
- `references/finding-companies.md`: choose and operate semantic search, lookalike, and Deep Search
- `references/researching-companies.md`: build or extend company research tables safely
- `references/finding-people-at-companies.md`: branch from company tables into people workflows
- `references/researching-people.md`: enrich standalone or generated people tables
- official Extruct API reference: https://www.extruct.ai/docs/api-reference/introduction
