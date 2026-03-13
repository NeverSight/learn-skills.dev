---
name: frontend-init
description: Standardizes an already-scaffolded frontend TypeScript web app with baseline tooling, structure, and conventions. Use when setting up or aligning pnpm + TypeScript strict + path aliases, Vitest, Oxc (oxlint/oxfmt), and a progressive FSD-style folder layout, or when the user asks about initial project rules and UI library choices.
---

# Frontend Init (Scaffolded Project)

## Quick start

1) Confirm baseline assumptions
- Project already scaffolded (no build-tool scaffolding in this skill)
- Package manager is pnpm
- TypeScript is used (or will be added)

2) Ask one decision question early
- UI/CSS: "Do you want a UI/component library or CSS framework? If yes, which one?" (If none, proceed with plain CSS Modules or the existing setup.)

3) Apply baseline setup
- Tooling: add Vitest + Oxc lint/format and wire `package.json` scripts
- TypeScript: enable strict mode + DOM libs + `@/*` path alias
- Structure: create progressive FSD-style folders (`src/app`, `src/shared`, `src/features`)

Links:
- Tooling details: see `frontend-init/references/tooling.md`
- TypeScript settings: see `frontend-init/references/typescript.md`
- Folder structure: see `frontend-init/references/structure.md`

## Workflow

### 1) Baseline checks

- Ensure `pnpm -v` works; prefer `pnpm install`
- Confirm Node version is compatible with the project tooling

### 2) Tooling baseline (test + lint + format)

- Add dev deps: `vitest`, `oxlint`, `oxfmt`
- Create an Oxlint config (`oxlint --init`)
- Add scripts:
  - `typecheck` (runs `tsc --noEmit`)
  - `test`, `test:run`
  - `lint`, `lint:fix`
  - `fmt`, `fmt:check`

Details: `frontend-init/references/tooling.md`

### 3) TypeScript baseline

- Turn on `strict`
- Ensure DOM libs are present
- Add `@/*` alias for `src/*` and make sure tooling resolves it

Details: `frontend-init/references/typescript.md`

### 4) Progressive FSD structure

- Create minimal layers only:
  - `src/app/`
  - `src/shared/`
  - `src/features/`
- Add `entities/pages/widgets` only when the project needs them

Details: `frontend-init/references/structure.md`

## Advanced

- Add UI/CSS dependencies after the user chooses a direction; keep the baseline independent.
