---
name: bascik-compatibility
description: Decide which HTML, CSS, and JavaScript features to use in a Bascik site. Use before reaching for a modern or unusual feature (popover, dialog, invoker commands, anchor positioning, container queries, @layer, @scope, :has(), view transitions, nesting, light-dark(), TypeScript in the browser, web components); when asking "can I use X", "does Bascik support X", or "is X Baseline"; when a selector, DOM call, or at-rule works in a page but not in a component; or when the linter reports css-* or js-* compatibility errors. Includes a live lookup of Bascik's compatibility matrix and a Baseline browser support checker.
license: MIT
metadata:
  author: bascik
  homepage: https://bascik.dev
---

# HTML, CSS, and JavaScript Compatibility

Every feature passes two gates: **browsers** must support it for your audience, and inside a component **Bascik's scoping** must handle it. Page markup, page `<style>` and `<script>` blocks, and global stylesheets are not renamed, so anything a browser supports works there. Requires the `bascik` skill; `bascik-components` has the scoping rules.

## Gate 1: browser support

```sh
node <skills-dir>/bascik-compatibility/scripts/baseline.mjs popover anchor-positioning "invoker commands"
```

| Status               | Decision                                                                                              |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
| Widely available     | Use it                                                                                                |
| Newly available      | Use it when the page still works without it, or behind `@supports` or a feature check with a fallback |
| Limited availability | Enhancement only, inside `@supports` or `if ('x' in ...)`, never for content or navigation            |

Never guess support from memory; statuses change every few months. The script queries the Web Platform Status API (the web-features data behind MDN and caniuse) and can take several seconds per feature. Prefer features that degrade to something usable.

## Gate 2: Bascik scoping (components only)

```sh
node <skills-dir>/bascik-compatibility/scripts/lookup.mjs container
node <skills-dir>/bascik-compatibility/scripts/lookup.mjs setAttribute
node <skills-dir>/bascik-compatibility/scripts/lookup.mjs --list
```

`lookup.mjs` searches every row of the live matrix at https://bascik.dev/compatibility and prints ✓ supported, △ partial, ✕ unsupported, or – not yet. Look up anything you have not used before in a component.

The surprises that matter most:

- **Container, layer, anchor, and view-transition names are scoped per component type** and invisible to other components. A child cannot query its parent's named container (use an unnamed `@container (...)`), a global `@layer` order does not place component layers, and two instances share one `anchor-name` or `view-transition-name`. Read `/compatibility#names-shared-by-every-instance` before using any of them.
- **Element names are not converted inside `:is()`, `:where()`, `:has()`,** and element selectors never reach slotted content or elements a script creates. Exception that is safe: `.markdown :is(p, ul)` (a scoped class, then a descendant combinator) matches every descendant, slotted content included, and is not flagged.
- **Attribute selectors are not scoped:** anchor them on a class in CSS, and never use them in `querySelector`.
- **`name` ships as written** (`scoping.attributes.name` is off by default): `FormData` keys, radio groups, `<details name>` accordions, `<iframe>` targets, and `<map>` names behave as the HTML standard defines them, across every component instance on the page. A component holding a whole radio group needs its own `<form>`, or `data-bascik-attr-name="group"` (no literal `name`) with a per-usage prop; the linter warns `shared-name-group`. With `scoping.attributes.name: true`, every `name` but `<meta name>` is scoped per instance and `data-bascik-preserve="name"` keeps one literal. Read `/component-best-practices#name-form-controls-and-groups`.
- **TypeScript runs in the browser only** through `<script type="text/typescript">` or a companion `.ts` file, with erasable syntax.
- **Not provided by design:** API middleware, schema validation, automatic CORS, and API response compression. Write them in the handler.

## Lint rules

`bascik --check` (through `@bascik/language-server`, and run by `verify.mjs`) reports these as errors:

| Rule                         | Pattern                                                                                                                                                                                              | Use instead                                                                                                                                                                                                                                                               |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `js-id-setter`               | `el.id = 'x'`                                                                                                                                                                                        | `setAttribute('id', ...)` with a value derived from a scoped ID, or keep the element reference                                                                                                                                                                            |
| `js-attribute-selector`      | `querySelector('[data-x]')`                                                                                                                                                                          | `getElementById`, a static class, or `.children` of an element found by ID                                                                                                                                                                                                |
| `js-template-classname`      | `` el.className = `a ${b}` ``                                                                                                                                                                        | `classList.add/remove/toggle` with static names                                                                                                                                                                                                                           |
| `js-style-setproperty`       | `el.style.setProperty('--x', v)`                                                                                                                                                                     | A `data-` attribute styled in CSS, or a global token the component does not declare                                                                                                                                                                                       |
| `js-unsupported-dom-methods` | `removeAttribute/hasAttribute/toggleAttribute('class' \| 'id' \| 'name')`                                                                                                                            | `classList` or the element reference                                                                                                                                                                                                                                      |
| `js-document-class-query`    | `document.querySelector('.cls')`, `querySelector('.a .b')`, `getElementsByClassName('cls')[0]` (warning; a selector with `#id` is per-instance and not flagged)                                      | `document.getElementById` or `rootEl.querySelector('.cls')` for per-instance lookup                                                                                                                                                                                       |
| `js-dynamic-id-lookup`       | `getElementById(targetId)`, `getElementById("pre-" + n)`, ``getElementById(`item-${i}`)`` (warning; only a `"`/`'` string literal is rewritten, and custom `data-*` attribute values are not scoped) | `getElementById('my-id')`, a standard ID-reference attribute Bascik rewrites, read back (`getElementById(btn.getAttribute("popovertarget"))`; also `aria-controls`, `commandfor`, `for`, `href="#my-id"` with `.slice(1)`), or `btn.closest()` / `rootEl.querySelector()` |
| `css-is-element-names`       | `:is(h2)`, `:has(img)`                                                                                                                                                                               | Classes inside the pseudo-class, or a global stylesheet                                                                                                                                                                                                                   |
| `css-attribute-selector`     | `[data-state]:hover {}` or `[data-state]:not(.disabled) {}` at the start of a selector                                                                                                               | `.card[data-state] {}`; a class in `:not()` is not an anchor                                                                                                                                                                                                              |
| `css-id-attribute-selector`  | `[id] {}`, `[id="x"] {}`, `.a:not([id])`, `.a[id]` (all stripped)                                                                                                                                    | `#x {}` or a class                                                                                                                                                                                                                                                        |
| `css-reserved-class-prefix`  | `.b_el_p {}`, `.b_id_btn {}` (warning; `b_el_` and `b_id_` start the classes Bascik generates for `p` and `#btn`)                                                                                    | Another class name, such as `.el-p` or `.item__p`                                                                                                                                                                                                                         |

## Look it up

| How do I...                                       | Read                                                 |
| ------------------------------------------------- | ---------------------------------------------------- |
| See every supported and unsupported pattern       | `/compatibility`                                     |
| Use popover, dialog, and other HTML-first widgets | `/how-to/interactivity`                              |
| Use a third-party custom element                  | `/how-to/third-party-web-components`                 |
| Use `light-dark()` and color schemes              | `/how-to/theming`                                    |
| Use TypeScript in a component                     | `/scoped-javascript#typescript-in-component-scripts` |

`node <skills-dir>/bascik/scripts/read-doc.mjs <path>` prints any of these.
