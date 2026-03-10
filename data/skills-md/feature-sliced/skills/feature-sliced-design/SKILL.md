---
name: feature-sliced-design
description: >
  Official Feature-Sliced Design (FSD) v2.1 skill for applying the methodology
  to frontend projects. Use when the task involves organizing project structure
  with FSD layers, deciding where code belongs, defining public APIs and import
  boundaries, resolving cross-imports or evaluating the @x pattern, deciding
  whether logic should remain local or be extracted, migrating from FSD v2.0 or
  a non-FSD codebase, integrating FSD with frameworks, or implementing common
  patterns such as auth, API handling, Redux, and React Query within FSD.
---

# Feature-Sliced Design (FSD) v2.1

> **Source**: [fsd.how](https://fsd.how) | Strictness can be adjusted based on
> project scale and team context.

---

## 1. Core Philosophy & Layer Overview

FSD v2.1 core principle: **"Start simple, extract when needed."**

Place code in `pages/` first. Duplication across pages is acceptable and does
not automatically require extraction to a lower layer. Extract only when the
team agrees it is necessary.

**Not all layers are required.** Most projects can start with only `shared/`,
`pages/`, and `app/`. Add `widgets/`, `features/`, `entities/` only when they
provide clear value. Do not create empty layer folders "just in case."

FSD uses 6 standardized layers with a strict top-down import direction:

```text
app/       → App initialization, providers, routing
pages/     → Route-level composition, owns its own logic
widgets/   → Large composite UI blocks reused across multiple pages
features/  → Reusable user interactions (only when used in 2+ places)
entities/  → Reusable business domain models (only when used in 2+ places)
shared/    → Infrastructure with no business logic (UI kit, utils, API client)
```

**Import rule**: A module may only import from layers strictly below it.
Cross-imports between slices on the same layer are forbidden.

```typescript
// ✅ Allowed
import { Button } from "@/shared/ui/Button"; // features → shared
import { useUser } from "@/entities/user"; // pages → entities

// ❌ Violation
import { loginUser } from "@/features/auth"; // entities → features
import { likePost } from "@/features/like-post"; // features → features
```

**Note**: The `processes/` layer is **deprecated** in v2.1. For migration
details, read `references/migration-guide.md`.

---

## 2. Decision Framework

When writing new code, follow this tree:

**Step 1 — Where is this code used?**

- Used in only one page → keep it in that `pages/` slice.
- Used in 2+ pages but duplication is manageable → keeping separate copies
  in each page is also valid.
- An entity or feature used in only one page → keep it in that page
  (Steiger: `insignificant-slice`).

**Step 2 — Is it reusable infrastructure with no business logic?**

- UI components → `shared/ui/`
- Utility functions → `shared/lib/`
- API client, route constants → `shared/api/` or `shared/config/`
- Auth tokens, session management → `shared/auth/`
- CRUD operations → `shared/api/`

**Step 3 — Is it a complete user action reused in 2+ places, and does the
team agree to extract it?**

- Yes → `features/`
- Uncertain or single use → keep in the page.

**Step 4 — Is it a business domain model reused in 2+ places, and does the
team agree to extract it?**

- Yes → `entities/`
- Uncertain or single use → keep in the page.

**Step 5 — Is it app-wide configuration?**

- Global providers, router, theme → `app/`

**Golden Rule: When in doubt, keep it in `pages/`. Extract only when the
team agrees.**

---

## 3. Quick Placement Table

| Scenario              | Single use                                  | Multi-use (with team agreement)       |
| --------------------- | ------------------------------------------- | ------------------------------------- |
| User profile form     | `pages/profile/ui/ProfileForm.tsx`          | `features/profile-form/`              |
| Product card          | `pages/products/ui/ProductCard.tsx`         | `entities/product/ui/ProductCard.tsx` |
| Product data fetching | `pages/product-detail/api/fetch-product.ts` | `entities/product/api/`               |
| Auth token/session    | `shared/auth/` (always)                     | `shared/auth/` (always)               |
| Auth login form       | `pages/login/ui/LoginForm.tsx`              | `features/auth/`                      |
| CRUD operations       | `shared/api/` (always)                      | `shared/api/` (always)                |
| Generic Card layout   | —                                           | `shared/ui/Card/`                     |
| Modal manager         | —                                           | `shared/ui/modal-manager/`            |
| Modal content         | `pages/[page]/ui/SomeModal.tsx`             | —                                     |
| Date formatting util  | —                                           | `shared/lib/format-date.ts`           |

---

## 4. Architectural Rules (MUST)

These rules are the foundation of FSD. Violations weaken the architecture.
If you must break a rule, ensure it is an intentional design decision —
document the reason and obtain team consensus.

### 4-1. Import only from lower layers

`app → pages → widgets → features → entities → shared`.
Upward imports and cross-imports between slices on the same layer are
forbidden.

### 4-2. Public API — every slice exports through index.ts

External consumers may only import from a slice's `index.ts`. Direct imports
of internal files are forbidden.

```typescript
// ✅ Correct
import { LoginForm } from "@/features/auth";

// ❌ Violation — bypasses public API
import { LoginForm } from "@/features/auth/ui/LoginForm";
```

**RSC / meta-framework exception:** In environments with distinct client/server
boundaries, split entry points are permitted (`index.client.ts`,
`index.server.ts`). See `references/framework-integration.md` for details.

### 4-3. No cross-imports between slices on the same layer

If two slices on the same layer need to share logic, follow the resolution
order in Section 7. Do not create direct imports.

### 4-4. Domain-based file naming (no desegmentation)

Name files after the business domain they represent, not their technical role.
Technical-role names like `types.ts`, `utils.ts`, `helpers.ts` mix unrelated
domains in a single file and reduce cohesion.

```text
// ❌ Technical-role naming
model/types.ts          ← Which types? User? Order? Mixed?
model/utils.ts

// ✅ Domain-based naming
model/user.ts           ← User types + related logic
model/order.ts          ← Order types + related logic
api/fetch-profile.ts    ← Clear purpose
```

### 4-5. No business logic in shared/

Shared contains only infrastructure: UI kit, utilities, API client setup,
route constants, assets. Business calculations, domain rules, and workflows
belong in `entities/` or higher layers.

```typescript
// ❌ Business logic in shared
// shared/lib/userHelpers.ts
export const calculateUserReputation = (user) => { ... };

// ✅ Move to the owning domain
// entities/user/lib/reputation.ts
export const calculateUserReputation = (user) => { ... };
```

---

## 5. Recommendations (SHOULD)

### 5-1. Pages First — place code where it is used

Place code in `pages/` first. Extract to lower layers only when truly needed.
When extraction seems worthwhile, discuss with the team — this is a design
decision that affects the whole project.

**What stays in pages:**

- Large UI blocks used only in one page
- Page-specific forms, validation, data fetching, state management
- Page-specific business logic and API integrations
- Code that looks reusable but is simpler to keep local

**Evolution pattern:** Start with everything in `pages/profile/`. When another
page needs the same user data and the team agrees, extract the shared model to
`entities/user/`. Keep page-specific API calls and UI in the page.

### 5-2. Be conservative with entities

The entities layer is highly accessible — almost every other layer can import
from it, so changes propagate widely.

1. **Start without entities.** `shared/` + `pages/` + `app/` is valid FSD.
   Thin-client apps rarely need entities.
2. **Do not split slices prematurely.** Keep code in pages. Extract to
   entities only when 2+ consumers are confirmed and the team agrees.
3. **Business logic does not automatically require an entity.** Keeping types
   in `shared/api` and logic in the current slice's `model/` segment may
   be sufficient.
4. **Place CRUD in `shared/api/`.** CRUD is infrastructure, not entities.
5. **Place auth data in `shared/auth/` or `shared/api/`.** Tokens and login
   DTOs are auth-context-dependent and rarely reused outside authentication.

### 5-3. Start with minimal layers

```text
// ✅ Valid minimal FSD project
src/
  app/         ← Providers, routing
  pages/       ← All page-level code
  shared/      ← UI kit, utils, API client

// Add layers only when the team decides they are needed:
// + widgets/   ← UI blocks reused in 2+ pages
// + features/  ← User interactions reused in 2+ pages
// + entities/  ← Domain models reused in 2+ pages/features
```

### 5-4. Validate with the Steiger linter

[Steiger](https://github.com/feature-sliced/steiger) is the official FSD
linter. Key rules:

- **`insignificant-slice`**: Suggests merging an entity/feature into its page
  if only one page uses it.
- **`excessive-slicing`**: Suggests merging or grouping when a layer has too
  many slices.

```bash
npm install -D @feature-sliced/steiger
npx steiger src
```

---

## 6. Anti-patterns (AVOID)

- **Do not create entities prematurely.** Data structures used in only one
  place belong in that place.
- **Do not put CRUD in entities.** Use `shared/api/`. Consider entities only
  for complex transactional logic.
- **Do not create a `user` entity just for auth data.** Tokens and login DTOs
  belong in `shared/auth/` or `shared/api/`.
- **Do not abuse @x.** It is a last resort, not a recommended pattern
  (see Section 7).
- **Do not extract single-use code.** A feature or entity used by only one
  page should stay in that page.
- **Do not use technical-role file names.** Use domain-based names
  (see Rule 4-4).
- **Be cautious adding UI to entities.** Entity UI tempts cross-imports from
  other entities. If you add UI segments to entities, only import them from
  higher layers (features, widgets, pages) — never from other entities.
- **Do not create god slices.** Slices with excessively broad responsibilities
  should be split into focused slices (e.g., split `user-management/` into
  `auth/`, `profile-edit/`, `password-reset/`).

---

## 7. Cross-Import Resolution Order

When two slices on the same layer need to share code, try these strategies
**in order**. Always attempt earlier strategies first.

1. **Merge slices** — If two slices always change together, they likely belong
   in one slice.
2. **Extract shared logic to entities** — If multiple features/widgets share
   domain logic, move that logic to `entities/`. Keep UI in features/widgets.
3. **Compose in a higher layer (IoC)** — Use inversion of control. The parent
   layer (pages or app) imports both slices and connects them via render props,
   slots, or dependency injection.
4. **@x notation (last resort)** — Create explicit, controlled cross-imports
   between entities only. Document why other strategies do not apply. Review
   periodically.

For detailed code examples of each strategy, read
`references/cross-import-patterns.md`.

---

## 8. Segments & Structure Rules

### Standard segments

Segments group code within a slice by technical purpose:

- **`ui/`** — UI components, styles, display-related code
- **`model/`** — Data models, state stores, business logic, validation
- **`api/`** — Backend integration, request functions, API-specific types
- **`lib/`** — Internal utility functions for this slice
- **`config/`** — Configuration, feature flags

### Layer structure rules

- **App and Shared**: No slices — organized directly by segments. Segments
  within these layers may import from each other.
- **Pages, Widgets, Features, Entities**: Slices first, then segments inside
  each slice.

### File naming within segments

Always use domain-based names that describe what the code is about:

```text
model/user.ts            ← User types + logic + store
model/order.ts           ← Order types + logic + store
api/fetch-profile.ts     ← Profile fetching
api/update-settings.ts   ← Settings update
```

If a segment has only one domain concern, the filename may match the slice
name (e.g., `features/auth/model/auth.ts`).

---

## 9. Shared Layer Guide

Shared contains infrastructure with **no business logic**. It is organized by
segments only (no slices). Segments within shared may import from each other.

**Allowed in shared:**

- `ui/` — UI kit (Button, Input, Modal, Card)
- `lib/` — Utilities (formatDate, debounce, classnames)
- `api/` — API client, route constants, CRUD helpers, base types
- `auth/` — Auth tokens, login utilities, session management
- `config/` — Environment variables, app settings
- `assets/` — Images, fonts, icons

Shared **may** contain application-aware code (route constants, API endpoints,
branding assets, common types). It must **never** contain business logic,
feature-specific code, or entity-specific code.

---

## 10. Quick Reference

- **Import direction**: `app → pages → widgets → features → entities → shared`
- **Minimal FSD**: `app/` + `pages/` + `shared/`
- **Create entities when**: 2+ pages/features/widgets share the same business
  domain model, and the team agrees.
- **Create features when**: 2+ pages/widgets share the same user interaction,
  and the team agrees.
- **Breaking rules**: Only as an intentional design choice — document the
  reason, get team consensus.
- **Cross-import resolution**: Merge → Extract to entities → Compose in higher
  layer → @x (last resort)
- **File naming**: Domain-based (`user.ts`, `order.ts`). Never technical-role
  (`types.ts`, `utils.ts`).
- **Processes layer**: Deprecated. See `references/migration-guide.md`.

---

## 11. Conditional References

Read the following reference files **only** when the specific situation applies.
Do **not** preload all references.

- **When creating, reviewing, or reorganizing folder and file structure** for
  FSD layers and slices (e.g., "set up project structure", "where does this
  folder go"):
  → Read `references/layer-structure.md`

- **When resolving cross-import issues** between slices on the same layer,
  evaluating the @x pattern, or dealing with excessive entity coupling:
  → Read `references/cross-import-patterns.md`

- **When migrating** from FSD v2.0 to v2.1, converting a non-FSD codebase to
  FSD, or deprecating the processes layer:
  → Read `references/migration-guide.md`

- **When integrating FSD with a specific framework** (Next.js, Nuxt, Vite,
  CRA) or configuring path aliases:
  → Read `references/framework-integration.md`

- **When implementing concrete code patterns** for authentication, API request
  handling, type definitions, or state management (Redux, React Query) within
  FSD structure:
  → Read `references/practical-examples.md`
  Note: If you already loaded `layer-structure.md` in this conversation,
  avoid loading this file simultaneously. Address structure first, then load
  patterns in a follow-up step if needed.
