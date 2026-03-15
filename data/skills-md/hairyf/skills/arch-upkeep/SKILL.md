---
name: arch-upkeep
description: Architecture health-check and upgrade orchestrator. Use to detect a repo’s current shape (lib/cli/monorepo/webext/vscode/...) and migrate it onto the canonical tsdown-based starter architectures.
metadata:
  author: hairy
  version: "2026.2.24"
  source: Internal architecture upkeep workflow, composed from existing arch-* skills (arch-unplugin, arch-tsdown-monorepo, arch-tsdown-cli, arch-tsdown, arch-webext-vue, arch-vscode)
---

# arch-upkeep

`arch-upkeep` is a **meta architecture skill** for keeping existing projects aligned with the canonical starter stacks:

- `arch-tsdown-monorepo` — pnpm monorepo for TS libs with tsdown per package
- `arch-tsdown` — single-package TS library with tsdown
- `arch-tsdown-cli` — CLI apps built on tsdown
- `arch-unplugin` — libraries built as unplugin (Vite/Rollup/Webpack/ESBuild)
- `arch-webext-vue` — browser extensions using Vue
- `arch-vscode` — VS Code extensions

Use this skill when a project already exists and you want to:

- **Identify** what architecture it currently matches (lib / CLI / monorepo / webext / vscode / unplugin / mixed)
- **Plan** a migration to one of the canonical `arch-*` starters
- **Incrementally upgrade** tooling, scripts, and CI without rewriting app logic

> This skill does not re-specify each architecture in detail — it helps you pick **which arch-skill** to apply and in what order.

## Quick start

1. **Classify the repo** using the checks in **1. Detect current architecture**.  
2. **Map to target skills** using **2. Choose the target architecture skill(s)**.  
3. **Ensure required `arch-*` skills are installed** via **2.1 Check & install required skills**.  
4. **Plan incremental migration** using **3. Migration strategy (incremental)** and **4. Architecture-specific notes**.  
5. **Run an upkeep pass** with the checklist in **5. Checklist: running an “arch upkeep” on a repo**.

## 1. Detect current architecture

Start by classifying the repo. Use these quick heuristics (you can apply multiple, projects may be “monorepo + CLI” etc.):

- **Monorepo (`arch-tsdown-monorepo` candidate)**  
  - Has `pnpm-workspace.yaml` or `packages/*`, `apps/*`, or similar layout  
  - Multiple `package.json` files under `packages/` or `apps/`  
  - Shared tooling at root (`eslint.config.*`, `vitest.config.*`, `tsconfig.base.json`, etc.)

- **Single TS library (`arch-tsdown` candidate)**  
  - Single `package.json` at root  
  - Library-style exports (`main`, `module`, `types`, maybe `exports`)  
  - No `bin` entrypoint, no browser manifest, no VS Code extension manifest

- **CLI (`arch-tsdown-cli` candidate)**  
  - Root `package.json` with `"bin"` or `"package.json#exports"` pointing to CLI entry  
  - Uses `#!/usr/bin/env node` in entry file  
  - Often depends on `cac`, `commander`, `yargs`, etc.

- **unplugin-based library (`arch-unplugin` candidate)**  
  - Depends on `unplugin`  
  - Exports `createUnplugin`, or has files under `src/core/`, `src/vite.ts`, `src/webpack.ts`, etc.  
  - Targets bundlers (Vite/Rollup/Webpack/ESBuild)

- **Browser extension + Vue (`arch-webext-vue` candidate)**  
  - Has `manifest.json`/`manifest.v3.json` (Chrome/Firefox extension)  
  - Vue SPA for popup/options or content scripts  
  - Build tooling around web extension dev (`web-ext`, `wxt`, or custom scripts)

- **VS Code extension (`arch-vscode` candidate)**  
  - Has `package.json` with `"contributes"`, `"activationEvents"`, `"engines.vscode"`  
  - `src/extension.ts` or similar activation entry  

Once you know what it “mostly is”, pick **one primary architecture** as the upgrade target. If the repo is mixed (e.g. monorepo with a CLI package), pair `arch-tsdown-monorepo` with the relevant per-package skill (`arch-tsdown`, `arch-tsdown-cli`, etc.).

## 2. Choose the target architecture skill(s)

Map your classification to the canonical skills:

- **pnpm multi-package repo** → start with `arch-tsdown-monorepo`  
- **Single TS library** → `arch-tsdown`  
- **CLI** (single or inside a monorepo package) → `arch-tsdown-cli`  
- **unplugin** lib → `arch-unplugin` (often inside an `arch-tsdown` or monorepo setup)  
- **Browser extension + Vue** → `arch-webext-vue` (app layer) plus `arch-tsdown` for any shared libs  
- **VS Code extension** → `arch-vscode` (extension app) plus `arch-tsdown` for shared libs

Then:

1. **Open the corresponding `arch-*` skill(s)**.  
2. **Use their “overview” / “core” references** as the target design you want your existing repo to converge to.  
3. Plan an incremental migration: configs and scripts first, CI next, then release automation.

### 2.1 Check & install required skills

Because `arch-upkeep` is only an orchestrator, it expects the concrete `arch-*` skills to be **installed and usable** in the agent environment.

Recommended flow:

1. **List installed skills** in your agent runtime  
   - Use your platform’s “list skills” command / UI (for example, look for `arch-tsdown-monorepo`, `arch-tsdown`, `arch-tsdown-cli`, `arch-unplugin`, `arch-webext-vue`, `arch-vscode`).  
   - If a target architecture skill is already present, you can call it directly.

2. **If a required skill is missing, install it by name**  
   - From the Agent Skills catalog (or your platform’s marketplace), search for the exact name, e.g. `arch-tsdown-monorepo`.  
   - Install it into the current agent profile / workspace.  

3. **Verify installation before proceeding**  
   - Re-run the “list skills” view and confirm the skill appears and is enabled.  
   - Optionally open its `SKILL.md` (or skill details in UI) to confirm version and scope.

4. **Compose multiple skills in one upkeep session**
   - For **monorepo + CLI**: use `arch-tsdown-monorepo` + `arch-tsdown-cli` on the CLI package, and `arch-tsdown` for shared libs.  
   - For **VS Code extension with shared libs**: use `arch-vscode` for the extension host + `arch-tsdown` for shared modules.  
   - For **web extension + shared TS libs**: use `arch-webext-vue` for the extension app + `arch-tsdown` for the reusable packages.  

Only after the relevant skills are installed and verified should you start applying the migration steps below.

## 3. Migration strategy (incremental)

General principles:

- **Do not rewrite app logic.** Only swap out **infrastructure** (build, test, lint, CI, release).
- **One layer at a time.** Avoid changing bundler, test runner, and tsconfig all in a single PR if you can split it.
- **Keep Git history readable.** Separate commits for “tooling move” vs “code fixes”.

Recommended order:

1. **Normalize package layout**
   - For monorepos: align `packages/*` layout, root `package.json`, workspace ranges, pnpm catalogs as per `arch-tsdown-monorepo`.
   - For single packages: align folder structure (`src/`, `dist/`, `tests/`), tsconfig names, etc. with `arch-tsdown`.

2. **Migrate build to tsdown (where applicable)**
   - Replace legacy build scripts (`tsc`, `rollup`, `tsup`, etc.) with `tsdown` configs from the target skill.
   - Ensure `package.json#exports`, `main/module/types`, and `files` fields match the target pattern.

3. **Align testing and linting**
   - Move to the recommended test runner (Vitest) and ESLint setup from the relevant arch skill.
   - For monorepos, centralize configs at root with per-package overrides where needed.

4. **Synchronize scripts**
   - Standardize on the script names from the target architecture (`build`, `dev`, `test`, `lint`, `typecheck`, `release`, etc.).
   - For monorepos, prefer root scripts using `pnpm -r` or `pnpm --filter`.

5. **Upgrade CI and release**
   - Adopt the GitHub Actions / release workflows from the relevant arch skills.  
   - If applicable, migrate to **npm Trusted Publisher**, tag-based release, and `bumpp` or similar.

6. **Clean up**
   - Remove obsolete configs, scripts, and unused devDependencies once the new pipeline is green.

## 4. Architecture-specific notes

- **When targeting `arch-tsdown-monorepo`:**
  - Centralize tooling (ESLint, Vitest, TS base config) at root.
  - Convert cross-package dependencies to `workspace:*` ranges.
  - Make each package buildable with tsdown independently.

- **When targeting `arch-tsdown` or `arch-tsdown-cli`:**
  - Treat the package as a canonical TS library/CLI; keep `src/` clean and side-effect free where possible.
  - Ensure binary entrypoints are small bootstrap files that import from internal modules.

- **When targeting `arch-unplugin`:**
  - Keep the unplugin core small and composable.
  - Provide clear exports for different bundlers (Vite, Rollup, Webpack, ESBuild) via the unified unplugin API.

- **When targeting `arch-webext-vue`:**
  - Separate app UI (Vue) from background/service worker logic and shared utilities.
  - Prefer shared TS libs (using `arch-tsdown`) for logic that can be reused outside the extension.

- **When targeting `arch-vscode`:**
  - Keep the extension host code (activation, commands) thin.
  - Move heavy logic to shared TS libs where possible.

## 5. Checklist: running an “arch upkeep” on a repo

Use this as a repeatable workflow:

1. **Classify architecture** (monorepo / lib / CLI / unplugin / webext / vscode).  
2. **Pick the primary `arch-*` skill(s)** that match the desired end state.  
3. **Read their overview/core references** and write down the target structure and scripts.  
4. **Plan incremental steps** (layout → build → test/lint → CI → release).  
5. **Apply changes** while keeping app logic intact.  
6. **Delete legacy tooling** once the new pipeline passes.  

After this, the project should look and behave like it was originally scaffolded from the chosen starter, which makes future maintenance and onboarding much easier.
