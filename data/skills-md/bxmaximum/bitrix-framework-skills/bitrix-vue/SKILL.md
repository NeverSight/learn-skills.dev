---
name: bitrix-vue
description: 'BitrixVue 3 (ui.vue3) — createApp, $Bitrix.Loc, kernel Vue components, Pinia, markRaw for kernel widgets, Vue 2 migration. Use when building reactive UI with Vue inside Bitrix pages, components or extensions.'
---

# BitrixVue 3

Baseline: main 23.0+ · Verified: main 26.800.0, ui 26.687.0

`ui.vue3` = Vue 3 + the BitrixVue plugin (`$Bitrix`), one shared Vue for the whole page. Runtime template compilation; no SFC `.vue`, no SSR. Vue 2 (`ui.vue`, global `BX.BitrixVue`) is legacy — don't start new code on it.

## In an extension (preferred)

```javascript
import { BitrixVue, ref } from 'ui.vue3';

BitrixVue.createApp({
    setup() {
        return { items: ref([]) };
    },
    mounted() {
        BX.ajax.runAction('vendor:module.item.list').then((r) => {
            this.items = r.data.items;
        });
    },
    template: `
        <h2>{{ $Bitrix.Loc.getMessage('VENDOR_ITEMS_TITLE') }}</h2>
        <div v-for="item in items" :key="item.id">{{ item.name }}</div>
    `,
}).mount('#vendor-items');
```

- Import `BitrixVue` and every Vue API (`ref`, `computed`, `markRaw`, `defineComponent` …) from `ui.vue3` (kernel canon, not `ui.vue3.bitrixvue`); `rel: ['ui.vue3']` is enough.
- Extension setup and phrases: `bitrix-extensions`.

## On a PHP page (no build)

```php
\Bitrix\Main\UI\Extension::load('ui.vue3');
```

```html
<div id="vendor-app"></div>
<script>
    BX.Vue3.BitrixVue.createApp({ template: '<div>Hello</div>' }).mount('#vendor-app');
</script>
```

Global is `BX.Vue3.BitrixVue`. `BX.BitrixVue` is Vue 2: undefined here, or silently Vue 2 if `ui.vue` is also on the page.

## `$Bitrix` (every component)

| Member | Use |
| --- | --- |
| `$Bitrix.Loc.getMessage(code, {'#N#': n})` | Phrases (from `BX.message`); JS outside Vue: `Loc` from `main.core` |
| `$Bitrix.eventEmitter` | App-scoped `EventEmitter` |
| `$Bitrix.Data.get/set` | App-scoped shared data |
| `$Bitrix.RestClient.get()` / `$Bitrix.PullClient.get()` | Default REST / Pull clients (`bitrix-pull`) |

`BitrixVue.getFilteredPhrases(this, 'VENDOR_')` — first arg is the component instance in Vue 3 (docs show the Vue 2 form without it).

## Kernel pieces

- Components: `ui.vue3.components.*` (`button`, `popup`, `hint`, `switcher` …), e.g. `import { Counter } from 'ui.vue3.components.counter'` (`components: { Counter }` → `<Counter :value="5"/>`; **Since ui 26.200\***; fallback: wrap `ui.cnt` yourself). Widget options: `bitrix-ui`.
- State and routing: `ui.vue3.pinia`, `ui.vue3.vuex`, `ui.vue3.router`.
- Lazy component: `BitrixVue.defineAsyncComponent('vendor.module.heavy', 'HeavyForm')` loads the extension on first render.
- Extensible component: `BitrixVue.mutableComponent(name, def)`; others change it via `mutateComponent()` / `cloneComponent()`.

## Kernel widgets inside Vue

Keep Popup / Menu / Dialog / Popover / ActionPanel instances non-reactive: `this.popup = markRaw(new Popup(...))`, or hold them outside `data()`. Widgets rebuilt since ui 26.650 use native `#private` fields; through a reactive Proxy they throw `TypeError: Cannot read private member`.

## Debug

`define('VUEJS_DEBUG', true);` in `/local/php_interface/init.php` (dev only) → dev build + devtools; with it, `VUEJS_LOCALIZATION_DEBUG` shows phrase codes instead of text.

## From Vue 2 (`ui.vue`)

- `BX.BitrixVue` / `import … from 'ui.vue'` → `ui.vue3`.
- `BitrixVue.component()` / `.directive()` do not register in Vue 3 (console error): use local `components: {}`, `app.component()` or `mutableComponent()`.
- `getFilteredPhrases(prefix)` → `getFilteredPhrases(this, prefix)`; `destroyed` → `unmounted`; no filters, no `$on`/`$off`.

## Checklist

- [ ] `ui.vue3` only; all imports from `ui.vue3`; inline scripts use `BX.Vue3.BitrixVue`.
- [ ] Kernel widget instances wrapped in `markRaw()`.
- [ ] Phrases via `$Bitrix.Loc` / `Loc`, never hard-coded.
- [ ] Server calls via `BX.ajax.runAction` (CSRF included), not raw `fetch`.
- [ ] Pull subscriptions removed in `unmounted`.
