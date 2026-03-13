---
name: hotdata-cli
description: Use this skill when the user wants to run hotdata CLI commands, query the HotData API, list workspaces, list connections, list tables, execute SQL queries, or interact with the hotdata service. Activate when the user says "run hotdata", "query hotdata", "list workspaces", "list connections", "list tables", "execute a query", or asks you to use the hotdata CLI.
version: 0.1.3
---

# HotData CLI Skill

Use the `hotdata` CLI to interact with the HotData service. In this project, run it as:

```
hotdata <command> [args]
```

Or if installed on PATH: `hotdata <command> [args]`

## Authentication

Config is stored in `~/.hotdata/config.yml` keyed by profile (default: `default`).
API key can also be set via `HOTDATA_API_KEY` env var.
API URL defaults to `https://api.hotdata.dev/v1` or overridden via `HOTDATA_API_URL`.

## Workspace ID

All commands that accept `--workspace-id` are optional. If omitted, the first workspace saved during `hotdata auth login` is used as the default. **Omit `--workspace-id` unless you need to target a specific workspace.**

## Available Commands

### List Workspaces
```
hotdata workspaces list [--format table|json|yaml]
```
Returns workspaces with `public_id`, `name`, `active`, `favorite`, `provision_status`.

### List Connections
```
hotdata connections list [--workspace-id <workspace_id>] [--format table|json|yaml]
```
Routes via API gateway using `X-Workspace-Id` header.

### List Tables and Columns
```
hotdata tables list [--workspace-id <workspace_id>] [--connection-id <connection_id>] [--schema <pattern>] [--table <pattern>] [--limit <int>] [--cursor <cursor>] [--format table|json|yaml]
```
- Default format is `table`.
- **Always use this command to inspect available tables and columns.** Do NOT use the `query` command to query `information_schema` for this purpose.
- Without `--connection-id`: lists all tables with `table`, `synced`, `last_sync`. The `table` column is formatted as `<connection>.<schema>.<table>`.
- With `--connection-id`: includes column definitions. Lists each column as its own row with `table`, `column`, `data_type`, `nullable`. Use this to inspect the schema before writing queries.
- **Always use the full `<connection>.<schema>.<table>` name when referencing tables in SQL queries.**
- `--schema` and `--table` support SQL `%` wildcard patterns (e.g. `--table order%` matches `orders`, `order_items`, etc.).
- Results are paginated (default 100 per page). If more results are available, a `--cursor` token is printed — pass it to fetch the next page.

### Execute SQL Query
```
hotdata query "<sql>" [--workspace-id <workspace_id>] [--connection <connection_id>] [--format table|json|csv]
```
- Default format is `table`, which prints results with row count and execution time.
- Use `--connection` to scope the query to a specific connection.
- Use `hotdata tables list` to discover tables and columns — do not query `information_schema` directly.
- **Always use PostgreSQL dialect SQL.**

### Get Query Result
```
hotdata results <result_id> [--workspace-id <workspace_id>] [--format table|json|csv]
```
- Retrieves a previously executed query result by its result ID.
- Query results include a `result-id` in the footer (e.g. `[result-id: rslt...]`).
- **Always use this command to retrieve past query results rather than re-running the same query.** Re-running queries wastes resources and may return different results.

### Auth
```
hotdata auth login          # Browser-based login
hotdata auth status         # Check current auth status
```

### Init
```
hotdata init                # Create ~/.hotdata/config.yml
```

## Workflow: Running a Query

1. List connections:
   ```
   hotdata connections list
   ```
2. Inspect available tables:
   ```
   hotdata tables list
   ```
3. Inspect columns for a specific connection:
   ```
   hotdata tables list --connection-id <connection_id>
   ```
4. Run SQL:
   ```
   hotdata query "SELECT 1"
   ```
