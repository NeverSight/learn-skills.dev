---
name: jotai-nextjs
description: Expert workflow for Jotai state management with a Next.js focus, covering core APIs, SSR hydration, utilities, recipes, and current release migrations.
---

# Jotai + Next.js

## Purpose

Use this skill to design, implement, debug, and migrate Jotai state in React/Next.js apps with version-aware guidance.

## Version baseline (re-check when invoked)

- Reference package version: `jotai@2.18.0` (npm `latest`, verified on 2026-02-22).
- Latest release reviewed: `v2.18.0` (published on 2026-02-19).
- Re-check commands:
  - `npm view jotai version`
  - `npm view jotai dist-tags --json`
  - `npm view jotai time.modified`
  - `https://github.com/pmndrs/jotai/releases`

## When to use

- SSR/CSR state architecture in Next.js (App Router or Pages Router).
- Atom modeling (core), utility selection (`storage`, `select`, `async`, `resettable`, `family`).
- Migration work for v2+ and upcoming v3 deprecations.
- Performance/debugging issues caused by atom identity or over-rendering.

## Non-negotiable rules

- For SSR, wrap the app/subtree in `<Provider>` to avoid shared global store across requests.
- Use `useHydrateAtoms` in client components (`'use client'`), not server components.
- Atoms hydrate once per store; do not expect rerender-time hydration to overwrite values.
- Avoid returning unresolved promises during SSR paths; prefetch and hydrate when possible.
- Keep atom references stable. Do not create raw `atom(...)` in render without `useMemo` or `useRef`.
- Prefer `useSetAtom` when write-only to reduce unnecessary rerenders.
- Treat `selectAtom` as an escape hatch; keep both the base atom and selector reference stable.
- `atomFamily` from `jotai/utils` is deprecated and planned for removal in v3; prefer `jotai-family`.
- `jotai/babel` is deprecated; use `jotai-babel`.
- `@swc-jotai/*` plugins are experimental; use only when the project accepts experimental compiler behavior.

## Quick snippets

```tsx
// app/providers.tsx
'use client'
import { Provider } from 'jotai'
export function Providers({ children }: { children: React.ReactNode }) {
  return <Provider>{children}</Provider>
}
```

```tsx
// app/page.tsx (client hydration entry)
'use client'
import { atom } from 'jotai'
import { useHydrateAtoms } from 'jotai/utils'
const countAtom = atom(0)
export function HydrateCount({ initial }: { initial: number }) {
  useHydrateAtoms([[countAtom, initial]])
  return null
}
```

```tsx
// stable selectAtom usage
const selectedAtom = useMemo(
  () => selectAtom(baseAtom, (s) => s.slice),
  [baseAtom],
)
```

## Workflow

### 1) Confirm app/runtime boundaries

- Identify Next.js router mode (`app/` vs `pages/`) and where client boundaries exist.
- Find atom definitions and where providers/stores are mounted.

### 2) Establish store strategy

- Default: one `<Provider>` at app root for SSR safety.
- Use custom stores (`createStore`) when scoping state to subtrees/tests or outside React via store API.

### 3) Hydration and async strategy

- Hydrate server-fetched values with `useHydrateAtoms`.
- For multiple stores, hydrate each store explicitly.
- If async atoms feed sync-only utilities (`splitAtom`, etc.), unwrap/load before composition.

### 4) Utility and recipe selection

- `atomWithStorage` for persistence; account for SSR mismatch and `getOnInit`.
- `resettable` APIs when reset semantics are explicit (`RESET`, `useResetAtom`).
- `selectAtom` only for equality-based slicing that pure derived atoms cannot handle.
- `atomWithDebounce`, `useAtomEffect`, and `focusAtom/splitAtom/selectAtom` patterns for advanced workflows.

### 5) Migration and release checks

- Scan recent releases for deprecations/internal changes before recommending imports.
- Call out migrations explicitly when touching Babel tooling, `atomFamily`, or deprecated async helpers.

### 6) Deliverables

Return:

- Suggested atom/store architecture.
- Exact API choices and why.
- Migration edits (before/after snippets).
- Risks and test checklist (SSR hydration, rerender behavior, stale identity).

## Progressive disclosure

Load only what is needed:

- `reference/nextjs-ssr-playbook.md` for Next.js setup and hydration.
- `reference/core-utilities-recipes.md` for API and recipe choices.
- `reference/latest-version-and-changelog.md` for version-aware migration guidance.
- `reference/sources.md` for canonical links and verification trail.
