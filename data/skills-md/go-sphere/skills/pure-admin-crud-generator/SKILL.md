---
name: pure-admin-crud-generator
description: Generate CRUD pages and router modules for pure-admin-thin from local swagger API definitions. MUST be used whenever you need to scaffold admin list/edit/detail pages, dashboard views, or route configurations from existing API methods in src/api/swagger/Api.ts. This skill replaces manual Vue page creation - use it for any admin panel development task involving API-driven pages.
---

# Pure Admin Thin CRUD Generator

## Overview
Generate runnable Vue pages under `src/views/<module>/` and route modules under `src/router/modules/` from local swagger-ts-api output in `src/api/swagger/Api.ts` and API wrapper behavior in `src/api/api.ts`.

This is an AI-first generator skill. Do not use external OpenAPI generators and do not add helper codegen scripts.

## When to Use
**ALWAYS use this skill** when the user asks to scaffold or update pure-admin-thin admin pages, including:

- CRUD pages (`index.vue`, `edit.vue`, optional `detail.vue`)
- dashboard-first admin pages
- route module files under `src/router/modules`
- action buttons backed by non-CRUD APIs (retry/enable/disable/export etc.)
- ANY admin management interface in a pure-admin-thin project

**Trigger examples:**
- "Generate admin pages for user management"
- "Create CRUD for voice-features module"
- "Add dashboard view for analytics"
- "Scaffold edit and detail pages for product management"
- "Generate route module and views for order management"

## Hard Gates
These are non-optional. If any gate fails, stop and report blocking issues.

1. Parse and generate from local `Api.ts` + `api.ts` only.
2. Do not regenerate API clients with external tools.
3. Do not create reusable business UI component libraries.
4. Use Element Plus components for page UI.
5. Do not add runtime dependencies only for generated pages.
6. Keep repository conventions first; only fallback to generic heuristics if local patterns are missing.
7. Page `name` must match route `name` for keepAlive to work.
8. Route `name` must be unique across the application.
9. Use `satisfies RouteConfigsTable` for route module type safety.

## Progressive Reference Loading

### Phase 1: Always Read First
1. [references/output-contract.md](references/output-contract.md) - Output format requirements
2. [references/api-parsing-rules.md](references/api-parsing-rules.md) - API classification rules

### Phase 2: Load On Demand
1. `pageMode=crud` or `mixed`: [references/page-generation-spec.md](references/page-generation-spec.md)
2. `pageMode=dashboard`: [references/dashboard-best-practices.md](references/dashboard-best-practices.md)
3. Need RBAC permissions: [references/rbac-permissions.md](references/rbac-permissions.md)
4. Need type declarations: [references/type-declarations.md](references/type-declarations.md)

### Phase 3: Final Gate
Run through [references/completion-checklist.md](references/completion-checklist.md) before output.

## Input Contract
Required and optional generation inputs:

- `moduleSelector` (required): module tag/entity/path keyword (e.g., "user", "voice-features", "order").
- `selectorMode` (optional, default `auto`): `auto | tag | entity | path`.
- `forceDetailPage` (optional, default `auto`): `auto | true | false`.
- `pageMode` (optional, default `crud`): `crud | dashboard | mixed`.
- `routeBase` (optional, default `/<kebab-module>`).
- `outputMode` (fixed): full file contents only.

**Examples:**
- User says: "Generate pages for user management" → `moduleSelector="user"`, infer module from API tags
- User says: "Create dashboard for voice-generate-text" → `moduleSelector="voice-generate-text"`, `pageMode="dashboard"`
- User says: "Add edit page for product module" → `moduleSelector="product"`, generate edit.vue + route module

If the user provides only a vague module name, resolve with `selectorMode=auto` and explicitly state matched methods.

## Repository Facts
Use these local assumptions first:

- API calls go through `API` from `src/api/api.ts`.
- `API` already unwraps axios response once.
- Swagger methods are under `new Api().api` in `src/api/swagger/Api.ts`.
- Method doc blocks include `@tags`, `@name`, `@summary`, `@request`.
- Routes are auto-collected via `import.meta.glob("./modules/**/*.ts")`; route index edits are usually unnecessary.

## Workflow

### Quick Path (Simple CRUD)
For simple CRUD operations with clear API patterns:
1. Parse API definitions (list, detail, create, update, delete endpoints)
2. Infer data structures from response types
3. Generate standard file set: `index.vue`, `edit.vue`, route module
4. Skip detailed validation notes
5. Use condensed output format

### Full Path (Complex/Dashboard)
For dashboard pages, custom actions, or complex workflows:
1. Parse API definitions with full classification
2. Analyze data structures and relationships
3. Plan file set based on `pageMode`
4. Generate pages with full error/retry handling
5. Apply dashboard best practices if needed
6. Use full output format with capability matrix

## Output Contract

### Condensed Output (Simple Tasks)
For straightforward CRUD with clear API patterns, use:

1. **Recognized APIs** - Brief list of matched endpoints
2. **Files** - File paths
3. **File Contents** - Full Vue files
4. **Route Registration** - Brief route module

### Full Output (Complex Tasks)
For dashboards or complex pages, include all sections:

1. **Scaffold Fit Decision** - Module config summary
2. **Recognized APIs** - Full endpoint list with classification
3. **API Capability Matrix** - What operations are available
4. **Files** - File paths
5. **File Contents** - Full Vue files
6. **Route Registration** - Full route module with meta
7. **Validation Notes** - Assumptions and risks
8. **Blocking Issues** - Only if any gate fails

Use [references/output-contract.md](references/output-contract.md) for detailed format.

## Degrade Gracefully
When full CRUD is not available:

- Generate only valid pages/operations based on available endpoints
- Remove unsupported actions from UI (e.g., no delete button if no delete endpoint)
- Explicitly report missing CRUD endpoints in output
- Keep code runnable even when some operations are unavailable

**Common degradation scenarios:**
- Only list endpoint → generate list page only, disable create/edit/delete buttons
- List + create only → generate index + edit (create mode), no edit for existing items
- No detail endpoint → omit detail page or disable view action

## Optional VueUse Policy
VueUse composables are optional. Use them only when complexity justifies it and `@vueuse/core` already exists in the project.

- do not add dependency automatically
- keep manual `ref/reactive` flow for simple pages
- when available in this session, `vueuse-functions` can be used for composable selection patterns

## Completion Checklist
Before returning, verify ALL of the following:

1. **Output format**: Section order matches output contract (condensed or full based on task complexity)
2. **Type safety**: Generated files compile under `pnpm typecheck`
3. **Pagination**: Internal state is 0-based, UI displays 1-based (`pageIndex + 1`)
4. **Route id handling**: Invalid id shows error message, does NOT silently fallback to create mode
5. **Filters**: Only include filters that match real API query parameters
6. **Delete safety**: All delete/destructive actions use `ElMessageBox.confirm`
7. **Runtime safety**: Uncertain API fields use `Array.isArray()` guards
8. **Missing endpoints**: Explicitly report which CRUD operations are unavailable
9. **Route module**: Root route redirects to `/index`, hidden routes use `showLink: false`
10. **Page name**: Vue component `name` matches route `name` for keepAlive
11. **Dashboard quality** (if dashboard mode): Has filter + metrics + main content + actions, per-region retry
12. **Route uniqueness**: No duplicate route names across the application
