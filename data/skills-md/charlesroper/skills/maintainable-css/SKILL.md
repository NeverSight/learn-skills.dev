---
name: maintainable-css
description: >-
  Plan, author, refactor and review CSS and HTML markup using Adam Silver's MaintainableCSS methodology. Use when designing modular CSS architecture, naming semantic classes with lowerCamelCase module/component/state/modifier conventions, untangling high-specificity legacy stylesheets or migrating away from utility and visual class patterns.
license: CC BY-NC-SA 4.0 concepts from maintainablecss.com, adapted for project use
metadata:
  author: Charles Roper
  based_on: Adam Silver's MaintainableCSS
  source: https://maintainablecss.com/
  version: "2.0"
---

# MaintainableCSS architecture

Author, refactor and review modular, low-specificity CSS and semantic HTML markup using Adam Silver's MaintainableCSS methodology.

## Procedure

1. **Map module boundaries.** Inspect the target markup and stylesheets to partition the UI into independent modules and internal components using the **standalone boundary test**. When resolving complex nesting, JS state bindings, modifier thresholds or A/B versioning, read [references/maintainable-css-manual.md](references/maintainable-css-manual.md). *Completion: Every UI element is classified as a root module or a child component with zero ambiguous ownership.*
2. **Define the semantic rename map.** Assign `lowerCamelCase` names to every module, component, state and modifier based on what the element is rather than how it looks. *Completion: Complete class map follows `.<module>[-<component>][-<state>|--<modifier>]` with zero visual, utility or unprefixed state names.*
3. **Update markup hooks before CSS.** Apply the semantic classes to HTML templates first, adding explicit `.module-component` classes wherever child modules can nest, and pairing ARIA state attributes with module-prefixed state classes. Then rewrite CSS selectors to single-class specificity with co-located `@media` rules. *Completion: Markup and CSS use single-class module-prefixed selectors with zero ID styling hooks and zero chained state selectors.*
4. **Prune dead rules and verify.** Delete orphaned selectors, superseded utility hooks and unused override chains, then run the project linter or build check and verify against the 5-point checklist below. *Completion: Dead selectors are removed, build checks pass and all five checklist items are satisfied.*

## Core architecture

### 1. Naming and delimiter grammar

Every class follows one delimiter grammar using `lowerCamelCase` for multi-word tokens:

```css
.searchResults {}                    /* Module: root container */
.searchResults-heading {}            /* Component: child part */
.searchResults-isLoading {}          /* Module state */
.searchResults-item-isSelected {}    /* Component state */
.categoryHeader--boys {}             /* Module modifier */
.button-icon--small {}               /* Component modifier */
```

- **Why `lowerCamelCase` is mandatory:** Hyphens are structural delimiters separating module, component, state and modifier segments. Writing `.search-results-heading` breaks delimiter parsing; always write `.searchResults-heading`.
- **Semantic over visual:** Name elements by domain role (`.basket`, `.orderSummary`, `.primaryNav`), never by visual traits (`.red-text`, `.mt-4`, `.grid-3col`).
- **Single-class specificity:** Target classes directly (`.searchResults-heading`). Never style with `#id` selectors; reserve `id` attributes strictly for label associations, fragment anchors and `aria-*` wiring.

### 2. Module vs component boundary test

- **Standalone boundary test:** Ask *"Can this piece of UI exist independently outside its parent?"*
  - **Yes:** Make it its own `.module` (for example `.logo` or `.button` inside `.header`).
  - **No:** Make it a `.module-component` owned by the parent (for example `.header-navWrapper` or `.basket-title`).
- **Leaf vs nestable containers:** Unscoped descendant tag selectors (`.article p`, `.article h2`) are safe only in leaf prose containers that never host child modules. If a container can hold nested modules, put explicit `.module-component` classes on its children so parent tag styles never bleed into nested modules.

### 3. State and ARIA pairing

- **Prefix states with the owner:** Write `<div class="basket basket-isEmpty">` or `<li class="nav-item nav-item-isActive">`.
- **No chained state selectors:** Style `.basket-isEmpty` as a single flat selector, never `.basket.isEmpty`. Unprefixed states collide across modules and double selector specificity.
- **Pair ARIA with state classes:** Use `aria-expanded`, `aria-selected`, `aria-invalid` and `hidden` for assistive technology, and apply the matching `.module-isState` class for visual styling rather than styling `[aria-*]` attribute selectors alone.

### 4. Modifiers vs new modules

- **Small deltas only:** Use `--modifier` classes (`<button class="button button--secondary">`) only for small, well-understood visual tweaks (colour, size or background variant) where structure and behaviour stay identical.
- **Split when overrides grow:** If a variation changes layout structure, adds new child components or overrides most of the base rules, create a separate module instead of a modifier.

### 5. Reuse, JavaScript and versioning

- **Reuse modules, not declarations:** If two components represent different domain concepts (`basket` vs `orderSummary`), keep them in separate modules even when their CSS rules look similar today. Share CSS only when semantics, visuals and evolution are identical.
- **Decouple JavaScript from CSS:** Reuse JS behaviour across modules by passing the module's own state class (`basket-isHidden`, `dropdown-isHidden`) or binding via data/JS hooks rather than forcing distinct modules to share a global `.isHidden` class, unless the visual transition is identical everywhere.
- **Parallel versioning for A/B tests and redesigns:** To test or migrate a redesigned module, duplicate it as `.basket2` (`.basket2-title`, `.basket2-isEmpty`) alongside `.basket`. Never layer conditional override chains onto the live module; delete the losing version once rollout completes.
- **Co-locate breakpoints and files:** Place `@media` queries directly inside or immediately beneath the module they modify, never in a global `responsive.css` file. Organise stylesheets either by module file (`basket.css`) or clearly delineated module sections so deleting a module removes all of its CSS in one edit.

## Verification checklist

Before delivering CSS and markup, verify all five criteria:

1. **Delimiter grammar:** Every multi-word token uses `lowerCamelCase` and every class conforms to `.<module>[-<component>][-<state>|--<modifier>]`.
2. **Module encapsulation:** Nested modules cannot inherit unwanted tag styles from parent modules, and every standalone UI unit is its own `.module`.
3. **Flat specificity:** Zero `#id` selectors are used for styling and zero state rules use chained `.module.isState` selectors.
4. **Bounded modifiers:** Every `--modifier` changes only minor visual properties; structural diverges are split into distinct modules.
5. **Co-located rules:** `@media` queries, states and modifiers sit directly alongside their owning module with zero orphaned selectors left behind.
