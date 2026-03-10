---
name: agent-notion
description: |
  Notion CLI for humans and LLMs. Use when:
  - Searching Notion pages or databases by title
  - Querying database rows with filters and sorts
  - Reading page properties and content (as markdown or structured blocks)
  - Creating, updating, or archiving pages
  - Reading, appending, updating, deleting, or replacing block content
  - Listing or adding comments on pages (page-level or inline on specific text)
  - Exporting pages or entire workspaces as markdown/HTML
  - Finding backlinks (pages that link to a given page)
  - Viewing version history snapshots of a page
  - Checking recent workspace or page activity
  - Chatting with Notion AI (send messages, list threads, stream responses)
  - Listing available Notion AI models
  - Managing Notion OAuth, integration token, or desktop session auth
  Triggers: "notion page", "notion database", "notion search", "query notion", "notion block", "notion comment", "notion auth", "notion content", "search notion", "create notion page", "notion workspace", "notion export", "notion backlinks", "notion history", "notion activity", "inline comment", "version history", "page activity", "notion ai", "ai chat", "notion chat", "ai model"
---

# Notion automation with `agent-notion`

`agent-notion` is a CLI binary installed on `$PATH`. Invoke it directly (e.g. `agent-notion search "Project Plan"`).

All output is JSON to stdout. Errors go to stderr as `{ "error": "..." }` with non-zero exit.

## Quick start (auth)

**Option A: OAuth (recommended for full access)**

```bash
agent-notion auth setup-oauth --client-id <id> --client-secret <secret>
agent-notion auth login                        # opens browser for OAuth flow
agent-notion auth status
```

**Option B: Internal integration token**

```bash
agent-notion auth login --token ntn_...
agent-notion auth status
```

**Option C: Desktop session (for v3 features)**

```bash
agent-notion auth import-desktop                   # macOS only — reads token from Notion Desktop app
```

Required for v3 commands: export, page backlinks, page history, activity log, inline comments, AI chat/models.

Multiple workspaces are supported:

```bash
agent-notion auth login --alias work
agent-notion auth workspace list
agent-notion auth workspace switch <alias>
agent-notion auth logout [--all]
agent-notion auth workspace remove <alias>
```

## Searching

**Important: Notion search is title-only.** It does not search page content, comments, or property values.

```bash
agent-notion search query "meeting notes"
agent-notion search query "Q1 Plan" --filter database
agent-notion search query "design doc" --filter page --limit 5
```

## Databases

```bash
agent-notion database list                                          # uses search API
agent-notion database get <database-id>                             # full metadata + property definitions
agent-notion database schema <database-id>                          # compact schema for LLMs (types, options)
agent-notion database query <database-id>                           # all rows
agent-notion database query <id> --filter '{"property":"Status","select":{"equals":"Done"}}'
agent-notion database query <id> --sort '[{"property":"Name","direction":"ascending"}]'
```

Use `database schema` to discover property names, types, and valid select/status options before building filters.

## Pages

```bash
agent-notion page get <page-id>                                     # properties only
agent-notion page get <page-id> --content                           # properties + markdown content
agent-notion page get <page-id> --raw-content                       # properties + structured block objects
agent-notion page create --parent <id> --title "New Page"           # auto-detects database vs page parent
agent-notion page create --parent <db-id> --title "Task" --properties '{"Status":"In Progress","Priority":"High"}'
agent-notion page create --parent <id> --title "Notes" --icon "📝"
agent-notion page update <page-id> --title "Updated Title"
agent-notion page update <page-id> --properties '{"Status":"Done"}' --icon "✅"
agent-notion page archive <page-id>
```

Property values in `--properties` are auto-converted: strings become select values, numbers become number properties, booleans become checkboxes, arrays become multi-select. Pass Notion API format for complex types.

## Blocks (page content)

```bash
agent-notion block list <page-id>                                   # markdown (default)
agent-notion block list <page-id> --raw                             # structured block objects with IDs
agent-notion block append <page-id> --content "## New Section\n\nParagraph text"
agent-notion block append <page-id> --blocks '[{"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"Hello"}}]}}]'
agent-notion block update <block-id> --content "New text"           # edit a single block's content
agent-notion block delete <block-id>                                # remove a block
agent-notion block move <block-id> --after <other-block-id>               # reorder (v3)
agent-notion block move <block-id> --parent <callout-id>                 # move into container (v3)
agent-notion block replace <page-id> --content "# Fresh\n\nAll new content"  # replace all page content
```

Markdown conversion supports: headings, lists, todos, code fences, blockquotes, dividers, and paragraphs.

Use `block list --raw` to get block IDs for `update` and `delete`. Use `block replace` to swap all content at once.

## Comments

```bash
agent-notion comment list <page-id>
agent-notion comment page <page-id> "This looks good!"
agent-notion comment inline <block-id> "Great point!" --text "target phrase"           # v3
agent-notion comment inline <block-id> "Second one" --text "the" --occurrence 2        # v3
```

Inline comments are anchored to specific text within a block and require a v3 desktop session.

## v3 Features (requires `auth import-desktop`)

These commands use Notion's internal API and require a desktop session token.

### Export

```bash
agent-notion export page <page-id>                             # export as markdown zip
agent-notion export page <page-id> --format html --recursive   # export page tree as HTML
agent-notion export workspace                                  # export entire workspace
agent-notion export workspace --output my-backup.zip           # custom output path
```

Options: `--format markdown|html`, `--recursive` (page only), `--output <path>`, `--timeout <seconds>`

### Backlinks

```bash
agent-notion page backlinks <page-id>                          # pages linking to this page
```

Returns `{ backlinks: [{ blockId, pageId, pageTitle }], total }`. Deduplicated by page.

### History

```bash
agent-notion page history <page-id>                            # recent version snapshots
agent-notion page history <page-id> --limit 50                 # fetch more
```

Returns `{ snapshots: [{ id, version, lastVersion, timestamp, authors }], total }`.

### Activity

```bash
agent-notion activity log                                      # workspace-wide activity
agent-notion activity log --page <page-id>                     # scoped to a page
agent-notion activity log --limit 50                           # fetch more entries
```

Returns `{ activities: [{ id, type, pageId, pageTitle, authors, editTypes, startTime, endTime }], total }`.

## Notion AI (requires `auth import-desktop`)

```bash
agent-notion ai model list                                         # available models (name, family, tier)
agent-notion ai model list --raw                                   # full model objects with codenames
agent-notion ai chat list [--limit 10]                             # recent chat threads
agent-notion ai chat send "Summarize my recent projects"           # new conversation
agent-notion ai chat send "Tell me more" --thread <id>             # continue thread
agent-notion ai chat send "Explain this page" --page <page-id>    # with page context
agent-notion ai chat send "Quick question" --stream                # stream to stderr
agent-notion ai chat send "Hello" --model "GPT-5.2"               # specific model
agent-notion ai chat mark-read <thread-id>                         # mark thread as read
```

Model resolution: `--model` flag > `config ai.defaultModel` > API default. Accepts codenames or display names.

With `--stream`, AI response text streams to stderr incrementally. JSON result always goes to stdout.

## Users

```bash
agent-notion user list
agent-notion user me                                                # current authenticated user/bot
```

## Truncation

Long text fields (`description`, `body`, `content`) are truncated to ~200 characters by default. A companion `*Length` field (e.g. `descriptionLength`) always shows the full size.

To see full content, use `--expand` or `--full`:

```bash
agent-notion --full page get <page-id>                              # expand all fields
agent-notion --expand description database get <id>                 # expand specific field
agent-notion --expand description,content page get <id> --content   # expand multiple
```

These are global flags — place them before the command or after it.

## IDs

All commands accept Notion UUIDs (with or without dashes):

- `aaaaaaaa-1111-2222-3333-444444444444`
- `aaaaaaaa111122223333444444444444`

## Pagination

List commands return `{ "items": [...], "pagination"?: { "hasMore": true, "nextCursor": "..." } }`.

Use `--limit <n>` (max 100) and `--cursor <token>` to paginate.

## Per-command usage docs

Every command group has a `usage` subcommand with detailed, LLM-optimized docs:

```bash
agent-notion usage                # top-level overview (~1000 tokens)
agent-notion search usage         # search command details
agent-notion database usage       # database commands
agent-notion page usage           # page commands
agent-notion block usage          # block commands
agent-notion comment usage        # comment commands (page + inline)
agent-notion export usage         # export commands (v3)
agent-notion activity usage       # activity log (v3)
agent-notion ai usage             # AI chat and models (v3)
agent-notion user usage           # user commands
agent-notion auth usage           # auth + workspace management
agent-notion config usage         # CLI settings keys, defaults, validation
```

Use `agent-notion <command> usage` when you need deep detail on a specific domain before acting.

## Configuration

```bash
agent-notion config list-keys                                       # all keys with defaults
agent-notion config get [key]                                       # current value(s)
agent-notion config set truncation.maxLength 500                    # increase truncation limit
agent-notion config set pagination.defaultPageSize 20               # change default page size
agent-notion config set ai.defaultModel <codename>                  # default AI model
agent-notion config reset [key]                                     # restore defaults
```

## References

- [references/commands.md](references/commands.md): full command map + all flags
- [references/output.md](references/output.md): JSON output shapes + field details
