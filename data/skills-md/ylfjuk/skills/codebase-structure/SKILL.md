---
name: codebase-structure
description: Where code belongs in a codebase — architectural layers, file and folder naming, imports and barrels, package boundaries. Use when adding, moving, or renaming files; building a page, screen, or route; scaffolding a feature or package; or reviewing structure, even if conventions aren't mentioned.
---

# Codebase Structure

## Precedence — read this first

**Existing standards supersede this guide** — the organization's, the language's, the framework's, and the repo's own, in that order. This covers everything here, including rules stated firmly and ones argued on quality grounds.

Follow the established standard and leave existing code alone. Refactor toward this guide only when explicitly asked to.

This guide is the default for greenfield code, and for anything no other standard has already decided.

---

This codebase organizes code by **conceptual responsibility**, not by technical category. The directory a file sits in is a consequence of what the code is responsible for and what concepts it needs to know about.

Two things follow from that, and they matter more than any individual rule below:

- **Do not create a layer because a kind of code exists.** The right structure is the smallest one that gives useful separation of responsibilities and dependency boundaries. A small frontend may only need `features/`, `pages/`, `routes/`.
- **Each app type brings its own composition layers.** A frontend app composes through `layouts`, `pages`, `routes`; a backend app through `controllers`, `middlewares`, `routes`. Neither set is the default — they're peer instantiations of the same application-composition responsibility, and a different kind of app (CLI, worker, job runner) introduces its own.
- **Do not promote code across ownership boundaries for hypothetical reuse.** Start at the narrowest reasonable scope. Move it when there's a concrete reason — real reuse, a clearer owner, dependency isolation, distribution, a meaningful boundary.

## Repository shape

**Always structure the repo as a monorepo**, even for a single app or a single package. This is a fixed convention, not a judgment call.

Create only the roots you actually use — a library monorepo has `packages/` and no `apps/`, and an empty `apps/` directory is decoration:

```text
packages/
  core/
    package.json        # @scope/core
    src/
  cli/
    package.json        # @scope/cli
    src/
```

What that means in practice:

- Workspace configuration lives at the root. The root holds workspace and shared tooling config — not source.
- Every app and package is a real workspace package with its own `package.json` and scoped name.
- Application source lives in `apps/{app}/`, never at the repo root.
- Cross-package imports go through the package name (`@scope/package`), never a relative path that climbs out of one workspace into another.

That last point is what makes the boundary rules enforceable rather than aspirational: the module resolver, not a convention, is what stops a consumer from reaching into another package's internals.

The distinction, when both are present: `apps/` holds deployables, `packages/` holds publishables and shared code. Adding the other root later requires no restructuring, since the shape is already correct.

## Placing code: the procedure

Work through these in order. Stop as soon as the answer is clear.

1. **What is this code's responsibility?** Not "what is it" (a hook, a util, a component) — what job does it do?
2. **What concepts does it need to know about?** If it knows about users, orders, or auth, it cannot live in a generic layer. Awareness of business concepts is the single strongest placement signal.
3. **Who is its narrowest legitimate owner?** The feature, domain, or app that the responsibility actually belongs to.
4. **Is it genuinely reused across that owner's boundary?** Not "could it be" — is it, now?
5. **Pick the layer** using the table below.
6. **Only then** decide whether it stays colocated, moves to a shared layer, becomes a submodule, or becomes a package.

## Layer quick reference

| The code is…                                          | It goes in                   |
| ----------------------------------------------------- | ---------------------------- |
| Generic, low-level, no business awareness             | `core`                       |
| Base or vendor UI primitives (e.g. shadcn components) | `ui`                         |
| Bindings/adapters around an external library          | `lib`                        |
| App-owned design-system component or visual block     | `design`                     |
| Reusable app-level building block, no domain owner    | `foundation`                 |
| A capability the app provides — what it can _do_      | `features/{feature}`         |
| Context-specific composition of features              | `domains/{domain}`           |
| App composition — frontend                            | `layouts`, `pages`           |
| App composition — backend                             | `controllers`, `middlewares` |
| Route definitions and runtime wiring                  | `routes`                     |
| Reused across apps or packages                        | a package                    |

Read `references/layers.md` for what each layer actually owns, and for the distinctions that are easy to get wrong: `core` vs `foundation`, `feature` vs `domain`, `ui` vs `design`, and generic vs app-specific use of a third-party library.

### Two traps this table sets

**Naming coincidence is not ownership.** A generic function whose first caller is `features/users` does not belong in `features/users`. A user-specific validator does not belong in `core/utils` because two features now call it.

**Technical subdirectories are not layers.** `components/`, `services/`, `utils/`, `types/` are organizational tools inside a feature or domain. Introduce one when there's enough related code to justify it — not to fill out a template.

## Dependency direction

Specificity increases from generic infrastructure toward application composition:

```text
core → ui / lib → design → foundation → features → domains → application composition
```

The final node is whatever composition layers the app type provides:

```text
frontend:  domains → layouts → pages → routes
backend:   domains → controllers / middlewares → routes
```

More-specific code may depend on less-specific code where it actually needs to. The reverse is the error to watch for: `core/utils → features/users` makes generic code aware of a specific capability. A feature must not depend on a domain that consumes it.

This is a direction, not a chain — no layer is required to depend on the one immediately before it. `ui`, `design`, and `lib` in particular don't sit in a strict line with the rest; place them by their actual dependencies.

## Rules that are not judgment calls

Apply these without deliberation.

**File and folder names use `kebab-case`**, components included:

```text
some-component.tsx      ✓
SomeComponent.tsx       ✗
```

Framework- or tooling-required filenames (`vite.config.ts`, Next.js route files, etc.) follow that tool's convention instead — see `references/conventions.md`.

**Don't repeat the folder name in the file name.** Avoid tautological names that repeat context the path already provides. In `users/user-service.ts`, `users/` already establishes the subject, so prefer `users/service.ts`. Keep a qualifier when it adds a meaningful distinction:

```text
feature/component.tsx           ✓
feature/feature-component.tsx   ✗
```

**Within a unit, import directly. Don't route through a barrel:**

```ts
import { X } from './X';   ✓
import { X } from '.';      ✗
```

**Barrels belong at the root of a conceptual unit, and nowhere else.** A feature, foundation block, lib integration, or domain has an `index.ts` at its own root defining its public API:

```text
features/users/index.ts        ✓  entry point for the feature
features/users/utils/index.ts  ✗  internal subdirectory
features/users/types/index.ts  ✗  internal subdirectory
```

Create it with the unit. The unit exists because something consumes it — that's what justified extracting it in the first place — so it needs an interface from the start. Without one, consumers reach into internals (`features/users/components/user-list`) and the boundary stops meaning anything.

The "does this have a consumer?" test applies to **creating the unit**, not to giving it a barrel. If nothing consumes it yet, the code should still be colocated with its owner rather than sitting in a feature of its own.

Curate what the barrel exports. It's a public API, not a re-export of everything inside:

```ts
export type * from "./types";
export { createUserService } from "./services/create-user-service";
```

What "don't abuse them" rules out: an `index.ts` in every subdirectory, barrels that re-export a unit's entire contents, and routing an import through a barrel when a direct path is available.

**`core` and `ui` get no barrel.** Neither is a cohesive unit with a public API — `core` is a collection of unrelated primitives, and `ui` mirrors whatever the generator emitted. Import from them directly:

```ts
import { isDefined } from '@scope/core/utils/is-defined';   ✓
import { Button } from '@scope/ui/components/button';        ✓
```

A barrel over either would export everything and mean nothing.

**Across a boundary, use the public entry point. Never reach inside:**

```ts
import { X } from '@scope/users';           ✓
import { useX } from '@scope/users/react';  ✓  (declared submodule)
import { X } from '@scope/users/src/internal/X';  ✗
```

**Type-only re-exports must be explicit:**

```ts
export type * from './types';   ✓
export * from './types';         ✗  (for type-only modules)
```

**Package names follow `@{scope}/{name}`** or `@{scope}/{sub-purpose}.{name}` — e.g. `@scope/web`, `@scope/feature-react`, `@scope/tests.utils`.

**File-based routing assigns an entry point, not all frontend responsibilities.** Keep the framework-required route module where the framework expects it and let it own routing concerns: route configuration, loading and validation, redirects, guards, and route-specific orchestration. Pages own a screen's general structure and compose its features, domains, and layouts, much as controllers compose application capabilities into a response. Extract when that division gives the screen a clear owner; do not add a page merely to wrap a trivial route, or override an established framework or repository convention that deliberately combines them.

## Files, configs, constants, utilities

A file should represent one cohesive concept. Multiple exports are fine when they form a coherent unit (`colors/guards.ts` exporting `isWarmColor` and `isColdColor`); unrelated helpers get separate files (`utils/is-defined.ts`, `utils/is-nullish.ts`). A concept's number of callers decides its scope, not whether it merits its own file. Give a distinct component, type, schema, or function its own file when that makes its responsibility easier to name, find, and understand; keep closely coupled details together when they form one concept. Do not split files just to enforce one export each.

Start with `constants.ts` or `utils.ts` for a small cohesive set; promote to a directory when distinct groups become independently meaningful.

`references/conventions.md` covers configs and env validation, constants, utils vs helpers, tests, and tool-owned files.

## Packages

Create a package when the boundary itself pays for something: reuse, isolation, ownership, distribution, dependency management, an independently consumable API. **Never create one just to make the physical structure mirror the conceptual architecture** — moving code into a package does not change its conceptual layer. The same layers still apply inside `packages/{package}/src/`: a package may contain features and, when it composes those capabilities for a context, domains.

Extraction doesn't have to take a whole layer. A feature's reusable types/utils/services can move to a package while its app-specific components stay behind.

Read `references/packages.md` before extracting anything, defining a public API, or adding a submodule.

## When the answer isn't clear

This guide is deliberately permissive about structure — layers can be omitted, combined, split, or spread across packages. When a placement is genuinely ambiguous after working through the procedure above:

- Prefer the narrower scope. Colocated code that later needs promoting is a cheaper mistake than shared code that shouldn't be.
- Say which call you made and why, rather than picking silently. Placement decisions are the reviewable part of the work.

Matching the surrounding code isn't a tiebreaker for ambiguous cases — it's the precedence rule at the top of this file, and it applies whether or not the guide is clear.
