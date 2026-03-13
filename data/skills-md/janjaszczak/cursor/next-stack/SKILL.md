---
name: next-stack
description: >
  Next.js App Router frontend stack workflow: Server Components-first, Prisma server-only (Node runtime),
  Tailwind + shadcn/ui, TanStack Query, React Hook Form + Zod, and conventions for work under frontend/.
  Use when implementing or refactoring UI, routes, data fetching, mutations, or forms in this stack.
compatibility: Cursor Agent Skills (Nightly). Next.js App Router. Prisma requires Node runtime (not Edge).
metadata:
  stack: "Next.js App Router + Tailwind + shadcn/ui + TanStack Query + RHF + Zod + Prisma"
  scope: "frontend/**"
  author: janjaszczak
  version: "1.0"
---

# Next Stack (App Router + Prisma + TanStack Query)

## Intent
Provide a **consistent decision framework + implementation checklist** for this stack, so changes stay:
- correct in server/client boundaries,
- consistent with UI & data patterns,
- testable and PR-ready.

## When to use
Activate this skill when the task involves any of:
- Next.js App Router pages/layouts/route handlers/server actions
- Prisma-backed reads/writes
- client mutations, optimistic UI, live updates (TanStack Query)
- forms & validation (RHF + Zod)
- shadcn/ui + Tailwind components under `frontend/`

## Non-negotiables (stack rules)
1) **Server Components first**
- Default to Server Components.
- Add `"use client"` only when you need interactivity, local state, effects, or client-only libraries.

2) **Prisma is server-only**
- Never import Prisma in Client Components.
- Ensure any Prisma usage runs in **Node runtime** (not Edge):
  - For Route Handlers that might run on Edge, explicitly set:
    - `export const runtime = "nodejs"` (where applicable in your codebase conventions).

3) **Data fetching split**
- Prefer server-side reads (RSC, route handlers, server actions) for static/deterministic reads.
- Use TanStack Query for:
  - mutations,
  - optimistic flows,
  - client revalidation,
  - “live-ish” / frequently changing UI state.

4) **React Query hygiene**
- Stable, deterministic query keys (no unstable objects in keys).
- Precise invalidation (invalidate the smallest relevant scope).

5) **Forms & validation**
- Use **React Hook Form + Zod resolver**.
- Maintain **one Zod schema** shared between client & server.
- Server must re-validate (do not trust client).

6) **Styling & UI**
- Tailwind default.
- shadcn/ui lives under `frontend/components/ui/*`.
- Preserve accessibility props/labels and semantic structure.

7) **Conventions**
- ESLint (AirBnB-style) + Prettier.
- React component files in PascalCase (e.g., `UserCard.tsx`).
- Prefer **named exports** (unless Next.js route file conventions force defaults).

## Workflow (how to execute tasks in this stack)
### Step 1 — Clarify & make it verifiable
- Ask 1–3 clarifying questions if critical requirements are missing.
- Define acceptance criteria as verifiable checks:
  - “what page shows what state”
  - “what API returns what”
  - “which tests prove it”

### Step 2 — Decide server vs client boundary
Choose the minimum client surface area:
- If no interactivity: stay in RSC.
- If interaction/mutation: isolate `"use client"` to the smallest component subtree.

### Step 3 — Pick the data path
**Reads**
- Prefer RSC/server fetch.
- Be explicit about caching behavior for user-specific or frequently changing data:
  - use `cache: "no-store"` / revalidate strategy as appropriate to the app conventions.

**Writes / mutations**
- Implement server action or route handler as the mutation boundary.
- Client uses React Query `useMutation` and invalidates exact keys.

### Step 4 — Implement with shared schema
- Create/locate a shared `zod` schema module (single source of truth).
- Client:
  - RHF + zodResolver(schema)
- Server:
  - schema.parse(...) (or safeParse with structured error return)

### Step 5 — UI integration (shadcn + Tailwind)
- Use shadcn components for primitives; Tailwind for layout/spacing.
- Keep a11y intact: labels, aria attributes, keyboard focus, form errors.

### Step 6 — Verification
Before finalizing:
- run lint + typecheck
- unit/component tests (Vitest + RTL) where applicable
- Playwright e2e for critical flows

(Use the repo’s package manager and scripts; inspect `package.json` / lockfiles and follow existing patterns.)

### Step 7 — PR output expectations
PR should include:
- runnable code and relevant tests,
- a short rationale: what you changed, why it matches this stack,
- explicit trade-offs (e.g., “RSC read chosen over React Query because X”).

## Anti-patterns (reject these)
- Prisma imported from any Client Component module graph
- Blanket `"use client"` at high-level layouts/pages without necessity
- React Query used for deterministic static reads with no client interactivity need
- Unstable query keys (objects/functions/dates) causing cache misses
- Over-broad invalidation (invalidate everything) instead of precise keys
- Duplicate schemas (one for client, one for server)

## Quick decision rules
- Start with RSC; promote to client only when you hit a real constraint.
- If Prisma is involved, ensure Node runtime and keep the boundary server-side.
- If you need optimistic UI or repeated client refresh, use React Query—but keep keys stable and invalidation precise.
