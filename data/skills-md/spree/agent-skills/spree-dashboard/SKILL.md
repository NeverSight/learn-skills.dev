---
name: spree-dashboard
description: Use when customizing the Spree 6 admin — the React dashboard (`@spree/dashboard`, Developer Preview) in `apps/dashboard/` — from inside the project. Covers `defineDashboardPlugin` in `src/plugins.ts`, sidebar/settings nav, custom pages/routes, slot widgets on built-in pages, table columns/filters, extension form fields and custom field widgets, permission gating, calling the Admin API (`adminClient`, store-scoped query keys, 422 mapping), exposing a new attribute end-to-end, theming tokens, translations, Vitest/Playwright tests and deployment. Common phrasings include "add a page to the admin", "admin sidebar item", "add a column to the products table", "add a card to the product page", "custom field on the product form", "hide menu item by permission", "restyle the admin", "dashboard plugin", "spree add dashboard", "React admin", "where did spree_admin go".
---

# Spree Dashboard (React admin) — in-app customization

The Spree 6 admin is a React SPA that talks only to the Admin API (`/api/v3/admin/*`). It is a **Developer Preview** — packages are `1.0.0-beta.x` and APIs can still move, so check the installed barrel (`node_modules/@spree/dashboard-core/src/index.ts`) when a name doesn't resolve. The Rails `spree_admin` gem no longer exists; there are no ERB views, partials, Stimulus or Turbo to override.

This skill is for customizing **your own** dashboard app. To ship a customization as an npm package other stores install, see `spree-dashboard-plugins` (same APIs, different packaging).

## Where it lives

```
my-store/
├── server/                 # Rails app (Spree gems, Admin API) — `backend/` in older projects
└── apps/
    ├── dashboard/          # the "host app" — you own this
    │   ├── src/main.tsx        # mounts <Dashboard>, imports plugins + virtual:spree-dashboard-plugins
    │   ├── src/plugins.ts      # ← your registrations
    │   ├── src/styles.css      # @import "@spree/dashboard/styles.css" + your token overrides
    │   ├── src/routeTree.gen.ts  # generated on every dev start/build (and by `spree add`) — commit it
    │   └── vite.config.ts      # spreeDashboardPlugin() + /api proxy
    └── seller-dashboard/   # optional marketplace seller panel (same model)
```

- New project: `npx create-spree-app my-store` → answer Yes to the React Dashboard. Existing project: `spree add dashboard` (`--template <git-url|path>`, `--no-install`).
- Dev: `spree dev` runs the API; `cd apps/dashboard && pnpm dev` → http://localhost:5173. Sign in with an admin email/password — no API keys (JWT in memory + httpOnly refresh cookie). Vite proxies `/api` and `/rails` to `VITE_API_PROXY_TARGET` (default `http://localhost:3000`).
- Every page is store-scoped: URLs are `/$storeId/...`. Registered paths are written **without** the store prefix.

Stack: Vite, React 19, TanStack Router (file-based) + TanStack Query v5, React Hook Form + Zod, Tailwind v4 + shadcn/ui + Base UI, lucide-react icons, i18next, Biome, `@spree/admin-sdk`.

### Packages — import from `@spree/dashboard`

| Package | Contains |
|---|---|
| `@spree/dashboard-ui` | Design system: shadcn primitives, `ResourceLayout`, `Empty*`, `RelativeTime`, `useConfirm`, tokens. Props in, no providers. |
| `@spree/dashboard-core` | Framework: registries, `defineDashboardPlugin`, providers/hooks (`useAuth`, `usePermissions`, `useStore`), `adminClient`, `ResourceTable`, `PageHeader`, `Slot`. |
| `@spree/dashboard` | The app shell (routes, resource pages, locales) **and** a facade re-exporting both packages above. |

In the host app, always `import { … } from '@spree/dashboard'`. Only a distributed plugin imports `-core`/`-ui` directly, and then only from their package entry points, never deep file paths. The packages ship source, and a deep import makes Vite leave a CommonJS dependency unconverted in an installed app, so the dashboard dies before rendering (1.0.0-beta.4's setup screen hit exactly this). Full list: [references/public-api.md](references/public-api.md).

### Where code goes (starter convention)

| Path | Holds |
|---|---|
| `src/plugins.ts` | Registrations only — a map of what you added |
| `src/pages/` | One screen per file |
| `src/hooks/` | Admin API wrappers (`use-brands.ts`) — components never call `adminClient` directly |
| `src/tables/` | `defineTable` calls |
| `src/schemas/` | Zod schemas + form value types |
| `src/slots/` | Widgets injected into built-in pages |
| `src/locales/` | Your `admin.*` translation bundles |

## `defineDashboardPlugin` — the one entry point

```tsx
// src/plugins.ts
import { defineDashboardPlugin, i18n } from '@spree/dashboard'
import { BarChartIcon } from 'lucide-react'
import en from './locales/en.json'
import { AnalyticsPage } from './pages/analytics'

i18n.addResourceBundle('en', 'translation', en, true, true) // translations first

defineDashboardPlugin({
  nav: [{ key: 'analytics', labelKey: 'admin.analytics.nav', path: '/analytics', icon: BarChartIcon, position: 650 }],
  routes: [{ key: 'analytics', path: '/analytics', component: AnalyticsPage }],
})
```

| Key | Does |
|---|---|
| `locales` | `{ en: bundle, de: bundle }` — registered before everything else in the call |
| `nav` | Array (adds) or `{ add, remove, update, addChildren }` |
| `settingsNavGroups` / `settingsNav` | Settings sub-shell groups, then entries (array or `{ add, remove, update }`) |
| `routes` | Runtime-registered pages under `/$storeId/…` |
| `slots` | `{ 'slot.name': [{ id, component, position?, if? }] }` |
| `tables` | `{ products: { add, update, remove } }` column mutations |
| `formFields` | `{ product: [{ name, from }] }` extension fields on built-in forms |
| `customFieldComponents` | `{ 'namespace.key': Component }` custom widgets for custom field definitions |

Registries are module singletons. Keys/ids must be unique (including against built-ins) — duplicates **throw at boot**; the facade collects every error and rethrows once (`AggregateError`). Each registry also has an imperative API (`nav.add`, `registerSlot`, `tables.products.addColumn`, …) — use it for fine control or strongly typed slots.

## Navigation

```ts
import { nav, settingsNav } from '@spree/dashboard'

nav.addChild('products', { key: 'products.brands', labelKey: 'admin.brands.nav', path: '/brands', subject: 'Spree::Brand' })
nav.insertAfter('orders', { key: 'returns-hub', label: 'Returns hub', path: '/returns-hub' })
nav.update('orders', { position: 150 })
nav.remove('loyalty')
nav.add({ key: 'help', label: 'Help', path: '/help', section: 'bottom' })       // pinned to the footer
nav.add({ key: 'onboarding', label: 'Onboarding', path: '/onboarding',
  if: ({ store }) => !isConfigured(store), badge: PendingCountBadge })        // badge is a component
```

- `NavEntry`: `key`, `label` | `labelKey`, `path` (required, leading `/`), `icon`, `section` (`'main'`|`'bottom'`), `position`, `subject` + `action` (default `'read'`), `if`, `badge`, `children`.
- Built-in top-level keys/positions: `getting-started` 50, `home` 100, `orders` 200, `products` 300, `inventory` 350, `customers` 400, `sellers` 450, `loyalty` 475, `promotions` 500, `reports` 600, `settings` (bottom). Use 650+ to append.
- `update(parent, { children })` **replaces** children — use `addChild` / `addChildren` to nest under a built-in menu.
- Prefer `labelKey` over `label: i18n.t(...)`: a literal label is frozen at registration and won't follow a language switch.
- Settings groups: `store`, `selling`, `shipping`, `marketplace`, `team`, `developer`. Settings paths are prefixed with `/$storeId/settings`. New group: `settingsNavGroups: [{ key: 'integrations', labelKey: '…', position: 700 }]`, then `settingsNav: [{ key: 'erp', label: 'ERP', path: '/erp', group: 'integrations', subject: 'Spree::Store', action: 'update' }]` (`comingSoon: true` shows a disabled "Soon" entry).

## Routes (custom pages)

```tsx
routes: [
  { key: 'reports', path: '/reports', component: ReportsPage, subject: 'Spree::Order' },
  { key: 'report', path: '/reports/$reportId', component: ReportPage },
]

function ReportPage({ params, storeId, searchParams }: { params: Record<string, string>; storeId: string; searchParams: Record<string, unknown> }) {
  return <ResourceLayout header={<PageHeader title="Report" />} main={<ReportBody id={params.reportId} />} />
}
```

- Registry routes are matched at navigation time by a catch-all (`/_authenticated/$storeId/$`), inherit the auth guard + chrome, and can be registered late. `subject` renders a 403 page on direct navigation — pair it with the same `subject` on the nav entry.
- They're not in the typed route tree, so links need casts: `<Link to={'/$storeId/reports/$reportId' as string} params={{ storeId, reportId } as never}>`.
- Any compiled **file route** at the same URL silently wins. File routes (typed, code-split, `validateSearch`) are the packaged-plugin mechanism — see `spree-dashboard-plugins`.
- Keep page state in the URL (filters, sort, page, open sheet `?edit=prod_…`), not React state.

## Slots — widgets inside built-in pages

```tsx
defineDashboardPlugin({
  slots: { 'product.form_sidebar': [{ id: 'acme-brand-card', component: BrandCard as never, position: 50 }] },
})
// or fully typed:
registerSlot<{ product: Product }>('product.form_sidebar', { id: 'acme-brand-card', component: ({ product }) => <BrandCard product={product} /> })
```

- The component receives only the slot's context (`{ product }`, `{ order }`, `{ resource }`, …). Ambient `permissions/store/user` are **not** injected yet — call `usePermissions()`, `useStore()`, `useAuth()`. The entry `if` sees only the slot context.
- `as never` is expected with the facade (slot map is type-erased); use `registerSlot<Ctx>` for type safety. `removeSlot(name, id)` / `updateSlot(name, id, patch)` alter any entry, including another plugin's.
- Main slots: `page.actions`, `page.actions_dropdown`, `page.tabs`, `product|category|collection|order|customer.form_sidebar`, `store.form_main`, `company.form_main|form_sidebar`, `seller.form_main|form_sidebar`, and per-type editor slots (`payment_method.form.<type>`, `promotion.rule_form.<type>`, …). Full catalog with contexts: [references/slots.md](references/slots.md).

## Tables

```tsx
import { tables } from '@spree/dashboard'

tables.products.addColumn({ key: 'brand', label: 'Brand', default: true, render: (p) => p.brand?.name ?? '—' })
tables.products.updateColumn('price', { label: 'Retail price' })
tables.products.removeColumn('tags')
tables.orders.addColumn({ key: 'channel_id', label: 'Channel', displayable: false, filterable: true, filterType: 'enum',
  filterOptions: [{ value: 'ch_web', label: 'Web' }] })            // filter-only entry
```

- `ColumnDef`: `key`, `label`, `render`, `className`, `default` (visible by default), `sortable`, `filterable`, `filterType` (`string` default | `boolean` | `number` | `currency` | `date` | `enum` + `filterOptions` | `resource` + `filterResource { queryKey, search, hydrate, getOptionLabel }` | `tags` + `taggableType`), `ransackAttribute`, `displayable`, `expand`, `quickFilter`.
- Sorting/filtering run server-side through Ransack — the attribute must be in the model's `whitelisted_ransackable_attributes`, or the request fails.
- Mutations against a table not registered yet (built-ins register when their page first loads) are queued and replayed — safe even for optional features. Built-in table keys include `products`, `orders`, `customers`, `promotions`, `collections`, `stock-levels`, `gift-cards`, `store-credits`, `sellers`, `companies`, `returns`, `price-lists`, …
- Own list pages: `defineTable<T>('brands', { columns, searchParam, defaultSort, emptyMessage })` + `<ResourceTable tableKey queryKey queryFn searchParams />` (pagination, filter panel, column picker, URL round-trip). `bulkActions` / `rowActions` / `reorder` are props on your own `<ResourceTable>` — you cannot inject them into built-in tables.

## Form fields and custom-field widgets

- **Custom field definitions** (no code) already render in the Custom Fields card and save with the form. Swap one definition's widget: `customFieldComponents: { 'specs.color': ColorInput }` (props: `id`, `ariaLabel`, `value`, `onChange`, `definition`).
- **Real column** on a built-in form: `formFields: { product: [{ name: 'lead_time_days', from: (p) => p?.lead_time_days ?? null }] }` + a slot widget binding the input with `useHostForm()` (`form.register(...)` or `<Controller control={form.control}>`). It hydrates, arms Save, ships in the page's PATCH, and shows server 422s inline. Host forms: `product`, `category`, `collection`, `store`. Never render a nested `<form>`; on order/customer pages use `useOptionalHostForm()` and save yourself.

Worked code for both paths, plus page actions, a sidebar widget and a custom list page: [references/recipes.md](references/recipes.md).

## Permissions — UI gating is not authorization

```tsx
import { Can, usePermissions } from '@spree/dashboard'

const { permissions, permissionKeys, rules, isLoading, refresh } = usePermissions()
permissions.can('update', 'Spree::Order')            // class-level, mirrors server abilities
permissions.isConditional('update', 'Spree::Order')  // true → record-level rules apply; expect a possible 403
permissionKeys.includes('write_orders')              // flat catalog keys the role holds on this store

<Can I="destroy" a="Spree::Product" fallback={null}><DeleteButton /></Can>
```

- `subject` (+ `action`) on nav entries, settings entries and routes; `if` on nav entries (`{ permissions, store, user }`); gate slot widgets inside the component.
- Hiding a button is UX. The Admin API enforces per-controller `read_*`/`write_*` permissions on every request — your custom endpoints must too (see `spree-auth-permissions`).
- For a new resource, register a catalog scope on the backend so roles can be granted it and `permissions.can('read', 'MyApp::Report')` resolves:
  ```ruby
  # server/config/initializers/spree.rb
  Spree.permissions.register_scope(:reports, group: :analytics, resources: -> { [MyApp::Report] })
  ```
  Abilities and `permission_keys` ship with `GET /api/v3/admin/me`; permissions reload on store switch.

## Talking to the backend

```ts
// src/hooks/use-brands.ts
import { adminClient, useResourceKey, useResourceMutation } from '@spree/dashboard'
import type { PaginatedResponse } from '@spree/admin-sdk'
import { useQuery } from '@tanstack/react-query'

export function useBrands(params?: Record<string, unknown>) {
  return useQuery({
    queryKey: useResourceKey('brands', params),   // → ['brands', storeId, params]
    queryFn: () => adminClient.request<PaginatedResponse<Brand>>('GET', '/brands', { params }),
  })
}

export function useUpdateBrand(id: string) {
  return useResourceMutation({
    mutationFn: (body: Partial<Brand>) => adminClient.request<Brand>('PATCH', `/brands/${id}`, { body }),
    invalidate: [['brands'], ['brands', id]],      // store id injected for you
    successMessage: 'Saved',
  })
}
```

- `adminClient` is the configured `@spree/admin-sdk` singleton: typed resources (`adminClient.products.list/get/update…`) and `request<T>(method, path, { params, body })` with paths relative to `/api/v3/admin`. Never create a second client or use raw `fetch`.
- Every query key must be store-scoped: `useResourceKey` in hooks, `useResourceKeyBuilder()` when ids arrive later, `withStoreScope(key, storeId)` outside React. A bare `['brands']` serves one store's rows to another after a store switch.
- Errors are `SpreeError` (`status`, `code`, `details`). `useResourceMutation` toasts non-422 failures and stays silent on 422 so the form can show them: `catch (e) { if (!mapSpreeErrorsToForm(e, form.setError)) throw e }` (`:base` → `errors.root`). On pages without a form (a header action, a dialog-less button), pass `showValidationErrors: true` — otherwise a server refusal (422 with the reason) shows the merchant nothing.
- Filtering, sorting or aggregating across resources belongs in a backend endpoint, not N client requests.
- IDs are prefixed strings (`prod_…`, `or_…`, `cust_…`) everywhere — never parse or strip them.

## End to end: a new product attribute (form + column + filter + sort)

Prefer a custom field definition unless you need Ransack filter/sort or DB guarantees. For a real column:

```ruby
# 1. server/db/migrate/…_add_lead_time_days_to_spree_products.rb
class AddLeadTimeDaysToSpreeProducts < ActiveRecord::Migration[8.1]
  def change
    add_column :spree_products, :lead_time_days, :integer
    add_index :spree_products, :lead_time_days
  end
end

# 2. server/config/initializers/spree.rb — writable, filterable/sortable
Spree::Product.additional_permitted_attributes += [:lead_time_days]   # += (never << — it's frozen; never = — drops other extensions')
Spree::Product.whitelisted_ransackable_attributes |= %w[lead_time_days]
Spree.api.admin_product_serializer = 'MyApp::AdminProductSerializer'

# 3. server/app/serializers/my_app/admin_product_serializer.rb — readable
module MyApp
  class AdminProductSerializer < Spree::Api::V3::Admin::ProductSerializer
    typelize lead_time_days: [:number, nullable: true]
    attributes :lead_time_days
  end
end

# + a model validation — the dashboard renders its 422 message inline
```

```tsx
// 4. apps/dashboard/src/plugins.ts
defineDashboardPlugin({
  formFields: { product: [{ name: 'lead_time_days', from: (p) => p?.lead_time_days ?? null }] },
  slots: { 'product.form_sidebar': [{ id: 'lead-time', component: LeadTimeCard as never, position: 60 }] },
  tables: { products: { add: [{
    key: 'lead_time_days', label: i18n.t('admin.fields.product.lead_time_days.label'),
    sortable: true, filterable: true, filterType: 'number', default: true,
    render: (p) => (p.lead_time_days != null ? `${p.lead_time_days} d` : '—'),
  }] } },
})
```

`LeadTimeCard` uses `useHostForm<{ lead_time_days: number | null }>()` and `form.register('lead_time_days', { setValueAs: (v) => (v === '' || v == null ? null : Number(v)) })`. The form `name`, serializer attribute and permitted attribute must be the same string. Verify the backend first: `spree api patch products/prod_… --data '{"lead_time_days":14}'` and `spree api get "products?q[lead_time_days_gt]=7&sort=-lead_time_days"`. Custom Admin controllers use `resource_permitted_attributes` instead (see `spree-resource`, `spree-decorators`).

## Theming

Everything is CSS custom properties. Override below the import in `src/styles.css`, and set **both** `:root` and `.dark` (the theme provider only toggles the `.dark` class):

```css
@import "@spree/dashboard/styles.css";

:root { --primary: oklch(0.55 0.22 264); --radius: 0.25rem; }
.dark { --primary: oklch(0.72 0.19 264); }

@theme inline { --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif; --text-base: 0.9375rem; }
```

Tokens: `--background/--foreground`, `--card*`, `--popover*`, `--muted*`, `--primary*` (aliases `--foreground` by default), `--secondary*`, `--accent*` (+ `-hover`, `-strong`), `--link`, `--ring`, `--destructive*`, `--status-{green,amber,red,blue}-{bg,border,fg}`, `--border*`, `--input`, `--radius`, `--sidebar*`, `--chart-1..5`. In your pages use Tailwind utilities (`bg-card text-muted-foreground`) rather than raw `var(--…)`, and `className="link"` for prose links. The seller panel (`@spree/seller-dashboard/styles.css`) uses the same tokens.

## Translations

i18next, single `translation` namespace, every key under `admin.`. Register with `i18n.addResourceBundle(locale, 'translation', { admin: { … } }, true, true)` at the top of `plugins.ts` (or `defineDashboardPlugin({ locales: { en, de } })`), use `useTranslation()` in components and `labelKey` in registries. Field keys: `admin.fields.<resource>.<attribute>.label|placeholder`, falling back to `admin.fields.<attribute>.*`. Built-in locales: en, de, es, fr, pl, ar, zh-CN. A gem that registers a promotion rule/action, calculator, price rule, collection rule, order routing rule, delivery method rule, commission rule, seller requirement, integration or permission should ship `admin.types.<family>.<code>.{name,description}` — otherwise the API's label (resolved in the store's locale, not the admin's) is shown. Server 422 messages are displayed verbatim — localize them with Rails i18n.

## Testing

`cd apps/dashboard && pnpm test` (Vitest, Node env, `src/**/*.test.ts`) and `pnpm test:e2e` (Playwright against `spree dev` + the dev server; `E2E_BASE_URL` to target a deployment).

- Unit-test the logic between UI and API — query keys, payload mappers, permission predicates, filter → Ransack mapping. Don't render components to assert markup; don't test one-line `adminClient.request` wrappers.
  ```ts
  import { withStoreScope } from '@spree/dashboard'
  import { QueryClient } from '@tanstack/react-query'
  it('invalidates only the current store', () => {
    const qc = new QueryClient()
    qc.setQueryData(withStoreScope(['brands'], 'store_a'), [])
    qc.setQueryData(withStoreScope(['brands'], 'store_b'), [])
    qc.invalidateQueries({ queryKey: withStoreScope(['brands'], 'store_a') })
    expect(qc.getQueryCache().getAll().filter((q) => q.state.isInvalidated)).toHaveLength(1)
  })
  ```
- E2E: drive and assert on the UI (click the sidebar link rather than `goto('/brands')` — real paths are `/:storeId/…`), suffix record names with `Date.now()` (specs share a DB; the config runs one worker).
- Checks before pushing: `pnpm typecheck && pnpm lint && pnpm test && pnpm build`.

## Deployment (pointer — see `spree-deployment`)

- **Single node (default):** the `spree_dashboard` gem serves a built dashboard at `/dashboard` from `Spree::Dashboard.dist_path` / `SPREE_DASHBOARD_DIST_PATH` (seller panel at `/sellers`). The official image ships the stock build; bake **your** customized build with `spree build --production [--tag …]` (or `docker build . -f server/Dockerfile`) — it detects `apps/dashboard/` and builds with `VITE_BASE_PATH=/dashboard/` and a relative API URL.
- **Static host / CDN:** `VITE_SPREE_API_URL=https://api.example.com pnpm build`, deploy `dist/` with a `/* → /index.html` rewrite, HTTPS on both sides (refresh cookie is `SameSite=None; Secure`), and add the origin under **Settings → Developer → Allowed Origins**. One build per environment.
- `VITE_*` values are compiled into the bundle — never put secrets there.

## Coming from `spree_admin` (Spree 5.x)

| `spree_admin` | Dashboard |
|---|---|
| `Spree.admin.navigation.sidebar.add/remove/update` | `nav.add/remove/update`, `nav.addChild`; `settingsNav` for settings |
| `spree:admin:scaffold` + ERB CRUD views | `defineTable` + `<ResourceTable>` page + `routes` entry (API from `spree:api_resource`) |
| `Spree.admin.tables.<t>.add/remove/update` | `tables.<t>.addColumn/removeColumn/updateColumn` |
| `Spree.admin.partials.<point> << 'partial'` | `slots: { '<slot>': [...] }` |
| Adding a field to `_form.html.erb` / `product_form` partial | `formFields` + slot widget with `useHostForm()`, or a custom field definition |
| Admin controller decorators / `permitted_attributes` | Admin API: `Model.additional_permitted_attributes +=`, serializer via `Spree.api.admin_*_serializer` |
| CanCanCan `can?` in views | `usePermissions()` / `<Can>` / `subject` (UX only) + backend permission keys |
| Stimulus controllers, importmap | React components + TanStack Query hooks |
| Overriding admin Tailwind/CSS | CSS token overrides in `src/styles.css` |
| `Spree.t` admin strings | i18next `admin.*` bundles |

For the full 5.x → 6 migration, see `spree-upgrade-5-to-6`.

## Gotchas

- **Duplicate key/id throws at boot** — namespace keys (`acme-reports`), and remember built-in keys (`orders`, `products`, …).
- **Unscoped query keys leak data across stores.** Always `useResourceKey`.
- **Slot widgets must gate themselves** — `page.actions` renders on every page; permissions aren't passed as props.
- **`nav.update(parent, { children })` drops built-in children** — use `addChild`.
- **Sortable/filterable column without a Ransack allowlist entry** fails at request time, not at build time.
- **Registry route shadowed by a file route** at the same URL never renders — no error.
- **Frozen labels:** `label: i18n.t(...)` doesn't follow language switches; use `labelKey`.
- **Nested `<form>` inside a host-form slot** breaks the page's Save. Use `useHostForm()`.
- **Never embed an SDK entity type in form-values types** — RHF walks nested keys and the TS compiler blows up; map to a flat values type.
- **Don't loosen the dashboard's dependency pins.** `@spree/dashboard-ui` compiles into your app, so its dependencies are pinned exactly (`@base-ui/react` 1.8.0, `recharts` 3.10.1, …) to what Spree tested. A newer Base UI floating in (via an override, a caret range, or dashboard packages older than 1.0.0-beta.7) fails before the first render with a `SyntaxError` about `useSyncExternalStore`. Upgrade the `@spree/dashboard*` packages together rather than bumping Base UI yourself.
- **Don't reach into Rails.** A missing endpoint is added to the Admin API first (`spree-resource`, `spree-api-v3`).

## Where to read further

- Docs (installed): `node_modules/@spree/docs/dist/developer/dashboard/` — `overview.md`, `concepts.md`, `customization/{quickstart,navigation,routes,slots,tables,permissions,backend,theming,translations}.md`, `recipes/*.md`, `slots-catalog.md`, `public-api.md`, `deployment.md`; tutorial `developer/tutorial/dashboard.md` and `developer/tutorial/testing.md`. Online: https://spreecommerce.org/docs/developer/dashboard/overview
- Your app's `apps/dashboard/AGENTS.md` (conventions) and `README.md`.
- Source: `packages/dashboard-core/src/{plugin.ts,lib/*-registry.ts}`, `packages/dashboard/src/nav/default.ts` (built-in nav), `packages/dashboard-plugin-example` (complete Brands example) in https://github.com/spree/spree
- Related skills: `spree-dashboard-plugins`, `spree-auth-permissions`, `spree-api-v3`, `spree-typescript-sdk`, `spree-resource`, `spree-catalog` (custom fields), `spree-deployment`.
