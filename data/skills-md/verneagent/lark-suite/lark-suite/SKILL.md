---
name: lark-suite
description: Read, create, and edit Lark wiki pages, documents, and project-tracking surfaces via the Open API.
allowed-tools: Bash, Read, Write, Glob, Grep
---

Read, create, and edit Lark wiki pages and documents using the Lark Open API.

## Prerequisites

- Config file: `~/.lark-suite/config.json` with `app_id` and `app_secret`
  - The skill still falls back to `~/.lark-wiki/config.json` if the old path exists and the new one does not
  - If the file doesn't exist, run the `init` command to create it interactively (see below)
- Required Lark app scopes: `wiki:wiki`, `docx:document` (for write operations)
- The bot must have edit permission on the target wiki space
- For browser-based commands (`comment`): set `LARK_BASE` env var to your organization's domain (e.g. `https://yourcompany.larksuite.com`)

## CLI Helper

All operations are available via the helper script:

```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py <command> [args]
```

**Important:** All commands require network access, so use `dangerouslyDisableSandbox: true` for Bash calls.

## Commands

### Initialize credentials (first-time setup)
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py init
```
Interactive prompt to create or update `~/.lark-suite/config.json`. Run this when credentials are missing or need updating. Shows existing values (masked for secrets) and lets you keep or replace them.

### Read a wiki page
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py read <node_token>
```
Extract `node_token` from wiki URLs: `https://...larksuite.com/wiki/<node_token>`

Returns the plain text content of the page.

### List child nodes
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py list <node_token>
```
Returns JSON array of child nodes with `node_token`, `title`, `obj_type`, `has_child`.

### Tree view (recursive)
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py tree <node_token> [--depth N]
```
Prints an indented tree of all descendant nodes. Default depth: 3.

### Create a wiki page
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py create <parent_node_token> "<title>"
```
Creates a new empty docx page under the given parent. Returns the new node's tokens.

### Read document blocks (structured)
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py blocks <document_id>
```
Returns the full block tree as JSON. Use `obj_token` (not `node_token`) as the document ID.

### Write blocks to a document
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py write <document_id> '<blocks_json>' [--index N]
```
Write blocks to a document. Accepts a JSON string or file path. Index -1 = append (default).

### Add a comment
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py comment <document_id> "<text>"
```
Adds a **global (whole-document) comment**. The Lark Open API only supports global comments for docx files — inline comments anchored to specific text selections require browser automation (see below).

## Browser-Based Commands (Playwright)

For operations the Lark API doesn't support (like inline comments), a separate Playwright-based script is available. Requires a one-time manual login.

**Prerequisites:**
- `pip3 install playwright && python3 -m playwright install chromium`
- Run `login` once to authenticate: browser opens, you log in manually, session is saved to `~/.playwright-lark-session`

### Login (one-time setup)
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite_browser.py login
```
Opens a headed browser to the Lark login page. Log in manually, then Ctrl+C. Session persists across runs.

### Add inline comment
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite_browser.py inline-comment <node_token_or_url> --search '<text_to_select>' --comment '<comment_text>'
```
Selects the specified text in the document and adds an inline comment anchored to it. Runs in **headed mode** by default (Lark's toolbar doesn't render in headless). Add `--headless` to attempt headless mode (less reliable).

### Extract highlighted text
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite_browser.py highlights <node_token_or_obj_token>
```
Uses the API (no browser needed) to find all text with `background_color` set. Returns JSON with text, color code, and color name.

### Screenshot a document
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite_browser.py screenshot <node_token_or_url> [-o output.png] [--full-page]
```
Takes a screenshot of a Lark document (headless). Useful for visual inspection.

## Contact Commands

### Look up user IDs by email
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py contact-lookup user@example.com [user2@example.com ...]
```
Returns open_id for each email. Useful for permission management (`perm-add` needs open_id).

## Permission Commands

### Add a collaborator
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py perm-add <token> <member_open_id> [--file-type docx] [--perm edit]
```
- `token`: Document/file obj_token
- `member_open_id`: User's open_id (from `contact-lookup`)
- `--file-type`: `docx`, `sheet`, `bitable`, `doc`, `slide` (default: `docx`)
- `--perm`: `view`, `edit`, `full_access` (default: `edit`)

### List collaborators
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py perm-list <token> [--file-type docx]
```

## Document Search

### Search documents globally
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py doc-search "<query>" [--count 20] [--doc-types docx,sheet,bitable]
```
- `--doc-types`: Comma-separated filter — `doc`, `docx`, `sheet`, `bitable`, `slide`, `wiki`
- Returns: title, token, type, URL, owner

## Block Type Reference

### Creatable via API

| Type | Key | Example |
|------|-----|---------|
| 2 | `text` | `{"block_type": 2, "text": {"elements": [{"text_run": {"content": "Hello", "text_element_style": {}}}], "style": {}}}` |
| 3-11 | `heading1`-`heading9` | Same structure as text, with `headingN` key |
| 12 | `bullet` | Unordered list item. **Requires** `"style": {"align": 1, "folded": false}` |
| 13 | `ordered` | Ordered list item. Same style requirement as bullet |
| 14 | `code` | Code block. `"style": {"language": 12}` (12=JS, 1=Python, etc.) |
| 15 | `quote` | Quote block |
| 17 | `todo` | Checkbox. `"style": {"done": false, "align": 1, "folded": false}` |
| 19 | `callout` | `{"block_type": 19, "callout": {"emoji_id": "thumbsup", "background_color": 2}}` |
| 22 | `divider` | `{"block_type": 22, "divider": {}}` |
| 24 | `grid` | Column layout. `{"block_type": 24, "grid": {"column_size": 2}}` |
| 26 | `iframe` | Embed. `{"block_type": 26, "iframe": {"component": {"iframe_type": 1, "url": "..."}}}` |
| 31 | `table` | `{"block_type": 31, "table": {"cells": ["H1","H2","R1C1","R1C2"], "property": {"column_size": 2, "row_size": 2}}}` |
| 34 | `quote_container` | Quote wrapper container |

### NOT Creatable via API

| Type | Block | Notes |
|------|-------|-------|
| 16 | Equation | Explicitly excluded from create API |
| 21 | Diagram / Flowchart / Mind Map / UML | "block not support to create" |
| 27 | Image | Requires separate upload flow, then reference token |
| 23 | File | Requires separate upload flow |
| 41 | Synced Block | "block not support to create" |
| 999 | Sub-doc | "block not support to create" |

### Board blocks (type 43)

Board blocks (whiteboard/画板) **CAN** be created via the docx API:
```json
{"block_type": 43, "board": {}}
```
The response includes a `board.token` for use with the Board API (`board/v1`). This is distinct from type 21 (diagram blocks) which cannot be created.

### Rich Text Elements

Text elements within blocks support these styles in `text_element_style`:
- `bold`: boolean
- `italic`: boolean
- `underline`: boolean
- `strikethrough`: boolean
- `inline_code`: boolean
- `background_color`: int (only present when set) — text highlight color. Values: 1=light grey, 2=light purple, 3=yellow, 4=light green, 5=pink, etc.
- `comment_ids`: string[] (only present when set) — IDs of inline comments anchored to this text. Read-only.

Example with mixed formatting:
```json
{
  "elements": [
    {"text_run": {"content": "Normal ", "text_element_style": {}}},
    {"text_run": {"content": "bold", "text_element_style": {"bold": true}}},
    {"text_run": {"content": " and ", "text_element_style": {}}},
    {"text_run": {"content": "italic", "text_element_style": {"italic": true}}}
  ]
}
```

## URL → Token Extraction

Wiki URL format: `https://{domain}.larksuite.com/wiki/{node_token}`

The `node_token` is the path segment after `/wiki/`. To get the `document_id` (obj_token) needed for block operations, use the `read` or `list` command which resolves it automatically, or call:
```bash
# Manual resolution
python3 -c "
import sys; sys.path.insert(0, '.claude/skills/lark-suite/scripts')
from lark_auth import LarkAuth
import json, urllib.request
t = LarkAuth('~/.lark-suite/config.json').get_token()
r = urllib.request.urlopen(urllib.request.Request(
    'https://open.larksuite.com/open-apis/wiki/v2/spaces/get_node?token=NODE_TOKEN',
    headers={'Authorization': f'Bearer {t}'}))
print(json.loads(r.read())['data']['node']['obj_token'])
"
```

## Bitable (Base) Commands

### List tables
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py base-tables <app_token>
```

### List fields in a table
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py base-fields <app_token> <table_id>
```

### List/search records
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py base-records <app_token> <table_id> [--filter '<json>']
```
Filter format (Lark filter syntax):
```json
{"conjunction": "and", "conditions": [{"field_name": "Status", "operator": "is", "value": ["Done"]}]}
```

### Add a record
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py base-add <app_token> <table_id> '{"Feature": "New item", "Status": "Backlog"}'
```

### Update a record
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py base-update <app_token> <table_id> <record_id> '{"Status": "Done"}'
```

### Create a table
```bash
python3 .claude/skills/lark-suite/scripts/lark_suite.py base-create-table <app_token> '<table_json>'
```
Table JSON example:
```json
{"name": "Tasks", "default_view_name": "All", "fields": [
  {"field_name": "Title", "type": 1},
  {"field_name": "Status", "type": 3, "property": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
  {"field_name": "Priority", "type": 2}
]}
```

### Bitable Field Types

| Type | Name | Notes |
|------|------|-------|
| 1 | Text | Multi-line text |
| 2 | Number | |
| 3 | SingleSelect | With `property.options` |
| 4 | MultiSelect | With `property.options` |
| 5 | DateTime | With `property.date_formatter` |
| 7 | Checkbox | true/false |
| 11 | User/Person | Uses open_id |
| 13 | Phone | |
| 15 | URL/Hyperlink | |
| 17 | Attachment | Needs file upload |
| 1001 | CreatedTime | Auto-filled |
| 1002 | ModifiedTime | Auto-filled |

## Bitable Patterns & Gotchas

### Accessing embedded bitables (bitable tabs within spreadsheets)

Spreadsheets can contain bitable-type tabs. These are NOT accessible via the regular Sheet Values API or directly via the Bitable API using the spreadsheet token. To access them:

1. Call the v2 metainfo endpoint: `GET /sheets/v2/spreadsheets/{spreadsheetToken}/metainfo`
2. Find the bitable tab — it has `blockInfo.blockToken` in format `{app_token}_{table_id}`
3. Use the extracted `app_token` and `table_id` with standard Bitable API endpoints

```python
# Example: extract app_token and table_id from blockToken
block_token = sheet["blockInfo"]["blockToken"]  # e.g. "Qnxmbq2euaQuI1sDOXVl5MGJg1d_tblcRkOGPnFoIr1Z"
app_token, table_id = block_token.rsplit("_", 1)
```

### Text field conversion for batch_create

When reading records via `records/search`, text fields (type 1) return as rich text arrays:
```json
[{"text": "Hello", "type": "text"}]
```
When writing via `batch_create`, text fields must be **plain strings** — passing the rich text array causes `TextFieldConvFail`. Convert first:
```python
value = "".join(e.get("text", "") for e in field_value if isinstance(e, dict))
```

### User field passthrough

User fields (type 11) can be written with the exact format returned by search:
```json
[{"id": "ou_xxx", "name": "Wind2star", "email": "user@example.com"}]
```
Minimal format also works: `[{"id": "ou_xxx"}]`. Plain strings do NOT work (`UserFieldConvFail`).

### View API limitations

The Bitable View API (`PATCH /bitable/v1/apps/{app_token}/tables/{table_id}/views/{view_id}`) only supports:
- `filter_info` — filter conditions
- `hidden_fields` — column visibility
- `hierarchy_config` — parent-child nesting

**NOT supported via API** (UI only): Group By, Sort, Frozen columns.

### SingleSelect filter values in views

View filter conditions for SingleSelect/MultiSelect fields require **option IDs** (not names):
```python
# Get option IDs from the fields endpoint first
# Then use them in the filter, wrapped as a JSON string:
"value": json.dumps(["optZDvNgr8"])  # NOT ["P0"]
```

### Option colors must be explicitly set

When creating bitable fields with select options (SingleSelect/MultiSelect), you must include the `color` property from the source. If omitted, the API assigns sequential defaults (0, 1, 2, ...) which causes visual mismatch with the original.

```python
# Include color when creating options
options = [{"name": opt["name"], "color": opt.get("color", 0)} for opt in source_options]
```

### Use batch_create response for record ID mapping

When copying records between tables, use the `batch_create` response to build old→new record ID mappings directly. Do NOT re-read records by index — leftover or deleted records can shift the order and break parent-child relationships.

```python
resp = batch_create(app_token, table_id, records_batch)
# resp["data"]["records"] contains new records in the same order as input
for old_rec, new_rec in zip(source_batch, resp["data"]["records"]):
    id_map[old_rec["record_id"]] = new_rec["record_id"]
```

### New bitables have 10 pre-created sample records

When creating a bitable via the wiki API (`obj_type: "bitable"`), it comes with 10 empty sample records. Delete them before or after copying data to avoid count mismatches:

```python
# Find and delete empty records
empty = [r['record_id'] for r in records if not any(
    v for v in r.get('fields', {}).values() if v is not None and v != '' and v != []
)]
if empty:
    api('POST', f'/bitable/v1/apps/{app}/tables/{table}/records/batch_delete', {'records': empty})
```

### Link field write format differs from read format

- **Read format**: `{"link_record_ids": ["recXXX"]}` (returned by search/get)
- **Write format**: `["recXXX"]` (plain list of record IDs)

Writing `{"link_record_ids": [...]}` causes `LinkFieldConvFail`.

### Field rename (PUT) requires type in body

When renaming a field via PUT, you must include the `type` parameter — not just `field_name`:

```python
# Wrong: {"field_name": "New Name"}  → 400 "type is required"
# Correct:
api('PUT', f'/bitable/.../fields/{field_id}', {"field_name": "New Name", "type": 1})
```

### Pagination is REQUIRED for querying records

When querying Bitable records via `base-records` or raw API calls, **always implement pagination**. The API returns results in pages — if you don't handle `page_token`, you'll only get the first page and miss remaining records.

**The problem:**
```python
# ❌ WRONG — only gets first 100 records, misses the rest
records_req = urllib.request.Request(
    f'https://open.larksuite.com/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=100',
    headers={'Authorization': f'Bearer {tenant_token}'}
)
with urllib.request.urlopen(records_req) as resp:
    records = json.loads(resp.read())['data']['items']  # Only page 1!
```

Even if the response shows `"total": 302`, you only got the first page.

**The solution:**
```python
# ✅ CORRECT — fetches all pages
all_records = []
page_token = None

while True:
    url = f'https://open.larksuite.com/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=100'
    if page_token:
        url += f'&page_token={page_token}'

    with urllib.request.urlopen(...) as resp:
        data = json.loads(resp.read())['data']
        all_records.extend(data['items'])

        if not data.get('has_more', False):
            break
        page_token = data.get('page_token')
```

**Key checklist:**
- Always check `has_more` in the response
- Use `page_token` from the response (not request parameters) to fetch the next page
- Stop when `has_more` is `false` or missing
- Same rule applies to: records, tables, views, fields — any list-type endpoint

## Board API (画板/Whiteboard)

The Board API (`board/v1`) manages content on whiteboard canvases. Boards are created as document blocks (type 43), then their content is managed via the Board API.

### Creating a board

No standalone "create board" endpoint exists. Instead, create a board block inside a document:
```python
# Creates board block — extract board.token from the response
resp = api('POST', f'/docx/v1/documents/{doc_id}/blocks/{parent_block_id}/children',
    {"children": [{"block_type": 43, "board": {}}], "index": -1})
# Response data.children contains FULL block objects, not just IDs
board_token = resp["data"]["children"][0]["board"]["token"]
```

### Node creation format

```python
api('POST', f'/board/v1/whiteboards/{board_token}/nodes', {"nodes": [
    {
        "type": "composite_shape",  # Node type
        "x": 100.0, "y": 100.0,    # Position (floats)
        "width": 200.0, "height": 80.0,  # Dimensions
        "composite_shape": {"type": "round_rect"},  # Shape subtype
        "text": {  # Text content (top-level, NOT inside shape)
            "text": "Hello",
            "font_size": 14,
            "horizontal_align": "center",
            "vertical_align": "mid"
        },
        "style": {  # Visual styling
            "fill_color": "#4A90D9",
            "fill_opacity": 100,  # 0-100 integer
            "border_style": "solid",  # "solid" | "none"
            "border_width": "medium",  # "medium" | "bold"
            "border_color": "#2D6CB4"
        }
    }
]})
```

### Connector format

Connectors use `start`/`end` with `attached_object` and relative position (0.0-1.0 within the target shape):
```python
{
    "type": "connector",
    "connector": {
        "start": {"attached_object": {"id": "o2:1", "position": {"x": 0.5, "y": 1.0}}},
        "end": {"attached_object": {"id": "o2:2", "position": {"x": 0.5, "y": 0.0}}}
    }
}
```

Free-floating connectors (no attachment) use position only:
```python
{"start": {"position": {"x": 100.0, "y": 200.0}}, "end": {"position": {"x": 300.0, "y": 200.0}}}
```

**Do NOT use** `start_object`/`end_object` at the connector level (error: "connector info empty"). `arrow_style` and `shape` fields cause field validation errors.

### Composite shape subtypes (confirmed working)

`rect`, `round_rect`, `diamond`, `ellipse`

### PlantUML / Mermaid diagrams

Generate diagrams from code using the `create_plantuml` endpoint:
```python
api('POST', f'/board/v1/whiteboards/{board_token}/nodes/plantuml', {
    "plant_uml_code": code_string,
    "syntax_type": 2,    # 1=PlantUML, 2=Mermaid
    "diagram_type": 1    # 1=flowchart, 4=sequence (and others)
})
```

- Returns `ids: []` (empty) on success — this is normal behavior
- Handles all layout, shapes, connectors, and styling automatically
- **Mermaid is recommended** — works reliably on new boards
- **PlantUML rendering bug**: New boards with ONLY PlantUML content show "Nothing on the board yet" in the doc preview, despite data being present (list/download APIs work). Workaround: add a dummy `composite_shape` node first to initialize the board renderer, or use Mermaid instead
- Cannot delete document blocks via API — no delete endpoint for docx blocks

### Known limitations

- **Append-only**: Can create and list nodes, but no update or delete endpoints
- **Doc block deletion**: Use `DELETE .../blocks/{parent_id}/children/batch_delete` with `{"start_index": N, "end_index": M}` (see below)
- **`sticky_note` type**: Returns error 4003101 despite being in the SDK types
- **Connector styling**: `arrow_style` and `shape` fields cause validation errors
- **Images**: Require pre-upload via Drive API (image token reference)
- **List nodes**: `GET .../nodes` may return empty for boards with content (inconsistent)

### Deleting boards from documents

While board nodes cannot be deleted, entire board **blocks** can be removed from a document using the docx batch delete API:
```python
# Delete blocks at indices start_index..end_index-1 (0-based) under the parent block
api('DELETE', f'/docx/v1/documents/{doc_id}/blocks/{parent_block_id}/children/batch_delete',
    {"start_index": 4, "end_index": 6})  # Deletes children at indices 4 and 5
```

First list blocks to find indices, then delete. **Careful**: indices shift after each delete.

### Other endpoints

- `GET /board/v1/whiteboards/{token}/download_as_image` — export as JPEG
- `GET/POST /board/v1/whiteboards/{token}/theme` — get/set board theme
- `POST /board/v1/whiteboards/{token}/nodes/plantuml` — create from PlantUML/Mermaid code
- `GET /board/v1/whiteboards/{token}/nodes` — list all nodes

## Tables in Documents

Create tables using block type 31:

```python
# 1. Create the table block — API auto-creates empty cells
resp = api('POST', f'/docx/v1/documents/{doc_id}/blocks/{parent_block_id}/children', {
    "children": [{"block_type": 31, "table": {"property": {"row_size": 4, "column_size": 3}}}],
    "index": -1
})
# Response contains cell block IDs in table.cells[]
cells = resp['data']['children'][0]['table']['cells']

# 2. Populate each cell by inserting text blocks as children
api('POST', f'/docx/v1/documents/{doc_id}/blocks/{cell_id}/children', {
    "children": [{"block_type": 2, "text": {
        "elements": [{"text_run": {"content": "Cell text", "text_element_style": {"bold": True}}}],
        "style": {"align": 1, "folded": False}
    }}],
    "index": 0
})
```

Tables also support `merge_info` (for merged cells) and `column_width` in property.

## Comments

### Read comments
```
GET /drive/v1/files/{document_id}/comments?file_type=docx&page_size=50
```
Returns all comments (both whole-document and inline). Each has `comment_id`, `is_whole`, `quote`, `is_solved`, `reply_list`.

### Create whole-document comment
```
POST /drive/v1/files/{document_id}/comments?file_type=docx
Body: {"reply_list": {"replies": [{"content": {"elements": [{"type": "text_run", "text_run": {"text": "..."}}]}}]}}
```

### Reply to a comment
```
POST /drive/v1/files/{document_id}/comments/{comment_id}/replies?file_type=docx
Body: {"content": {"elements": [{"type": "text_run", "text_run": {"text": "..."}}]}}
```

### Resolve/unresolve a comment
```
PATCH /drive/v1/files/{document_id}/comments/{comment_id}?file_type=docx
Body: {"is_solved": true}
```

### Inline comment limitations
- **Creating inline (anchored) comments is NOT possible via API** — the endpoint only creates whole-document comments
- `is_whole` and `quote` are response-only fields, not settable inputs
- `comment_ids` in `text_element_style` is read-only (cannot be set via block PATCH)
- Reading inline comments (created via UI) works fine — they have `is_whole: false` and `quote`

## Slides API

The Slides API is very limited:

```python
# Create empty presentation
api('POST', '/slides/v1/presentations', {"title": "My Slides"})

# Read presentation metadata (slide IDs, layouts, masters, page size)
api('GET', f'/slides/v1/presentations/{token}')

# Update title only (requires client_token as query param)
api('PATCH', f'/slides/v1/presentations/{token}?client_token={uuid}', {"title": "New Title"})
```

**Limitations:**
- Cannot read slide page content (elements, shapes, text) — only metadata
- Cannot create/add new slide pages — all formats return "param is invalid" (3130001)
- Cannot modify slide content — no known endpoint
- Not in any official SDK (Go, Node, Python)
- Scopes exist: `slides:presentation:read`, `slides:presentation:create`, `slides:presentation:update`, `slides:presentation:write_only`

## Required Lark App Scopes

| Scope | Operations |
|-------|-----------|
| (default) | Read wiki nodes, read document content, read blocks |
| `wiki:wiki` | Create wiki nodes |
| `docx:document` | Write document blocks (including board blocks) |
| `bitable:app` | All bitable operations (tables, fields, records) |
| `board:whiteboard:node:read` | List board nodes, download board as image |
| `board:whiteboard:node:create` | Create nodes on boards |
| `drive:drive` | Delete documents (not fully working yet) |
| `drive:drive:permission:member` | Add/list document collaborators |
| `contact:user.id:readonly` | Look up user IDs by email |
| `search:docs` | Search documents globally |
| `slides:presentation:read` | Read slides metadata |
| `slides:presentation:create` | Create empty presentations |
| `slides:presentation:update` | Update presentation title |

The bot also needs **edit permission** on the wiki space (added via wiki space settings → Members).
