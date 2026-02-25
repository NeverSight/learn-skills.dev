---
name: bun-expert
description: >
  Expert guidance for JavaScript/TypeScript development with the Bun runtime.
  Covers project setup, package management, HTTP servers, built-in APIs,
  testing, bundling, and migration from Node.js. Use when starting Bun
  projects, using Bun APIs (Bun.serve, sql/SQL, s3, redis, Bun.$), migrating
  from Node.js, or troubleshooting Bun-specific behavior.
license: MIT
metadata:
  author: Andy Pai
  version: "1.1"
  upstream_skill: "https://bun.com/docs"
  tags: "bun javascript typescript runtime server bundler test"
---

# Bun Runtime Development Guide

This skill is intentionally grounded in official Bun documentation. Bun moves
quickly, so prefer current docs over hard-coded release timelines or benchmark
claims.

---

## Project Setup

### Initialize a new project

```bash
bun init                      # Interactive setup (package.json + tsconfig.json)
bun init -y                   # Accept defaults
bun create <template> <dir>   # Scaffold from a template
```

### TypeScript notes

- Bun runs TypeScript directly.
- `bun init` generates a compatible `tsconfig.json`.
- Add extra typing packages only when your editor/toolchain requires them.

---

## Package Management

### Essential commands

```bash
bun install
bun add <pkg>
bun add -d <pkg>
bun add -g <pkg>
bun remove <pkg>
bun update
bunx <pkg>
```

### Lockfile

- `bun.lock` is the default text lockfile format in modern Bun.
- `bun.lockb` remains supported for compatibility.
- Force text lockfile output:

```bash
bun install --save-text-lockfile
```

### Diagnostics and security

```bash
bun why <pkg>
bun audit
bun list
bun pm migrate
```

### Monorepo catalogs

Bun supports dependency catalogs in workspace roots:

```json
{
  "workspaces": {
    "packages": ["packages/*"],
    "catalog": {
      "react": "^19.0.0",
      "typescript": "^5.7.0"
    }
  }
}
```

Reference from packages:

```json
{
  "dependencies": {
    "react": "catalog:"
  }
}
```

---

## Running Code

```bash
bun index.ts
bun run start
bun --watch index.ts
bun --hot index.ts
```

### Environment variables

Bun auto-loads `.env` files. Order is:

1. `.env`
2. `.env.{NODE_ENV}` (`development`, `production`, `test`)
3. `.env.local`

```typescript
const apiKey = process.env.API_KEY;
const bunApiKey = Bun.env.API_KEY;
```

### HTML entrypoints (zero-config)

```bash
bun --hot index.html
bun --watch index.html
```

---

## HTTP Server

Bun supports route-based servers with `Bun.serve()`.

```typescript
Bun.serve({
  port: 3000,
  routes: {
    "/": new Response("Hello"),
    "/api/users/:id": (req) => Response.json({ id: req.params.id }),
    "/api/posts": {
      GET: () => Response.json({ posts: [] }),
      POST: async (req) => Response.json(await req.json(), { status: 201 }),
    },
  },
  fetch() {
    return new Response("Not Found", { status: 404 });
  },
});
```

---

## Built-in API Map

| Need | Bun API |
|---|---|
| HTTP server + WebSockets | `Bun.serve()` |
| SQL databases | `sql`, `SQL`, `Bun.sql`, `Bun.SQL` |
| S3-compatible storage | `s3`, `S3Client` |
| Redis | `redis`, `RedisClient` |
| Shell scripting | `Bun.$` / `$` |
| Local files | `Bun.file`, `Bun.write` |
| SQLite (embedded) | `bun:sqlite` |
| Password hashing | `Bun.password` |

---

## Testing and Bundling

### Test runner (`bun test`)

```bash
bun test
bun test --watch
bun test --test-name-pattern "auth"
bun test --bail
bun test --coverage
bun test --coverage-reporter text
```

### Bundling

```bash
bun build ./src/index.ts --outdir ./dist
bun build --target=bun ./src/server.ts --outfile ./dist/server.js
bun build --compile ./src/cli.ts --outfile ./dist/my-cli
```

---

## Node.js Migration Checklist

1. Install Bun and run `bun install`.
2. Keep existing Node APIs where they work; Bun is highly Node-compatible.
3. Replace tooling incrementally (`bun test`, `bun build`, `bun run`).
4. Adopt Bun-native APIs where they simplify code (`Bun.serve`, `sql`, `redis`, `s3`, `Bun.$`).
5. Run your full tests in CI on Bun before removing Node-specific fallbacks.

---

## Deep-Dive References

| Reference | Contents |
|-----------|----------|
| [references/builtin-apis.md](references/builtin-apis.md) | `Bun.serve`, SQL, S3, Redis, shell, filesystem, crypto/password utilities |
| [references/testing-and-bundling.md](references/testing-and-bundling.md) | `bun test` usage, mocking patterns, `bun build` CLI and API |
| [references/node-migration.md](references/node-migration.md) | Practical Node-to-Bun migration steps and compatibility guidance |

---

## Authoritative Docs

- https://bun.com/docs
- https://bun.com/docs/cli/test
- https://bun.com/docs/cli/pm
- https://bun.com/docs/runtime/http/routing
- https://bun.com/docs/runtime/env
- https://bun.com/docs/runtime/sql
- https://bun.com/docs/runtime/s3
- https://bun.com/docs/runtime/redis
- https://bun.com/docs/guides/ecosystem/migrate-from-nodejs
