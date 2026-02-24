---
name: implementing-dapper-queries
description: Implementing Dapper repository methods and stored procedures for MSSQL at Bitwarden. Use when creating or modifying Dapper repositories, writing stored procedures, or working with MSSQL-specific data access in the server repo.
---

## Repository Pattern

All Dapper implementations live in `src/Infrastructure/Dapper/Repositories/`. Each repository class implements an interface from `src/Core/` and uses stored procedures for all database operations. The repository method is intentionally thin — it maps C# parameters to SQL parameters and maps result sets back to domain objects.

### Stored procedures over inline SQL

The default pattern is stored procedures for all Dapper database operations. Some exceptions exist where inline SQL is used — these are provided automatically by the repository base class and parent patterns, not written ad-hoc in individual repository methods.

## Workflow

1. **Define/update the stored procedure** in `src/Sql/dbo/Stored Procedures/`
2. **Create a migration script** in `util/Migrator/DbScripts/` that deploys it
3. **Implement the repository method** in `src/Infrastructure/Dapper/Repositories/` using `DapperServiceProvider` to call the procedure
4. **Write integration tests** using `[DatabaseData]` attribute

The stored procedure is the source of truth for MSSQL query behavior. The Dapper repository method is thin — it maps parameters and results.

### Stored procedure naming convention

Procedures follow `{Entity}_{Action}` pattern: `User_Create`, `Cipher_ReadManyByUserId`, `Organization_DeleteById`. Tooling and code generation rely on this convention to map repository methods to their procedures.

## Key Decisions That Trip Up AI Assistants

### Always use `CREATE OR ALTER`

Never use `CREATE PROCEDURE` or `DROP/CREATE`. `CREATE OR ALTER` is idempotent — it works whether the procedure exists or not. This is critical for migrations that might be re-run.

### New parameters must be nullable with defaults

When adding parameters to existing stored procedures, always use `@NewParam DATATYPE = NULL`. Existing callers don't pass the new parameter — without a default, they break.

### NOT NULL columns: use inline defaults, not ALTER-UPDATE-ALTER

Adding a NOT NULL column by first adding it nullable, updating all rows, then altering to NOT NULL causes a full table scan. Instead, use `ADD [Column] INT NOT NULL CONSTRAINT DF_Table_Column DEFAULT 0` — this is a metadata-only operation in SQL Server. **This is the single most common mistake AI assistants make with Bitwarden migrations.**

### Never create indexes on large tables in migration scripts

Creating indexes on `dbo.Cipher`, `dbo.OrganizationUser`, or other large tables in migration scripts can cause outages. Never specify `ONLINE = ON` in scripts — production handles this automatically, and the option fails on unsupported SQL Server editions. Large index operations belong in `DbScripts_manual`.

### Use defaults only for numeric types

Use defaults for `BIT`, `TINYINT`, `INT`, `BIGINT`. Never use defaults for `VARCHAR`, `NVARCHAR`, or MAX types. SQL Server handles these differently and defaults on strings create unexpected behavior with EF Core migrations.

### Views require metadata refresh

After modifying a table, any views that reference it have stale metadata. Call `sp_refreshview` on affected views. After altering views, call `sp_refreshsqlmodule` on dependent procedures. This is the most frequently forgotten step.

### GUID columns use `UNIQUEIDENTIFIER`

All entity IDs are `UNIQUEIDENTIFIER` populated by `CoreHelpers.GenerateComb()` in application code, not by SQL Server. Never use `NEWID()` or `NEWSEQUENTIALID()` in stored procedures.

## EF Parity Requirement

Every stored procedure's behavior must be exactly replicated in the EF Core implementation. When writing a new stored procedure, think about how the EF implementation will reproduce the same filtering, ordering, and side effects. If a stored procedure does something complex (e.g., conditional updates, multi-table operations), document the expected behavior clearly so the EF implementation can match it.

## Critical Rules

These are the most frequently violated conventions. Claude cannot fetch the linked docs at runtime, so these are inlined here:

- **`SET NOCOUNT ON`** at the start of every stored procedure
- **Parameter naming:** `@ParamName` in PascalCase, matching C# property names
- **All procedures must be idempotent** — use `CREATE OR ALTER`, never `CREATE` alone
- **Constraint naming:** `PK_TableName`, `FK_Child_Parent`, `IX_Table_Column`, `DF_Table_Column`
- **Stored procedure file naming:** one procedure per file, named `{Entity}_{Action}.sql`

## Examples

### Stored procedure creation

```sql
-- CORRECT — idempotent
CREATE OR ALTER PROCEDURE [dbo].[User_ReadById]
    @Id UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON
    SELECT * FROM [dbo].[User] WHERE [Id] = @Id
END

-- WRONG — fails if procedure already exists
CREATE PROCEDURE [dbo].[User_ReadById]
```

### Adding a NOT NULL column

```sql
-- CORRECT — metadata-only operation, no table scan
ALTER TABLE [dbo].[Organization]
    ADD [UseCustomPermissions] BIT NOT NULL CONSTRAINT DF_Organization_UseCustomPermissions DEFAULT 0

-- WRONG — causes full table scan on large tables
ALTER TABLE [dbo].[Organization] ADD [UseCustomPermissions] BIT NULL
UPDATE [dbo].[Organization] SET [UseCustomPermissions] = 0
ALTER TABLE [dbo].[Organization] ALTER COLUMN [UseCustomPermissions] BIT NOT NULL
```

### Adding parameters to existing procedures

```sql
-- CORRECT — existing callers won't break
CREATE OR ALTER PROCEDURE [dbo].[Cipher_Create]
    @Id UNIQUEIDENTIFIER,
    @NewField NVARCHAR(MAX) = NULL  -- default protects existing callers

-- WRONG — breaks all existing callers immediately
CREATE OR ALTER PROCEDURE [dbo].[Cipher_Create]
    @Id UNIQUEIDENTIFIER,
    @NewField NVARCHAR(MAX)  -- no default = required parameter
```

## Further Reading

- [SQL code style](https://contributing.bitwarden.com/contributing/code-style/sql/)
- [Database migrations (MSSQL)](https://contributing.bitwarden.com/contributing/database-migrations/mssql)
