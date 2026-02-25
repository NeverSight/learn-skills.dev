---
name: bun-runtime
description: |
  Bun JavaScript runtime, bundler, and package manager. Covers Bun.serve() HTTP server, Bun.file() I/O, SQLite, password hashing, Bun.build() bundler, bun:test runner, and package management.

  Use when building with Bun APIs, running scripts with Bun, bundling code, managing packages with bun install/add, or writing tests with bun:test.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://bun.sh/docs
user-invocable: false
---

# Bun Runtime

## Overview

Bun is an all-in-one JavaScript and TypeScript runtime that includes a fast package manager, bundler, test runner, and Node.js-compatible APIs. It natively executes TypeScript and JSX without a separate compilation step.

**When to use:** Fast server-side JavaScript, TypeScript-first projects, replacing Node.js for better startup performance, built-in SQLite, password hashing, file I/O, HTTP servers, bundling, and testing without external tooling.

**When NOT to use:** Projects requiring full Node.js ecosystem compatibility (some native modules unsupported), production environments needing battle-tested stability of Node.js, or browser-only code that does not need a runtime.

## Quick Reference

| Pattern          | API                                       | Key Points                                               |
| ---------------- | ----------------------------------------- | -------------------------------------------------------- |
| HTTP server      | `Bun.serve({ routes, fetch })`            | Route-based, static/dynamic routes, per-method handlers  |
| File read        | `Bun.file(path)`                          | Lazy BunFile (Blob), `.text()`, `.json()`, `.stream()`   |
| File write       | `Bun.write(dest, data)`                   | Accepts string, Blob, Response, BunFile                  |
| SQLite           | `new Database(path)` from `bun:sqlite`    | Synchronous queries, prepared statements, WAL mode       |
| Password hash    | `Bun.password.hash(pw)`                   | Argon2id default, bcrypt option, async and sync variants |
| Password verify  | `Bun.password.verify(pw, hash)`           | Auto-detects algorithm from hash format                  |
| Bundler          | `Bun.build({ entrypoints, outdir })`      | Tree-shaking, code splitting, plugins, multiple targets  |
| Test runner      | `import { test, expect } from "bun:test"` | Jest-compatible, mocking, snapshots, watch mode          |
| Install packages | `bun install`                             | Fast lockfile resolution, npm-compatible                 |
| Add package      | `bun add <pkg>`                           | `-d` for dev, `-g` for global                            |
| Run script       | `bun run <script>`                        | Runs package.json scripts or files directly              |
| Execute binary   | `bunx <pkg>`                              | Like npx, runs without installing                        |
| S3 client        | `new S3Client(opts)` / `s3.file(key)`     | Built-in S3-compatible storage client                    |
| HTML imports     | `import page from './index.html'`         | Fullstack: import HTML as route handler                  |

## Common Mistakes

| Mistake                                               | Correct Pattern                                                                   |
| ----------------------------------------------------- | --------------------------------------------------------------------------------- |
| Using `fetch` handler only without `routes`           | Use `routes` object for static/dynamic routing (Bun v1.2.3+), `fetch` as fallback |
| Forgetting `await` on `Bun.write()`                   | `Bun.write()` is async, always await it                                           |
| Using `Bun.file(path).text()` without `await`         | `.text()`, `.json()`, `.arrayBuffer()` all return Promises                        |
| Creating SQLite database without WAL mode             | Enable WAL for concurrent reads: `db.exec("PRAGMA journal_mode = WAL")`           |
| Using `bun install` without `--frozen-lockfile` in CI | Use `bun install --frozen-lockfile` for reproducible CI builds                    |
| Importing `jest` globals in Bun tests                 | Import from `bun:test`, not `@jest/globals` or `vitest`                           |
| Using `node_modules/.bin/` directly                   | Use `bunx` or `bun run` instead of referencing bin paths                          |
| Expecting `Bun.build()` to throw on failure           | Check `result.success` boolean, errors are in `result.logs`                       |
| Using `--target node` when deploying to Bun           | Use `--target bun` for Bun-specific optimizations and bytecode                    |
| Synchronous password hashing in request handlers      | Use `await Bun.password.hash()` async variant in servers                          |

## Delegation

- **Project scaffolding**: Use `Explore` agent
- **Performance profiling**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `typescript-patterns` skill is available, delegate advanced TypeScript typing questions to it.

## References

- [Runtime APIs: Bun.serve(), Bun.file(), SQLite, password hashing, and utilities](references/runtime-apis.md)
- [Package management: install, add, remove, workspaces, lockfile](references/package-management.md)
- [Bundler: Bun.build(), entrypoints, plugins, tree-shaking](references/bundler.md)
- [Testing: bun:test, assertions, mocking, snapshots, lifecycle hooks](references/testing.md)
