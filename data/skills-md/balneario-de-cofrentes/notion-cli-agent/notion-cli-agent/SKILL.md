---
name: notion-cli-agent
description: Use the local Notion CLI (notion-cli-agent) to query, create, update, and manage Notion pages and databases via shell. Use when interacting with Notion workspaces, querying databases, creating or updating pages, managing tasks, reading content blocks, or running bulk/batch operations on Notion data. Prefer over Notion MCP or API calls.
---

# notion-cli-agent

Local CLI for full Notion access.

## Binary

```bash
~/clawd/bin/notion <args>   # OpenClaw wrapper
# or: notion <args>          # if globally installed
```

Auth: `NOTION_TOKEN` env var, or `~/.config/notion/api_key`.

## Load workspace state first

If `~/.config/notion/workspace.json` exists, read it to get database IDs — no need to run `inspect` every time:

```bash
cat ~/.config/notion/workspace.json 2>/dev/null
# extract: .databases.tasks.id, .databases.projects.id, etc.
```

If the file is missing, suggest the user run the **notion-onboarding** skill first.

## Agent Workflow

1. **Load state** (above) or `notion inspect ws --compact` / `notion inspect ws --json` to discover databases
2. **Understand schema** — `notion inspect context <db_id>` and `notion inspect schema <db_id> --llm`
3. **Query** with `--json` or `--llm` only where the command supports it
4. **Write** with `--dry-run` first on bulk/batch ops, then confirm with user

## Core Commands

### Discover
```bash
notion inspect ws --compact                     # all databases, names + ids
notion inspect ws --json                        # full raw inventory
notion inspect schema <db_id> --llm             # property types + valid values
notion inspect context <db_id>                  # workflow context + examples
notion ai prompt <db_id>                        # DB-specific agent instructions
```

### Query
```bash
notion search "keyword" --limit 10
notion db query <db_id> --limit 20
notion db query <db_id> --limit 20 --json
notion find "overdue tasks unassigned" -d <db_id> --llm   # natural language
notion find "high priority" -d <db_id> --explain          # preview filter, don't run
```

### Read pages
```bash
notion page get <page_id>                       # properties
notion page get <page_id> --content             # + content blocks
notion page get <page_id> --json                # raw JSON
notion ai summarize <page_id>                   # concise summary
notion ai extract <page_id> --schema "email,phone,date"
```

### Write pages
```bash
notion page create --parent <db_id> --title "Task Name"
notion page create --parent <db_id> --title "Task" --prop "Status=Todo" --prop "Priority=High"
notion page update <page_id> --prop "Status=Done"
```

### Add blocks
```bash
notion block append <page_id> --text "Paragraph"
notion block append <page_id> --heading2 "Section" --bullet "Item 1" --bullet "Item 2"
notion block append <page_id> --todo "Action item"
```

### Batch (minimize tool calls)
```bash
notion batch --dry-run --data '[
  {"op":"get","type":"page","id":"<page_id>"},
  {"op":"create","type":"page","parent":"<db_id>","data":{"title":"New"}},
  {"op":"update","type":"page","id":"<page_id2>","data":{"Status":"Done"}}
]'
notion batch --llm --data '[...]'               # execute
```

### Bulk & maintenance
```bash
notion bulk update <db_id> --where "Status=Todo" --set "Status=In Progress" --dry-run
notion stats overview <db_id>
notion validate check <db_id> --check-dates --check-stale 30
```

## Output flags

| Flag | Use for |
|------|---------|
| `--llm` | Compact, structured output for agents on supported commands (`find`, `batch`, `inspect schema`) |
| `--json` / `-j` | Raw JSON for parsing |
| (default) | Human-readable |

## Property type filters

`--filter-prop-type` is required for non-text properties:

```bash
notion db query <db_id> \
  --filter-prop "Status" --filter-type equals \
  --filter-value "Done" --filter-prop-type status
```

Types: `status` · `select` · `multi_select` · `number` · `date` · `checkbox` · `people` · `relation`

See `references/filters.md` for full operator reference.

## Rules

- Property names and values are **case-sensitive** — always verify with `inspect context`
- Title property name varies per DB (`"Name"`, `"Título"`, `"Task"` — check state or schema)
- `--dry-run` before any bulk/batch write
- Confirm with user before destructive bulk operations

## References

- `references/filters.md` — all property types × filter operators with examples
- `references/batch-patterns.md` — batch workflows (multi-update, bulk status sweep, multi-get)
- `references/workflows.md` — agent workflow recipes (task triage, weekly review, project sync)

## Self-help

```bash
notion quickstart          # full quick reference
notion <command> --help    # per-command help
notion ai suggest <db_id> "what I want to do"
```
