---
name: mssql
description: Queries and manages Microsoft SQL Server databases via the mssql CLI. Use when running SQL queries, inspecting table schemas, or managing server connections. Triggers on phrases like "SQL query", "database", "table schema", "run query", "SQL Server", "mssql", "check the database", "look up in the database".
compatibility: Requires mssql CLI installed (npm install -g @billpeet/mssql-cli) and configured (mssql server add --name <name> --server <host> --database <db>), or MSSQL_SERVER, MSSQL_DATABASE, and authentication environment variables set.
---

# Microsoft SQL Server

Interact with Microsoft SQL Server databases using the `mssql` CLI. All commands output JSON by default for reliable parsing.

> **IMPORTANT — Agent safety rules:**
>
> 1. **Never run `mssql sql-dangerous` without explicit user approval.** Always present the full SQL query to the user and explain what it does before executing. This command can modify or destroy data (INSERT, UPDATE, DELETE, DROP, etc.).
> 2. **Prefer `mssql sql` for reads.** Use the read-only `mssql sql` command for SELECT queries. It blocks dangerous statements automatically.
> 3. **Prefer `mssql schema` over raw queries** when you need table structure information.
> 4. If you are unsure of the schema, use `mssql schema` to check first — do not guess column or table names.

## Setup

### Add a server connection

```bash
mssql server add --name mydb --server localhost --database MyDatabase --user sa --password "secret" --format json
mssql server add --name mydb --server db.example.com --database MyDatabase --windows-auth --trust-cert --format json
```

The first server added is automatically set as the default. Config is saved to `~/.config/mssql-cli/config.json`.

### Environment variables

Environment variables create a transient connection that takes priority over the config file:

```bash
export MSSQL_SERVER=localhost
export MSSQL_DATABASE=MyDatabase
export MSSQL_USER=sa
export MSSQL_PASSWORD=secret
export MSSQL_PORT=1433          # optional, default 1433
export MSSQL_ENCRYPT=true       # optional
export MSSQL_TRUST_CERT=true    # optional
export MSSQL_WINDOWS_AUTH=true  # optional, use instead of user/password
```

## Server Management

### List configured servers

```bash
mssql server list --format json --pretty
```

### Set the default server

```bash
mssql server default --name mydb --format json
```

### Test connectivity

```bash
mssql server test --format json
mssql server test --name mydb --format json
```

### Remove a server

```bash
mssql server remove --name mydb --format json
```

### View or update global settings

```bash
mssql server config --format json
mssql server config --max-rows 500 --format json
```

The `maxRows` setting (default: 100) limits the number of rows returned by queries. A truncation warning is included when results are capped.

## Queries (Read-Only)

Use `mssql sql` for SELECT queries. This command **blocks** any statements that could modify data (INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE, MERGE, EXEC, etc.) and directs you to use `sql-dangerous` instead.

```bash
mssql sql --query "SELECT TOP 10 * FROM Users" --format json --pretty
mssql sql --query "SELECT COUNT(*) AS total FROM Orders WHERE Status = 'Pending'" --format json
mssql sql --query "SELECT u.Name, COUNT(o.Id) AS OrderCount FROM Users u JOIN Orders o ON u.Id = o.UserId GROUP BY u.Name" --server mydb --format json --pretty
mssql sql --file report.sql --format json --pretty
```

Use `--query` for inline SQL or `--file` to read SQL from a `.sql` file. These options are mutually exclusive.

Results are limited to the configured `maxRows` (default 100). If more rows exist, the output includes a truncation warning.

## Queries (Dangerous — Modifying)

> **Agents: NEVER run this command without first showing the query to the user and receiving explicit approval.**

Use `mssql sql-dangerous` for statements that modify data or schema. This command has no safety restrictions.

```bash
mssql sql-dangerous --query "INSERT INTO Users (Name, Email) VALUES ('Alice', 'alice@example.com')" --format json
mssql sql-dangerous --query "UPDATE Orders SET Status = 'Shipped' WHERE Id = 42" --format json
mssql sql-dangerous --query "DELETE FROM Sessions WHERE ExpiresAt < GETDATE()" --format json
mssql sql-dangerous --query "CREATE INDEX IX_Users_Email ON Users(Email)" --format json
mssql sql-dangerous --file migration.sql --format json
```

As with `mssql sql`, use `--query` for inline SQL or `--file` to read from a file (mutually exclusive).

The output includes `rowsAffected` count in addition to any result rows.

## Schema Inspection

Get full schema details for one or more tables — columns, data types, primary keys, foreign keys (both directions), and indexes.

```bash
mssql schema Users --format json --pretty
mssql schema Users Orders --format json --pretty
mssql schema dbo.Users sales.Orders --format json --pretty
```

Tables default to the `dbo` schema if not specified. Use `schema.table` notation for other schemas.

## Output Format

All commands support `--format json` (compact, default) or `--format text` (human-readable tables). Add `--pretty` for indented JSON.

Exit codes: `0` = success, `1` = error. Errors are written to stderr as JSON.

## Common Workflows

**Explore a table before querying:**
```bash
mssql schema Users --format json --pretty
mssql sql --query "SELECT TOP 5 * FROM Users" --format json --pretty
```

**Check row counts across tables:**
```bash
mssql sql --query "SELECT 'Users' AS TableName, COUNT(*) AS Rows FROM Users UNION ALL SELECT 'Orders', COUNT(*) FROM Orders" --format json --pretty
```

**Safe data fix (always confirm with user first):**
```bash
# 1. Check current state
mssql sql --query "SELECT Id, Email FROM Users WHERE Id = 42" --format json --pretty
# 2. After user approval, apply the fix
mssql sql-dangerous --query "UPDATE Users SET Email = 'new@example.com' WHERE Id = 42" --format json
# 3. Verify the change
mssql sql --query "SELECT Id, Email FROM Users WHERE Id = 42" --format json --pretty
```
