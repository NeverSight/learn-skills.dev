---
name: create-feature
description: Plan and implement a complete feature using spec-driven development. Analyzes requirements, designs data model, selects Buildpad components, and produces spec artifacts (requirements.md, design.md, tasks.md) with a testing strategy. Use when the user wants to add a new feature, module, or capability to an existing DaaS project.
argument-hint: "[feature name] [description]"
---

# Create Feature

Plan and coordinate implementation of a complete feature using **spec-driven development** (see the `spec-driven-development` skill).

> **BEFORE generating ANY `.tsx` files** (pages, components, forms, lists), you MUST `read_file` the Buildpad component reference at `.github/skills/buildpad-reference/SKILL.md`. This loads the full 40+ component catalog with import paths and usage patterns. Skipping this step leads to raw Mantine usage violations.

## Spec Workflow

Every feature gets spec artifacts in `.kiro/specs/<feature-name>/` before implementation. In Kiro, use native specs; in other IDEs, run `/buildpad-spec-init` → `/buildpad-spec-requirements` → `/buildpad-spec-design` → `/buildpad-spec-tasks` → `/buildpad-impl`. The DaaS-specific planning below feeds those artifacts:

| Stage           | Focus                        | Artifact          |
| --------------- | ---------------------------- | ----------------- |
| **Requirements**| Problem, users, acceptance criteria (EARS) | `requirements.md` |
| **Design**      | Data model, API, UI, Buildpad components   | `design.md`       |
| **Tasks**       | Ordered, verifiable tasks with tests       | `tasks.md`        |
| **Implement**   | Task-by-task with review                   | Working code      |

## Planning Process

1. **Understand Requirements** — What problem does this solve? Who are the users?
2. **Check Built-In DaaS Features** — Before designing anything, review the [Built-in DaaS features reference](../daas-platform/references/builtin-features.instructions.md). If DaaS provides it natively (audit trail, workflow, versioning, file management, cron, RBAC, scoping, import/export), use it — do NOT rebuild it. On an Engine project the Engine provides them; where one differs there (scheduled cron runs, for example), the checklist below and the skill for that feature say so.
3. **Design Data Model** — Collections, fields, types, relationships, permissions. For every collection, follow the [Standard Fields decision tree](../create-collection/references/standard-fields.instructions.md#decision-tree--which-field-groups-to-include): always include audit fields, add workflow fields if approval/lifecycle needed, add scope field if multi-tenancy needed.
4. **Plan API Endpoints** — CRUD routes with request/response formats
5. **Design UI** — Pages, components, user flows
6. **Select Components (Buildpad-First MANDATORY)** — Check Buildpad's 40+ components before creating custom
7. **Plan Implementation** — Numbered tasks with estimates
8. **Plan Testing** — API tests, page tests, component tests, E2E tests

### Feature Planning Checklist

For each collection in the feature, answer these questions during the design stage:

- [ ] **Audit fields included?** → ALWAYS yes (Group A: user_created, date_created, user_updated, date_updated)
- [ ] **Needs workflow/approval?** → Add Group B fields + plan `create-workflow` skill invocation
- [ ] **Needs multi-tenancy (data separated by scope)?** → Add Group C field + plan `manage-scope` skill invocation. On an Engine project the project is one tenant, and the scopes are levels below its tenant node.
- [ ] **Needs versioning?** → Plan DaaS versioning API integration (NOT custom version tables)
- [ ] **Needs scheduled tasks?** → Plan DaaS cron jobs (NOT Next.js cron routes). On an Engine project a cron job's body runs in the Engine's runtime: it has no `fetch`, `process`, `require` or timers, no Supabase service and no SQL; it reads and writes data through `services.items(collection)` (with `{ elevated: true }` where it must act as an administrator) and calls outside hosts through `services.fetch` (see [create-cron](../create-cron/SKILL.md)). On an Engine project an active cron job fires at its scheduled time.
- [ ] **Needs capability/role gating?** → Plan Module-Level Access Keys (`grant-module-access` skill): register key in `daas_module_access_keys`, grant on policy `module_access` JSONB, check in React with `usePermissions().hasModuleAccess(key)`. **NEVER check role names directly** — this applies to every button, section, page, or nav item that is conditionally shown/hidden based on role.
- [ ] **Needs audit/change tracking?** → Already built-in via `GET /api/activity` (do NOT build custom)

On an Engine project some files the Buildpad CLI generates cannot be used yet: `lib/supabase/admin.ts`, the OAuth callback and provider routes of the `external-oauth` module, the server-side enforcer and session modules, and `lib/module-access/enforce.ts`. Do not call them; check module access by forwarding the user's token to `GET <Engine_URL>/api/permissions/me` and reading `isAdmin` and `moduleAccess`. For XAppHub sign-in the CLI installs the `external-oauth-engine` module in place of `external-oauth`; its routes are used as the `add-external-oauth` skill says.

## Buildpad Component Selection

| Need              | Buildpad Component                                              |
| ----------------- | --------------------------------------------------------------- |
| Text input        | `Input`, `Textarea`                                             |
| Rich text         | `RichTextHtml`, `RichTextMarkdown`                              |
| Select/dropdown   | `SelectDropdown`, `SelectRadio`                                 |
| Multi-select      | `SelectMultipleDropdown`, `Tags`                                |
| Toggle            | `Toggle`, `Boolean`                                             |
| Date/time         | `DateTime`                                                      |
| File upload       | `FileInterface`, `FileImage`, `Files`                           |
| Relations         | `ListM2O`, `ListM2M`, `ListO2M`, `ListM2A`                      |
| Dynamic form      | `VForm`, `CollectionForm`                                       |
| Listing records   | `CollectionList` (with search, filter, pagination, permissions) |
| Filtering records | `FilterPanel` (field-type-aware, DaaS-compatible JSON output)   |
| Aggregate/stats   | DaaS aggregate API (`aggregate[count]=id&groupBy=status`), on either kind of project |

Custom components allowed ONLY for: app-specific layouts, dashboards, specialized visualizations.

## CollectionList Usage (MANDATORY for list pages)

When the design includes a list page, you MUST use `CollectionList` with the full-featured pattern.
Do NOT create custom tables with Mantine `<Table>` or raw HTML for collection records.

```tsx
import { CollectionList } from "@/components/ui";

<CollectionList
  collection="articles"
  enableSearch
  enableFilter // Integrated FilterPanel with badge count
  enableSelection // Row selection with bulk actions
  enableCreate // Permission-gated create button
  enableDelete // Built-in delete with confirmation modal
  enableSort
  enableResize
  enableReorder
  enableHeaderMenu
  limit={25}
  onCreate={() => router.push("/content/articles/+")}
  onItemClick={(item) => router.push(`/content/articles/${item.id}`)}
/>;
```

Key features: integrated search + FilterPanel toggle with badge, permission-gated create/bulk actions,
pagination (25/50/100/250), field-type-aware cell rendering, column management.

## VForm Usage (CRITICAL)

When the design includes a form page, you MUST follow the VForm controlled component pattern.
See [VForm usage reference](references/vform-usage.instructions.md) for the required pattern.

**Key rules:**

- VForm has NO `onSubmit` prop — pass `modelValue` + `onUpdate` for controlled state
- VForm renders a `<div>`, NOT a `<form>` — do NOT use `type="submit"` or `form="vform"`
- Handle submission externally via `onClick` on a Button
- Consider `CollectionForm` as an all-in-one alternative to VForm for CRUD pages

## Scope-Aware Context Pattern (REQUIRED when feature has scoped data)

On an Engine project the project is one tenant. Every scope hierarchy begins below the project's tenant node: create no scope type without a parent and no scope item without a parent. Scope types, items and collection settings are managed through `/api/scope/types`, `/api/scope/items` and `/api/scope/collection-config` with an administrator's session; the MCP `scope` tool, served to an administrator only, assigns a role to a user at a scope (`assign_user_role`) and registers a collection as tenanted (`create_config`, the body of `POST /api/scope/collection-config`). On a Supabase project the scope hierarchy is the project's own, as `manage-scope` describes.

> **Bug 26:** Any React context or component that calls DaaS on mount AND lives inside `ScopeProvider` must wait for the scope to be ready before fetching. Firing the request before the `daas_resource_uri` cookie is set results in a 401. The `.catch()` handler will have set state to `false`/empty, and the effect will NOT re-run unless `scopeLoading` is in the dependency array.

When implementing a new context/provider that fetches from DaaS:

```tsx
import { useScope } from '@/lib/contexts/ScopeContext';

const { resourceUri, isLoading: scopeLoading } = useScope();

useEffect(() => {
  if (scopeLoading) return; // ← REQUIRED guard — do not remove

  apiRequest('/api/...')
    .then(...)
    .catch(...);

  // Re-fetch when the scope changes (policies/data may differ per scope)
}, [version, resourceUri, scopeLoading]);
//             ^^^^^^^^^^  ^^^^^^^^^^^  ← REQUIRED deps
```

## Output Format

Provide a structured plan with:

- Overview and requirements
- Data model design
- API design
- UI design with Buildpad components
- Capability matrix (required for role-gated features):
  - module key (`domain:capability`)
  - granted policies
  - UI guard points (`hasModuleAccess`)
  - API guard points (policy module_access OR-merge; on an Engine project, the user's token forwarded to `GET <Engine_URL>/api/permissions/me`)
- Implementation tasks in `tasks.md`, ordered by dependency layer
- Testing strategy per layer
- Time estimates

## Testing Strategy (per layer)

- **Schema**: API tests for all endpoints
- **UI**: Page tests for all pages
- **Logic**: Integration tests for business rules
- **Hardening**: E2E tests for user flows

## Post-Generation Validation (MANDATORY)

After generating ANY `.tsx` files for this feature, run the Buildpad-First violation check:

```bash
# Scan generated files for forbidden raw Mantine form/input imports
grep -rn "from '@mantine/form'\|from '@mantine/dates'\|from '@mantine/dropzone'\|<TextInput\|<NumberInput\|<Select \|<Switch \|<Checkbox \|<DatePicker\|<Dropzone" app/ components/ 2>/dev/null
```

**If any matches are found, replace them with Buildpad equivalents before proceeding.**

Then run module-access anti-pattern checks (UI + API):

```bash
grep -rn "role === \|roleName\|user\.role\|is_manager\|is_admin\|isManager\b\|currentUser\.role" app/ components/ 2>/dev/null
grep -rn "detectAdminFromMe\|checkAdmin\|roleObj\.name === 'Administrator'\|admin_access\s*===\s*true\|\bisAdmin\b" app/ components/ 2>/dev/null
```

Any match used for capability gating must be replaced with Module-Level Access Keys checks.

Quick fix reference:
| Violation | Replace With |
|---|---|
| `<TextInput>` / `<Textarea>` | `Input` / `Textarea` from `@/components/ui` |
| `<Select>` | `SelectDropdown` from `@/components/ui` |
| `<DatePicker>` | `DateTime` from `@/components/ui` |
| `<Switch>` / `<Checkbox>` | `Toggle` / `Boolean` / `SelectMultipleCheckbox` |
| `<Dropzone>` | `Upload` / `Files` from `@/components/ui` |
| `useForm` (@mantine/form) | `VForm` or `CollectionForm` from `@/components/ui` |
| Custom `<Table>` for records | `CollectionList` from `@/components/ui` |

For capability gating rules, load and follow:
- `../grant-module-access/SKILL.md`
- `../../references/module-access-checklist.md`
