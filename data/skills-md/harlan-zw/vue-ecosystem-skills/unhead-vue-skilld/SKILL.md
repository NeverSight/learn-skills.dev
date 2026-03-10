---
name: unhead-vue-skilld
description: "Full-stack head manager built for Vue. ALWAYS use when writing code importing \"@unhead/vue\". Consult for debugging, best practices, or modifying @unhead/vue, unhead/vue, unhead vue, unhead."
metadata:
  version: 2.1.12
  generated_at: 2026-03-10
  references_synced_at: 2026-03-10
---

# unjs/unhead `@unhead/vue`

> Full-stack <head> manager built for Vue.

**Version:** 2.1.12 (Mar 2026)
**Deps:** hookable@^6.0.1, unhead@2.1.12
**Tags:** next: 3.0.0-beta.9 (Feb 2026), beta: 3.0.0-beta.11 (Mar 2026), latest: 2.1.12 (Mar 2026)

**References:** [Docs](./references/docs/_INDEX.md) — API reference, guides
## API Changes

This section documents version-specific API changes — prioritize recent major/minor releases.

- BREAKING: `createHead()` and `createServerHead()` removed from `@unhead/vue` root in v2 — use subpath imports: `createHead()` from `@unhead/vue/client` (SPA) or `@unhead/vue/server` (SSR); `createServerHead()` no longer exists [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#client--server-subpath-exports)

- BREAKING: Implicit context removed in v2 — `setHeadInjectionHandler()` deleted; `useHead()` called after an `await` in lifecycle hooks (e.g. `onMounted`) throws because Vue context is lost; wrap async data fetching before calling `useHead()` [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#removed-implicit-context)

- BREAKING: `vmid` and `hid` tag properties removed in v2 — use `key` for deduplication: `script: [{ key: 'my-key' }]` [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#removed-vmid-hid-children-body)

- BREAKING: `children` tag property removed in v2 — use `innerHTML` instead [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#removed-vmid-hid-children-body)

- BREAKING: `body: true` tag property removed in v2 — use `tagPosition: 'bodyClose'` instead [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#removed-vmid-hid-children-body)

- BREAKING: `useScript()` no longer returns a Promise in v2 — `.then()` calls silently fail; use `.onLoaded(() => ...)` instead [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#updated-usescript)

- BREAKING: `useScript()` API no longer accessible directly on the instance in v2 — must use `.proxy` explicitly: `script.proxy.myFn()` not `script.myFn()`; code compiles but calls are lost at runtime [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#updated-usescript)

- BREAKING: `stub()` option and `script:instance-fn` hook removed from `useScript()` in v2 — replace with custom `use()` logic [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#updated-usescript)

- BREAKING: Promise inputs in `useHead()` no longer auto-resolved in v2 — await the promise before passing, or opt in to `PromisePlugin` from `@unhead/vue/plugins` [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#promise-input-support)

- BREAKING: `TemplateParamsPlugin` and `AliasSortingPlugin` no longer built-in in v2 — must opt in: `createHead({ plugins: [TemplateParamsPlugin, AliasSortingPlugin] })` imported from `@unhead/vue/plugins` [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#opt-in-template-params--tag-alias-sorting)

- BREAKING: Capo.js tag sorting is now the default in v2 — breaks snapshot tests; opt out with `createHead({ disableCapoSorting: true })` [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#tag-sorting-updated)

- DEPRECATED: `useServerHead()`, `useServerHeadSafe()`, `useServerSeoMeta()` — use `useHead()`, `useHeadSafe()`, `useSeoMeta()` with `import.meta.server` conditionals or `{ mode: 'server' }` option for tree-shaking

- NEW: `<Head>`, `<Title>`, `<Meta>`, `<Link>`, `<Script>` template components — import from `@unhead/vue/components` [source](./references/docs/0.vue/head/guides/1.core-concepts/1.components.md:L8)

- NEW: `DeprecationsPlugin` from `@unhead/vue/plugins` — re-enables removed `vmid`, `hid`, `children`, `body` properties for gradual migration to v2 [source](./references/docs/0.vue/head/guides/0.get-started/1.migration.md#removed-vmid-hid-children-body)

**Also changed:** `@unhead/schema` deprecated — use `@unhead/vue/types` instead · `createHeadCore` deprecated — use `createUnhead` · Default SSR tags auto-inserted in v2 (`charset`, `viewport`, `html lang="en"`); disable with `createHead({ disableDefaults: true })` · CJS exports removed, ESM only · Vue 2 support removed · `useHead()` context lost after `async` in Vue lifecycle hooks — fetch data first, then call `useHead()`

## Best Practices

- Always use `injectHead()` from `@unhead/vue` instead of `getActiveHead()` from `unhead` in Vue components — `injectHead()` binds to the Vue component context (visible in `onServerPrefetch`), while `getActiveHead()` returns a shared cross-request instance that breaks in SSR. The maintainer confirmed this is the correct approach for Vue. [source](./references/discussions/discussion-362.md)

- Avoid calling `useHead()` inside watchers — each call creates a new entry rather than updating the existing one, leading to duplicate entries. Instead, pass reactive refs or computed getters directly to a single `useHead()` call at setup time so updates flow automatically. [source](./references/docs/0.vue/head/guides/1.core-concepts/0.reactivity-and-context.md#can-i-use-usehead-inside-a-watcher)

- When `useHead()` must be called after async operations (e.g. inside `onMounted`), capture the head instance at setup time with `injectHead()` and pass it as `{ head }` in the second argument — Vue's inject context is lost after `await`. For most cases, prefer the reactive state pattern: define `useHead()` once at setup with computed getters, and update a `ref` asynchronously. [source](./references/docs/0.vue/head/guides/1.core-concepts/0.reactivity-and-context.md#solution-3-using-injecthead)

- Use `useHeadSafe()` instead of `useHead()` whenever head input comes from user-provided or third-party sources — it enforces an attribute whitelist and strips script tags and event handlers, preventing XSS without requiring manual sanitization. [source](./references/docs/head/7.api/composables/1.use-head-safe.md#how-it-works)

- Add the `UnheadVite()` plugin from `@unhead/addons/vite` to your Vite config for Vue apps — it tree-shakes server-only composables from the client build and transforms `useSeoMeta()` calls into raw `useHead()` calls, saving ~3kb. Nuxt configures this automatically; standalone Vue apps must opt in. [source](./references/docs/head/1.guides/2.advanced/9.vite-plugin.md#how-do-i-configure-the-plugin)

- Pass `{ mode: 'server' }` to `useHead()` for static SEO metadata (Open Graph images, robots, schema.org) that doesn't need client-side reactivity — this strips the tags from the client bundle entirely. Similarly use `{ mode: 'client' }` for analytics scripts to keep them out of SSR output. Caveat: `titleTemplate` must be included in both environments to avoid title flashing. [source](./references/docs/head/1.guides/2.advanced/7.client-only-tags.md#how-do-i-add-server-only-tags)

- Use `tagPosition: 'bodyClose'` for non-critical scripts (analytics, chat widgets) instead of `head` — this prevents render-blocking and improves page load performance. Use `tagPriority: 'critical' | 'high' | 'low'` aliases rather than raw numbers to preserve Capo.js-derived ordering weights that Unhead applies automatically. [source](./references/docs/head/1.guides/1.core-concepts/2.positions.md#how-do-i-set-tag-priority)

- Use `textContent` instead of `innerHTML` for inline scripts and styles — `textContent` escapes HTML characters, preventing injection. Only use `innerHTML` when HTML entities are required, and sanitize the content yourself (e.g. with DOMPurify). For user-generated inline content, prefer `useHeadSafe()` which restricts scripts to `type="application/json"` only. [source](./references/docs/head/1.guides/1.core-concepts/4.inner-content.md#when-should-i-use-innerhtml-vs-textcontent)

- Register `TemplateParamsPlugin` and define global `templateParams` (e.g. `siteName`, `separator`) once in your head instance setup rather than repeating them per page. These params work across all head tags — including `og:title` and `meta` descriptions — not just `titleTemplate`. Set `%separator` to a smart separator like `·` or `—`; it auto-removes when adjacent to empty content. [source](./references/docs/head/1.guides/plugins/6.template-params.md#how-do-i-maintain-brand-consistency)

- Use `InferSeoMetaPlugin` to automatically derive `og:title` and `og:description` from existing `title` and `description` tags, eliminating manual duplication. Configure `ogTitle` with a transform function to strip the site name suffix from Open Graph titles (e.g. removing `"| My Site"` that `titleTemplate` appends). [source](./references/docs/head/1.guides/plugins/infer-seo-meta-tags.md#how-do-i-customize-the-og-title)
