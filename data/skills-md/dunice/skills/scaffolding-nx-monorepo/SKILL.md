---
name: scaffolding-nx-monorepo
description: Use when starting a new full-stack TypeScript repository from nothing — an Nx monorepo with NestJS, Drizzle + Postgres, React, tRPC, Vitest, Biome, pnpm, Docker, husky hooks, GitHub Actions and an agent harness that scores harness-score L4.
---

# Scaffolding an Nx full-stack monorepo

A repository built to this recipe has **one root `package.json`**, exact dependency versions, Nx-cached targets, affected-only git hooks, two compose files, and an agent harness under `.agents/` that both Claude Code and Cursor read through symlinks.

**Build it by hand. Do not run `create-nx-workspace`.** Every generator on this stack emits per-project manifests, ESLint + Prettier, and Jest — the three things this layout deliberately does not have. Undoing a generator costs more than writing the eleven config files yourself.

Rules still get asked for in ESLint's vocabulary — `curly`, `max-params`, `object-curly-newline`. That is a naming problem, not a tooling one: `references/lint-rules.md` maps each ESLint rule name onto the Biome rule or plugin that carries it here, and says plainly which have no equivalent. Adding ESLint to satisfy the phrasing breaks property 5 and gives the repo two linters to keep in agreement.

## The contract

The finished repository has exactly these properties. Check each one before calling the scaffold done.

| # | Property | How to verify |
|---|---|---|
| 1 | One `package.json`, at the root | `find . -name package.json -not -path '*/node_modules/*'` returns 1 line |
| 2 | Every version exact — no `^`, no `~` | `grep -E '"[~^][0-9]' package.json` returns nothing |
| 3 | pnpm only | `pnpm-lock.yaml` exists; no `package-lock.json`, no `yarn.lock` |
| 4 | Node pinned | `.nvmrc` holds a bare version; `engines.node` agrees |
| 5 | Biome only | no `.eslintrc*`, no `.prettierrc*`, no `eslint`/`prettier` in the manifest |
| 6 | Code-shape rules enforced | a 3-deep `if`, a 51-line function, a 1001-line file, a `const ab`, a stray `console.log`, an unbraced `if`, a four-parameter function and a two-property object on one line each fail `pnpm check` |
| 7 | Cross-project imports via subpath imports | `grep -r "\.\./\.\./packages" apps/` returns nothing |
| 8 | Named migrations | every file matches `migrations/NNNN_<snake_case>.sql` |
| 9 | Bind-mounted data under `.data/<service>/` | `compose.yml` has no top-level `volumes:` block |
| 10 | Hooks are affected-only | `.husky/*` calls `nx affected`, never `run-many`, when a base ref exists |
| 11 | Harness under `.agents/`, tools symlink in | `.claude/skills` and `CLAUDE.md` are symlinks; `.cursor/` holds only `hooks.json` |
| 12 | Harness scores L4 | `npx --yes harness-score@1.6.3 . --min-level 4` exits 0 |
| 13 | Every rule visible in the editor | `.vscode/extensions.json` recommends the Biome extension, `.vscode/settings.json` is committed, and nothing is enforced outside Biome |

## Build order

Each step depends on the one before it. Do not reorder.

1. **Preflight.** Resolve the current Node LTS and pnpm major, write `.nvmrc`, `corepack enable`, set `packageManager` and `engines`.
2. **Root manifest.** `type: module`, `private: true`, the `imports` subpath map, the script table. See `references/repo-layout.md`.
3. **Install.** Resolve the latest version of every dependency at build time and pin it: `pnpm add --save-exact <pkg>`. Never copy version numbers out of this skill — they are a snapshot, not a target.
4. **TypeScript.** `tsconfig.base.json` at the root, one `tsconfig.json` per project for the build, one `tsconfig.typecheck.json` where typecheck needs a wider include than the build.
5. **Nx.** `nx.json` with `namedInputs`, `targetDefaults` (`dependsOn: ["^build"]` on build/typecheck/test), and `defaultBase: origin/main`. One `project.json` per project, all targets `nx:run-commands`.
6. **Projects, in dependency order:** `contracts` → `db` → `api` → `web`. Dependency direction is one-way and enforced by `implicitDependencies`.
7. **Vitest.** One root `vitest.config.ts` declaring every project. `globals: false`.
8. **Biome.** One `biome.json`; `vcs.useIgnoreFile: true`; ignore `dist`, `coverage`, `.nx`, the lockfile, and the generated migrations. Then the `**/*.ts` + `**/*.tsx` override carrying the code-shape rules — type-only imports first, then grouped and sorted value imports, 1000 lines per file, 50 lines per function, braces on every branch, 3 parameters before an options object — plus two GritQL plugins, one capping if/else nesting at 2 and one keeping multi-property object literals off a single line. It must come **before** the `apps/api/**` override, which switches `useImportType` back off for Nest DI. See `references/lint-rules.md`.
9. **Docker.** `compose.yml` (bind mounts under `.data/`) and `compose.test.yml` (shifted ports, tmpfs). See `references/infra-and-ci.md`.
10. **Hooks and CI.** husky + lint-staged, then the two workflows.
11. **Harness.** `.agents/` tree, then the symlinks, then the two hook scripts under `scripts/`. See `references/harness-and-hooks.md`.
12. **Verify.** `pnpm check`, `pnpm typecheck`, `pnpm test`, `pnpm build`, then `pnpm harness:score`. Report real output.

## The traps

These cost hours each. All of them are silent — nothing errors, the result is just wrong.

| Trap | Symptom | Fix |
|---|---|---|
| Nx loads root `.env` into every task | `web` build ships React's **development** bundle, no warning | Pin `"env": { "NODE_ENV": "production" }` on the web `build` target |
| esbuild drops `design:paramtypes` | Nest constructor injection returns `undefined` in Vitest only | Run the api Vitest project through `unplugin-swc` |
| `pnpm add` writes `^` by default | Version drift between machines | `pnpm add --save-exact`, and add `save-exact=true` to `.npmrc` |
| drizzle-kit auto-titles migrations | `0000_curious_wolverine.sql` | Only ever generate through `pnpm db:generate <snake_case_name>` (`drizzle-kit generate --name`) |
| Subpath imports point at `dist/` | Cross-project change invisible until rebuilt | `dependsOn: ["^build"]` on every consuming target |
| Cursor auto-detects `.agents/` | Duplicate skills if `.cursor/skills/` also exists | `.cursor/` holds `hooks.json` and nothing else |
| Postgres 18 moved the data directory | Bind mount silently empty | Mount `/var/lib/postgresql`, not `/var/lib/postgresql/data` |
| `nx affected` with no base ref | Hook explodes on the first commit | Guard with `git rev-parse --verify --quiet` and fall back to `run-many` |
| Biome shape rules default to `info` | `noExcessiveLinesPerFile` / `PerFunction` print but never fail a hook or CI | Pin `"level": "error"` on each one |
| `null` as an import-group separator | Config schema advertises it; the runtime rejects it and Biome refuses to start | Use the `":BLANK_LINE:"` string instead |
| Biome's GritQL vocabulary is narrow | `statement_block()` and the `alternative` field fail to compile; the plugin silently loads with no matches | Match with backtick snippets (`` `if ($_) { $body }` ``), and probe a new pattern against a fixture before trusting it |
| GritQL cannot localise whitespace between siblings | A plugin that checks the gap between two statements compiles, matches, and flags the wrong one | A statement node carries no trivia and a list-wide regex cannot be tied to the pair — the rule is not expressible; don't ship the plugin |
| A lint script added to `package.json` only | `nx affected -t lint` and the pre-push hook never run it | Append it to every `project.json` `lint` target as well |

## Latest-version policy

"Latest" is resolved **when you scaffold**, not when this skill was written. For each of node, pnpm, nx, nest, react, vite, vitest, biome, drizzle-orm, drizzle-kit, trpc, zod, typescript, and the postgres and redis images: look up the current release, then pin it exactly. Two follow-ons:

- A brand-new Nx release ships its native binaries the same day, which trips pnpm's `minimumReleaseAge` gate. Exclude those specifiers in `pnpm-workspace.yaml` rather than lowering the gate globally.
- `pnpm-workspace.yaml` still belongs in a single-package repo — it carries the install policy (`dangerouslyAllowAllBuilds: false` plus an `allowBuilds` allowlist) even with no workspace members.

## Editor integration

Scaffold it in the same pass as the lint rules, not later. A rule that only fires at commit time gets discovered by the person least able to fix it cheaply.

- `.vscode/extensions.json` — recommend the Biome extension, and list the ESLint and Prettier extensions under `unwantedRecommendations`. Both are installed on most machines and both will fight Biome.
- `.vscode/settings.json` — **commit it.** Biome as `editor.defaultFormatter` for every language it owns, `source.fixAll.biome` and `source.organizeImports.biome` in `codeActionsOnSave`, `prettier.enable: false`, `eslint.enable: false`, and `typescript.tsdk` pointed at the pinned workspace TypeScript. The usual `.gitignore` line is `.vscode/*` plus a negation per file worth sharing.
- Never put `quickfix.biome` in `codeActionsOnSave` — Biome's own `suspicious/noQuickfixBiome` rule flags it, because it applies every rule's fix atomically and can emit invalid code. Use `source.fixAll.biome`.
- Cursor does not inherit VS Code's installed extensions. A repo whose diagnostics "do not show up" is usually a Cursor session with no Biome extension.
- GritQL plugin diagnostics do reach the editor — they arrive over the LSP as `biome/plugin`. Nothing extra to configure.
- Keep every rule inside Biome if you possibly can. A rule enforced by a **script** needs its own TypeScript language-service plugin to be visible in the editor at all, and the directory shape that plugin demands is forced by tsserver's resolver and is not guessable. `references/lint-rules.md` has the full recipe under "When a rule needs a script", along with the reason this scaffold ships none.

## Frontend styling

Impeccable (<https://impeccable.style/>) is an installable agent skill, not a CSS framework. Install it into `.agents/skills/` so both tools pick it up, give it a `DESIGN.md`, and let it own the visual pass. Without it, hand-write one `styles.css` of design tokens — colour, space, type, radius, measure — and let every component resolve to a token. No ad-hoc values in component styles.

## QA the running app

Vitest proves the units; it cannot tell you the page rendered or that an endpoint returns what its types claim. Two surfaces, one recipe.

`agent-browser` (<https://github.com/vercel-labs/agent-browser>) is a native CLI that drives Chrome over CDP from the terminal, so an agent can open the web app, snapshot the accessibility tree, click a ref, and read the console back. Install it globally — `pnpm add -g agent-browser && agent-browser install` — never as a repo dependency; it is a machine tool the repo does not import, and adding it would put a native binary under the exact-version contract. The API side needs nothing but `curl`. See `references/agent-browser.md`.

Scaffold four harness pieces for this, in `.agents/`:

| Piece | What it holds |
|---|---|
| `skills/browser-testing/` | the snapshot/ref loop, session isolation, the states worth exercising, teardown |
| `skills/cli-testing/` | your API's real wire format and error envelope, one probe per contract rule, teardown |
| `agents/qa-engineer.md` | a subagent that picks a surface, follows the skill, and returns ranked findings |
| `workflows/qa.md` | the `/qa` slash command that dispatches it |

**The subagent is justified by context economics, not by role-play.** A thorough pass emits accessibility trees, network logs, console dumps and dozens of probe responses whose only valuable residue is "these four things are broken" — heavy output in, compact verdict out. That is the same argument that earns a `code-reviewer` its place. An agent that merely runs `pnpm test` is not worth one; that belongs in `verify-changes`.

Two rules that make the findings trustworthy, and both belong in writing:

- **Confirmed vs Suspected.** Confirmed means reproduced this run; Suspected means read in the source. A prediction is Suspected however confident it is. Without this split, static reads get filed as bugs and someone burns an afternoon.
- **Teardown is a required step, not a closing remark.** A pass that seeds rows leaves the dev database dirty for everyone after it. Seed behind a marker so cleanup is one predicate, and match it case-insensitively if the column has no case-folding index.

Keep all of it out of `verify-changes` and the git hooks. Those stay affected-only and fast; a QA pass takes minutes and needs a running stack, so it is deliberately invoked.

**Write these skills against your own running stack, not from memory.** Framework documentation describes the default configuration, and yours will differ — mounting tRPC with `app.use()` puts it outside a Nest global prefix, and an API with no transformer has a flatter error envelope than the docs show. Boot the stack, probe it, and paste what came back.

## References

- `references/repo-layout.md` — tree, root manifest, `nx.json`, tsconfigs, `project.json` per project, vitest, biome
- `references/lint-rules.md` — every lint rule with examples, the full `biome.json`, the GritQL plugin, and how to verify each rule is live
- `references/harness-and-hooks.md` — `.agents/` layout, symlinks, the two shared hook scripts, harness-score L4
- `references/infra-and-ci.md` — both compose files, `.env.example`, husky, the two workflows
- `references/agent-browser.md` — driving a real browser from the terminal to verify the web app: install, the snapshot/ref loop, sessions and auth, and how to wire it into the harness

The editor wiring lives in `references/lint-rules.md` alongside the rules it surfaces, since the two are decided together.

The QA skills themselves are repo-specific — they carry your routes, your envelope and your teardown predicate — so they are written per repository rather than copied from here.

## Red flags

- You typed `npx create-nx-workspace` → stop, delete, hand-build.
- A second `package.json` appeared under `apps/` → delete it, move the dep to root.
- Both `pnpm-lock.yaml` and `package-lock.json` exist → the tree is forked; drop `node_modules` and `package-lock.json`, reinstall with pnpm.
- A migration filename has an adjective in it → regenerate with `--name`.
- `.claude/skills/` is a real directory → it must be a symlink to `../.agents/skills`.
- You reported "scaffold complete" without pasting `harness:score` output → not complete.
