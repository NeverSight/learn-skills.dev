---
name: spree-dashboard-plugins
description: Use when packaging Spree 6 React dashboard customizations as a redistributable npm plugin (optionally paired with a Rails extension gem) that other Spree stores install — scaffolding with `npx @spree/cli plugin new`, file routes and route collisions, peerDependencies against `@spree/dashboard-core`/`-ui`, prebuilt vs source publishing, `sideEffects`, the `spree.dashboard.plugin` package.json marker, auto-discovery via `virtual:spree-dashboard-plugins` vs an explicit whitelist, Tailwind class scanning, `definePlugin(config)` factories, Changesets, and the backend gem half. Common phrasings include "publish a dashboard plugin", "npm package for the Spree admin", "spree plugin new", "share admin screens across stores", "plugin not showing up", "Dashboard route collision", "plugin styles missing", "marketplace extension with admin UI".
---

# Spree Dashboard Plugins — packaging & distribution

A dashboard plugin is an npm package whose entry module calls `defineDashboardPlugin({...})` at import time. It uses **exactly the same registries** as in-app customization (nav, settingsNav, routes, slots, tables, formFields, customFieldComponents — see `spree-dashboard`). What changes is packaging: peer deps, discovery, file routes, publishing.

**Don't reach for a plugin by default.** For your own store, put the code in `apps/dashboard/src/plugins.ts`. Package it only when several stores/projects will install it (open-source integration, agency rollout, commercial add-on). Promoting in-app code to a plugin later is mostly a copy.

The dashboard is a Developer Preview (`@spree/dashboard-*` at `1.0.0-beta.x`) — expect to track releases closely.

## Scaffold

```bash
npx @spree/cli plugin new reviews \
  --npm-scope @acme --ruby-name spree_reviews --module-name Reviews \
  --author "Ada Lovelace" --author-email ada@example.com --license MIT
# -y / --yes     accept defaults for anything not passed (author/email from git config)
# --no-install   skip pnpm install        --force   overwrite a non-empty directory
# --no-dashboard / --no-engine  reserved for when engine scaffolding lands (--no-dashboard leaves nothing to scaffold today)
```

Licenses: MIT (default), Apache-2.0, BSD-3-Clause. Generated layout:

```
reviews/
├── package.json            # workspace root (pnpm -r build/lint/typecheck/test), private
├── pnpm-workspace.yaml
├── LICENSE, README.md, .gitignore
└── packages/dashboard/
    ├── package.json        # @acme/reviews-dashboard — marker + peerDependencies
    ├── tsconfig.json       # excludes src/routes (see File routes)
    ├── biome.json
    └── src/
        ├── index.tsx       # i18n bundle + defineTable + defineDashboardPlugin (nav + product slot)
        ├── client.ts       # adminClient.request wrappers for /reviews
        ├── types.ts
        ├── pages/reviews-list.tsx
        ├── routes/reviews.index.tsx   # TanStack file route → /$storeId/reviews
        ├── slots/product-reviews-card.tsx
        └── locales/en.json
```

The dashboard package is named `<scope>/<name>-dashboard`. **The CLI scaffolds only the dashboard half** — the generated README says so and points at the extension guide. The example pages call `/api/v3/admin/<name>` endpoints that don't exist until you build the backend half as a separate extension gem (see below). The scaffolded package's `build` script is `tsc --noEmit`: it type-checks the TypeScript source it ships, it doesn't emit JS (see Prebuilt vs source below).

## Entry module

```tsx
// packages/dashboard/src/index.tsx — imports from -core/-ui, NEVER from @spree/dashboard
import { defineDashboardPlugin, defineTable, i18n } from '@spree/dashboard-core'
import { MessageSquareIcon } from 'lucide-react'
import en from './locales/en.json'
import { ProductReviewsCard } from './slots/product-reviews-card'

i18n.addResourceBundle('en', 'translation', en, true, true)   // before anything calls i18n.t

defineTable('acme-reviews', { title: i18n.t('admin.acme_reviews.title'), columns: [/* … */] })

defineDashboardPlugin({
  nav: [{ key: 'acme-reviews', labelKey: 'admin.acme_reviews.nav', path: '/reviews', icon: MessageSquareIcon, position: 650, subject: 'Spree::Review' }],
  slots: { 'product.form_sidebar': [{ id: 'acme-reviews-card', component: ProductReviewsCard as never, position: 250 }] },
  // pages ship as file routes, not `routes:` entries
})
```

Why `-core`/`-ui` and not `@spree/dashboard`: the plugin plugs into the host's shell; importing the shell package would pull the whole app into your package and pin it to one dashboard version.

**Namespace everything** — registry keys, slot ids, table keys (`acme-reviews`), locale keys (`admin.acme_reviews.*`), and backend API paths. Duplicate keys throw at boot in the consumer's app, naming the conflict.

## File routes

Packaged plugins ship pages as TanStack file routes compiled into the host's typed route tree (typed `<Link>`s, code splitting, `validateSearch`, loaders). Declare the directory in the marker:

```jsonc
// packages/dashboard/package.json
"spree": { "dashboard": { "plugin": true, "routes": "./src/routes" } }
```

```tsx
// src/routes/reviews.$reviewId.tsx
import { createFileRoute } from '@tanstack/react-router'
import { ReviewPage } from '../pages/review'

export const Route = createFileRoute('/_authenticated/$storeId/reviews/$reviewId')({
  component: () => <ReviewPage id={Route.useParams().reviewId} />,
})
```

- Commit the **final composed path literal** (`/_authenticated/$storeId/…`); the generator verifies it.
- The host regenerates `src/routeTree.gen.ts` on every dev start and build from installed versions — upgrading your plugin adds its routes after a dev-server restart.
- Exclude `src/routes` from the package's standalone `tsc` (the scaffold does) — route files only type-check inside a host program. Develop against a host (a `create-spree-app` project or a `dashboard-starter` checkout) with your package linked (`pnpm add ../reviews/packages/dashboard` or a workspace).
- File routes skip the registry dispatcher, so `subject` gating doesn't apply — gate inside the component with `<Can>` / `usePermissions()` (UX only; the API authorizes).
- **Collisions fail the build:** two packages (or a plugin and a built-in page) declaring the same path produce `Dashboard route collision. Route "/_authenticated/$storeId/brands/" is declared by more than one package: …` listing both packages and files. Rename one. A runtime `routes:` entry at the same URL as a file route is *not* detected — the file route silently wins.
- Keep `routes:` registry entries for pages that must be registered conditionally at runtime.

## package.json essentials

```json
{
  "name": "@acme/reviews-dashboard",
  "version": "0.1.0",
  "type": "module",
  "sideEffects": ["./src/index.tsx", "./dist/index.js", "./dist/index.cjs"],
  "spree": { "dashboard": { "plugin": true, "routes": "./src/routes" } },
  "peerDependencies": {
    "@spree/dashboard-core": ">=1.0.0-0 <2.0.0-0",
    "@spree/dashboard-ui": ">=1.0.0-0 <2.0.0-0",
    "@spree/admin-sdk": ">=1.0.0-0 <2.0.0-0",
    "@tanstack/react-query": "^5",
    "@tanstack/react-router": "^1",
    "i18next": "^26",
    "react-i18next": "^17",
    "lucide-react": "^1",
    "react": "^19",
    "react-dom": "^19"
  }
}
```

- **peerDependencies, not dependencies,** for React, the dashboard packages, TanStack, i18next, lucide. Registries are module singletons: a second copy of `@spree/dashboard-core` means your registrations land in a registry the host never reads (plugin "does nothing"). `dependencies` is only for small utilities the host doesn't have. Never add `@base-ui/react` (or another `@spree/dashboard-ui` dependency) at your own version. The host pins them exactly, and a second Base UI can break the build. Import from the dashboard packages' entry points only: a deep file import makes Vite skip converting a CommonJS dependency in installed apps, and the dashboard dies before rendering.
- Use ranges. `spree plugin new` scaffolds caret ranges on the `@spree/admin-sdk` / `@spree/dashboard-core` / `@spree/dashboard-ui` versions released alongside your `@spree/cli` (e.g. `^1.0.0-beta.3`). Caret ranges on prereleases are narrow — `^1.0.0-beta.3` accepts later `1.0.0` betas and stable `1.x`, but not betas of other versions — so keep the peers in step with the dashboard until 1.0 ships, or widen to `>=1.0.0-0 <2.0.0-0` as above.
- **`sideEffects`** must list the entry files — otherwise a bundler may tree-shake `import '@acme/reviews-dashboard'` away. The scaffold lists `./src/index.tsx`; add the `dist/` entries if you ship prebuilt JS.
- **The marker** `spree.dashboard.plugin: true` is what auto-discovery and Tailwind scanning look for. Without it hosts won't activate the plugin and its classes won't compile.
- Scaffold is `"private": true` — flip it (and drop any `publishConfig.access: restricted`) before publishing.

## Prebuilt vs source

| | Ship source (scaffold default) | Ship prebuilt JS |
|---|---|---|
| `package.json` | `"main"/"types": "./src/index.tsx"`, `"files": ["src"]` | `"main": "./dist/index.cjs"`, `"module": "./dist/index.js"`, `"types": "./dist/index.d.ts"`, `"files": ["dist", "src"]` |
| Build | `tsc --noEmit` (type-check only) — the host's Vite compiles TSX | `tsup src/index.tsx --format cjs,esm --dts --external react` + `"prepublishOnly": "pnpm build"` |
| When | Internal packages, Vite hosts (all Spree dashboards are Vite) | Public npm releases |

Either way keep `src/` in `files`: the Vite plugin resolves your package and scans its source for Tailwind classes, and file routes are compiled from `src/routes`. Use static class strings — Tailwind can't see `` `text-${tone}-500` ``.

## How hosts install it (document this in your README)

```bash
pnpm add @acme/reviews-dashboard     # in apps/dashboard, then restart the dev server
# backend half, in server/
bundle add spree_reviews && bin/rails g spree_reviews:install && bin/rails db:migrate
```

No host code edits. `spreeDashboardPlugin()` (from `@spree/dashboard/vite`) walks the host's `dependencies` + `devDependencies`, reads each manifest, and for every package with the marker:

1. **Activates it** — synthesizes `virtual:spree-dashboard-plugins` (one side-effect import per plugin), which the starter's `main.tsx` imports after the shell and before `./plugins`.
2. **Injects Tailwind `@source`** for the package.
3. **Composes its file routes** into `routeTree.gen.ts` (with the collision check).

Hosts that want control whitelist instead — this disables discovery:

```ts
// apps/dashboard/vite.config.ts
plugins: [spreeDashboardPlugin({ plugins: ['@acme/reviews-dashboard'] }), react()]
// plugins: [] → no third-party plugins at all
```

A whitelisted or discovered plugin that can't be resolved shows a Vite error overlay with the package name and a checklist. Installing a plugin runs its code in the admin — same trust model as adding a gem.

## Configurable plugins

- **Module-level `configure()`** — only for values read lazily (at render/fetch). ES imports are hoisted, so the plugin's top-level `defineDashboardPlugin` always runs before the host's `configure(...)` line.
- **`definePlugin(config)` factory** — when config shapes *what* is registered (which nav entries/routes). Don't call `defineDashboardPlugin` at import time; export a factory, drop the `spree.dashboard.plugin` auto-activating entry (or keep the marker only for Tailwind/routes and make the entry side-effect free), and document that hosts call it in `main.tsx`/`plugins.ts`:
  ```ts
  export function definePlugin(config: { showRatingsColumn?: boolean }) {
    defineDashboardPlugin({ nav: [/* … */], tables: config.showRatingsColumn ? { products: { add: [/* … */] } } : undefined })
  }
  ```

## The Rails gem half

Most plugins need endpoints. Build a normal Spree extension gem (see `spree-extensions`; `gem install spree_extension -v '>= 2.0' && spree-extension create reviews` — 1.x generates a Spree 5 scaffold). Register its scope, hooks and subscribers in the gem's `config/initializers/spree.rb`:

- Model + migration (`Spree.base_class`, `has_prefix_id`, no FKs), Admin API controller under `Spree::Api::V3::Admin` with `scoped_resource :reviews`, serializer, routes via `Spree::Core::Engine.add_routes { namespace :api … namespace :v3 … namespace :admin { resources :reviews } }` — consider an extension namespace (`/api/v3/admin/acme/…`) so a future core resource can't collide.
- Permissions so roles can be granted it and `permissions.can('read', 'Spree::Review')` resolves in the dashboard: `Spree.permissions.register_scope(:reviews, group: :catalog, resources: -> { [Spree::Review] })`, plus `spree.permissions_catalog.resources.reviews.label` in the gem's locale.
- New columns on core models: `Spree::Product.additional_permitted_attributes += [:reviews_enabled]` + a serializer swap.
- Type names: if the gem registers a promotion rule/action, calculator, price rule, delivery method rule, commission rule, seller requirement, integration or permission, ship `admin.types.<family>.<code>.{name,description}` in the npm package's locales.
- Version the gem and the npm package together; the README's compatibility table should state both (`@spree/dashboard-core`, `spree` gem).

## Publishing & versioning

```bash
pnpm build && pnpm publish --access public        # or --tag next for pre-1.0 lines
```

- Channels: public npm, private npm, GitHub Packages (`@acme:registry=https://npm.pkg.github.com` in `.npmrc`), or `pnpm add github:acme/reviews#main` while iterating.
- Changesets (optional; the scaffold doesn't configure it): `pnpm changeset` → `pnpm changeset version` → `pnpm install` → `pnpm publish -r`.
- CI: build/typecheck against the lowest supported dashboard version and the next minor to catch APIs you depend on that don't exist everywhere.
- Treat as public API (breaking changes need a major + changelog entry): nav/route keys and paths, slot ids you expose, locale keys, table keys, `configure`/`definePlugin` signatures, peer ranges.

## Common mistakes

- Importing from `@spree/dashboard` in a plugin → duplicated shell, version pinning.
- Dashboard packages in `dependencies` → duplicate registries; plugin silently does nothing.
- Missing marker or no `src/` in the tarball → plugin not activated / unstyled.
- Missing `sideEffects` → entry tree-shaken in production builds only.
- Registering pages with `routes:` in a packaged plugin → untyped links, and any file route at the same URL shadows it.
- Unnamespaced keys → boot-time duplicate-key errors on stores running another plugin.
- Expecting `spree plugin new` to generate the Rails engine — it scaffolds only the dashboard half; the example pages 404 until your gem ships the endpoints.
- Forgetting the dev-server restart after installing/upgrading (discovery and route composition run at startup).

## Where to read further

- Docs (installed): `node_modules/@spree/docs/dist/developer/dashboard/plugins/{overview,scaffolding,publishing,distributing}.md`, `dashboard/customization/routes.md`, `developer/contributing/creating-an-extension.md`. Online: https://spreecommerce.org/docs/developer/dashboard/plugins/overview
- Reference implementation: `packages/dashboard-plugin-example` (Brands) and the CLI templates `packages/cli/templates/plugin/` in https://github.com/spree/spree
- Discovery / Vite plugin source: `packages/dashboard-core/src/vite/{index,discover}.ts`, `packages/dashboard/src/vite/route-collisions.ts`
- Related skills: `spree-dashboard` (all registry APIs), `spree-extensions` (the gem half), `spree-auth-permissions`, `spree-api-v3`.
