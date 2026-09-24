---
name: vuetify-skilld
description: Vue Material Component Framework. Use when writing, debugging, or configuring code that imports vuetify v4.x. Covers createVuetify setup, components and labs, composables, theming, icons, dates and locale, styles and SASS variables, treeshaking, and v3 to v4 migration.
---

# vuetify@4.0.1

Material Design component framework for Vue 3. Source citations like `lib/framework.js:15` refer to the prepared `vuetify@4.0.1` package (`package.json:4`).

## Environment limits

- Vue `^3.5.0` peer dependency (`package.json:208`). No Vue 2 support; Vuetify 2 is EOL (`README.md:274`).
- ESM only: `"type": "module"` (`package.json:32`).
- Optional peers: `vite-plugin-vuetify >=2.1.0`, `webpack-plugin-vuetify >=3.1.0`, `typescript >=4.7` (`package.json:205`).
- Modern browsers, Safari 13+ with polyfills, minimum design width 320px (`README.md:159`).
- Default font is Roboto; you must add it yourself, e.g. `@fontsource/roboto` (https://vuetifyjs.com/getting-started/installation/).

## Setup

Vite with automatic treeshaking (preferred). The vuetify plugin must come after the vue plugin:

```js
// vite.config.js
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
export default defineConfig({ plugins: [vue(), vuetify()] })
```

```js
// src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
export default createVuetify({
  // components, directives not needed with the loader plugin
})
```

Without a loader plugin, register manually; wildcard imports include everything and slow development builds:

```js
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
createVuetify({ components, directives })
```

`createVuetify` accepts `aliases`, `blueprint`, `components`, `date`, `defaults`, `directives`, `display`, `goTo`, `icons`, `locale`, `ssr`, `theme` and returns `{ install, unmount, defaults, display, theme, icons, locale, date, goTo }` (`lib/framework.js:15`). Install with `app.use(vuetify)`; wrap the app in a single `<v-app>` root.

For SSR frameworks (Nuxt, vite-ssr) set `ssr: true` so display values render correctly (https://vuetifyjs.com/getting-started/installation/).

Scaffolding: `pnpm create vuetify` / `npm create vuetify@latest` (`README.md:44`).

CDN bundle with everything included: `vuetify/dist/vuetify.js` (`package.json:35`).

## Components

- Prefer imports from `vuetify/components/<Group>` over `vuetify/components` (loads only needed styles in dev).
- Labs components are NOT production ready; import from `vuetify/labs/<Name>` or `vuetify/labs/components`. In 4.0.1 labs holds: VAvatarGroup, VColorInput, VCommandPalette, VDateInput, VFileUpload, VIconBtn, VMaskInput, VPicker, VPie, VStepperVertical, VPullToRefresh, VVideo (`lib/labs/components.js:1`).
- Dynamic `<component :is>` is invisible to the loader plugin; import those components manually (https://vuetifyjs.com/features/treeshaking/).
- Full inventory and export paths: [references/exports.md](./references/exports.md)

## Configuration

- Theme: the v4 default is `system` (follows `prefers-color-scheme`), not `light` (`lib/composables/theme.js:10`). Pin it with `theme: { defaultTheme: 'light' }` if system switching is unwanted.
- Defaults: set prop defaults per component with `createVuetify({ defaults: { VBtn: { ... } } })`. `class` and `style` work only on component keys, never in the `global` key (https://vuetifyjs.com/features/global-configuration/).
- Display: v4 breakpoints changed; defaults are `sm 600, md 840, lg 1145, xl 1545, xxl 2138` (`lib/composables/display.js:10`).
- Icons: default set is `mdi` and expects the `@mdi/font` stylesheet, or use `mdi-svg` for bundled SVG icons (https://vuetifyjs.com/features/icon-fonts/).
- Dates: default adapter wraps native `Date`; swap with any date-io adapter (https://vuetifyjs.com/features/dates/).
- Blueprints: `createVuetify({ blueprint: md3 })` applies a design-system preset; explicit options override the blueprint (`lib/framework.js:15`, `lib/blueprints/index.js:1`).
- Details and examples: [references/configuration.md](./references/configuration.md)

## Composables

All exported from the `vuetify` entry point (`lib/composables/index.js:1`): `useDate`, `useDefaults`, `useDisplay`, `useGoTo`, `useLayout`, `useLocale`, `useRtl`, `useTheme`, `useHotkey`, `useMask`.

```vue
<script setup>
import { useTheme } from 'vuetify'
const theme = useTheme()
theme.toggle() // light <-> dark
</script>
```

For hotkeys prefer the `cmd` modifier (`useHotkey('cmd+s', save)`); it resolves to Command on Mac and Control elsewhere (`lib/composables/hotkey/key-aliases.js:10`).

Full API per composable: [references/composables.md](./references/composables.md)

## Styles

- `import 'vuetify/styles'` is the all-in-one precompiled CSS; modular entries are `vuetify/styles/core` (must be first), `vuetify/styles/colors`, `vuetify/styles/utilities` (`package.json:61`).
- SASS variable overrides require the sass preprocessor and `vuetify({ styles: { configFile: 'src/styles/settings.scss' } })` in the loader plugin; use `@use 'vuetify/settings' with (...)`.
- v4 styles ship in cascade layers (`vuetify-core`, `vuetify-components`, `vuetify-overrides`, `vuetify-utilities`, `vuetify-final`); unlayered user CSS now always wins over Vuetify.
- Entry points, variables, layers, Tailwind interop, legacy grid restore: [references/styling.md](./references/styling.md)

## Migrating from v3

v4 is a breaking MD3 release. Highest-impact changes:

- Grid uses CSS `gap`; `dense` is now `density="compact"`, `align`/`justify`/`order`/`align-self` props replaced by utility classes. VRow gains a `gap` prop (`lib/components/VGrid/VRow.js:154`).
- Typography variants renamed: `h1`-`h3` -> `display-*`, `h4`-`h6` -> `headline-*`, `subtitle-1`/`body-1` -> `body-large`, `caption` -> `body-small`, `button`/`subtitle-2` -> `label-large`.
- Elevation reduced from levels 0-24 to 0-5 (`lib/styles/settings/_elevations.scss:6`).
- `VSelect`/`VCombobox`/`VAutocomplete` slot `item` renamed to `internalItem`; `item` is now an alias for `internalItem.raw`.
- `VForm` slot values (`isValid`, `errors`, ...) are unwrapped, no longer refs.
- Defaults merging skips `undefined`; use `null` to override a global default.

Full change list with compat snippets: [references/migration-v4.md](./references/migration-v4.md)

## Common pitfalls

- Missing icon font: components render blank icons until `@mdi/font` CSS (or an SVG set) is installed.
- Missing Roboto font: text renders with fallback font (`README.md:159`).
- Styles broken after adding custom CSS: check layer order; place overrides inside `@layer vuetify-overrides` or declare your layer order explicitly.
- `VNumberInput` uses `toFixed()` internally; for arbitrary-precision decimals use `v-text-field` with decimal.js (`lib/components/VNumberInput/VNumberInput.js:81`, https://vuetifyjs.com/components/number-inputs/).
- Do not use `vuetify/styles` inside SASS files; it resolves to precompiled CSS. Use `vuetify` or `vuetify/settings` (https://vuetifyjs.com/features/sass-variables/).

## References

- [references/exports.md](./references/exports.md) — entry points, component inventory, directives, iconsets, locale
- [references/configuration.md](./references/configuration.md) — every `createVuetify` option with examples
- [references/composables.md](./references/composables.md) — public composables API
- [references/styling.md](./references/styling.md) — CSS and SASS entry points, variables, layers
- [references/migration-v4.md](./references/migration-v4.md) — v3 to v4 breaking changes and compat snippets

Official documentation: https://vuetifyjs.com. Release notes by URL: https://vuetifyjs.com/getting-started/release-notes/.
