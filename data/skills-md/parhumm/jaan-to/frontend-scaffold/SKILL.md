---
name: frontend-scaffold
description: Convert designs to React/Next.js components with TailwindCSS, TypeScript, and typed API hooks. Use when scaffolding frontend from designs.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/frontend/**), Task, WebSearch, AskUserQuestion, Edit(jaan-to/config/settings.yaml)
argument-hint: [frontend-design, frontend-task-breakdown, backend-api-contract]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# frontend-scaffold

> Convert designs and specs into production-ready React/Next.js component scaffolds with typed API hooks.

## Context Files

- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack context (CRITICAL — determines framework, styling, versions)
  - Uses sections: `#current-stack`, `#frameworks`, `#constraints`
- `$JAAN_CONTEXT_DIR/design.md` - Design system guidelines (optional)
- `$JAAN_CONTEXT_DIR/brand.md` - Brand guidelines (optional)
- `$JAAN_TEMPLATES_DIR/jaan-to-frontend-scaffold.template.md` - Output template
- `$JAAN_LEARN_DIR/jaan-to-frontend-scaffold.learn.md` - Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Upstream Artifacts**: $ARGUMENTS

Accepts 1-3 file paths or descriptions:
- **frontend-design** — Path to HTML preview or component description (from `/jaan-to:frontend-design` output)
- **frontend-task-breakdown** — Path to FE task breakdown (from `/jaan-to:frontend-task-breakdown` output)
- **backend-api-contract** — Path to OpenAPI YAML (from `/jaan-to:backend-api-contract` output)
- **Empty** — Interactive wizard
- Cross-role: optionally consumes `/jaan-to:ux-microcopy-write` output

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `frontend-scaffold`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read context files if available:
- `$JAAN_CONTEXT_DIR/tech.md` — Know the tech stack for framework-specific code generation
- `$JAAN_CONTEXT_DIR/design.md` — Know the design system patterns
- `$JAAN_CONTEXT_DIR/brand.md` — Know brand colors, fonts, tone

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_frontend-scaffold`

> **Language exception**: Generated code output (variable names, code blocks, schemas, SQL, API specs) is NOT affected by this setting and remains in the project's programming language.

---

# PHASE 1: Analysis (Read-Only)

## Thinking Mode

ultrathink

Use extended reasoning for:
- Analyzing design artifacts to derive component architecture
- Mapping API contract schemas to TypeScript interfaces and hooks
- Planning Server Component vs Client Component boundaries
- Identifying accessibility requirements per component

## Step 1: Validate & Parse Inputs

For each provided path:
- **frontend-design**: Read HTML preview or component description, extract component list, layout, interactions
- **frontend-task-breakdown**: Read markdown, extract component inventory, state matrices, estimates, dependencies
- **backend-api-contract**: Read OpenAPI YAML, extract schemas for TypeScript interfaces, endpoints for API hooks
- Report which inputs found vs missing; suggest fallback for missing

Present input summary:
```
INPUT SUMMARY
─────────────
Sources Found:    {list}
Sources Missing:  {list with fallback suggestions}
Components:       {extracted component names with atomic level}
API Endpoints:    {count from API contract}
TypeScript Types: {count derivable from schemas}
```

## Step 2: Detect Tech Stack

Read `$JAAN_CONTEXT_DIR/tech.md`:
- Extract frontend framework from `#current-stack` (default: React v19 + Next.js v15)
- Extract styling approach (default: TailwindCSS v4)
- Extract state management, testing tools
- If tech.md missing: ask framework/styling via AskUserQuestion

## Step 3: Design System Check

Read `$JAAN_CONTEXT_DIR/design.md` and `$JAAN_CONTEXT_DIR/brand.md` if available:
- Extract color tokens, typography, spacing scale
- Identify existing component patterns to extend
- Note brand guidelines affecting component appearance

## Step 4: Clarify Architecture

AskUserQuestion for items not in tech.md or design.md:
- State management (TanStack Query only / + Zustand / + URL state via nuqs)
- Routing (App Router / Pages Router / custom)
- Testing (Vitest + Testing Library / Playwright / both)
- Responsive strategy (mobile-first / desktop-first / adaptive)

## Step 5: Plan Component Tree

Present component tree with atomic design levels:
```
COMPONENT TREE
══════════════

STACK: {framework} + {styling} + {state_management}

COMPONENTS ({count} total)
──────────────────────────
Atoms:     {list with estimates}
Molecules: {list with estimates}
Organisms: {list with estimates}
Templates: {list}
Pages:     {list}

API HOOKS ({count})
───────────────────
{list of TanStack Query hooks with endpoints}

TYPES ({count})
───────────────
{list of TypeScript interfaces from API schemas}
```

---

# HARD STOP — Review Scaffold Plan

Use AskUserQuestion:
- Question: "Proceed with generating the frontend scaffold?"
- Header: "Generate"
- Options:
  - "Yes" — Generate the scaffold code
  - "No" — Cancel
  - "Edit" — Let me revise the component tree or architecture first

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Phase 2 Output — Flat folder

All files in `$JAAN_OUTPUTS_DIR/frontend/scaffold/{id}-{slug}/`:

```
{id}-{slug}/
├── {id}-{slug}.md                     # Main doc (architecture + component map)
├── {id}-{slug}-components.tsx          # React components
├── {id}-{slug}-hooks.ts               # Typed API client hooks
├── {id}-{slug}-types.ts               # TypeScript interfaces from API schemas
├── {id}-{slug}-pages.tsx               # Page layouts / routes
├── {id}-{slug}-config.ts              # Package.json + tsconfig + tailwind config
└── {id}-{slug}-readme.md              # Setup + run instructions
```

## Step 7: Generate Content

Read `$JAAN_TEMPLATES_DIR/jaan-to-frontend-scaffold.template.md` and populate all sections based on Phase 1 analysis.

If tech stack needed, extract sections from tech.md:
- Current Stack: `#current-stack`
- Frameworks: `#frameworks`
- Constraints: `#constraints`

## Step 8: Quality Check

Validate generated output against checklist:
- [ ] All components from task breakdown inventory generated
- [ ] Server Components default; `'use client'` only where needed
- [ ] TypeScript interfaces match API contract schemas
- [ ] TanStack Query hooks for client-side data fetching
- [ ] Loading/error/empty/success states on all data components
- [ ] Accessibility: ARIA, semantic HTML, keyboard nav
- [ ] No anti-patterns present in generated code
- [ ] Framework-implied build dependencies included (e.g., `babel-plugin-react-compiler` when `reactCompiler: true`)

If any check fails, fix before preview.

## Step 9: Preview & Approval

Present generated output summary. Use AskUserQuestion:
- Question: "Write scaffold files to output?"
- Header: "Write Files"
- Options:
  - "Yes" — Write the files
  - "No" — Cancel
  - "Refine" — Make adjustments first

## Step 10: Generate ID and Folder Structure

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/frontend/scaffold"
mkdir -p "$SUBDOMAIN_DIR"
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")
slug="{project-name-slug}"
OUTPUT_FOLDER="${SUBDOMAIN_DIR}/${NEXT_ID}-${slug}"
```

Preview output configuration:
> **Output Configuration**
> - ID: {NEXT_ID}
> - Folder: `$JAAN_OUTPUTS_DIR/frontend/scaffold/{NEXT_ID}-{slug}/`
> - Main file: `{NEXT_ID}-{slug}.md`

## Step 11: Write Output

1. Create output folder: `mkdir -p "$OUTPUT_FOLDER"`
2. Write all scaffold files to `$OUTPUT_FOLDER`
3. Update subdomain index:
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${slug}" \
  "{Project Title}" \
  "{Executive summary — 1-2 sentences}"
```

4. Confirm completion:
> Scaffold written to: `$JAAN_OUTPUTS_DIR/frontend/scaffold/{NEXT_ID}-{slug}/`
> Index updated: `$JAAN_OUTPUTS_DIR/frontend/scaffold/README.md`

## Step 12: Suggest Next Actions

> **Scaffold generated successfully!**
>
> **Next Steps:**
> - Copy scaffold files to your project directory
> - Run `npm install` to install dependencies
> - Run `/jaan-to:dev-integration-plan` to plan integration with existing code
> - Run `/jaan-to:dev-test-plan` to generate test plan
> - Run `/jaan-to:qa-test-cases` to generate test cases

## Step 13: Capture Feedback

Use AskUserQuestion:
- Question: "How did the scaffold turn out?"
- Header: "Feedback"
- Options:
  - "Perfect!" — Done
  - "Needs fixes" — What should I improve?
  - "Learn from this" — Capture a lesson for future runs

If "Learn from this": Run `/jaan-to:learn-add frontend-scaffold "{feedback}"`

---

## Key Generation Rules (Research-Informed)

**React 19 Patterns (CRITICAL — differs from React 18):**
- Server Components are default — only add `'use client'` when needed
- `async/await` in Server Components, NOT `useEffect` + `useState`
- `use(promise)` with Suspense, NOT `useEffect`; never create promises during render (infinite loops)
- `ref` is a regular prop, NOT `forwardRef`
- React Compiler (stable v1.0, October 2025) handles memoization — no `useMemo`/`useCallback`/`React.memo`; enable in `next.config.ts` with `{ reactCompiler: true }`; requires `babel-plugin-react-compiler` in devDependencies; up to 12% faster initial loads
- `useActionState` + `useFormStatus` (must be in **child component** of `<form>`) for forms
- Server Actions for mutations, ES6 default parameters (NOT `defaultProps`)
- `<Context.Provider>` deprecated — use `<Context>` directly
- `ref` callbacks support cleanup functions

**TailwindCSS v4 Patterns:**
- CSS-first config: `@import "tailwindcss"` + `@theme { }` — NO `tailwind.config.js`
- Dark mode: `@custom-variant dark (&:where(.dark, .dark *))` + `next-themes`
- `cn()` helper (clsx + tailwind-merge), OKLCH colors
- **v3→v4 breaking syntax**: `!bg-red-500` → `bg-red-500!` (suffix), `@layer utilities` → `@utility`, `bg-[--my-var]` → `bg-(--my-var)`; requires Safari 16.4+, Chrome 111+, Firefox 128+
- PostCSS uses `@tailwindcss/postcss` as single plugin — autoprefixer is built-in
- Content detection is automatic (no `content` array)

**Component Generation:**
- 4 states per data component: loading, error, empty, success
- Atomic Design: Atoms -> Molecules -> Organisms -> Templates
- Feature-based organization, `aria-*` on all interactive elements
- Minimum 24x24px touch targets (WCAG 2.2 AA); 44x44px recommended (AAA / mobile guideline)
- Use semantic HTML (`<button>`, `<nav>`, `<main>`) before ARIA; enforce with `eslint-plugin-jsx-a11y`

**API Integration:**
- **Orval** v7 for TypeScript types + TanStack Query hooks from OpenAPI (ready-to-use `useQuery`/`useMutation` with auto-generated keys)
- **Alternative**: `openapi-typescript` (~1.68M weekly downloads) generates only TypeScript types with zero runtime; companion `openapi-fetch` provides type-safe `createClient<paths>()` wrapper; requires manually writing TanStack Query hooks but offers more control
- TanStack Query v5 for client-side fetching; `HydrationBoundary` for RSC → client data handoff (prefetch with `queryClient.prefetchQuery()`, dehydrate cache, wrap in `<HydrationBoundary state={dehydrate(queryClient)}>`)
- Use `queryOptions()` factories for type-safe, reusable query definitions with hierarchical key factories
- Separate generated API code into `src/lib/api/generated/` — treated as dependency, never hand-edited
- Add `"generate:api": "orval --config ./orval.config.ts"` to package.json

**State Management:**
- Server/API data → TanStack Query v5
- Local state → `useState`/`useReducer`
- Global client state → Zustand v5 (no Provider needed, ~1KB gzip); use targeted selectors to minimize re-renders
- URL state → `nuqs` v2.5+ (used by Sentry, Supabase, Vercel); type-safe parsers, server-side via `createLoader()`
- Form state → `useActionState` + `useFormStatus`
- Optimistic UI → `useOptimistic` (React 19); instant UI feedback, auto-reconcile or rollback

**Next.js 15 Caching:**
- `fetch()` defaults to `no-store` (was `force-cache` in v14); opt into caching with `cache: 'force-cache'` or `next: { revalidate: 3600 }`
- `unstable_cache` deprecated — use `'use cache'` directive with `cacheTag()` and `cacheLife()`
- Server Actions for internal mutations; Route Handlers (`route.ts`) for external consumers
- ESLint 9 flat config (`eslint.config.mjs`) replaces `.eslintrc.json`

## Anti-Patterns to NEVER Generate

**React 19**: `useEffect` for data fetching, `forwardRef`, manual memoization (`useMemo`/`useCallback`/`React.memo`), `defaultProps`, `PropTypes`, `<Context.Provider>`

**Next.js 15**: `'use client'` everywhere, API routes for internal mutations, `unstable_cache` (deprecated — use `'use cache'` directive with `cacheTag()`/`cacheLife()`), `next lint` (removed in Next.js 16 — use ESLint CLI with `eslint.config.mjs` flat config)

**TailwindCSS v4**: `tailwind.config.js`, dynamic class construction, `@tailwind` directives, v3 bang syntax (`!bg-red-500`), `@layer utilities`

**Accessibility**: `<div onClick>`, missing `alt`, color-only indicators, missing form labels

## Package Dependencies (Research-Validated)

**Production**: `react` ^19, `react-dom` ^19, `next` ^15, `@tanstack/react-query` ^5.60, `zustand` ^5, `nuqs` ^2.5, `next-themes` ^0.4, `clsx` ^2.1, `tailwind-merge` ^2.6, `zod` ^3.23, `axios` ^1.7

**Dev**: `typescript` ^5.7, `@types/react` ^19, `@types/node` ^22, `@tailwindcss/postcss` ^4, `tailwindcss` ^4, `eslint` ^9, `prettier` ^3.4, `orval` ^7, `vitest` ^2, `@testing-library/react` ^16, `eslint-plugin-jsx-a11y`, `babel-plugin-react-compiler` (when `reactCompiler: true`)

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Framework-agnostic with `tech.md` detection
- Template-driven output structure
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] All components from frontend-task-breakdown inventory generated
- [ ] Server Components default; `'use client'` only where needed
- [ ] TypeScript interfaces from API contract schemas
- [ ] TanStack Query hooks for client-side data fetching
- [ ] Loading/error/empty/success states on all data components
- [ ] Accessibility: ARIA, semantic HTML, keyboard nav
- [ ] TailwindCSS v4 CSS-first config
- [ ] Responsive mobile-first breakpoints
- [ ] Setup README complete
- [ ] Output follows v3.0.0 structure
- [ ] Index updated with executive summary
- [ ] User approved final result
