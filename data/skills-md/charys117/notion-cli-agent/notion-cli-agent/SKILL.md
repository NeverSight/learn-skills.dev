---
name: notion-cli-agent
description: Operates Notion through the `notion` or `notion-cli-agent` CLI with agent-optimized commands for schema inspection, database querying, page editing, Markdown import/export, batch operations, validation, backup, and AI helper prompts. Use when the user wants to manage Notion from the terminal through this CLI instead of using the Notion API directly.
---

# Notion Automation with notion-cli-agent

## Quick start

```bash
# get the built-in guide first
notion quickstart

# discover workspace structure
notion inspect workspace
notion inspect schema <db_id> --llm
notion inspect context <db_id>

# query a database
notion db query <db_id> --limit 10
notion find "overdue tasks" -d <db_id>

# read and update a page
notion page get <page_id> --content
notion page update <page_id> --prop "Status=Done"

# write Markdown content
notion page read <page_id>
notion page write <page_id> --file ./notes.md
```

## Commands

### Discovery

```bash
notion quickstart
notion inspect workspace
notion inspect schema <db_id>
notion inspect schema <db_id> --llm
notion inspect context <db_id> --examples 3
notion search "project plan"
notion search "" --type database
```

### Querying

```bash
notion db query <db_id> --limit 20
notion db query <db_id> \
  --filter-prop "Status" \
  --filter-type equals \
  --filter-value "Done" \
  --filter-prop-type status
notion db query <db_id> --sort "Due Date" --sort-dir asc --limit 20
notion find "in progress unassigned" -d <db_id>
notion find "urgent pending" -d <db_id> --explain
```

### Pages

```bash
notion page get <page_id>
notion page get <page_id> --content
notion page create --parent <db_id> --title "New Task"
notion page create --parent <db_id> --title "Bug Fix" --prop "Status=Todo" --prop "Priority=High"
notion page update <page_id> --title "Renamed"
notion page update <page_id> --prop "Status=Done" --icon ✅
notion page archive <page_id>
```

### Content and blocks

```bash
notion page read <page_id>
notion page read <page_id> --output ./page.md
notion page write <page_id> --file ./notes.md
notion page write <page_id> --file ./replacement.md --replace
notion page edit <page_id> --at 3 --delete 2 --markdown "## New Section"

notion block list <page_id>
notion block append <page_id> --heading2 "Status" --bullet "Item 1" --bullet "Item 2"
notion block append <page_id> --todo "**Review** PR"
notion block update <block_id> --text "Updated text"
notion block delete <block_id>
```

### Comments

```bash
notion comment list <page_id>
notion comment create --page <page_id> --text "Follow up here."
notion comment create --discussion <discussion_id> --text "Reply in thread."
```

### AI helpers

```bash
notion ai prompt <db_id>
notion ai suggest <db_id> "show me completed work from this week"
notion ai summarize <page_id> --max-lines 30
notion ai summarize <page_id> --json
notion ai extract <page_id> --schema "email,phone,date"
```

### Batch and bulk

```bash
notion batch --dry-run --data '[
  {"op":"get","type":"page","id":"<page_id>"},
  {"op":"query","type":"database","id":"<db_id>","data":{"page_size":5}}
]'

notion batch --llm --data '[
  {"op":"create","type":"page","parent":"<db_id>","data":{"properties":{"Name":{"title":[{"text":{"content":"Task"}}]}}}},
  {"op":"update","type":"page","id":"<page_id>","data":{"properties":{"Status":{"status":{"name":"Done"}}}}}
]'

notion bulk update <db_id> --where "Status=Todo" --set "Status=In Progress" --dry-run
notion bulk update <db_id> --where "Status=Todo" --set "Status=In Progress" --yes
notion bulk archive <db_id> --where "Status=Done" --dry-run
```

### Validation, backup, import, export

```bash
notion validate check <db_id> --required "Status,Owner" --check-dates --check-stale 14 --fix
notion validate lint <db_id>
notion validate health <db_id>
notion stats overview <db_id>
notion backup <db_id> -o ./backups --format markdown --content
notion export db <db_id> --vault ~/vault --folder notion-export
notion import markdown ./doc.md --to <page_id>
notion import csv ./tasks.csv --to <db_id>
```

### Escape hatch

```bash
notion api GET pages/<page_id>
notion api POST databases/<db_id>/query --data '{"page_size":10}'
```

## Output modes

Use `--json` when another tool or agent step needs structured output.

Use `--llm` for commands that support LLM-friendly summaries such as `inspect schema`, `batch`, `find`, `stats`, and `relations`.

## Property rules

- Inspect schema before mutating unfamiliar databases.
- Property names and option values are exact and case-sensitive.
- Title property names vary by database. `page create` and `page update` try to auto-detect them.
- `--prop` infers types from values:
  - `true` or `false` -> checkbox
  - `42` -> number
  - `2026-03-10` -> date
  - `https://...` -> url
  - `a@b.com` -> email
  - `bug,urgent` -> multi_select
  - plain strings -> select
- For `db query`, pass `--filter-prop-type` for non-text fields when precision matters.

## Safety notes

- Run `--dry-run` before `batch`, `bulk update`, `bulk archive`, and any broad mutation.
- Treat `page write --replace` as destructive and non-atomic because existing blocks are deleted before new blocks are appended.
- Prefer `page read` or `block list` before surgical edits.
- `page write` already chunks appends into 100-block requests to match the Notion API limit.

## Local usage

If the global `notion` binary is unavailable, run the built CLI from this repository:

```bash
pnpm build
node dist/cli.js quickstart
node dist/cli.js inspect workspace
node dist/cli.js page get <page_id>
```

## Example: schema-first workflow

```bash
notion inspect context <db_id>
notion find "overdue tasks" -d <db_id>
notion bulk update <db_id> --where "Status=Todo" --set "Status=In Progress" --dry-run
```

## Example: Markdown round-trip

```bash
notion page read <page_id> --output ./page.md
# edit ./page.md locally
notion page write <page_id> --file ./page.md --replace
```

## Specific tasks

* **Database discovery and querying** [references/database-workflows.md](references/database-workflows.md)
* **Markdown editing and block operations** [references/content-workflows.md](references/content-workflows.md)
* **Validation, backup, import, and export** [references/maintenance-workflows.md](references/maintenance-workflows.md)
