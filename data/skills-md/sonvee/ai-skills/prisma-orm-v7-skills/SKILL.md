---
name: prisma-orm-v7-skills
description: Key facts and breaking changes for upgrading to Prisma ORM 7. Consider version 7 changes before generation or troubleshooting
---

## Links

- Upgrade guide (v7): https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-7
- Prisma Config reference: https://www.prisma.io/docs/orm/reference/prisma-config-reference
- Prisma Client Extensions: https://www.prisma.io/docs/orm/prisma-client/client-extensions
- Prisma 7 migration prompt (AI agents): https://www.prisma.io/docs/ai/prompts/prisma-7

## Upgrade

```sh
# Upgrade packages
pnpm add @prisma/client@7
pnpm add -D prisma@7
```

## Breaking Changes (v7)

### Minimum versions

- Node.js: 20.19.0+ (and 22.x)
- TypeScript: 5.4.0+

### Prisma is now ESM

- Prisma ORM ships as ES modules.
- Set `"type": "module"` in `package.json` (or migrate your project to ESM).
- TypeScript projects must compile/resolve ESM (guide example: `module: ESNext`, `target: ES2023`, `moduleResolution: node`).

### Prisma schema + generation changes

- Generator provider: `prisma-client-js` → `prisma-client`.
- `output` is required in `generator client`.
- Prisma Client is no longer generated into `node_modules` by default.
- After `npx prisma generate`, update imports to your generated output path (example:
	`import { PrismaClient } from './generated/prisma/client'`).

Schema datasource deprecations:

- `url`, `directUrl`, `shadowDatabaseUrl` in `schema.prisma` are deprecated.
- Move datasource config to `prisma.config.ts` (Prisma Config).
- If you used `directUrl` for migrations, set the CLI migration connection string in `prisma.config.ts`.

### Driver adapters required for Prisma Client (new instantiation)

- Prisma Client creation now requires a driver adapter for all databases.
- Example adapters:
	- Postgres: `@prisma/adapter-pg` (use `PrismaPg` with a direct DB connection string)
	- SQLite: `@prisma/adapter-better-sqlite3`

### Prisma Accelerate users (v6 → v7)

- Do not pass `prisma://` or `prisma+postgres://` (Accelerate URLs) to a driver adapter.
- Keep the Accelerate URL and instantiate Prisma Client with the Accelerate extension instead.

### Env vars are not loaded by default

- Prisma CLI no longer auto-loads `.env` files in v7.
- Explicitly load env vars (for example `import 'dotenv/config'` in `prisma.config.ts`, or load env in your scripts).
- Bun users: no change required (bun auto-loads `.env`).

### Prisma CLI config moved to `prisma.config.ts`

- Prisma Config is now the default place to configure how Prisma CLI behaves.
- Place `prisma.config.ts` at the project root (next to `package.json`).
- Configure schema path, migrations path/seed, and datasource URL there.

### Client middleware removed

- `prisma.$use(...)` is removed.
- Migrate middleware logic to Prisma Client Extensions.

### Metrics removed from Client Extensions

- The Metrics preview feature is removed in v7.
- Use your database driver/adapter or implement custom counters via extensions.

### Migrate/seed/generate behavior changes

- Automatic seeding after `prisma migrate dev` / `prisma migrate reset` is removed.
	- Run seeding explicitly: `pnpm prisma db seed` (or `pnpm exec prisma db seed`).
- `--skip-generate` and `--skip-seed` flags removed.
- `prisma migrate dev` and `prisma db push` no longer run `prisma generate` automatically.
	- Run `pnpm prisma generate` (or `pnpm exec prisma generate`) explicitly.

### Prisma-specific env vars removed

- Removed env vars:
	- `PRISMA_CLI_QUERY_ENGINE_TYPE`
	- `PRISMA_CLIENT_ENGINE_TYPE`
	- `PRISMA_QUERY_ENGINE_BINARY`
	- `PRISMA_QUERY_ENGINE_LIBRARY`
	- `PRISMA_GENERATE_SKIP_AUTOINSTALL`
	- `PRISMA_SKIP_POSTINSTALL_GENERATE`
	- `PRISMA_GENERATE_IN_POSTINSTALL`
	- `PRISMA_GENERATE_DATAPROXY`
	- `PRISMA_GENERATE_NO_ENGINE`
	- `PRISMA_CLIENT_NO_RETRY`
	- `PRISMA_MIGRATE_SKIP_GENERATE`
	- `PRISMA_MIGRATE_SKIP_SEED`

### MongoDB support

- Prisma ORM 7 does not support MongoDB yet; stay on Prisma ORM 6 if you need MongoDB.

## Upgrade Checklist (quick)

- Upgrade packages; confirm Node/TypeScript versions.
- Move to ESM (or adjust your runtime/build to consume ESM).
- Update `schema.prisma` generator to `provider = "prisma-client"` and set `output`.
- Run `pnpm prisma generate` and update Prisma Client imports to the generated output path.
- Add `prisma.config.ts` at repo root; move datasource config and load env explicitly.
- Update Prisma Client instantiation to use a driver adapter (unless using Accelerate).
- Update workflows: run `pnpm prisma generate` and `pnpm prisma db seed` explicitly.



