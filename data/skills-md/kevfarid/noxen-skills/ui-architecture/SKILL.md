---
name: ui-architecture
description: >
  Detects which frontend architecture convention a repo (React/Next.js/
  monorepo) uses, and tells you where an app-wide shared component/hook/
  utility should live — the `ui/` vs. feature-specific boundary, and 9 other
  repo shapes beyond it (monorepo, Feature-Sliced Design, shadcn-vendored,
  …). Use it when the user asks "where do I put this component", "should
  this be a shared component", "where does shared stuff go", is creating a
  new cross-cutting component, or is evaluating/migrating the frontend
  folder organization. Complements `architecture`, which covers feature-
  module folder structure but not this app-wide-shared-component boundary.
  Do NOT trigger for a component that's clearly feature-specific already —
  see `architecture`.
metadata:
  version: 1.0
  collection: noxen
---

# Noxen — UI Architecture

Part of the **Noxen** skill set (a personal engineering standard for React +
TypeScript). This skill covers the full decision tree for where an
app-wide shared component/hook/util belongs — including the common `ui/`
vs. feature-specific boundary and 9 less common repo shapes. For
feature-module folder structure itself, see `architecture`.

Goal: given an unfamiliar repo, identify which of the 10 frontend organization scenarios it's
in, and decide where a component/hook/util **shared across the whole app** (not specific to a
single feature/domain) should live.

Don't assume the scenario from the framework. Next.js, CRA, Vite, and monorepos can each
implement any of the 9. Detect by folder structure and config files, not by framework.

## How to detect the scenario (check in order)

Run these checks in order; the first match wins. Several can coexist (e.g. a monorepo +
shadcn inside one app) — in that case, a shared component *inside one app* follows that app's
internal scenario rules, and only moves to the shared package once there's a real second
consumer.

1. **Is there a monorepo workspace?** (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`,
   `lerna.json`, or `"workspaces"` in the root `package.json`) + `ls packages/ apps/`
   - Does a `packages/design-system`, `packages/ui`, or `packages/ui-kit` package exist with
     its own `package.json`, imported from apps via alias (`@scope/ui`)?
     → **Scenario 1** (`references/monorepo-design-system-package.md`)
   - Is there a monorepo but NO such package, with shared components living inside one app and
     imported by others via relative path / cross alias?
     → **Scenario 8** (`references/monorepo-no-shared-package.md`)

2. **Is there a `components.json` at the app root?** (shadcn/ui config) and/or
   `src/components/ui/*` with Radix-based primitives + a `cn()` helper.
   → **Scenario 7** (`references/shadcn-vendored.md`)

3. **Are the top-level folders under `src/` generic technical layers** (`components/`,
   `hooks/`, `services/`, `pages/`, `utils/`) **instead of domain names**?
   → **Scenario 2** (`references/react-basic-structure.md`)

3b. **Does a self-contained generic `ui/` folder exist, with no `design-system/` sibling and
   no top-level domain folders either** (i.e. no screaming architecture yet)? Business-specific
   components are either scattered per-route or dumped in one flat non-generic bucket
   (`core/components/`, `app/components/`)?
   → **Scenario 10** (`references/two-layer-ui-vs-feature-components.md`) — note: prefer
   routing business components to their owning feature/route over a flat bucket; see that
   reference for why.

4. **Do the canonical Feature-Sliced Design folders exist** (`app/`, `processes/`, `pages/`,
   `widgets/`, `features/`, `entities/`, `shared/`), especially `shared/ui`?
   → **Scenario 5** (`references/feature-sliced-design.md`)

5. **Do literal `atoms/`, `molecules/`, `organisms/` folders exist** (with or without
   `templates/`), at any level?
   → **Scenario 6** (`references/atomic-design.md`) — this is a naming variant that can
   combine with scenarios 1, 3, or 4; document both if applicable.

6. **Are the top-level folders domain/feature names** (`auth/`, `events/`, `billing/`...) —
   i.e. "screaming architecture" — **and is there also a top-level folder dedicated to
   business-logic-free components?**
   - Is that split into two folders (`design-system/` + `ui/`, or `design-system/` +
     `layout/`)? → **Scenario 3** (`references/screaming-design-system-folder.md`)
   - Is it a single folder (`ui/` or `components/`) mixing primitives and layout?
     → **Scenario 4** (`references/screaming-ui-merged.md`)

7. **Does the code import a third-party UI library directly everywhere**
   (`@mui/material`, `@chakra-ui/react`, `@mantine/core`, `antd`) **with no local wrapper
   layer**, just a theme/theme-override file?
   → **Scenario 9** (`references/third-party-ui-library.md`)

If nothing matches clearly, say so explicitly to the user instead of forcing a scenario — it
may be a new repo without an established convention yet; in that case recommend Scenario 3 or
4 depending on whether the team already separates primitives from layout.

## The 9 scenarios (summary)

| # | Scenario | Strong signal |
|---|----------|---------------|
| 1 | Monorepo with a design system package | `packages/design-system` imported via alias |
| 2 | Basic/flat React | root folders = technical layers (`components/`, `services/`...) |
| 3 | Screaming + `design-system/` separate from `ui/` | two dedicated sibling folders |
| 4 | Screaming + merged `ui/` | a single folder, no split |
| 5 | Feature-Sliced Design | `shared/`, `entities/`, `widgets/` folders |
| 6 | Atomic Design | `atoms/molecules/organisms/` folders |
| 7 | shadcn/ui vendored | `components.json` + `components/ui/*` |
| 8 | Monorepo without a dedicated package | workspace with no UI package, cross-app imports |
| 9 | Third-party UI library with no own layer | MUI/Chakra/Mantine direct, no local wrapper |
| 10 | Two-layer generic `ui/` vs. feature-owned components | `ui/` exists, no domain folders yet, no `design-system/` sibling |

Only load the reference for the detected scenario — don't load all 10 at once.

## Hard Rules

- Detect the scenario from folder structure and config files, never from the framework alone — Next.js, CRA, Vite, and monorepos can each implement any of the 10.
- Load only the reference for the detected scenario — never load all of them to "be thorough."
- If nothing matches clearly, say so explicitly and recommend a starting scenario — never force a bad fit silently.
