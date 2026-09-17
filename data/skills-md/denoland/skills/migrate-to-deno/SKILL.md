---
name: migrate-to-deno
description: Use when moving a Node.js, npm, Yarn, pnpm, or Bun project to Deno, or when adopting Deno incrementally in an existing JavaScript or TypeScript codebase. Covers using Deno as a drop-in package manager, running existing package.json scripts, CommonJS versus ESM, node_modules layout, lockfile migration, permissions, whether to adopt the built-in toolchain, and per-tool command equivalents.
license: MIT
metadata:
  author: denoland
  version: "1.0"
---

# Migrating to Deno

Requires Deno 2.9 or later. For general Deno usage once migrated, see the `deno`
skill.

## Most Node projects already run under Deno

Deno reads an existing `package.json`, resolves the same npm packages, writes a
real `node_modules`, runs the same scripts, and supports `node:` built-ins.
TypeScript runs with no build step.

There is usually **no code to change** — only which binary you invoke. Don't
start by rewriting imports to `jsr:`, swapping dependencies for Deno-specific
ones, or restructuring directories. Proposing that is the most common way this
goes wrong.

## Migrate in rungs

Each rung is independently useful and reversible. Stop wherever suits the
project; plenty of teams stop at rung 1.

### Rung 1 — Deno as the package manager only

```bash
deno install
```

Reads `package.json`, resolves the same dependencies, writes `node_modules`, and
creates `deno.lock` — seeded from any existing `package-lock.json`, `yarn.lock`,
`bun.lock`, or pnpm lockfile, so pins and integrity hashes carry over instead of
drifting.

The app still runs under `node`; teammates are unaffected. Commit `deno.lock`
once verified. **To back out:** delete `deno.lock` and `node_modules`, then
`npm install`.

### Rung 2 — Run it with Deno

```bash
deno run -A main.js      # or: deno -A main.js
deno task build          # runs scripts.build from package.json
```

Use `-A` here. The goal is confirming the program works, not designing a
permission policy — changing both at once makes failures ambiguous.

### Rung 3 — Tighten permissions

Replace `-A` with the narrowest set that works: run it, read what it asks for,
grant exactly that.

```bash
deno run --allow-net=api.example.com --allow-read=./config --allow-env=PORT main.js
```

This buys something Node cannot offer, and is worth doing before deploying.

### Rung 4 — Optionally, adopt the built-in toolchain

`deno fmt` for prettier, `deno lint` for eslint, `deno test` for jest or vitest,
`deno check` for tsc, `deno watch` for nodemon, `deno compile` for pkg.

**Optional, and usually not worth it for an existing project.** These are not
drop-in replacements; parity is incomplete, so this is a real migration, not a
config change. A project happy with prettier, eslint, and vitest should keep
them and use Deno as runtime and package manager only. Prefer the built-in tools
for new projects. If you do move an existing one, go a tool at a time.

## Command equivalents

| Task          | npm                 | Yarn                        | pnpm                       | Bun                             | Deno              |
| ------------- | ------------------- | --------------------------- | -------------------------- | ------------------------------- | ----------------- |
| Install all   | `npm install`       | `yarn install`              | `pnpm install`             | `bun install`                   | `deno install`    |
| Add           | `npm i <p>`         | `yarn add <p>`              | `pnpm add <p>`             | `bun add <p>`                   | `deno add <p>`    |
| Add dev       | `npm i -D <p>`      | `yarn add -D <p>`           | `pnpm add -D <p>`          | `bun add -d <p>`                | `deno add -D <p>` |
| Remove        | `npm uninstall <p>` | `yarn remove <p>`           | `pnpm remove <p>`          | `bun remove <p>`                | `deno remove <p>` |
| CI install    | `npm ci`            | `yarn install --immutable`† | `pnpm i --frozen-lockfile` | `bun install --frozen-lockfile` | `deno ci`         |
| Run script    | `npm run <s>`       | `yarn <s>`                  | `pnpm <s>`                 | `bun run <s>`                   | `deno task <s>`   |
| Run binary    | `npx <p>`           | `yarn dlx <p>`              | `pnpm dlx <p>`             | `bunx <p>`                      | `dx <p>`          |
| Outdated      | `npm outdated`      | `yarn outdated`‡            | `pnpm outdated`            | `bun outdated`                  | `deno outdated`   |
| Audit         | `npm audit`         | `yarn npm audit`†           | `pnpm audit`               | `bun audit`                     | `deno audit`      |
| Why           | `npm ls <p>`        | `yarn why <p>`              | `pnpm why <p>`             | `bun why <p>`                   | `deno why <p>`    |
| Run a file    | `node f.js`         |                             |                            | `bun f.ts`                      | `deno f.ts`       |
| Run TS        | `ts-node f.ts`      |                             |                            | `bun f.ts`                      | `deno f.ts`       |
| Watch         | `nodemon f.js`      |                             |                            | `bun --watch f.ts`              | `deno watch f.ts` |
| Format        | prettier            |                             |                            | prettier                        | `deno fmt`        |
| Lint          | eslint              |                             |                            |                                 | `deno lint`       |
| Test          | jest, vitest        |                             |                            | `bun test`                      | `deno test`       |
| Coverage      | nyc, c8             |                             |                            |                                 | `deno coverage`   |
| Type-check    | `tsc --noEmit`      |                             |                            | `tsc`                           | `deno check`      |
| Bundle binary | pkg, nexe           |                             |                            | `bun build --compile`           | `deno compile`    |

† Yarn Berry (v2+) spelling. Yarn Classic (v1) uses
`yarn install --frozen-lockfile` and `yarn audit`.

‡ Yarn Classic only — Berry removed `yarn outdated`.

`dx` is a separate binary installed alongside Deno, and an alias for `deno x`.
It does not appear in the top-level `deno --help` output. Like `npx`, it runs
the package with the sandbox disabled.

## The four things that actually break

### `Requires net access to "..."` (or read, env, run)

Deno grants nothing by default. Add that specific permission, or `-A` while
still establishing the program works at all.

### `ReferenceError: require is not defined`

A file containing CommonJS is being parsed as ESM. `.cjs` is always CommonJS,
`.mjs` always ESM; `.js` and `.ts` follow `"type"` in the nearest
`package.json`. For a CommonJS project, set `"type": "commonjs"`.

### A dependency is broken, or `postinstall` never ran

Lifecycle scripts don't run by default. Native addons notice immediately.
Approvals are recorded in the config file, so this is one-time:

```bash
deno approve-scripts                              # interactive picker
deno install --allow-scripts=npm:better-sqlite3   # or name them directly
```

### A tool cannot find files inside `node_modules`

Deno's layout is pnpm-style: real files in `node_modules/.deno/`, exposed via
symlinks. Tools assuming npm's flat hoisted tree need:

```json
{ "nodeModulesLinker": "hoisted" }
```

## What has no Deno equivalent

Say so rather than improvising a workaround that won't hold:

- **Yarn Plug'n'Play.** Deno creates a real `node_modules`; `.pnp.cjs` is unused
  and `.yarnrc.yml` resolver settings don't transfer.
- **`yarn patch` / pnpm patched dependencies.** Vendor or fork.
- **`overrides` / `resolutions`.** Pin via an import map entry instead.
- **Registry and resolver tuning** in `.npmrc` / `.yarnrc.yml`.
- **Bun build features** — macros, HTMLRewriter, HTML entrypoints.

## Per-tool details

- `references/FROM_NPM.md` — lockfile seeding, `node_modules` layout, overrides
- `references/FROM_YARN.md` — Plug'n'Play, Berry vs Classic, workspaces
- `references/FROM_PNPM.md` — `pnpm-workspace.yaml`, `catalog:`, patches
- `references/FROM_BUN.md` — Bun API translation, `bunfig.toml`
- `references/NODE_APIS.md` — `node:` built-ins, `DENO_COMPAT`, CJS/ESM

## Further reading

- <https://docs.deno.com/runtime/migrate/> — official migration guides
- <https://docs.deno.com/runtime/fundamentals/node/> — Node and npm
  compatibility
- <https://docs.deno.com/runtime/reference/node_apis/> — per-module Node API
  status
