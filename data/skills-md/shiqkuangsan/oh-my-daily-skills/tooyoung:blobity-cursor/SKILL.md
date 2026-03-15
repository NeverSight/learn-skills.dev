---
name: tooyoung:blobity-cursor
description: "Add Blobity canvas cursor effect to any landing page. Supports HTML/React/Vue3/Vue2, light/dark theme, tooltip mode. Trigger words: blobity, cursor effect, landing page cursor, 光标特效"
metadata:
  version: "1.0.0"
---

# Blobity Cursor

Add a canvas-based custom cursor effect to landing pages. The cursor follows the mouse with spring physics, expands to wrap interactive elements, and inverts colors via `mix-blend-mode: difference`.

**Core mechanism**: Blobity creates a `<canvas>` overlay (`position: fixed`, `pointer-events: none`, `z-index: max`) and draws a blob that follows the cursor using the Kinet spring physics engine. With `invert: true`, the canvas uses `mix-blend-mode: difference` to create a color-inversion effect.

## Quick Start (HTML)

Minimal working example — copy into any HTML page:

```html
<!-- Hide default cursor -->
<style>
  body.blobity-active,
  body.blobity-active a,
  body.blobity-active button,
  body.blobity-active [data-blobity],
  body.blobity-active [data-blobity-tooltip] {
    cursor: none !important;
  }
</style>

<!-- Load Blobity via ESM CDN (npm: import Blobity from 'blobity') -->
<script type="module">
  import Blobity from "https://esm.sh/blobity@0.2.3";

  // Skip touch devices
  if ("ontouchstart" in window || navigator.maxTouchPoints > 0) {
    throw new Error("Touch device — skip Blobity");
  }

  const blobity = new Blobity({
    licenseKey: "opensource",
    invert: true,
    zIndex: 50,
    color: "#ffffff", // Canvas fill → difference with dark bg = light
    dotColor: "#10b981", // Resting cursor dot color
    radius: 6,
    magnetic: false,
    mode: "normal",
    focusableElements: "a, button, [data-blobity], [data-blobity-tooltip]",
    focusableElementsOffsetX: 5,
    focusableElementsOffsetY: 4,
    font: "'JetBrains Mono', monospace",
    fontSize: 16,
    fontWeight: 600,
    fontColor: "#0d1117", // Tooltip text color on canvas
    tooltipPadding: 12,
  });

  document.body.classList.add("blobity-active");
</script>
```

Add `data-blobity-tooltip="Label text"` to any element for tooltip mode:

```html
<div class="card" data-blobity-tooltip="View details">...</div>
```

## Installation

**CDN** (no build tool):

```html
<script type="module">
  import Blobity from "https://esm.sh/blobity@0.2.3";
</script>
```

> Other CDNs (`cdn.jsdelivr.net`, `cdn.blobity.dev`) have known 404/connection issues. Use `esm.sh`.

**npm** (with bundler):

```bash
# pnpm (recommended)
pnpm add blobity

# npm
npm install blobity

# yarn
yarn add blobity
```

```js
import Blobity from "blobity";
```

> Blobity has `react` and `vue` as optional peer dependencies. Ignore the warning if you're not using their bindings.

## Theme Adaptation (Light/Dark)

The `mix-blend-mode: difference` formula is `|page_pixel - canvas_pixel|`. This means:

- **Dark page + white canvas** → light result (standard inversion) ✓
- **Light page + dark canvas** → light result (soft tint) ✓
- **Light page + white canvas** → black result (harsh) ✗

Key rule: **dark bg uses white `color`, light bg uses a dark `color` calculated from your target tint**.

### Recommended Color Scheme

| Option      | Dark Mode | Light Mode | Notes                                                                         |
| ----------- | --------- | ---------- | ----------------------------------------------------------------------------- |
| `color`     | `#ffffff` | `#190a11`  | Light mode produces soft mint `#e6f5ee` on white                              |
| `dotColor`  | `#10b981` | `#111827`  | Accent green / dark gray                                                      |
| `fontColor` | `#0d1117` | `#000000`  | Tooltip text: dark→black on light bg, light→white on dark bg after difference |

### Theme Switching Pattern

Watch for theme attribute changes and update Blobity options dynamically:

```js
const isDark = () =>
  document.documentElement.getAttribute("data-theme") !== "light";
// Alternative checks:
//   document.documentElement.classList.contains('dark')
//   window.matchMedia('(prefers-color-scheme: dark)').matches

const observer = new MutationObserver(() => {
  blobity.updateOptions({
    color: isDark() ? "#ffffff" : "#190a11",
    dotColor: isDark() ? "#10b981" : "#111827",
    fontColor: isDark() ? "#0d1117" : "#000000",
  });
});

observer.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ["data-theme", "class"],
});
```

> To calculate custom light-mode colors, see `references/color-math.md`.

## Configuration Options

| Option                     | Type    | Default       | Description                                        |
| -------------------------- | ------- | ------------- | -------------------------------------------------- |
| `licenseKey`               | string  | —             | Use `'opensource'` for open-source projects        |
| `invert`                   | boolean | `false`       | Enable `mix-blend-mode: difference` on canvas      |
| `color`                    | string  | `'#000000'`   | Canvas fill color when hovering focusable elements |
| `dotColor`                 | string  | `'#000000'`   | Resting cursor dot color                           |
| `radius`                   | number  | `4`           | Dot radius in pixels                               |
| `magnetic`                 | boolean | `true`        | Whether cursor snaps to element center on hover    |
| `mode`                     | string  | `'normal'`    | Cursor mode                                        |
| `zIndex`                   | number  | `-1`          | Canvas z-index                                     |
| `focusableElements`        | string  | `'a, button'` | CSS selector for interactive elements              |
| `focusableElementsOffsetX` | number  | `0`           | Horizontal padding when wrapping elements          |
| `focusableElementsOffsetY` | number  | `0`           | Vertical padding when wrapping elements            |
| `font`                     | string  | —             | Tooltip font family                                |
| `fontSize`                 | number  | `16`          | Tooltip font size                                  |
| `fontWeight`               | number  | `400`         | Tooltip font weight                                |
| `fontColor`                | string  | `'#000000'`   | Tooltip text color on canvas                       |
| `tooltipPadding`           | number  | `4`           | Tooltip inner padding                              |

## Tooltip Mode

Add `data-blobity-tooltip` to elements — cursor morphs into a text label instead of expanding:

```html
<div class="step-card" data-blobity-tooltip="Step 1: Upload">...</div>
<a href="/docs" data-blobity-tooltip="Documentation">Docs</a>
```

Tooltip elements should be included in `focusableElements` via `[data-blobity-tooltip]` selector.

**Light mode tooltip text visibility**: tooltip background gets darkened by difference blend, so `fontColor` must also produce a light result after blending. Use `#000000` for light mode (becomes white after `|#fff - #000| = #fff`).

## Common Pitfalls

### 1. CDN 404 Errors

```
✗ cdn.jsdelivr.net/npm/blobity@latest/lib/blobity.min.js  → wrong path
✗ cdn.blobity.dev/by.js                                    → server down
✗ cdn.jsdelivr.net/npm/blobity@0.2.4                       → version doesn't exist
✓ esm.sh/blobity@0.2.3                                     → works
```

### 2. Cursor Invisible or Pure Black on Light Background

This is a `mix-blend-mode: difference` color math issue. See the Theme Adaptation section — use a dark `color` value for light backgrounds (NOT white).

### 3. Touch Device Detection

Always skip Blobity on touch devices — there's no mouse cursor to replace:

```js
const isTouchDevice = "ontouchstart" in window || navigator.maxTouchPoints > 0;
if (isTouchDevice) return;
```

### 4. SPA Page Navigation Cleanup

Blobity must be destroyed on route change to avoid canvas leaks:

```js
// Astro view transitions
document.addEventListener(
  "astro:before-swap",
  () => {
    observer.disconnect();
    document.body.classList.remove("blobity-active");
    blobity.destroy();
  },
  { once: true },
);

// React Router / Vue Router
onUnmounted(() => {
  blobity.destroy();
});
// Or useEffect cleanup in React
```

### 5. Peer Dependency Warnings

Blobity declares `react` and `vue` as peer deps. Safe to ignore if not using their framework bindings:

```bash
# pnpm
pnpm add blobity --no-strict-peer-dependencies

# npm (if needed)
npm install blobity --legacy-peer-deps
```

### 6. z-index Conflicts

Set `zIndex` high enough to overlay page content but below modals/dialogs. `50` works for most cases. If your site has a sticky header at `z-index: 100+`, either raise Blobity's value or accept the cursor rendering behind the header.

## Scroll Bounce

Add a playful bounce effect when user scrolls:

```js
let scrollTimeout = null;
window.addEventListener(
  "scroll",
  () => {
    if (scrollTimeout) return;
    scrollTimeout = setTimeout(() => {
      blobity.bounce();
      scrollTimeout = null;
    }, 150);
  },
  { passive: true },
);
```

## References

| File                       | Content                                                                       |
| -------------------------- | ----------------------------------------------------------------------------- |
| `references/frameworks.md` | React hook, Vue 3 composable, Vue 2 mixin — complete templates                |
| `references/color-math.md` | `mix-blend-mode: difference` color calculation, lookup table, reverse formula |
