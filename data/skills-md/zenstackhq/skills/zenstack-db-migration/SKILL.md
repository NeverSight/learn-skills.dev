---
name: zenstack-db-migration
description: Manage database schema migrations in ZenStack V3. Use when creating/applying migrations (zen migrate dev/deploy/reset/status/resolve), prototyping with zen db push, introspecting an existing database with zen db pull, seeding, handling unsupported features (views) with --create-only, or wiring migrations into a deployment pipeline.
---

# ZenStack V3 — Database Migrations

ZenStack keeps your database schema in sync with your ZModel data model. Migration is built on top
of [Prisma Migrate](https://www.prisma.io/docs/orm/prisma-migrate): the `zen` CLI generates a Prisma
schema from your ZModel under the hood and wraps the corresponding Prisma command. If you know Prisma
Migrate, the workflow is identical — just swap `prisma` for `zen`. Existing migration history keeps
working once moved into ZenStack's layout (`prisma/migrations` → `zenstack/migrations`, the default
location next to `zenstack/schema.zmodel`).

This skill assumes a project is already set up (see `zenstack-project-setup`). Schema authoring is in
`zenstack-schema-modeling`. `@zenstackhq/cli` carries a peer dependency on `prisma`, installed
automatically when needed.

> Run `zen generate` after schema changes to refresh generated types; migration commands operate on
> the schema independently of the generated client.

## Two ways to evolve the schema

| Approach | Command | When |
| -------- | ------- | ---- |
| **Schema prototyping** | `zen db push` | Local dev/experimentation — syncs the DB to the schema with **no migration file**. Fast, but loses history. **Never in production.** |
| **Tracked migrations** | `zen migrate dev` → `zen migrate deploy` | Anything you ship — generates reviewable, committed SQL migration files applied deterministically across environments. |

Typical loop: prototype with `db push` while iterating, then create a migration with `migrate dev`
once the shape settles.

## Commands

All migration/db commands accept `--schema <file>` (defaults to `zenstack/schema.zmodel`) and
`--migrations <path>` (the directory holding `migrations/`).

### `zen migrate dev` — create + apply a migration (development)

Diffs the schema against migration history, generates a new timestamped migration file, and applies
it to the dev database. Prompts if a full reset is required (e.g. drift).

```bash
zen migrate dev --name add_published_flag
```

- `-n, --name <name>` — name the migration (otherwise you're prompted).
- `--create-only` — generate the migration file **without applying it**. Use this to hand-edit SQL,
  or to implement features the migration engine doesn't generate yet (e.g. database views — create
  an empty migration and write the SQL manually), then apply later with `zen migrate dev`.

Review the generated SQL before committing it to source control.

### `zen migrate deploy` — apply pending migrations (production)

Applies all not-yet-applied migrations. Idempotent and non-interactive — this is the command for
your **deployment pipeline**. It never generates new migrations or resets data.

```bash
zen migrate deploy
```

### `zen migrate status` — inspect migration state

Shows which migrations are applied vs. pending. Useful in CI before deploying.

```bash
zen migrate status
```

### `zen migrate resolve` — fix history without touching the schema

Marks a migration as applied or rolled back — for manual recovery (e.g. a migration applied
out-of-band, or a failed one). Does not change the database schema.

```bash
zen migrate resolve --applied 20240101120000_add_users
zen migrate resolve --rolled-back 20240101120000_add_users
```

### `zen migrate reset` — wipe and reapply (development)

Drops all tables and replays every migration from scratch. Destructive — **dev/testing only, never
production**.

```bash
zen migrate reset --force   # --force skips the confirmation prompt
```

If a seed script is configured, it runs after reset (use `--skip-seed` to skip).

### `zen db push` — sync schema, no migration file (development)

Pushes the schema straight to the database. Great for rapid prototyping; no history is recorded.

```bash
zen db push
zen db push --accept-data-loss   # proceed despite data-loss warnings
zen db push --force-reset        # reset the DB before pushing
```

### `zen db pull` — introspect an existing database (v3.4.0+, experimental)

Loads the database schema, diffs it against your ZModel, and updates the ZModel to match. Useful for
adopting ZenStack on an existing DB, or re-syncing after out-of-band DB changes. This has its own
implementation (not Prisma's introspection engine).

```bash
zen db pull
```

Options: `-o, --output <path>`, `--model-casing <pascal|camel|snake|none>` (default `pascal`),
`--field-casing <...>` (default `camel`), `--always-map` (always emit `@map`/`@@map`),
`--quote <double|single>` (default `single`), `--indent <number>` (default `4`).

> **Warning:** `zen db pull` can overwrite your schema file. Commit or back it up first.

### `zen db seed` — seed the database

Runs the seed script declared in `package.json` under `zenstack.seed`:

```json
{ "zenstack": { "seed": "tsx ./zenstack/seed.ts" } }
```

```bash
zen db seed
zen db seed -- --users 10   # args after -- are forwarded to the seed script
```

## Workflows

**Development**

1. Edit `zenstack/schema.zmodel`.
2. `zen db push` to try it instantly while iterating (optionally `zen db seed`).
3. When the shape is final, `zen migrate dev --name <change>` to create the migration.
4. Review the SQL, commit the migration file.

**Production / CI deployment**

```bash
zen migrate deploy
```

Run it in the release pipeline. Optionally gate on `zen migrate status` first. Do **not** run
`db push`, `migrate dev`, or `migrate reset` against production.

**Adopt an existing database**

`zen init` → set the datasource `url` → `zen db pull` → refine the schema (policies, computed
fields) → `zen generate`. See `zenstack-project-setup`.

## Adopting from Prisma

Because migration wraps Prisma Migrate, your existing migration history keeps working once you move
the `prisma/migrations` directory to `zenstack/migrations` (ZenStack's default, next to
`zenstack/schema.zmodel`) and replace the `prisma migrate ...` / `prisma db ...` scripts with the
`zen` equivalents. Full framework migration is covered by `zenstack-migrate-from-prisma`.

## Reference docs

Full ZenStack documentation for this topic is bundled under [`references/`](references/):

- [migration.md](references/migration.md) — migration concepts and workflows
- [introspection.md](references/introspection.md) — `zen db pull` introspection
- [cli-reference.md](references/cli-reference.md) — complete `migrate`/`db` command + option reference
