---
name: notion
description: >-
  Operate Notion from a terminal or agent: retrieve pages, query databases,
  search pages and databases, and update page properties — with a bundled
  notion-cli script that is read-only by default and gates every create or
  update behind a --dry-run/--yes confirmation. Use when an agent needs to
  read Notion content, answer questions from a team wiki or database, or make
  a confirmed edit. Do not use for building Notion integrations or
  block-level page composition beyond property updates (that is Notion API
  application development), or for other knowledge bases (that is their own
  tooling).
license: MIT
compatibility: >-
  The bundled notion-cli script runs on Python 3.9+ with only the standard
  library. --help and page/database/search reads need no network; live reads
  require a Notion integration token (secret_...) with the right workspace
  capabilities and network access to api.notion.com.
metadata:
  source: https://developers.notion.com/reference
  source_index: references/00-source-index.md
  research_checked: "2026-08-03"
---

# Notion Operations

Use this skill to read and, with explicit confirmation, write Notion content through the Notion API: pages, database queries, search, and page property updates. This is a **tool skill** for the Notion platform. Building Notion integrations, writing complex block compositions, or building an app on the Notion API is application development; this skill owns the everyday agent workflow: finding the right page, answering from a database, and making a confirmed edit.

## Operating contract

1. **Read-only discovery before any mutation.** Retrieve pages, query databases, and search freely. The bundled `notion-cli` script makes reads without writing anything.
2. **Confirm the target, scope, and rollback path before acting.** Creating a page or updating properties changes a shared workspace that teammates read. Both require an explicit human directive plus `--dry-run` preview and `--yes` confirmation through `notion-cli`. Property updates overwrite existing values — state the current value and the replacement before confirming.
3. **Respect bounded reads.** Notion paginates with `page_size` and `has_more`; never page past what the task needs. `notion-cli --limit` caps every search and query.
4. **Keep evidence bounded.** Quote short page titles, property values, and IDs; never paste full pages, tokens, or raw API payloads into chat.
5. **Know the API version.** The `Notion-Version` header pins the API contract; reads that work today can change with a version bump. `notion-cli` sends `2022-06-28` by default and honors `NOTION_VERSION`.

## The notion-cli script

`scripts/notion-cli` is an agent-first, stdlib-only CLI over the Notion API. It covers the full issue scope: pages, databases (query), search, and updates.

```bash
notion/scripts/notion-cli --help                           # no token or network needed
notion/scripts/notion-cli --json pages get --page-id <page>
notion/scripts/notion-cli --json --limit 10 databases query --database-id <db>
notion/scripts/notion-cli --json search query --query "on-call runbook"
notion/scripts/notion-cli pages update --page-id <page> --properties props.json --dry-run
notion/scripts/notion-cli pages update --page-id <page> --properties props.json --yes
notion/scripts/notion-cli pages create --parent-database <db> --title "New row" --yes
```

Exit codes: 0 success, 1 API error or failed check, 2 usage error. Creates and updates are guarded: without `--dry-run` or `--yes` the script refuses with exit 1 and never calls the API. Reads are bounded by `--limit` (default 20, max 100).

## Operating loop

1. **Locate the content**: `search query` to find pages and databases by text, or a known ID directly.
2. **Read with bounds**: `pages get` for a single page, `databases query` for rows in a database (optionally with a JSON `--filter`), always capped by `--limit`.
3. **Triage the answer**: map the question to evidence (page title + properties, database rows, search results with `has_more` state).
4. **Act with confirmation**: only a human directive to change, previewed with `--dry-run` and confirmed with `--yes`.
5. **Verify**: re-read the page (`pages get`) and confirm the property values landed.

## Pages, databases, search

- **Pages** (`GET /pages/{id}`): a page is an ID, a title (extracted from the `title` or `Name` property), a URL, and timestamps. Property values live under `properties`; the CLI summarizes them rather than dumping the full block tree.
- **Databases** (`POST /databases/{id}/query`): query rows as pages with a `page_size` cap and an optional structured `--filter` JSON file (e.g. `{"property": "Status", "select": {"equals": "Done"}}`). `has_more` tells you whether the cap hid further rows.
- **Search** (`POST /search`): finds pages and databases by text across the integration's accessible workspace; results are bounded by `--limit`.
- **Updates** (`PATCH /pages/{id}`): property updates overwrite values (select, status, checkbox, rich text, etc.). Preview the exact properties payload with `--dry-run` and confirm with `--yes`; verify with a follow-up `pages get`.

## Integration access model

- Notion integrations authenticate with a bot-style token (`secret_...`) and can only see the pages and databases explicitly **shared with the integration**. A page that exists in the workspace but is not shared returns 404/`object_not_found` — that is an access-model result, not a missing page.
- The `Notion-Version` header selects the API contract. The CLI defaults to `2022-06-28`; set `NOTION_VERSION` when a workspace or application pins a different version.
- Tokens are workspace-scoped credentials. Store them in the environment (`NOTION_TOKEN`), never in code, chat, or commits. Revoke a leaked integration token in the Notion integration settings.

## Reference routing

| Load when | Reference |
|---|---|
| Sources, version notes, refresh procedure | `references/00-source-index.md` |
| API endpoints, pagination, property types, filters, and error handling | `references/01-api-operations.md` |

## Included artifacts

- `scripts/notion-cli`: bounded, stdlib-only CLI (pages get/create/update, databases query, search; `--json`; `--limit`; mutations gated by `--dry-run`/`--yes`).
- `tests/test_notion_cli.py`: 13 deterministic tests against a stub Notion API, including the mutation gate and the read-only contract.
- `references/`: dated source index + API operations reference.
- `evals/evals.json`: six output-quality evaluation cases for agent runs.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| A page exists and its title | `notion-cli pages get --page-id ... --json` returns the title and ID |
| A database query answered the question | `notion-cli databases query --json` returns bounded rows with `has_more` state |
| Search found the content | `notion-cli search query --json` returns the matching page/database with ID and title |
| An update landed | `notion-cli pages update --yes` exits 0 and a follow-up `pages get` shows the new property values |
| A mutation is safe to run | `notion-cli ... --dry-run` prints the exact payload that would be sent |

## Hard boundaries

- Never create or update a page without a human directive, `--dry-run` preview, and `--yes` confirmation — Notion edits are visible to everyone with access to the page.
- Never claim a page is missing when it may simply not be shared with the integration; verify the access model first.
- Never page reads past `--limit`; never dump full pages, tokens, or raw payloads into chat.
- This skill operates the Notion API. It does not build Notion integrations (application development) or cover other knowledge-base products.

## When not to use

- **Building Notion integrations or apps** (OAuth flows, custom blocks, public API products, block-tree composition beyond property updates) — that is application development; see [backend-engineering](../backend-engineering/SKILL.md) for service design.
- **Other knowledge bases and document tools** (Confluence, Google Docs, wikis) — each has its own tooling; this skill covers Notion only.
- **Workspace administration** (user management, workspace settings, integration approval) — that is the Notion admin console.
