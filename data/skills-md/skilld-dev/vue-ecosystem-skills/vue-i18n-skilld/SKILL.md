---
name: vue-i18n-skilld
description: Use when writing or debugging code that imports vue-i18n (Vue 3 internationalization). Covers createI18n, useI18n, message syntax, i18n-t/i18n-n/i18n-d components, pluralization, datetime and number formatting, TypeScript schemas, lazy loading, bundle optimization, and v10/v11/v12 migration.
---

# vue-i18n 11.4.12 (Vue 3)

Internationalization plugin for Vue.js.

- Peer dependency: `vue` `^3.0.0` (package.json:44). No Vue 2 support; use vue-i18n v8 for Vue 2.
- Node engines: `>= 22` (package.json:47).
- For Nuxt 3, use `@nuxtjs/i18n` instead of installing this directly (https://vue-i18n.intlify.dev/guide/integrations/nuxt3.html).

## Core rules

1. **Default to Composition API mode.** Pass `legacy: false` to `createI18n` and use `useI18n()`. Legacy API mode (`legacy: true`, the default) is deprecated in v11 and removed in v12 (dist/vue-i18n.d.ts:1728).
2. **Do not use the `v-t` directive** in new code. Deprecated in v11, removed in v12 (dist/vue-i18n.d.ts:2138). Use `t()`, `$t`, or the `<i18n-t>` component.
3. **`tc` and `$tc` no longer exist.** Dropped in v11; `t`/`$t` handle pluralization via the plural option (verified: no `tc` export in dist/vue-i18n.d.ts).
4. **Interpolation uses `{name}` syntax.** The v8 modulo `%` syntax was dropped in v10 (https://vue-i18n.intlify.dev/guide/migration/breaking10.html#drop-modulo-syntax).
5. **Messages are compiled at runtime (JIT) by default since v10.** For CSP-strict environments or best performance, pre-compile with `@intlify/unplugin-vue-i18n` (https://vue-i18n.intlify.dev/guide/advanced/optimization.html).
6. **Never interpolate user input into messages rendered with `v-html`** without `escapeParameter: true`; translate content, do not concatenate HTML.

## Setup

```js
// i18n.js
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false, // Composition API mode
  locale: 'ja',
  fallbackLocale: 'en',
  messages: {
    en: { message: { hello: 'hello world' } },
    ja: { message: { hello: 'こんにちは、世界' } }
  }
})

export default i18n
```

```js
// main.js
import { createApp } from 'vue'
import App from './App.vue'
import i18n from './i18n'

createApp(App).use(i18n).mount('#app')
```

`app.use(i18n)` installs the `$t`/`$d`/`$n`/`$rt` global properties (when `globalInjection: true`, the default), enables `useI18n`, and globally registers `i18n-t`, `i18n-d`, `i18n-n` (when `globalInstall: true`, the default; dist/vue-i18n.d.ts:1810-1822).

## Translate in a component

```vue
<script setup>
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()
</script>

<template>
  <h1>{{ t('message.hello') }}</h1>
  <p>{{ t('greeting', { name: 'Kyoko' }) }}</p>
  <p>{{ $t('message.hello') }}</p><!-- works in templates via globalInjection -->
</template>
```

Call `useI18n()` inside `setup` only. It throws "Must be called at the top of a `setup` function" otherwise.

## Common tasks

**Pluralize.** Message: `'no apples | one apple | {count} apples'` (pipe-separated forms, selected by plural rules for the locale).

```js
t('apple', count, { count }) // or t('apple', { count }, choice)
```

Custom rules: `pluralRules` on `Composer` options (Composition), `pluralizationRules` (Legacy).

**Format dates and numbers.**

```js
const { d, n } = useI18n()
d(new Date(), 'long') // named format from datetimeFormats option, else Intl fallback
n(1234567, 'currency') // named format from numberFormats option
```

**Interpolate components.** Use `<i18n-t keypath="..." tag="p">` with slot children per placeholder; see [components](./references/components.md).

**Switch locale.** `locale.value = 'en'` from a Composer; also update the document `lang` attribute and, on SSR, the `Accept-Language` handling (https://vue-i18n.intlify.dev/guide/advanced/lazy.html).

**Lazy load locales.** Dynamic `import()` plus `setLocaleMessage` / `mergeLocaleMessage`; see [optimization](./references/optimization.md).

## Type-safe keys

Augment the global `DefineLocaleMessage`, `DefineDateTimeFormat`, `DefineNumberFormat` interfaces to get key completion and inference in `useI18n` without generics; see [typescript](./references/typescript.md).

## Pitfalls

- `useI18n({ messages: ... })` creates a local scope; without `useScope: 'global'` local messages do not merge with global ones (https://vue-i18n.intlify.dev/guide/essentials/scope.html).
- `$t` in templates requires `globalInjection: true` in Composition mode (dist/vue-i18n.d.ts:1735-1746).
- Vue warns about a missing `locale` message with key fallback to the key itself; configure `missing`/`missingWarn`/`fallbackWarn` to control noise.
- Linked messages (`@:key`), literal `{` `}`, and `@` `|` in messages need escaping; see [message-syntax](./references/message-syntax.md).
- Do not import from deep paths such as `vue-i18n/dist/*` in bundler projects; use the package root so the correct build resolves (package.json:63-83).

## Migration status

| Change | Version | Action |
| --- | --- | --- |
| Legacy API mode deprecated | v11 | Move to `legacy: false` before v12 (dist/vue-i18n.d.ts:1728) |
| `v-t` directive deprecated | v11 | Replace with `t()`/`$t`/`<i18n-t>` (dist/vue-i18n.d.ts:2138) |
| `tc`/`$tc` removed | v11 | Use `t`/`$t` plural option |
| JIT message compilation default | v10 | Pre-compile for strict CSP |
| `%` named interpolation removed | v10 | Use `{name}` |
| `$t` positional overload changed | v10 | Pass plural via options object |

Details: [migration](./references/migration.md).

## References

- [composition-api](./references/composition-api.md): createI18n, useI18n, Composer members, scopes, locale switching
- [message-syntax](./references/message-syntax.md): interpolation, pluralization, linked messages, HTML safety
- [components](./references/components.md): i18n-t, i18n-n, i18n-d
- [formats](./references/formats.md): datetime and number formatting, custom format definitions
- [typescript](./references/typescript.md): schema typing, generated locale types
- [optimization](./references/optimization.md): tree shaking flags, pre-compilation, lazy loading, dist files
- [migration](./references/migration.md): v9, v10, v11 breaking changes and v12 removals
- [legacy-api](./references/legacy-api.md): Legacy API mode surface still present in v11

Official documentation: https://vue-i18n.intlify.dev/
API reference: https://vue-i18n.intlify.dev/api/general.html
Changelog (cited, not copied): https://github.com/intlify/vue-i18n/blob/master/CHANGELOG.md
