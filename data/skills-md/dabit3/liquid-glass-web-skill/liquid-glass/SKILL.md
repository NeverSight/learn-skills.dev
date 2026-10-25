---
name: liquid-glass
description: Build and migrate websites and web apps with the Liquid Glass design language using HTML, CSS, and JavaScript. Use when creating glass/translucent UI on the web, applying backdrop-filter glass surfaces, glass navbars, glass tab bars, glass dialogs and bottom sheets, morphing transitions with the View Transition API, SVG refraction filters, or any liquid-glass / glassmorphism UI work. Also use when the user asks about frosted glass effects, translucent navigation layers, backdrop-filter best practices, or bringing Apple-style Liquid Glass to the web.
license: MIT
---

# Liquid Glass Design System for the Web

Build and migrate websites and web apps using the Liquid Glass design language with plain HTML, CSS, and JavaScript. Works in all evergreen browsers (Chrome/Edge, Safari, Firefox) with progressive enhancement for advanced effects. No framework required; all patterns translate directly to React, Vue, Svelte, etc.

## Important: Use Latest Documentation

Always check current browser support before implementing Liquid Glass features. Support for the advanced pieces (SVG backdrop filters, scroll-driven animations) is still evolving. Key references:

- `https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter`
- `https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API`
- `https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency`
- `https://caniuse.com/css-backdrop-filter`

## Core Concept

Liquid Glass is a translucent, dynamic material exclusively for the **navigation layer** (headers, toolbars, tab bars, buttons, floating controls) that floats above page content. It samples and refracts the content behind it, responds to pointer movement with specular highlights, and adapts to whatever scrolls underneath.

**Never apply glass to content itself** (articles, cards grids, tables, media, text blocks). Glass is for controls and navigation only.

On the web the material is built from three layers:

1. **Backdrop sampling** - `backdrop-filter: blur() saturate()` filters whatever is painted behind the element
2. **Fill and rim** - a semi-transparent background, a 1px light border, and inset box-shadows for specular edge highlights
3. **Refraction and motion** (optional) - SVG displacement filters and pointer-tracking highlights, as progressive enhancement

## Quick Start: Key APIs

### 1. The Base Glass Material

Define tokens once, apply with a class. Capsule (pill) is the default shape:

```css
:root {
  --glass-blur: 12px;
  --glass-saturate: 180%;
  --glass-fill: rgb(255 255 255 / 10%);
  --glass-rim: rgb(255 255 255 / 25%);
  --glass-highlight: rgb(255 255 255 / 40%);
  --glass-shadow: rgb(0 0 0 / 15%);
  --glass-radius: 999px; /* capsule by default */
  --glass-tint: transparent;
}

.glass {
  background:
    linear-gradient(var(--glass-tint), var(--glass-tint)),
    var(--glass-fill);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  border: 1px solid var(--glass-rim);
  border-radius: var(--glass-radius);
  box-shadow:
    inset 0 1px 0 var(--glass-highlight),   /* top specular edge */
    inset 0 -1px 0 rgb(255 255 255 / 8%),   /* bottom rim */
    0 8px 24px var(--glass-shadow);         /* lift off the page */
}
```

```html
<span class="glass" style="padding: 8px 16px;">Label</span>
<button class="glass" style="--glass-radius: 16px;">Rounded</button>
<button class="glass" style="--glass-tint: rgb(0 122 255 / 25%);">Tinted</button>
```

### 2. Glass Variants

| Class | Use Case | Transparency |
|-------|----------|-------------|
| `.glass` (regular) | Standard UI: toolbars, buttons, nav bars | Medium |
| `.glass-clear` | Media-rich backgrounds where content is bold/bright | High |
| `.glass-identity` | Conditionally disable glass (accessibility, fallback) | None |

```css
.glass-clear { --glass-blur: 6px; --glass-fill: rgb(255 255 255 / 4%); --glass-rim: rgb(255 255 255 / 15%); }
.glass-identity { background: none; -webkit-backdrop-filter: none; backdrop-filter: none; border-color: transparent; box-shadow: none; }
```

### 3. Shared Glass Surfaces (Critical)

Every `backdrop-filter` element forces the browser to snapshot and filter its backdrop separately. Overlapping glass also double-filters. Nearby glass controls MUST share one surface: put the glass on a group container, keep children transparent.

```html
<!-- BAD: three separate backdrop snapshots, inconsistent sampling -->
<button class="glass">A</button> <button class="glass">B</button> <button class="glass">C</button>

<!-- GOOD: one shared glass surface -->
<div class="glass toolbar-group" role="group">
  <button>A</button> <button>B</button> <button>C</button>
</div>
```

```css
.toolbar-group { display: flex; gap: 4px; padding: 4px; }
.toolbar-group > button { background: none; border: none; border-radius: inherit; }
```

### 4. Morphing Transitions

Use the View Transition API (`view-transition-name` + `document.startViewTransition()`) for glass elements that expand, collapse, or merge:

```css
.badge-stack { view-transition-name: badge-stack; }
.badge-toggle { view-transition-name: badge-toggle; }
```

```js
function toggleExpanded() {
  const update = () => stack.classList.toggle('expanded');
  document.startViewTransition ? document.startViewTransition(update) : update();
}
```

### 5. Background Extension Effect

Let hero content extend behind the glass navigation layer - full-bleed content plus a fixed/sticky glass header with no opaque background:

```css
.site-header {
  position: fixed; inset-inline: 0; top: 0; z-index: 10;
  background: none; pointer-events: none;   /* the bar is invisible... */
}
.site-header :is(a, button, .toolbar-group) { pointer-events: auto; } /* ...only controls are glass */

.hero { height: 55svh; }
.hero img { width: 100%; height: 100%; object-fit: cover; } /* starts at y=0, under the header */
```

To extend content sideways behind a sidebar/inspector (mirror-and-blur), see [references/api-reference.md](references/api-reference.md#background-extension-effect).

### 6. Glass Buttons

```css
/* Standard glass button */
.btn-glass { padding: 10px 20px; font: inherit; color: inherit; cursor: pointer; }

/* Prominent glass button (primary actions) */
.btn-glass-prominent { --glass-tint: color-mix(in srgb, var(--accent, #0a84ff) 80%, transparent); color: white; }

/* Interactive: scale + bounce on press */
.glass-interactive { transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); }
.glass-interactive:active { transform: scale(0.96); }
```

```html
<button class="glass btn-glass glass-interactive">Action</button>
<button class="glass btn-glass btn-glass-prominent glass-interactive">Save</button>
```

### 7. Toolbars with Glass

The bar itself is transparent; controls float as glass pills and grouped capsules. Use flex spacers for layout:

```html
<header class="site-header">
  <nav class="toolbar">
    <a class="glass toolbar-item" href="/">Back</a>
    <div class="toolbar-spacer-flexible"></div>
    <button class="glass toolbar-item">Share</button>
    <div class="toolbar-spacer-fixed"></div>
    <div class="glass toolbar-group" role="group">
      <button aria-label="Favorite">♥</button>
      <button aria-label="Add">+</button>
    </div>
  </nav>
</header>
```

```css
.toolbar { display: flex; align-items: center; gap: 8px;
  padding: 8px max(12px, env(safe-area-inset-right)) 8px max(12px, env(safe-area-inset-left)); }
.toolbar-spacer-flexible { flex: 1; }
.toolbar-spacer-fixed { width: 16px; }
```

### 8. Tab Bars

Floating glass tab bar that minimizes on scroll down:

```css
.tab-bar {
  position: fixed; inset-inline: 0; bottom: max(12px, env(safe-area-inset-bottom));
  margin-inline: auto; width: fit-content;
  display: flex; gap: 4px; padding: 6px;
  transition: transform 0.35s ease, opacity 0.35s ease;
}
.tab-bar.minimized { transform: translateY(calc(100% + 24px)); }
```

```js
let lastY = 0;
addEventListener('scroll', () => {
  tabBar.classList.toggle('minimized', scrollY > lastY && scrollY > 120);
  lastY = scrollY;
}, { passive: true });
```

### 9. Sheets and Dialogs with Glass

Use the native `<dialog>` element; the sheet surface is glass, sampling the page through the top layer:

```html
<dialog class="glass sheet" id="infoSheet"> ... </dialog>
```

```css
.sheet {
  position: fixed; inset: auto 0 0 0; margin-inline: auto;
  width: min(640px, 100%); max-height: 50dvh;   /* "medium" detent */
  border: none; --glass-radius: 24px 24px 0 0; --glass-blur: 20px;
}
.sheet.large { max-height: 92dvh; }
.sheet::backdrop { background: rgb(0 0 0 / 15%); }
```

Do NOT give sheets an opaque background - the glass sampling is the point.

### 10. Liquid Refraction (Progressive Enhancement)

True light-bending uses an SVG displacement filter inside `backdrop-filter` - **Chromium-only** today. Always gate it and design so plain blur looks complete:

```html
<svg width="0" height="0" aria-hidden="true">
  <filter id="liquid-lens">
    <feTurbulence type="fractalNoise" baseFrequency="0.008 0.008" numOctaves="2" seed="7" result="noise"/>
    <feGaussianBlur in="noise" stdDeviation="2" result="soft"/>
    <feDisplacementMap in="SourceGraphic" in2="soft" scale="48" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>
```

```css
@supports (backdrop-filter: url(#liquid-lens)) {
  .glass-refract { backdrop-filter: url(#liquid-lens) blur(4px) saturate(var(--glass-saturate)); }
}
```

## Migration Workflow (Existing Sites)

For detailed migration steps, see [references/migration-guide.md](references/migration-guide.md).

**Summary:**
1. Establish glass design tokens and the base `.glass` class; nothing adopts automatically on the web
2. Remove conflicting styles: opaque header/nav backgrounds, heavy borders, old `filter: blur()` hacks
3. Make content full-bleed under the navigation layer so glass has something to sample
4. Convert floating controls, toolbars, tab bars, and sheets to glass surfaces
5. Group neighboring glass controls onto shared surfaces
6. Add morphing (View Transitions) and refraction (SVG filter) as progressive enhancement
7. Test accessibility (`prefers-reduced-transparency`, `prefers-contrast`, `prefers-reduced-motion`, `forced-colors`) and performance

## Browser Considerations

For browser- and device-specific details, see [references/platform-specifics.md](references/platform-specifics.md).

**Key differences:**
- **Baseline** `backdrop-filter`: Chrome 76+, Edge 79+, Firefox 103+, Safari 18+ unprefixed (9+ with `-webkit-` prefix - always ship both)
- **Chromium**: only engine that supports SVG `url(#filter)` inside `backdrop-filter` (real refraction)
- **Safari**: needs `-webkit-backdrop-filter` for older versions; known quirks with `border-radius` clipping and nested filters; iOS needs `viewport-fit=cover` + `env(safe-area-inset-*)`
- **Firefox**: solid blur/saturate support; no SVG backdrop filters; `prefers-reduced-transparency` and scroll-driven animations behind flags
- **Mobile**: reduce blur radius and glass area for performance; respect 44px minimum touch targets

## Common Pitfalls

For detailed pitfalls and solutions, see [references/pitfalls-and-solutions.md](references/pitfalls-and-solutions.md).

**Critical issues:**
- Glass over a plain background is invisible - there must be content behind it to sample
- An ancestor with `filter`, `opacity < 1`, `mask`, `clip-path`, `mix-blend-mode`, or another `backdrop-filter` becomes a **backdrop root** - descendants' glass stops sampling the page behind it
- `backdrop-filter` creates a stacking context and a containing block for `position: fixed` descendants
- Animating the blur radius is expensive - animate `transform`/`opacity` instead
- Too many separate glass elements cause scroll jank - share surfaces
- Text over glass needs contrast help: tint, gradient scrim, or `text-shadow`

## Real-World Example Patterns

For complete code patterns for a production-style web app (glass header, hero extension, badge stack with morphing, split view, inspector, editing mode), see [examples/web-app-patterns.md](examples/web-app-patterns.md).

## Architecture Best Practices

1. **Semantic landmarks** as the skeleton: `<header>`, `<nav>`, `<main>`, `<aside>`, `<dialog>` - glass lives on `header`/`nav`/`aside`/`dialog`, never `main`
2. **Design tokens first**: all glass parameters as custom properties on `:root`, adjusted per theme with `prefers-color-scheme`
3. **One glass surface per cluster** of controls; transparent children inside
4. **Progressive enhancement ladder**: solid fallback → translucent fill → blur + saturate → refraction filter
5. **`position: sticky/fixed` navigation** over full-bleed content, padded with `env(safe-area-inset-*)`
6. **View Transitions** for state morphing, with a plain-DOM fallback function
7. **Scroll-driven animations** (`animation-timeline: scroll()`) with `@supports` guard and JS scroll fallback
8. **`<dialog>` and Popover API** for sheets, menus, and inspectors - free focus management and top layer
9. **Feature-detect, don't browser-sniff** where possible: `@supports`, `CSS.supports()`, `'startViewTransition' in document`
10. **Test with DevTools emulation**: reduced transparency, reduced motion, forced colors, and CPU throttling for filter cost
