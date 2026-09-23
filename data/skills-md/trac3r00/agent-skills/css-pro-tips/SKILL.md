---
name: css-pro-tips
description: Use when writing, reviewing, refactoring, or modernizing CSS/Tailwind with source-validated patterns for resets, box sizing, focus styles, centering, aspect ratios, selectors, layout, modern CSS, progressive enhancement, older-pattern modernization, MDN Baseline support buckets, user-preference media queries (reduced motion, contrast, forced colors, reduced transparency), container size and style queries, @property, popovers, View Transitions, custom highlights, scroll-state queries, text-box trim, and typed attr().
version: 1.0.0
license: MIT (from PyModel/css-pro-tips; see LICENSE.txt)
metadata:
  agentskills:
    tags: [css, tailwind, frontend, modern-css]
---

# CSS Protips — Validated Skill

This skill is a source-validated update of the uploaded `css-protips` Markdown skill. It keeps the useful practical guidance, corrects current compatibility status where needed, adds explicit references for each claim, and now includes an expanded set of modern CSS tricks validated against MDN/web platform references.

## How to use this skill

Use this skill when writing, reviewing, or modernizing CSS. Prefer the “Validated patterns” section for day-to-day code. Use the “Modern CSS support buckets” section when deciding whether a feature can ship as normal production CSS or should be guarded with `@supports`. Use the “Retire or modernize older tips” section when replacing older CSS tricks with current native features.

## Validation rules used

1. **Compatibility language is source-bound.** “Widely available,” “Newly available,” and “Limited availability” follow MDN Baseline definitions unless a different source is named.
2. **Baseline is not QA.** Baseline says whether a web platform feature is broadly implemented across core browsers; it does not replace accessibility, keyboard, contrast, motion, performance, or project-specific testing.
3. **Progressive enhancement is required for limited or audience-dependent features.** If browser support is incomplete for your audience, ship a working fallback first, then add the enhanced rule with `@supports`.
4. **Do not turn tips into global rules blindly.** Global selectors such as `:empty`, `* + *`, or blanket resets can affect third-party widgets, CMS content, accessibility, or embedded components. Scope them unless the whole project explicitly opts in.

References: [MDN Baseline][ref-baseline], [MDN @supports][ref-supports].

## Validation window and status review dates

Statuses in this file were verified against live MDN Baseline banners, MDN browser-compat-data, and web.dev platform updates in **August 2026**.

Several statuses flip on known dates. Check these lines first when revalidating:

| Feature | Current status | Next expected change |
|---|---|---|
| `light-dark()` | Baseline Newly available, May 2024 | Widely available around November 2026 |
| `transition-behavior` | Baseline Newly available, August 2024 | Widely available around February 2027 |
| `@scope` | Baseline Newly available, March 2026 | Widely available around September 2028 |
| Anchor positioning | Baseline Newly available, January 2026 | Widely available around July 2028 |
| `field-sizing` | Baseline Newly available, June 2026 | Widely available around December 2028 |
| Container style queries, name-only container queries, `:open` | Baseline Newly available, May 2026 | Widely available around November 2028 |
| Scroll-driven animations | Limited, Firefox pending | Baseline whenever Firefox ships |
| `text-box-trim` | Chrome 133+, Safari 18.2+, Firefox 154+ | Baseline once the Firefox release is counted |

---

# Key corrections from the uploaded skill

| Area | Validated decision | Why |
|---|---|---|
| Baseline meaning | Keep the caveat. Baseline is a browser-compatibility signal only, not an accessibility/performance/QA guarantee. | MDN Baseline defines support buckets and explicitly says Baseline is not a substitute for accessibility, performance, and other tests. [MDN Baseline][ref-baseline] |
| Anchor positioning | Update from “Limited availability” to **Baseline 2026 Newly available** for core properties such as `anchor-name`, `position-area`, and `position-try-fallbacks`; still verify support floor and keep fallbacks for older audiences. | MDN now marks key anchor-positioning properties as Baseline 2026 Newly available. [MDN anchor-name][ref-anchor-name], [MDN position-area][ref-position-area], [MDN position-try-fallbacks][ref-position-try-fallbacks] |
| `field-sizing` | Update from “Limited availability” to **Baseline 2026 Newly available**; still use a fallback if your browser floor includes older browsers. | MDN marks `field-sizing` as Baseline 2026 Newly available. [MDN field-sizing][ref-field-sizing] |
| `accent-color` | Keep as **Limited availability**. Use as a progressive enhancement, not as the only brand-control styling mechanism. | MDN marks `accent-color` Limited availability. [MDN accent-color][ref-accent-color] |
| Scroll-driven animations | Keep as **progressive enhancement**. `animation-timeline` remains Limited availability, though Safari 26 now ships it and only Firefox is missing. | MDN marks `animation-timeline` Limited availability. [MDN animation-timeline][ref-animation-timeline], [WebKit scroll-driven animations][ref-webkit-sda] |
| `interpolate-size` / `calc-size()` | Keep as progressive enhancement. Do not treat native `height: auto` interpolation as Baseline. | MDN marks `interpolate-size` and `calc-size()` Limited availability/experimental. [MDN interpolate-size][ref-interpolate-size], [MDN calc-size][ref-calc-size] |
| `transition-behavior` | Use it for discrete transitions such as `display`; it does **not** by itself interpolate `height: 0` to `height: auto`. | MDN defines `transition-behavior` as enabling transitions for discrete animation properties. [MDN transition-behavior][ref-transition-behavior] |
| Generated-content commas/empty-link URLs | Keep only with accessibility/copy-paste caveats. Generated text from `content` may not behave like real DOM text. | MDN documents generated/replaced content and the `attr()` function, including accessibility-oriented alt text syntax. [MDN content][ref-content] |
| Native CSS nesting | Use it as normal production CSS. It reached Baseline Newly available in August 2023 and Widely available in February 2026; MDN confirms browser-native parsing, not preprocessor compilation. | [web.dev Baseline][ref-webdev-baseline], [MDN CSS nesting][ref-nesting] |

---

# Validated patterns

## 1. Use a CSS reset deliberately

A minimal reset can remove browser-default margin/padding and make layout more predictable. Prefer a project-owned reset rather than copy-pasting an aggressive global reset blindly.

```css
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

Validation: `box-sizing` is a widely available property. `border-box` makes the declared width/height include padding and border, which usually makes component sizing easier. [MDN box-sizing][ref-box-sizing]

## 2. Inherit `box-sizing` when components may need overrides

This variant sets the root sizing model once, then lets components inherit it.

```css
html {
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}
```

Validation: `box-sizing` supports `content-box` and `border-box`; inheriting from `html` is a safe pattern when a component needs to override sizing context locally. [MDN box-sizing][ref-box-sizing]

## 3. Use `all: unset` carefully for component resets

`all: unset` resets almost all CSS properties. It excludes `unicode-bidi`, `direction`, and custom properties. Because non-inherited properties go to their initial values, a button can lose its native display/box behavior. Restore layout and focus styles explicitly.

```css
button.reset {
  all: unset;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

button.reset:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 0.15em;
}
```

Use `all: revert` when the intent is “undo author styles and return toward UA/user defaults,” not “strip everything to a blank slate.”

Validation: MDN documents that `all` resets all properties except `unicode-bidi`, `direction`, and CSS custom properties. [MDN all][ref-all]

## 4. Prefer `:focus-visible` for keyboard focus styles

Use `:focus-visible` so keyboard users keep a visible focus indicator without forcing the same ring on every pointer click.

```css
:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 0.15em;
}
```

Validation: MDN describes `:focus-visible` as matching when the user agent determines that focus should be made evident, and notes that people need to know which element has focus. [MDN :focus-visible][ref-focus-visible]

## 5. Add unitless `line-height` to text containers

Set a readable unitless line height on `body` or on text-heavy containers.

```css
body {
  line-height: 1.5;
}
```

Validation: `line-height` sets the height of a line box, and MDN recommends unitless values because descendants inherit the number rather than a computed fixed length. [MDN line-height][ref-line-height]

## 6. Center with Grid or Flexbox

For page-level centering, Grid is concise. Use dynamic viewport block units on mobile when browser toolbars matter.

```css
.center-page {
  min-block-size: 100dvb;
  display: grid;
  place-items: center;
}
```

For flex layouts, set the container’s size and center on both axes.

```css
.center-flex {
  min-block-size: 100dvb;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

Validation: `place-items` aligns items in block and inline directions at once. Flexbox centering uses `align-items` and `justify-content`. Dynamic viewport units represent viewport dimensions that update as browser UI expands/retracts; MDN also notes that dynamic units can resize during scrolling, so test the result. [MDN place-items][ref-place-items], [MDN flex alignment][ref-flex-align], [MDN viewport units][ref-viewport-units]

## 7. Use `aspect-ratio` for media boxes

Prefer `aspect-ratio` over wrapper/padding hacks for modern browsers.

```css
.media {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.media > img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

Validation: `aspect-ratio` sets a preferred width-to-height ratio; `object-fit: cover` preserves aspect ratio while filling and clipping as needed. [MDN aspect-ratio][ref-aspect-ratio], [MDN object-fit][ref-object-fit]

## 8. Use `:not()` for exclusion selectors

Use `:not()` to apply styles to everything except the excluded case.

```css
.nav li:not(:last-child) {
  border-inline-end: 1px solid #666;
}
```

Validation: `:not()` matches elements that are not represented by its argument selector list. [MDN :not][ref-not]

## 9. Use `:is()` for compact selector lists

Use `:is()` to reduce repeated selector groups.

```css
:is(section, article, aside, nav) :is(h1, h2, h3, h4, h5, h6) {
  margin-block-end: 0.5em;
}
```

Validation: `:is()` takes a selector list and selects elements matched by any selector in the list. MDN also documents its forgiving selector-list behavior. [MDN :is][ref-is]

## 10. Use `:where()` for low-specificity defaults

Use `:where()` when a default should be trivial to override.

```css
:where(a[href]:not([class])) {
  color: LinkText;
  text-decoration: underline;
}
```

Validation: `:where()` always has zero specificity, unlike `:is()`, whose specificity comes from the most specific selector in its arguments. [MDN :where][ref-where]

## 11. Use generated `content` only for non-critical presentation

Generated commas, visible URLs, and labels can be convenient, but they are not a replacement for semantic text in the DOM.

```css
ul.tags > li:not(:last-child)::after {
  content: ",";
}
```

Validation: the `content` property replaces or generates content; MDN documents `attr()` support and accessibility-related alternative text syntax. Treat generated content as presentational unless you have tested your assistive-technology target matrix. [MDN content][ref-content]

## 12. Use negative `:nth-child()` for first-N selection

```css
li:nth-child(-n + 3) {
  display: block;
}
```

Validation: `:nth-child()` matches elements by child index, and MDN documents the `An+B` syntax. [MDN :nth-child][ref-nth-child]

## 13. Use scoped `:nth-child(... of selector)` when sibling filtering matters

```css
li:nth-child(-n + 3 of .item) {
  display: block;
}
```

Validation: MDN documents the `of <complex-real-selector-list>` syntax, which counts only matching siblings for the formula. [MDN nth-child of selector][ref-nth-child-of]

## 14. Use SVG or masks for icons depending on recoloring needs

Use inline SVG or image SVGs for multicolor art. For monochrome, CSS-recolorable icons, use `mask` and paint with `currentColor`.

```css
.icon {
  inline-size: 1.5rem;
  block-size: 1.5rem;
  background-color: currentColor;
  mask: url("icon.svg") no-repeat center / contain;
}
```

Validation: CSS `mask` hides or clips parts of an element using a mask image; painting the masked element with `currentColor` lets the icon follow the text color. [MDN mask][ref-mask]

## 15. Scope flow spacing instead of using a global owl selector

The global `* + *` pattern is powerful but can leak into third-party widgets and internal component layouts. Scope it.

```css
.flow > * + * {
  margin-block-start: 1.5em;
}
```

Validation: adjacent sibling combinators are standard CSS selector behavior; logical `margin-block-start` follows the block axis for the writing mode. [MDN margin-inline/logical margin][ref-margin-inline], [MDN logical properties][ref-logical]

## 16. Use `max-height` disclosure only with caveats

A `max-height` transition works mechanically but animates toward an arbitrary ceiling, which can make timing feel wrong and can truncate content if the ceiling is too small.

```css
.disclosure {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.disclosure.is-open {
  max-height: 50rem;
}
```

Validation: `max-height` caps used height, and `overflow` controls clipping/scroll behavior when content does not fit. MDN warns to ensure `max-height` content is not truncated/obscured when users zoom text. [MDN max-height][ref-max-height], [MDN overflow][ref-overflow]

## 17. Prefer grid-row disclosure for unknown-height content

For modern layouts, animate grid rows instead of guessing a `max-height` ceiling.

```css
.disclosure {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s ease;
}

.disclosure.is-open {
  grid-template-rows: 1fr;
}

.disclosure > * {
  min-block-size: 0;
  overflow: hidden;
}
```

Validation: CSS Grid defines row/column tracks, and grid track sizes are animatable in modern engines; still test because animation edge cases depend on content, overflow, and layout. [MDN CSS grid][ref-grid], [MDN grid-template-columns][ref-grid-template-columns]

## 18. Use `table-layout: fixed` only when the table width is known

```css
table.report {
  inline-size: 100%;
  table-layout: fixed;
}
```

Validation: MDN says the fixed table-layout algorithm is faster because horizontal layout depends on table width, column widths, borders, and cell spacing, not cell contents; it also notes that if `width` is `auto` or unspecified, `fixed` has no effect. [MDN table-layout][ref-table-layout]

## 19. Use Grid `auto-fit` for responsive cards

Prefer auto-fitting Grid over `space-between` plus percentage flex basis for card galleries, because Grid keeps incomplete rows aligned.

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
  gap: 1.5rem;
}
```

Validation: `repeat()` supports `auto-fit`, `minmax()` defines a size range, and `gap` defines spacing between grid/flex tracks/items. [MDN repeat()][ref-repeat], [MDN minmax()][ref-minmax], [MDN gap][ref-gap]

## 20. Prefer `gap` over margin hacks in Flexbox/Grid

```css
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
```

Validation: `gap` applies to multi-column, flex, and grid layouts and avoids first/last-child margin cleanup. [MDN gap][ref-gap]

## 21. Use logical properties for internationalized layout

```css
.card {
  padding-block: 1rem;
  padding-inline: 1.25rem;
  margin-inline: auto;
}

.overlay {
  position: absolute;
  inset: 0;
}
```

Validation: logical properties map to physical properties depending on writing mode, direction, and text orientation. [MDN logical properties][ref-logical], [MDN margin-inline][ref-margin-inline], [MDN padding-block][ref-padding-block]

## 22. Use `:empty` narrowly

```css
.error-message:empty {
  display: none;
}
```

Validation: `:empty` matches elements with no children; text nodes, including whitespace, make an element non-empty. Scope it to known elements instead of using `:empty` globally. [MDN :empty][ref-empty]

## 23. Use `pointer-events: none` only for pointer hit-testing

```css
button:disabled {
  opacity: 0.5;
  pointer-events: none;
}
```

Validation: `pointer-events: none` affects pointer targeting; MDN notes elements with `pointer-events: none` can still receive focus through sequential keyboard navigation. Prefer the native `disabled` attribute where available. [MDN pointer-events][ref-pointer-events]

## 24. Hide autoplaying unmuted video only as a user stylesheet or controlled policy

```css
video[autoplay]:not([muted]) {
  display: none;
}
```

Validation: the selector is valid CSS because attribute selectors and `:not()` can combine; however, hiding media can affect content access. Use it as a user preference or product policy, not as an invisible surprise. [MDN :not][ref-not]

## 25. Use `@font-face local()` cautiously

```css
@font-face {
  font-family: "ExampleBrand";
  src: url("/fonts/example-brand.woff2") format("woff2");
  font-display: swap;
}
```

Avoid `local()` for strict brand fonts unless you have measured metrics and version risk. A user-installed font with the same name can be stale or metrically different. Use `local()` mainly for system font stacks or when accepting local substitution is intentional.

Validation: MDN documents `local()` in `@font-face src`, including local full font name/PostScript name lookup and notes that user agents may ignore user-installed fonts for security/privacy reasons. `font-display: swap` gives an extremely small block period and an infinite swap period. [MDN @font-face src][ref-font-src], [MDN font-display][ref-font-display]

## 26. Use fluid type with `clamp()` instead of unbounded viewport math

```css
h1 {
  font-size: clamp(1.75rem, 1rem + 3vw, 3rem);
}
```

Validation: `clamp(min, preferred, max)` clamps a value between lower and upper bounds; it is a better default than raw `calc(1vw + 1vh + ...)` because it includes floor and ceiling values. [MDN clamp()][ref-clamp]

## 27. Use `@supports` for layout-changing enhancements

```css
.card {
  position: relative;
}

@supports (anchor-name: --tip) {
  .trigger {
    anchor-name: --tip;
  }

  .tooltip {
    position-anchor: --tip;
    position-area: top;
  }
}
```

Validation: `@supports` tests whether a browser supports a CSS declaration before applying a block. [MDN @supports][ref-supports]

---

# Modern CSS support buckets

## Baseline Widely available / normal production CSS for current evergreen targets

Treat these as normal production CSS for current evergreen targets, while still testing your project’s real browser floor.

### `:has()`

Use `:has()` to style an element based on its descendants or following siblings.

```css
.card:has(> img) {
  grid-template-columns: 8rem 1fr;
}

.field:has(input:focus-visible) {
  outline: 2px solid currentColor;
}
```

Validation: MDN marks `:has()` Baseline Widely available and describes it as matching an element if any relative selector passed as an argument matches when anchored against that element. MDN also notes performance considerations for broad `:has()` usage, so keep selectors scoped. [MDN :has][ref-has]

### Container queries

Use container queries when a component should respond to its parent/container instead of the viewport.

```css
.wrapper {
  container-type: inline-size;
}

.card {
  grid-template-columns: 1fr;
}

@container (width > 400px) {
  .card {
    grid-template-columns: auto 1fr;
  }
}
```

Validation: MDN marks container queries Baseline Widely available and describes them as applying styles to descendants based on a container’s size or style. [MDN container queries][ref-container-queries], [MDN @container][ref-container-at]

### Native CSS nesting

Use native nesting for readability, but keep `&` explicit when joining selectors or pseudo-classes.

```css
.card {
  padding: 1rem;

  & .title {
    font-weight: 600;
  }

  &:hover {
    background: Canvas;
  }
}
```

Validation: MDN documents that CSS nesting is parsed by the browser, unlike Sass-style preprocessing. Nesting became Baseline Newly available in August 2023 and crossed the 30-month mark in February 2026, so it is now Baseline Widely available and needs no guard on evergreen targets. [MDN CSS nesting][ref-nesting], [Can I use CSS nesting][ref-caniuse-nesting], [web.dev Baseline][ref-webdev-baseline]

### Cascade layers with `@layer`

Use layers to define cascade order across reset/base/components/utilities.

```css
@layer reset, base, components, utilities;

@layer base {
  a { color: LinkText; }
}

@layer utilities {
  .text-red { color: red; }
}
```

Validation: MDN marks `@layer` Baseline Widely available and documents that later layers have higher precedence, allowing lower-specificity selectors in later layers to override higher-specificity selectors in earlier layers. [MDN @layer][ref-layer]

### Subgrid

Use `subgrid` when nested grid items need to align to parent grid tracks.

```css
.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
}
```

Validation: MDN marks subgrid Baseline Widely available and documents that subgrid lets a grid item use the parent grid’s tracks. [MDN subgrid][ref-subgrid]

### `color-mix()`

Use `color-mix()` for browser-computed tints, shades, and transparent variants. Prefer a perceptual color space such as `oklab`/`oklch` when design intent depends on perceived color.

```css
.btn {
  background: var(--brand);
}

.btn:hover {
  background: color-mix(in oklab, var(--brand) 85%, black);
}
```

Validation: MDN marks `color-mix()` Baseline Widely available and defines it as mixing two colors in a given color space by a specified amount. [MDN color-mix()][ref-color-mix]

### Logical properties

Use flow-relative properties instead of physical `left/right/top/bottom` where layout should adapt to writing mode.

```css
.box {
  margin-inline: auto;
  padding-block: 1rem;
}
```

Validation: MDN defines logical properties and values as mapping to physical equivalents based on writing mode, direction, and text orientation. [MDN logical properties][ref-logical]

### `clamp()`

Use `clamp()` for fluid sizes with hard limits.

```css
.section {
  padding-block: clamp(2rem, 5vw, 5rem);
}
```

Validation: MDN marks `clamp()` Baseline Widely available and describes its min/preferred/max behavior. [MDN clamp()][ref-clamp]

---

## Baseline Newly available / verify support floor

Treat these as production-ready only when your project’s supported browsers include the required versions.

### `text-wrap`

```css
h1,
h2,
.hero-title {
  text-wrap: balance;
}

.prose p {
  text-wrap: pretty;
}
```

Validation: MDN marks `text-wrap` Baseline 2024 Newly available. `balance` balances line lengths, while `pretty` aims for better typography such as avoiding orphans. MDN cautions that `balance` can be computationally expensive and is best for short blocks/headings. The shorthand status hides per-value differences: MDN flags that some parts of the feature have varying support, and `pretty` lands later and less evenly than `balance`, so treat `pretty` as an enhancement even where `balance` is safe. [MDN text-wrap][ref-text-wrap]

### `light-dark()`

```css
:root {
  color-scheme: light dark;
}

body {
  background: light-dark(#fff, #111);
  color: light-dark(#111, #eee);
}
```

Validation: MDN marks `light-dark()` Baseline 2024 Newly available, since May 2024. It returns one of two colors based on active color scheme, and it requires `color-scheme: light dark` or equivalent opt-in. It crosses the 30-month Widely available threshold around November 2026, so this entry moves buckets then. [MDN light-dark()][ref-light-dark], [web.dev Baseline][ref-webdev-baseline]

### `@scope`

```css
@scope (.card) to (.card__content) {
  img {
    border-radius: 8px;
  }
}
```

Validation: MDN marks `@scope` Baseline 2026 Newly available, since March 2026, and describes it as limiting selectors to specific DOM subtrees without requiring over-specific selectors. [MDN @scope][ref-scope]

### `@starting-style`

```css
.toast {
  transition: opacity 0.3s, translate 0.3s;
  opacity: 1;
  translate: 0 0;
}

@starting-style {
  .toast {
    opacity: 0;
    translate: 0 1rem;
  }
}
```

Validation: MDN marks `@starting-style` Baseline 2024 Newly available and defines it as starting values for elements before their first style update. [MDN @starting-style][ref-starting-style]

### Anchor positioning

```css
.trigger {
  anchor-name: --tip;
}

.tooltip {
  position: fixed;
  position-anchor: --tip;
  position-area: top;
  position-try-fallbacks: flip-block;
}
```

Validation: MDN marks `anchor-name`, `position-area`, and `position-try-fallbacks` Baseline 2026 Newly available, completed by Firefox 147 in January 2026. Newly available is not the same as bug-free here: web-features maintainers debated this feature's entry because of broken fixed-position anchors in Safari, `position-try` edge cases, and popover placement gaps. Use `@supports`, keep a non-anchored fallback, and test the real placements you ship. [MDN anchor positioning][ref-anchor-module], [MDN anchor-name][ref-anchor-name], [MDN position-area][ref-position-area], [MDN position-try-fallbacks][ref-position-try-fallbacks]

### `contrast-color()`

```css
.badge {
  background: var(--brand);
  color: white;
}

@supports (color: contrast-color(red)) {
  .badge {
    color: contrast-color(var(--brand));
  }
}
```

Validation: MDN marks `contrast-color()` Baseline 2026 Newly available. It returns black or white based on the input color, but MDN warns that mid-tone backgrounds can still fail readability/WCAG AA, so test real tokens. [MDN contrast-color()][ref-contrast-color]

### `field-sizing`

```css
textarea,
input {
  field-sizing: content;
}
```

Validation: MDN marks `field-sizing` Baseline 2026 Newly available, since June 2026, and defines it as enabling form controls to fit their content. Early Firefox builds implemented it partially and Firefox 152 beta notes describe filling in full support, so keep min/max sizes and a working fallback rather than assuming identical sizing behavior across the Baseline set. [MDN field-sizing][ref-field-sizing], [web.dev platform update, May 2026][ref-webdev-0526]

### Container style queries

```css
.theme-scope {
  container-name: --theme;
}

@container style(--theme: dark) {
  .card {
    background: #14181f;
    color: #e8ecf2;
  }
}
```

Validation: style queries against a custom property became Baseline Newly available in May 2026 when Firefox 151 completed the set. Only custom properties can be queried; `style()` cannot test arbitrary declared values. [MDN container queries][ref-container-queries], [MDN @container][ref-container-at], [web.dev platform update, May 2026][ref-webdev-0526]

### Name-only container queries

```css
#sidebar {
  container-name: --sidebar;
  container-type: inline-size;
}

/* Match the named container without also writing a size condition. */
@container --sidebar {
  .content {
    padding: 2rem;
  }
}
```

Validation: querying a container by name with no size or style condition became Baseline Newly available in May 2026 with Chrome 148. The rule applies whenever a matching named container exists in the ancestor chain. [MDN @container][ref-container-at], [web.dev platform update, May 2026][ref-webdev-0526]

### `:open`

```css
details:open > summary {
  font-weight: 600;
}

dialog:open {
  border-color: color-mix(in oklab, currentColor 30%, transparent);
}
```

Validation: `:open` became Baseline Newly available in May 2026 with Safari 26.5. It matches elements in an open state, including `details`, `dialog`, and `select` with an open picker, which makes the `[open]` attribute selector unnecessary for those cases. Attribute selectors still work as a fallback below your floor. [MDN :open][ref-open], [web.dev platform update, May 2026][ref-webdev-0526]

### `text-box-trim` and the `text-box` shorthand

```css
h1 {
  /* Trim the space above cap height and below the alphabetic baseline. */
  text-box: trim-both cap alphabetic;
}
```

Validation: MDN browser-compat-data records `text-box-edge` and `text-box-trim` in Chrome 133+, Safari 18.2+, and Firefox 154+. Leading trim removes the half-leading that makes headings look mis-centered inside their box. Browsers without support keep normal leading, so the fallback is the old spacing rather than a broken layout. Check your floor before relying on trimmed metrics for tight vertical rhythm. [MDN text-box][ref-text-box], [MDN text-box-trim][ref-text-box-trim], [MDN text-box-edge][ref-text-box-edge]

---

## Limited availability / progressive enhancement only

Ship a working default first. Add these behind `@supports` or feature detection.

### `accent-color`

```css
:root {
  accent-color: rebeccapurple;
}
```

Validation: MDN marks `accent-color` Limited availability. It sets the accent color for some user-interface controls, but browser/element behavior varies, so do not rely on it as the only way to convey state. [MDN accent-color][ref-accent-color]

### Scroll-driven animations

```css
.reveal {
  opacity: 1;
}

@supports (animation-timeline: view()) {
  .reveal {
    animation: fade-in linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 40%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .reveal {
    animation: none;
  }
}
```

Validation: MDN’s scroll-driven animation module documents scroll progress and view progress timelines; `animation-timeline` is marked Limited availability. Support is wider than it used to be: Safari 26 shipped scroll-driven animations, leaving Firefox as the remaining holdout, and the feature is an Interop 2026 focus area. It is still not Baseline, so provide static content by default and honor reduced motion. [MDN scroll-driven animations][ref-scroll-driven], [MDN animation-timeline][ref-animation-timeline], [WebKit scroll-driven animations][ref-webkit-sda], [Interop 2026 CSS focus areas][ref-interop-2026]

### `interpolate-size` and `calc-size()`

```css
@supports (interpolate-size: allow-keywords) {
  :root {
    interpolate-size: allow-keywords;
  }

  .details {
    transition: block-size 0.3s ease;
    block-size: 0;
    overflow: hidden;
  }

  .details.is-open {
    block-size: auto;
  }
}
```

Validation: MDN marks `interpolate-size` and `calc-size()` Limited availability/experimental. Chrome’s developer documentation describes Chrome 129 support and recommends progressive enhancement. Do not treat intrinsic-size interpolation as Baseline yet. [MDN interpolate-size][ref-interpolate-size], [MDN calc-size][ref-calc-size], [Chrome interpolate-size][ref-chrome-interpolate]

### `transition-behavior: allow-discrete`

```css
.dialog {
  transition:
    opacity 0.2s ease,
    display 0.2s allow-discrete;
  transition-behavior: allow-discrete;
}
```

Validation: MDN marks `transition-behavior` Baseline 2024 Newly available and defines `allow-discrete` as starting transitions for discrete animation-type properties. It is not a replacement for `interpolate-size` when the problem is animating to/from intrinsic sizes. [MDN transition-behavior][ref-transition-behavior]

### Typed `attr()`

```css
.columns {
  column-count: 2;
}

@supports (column-count: attr(data-cols type(<number>), 2)) {
  .columns {
    column-count: attr(data-cols type(<number>), 2);
  }
}
```

Validation: `attr()` outside the `content` property is not Baseline. The typed form reads an attribute as a real CSS type with a fallback value, and it currently ships in Chromium while remaining an Interop 2026 focus area. Declare the plain value first and gate the typed version. [MDN attr()][ref-attr], [Interop 2026 CSS focus areas][ref-interop-2026]

### Customizable `<select>`

```css
/* Native select stays intact for every browser that ignores these rules. */
select {
  font: inherit;
}

@supports (appearance: base-select) {
  select,
  ::picker(select) {
    appearance: base-select;
  }

  ::picker(select) {
    border: 1px solid CanvasText;
    border-radius: 0.5rem;
  }
}
```

Validation: `appearance: base-select` and the `::picker(select)` pseudo-element opt a select into a stylable rendering while keeping native semantics and keyboard behavior. It ships in Chromium from Chrome 135, with listbox support following in Chrome 145, and is not Baseline. Never rebuild a select out of divs to get the styling; gate the opt-in and let other browsers keep the platform control. [MDN appearance][ref-appearance], [MDN ::picker()][ref-picker]

### `shape()` for `clip-path`

```css
.blob {
  clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%);
}

@supports (clip-path: shape(from 0 0, line to 100% 0)) {
  .blob {
    clip-path: shape(
      from 0 0,
      line to 100% 0,
      curve to 100% 80% with 60% 40%,
      line to 0 100%,
      close
    );
  }
}
```

Validation: `shape()` describes a clip path with a path-like command list that accepts CSS units, `calc()`, and custom properties, which `path()` does not. It is an Interop 2026 focus area and is not Baseline, so keep a `polygon()` fallback. [MDN shape()][ref-shape], [Interop 2026 CSS focus areas][ref-interop-2026]

### `corner-shape`

```css
.card {
  border-radius: 1.5rem;
}

@supports (corner-shape: squircle) {
  .card {
    corner-shape: squircle;
  }
}
```

Validation: `corner-shape` changes how `border-radius` corners are drawn, including superellipse and squircle curves. It shipped in Chrome 139 and is not Baseline. Corners fall back to normal rounding, so this is a safe enhancement. [MDN corner-shape][ref-corner-shape]

### Media state pseudo-classes

```css
video:paused::after {
  content: "";
  position: absolute;
  inset: 0;
  background: rgb(0 0 0 / 0.35);
}

video:buffering {
  cursor: progress;
}
```

Validation: `:playing`, `:paused`, `:muted`, `:volume-locked`, `:buffering`, `:seeking`, and `:stalled` match media element state without a JavaScript event listener. They are an Interop 2026 focus area rather than Baseline, so drive any state your UI depends on from script and use these for polish. [MDN :playing][ref-playing], [MDN :buffering][ref-buffering], [Interop 2026 CSS focus areas][ref-interop-2026]

---


# More cool modern CSS tricks — validated additions

These additions are meant to sit beside the original patterns. The same rule applies: ship a boring, working fallback first, then enhance only where your browser floor supports the feature.

## 28. Animate real custom properties with `@property`

Unregistered custom properties animate as untyped token strings. Register a property when you want the browser to understand its type, interpolate it, validate it, and give it an initial value.

```css
@property --angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.spinner {
  inline-size: 3rem;
  aspect-ratio: 1;
  border-radius: 50%;
  background: conic-gradient(from var(--angle), currentColor 0 25%, transparent 0);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { --angle: 1turn; }
}
```

Validation: MDN marks `@property` as Baseline 2024 Newly available and describes it as a way to explicitly define CSS custom properties, including syntax, inheritance, and initial values. Use computationally independent `initial-value`s such as `0deg`, `10px`, or a named color. [MDN @property][ref-property]

## 29. Make component typography respond to the container with `cqi`

Viewport units make every copy of a component scale the same way. Container query units let each copy scale to its own container.

```css
.article-card-list {
  container-type: inline-size;
}

.article-card h2 {
  font-size: clamp(1.125rem, 0.85rem + 3cqi, 1.75rem);
}

.article-card {
  padding: clamp(1rem, 4cqi, 2rem);
}
```

Validation: MDN documents container query length units: `cqi` is 1% of the query container's inline size, `cqb` is 1% of its block size, and `cqmin`/`cqmax` use the smaller/larger of those axes. If no eligible query container exists, container query units fall back to the small viewport unit for that axis, so set the container deliberately. [MDN container query units][ref-container-query-units]

## 30. Validate forms after interaction with `:user-valid` and `:user-invalid`

Use the user-action pseudo-classes to avoid yelling at users before they have typed anything.

```css
.field {
  display: grid;
  gap: 0.35rem;
}

.field:has(input:user-invalid) {
  color: #b42318;
}

input:user-invalid {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}

input:user-valid {
  outline: 2px solid color-mix(in oklab, green 70%, currentColor);
  outline-offset: 2px;
}
```

Validation: MDN marks both `:user-valid` and `:user-invalid` as Baseline Widely available since November 2023. `:user-valid` matches a validated element only after user interaction, while `:user-invalid` represents validated form elements that fail their constraints after interaction. [MDN :user-valid][ref-user-valid], [MDN :user-invalid][ref-user-invalid]

## 31. Style popovers by open state instead of toggling classes

For HTML popovers, use `:popover-open` for the visible state and `::backdrop` for modal-style dimming when the element is placed in the top layer.

```css
[popover] {
  max-inline-size: min(32rem, calc(100vw - 2rem));
  padding: 1rem;
  border: 1px solid color-mix(in oklab, currentColor 25%, transparent);
  border-radius: 0.75rem;
  box-shadow: 0 1rem 3rem rgb(0 0 0 / 0.2);
}

[popover]:popover-open {
  display: grid;
  gap: 0.75rem;
}

[popover]::backdrop {
  background: rgb(0 0 0 / 0.35);
}
```

Validation: MDN marks `:popover-open` as Baseline 2024 Newly available and defines it as matching a popover element in the showing state. MDN marks `::backdrop` as Baseline Widely available, with some support caveats, and defines it as the box rendered beneath top-layer elements. [MDN :popover-open][ref-popover-open], [MDN ::backdrop][ref-backdrop]

## 32. Animate top-layer entrances carefully

Top-layer UI such as popovers and dialogs can combine `@starting-style`, discrete transitions, and `overlay` for smoother open/close behavior. Keep this behind feature checks because `overlay` is still limited.

```css
.toast[popover] {
  opacity: 0;
  translate: 0 0.75rem;
  transition:
    opacity 180ms ease,
    translate 180ms ease;
}

.toast[popover]:popover-open {
  opacity: 1;
  translate: 0 0;
}

@starting-style {
  .toast[popover]:popover-open {
    opacity: 0;
    translate: 0 0.75rem;
  }
}

@supports (transition-behavior: allow-discrete) and (overlay: auto) {
  .toast[popover] {
    transition:
      opacity 180ms ease,
      translate 180ms ease,
      overlay 180ms ease allow-discrete,
      display 180ms ease allow-discrete;
  }
}
```

Validation: `@starting-style` is already covered above as Baseline 2024 Newly available. MDN marks `overlay` as Limited availability and experimental; it is only relevant in `transition-property` when `transition-behavior: allow-discrete` is set. Keep the non-animated open/closed state correct without it. [MDN overlay][ref-overlay], [MDN transition-behavior][ref-transition-behavior], [MDN @starting-style][ref-starting-style]

## 33. Reserve scrollbar space with `scrollbar-gutter`

Prevent content from shifting sideways when a page or pane crosses the overflow threshold.

```css
html {
  scrollbar-gutter: stable;
}

.panel {
  max-block-size: 24rem;
  overflow: auto;
  scrollbar-gutter: stable both-edges;
}
```

Validation: MDN marks `scrollbar-gutter` as Baseline 2024 Newly available and describes it as reserving scrollbar space to prevent unwanted layout changes as content grows. [MDN scrollbar-gutter][ref-scrollbar-gutter]

## 34. Skip offscreen rendering with `content-visibility: auto`

For long feeds, documentation pages, and below-the-fold sections, let the browser skip layout/paint work until content becomes relevant.

```css
.feed-item {
  content-visibility: auto;
  contain-intrinsic-size: auto 320px;
}
```

Validation: MDN marks `content-visibility` as Baseline 2024 Newly available with some support caveats. The `auto` value turns on layout, style, and paint containment and can skip rendering when the element is not relevant to the user, while keeping skipped content available to find-in-page, tab order, focus, and selection. `contain-intrinsic-size` is Baseline Widely available and supplies the fallback size used for layout under size containment. [MDN content-visibility][ref-content-visibility], [MDN contain-intrinsic-size][ref-contain-intrinsic-size]

## 35. Fix sticky-header anchor jumps with `scroll-margin-top`

When fixed or sticky headers cover in-page anchors, give target sections a scroll margin instead of adding spacer elements.

```css
:root {
  --header-offset: 5rem;
}

[id] {
  scroll-margin-top: var(--header-offset);
}
```

Validation: MDN marks `scroll-margin-top` as Baseline Widely available since April 2021 and defines it as setting the top margin of the scroll snap area used for snapping the box into view. This also helps `#hash` navigation and `scrollIntoView()` land below a sticky header. [MDN scroll-margin-top][ref-scroll-margin-top]

## 36. Contain nested scroll chaining with `overscroll-behavior`

Use this on scrollable panes inside modals, drawers, and mobile sheets so reaching the pane boundary does not accidentally scroll the page behind it.

```css
.dialog__body {
  max-block-size: min(70dvb, 40rem);
  overflow: auto;
  overscroll-behavior: contain;
}
```

Validation: MDN marks `overscroll-behavior` as Limited availability and defines it as controlling what the browser does when reaching the boundary of a scrolling area. Treat it as progressive enhancement: the modal must still work if the rule is ignored. [MDN overscroll-behavior][ref-overscroll-behavior]

## 37. Use perceptual color tokens with `oklch()` and relative colors

`oklch()` makes token ramps easier to reason about because lightness, chroma, and hue are separate axes. Relative color syntax lets you derive variants from a base token.

```css
:root {
  --brand: oklch(62% 0.18 265);
  --brand-hover: oklch(from var(--brand) calc(l - 0.07) c h);
  --brand-soft: oklch(from var(--brand) 92% calc(c * 0.3) h);
}

.button {
  background: var(--brand);
}

.button:hover {
  background: var(--brand-hover);
}
```

Validation: the two halves of this pattern do not share a status. MDN marks `oklch()` Baseline Widely available and defines it as the cylindrical form of Oklab using lightness, chroma, and hue coordinates. Relative color syntax, the `from` keyword that derives one color from another, is the newer half and reached Baseline later, so it should be treated as the part that needs a floor check. Write literal fallback tokens first when your floor is unclear:

```css
:root {
  --brand: oklch(62% 0.18 265);
  --brand-hover: oklch(55% 0.18 265);
}

@supports (color: oklch(from red l c h)) {
  :root {
    --brand-hover: oklch(from var(--brand) calc(l - 0.07) c h);
  }
}
```

[MDN oklch()][ref-oklch], [MDN relative colors][ref-relative-colors]

## 38. Quarantine vendor CSS with `@import ... layer()`

Import third-party CSS into a known low-priority cascade layer so your components and utilities can override it without specificity wars.

```css
@layer reset, vendor, base, components, utilities;

@import url("vendor.css") layer(vendor);

@layer components {
  .button {
    border-radius: 0.5rem;
  }
}
```

Validation: MDN documents `@import url layer(layer-name)` and says `@import` must be defined before other style declarations, with `@charset` and layer-creating `@layer` statements as exceptions. MDN also documents importing external stylesheets into named cascade layers. [MDN @import][ref-import]

## 39. Use `:dir()` for direction-specific exceptions

Start with logical properties. Use `:dir()` only when the design itself changes for RTL/LTR, such as directional icons or asymmetric decoration.

```css
.breadcrumb__chevron {
  inline-size: 1em;
  block-size: 1em;
}

:dir(rtl) .breadcrumb__chevron {
  transform: scaleX(-1);
}
```

Validation: MDN marks `:dir()` as Baseline Widely available since December 2023 and defines it as matching elements based on text directionality. [MDN :dir()][ref-dir]

## 40. Avoid custom-element flash with `:defined`

When using web components, style the not-yet-upgraded state explicitly, then reveal the upgraded state.

```css
fancy-tabs:not(:defined) {
  display: block;
  min-block-size: 12rem;
  border-radius: 0.75rem;
  background: color-mix(in oklab, currentColor 8%, transparent);
}

fancy-tabs:defined {
  min-block-size: auto;
}
```

Validation: MDN marks `:defined` as Baseline Widely available and says it matches standard browser-defined elements and custom elements that have been successfully defined. [MDN :defined][ref-defined]

## 41. Expose web-component state with `:state()`

For autonomous custom elements, expose internal states through `CustomStateSet`, then style them from outside without leaking implementation classes.

```css
toggle-card {
  display: block;
  border: 1px solid currentColor;
  border-radius: 0.75rem;
}

toggle-card:state(open) {
  box-shadow: 0 0 0 3px color-mix(in oklab, currentColor 20%, transparent);
}

toggle-card::part(summary):state(open) {
  font-weight: 700;
}
```

Validation: MDN marks `:state()` as Baseline 2024 Newly available and defines it as matching custom elements that have the specified custom state. MDN also documents use with `:host()` and `::part()` for custom element internals and exposed shadow parts. [MDN :state()][ref-state]

## 42. Name shared elements for View Transitions

For same-document transitions, a stable `view-transition-name` lets an element animate separately from the default page cross-fade.

```css
@supports (view-transition-name: product-image) {
  .product-card__image {
    view-transition-name: product-image;
  }

  ::view-transition-old(product-image),
  ::view-transition-new(product-image) {
    animation-duration: 250ms;
  }
}

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 1ms;
  }
}
```

Two additions make larger transitions manageable. `view-transition-class` groups snapshots so one rule styles many named elements, and transition types let a single page describe different animations for different navigations.

```css
.product-card__image {
  view-transition-class: card-media;
}

/* One rule for every snapshot in the group. */
::view-transition-group(.card-media) {
  animation-timing-function: ease-out;
}

/* Only when the transition was started with the "forward" type. */
html:active-view-transition-type(forward) {
  &::view-transition-old(root) {
    animation-name: slide-out-left;
  }
}
```

Validation: MDN marks `view-transition-name` and `::view-transition-old()` as Baseline 2025 Newly available and says `view-transition-name` specifies the snapshot an element participates in so it can animate separately from the default cross-fade. Firefox 147 added same-document view-transition types in January 2026, and `view-transition-class` styles a group of snapshots at once. Cross-document `@view-transition` is still Limited availability, so keep that opt-in progressive. [MDN view-transition-name][ref-view-transition-name], [MDN ::view-transition-old()][ref-view-transition-old], [MDN view-transition-class][ref-view-transition-class], [MDN :active-view-transition-type()][ref-active-vt-type], [MDN @view-transition][ref-view-transition-at], [MDN prefers-reduced-motion][ref-reduced-motion], [web.dev platform update, January 2026][ref-webdev-0126]

## 43. Style search and editor ranges with `::highlight()`

Custom highlights let an app highlight arbitrary text ranges without wrapping the text in spans. CSS controls the presentation; JavaScript registers the ranges.

```css
::highlight(search-match) {
  background-color: yellow;
  color: black;
  text-decoration: underline;
}

::highlight(active-search-match) {
  background-color: orange;
  color: black;
}
```

Validation: MDN marks `::highlight()` as Baseline 2026 Newly available and defines it as styling a custom highlight registered with `HighlightRegistry`. MDN also limits supported properties to text-oriented properties such as `color`, `background-color`, text decoration, and `text-shadow`; `background-image` is ignored. [MDN ::highlight()][ref-highlight]

## 44. Adapt CSS to JavaScript availability with `@media (scripting)`

Use the `scripting` media feature for UI that is usable without JavaScript but enhanced when JavaScript is available.

```css
.carousel__controls {
  display: none;
}

@media (scripting: enabled) {
  .carousel__controls {
    display: flex;
  }
}

@media (scripting: none) {
  .carousel {
    overflow-x: auto;
  }
}
```

Validation: MDN marks the `scripting` media feature as Baseline 2023 Newly available and says it tests whether scripting, such as JavaScript, is available. [MDN scripting media feature][ref-scripting]

## 45. Use scroll-state container queries for scroll-aware UI

Scroll-state queries let CSS react to whether a container can scroll, was scrolled in a direction, is snapped, or is sticky-stuck.

```css
html {
  container-type: scroll-state;
  container-name: page-scroller;
}

.back-to-top {
  position: fixed;
  inset-block-end: 1rem;
  inset-inline-end: 1rem;
  translate: 120% 0;
  transition: translate 180ms ease;
}

@container page-scroller scroll-state(scrollable: top) {
  .back-to-top {
    translate: 0 0;
  }
}
```

Validation: MDN documents container scroll-state queries as a type of container query that applies styles based on scroll state, including `scrollable`, `scrolled`, `snapped`, and `stuck` descriptors. Because scroll-state queries are newer and interaction-heavy, keep a usable static fallback and test across your support matrix. [MDN scroll-state queries][ref-scroll-state-queries]

## 46. Snap fluid values to a rhythm with `round()`

When a fluid value produces awkward fractional spacing, round it to your spacing step.

```css
:root {
  --space-step: 0.25rem;
}

.card {
  padding: round(up, clamp(1rem, 3cqi, 2rem), var(--space-step));
}
```

Validation: MDN marks `round()` as Baseline 2024 Newly available and defines it as returning a rounded number based on a selected rounding strategy and interval. [MDN round()][ref-round]

## 47. Use `line-clamp` as an enhancement, not as content policy

Line clamping is useful for cards, previews, and teasers. Do not use it as the only way to access essential content.

```css
.excerpt {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

@supports (line-clamp: 3) {
  .excerpt {
    display: block;
    line-clamp: 3;
  }
}
```

Validation: MDN marks unprefixed `line-clamp` as Limited availability. MDN also documents the legacy `-webkit-line-clamp` co-dependency with `display: -webkit-box` or `-webkit-inline-box` and `-webkit-box-orient: vertical` as fully specified behavior that remains supported. [MDN line-clamp][ref-line-clamp]

## 48. Tune fallback font metrics with `size-adjust`

Instead of relying on a stale local brand font, tune a fallback face so its metrics better approximate your web font while the real font loads.

```css
@font-face {
  font-family: "Brand";
  src: url("/fonts/brand.woff2") format("woff2");
  font-display: swap;
}

@font-face {
  font-family: "Brand Fallback";
  src: local("Arial");
  size-adjust: 103%;
}

body {
  font-family: "Brand", "Brand Fallback", system-ui, sans-serif;
}
```

Validation: MDN marks `size-adjust` as Baseline Widely available since September 2023 and defines it as a multiplier for glyph outlines and font metrics to harmonize the rendered design of different fonts. More exact descriptors such as `ascent-override` remain Limited availability, so verify before relying on them. [MDN size-adjust][ref-size-adjust], [MDN ascent-override][ref-ascent-override]

## 49. Future/lab CSS to watch, not rely on yet

These are genuinely cool, but not baseline-safe. Keep them in experiments, demos, or progressive enhancements until your target browsers support them.

```css
/* Conditional single-value logic. Always write a fallback first. */
.card {
  padding: 1rem;
  padding: if(style(--density: compact): 0.5rem; else: 1rem);
}

/* Custom CSS functions: powerful, but experimental/limited. */
@function --alpha(--color <color>, --amount <number>) returns <color> {
  result: oklch(from var(--color) l c h / var(--amount));
}

/* Sibling math: useful for stagger/index effects, still limited. */
.gallery > * {
  --delay: calc(sibling-index() * 40ms);
  animation-delay: var(--delay);
}

/* Clip without creating a scroll container; extend the clip edge only where supported. */
.avatar {
  overflow: clip;
}

@supports (overflow-clip-margin: 1rem) {
  .avatar {
    overflow-clip-margin: 0.5rem;
  }
}
```

Also on the watchlist, shipping in one engine or newly landed as of August 2026:

- Interest invokers (`interesttarget`) for hover and focus triggered popovers, which remove a common JavaScript hover-card implementation.
- `::search-text` for styling find-in-page matches, and `caret-shape` for block or underscore carets, both from Chrome 144.
- Gap decorations (`column-rule` and `row-rule` on grid and flex containers) and `shape-outside` accepting `path()`, `rect()`, and `xywh()`, from Chrome 149.
- Multi-column `column-wrap` and `column-height` for wrapping column layouts.
- Standardized `zoom`, carried through Interop 2025 into 2026.

Validation: MDN marks `if()`, `@function`, `sibling-index()`, `sibling-count()`, and `overflow-clip-margin` as Limited availability. `overflow` itself is Baseline Widely available, but `overflow-clip-margin` is not; gate the extra clip-edge polish behind `@supports`. The items in the list above are single-engine or freshly shipped, so treat them the same way: build the working version first, then layer these on. [MDN if()][ref-if], [MDN @function][ref-function], [MDN sibling-index()][ref-sibling-index], [MDN sibling-count()][ref-sibling-count], [MDN overflow][ref-overflow], [MDN overflow-clip-margin][ref-overflow-clip-margin], [web.dev platform update, January 2026][ref-webdev-0126], [web.dev platform update, May 2026][ref-webdev-0526]


# Respect user preferences

Baseline tells you what a browser can parse. It says nothing about whether the result works for the person looking at it. These four media features are the highest-leverage accessibility defaults an agent can apply, and all of them are Baseline Widely available.

## 50. Treat reduced motion as the default for large movement

```css
.panel {
  transition: translate 0.25s ease, opacity 0.25s ease;
}

@media (prefers-reduced-motion: reduce) {
  .panel {
    transition-duration: 1ms;
  }

  *,
  ::before,
  ::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }
}
```

Reduce motion, do not delete feedback. A state change that only animation communicated needs another cue, such as an opacity change or a text label. Vestibular triggers are large translations, parallax, scale changes, and spin, not fades.

Validation: MDN documents `prefers-reduced-motion` as detecting a user request for reduced motion, and marks it Baseline Widely available. [MDN prefers-reduced-motion][ref-reduced-motion]

## 51. Adapt to `prefers-contrast` instead of hard-coding one contrast level

```css
.button {
  background: oklch(62% 0.18 265);
  color: white;
  border: 1px solid transparent;
}

@media (prefers-contrast: more) {
  .button {
    background: #10214a;
    border-color: currentColor;
  }
}

@media (prefers-contrast: less) {
  .button {
    background: oklch(72% 0.09 265);
  }
}
```

Validation: MDN documents `prefers-contrast` with `no-preference`, `more`, `less`, and `custom` values, and marks it Baseline Widely available. Meet WCAG contrast in the default rules; use `more` to strengthen borders and separators that were carrying meaning through subtle color alone. [MDN prefers-contrast][ref-prefers-contrast]

## 52. Survive forced colors with system color keywords

```css
.badge {
  background: var(--brand);
  color: white;
  border: 1px solid transparent;
}

@media (forced-colors: active) {
  .badge {
    background: Canvas;
    color: CanvasText;
    border-color: CanvasText;
    forced-color-adjust: none;
  }
}
```

In forced-colors mode the browser replaces your palette with the user's. Backgrounds on images, box-shadow outlines, and color-only state indicators disappear. Re-express those with borders, underlines, or text. Reach for `forced-color-adjust: none` only on an element whose colors you have deliberately rebuilt from system keywords.

Validation: MDN documents `forced-colors` as detecting an active forced color palette and lists the system color keywords (`Canvas`, `CanvasText`, `LinkText`, `ButtonFace`, `ButtonText`, `AccentColor`, `Highlight`) that map into it. Both are Baseline Widely available. [MDN forced-colors][ref-forced-colors], [MDN forced-color-adjust][ref-forced-color-adjust], [MDN system colors][ref-system-colors]

## 53. Drop decorative transparency when it is not wanted

```css
.overlay {
  background: rgb(20 24 31 / 0.72);
  backdrop-filter: blur(12px);
}

@media (prefers-reduced-transparency: reduce) {
  .overlay {
    background: rgb(20 24 31);
    backdrop-filter: none;
  }
}
```

Validation: MDN documents `prefers-reduced-transparency` as detecting a request to minimize transparent or translucent effects. Blur behind text is the usual offender, since it lowers effective contrast in a way a static contrast check will not catch. [MDN prefers-reduced-transparency][ref-reduced-transparency]


# Retire or modernize older tips

## Replace padding-hack ratio boxes with `aspect-ratio`

```css
.embed {
  aspect-ratio: 16 / 9;
}
```

Why: `aspect-ratio` directly expresses the intended ratio on the element. The old `height: 0; padding-bottom: ...` trick remains a legacy fallback only. [MDN aspect-ratio][ref-aspect-ratio]

## Replace max-height disclosure with grid-row disclosure where possible

Use the grid-row technique in Pattern 17 for unknown-height content. Reserve `max-height` for cases where the max is truly bounded and tested. [MDN max-height][ref-max-height], [MDN CSS grid][ref-grid]

## Replace `space-between` card gutters with Grid `auto-fit`

Use Pattern 19 for responsive cards. `justify-content: space-between` distributes leftover main-axis space; in wrapping galleries, this can make incomplete rows look detached. [MDN justify-content][ref-justify-content], [MDN repeat()][ref-repeat]

## Choose `unset` vs `revert` by reset intent

```css
button.clean {
  all: unset;
  display: inline-flex;
}

button.native {
  all: revert;
}
```

Why: `unset` means inherited properties inherit and non-inherited properties become initial; `revert` rolls back toward the previous cascade origin. [MDN all][ref-all]

## Do not `local()` strict brand fonts by default

Use self-hosted `.woff2`, font metrics strategy, and `font-display` instead. Use `local()` only when local substitution is acceptable. [MDN @font-face src][ref-font-src], [MDN font-display][ref-font-display]

## Scope the owl selector

```css
.flow > * + * {
  margin-block-start: 1.5em;
}
```

Why: the global version can affect widgets, grid/flex children, and embedded content. Scoping gives the spacing behavior only where intended. [MDN logical properties][ref-logical]

## Use masks for monochrome recolorable icons

Use `mask` plus `currentColor` for single-color icons. Keep inline SVG or image backgrounds for multicolor art. [MDN mask][ref-mask]

## Use `:where()` for defaults that should lose easily

```css
:where(a[href]:not([class])) {
  color: LinkText;
  text-decoration: underline;
}
```

Why: zero specificity makes component overrides straightforward. [MDN :where][ref-where]

---

# Tailwind v4 mapping

Tailwind v4 compiles to native CSS features rather than emulating them, so everything in this skill applies directly inside a Tailwind project. The mapping that matters:

| Tailwind v4 | Native CSS it emits or relies on | Notes |
|---|---|---|
| `@theme { --color-brand: oklch(62% 0.18 265); }` | Custom properties, `oklch()` | Theme variables are real custom properties, so relative color syntax and `color-mix()` work on them at runtime |
| `@import "tailwindcss"` | `@layer theme, base, components, utilities` | Tailwind's layers are native cascade layers, so `@layer` ordering rules from this skill apply |
| `@utility` and `@variant` | Plain selectors and at-rules | Custom utilities are ordinary CSS; write them with the patterns here |
| `@custom-variant dark (&:where(.dark, .dark *))` | `:where()` zero specificity | Keeps variants from winning specificity fights |
| Nested rules in `.css` files | Native CSS nesting | Parsed by the browser, Baseline Widely available since February 2026 |
| `@container` and `@container/name` variants | Container queries | Named containers, size queries, and style queries behave exactly as documented above |

Two rules for agents working in Tailwind:

1. Utilities do not change the compatibility question. A `field-sizing-content` or `text-balance` utility emits the same property with the same support story, so the `@supports` guidance in this skill still applies. Write the guard in a CSS file rather than trying to express it as a utility.
2. Prefer a theme variable over an arbitrary value when a value repeats. `bg-[oklch(62%_0.18_265)]` scattered across a codebase is the token problem this skill's `oklch()` pattern exists to avoid.

Validation: Tailwind v4's documentation describes the CSS-first configuration (`@theme`, `@utility`, `@variant`) and states that v4 is built on native cascade layers, registered custom properties, and `color-mix()`. [Tailwind theme variables][ref-tw-theme], [Tailwind functions and directives][ref-tw-directives]


# Validation matrix

| Claim / pattern | Status | Reference |
|---|---:|---|
| Baseline is compatibility signal, not QA | Validated | [MDN Baseline][ref-baseline] |
| `box-sizing: border-box` includes padding/border in sizing | Validated | [MDN box-sizing][ref-box-sizing] |
| `all` excludes `unicode-bidi`, `direction`, custom props | Validated | [MDN all][ref-all] |
| `:not()` matches elements not matching selector list | Validated | [MDN :not][ref-not] |
| `@font-face src local()` checks local names; privacy constraints exist | Validated | [MDN @font-face src][ref-font-src] |
| `font-display: swap` has tiny block period and infinite swap period | Validated | [MDN font-display][ref-font-display] |
| Unitless line-height is recommended for inheritance | Validated | [MDN line-height][ref-line-height] |
| `:focus-visible` is preferred for keyboard-visible focus styling | Validated | [MDN :focus-visible][ref-focus-visible] |
| Dynamic viewport units respond to browser UI changes | Validated | [MDN viewport units][ref-viewport-units] |
| `aspect-ratio` defines preferred width/height ratio | Validated | [MDN aspect-ratio][ref-aspect-ratio] |
| `object-fit: cover` preserves ratio while filling/clipping | Validated | [MDN object-fit][ref-object-fit] |
| Generated `content` is generated/replaced content | Validated | [MDN content][ref-content] |
| `:nth-child(-n + 3)` selects first three children | Validated | [MDN :nth-child][ref-nth-child] |
| `:nth-child(... of selector)` filters counted siblings | Validated | [MDN nth-child of selector][ref-nth-child-of] |
| `table-layout: fixed` requires table width to matter | Validated | [MDN table-layout][ref-table-layout] |
| `gap` works for grid/flex/multicol layouts | Validated | [MDN gap][ref-gap] |
| `:empty` ignores comments but not whitespace text nodes | Validated | [MDN :empty][ref-empty] |
| `pointer-events: none` does not prevent keyboard focus | Validated | [MDN pointer-events][ref-pointer-events] |
| `:has()` is Baseline Widely available | Validated | [MDN :has][ref-has] |
| Container queries are Baseline Widely available | Validated | [MDN container queries][ref-container-queries] |
| Native CSS nesting is browser parsed and Baseline Widely available since February 2026 (Newly available August 2023) | Updated | [MDN CSS nesting][ref-nesting], [web.dev Baseline][ref-webdev-baseline] |
| `@layer` layer order can outrank selector specificity | Validated | [MDN @layer][ref-layer] |
| `subgrid` is Baseline Widely available | Validated | [MDN subgrid][ref-subgrid] |
| `color-mix()` is Baseline Widely available | Validated | [MDN color-mix()][ref-color-mix] |
| Logical properties map to writing mode/direction | Validated | [MDN logical properties][ref-logical] |
| `clamp()` sets min/preferred/max | Validated | [MDN clamp()][ref-clamp] |
| `@supports` is feature-query CSS | Validated | [MDN @supports][ref-supports] |
| `text-wrap` is Baseline 2024 Newly available, with varying support per value | Updated | [MDN text-wrap][ref-text-wrap] |
| `light-dark()` is Baseline 2024 Newly available | Validated | [MDN light-dark()][ref-light-dark] |
| `@scope` is Baseline 2026 Newly available (since March 2026) | Corrected from 2025 | [MDN @scope][ref-scope] |
| `@starting-style` is Baseline 2024 Newly available | Validated | [MDN @starting-style][ref-starting-style] |
| Core anchor positioning properties are Baseline 2026 Newly available | Updated from uploaded skill | [MDN anchor-name][ref-anchor-name], [MDN position-area][ref-position-area], [MDN position-try-fallbacks][ref-position-try-fallbacks] |
| `contrast-color()` is Baseline 2026 Newly available and returns black/white | Validated | [MDN contrast-color()][ref-contrast-color] |
| `accent-color` is Limited availability | Validated | [MDN accent-color][ref-accent-color] |
| Scroll-driven `animation-timeline` is Limited availability; Safari 26 ships it and Firefox does not | Updated | [MDN animation-timeline][ref-animation-timeline], [WebKit scroll-driven animations][ref-webkit-sda] |
| `field-sizing` is Baseline 2026 Newly available | Updated from uploaded skill | [MDN field-sizing][ref-field-sizing] |
| Container style queries are Baseline Newly available since May 2026 and can only test custom properties | Added | [MDN container queries][ref-container-queries], [web.dev platform update, May 2026][ref-webdev-0526] |
| Name-only `@container` queries are Baseline Newly available since May 2026 | Added | [MDN @container][ref-container-at], [web.dev platform update, May 2026][ref-webdev-0526] |
| `:open` is Baseline Newly available since May 2026 | Added | [MDN :open][ref-open], [web.dev platform update, May 2026][ref-webdev-0526] |
| `text-box-trim` / `text-box-edge` ship in Chrome 133+, Safari 18.2+, Firefox 154+ | Added | [MDN text-box][ref-text-box], [MDN text-box-trim][ref-text-box-trim], [MDN text-box-edge][ref-text-box-edge] |
| Typed `attr()` is not Baseline, ships in Chromium, and is an Interop 2026 focus area | Added | [MDN attr()][ref-attr], [Interop 2026 CSS focus areas][ref-interop-2026] |
| `appearance: base-select` and `::picker(select)` are Chromium-only and not Baseline | Added | [MDN appearance][ref-appearance], [MDN ::picker()][ref-picker] |
| `shape()` for `clip-path` is not Baseline and is an Interop 2026 focus area | Added | [MDN shape()][ref-shape], [Interop 2026 CSS focus areas][ref-interop-2026] |
| `corner-shape` shipped in Chrome 139 and is not Baseline | Added | [MDN corner-shape][ref-corner-shape] |
| Media state pseudo-classes such as `:paused` and `:buffering` are not Baseline | Added | [MDN :playing][ref-playing], [MDN :buffering][ref-buffering] |
| `view-transition-class` groups snapshots; same-document view-transition types landed in Firefox 147 | Added | [MDN view-transition-class][ref-view-transition-class], [MDN :active-view-transition-type()][ref-active-vt-type], [web.dev platform update, January 2026][ref-webdev-0126] |
| `interpolate-size` / `calc-size()` are not Baseline | Validated | [MDN interpolate-size][ref-interpolate-size], [MDN calc-size][ref-calc-size] |
| `transition-behavior` is for discrete transitions | Validated | [MDN transition-behavior][ref-transition-behavior] |
| `mask` supports CSS masking for icons | Validated | [MDN mask][ref-mask] |
| `:where()` has zero specificity | Validated | [MDN :where][ref-where] |
| `@property` is Baseline 2024 Newly available and registers typed custom properties | Added | [MDN @property][ref-property] |
| Container query units such as `cqi`, `cqb`, `cqmin`, and `cqmax` are relative to a query container | Added | [MDN container query units][ref-container-query-units] |
| `:user-valid` / `:user-invalid` are Baseline Widely available and match after user interaction | Added | [MDN :user-valid][ref-user-valid], [MDN :user-invalid][ref-user-invalid] |
| `:popover-open` is Baseline 2024 Newly available; `::backdrop` is Baseline Widely available | Added | [MDN :popover-open][ref-popover-open], [MDN ::backdrop][ref-backdrop] |
| `overlay` is Limited availability and only relevant for top-layer discrete transitions | Added | [MDN overlay][ref-overlay] |
| `scrollbar-gutter` is Baseline 2024 Newly available | Added | [MDN scrollbar-gutter][ref-scrollbar-gutter] |
| `content-visibility` is Baseline 2024 Newly available; `contain-intrinsic-size` is Baseline Widely available | Added | [MDN content-visibility][ref-content-visibility], [MDN contain-intrinsic-size][ref-contain-intrinsic-size] |
| `scroll-margin-top` is Baseline Widely available | Added | [MDN scroll-margin-top][ref-scroll-margin-top] |
| `overscroll-behavior` is Limited availability | Added | [MDN overscroll-behavior][ref-overscroll-behavior] |
| `oklch()` is Baseline Widely available; relative color syntax is newer and carries its own status | Updated | [MDN oklch()][ref-oklch], [MDN relative colors][ref-relative-colors] |
| `@import ... layer()` imports styles into cascade layers and must appear before normal declarations | Added | [MDN @import][ref-import] |
| `:dir()` is Baseline Widely available | Added | [MDN :dir()][ref-dir] |
| `:defined` is Baseline Widely available | Added | [MDN :defined][ref-defined] |
| `:state()` is Baseline 2024 Newly available for custom element states | Added | [MDN :state()][ref-state] |
| `view-transition-name` and `::view-transition-old()` are Baseline 2025 Newly available; cross-document `@view-transition` is Limited availability | Added | [MDN view-transition-name][ref-view-transition-name], [MDN ::view-transition-old()][ref-view-transition-old], [MDN @view-transition][ref-view-transition-at] |
| `::highlight()` is Baseline 2026 Newly available and supports only a limited text-oriented property set | Added | [MDN ::highlight()][ref-highlight] |
| `scripting` media feature is Baseline 2023 Newly available | Added | [MDN scripting][ref-scripting] |
| `prefers-reduced-motion` is Baseline Widely available | Added | [MDN prefers-reduced-motion][ref-reduced-motion] |
| `prefers-contrast` is Baseline Widely available with `more`, `less`, and `custom` values | Added | [MDN prefers-contrast][ref-prefers-contrast] |
| `forced-colors` and system color keywords are Baseline Widely available | Added | [MDN forced-colors][ref-forced-colors], [MDN forced-color-adjust][ref-forced-color-adjust], [MDN system colors][ref-system-colors] |
| `prefers-reduced-transparency` detects a request to reduce translucent effects | Added | [MDN prefers-reduced-transparency][ref-reduced-transparency] |
| Container scroll-state queries are documented for `scrollable`, `scrolled`, `snapped`, and `stuck` states | Added | [MDN scroll-state queries][ref-scroll-state-queries] |
| `round()` is Baseline 2024 Newly available | Added | [MDN round()][ref-round] |
| `line-clamp` is Limited availability; legacy `-webkit-line-clamp` behavior is fully specified | Added | [MDN line-clamp][ref-line-clamp] |
| `size-adjust` is Baseline Widely available; `ascent-override` is Limited availability | Added | [MDN size-adjust][ref-size-adjust], [MDN ascent-override][ref-ascent-override] |
| `if()`, `@function`, `sibling-index()`, `sibling-count()`, and `overflow-clip-margin` are Limited availability | Added | [MDN if()][ref-if], [MDN @function][ref-function], [MDN sibling-index()][ref-sibling-index], [MDN sibling-count()][ref-sibling-count], [MDN overflow-clip-margin][ref-overflow-clip-margin] |

---

# Reference index

[ref-baseline]: https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility
[ref-tw-theme]: https://tailwindcss.com/docs/theme
[ref-tw-directives]: https://tailwindcss.com/docs/functions-and-directives
[ref-supports]: https://developer.mozilla.org/en-US/docs/Web/CSS/@supports
[ref-box-sizing]: https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing
[ref-all]: https://developer.mozilla.org/en-US/docs/Web/CSS/all
[ref-not]: https://developer.mozilla.org/en-US/docs/Web/CSS/:not
[ref-font-src]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/src
[ref-font-display]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display
[ref-line-height]: https://developer.mozilla.org/en-US/docs/Web/CSS/line-height
[ref-focus-visible]: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
[ref-viewport-units]: https://developer.mozilla.org/en-US/docs/Web/CSS/length#relative_length_units_based_on_viewport
[ref-place-items]: https://developer.mozilla.org/en-US/docs/Web/CSS/place-items
[ref-flex-align]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Aligning_items_in_a_flex_container
[ref-aspect-ratio]: https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio
[ref-object-fit]: https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit
[ref-content]: https://developer.mozilla.org/en-US/docs/Web/CSS/content
[ref-is]: https://developer.mozilla.org/en-US/docs/Web/CSS/:is
[ref-where]: https://developer.mozilla.org/en-US/docs/Web/CSS/:where
[ref-nth-child]: https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child
[ref-nth-child-of]: https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child#the_of_selector_syntax
[ref-mask]: https://developer.mozilla.org/en-US/docs/Web/CSS/mask
[ref-margin-inline]: https://developer.mozilla.org/en-US/docs/Web/CSS/margin-inline
[ref-padding-block]: https://developer.mozilla.org/en-US/docs/Web/CSS/padding-block
[ref-logical]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
[ref-max-height]: https://developer.mozilla.org/en-US/docs/Web/CSS/max-height
[ref-overflow]: https://developer.mozilla.org/en-US/docs/Web/CSS/overflow
[ref-grid]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
[ref-grid-template-columns]: https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-columns
[ref-table-layout]: https://developer.mozilla.org/en-US/docs/Web/CSS/table-layout
[ref-repeat]: https://developer.mozilla.org/en-US/docs/Web/CSS/repeat
[ref-minmax]: https://developer.mozilla.org/en-US/docs/Web/CSS/minmax
[ref-gap]: https://developer.mozilla.org/en-US/docs/Web/CSS/gap
[ref-empty]: https://developer.mozilla.org/en-US/docs/Web/CSS/:empty
[ref-pointer-events]: https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events
[ref-clamp]: https://developer.mozilla.org/en-US/docs/Web/CSS/clamp
[ref-has]: https://developer.mozilla.org/en-US/docs/Web/CSS/:has
[ref-container-queries]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
[ref-container-at]: https://developer.mozilla.org/en-US/docs/Web/CSS/@container
[ref-nesting]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting/Using_CSS_nesting
[ref-caniuse-nesting]: https://caniuse.com/css-nesting
[ref-layer]: https://developer.mozilla.org/en-US/docs/Web/CSS/@layer
[ref-subgrid]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid
[ref-color-mix]: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix
[ref-text-wrap]: https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
[ref-light-dark]: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark
[ref-scope]: https://developer.mozilla.org/en-US/docs/Web/CSS/@scope
[ref-starting-style]: https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style
[ref-anchor-module]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning
[ref-anchor-name]: https://developer.mozilla.org/en-US/docs/Web/CSS/anchor-name
[ref-position-area]: https://developer.mozilla.org/en-US/docs/Web/CSS/position-area
[ref-position-try-fallbacks]: https://developer.mozilla.org/en-US/docs/Web/CSS/position-try-fallbacks
[ref-contrast-color]: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/contrast-color
[ref-accent-color]: https://developer.mozilla.org/en-US/docs/Web/CSS/accent-color
[ref-scroll-driven]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations
[ref-animation-timeline]: https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline
[ref-field-sizing]: https://developer.mozilla.org/en-US/docs/Web/CSS/field-sizing
[ref-container-at]: https://developer.mozilla.org/en-US/docs/Web/CSS/@container
[ref-open]: https://developer.mozilla.org/en-US/docs/Web/CSS/:open
[ref-text-box]: https://developer.mozilla.org/en-US/docs/Web/CSS/text-box
[ref-text-box-trim]: https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-trim
[ref-text-box-edge]: https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-edge
[ref-attr]: https://developer.mozilla.org/en-US/docs/Web/CSS/attr
[ref-webdev-baseline]: https://web.dev/baseline
[ref-webkit-sda]: https://webkit.org/blog/17101/a-guide-to-scroll-driven-animations-with-just-css
[ref-appearance]: https://developer.mozilla.org/en-US/docs/Web/CSS/appearance
[ref-picker]: https://developer.mozilla.org/en-US/docs/Web/CSS/::picker
[ref-shape]: https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape/shape
[ref-corner-shape]: https://developer.mozilla.org/en-US/docs/Web/CSS/corner-shape
[ref-playing]: https://developer.mozilla.org/en-US/docs/Web/CSS/:playing
[ref-buffering]: https://developer.mozilla.org/en-US/docs/Web/CSS/:buffering
[ref-view-transition-class]: https://developer.mozilla.org/en-US/docs/Web/CSS/view-transition-class
[ref-active-vt-type]: https://developer.mozilla.org/en-US/docs/Web/CSS/:active-view-transition-type
[ref-webdev-0126]: https://web.dev/blog/web-platform-01-2026
[ref-webdev-0526]: https://web.dev/blog/web-platform-05-2026
[ref-interop-2026]: https://css-tricks.com/interop-2026
[ref-interpolate-size]: https://developer.mozilla.org/en-US/docs/Web/CSS/interpolate-size
[ref-calc-size]: https://developer.mozilla.org/en-US/docs/Web/CSS/calc-size
[ref-chrome-interpolate]: https://developer.chrome.com/docs/css-ui/animate-to-height-auto
[ref-transition-behavior]: https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior
[ref-justify-content]: https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content
[ref-property]: https://developer.mozilla.org/en-US/docs/Web/CSS/@property
[ref-container-query-units]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries#container_query_length_units
[ref-user-invalid]: https://developer.mozilla.org/en-US/docs/Web/CSS/:user-invalid
[ref-user-valid]: https://developer.mozilla.org/en-US/docs/Web/CSS/:user-valid
[ref-popover-open]: https://developer.mozilla.org/en-US/docs/Web/CSS/:popover-open
[ref-backdrop]: https://developer.mozilla.org/en-US/docs/Web/CSS/::backdrop
[ref-overlay]: https://developer.mozilla.org/en-US/docs/Web/CSS/overlay
[ref-scrollbar-gutter]: https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-gutter
[ref-content-visibility]: https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility
[ref-contain-intrinsic-size]: https://developer.mozilla.org/en-US/docs/Web/CSS/contain-intrinsic-size
[ref-line-clamp]: https://developer.mozilla.org/en-US/docs/Web/CSS/line-clamp
[ref-overflow-clip-margin]: https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-clip-margin
[ref-scroll-margin-top]: https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-margin-top
[ref-overscroll-behavior]: https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior
[ref-size-adjust]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust
[ref-ascent-override]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override
[ref-import]: https://developer.mozilla.org/en-US/docs/Web/CSS/@import
[ref-dir]: https://developer.mozilla.org/en-US/docs/Web/CSS/:dir
[ref-defined]: https://developer.mozilla.org/en-US/docs/Web/CSS/:defined
[ref-state]: https://developer.mozilla.org/en-US/docs/Web/CSS/:state
[ref-view-transition-name]: https://developer.mozilla.org/en-US/docs/Web/CSS/view-transition-name
[ref-view-transition-old]: https://developer.mozilla.org/en-US/docs/Web/CSS/::view-transition-old
[ref-view-transition-at]: https://developer.mozilla.org/en-US/docs/Web/CSS/@view-transition
[ref-oklch]: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch
[ref-relative-colors]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors
[ref-scripting]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/scripting
[ref-reduced-motion]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
[ref-prefers-contrast]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast
[ref-forced-colors]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors
[ref-forced-color-adjust]: https://developer.mozilla.org/en-US/docs/Web/CSS/forced-color-adjust
[ref-system-colors]: https://developer.mozilla.org/en-US/docs/Web/CSS/system-color
[ref-reduced-transparency]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency
[ref-round]: https://developer.mozilla.org/en-US/docs/Web/CSS/round
[ref-if]: https://developer.mozilla.org/en-US/docs/Web/CSS/if
[ref-function]: https://developer.mozilla.org/en-US/docs/Web/CSS/@function
[ref-sibling-index]: https://developer.mozilla.org/en-US/docs/Web/CSS/sibling-index
[ref-sibling-count]: https://developer.mozilla.org/en-US/docs/Web/CSS/sibling-count
[ref-highlight]: https://developer.mozilla.org/en-US/docs/Web/CSS/::highlight
[ref-scroll-state-queries]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_conditional_rules/Container_scroll-state_queries
