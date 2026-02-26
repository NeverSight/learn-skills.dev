---
name: better-env
description: Better environment variable management for agents and humans with full type safety, CLI-based remote environment synchronization, and environment validation. Use when setting up typed config schemas, validating env variables, or managing remote env vars across Vercel, Netlify, Railway, Cloudflare, and Fly.io with better-env.
---

## Work With better-env In A Repo

## Type-safe environment config modules

Follow this best practice to manage environment variables in TypeScript applications with full type safety and clear server/public boundaries.

`better-env` exports `configSchema` to define typed env modules and recommends placing them in feature-level `config.ts` files (for example `src/lib/auth/config.ts` and `src/lib/database/config.ts`).

Learn more:

- `references/config-schema.md`

## Validate existence of all env variables in the current environment

Run env validation early so missing or invalid values fail fast before `dev`, `build`, or deploy steps.

`better-env validate --environment <name>` loads `.env*` files with Next.js semantics, discovers `src/lib/*/config.ts` modules, and checks every declared variable from your `configSchema` modules.

If your dotenv files intentionally include keys that are not referenced by config modules, add per-env suppressions in `better-env.ts`:

`environments.<env>.ignoreUnused: string[]`

These suppress only the selected local environment during `validate`.
Adapter defaults are merged in automatically; for Vercel,
`VERCEL_OIDC_TOKEN` is ignored by default in `development`, `preview`, and `production`.

Learn more:

- `references/env-validation.md`

## Configure runtime syncing between local files and hosted providers

Use runtime configuration to keep local dotenv targets aligned with provider environments while preserving safe defaults.

Create `better-env.ts` with `defineBetterEnv(...)` and an adapter (`vercelAdapter`, `netlifyAdapter`, `railwayAdapter`, or `cloudflareAdapter`), then define environment mappings, env-file targets, and gitignore behavior.

Learn more:

- `references/config.md`
- `references/runtime.md`

## Use the CLI for day-to-day environment operations

The CLI gives a consistent workflow for initialization, sync, validation, and remote variable management, which is great for local development and CI automation.

Recommended flow in a repo:

1. Run `better-env init` once to verify adapter prerequisites.
2. Run `better-env pull --environment <name>` to sync local env files.
3. Run `better-env validate --environment <name>` before app startup/build.
4. Use `add`, `upsert`, `update`, `delete`, and `load` for remote env changes.

Choose command behavior intentionally:

- `upsert` for idempotent automation and scripts
- `add` when duplicate keys should fail
- `update` when missing keys should fail
- `delete` to remove remote keys
- `load` for batch updates from dotenv files

Learn more:

- `references/cli.md`
- `references/vercel-adapter.md`
