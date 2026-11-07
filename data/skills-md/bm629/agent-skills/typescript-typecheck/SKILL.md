---
name: typescript-typecheck
description: >
  Use when setting up or running TypeScript type-checking as a standalone
  quality gate — writing or tightening a strict tsconfig.json, adding a
  `tsc --noEmit` (or `tsc -b --noEmit`) check that runs separately from the
  build, wiring that check into CI, or configuring TypeScript project
  references for a multi-package (pnpm/Turborepo) monorepo. Covers why a
  dedicated type-check gate is mandatory (bundlers and transpilers strip
  types without checking them), the strict compiler-option set worth enabling
  beyond `strict: true`, the Vite split-config layout, and cross-package type
  resolution via composite project references. TypeScript 5.x.
extensions:
  claude:
    when_to_use: "Setting up/running TypeScript type-checking as a CI/quality gate, a strict tsconfig, or project references."
  copilot:
    applyTo: "**/tsconfig*.json"
  cursor:
    alwaysApply: false
    globs: ["**/tsconfig*.json"]
  gemini: {}
  codex: {}
version: "1.0.0"
forge:
  status: reviewed
  forged: 2026-06-09
  reviewed: 2026-06-09
---

# `typescript-typecheck` — SKILL.md

> **Variant:** standard · **When to use:** the skill is invoked, runs to completion, returns a configured type-check gate (tsconfig + scripts + CI step), control passes back to the caller.

## Overview

TypeScript's compiler (`tsc`) is the only tool that actually checks types. Bundlers and transpilers in a typical TS toolchain — Vite (esbuild in dev, Rollup in prod) and the SWC-based React plugin — **transpile/strip type annotations without checking them**. That means `vite build` (or any esbuild/SWC build) compiles successfully even when the code is full of type errors. This skill sets up the missing piece: a dedicated `tsc --noEmit` type-check gate that runs locally and in CI, backed by a genuinely strict `tsconfig`, plus TypeScript **project references** so cross-package types resolve in a monorepo. It is the type-system analog of a separate static-analysis gate — a linter (Biome/ESLint) finds style and bug patterns but has no type system and cannot do this job. Pinned to TypeScript 5.x. Verified flag list and worked examples live in `references/`.

## When to activate

- ✅ Setting up TypeScript type-checking for a project for the first time (a `typecheck` script + CI step).
- ✅ Writing or tightening a `tsconfig.json` and wanting it *genuinely* strict (not just `strict: true`).
- ✅ Configuring `moduleResolution: "bundler"` for a Vite/esbuild/bundler app and getting the companion flags right.
- ✅ Setting up TypeScript **project references** (`composite`, `references`, `tsc -b`) so an app package can consume a library/generated package's types in a monorepo.
- ✅ Adding a CI type-check gate (e.g. GitHub Actions with pnpm) that fails the build on a type error the bundler would have ignored.

**Do NOT activate when:**

- The task is lint/format rules — that is a linter's job (e.g. the `biome` skill); a linter does not type-check.
- The task is the actual production bundle/build output — that belongs to the bundler (e.g. the `vite` skill); this skill only owns the `tsc` *check*.
- The task is a deep TypeScript type-system tutorial (advanced conditional/mapped types, generics gymnastics) — this skill is about the *gate and its config*, not type theory.
- The task is wiring the monorepo task runner's pipeline/caching — that belongs to the task-runner skill (e.g. `turborepo`); this skill only contributes the `typecheck` task it should run.

## Workflow

### Step 1: Establish *why* the gate is separate (and never skip it)

Internalize and, where relevant, state in the setup: **no transpiler type-checks.**

- Vite's own docs state it only transpiles `.ts` files and does **not** type-check, assuming "type checking is taken care of by your IDE and build process" — explicitly recommending a `tsc --noEmit` step. esbuild "only performs transpilation without type information."
- The SWC-based React plugin (`@vitejs/plugin-react-swc`) is the same: SWC strips types without checking them. Choosing SWC over Babel/esbuild is a **build-speed decision** owned by the bundler config — it does **not** add or remove a type-check; the `tsc` gate is still required.

Conclusion: a standalone `tsc --noEmit` (or `tsc -b --noEmit` with references) gate is **mandatory**, not optional, and must be **distinct from `vite build`**.

### Step 2: Write a genuinely strict `tsconfig`

`strict: true` is the floor, not the ceiling. It turns on a known family (full list + worked configs in [`references/strict-tsconfig.md`](references/strict-tsconfig.md)):
`noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `useUnknownInCatchVariables`, `alwaysStrict`.

Add the high-value flags **not** covered by `strict`:

- `noUncheckedIndexedAccess` — adds `undefined` to index/array access results (the single biggest real-bug catcher beyond `strict`).
- `noImplicitOverride` — requires the `override` keyword so subclasses can't silently drift.
- `noFallthroughCasesInSwitch`, `noImplicitReturns` — control-flow completeness.
- `noUnusedLocals`, `noUnusedParameters` — dead-code (params prefixed `_` are exempt).
- `exactOptionalPropertyTypes` — distinguishes "absent" from "set to `undefined`" (see Gotchas — it is the one to add knowingly).
- `verbatimModuleSyntax` — drops imports/exports exactly per the `type` modifier you wrote (no elision guessing).

For a Vite/bundler app, the module block is: `"module": "esnext"` (or `"preserve"`), `"moduleResolution": "bundler"`, `"noEmit": true`, `"jsx": "react-jsx"`, `"isolatedModules": true`, `"moduleDetection": "force"`. Easiest strict floor: `"extends": "@tsconfig/strictest"` then layer the bundler block on top.

### Step 3: Adopt the Vite split-config layout (if Vite)

A Vite TS app scaffolds three files: a **solution** `tsconfig.json` that only holds `"files": []` + `"references"` to the two leaf configs; `tsconfig.app.json` (your `src/`, DOM lib, bundler resolution, `noEmit`); `tsconfig.node.json` (`vite.config.ts`, node lib). `package.json` gets `"build": "tsc -b && vite build"` and you add a standalone `"typecheck": "tsc -b --noEmit"`. The `tsc -b` step is **type-check-only** here because the leaf configs set `noEmit`. Layout + exact files in [`references/vite-split-config.md`](references/vite-split-config.md).

### Step 4: Configure project references for the monorepo

For a multi-package repo where an app consumes a library or **generated** package (e.g. a generated API client): set `"composite": true` on the referenced package (this **forces** `declaration: true` and requires every source file be matched by `include`/`files`), add a `"references": [{ "path": "../<pkg>" }]` entry on the consumer, and build/check with `tsc -b`. Importing from a referenced project resolves against its emitted `.d.ts`, and `tsc -b` builds dependencies in order and is incremental via `.tsbuildinfo`. Worked 2-package example in [`references/project-references.md`](references/project-references.md). Wire the resulting `typecheck` task into the monorepo task runner (caching, dependency order) via the **`turborepo`** skill — do not re-derive a pipeline here.

### Step 5: Add the CI gate

Add a CI job that runs the `typecheck` script on every push/PR so a type error fails the build (the bundler never would). High-level GitHub Actions shape (checkout → pnpm + Node with cache → install → `pnpm run typecheck` or `turbo run typecheck`) in [`references/ci-gate.md`](references/ci-gate.md); the pipeline/caching specifics belong to the task-runner skill.

## Rules

**Hard rules (never violate):**

- **The `tsc` check is separate from the build.** Never claim or imply that `vite build` / esbuild / SWC validates types. Keep `typecheck` a distinct script and a distinct CI step.
- **`strict: true` is mandatory; `strict` alone is not "strict enough."** Ship at least `noUncheckedIndexedAccess` on top, and prefer a strictest base.
- **Don't trust a scaffold to be strict — verify it.** A freshly scaffolded `tsconfig.app.json` may *not* contain `strict: true`; open it and confirm (or `extends: "@tsconfig/strictest"`). Never assume.
- **With project references, check via `tsc -b`, not bare `tsc`.** Bare `tsc -p` on the solution file ignores the `references` graph; `tsc -b` (build mode) honors it and is incremental.
- **`composite: true` forces `declaration: true`** and requires all files be in `include`/`files` — set `outDir`/`tsBuildInfoFile` deliberately.

**Preferences (override-able):**

- Prefer `extends: "@tsconfig/strictest"` as the strict floor, then override the module/jsx block per project.
- Prefer `module: "esnext"` (or `"preserve"`) with `moduleResolution: "bundler"` for bundler apps; `nodenext` for Node libraries.
- Use `vite-plugin-checker` for fast in-editor/in-dev feedback **in addition to** — never instead of — the CI `tsc` gate.
- Keep `skipLibCheck: true` on by default for speed, knowing the trade-off (Gotchas).

## Gotchas

- **"`vite build` passed, so the types are fine."** False — the highest-value mistake this skill prevents. The bundler stripped the types; only `tsc --noEmit` checked them. Always run the `typecheck` script independently.
- **Scaffold is not automatically strict.** The current create-vite `react-ts` `tsconfig.app.json` carries the bundler + lint flags but you must confirm `strict: true` is actually present (it has drifted across template versions); add it or `extends: "@tsconfig/strictest"`.
- **`moduleResolution: "bundler"` has hard companions.** It requires `module` to be `esnext` or `preserve` (not `commonjs`). `allowImportingTsExtensions: true` is only legal when `noEmit` (or `emitDeclarationOnly`) is set — which is exactly the type-check-only setup, so it fits, but emitting JS with it will error.
- **`exactOptionalPropertyTypes` surprises.** With it on, `{ a?: string }` no longer accepts `{ a: undefined }` — you must write `a?: string | undefined` to allow that. It is *not* in `strict` for this reason; add it deliberately and expect to touch optional-property call sites.
- **Forgetting `tsc -b` in a references setup.** Running `tsc --noEmit` against a solution `tsconfig.json` with only `references` checks nothing useful — build mode (`tsc -b`) is what walks the graph. The `typecheck` script must use `-b`.
- **`skipLibCheck: true` hides real errors.** It skips type-checking *all* `.d.ts` (including your generated client's emitted declarations and conflicting `node_modules` lib types). It's a deliberate speed/noise trade-off; if a generated `.d.ts` is itself malformed, this mask will let it through.
- **`verbatimModuleSyntax` needs explicit `import type`.** With it on, a value-position import of a type is no longer elided and can crash at runtime — mark type-only imports with `import type`. It supersedes the deprecated `importsNotUsedAsValues`/`preserveValueImports`.

## Anti-patterns

- **"We have a linter, so we don't need `tsc`."** A linter (Biome/ESLint) has no type system; it cannot catch a type error. The type-check gate is non-negotiable and orthogonal to lint.
- **"Switching to the SWC plugin removed the need for the `tsc` step."** No — SWC is a faster transpiler that still does not type-check. The build plugin choice is independent of the type-check gate.
- **"Just turn on `skipLibCheck` and the errors go away."** That suppresses *declaration-file* errors, not your code's errors, and can mask a broken generated `.d.ts`. Don't reach for it to silence a real type failure.
- **"Set `strict: true` and call the config strict."** Strict-floor only; ship the extra flags (`noUncheckedIndexedAccess` at minimum) or a strictest base.
- **"Let CI rely on `vite build` to catch type problems."** It never will. The CI gate must invoke `tsc`/`tsc -b --noEmit` (directly or via the task runner) as its own step.

## Output

A working TypeScript type-check gate for a project: a genuinely strict `tsconfig` set (solution + leaf configs where applicable), a standalone `typecheck` npm script (`tsc --noEmit` or `tsc -b --noEmit`) distinct from the build, project references wired for any consumed/generated package, and a CI step that runs the check and fails on type errors. The consumer is the next workflow phase — the developer or dispatched agent who now has a type-error gate the bundler does not provide, and CI that enforces it.

## Related

- `biome` (or any linter skill) — the lint/format complement; it does **not** type-check, which is why this skill exists.
- `vite` — owns the build/bundle; this skill owns only the `tsc` *check* that the build skips.
- `turborepo` — owns the monorepo task pipeline/caching; this skill contributes the `typecheck` task it runs.
- Python analog (conceptual only, different toolchain): a standalone Python type-checker such as `ty` plays the same "separate type-check gate" role for Python that `tsc --noEmit` plays here.

## Progressive disclosure

- [`references/strict-tsconfig.md`](references/strict-tsconfig.md) — the full `strict` family, the recommended extra flags with exact behavior, the bundler module block, shareable bases, and a worked strict `tsconfig.app.json`. Load when writing/tightening a tsconfig.
- [`references/vite-split-config.md`](references/vite-split-config.md) — the three-file Vite TS layout, the `tsc -b && vite build` + `typecheck` scripts, and `vite-plugin-checker`. Load when setting up a Vite app's type-check.
- [`references/project-references.md`](references/project-references.md) — composite/references/`tsc -b`/incremental semantics with a worked 2-package (app → generated-client) example, and `skipLibCheck`. Load when wiring a monorepo.
- [`references/ci-gate.md`](references/ci-gate.md) — the `tsc` CLI flag reference, the GitHub Actions gate shape, and the verified `tsgo`/typescript-go status note. Load when adding CI or asked about the native compiler.
- [`references/sources.md`](references/sources.md) — research provenance.

## Body budget

- `description` ≤ 1,024 chars.
- Body ≤ ~500 lines / 5,000 tokens; heavy content lives in `references/`, loaded on demand.
