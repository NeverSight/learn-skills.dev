---
name: using-backstage-frontend-system
description: Use when defining or authoring extensions for a Backstage frontend plugin in the new frontend system. Covers createFrontendPlugin, route refs from @backstage/frontend-plugin-api, ApiBlueprint, PageBlueprint, SubPageBlueprint, and hook usage. Triggers on imports from @backstage/frontend-plugin-api or when writing src/plugin.tsx, src/routes.ts, src/apis.ts, src/extensions.tsx.
---

# Backstage New Frontend System (NFS) Patterns

## When to use this skill

- Defining a new frontend plugin (`src/plugin.tsx`)
- Declaring route refs (`src/routes.ts`)
- Exposing APIs from a plugin (`src/apis.ts`)
- Adding pages, sub-pages, or other extensions (`src/extensions.tsx`)
- Using NFS hooks (`useApi`, `useRouteRef`)

## Choose the right pattern

| Building...                                         | Pattern                                                                                                | Reference                       |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------- |
| The plugin itself                                   | `createFrontendPlugin({ pluginId, ..., extensions })`                                                  | references/plugin-definition.md |
| Route refs                                          | `createRouteRef`, `createSubRouteRef`, `createExternalRouteRef` from `@backstage/frontend-plugin-api`  | references/route-refs.md        |
| Calling a backend endpoint (default)                | A data hook wrapping `useAsync` / `useAsyncFn` around `fetchApi.fetch` — no client class, no extension | references/api-extensions.md    |
| Exposing an extensible API on an open-source plugin | `ApiBlueprint.make({ params })`                                                                        | references/api-extensions.md    |
| A page (single route)                               | `PageBlueprint.make({ params: { path, routeRef, loader } })`                                           | references/page-extensions.md   |
| A page with tabs                                    | `PageBlueprint` (no loader) + `SubPageBlueprint`s                                                      | references/sub-pages.md         |
| Reading APIs in components                          | `useApi(apiRef)`, `useRouteRef(routeRef)` from `@backstage/frontend-plugin-api`                        | references/hooks.md             |

## Two invocation modes

- **Standalone**: user is editing an existing NFS plugin. Pick a reference and apply.
- **Post-scaffold** (called by `creating-backstage-plugin` for `frontend-plugin` / `frontend-plugin-module` templates): wire up the canonical NFS structure in the freshly scaffolded plugin — `src/routes.ts`, `src/plugin.tsx` using `createFrontendPlugin`, and an example `PageBlueprint` extension.

## Common gotchas

- In NFS, plugin-system imports come from `@backstage/frontend-plugin-api`, not `@backstage/core-plugin-api`. Hooks (`useApi`, `useRouteRef`), refs (`identityApiRef`, `configApiRef`, `discoveryApiRef`, `fetchApiRef`, `storageApiRef`, `analyticsApiRef`), and primitives (`createApiRef`) all live in the new package.
- `createRouteRef()` takes no `id` argument — the id is derived from the extension that owns the route.
- `createExternalRouteRef({ defaultTarget: '<pluginId>.<routeName>' })` — set `defaultTarget` to the most common binding so apps don't need explicit `bindRoutes` calls.
- `useRouteRef(externalRef)` may return `undefined` if the external route isn't bound — always handle the undefined case.
- Page components inside a `PageBlueprint` loader should NOT include `Page`, `Header`, or `PageWithHeader` from `@backstage/core-components`. The framework's `PageLayout` renders `PluginHeader` automatically. Use `Container` from `@backstage/ui` as the outermost wrapper for page content. Use `Header` from `@backstage/ui` only when you need a subtitle or custom actions.
- `SubPageBlueprint` paths are relative (no leading `/`). Sub-page components render content only — no `Page`, no `Header`, no `HeaderTabs`. Wrap sub-page content in `Container` from `@backstage/ui` if padding is needed.
- `createApiRef<T>().with({ id, pluginId })` — the builder form is preferred so ownership is explicit. The `id` must still be globally unique. Only the owning plugin (or a module targeting it) can override the API.
- For any `fetchApi.fetch` call, handle non-OK responses with `throw await ResponseError.fromResponse(response)` from `@backstage/errors` — it parses the response body for structured error info and produces a typed error other Backstage UI surfaces (e.g. `<ResponseErrorPanel>`) understand. Never just `throw new Error(\`Failed: ${response.status}\`)`.
