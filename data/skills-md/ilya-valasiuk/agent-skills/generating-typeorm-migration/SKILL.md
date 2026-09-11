---
name: generating-typeorm-migration
description: Explains how to create and review TypeORM migrations. Use this skill whenever the user wants to change an entity, add or update schema-related database objects, generate a migration, or decide whether a database change should be handled through TypeORM metadata or a custom migration.
---

# Generating TypeORM Migrations

This skill covers the end-to-end process for creating a TypeORM database migration. It ensures migrations are generated correctly, named clearly, and never run automatically. Follow these steps in order every time.

## Step 1 — Update the Entity

Modify the relevant TypeORM entity file (located in `apps/api/src/core/<domain>/entities/` or `libs/`). Add or change columns, indexes, relations, etc. using TypeORM decorators.

Use generated migrations by default. Do **not** write migration SQL by hand unless TypeORM cannot represent the database object you need.

## Step 2 — Generate the Migration

Run the following command from the project root, passing a `--name` flag with a clear descriptive slug:

```bash
npm run migration:api:generate --name=<migration-name>
```

The name becomes part of the filename: `apps/api/src/database/migrations/<timestamp>-<migration-name>.ts`. Choose it carefully upfront — use kebab-case and follow the conventions from existing migrations:

- `add-` — adding a column, index, constraint, or trigger
- `remove-` / `delete-` / `drop-` — removing something
- `create-` — creating a new table
- `update-` / `rename-` / `replace-` / `normalize-` — modifying existing data or structure
- `migrate-` — moving/transforming data between columns or tables
- `new-` — introducing a new enum value or entity

**Examples from this project:**

```bash
npm run migration:api:generate --name=add-new-office-index
npm run migration:api:generate --name=create-integration-table
npm run migration:api:generate --name=migrate-office-and-remcat-sources-to-integration-source
npm run migration:api:generate --name=add-has-active-office-to-place-trigger
npm run migration:api:generate --name=new-integration-mapper-enum
```

## Step 2A — Handle TypeORM Limitations

If the required database change cannot be expressed in TypeORM entity metadata, do **not** force it into the entity with a fake column or workaround just to make migration generation pass.

Typical examples:

- Expression indexes, such as `USING GIST (ST_Transform(geom, 2056))`
- Custom SQL functions or triggers
- Postgres features not supported by this TypeORM version's decorators/metadata model

In these cases:

1. Confirm that TypeORM really cannot model the change in this project version.
2. Keep the entity as the real source of truth for the actual columns and relations only.
3. Add a short code comment near the relevant entity field or in the entity-level DB notes that explains:
   - what custom DB object exists
   - which migration created it
   - why it is not declared through TypeORM metadata
4. Create the migration intentionally for that custom SQL:

```bash
npm run migration:api:create --name=<migration-name>
```

5. Fill in the migration file manually with the minimal `up()` / `down()` SQL required.

If you need a concrete project example for a custom migration plus matching entity comment, read `references/custom-migration-example.md`.

## Step 3 — Review the Generated File

Open the newly created file and verify:

- The `up()` method contains only the expected changes.
- The `down()` method correctly reverts them.
- No unrelated tables or columns are touched.

If the diff looks wrong, check whether other entities have unsaved changes that were picked up unintentionally.

For hand-written custom migrations, review the same way:

- The SQL does only the intended custom change
- The rollback is correct
- The entity contains the explanatory comment when the DB object is not representable in TypeORM

## Step 4 — Stop Here. Do NOT Run the Migration.

**Never run `npm run migration:api:run` automatically.** The developer runs migrations manually at the right time (e.g., before a deployment or after coordinating with the team).

Do not suggest running the migration. Do not run it "just to test". Simply leave the generated file in place and inform the user that the migration is ready and they should run it when appropriate.

---

## Quick Reference

| Command                                        | Purpose                                              |
| ---------------------------------------------- | ---------------------------------------------------- |
| `npm run migration:api:generate --name=<name>` | Generate a migration from entity changes             |
| `npm run migration:api:create --name=<name>`   | Create an empty migration file for custom/manual SQL |
| `npm run migration:api:show`                   | List applied/pending migrations                      |
| `npm run migration:api:run`                    | **Run manually only — never automated**              |
| `npm run migration:api:revert`                 | Revert the last migration                            |

## Key Paths

- **Entities**: `apps/api/src/core/<domain>/entities/` or `libs/domains/`
- **Migrations**: `apps/api/src/database/migrations/`
- **TypeORM config**: `apps/api/src/config/typeorm.config.ts`
