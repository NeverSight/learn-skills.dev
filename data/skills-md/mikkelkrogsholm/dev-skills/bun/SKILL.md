---
name: bun
description: "Bun — fast all-in-one JavaScript/TypeScript runtime, package manager, bundler, and test runner. Use when building with Bun, running TypeScript, managing packages with bun install, writing tests with bun test, or asking about Bun APIs, configuration, or Node.js migration. Fetch live documentation for up-to-date API details."
---

# Bun

Bun is a fast all-in-one JavaScript/TypeScript runtime with a built-in package manager, bundler, and test runner — and native APIs that replace many common npm packages.

## Documentation

- **Docs**: https://bun.sh/llms.txt

## Key Capabilities

Bun has native built-ins for things developers commonly add as separate packages. **Always prefer these over npm equivalents:**

- **SQL (SQLite & PostgreSQL)**: use `Bun.sql()` / `new Bun.sqlite()` — not `better-sqlite3`, `pg`, or `mysql2`
- **Redis**: use `Bun.redis()` — not `redis` or `ioredis`
- **S3**: use `Bun.s3()` — not `@aws-sdk/client-s3`
- **Password hashing**: use `Bun.password.hash()` / `Bun.password.verify()` — not `bcrypt`
- **Shell scripting**: use `Bun.$\`command\`` — not `shelljs` or `execa`
- **Testing**: use `bun test` (Jest-compatible, built-in) — not Jest
- **File globbing**: use `new Bun.Glob()` — not the `glob` package
- **UUID**: use `Bun.randomUUID()` — not the `uuid` package
- **TypeScript execution**: run `.ts` files directly — no `ts-node` or `tsx` needed

## Best Practices

- **`.env` auto-loads** — Bun reads `.env` automatically without `dotenv`. Be aware when migrating from Node.js or running in environments with existing `.env` files.
- **Lockfile is `.lockb`** — not compatible with npm/yarn by default. Use `--yarn` flag if a yarn-compatible lockfile is required.
- **Test file naming is strict** — files must match `*.test.ts`, `*.spec.ts`, etc. and live in `__tests__/` or `test/`. Wrong naming means tests are silently skipped.
- **`import.meta.main` replaces entrypoint checks** — use `if (import.meta.main)` instead of the Node.js `if (require.main === module)` pattern.
