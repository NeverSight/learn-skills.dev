---
name: basmilius
description: >-
  Use when a project depends on a package in the `@basmilius` npm scope (by Bas
  Milius): `@basmilius/utils` (standalone Luxon-based date, number, color,
  download, DOM, timing, geo and PRNG helpers), `@basmilius/http-client` (the
  typed DTO data layer) and `@basmilius/common` (Vue 3 app primitives on Pinia
  and Vue Router). Trigger on any `@basmilius/*` import; on formatDate /
  formatNumber, hexToRGB / hslToRGB, debounce / waitFor, downloadBlob,
  mulberry32, getSeason / getMoonPhase; on `@dto` / `@adapter`, `HttpClient`,
  `RequestBuilder`, `BaseService`, `BaseResponse`, `Paginated`, `.runAdapter`,
  `RequestError` / `ValidationError`, `serialize` / `deserialize`, the
  `dtoNames` Vite plugin; on the ref-returning `defineStore`, `useService` /
  `guarded`, `useDataTable` / `useDataReport`, `useDtoForm`, `useUrlState`,
  `persistentRef`, its composables (useClickOutside, useHotKey, ...), router
  helpers (useRouteParam, useNavigate, ...) and exceptions
  (ForbiddenException, HandledException, ...). NOT for `@flux-ui/*` (see
  `flux-ui`); `@basmilius/vite-preset` is intentionally out of scope.
license: MIT (skill content); @basmilius/utils, @basmilius/http-client and @basmilius/common are MIT, by Bas Milius
---

# Bas Milius packages

The `@basmilius` npm scope is one stack in three layers, each covered by a
guide in `references/`:

1. **`@basmilius/utils`** - ~45 framework-agnostic helpers (dates via Luxon,
   colors, numbers, downloads, DOM, timing, geo/astro, seeded PRNG). Usable in
   any TypeScript project.
2. **`@basmilius/http-client`** - the typed data layer: every body a `@dto`
   class, every endpoint group a `BaseService`, raw snake_case JSON mapped by a
   static `@adapter`. Builds on `utils`.
3. **`@basmilius/common`** - Vue 3 app primitives: a ref-returning
   `defineStore`, `useService` + `guarded`, `useDataTable` / `useDataReport`,
   `useDtoForm`, a large composable catalog and thin `vue-router` wrappers.
   Assumes Pinia and Vue Router, builds on both packages above.

Shared assumptions: a Vue 3.6 pre-release where Vue is involved (exact range per
the package's `peerDependencies`), `luxon` as a peer for dates. `@flux-ui/*` is a
separate library with its own skill (`flux-ui`); `@basmilius/vite-preset` is
deliberately not covered.

## Routing: read the package guide before writing code

The per-package traps and judgment live in the guides, not here. **Read the
matching guide first**, then dip into the signature/pattern files as needed:

| Working on | Read first | Then as needed |
| --- | --- | --- |
| A date/number/color/download/DOM helper, or anything imported from `@basmilius/utils` | `references/utils.md` | `references/utils-function-index.md` (every function with exact signatures and the browser-vs-pure split) |
| DTOs, adapters, services, requests, (de)serialization, the Vite plugin, tsconfig decorator flags | `references/http-client.md` | `references/http-client-reference.md` (full export surface), `references/http-client-patterns.md` (worked DTO -> adapter -> service recipes, error handling, dirty-save) |
| Stores, data tables/reports, forms, URL state, composables, router helpers, exceptions | `references/common.md` | `references/common-reference.md` (composable catalog with signatures), `references/common-patterns.md` (worked stores, `useService`, `useDataTable` view, `useDtoForm`, `useUrlState`) |

Tasks often span layers: a data table view touches `common` (`useDataTable`),
`http-client` (the service and DTOs) and sometimes `utils` (formatting). Read
each involved guide; they are short and cross-link where the layers meet.

## Related skills

- **`vue-build-feature`** / **`vue-component-anatomy`** - the library-neutral
  Vue architecture and SFC patterns these packages slot into; `common` is the
  concrete data/state layer `vue-build-feature` defers to.
- **`flux-ui`** - the Flux UI component library (separate `@flux-ui` scope).
