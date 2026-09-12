---
name: pipefy-database-tables
description: >
  Use this skill when the user wants to work with Pipefy Database Tables —
  creating/reading/updating/deleting tables, records (rows), or table fields
  (schema columns). Covers 17 MCP tools.
tags: [pipefy, database, tables, records, fields]
---

# Database Tables

Tables, records (rows), schema columns (table fields), and attachments for Pipefy Database Tables. **17 MCP tools.**

---

## Cross-cutting patterns

- Same conventions as pipe building: `introspect_type` on inputs such as `CreateTableFieldInput` / `UpdateTableFieldInput`, `debug=true` on mutations.
- **Pagination:** `get_table_records` and `find_records` support `first` / `after`. With the unified MCP envelope, read top-level `pagination.has_more` and `pagination.end_cursor` (and `pagination.page_size`) and pass `after=end_cursor` for the next page (default page size is 50).
- **`find_records` over paginated `get_table_records`** when you know the field value. One `find_records` call with a `column_id`/`search_value` filter beats N pages of `get_table_records`.
- **Legacy mutation envelope.** Several table mutation tools still return the GraphQL operation name as a nested key under `result` (for example `result.createTableRecord`). Read the payload inside that key; shape may differ from tools that already use the unified envelope.

---

## Table operations

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_tables` | `pipefy table list` | Yes | List database tables by org. |
| `search_tables` | `pipefy table list --search` | Yes | Search tables by name. |
| `get_table` | `pipefy table get <id>` | Yes | Table metadata and field schema. |
| `create_table` | `pipefy table create` | No | Create a new database table. |
| `update_table` | `pipefy table update <id>` | No | Rename or change settings. |
| `delete_table` | `pipefy table delete <id>` | No | **Two-step destructive.** |

---

## Table field (schema column) operations

| Tool (MCP) | CLI | Purpose |
|------------|-----|---------|
| `create_table_field` | `pipefy table field create <table_id> --label <name> --type <type>` | Add a column to a table schema. |
| `update_table_field` | `pipefy table field update <field_id> --table <table_id> --label <name>` | Rename or change column settings (`--description`, `--required`, `--options`). |
| `delete_table_field` | `pipefy table field delete <field_id> --table <table_id>` | **Two-step destructive.** Requires `table_id`. |

---

## Record operations

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_table_records` | `pipefy record find --table <id>` | Yes | Paginated list of all records in a table. |
| `find_records` | `pipefy record find --filter` | Yes | Filter records by field value (JSON filter) — preferred over paginating `get_table_records`. |
| `get_table_record` | `pipefy record get <id>` | Yes | Single record with all populated field values. |
| `create_table_record` | `pipefy record create` | No | Add a row to a table. |
| `update_table_record` | `pipefy record update <id> --fields ...` | No | Update one or more field values on a row. |
| `set_table_record_field_value` | `pipefy record update <id> --field-id <slug> --value <json>` | No | More targeted single-field update than `update_table_record`. |
| `delete_table_record` | `pipefy record delete <id>` | No | **Two-step destructive.** |

---

## Attachment uploads

| Tool (MCP) | CLI | Purpose |
|------------|-----|---------|
| `upload_attachment_to_table_record` | `pipefy attachment upload --record <id> --field <slug> --file <path> --organization <id>` | Attach a file to a table record. Exactly one source: `file_path` (local; local profile only) or `file_url` (downloaded, SSRF-guarded; any profile — required on the hosted server). CLI is `--file` only. See [`pipefy-attachments`](../../attachments/pipefy-attachments/SKILL.md). |

---

## Steps — find and update a record

1. **Get table ID** (if not known):

   MCP: `get_tables organization_id=123`

   CLI: `pipefy table list`

2. **Find the record** (use `find_records`, not pagination):

   MCP: `find_records table_id=456 filter='{"column_id":"email","search_value":"user@example.com"}'`

   CLI: `pipefy record find --table 456 --filter '{"column_id":"email","search_value":"user@example.com"}'`

3. **Update one field** (targeted):

   MCP: `set_table_record_field_value record_id=789 field_id="status" value="Active"`

   CLI: `pipefy record update 789 --field-id status --value '"Active"'`

   **Update multiple fields:**

   MCP: `update_table_record record_id=789 node_fields='[{"field_id":"status","field_value":"Active"}]'`

   CLI: `pipefy record update 789 --fields '{"status":"Active"}'`

---

## Two-step destructive previews

Always call without `confirm=true` first, surface the preview (including `confirmation_token`) to the user, then call again with `confirm=true` and that token after explicit approval. CLI uses `--yes` (no token). Preview content per tool:

- **`delete_table`** — show table **name**, **field count**, and **record count**. Deleting a table destroys all rows and schema.
- **`delete_table_record`** — show record **title** and **key field values** so the user can identify which row will vanish.
- **`delete_table_field`** — show field **name** and **type**; warn explicitly that **all column data will be permanently lost**.

Never delete in a single call.

---

## Success criteria

- `get_table_records` returns the created/updated records with correct field values.
- Schema changes reflect immediately in `get_table`.

## Failure modes

- **`get_table_record` / `get_table_records` omit empty fields.** Records only return populated fields, so you cannot tell "field unset" from "field doesn't exist" without calling `get_table` for the full schema.
- **`create_table_record` title silently overridden.** When the first table field is a start-form-style label column, Pipefy uses that field's value as the record `title`, ignoring the `title` parameter. Don't rely on `title` if the first field auto-populates a label-like column.
- **`create_table_field` rejects type:** call `introspect_type type_name="CreateTableFieldInput"` for valid field types.
- **`find_records` returns empty:** check that `column_id` matches a field's **ID** (not label) from `get_table`.
- **Pagination cursor expired:** re-fetch from the beginning; cursors are short-lived.

## See also

- [skills/relations/pipefy-relations/SKILL.md](../../relations/pipefy-relations/SKILL.md) — connect tables to pipes (and the table-relation ID namespace gotcha).
- [skills/introspection/pipefy-introspection/SKILL.md](../../introspection/pipefy-introspection/SKILL.md) — discover field input schemas.
