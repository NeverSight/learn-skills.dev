---
name: sileo-react-toasts
description: Provide implementation guidance for Sileo (npm package "sileo") toast notifications in React apps. Use when adding the Toaster viewport, firing global toasts via sileo.success/error/warning/info/show/action, handling async flows with sileo.promise, dismissing/clearing toasts, configuring positions/offset, theming with light/dark/system modes, and customizing styling via fill, styles overrides, autopilot, roundness, CSS variables, and data-attribute selectors. Also use this skill for swipe-to-dismiss behavior, custom icons, JSX descriptions, reduced-motion support, TypeScript type exports, and understanding Sileo's internal SVG gooey morphing architecture. Make sure to use this skill whenever the user mentions sileo, toast notifications in React, gooey toasts, physics-based notifications, or wants to add any kind of toast/notification system using sileo, even if they don't explicitly name the package.
keywords: [sileo, react, toast, toasts, notifications, toaster, ui, promise, action, styling, tailwind, css-variables, theme, dark-mode, swipe, gooey, spring-physics]
---
# SKILL: Sileo (React Toast Notifications)

> **Official documentation:** https://sileo.aaryan.design/docs
> **API Reference:** https://sileo.aaryan.design/docs/api
> **Toaster API:** https://sileo.aaryan.design/docs/api/toaster
> **Styling Guide:** https://sileo.aaryan.design/docs/styling
> **Playground:** https://sileo.aaryan.design/play
> **GitHub:** https://github.com/hiaaryan/sileo

---

## What is Sileo?

**Sileo** is a tiny, opinionated, **physics-based** toast component for React. It uses **gooey SVG morphing** (via an `feGaussianBlur` + `feColorMatrix` filter chain) and **spring animations** (powered by `motion/react`, formerly Framer Motion) to create buttery-smooth notifications that look beautiful by default with zero configuration.

Sileo is **not** a general-purpose notification center. It is a highly polished, visually distinctive toast system designed for single-line feedback messages with optional expandable descriptions.

**Key characteristics:**
- Framework: **React only** (ships with `"use client"` directive for Next.js App Router compatibility)
- Peer dependency: **`motion`** (spring physics engine, `motion/react`)
- Architecture: SVG-based rendering with gooey blob morphing between pill (collapsed) and card (expanded) states
- TypeScript-first: All types are exported (`SileoOptions`, `SileoPosition`, `SileoState`, `SileoStyles`, `SileoButton`)
- Accessibility: Uses `aria-live="polite"` on viewport sections, respects `prefers-reduced-motion`
- Swipe-to-dismiss: Built-in pointer-event-based vertical swipe gesture (30px threshold)

---

## Installation

```bash
npm install sileo
```

Sileo requires `react` and `motion` as peer dependencies.

---

## Quick Setup

1. Mount `<Toaster />` **once** at your app's root layout.
2. Fire toasts from anywhere by importing `sileo`.

```tsx
import { sileo, Toaster } from "sileo";

export default function App() {
  return (
    <>
      <Toaster position="top-right" />
      <YourApp />
    </>
  );
}
```

> Because `sileo` ships with `"use client"`, it works seamlessly in Next.js App Router without extra wrappers.

---

## Basic Usage

Sileo exposes a global controller `sileo` with state-specific shortcuts:

```tsx
import { sileo } from "sileo";

// State shortcuts (each returns the toast `id` as a string)
sileo.success({ title: "Saved", description: "Your changes were stored." });
sileo.error({ title: "Failed", description: "Could not save." });
sileo.warning({ title: "Warning", description: "Disk space low." });
sileo.info({ title: "Tip", description: "Try the new feature." });

// Generic toast (defaults to success, but accepts `type` for dynamic state)
sileo.show({ title: "Done", type: "success" });

// Dynamic state selection
sileo.show({
  type: response.ok ? "success" : "error",
  title: "Upload complete",
});
```

---

## All `sileo` Methods

| Method | Returns | Description |
| --- | --- | --- |
| `sileo.success(options)` | `string` (id) | Green success toast |
| `sileo.error(options)` | `string` (id) | Red error toast |
| `sileo.warning(options)` | `string` (id) | Amber warning toast |
| `sileo.info(options)` | `string` (id) | Blue info toast |
| `sileo.action(options)` | `string` (id) | Toast with an action button |
| `sileo.show(options)` | `string` (id) | Generic toast. Uses `options.type` for state, defaults to `"success"` |
| `sileo.promise(promise, opts)` | `Promise<T>` | Loading -> success/error flow. Returns the **original promise** |
| `sileo.dismiss(id)` | `void` | Dismiss a specific toast by id |
| `sileo.clear(position?)` | `void` | Clear all toasts, or only those at a specific position |

---

## `SileoOptions`

Passed to every `sileo.*()` call.

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `title` | `string` | -- | Toast heading (displayed in the pill) |
| `description` | `ReactNode \| string` | -- | Body content (shown when expanded). Accepts JSX for rich content |
| `type` | `SileoState` | -- | Dynamic state for `sileo.show()`. One of `"success" \| "loading" \| "error" \| "warning" \| "info" \| "action"` |
| `position` | `SileoPosition` | Toaster default | Override position for this individual toast |
| `duration` | `number \| null` | `6000` | Auto-dismiss in milliseconds. `null` = sticky (never auto-dismisses) |
| `icon` | `ReactNode \| null` | State icon | Custom icon replacing the default in the badge circle |
| `fill` | `string` | `"#FFFFFF"` | SVG fill color for the toast background shape |
| `styles` | `SileoStyles` | -- | CSS class overrides for sub-elements |
| `roundness` | `number` | `16` | Border radius in pixels for the SVG shapes |
| `autopilot` | `boolean \| { expand?: number; collapse?: number }` | `true` | Auto expand/collapse timing. `false` = hover only |
| `button` | `SileoButton` | -- | Action button configuration |

---

## Action Toast

Action toasts include a clickable button inside the expanded area:

```tsx
sileo.action({
  title: "New version available",
  description: "Reload to update",
  button: {
    title: "Reload",
    onClick: () => window.location.reload(),
  },
});
```

### `SileoButton`

```ts
interface SileoButton {
  title: string;
  onClick: () => void;
}
```

---

## Promise Toast

`sileo.promise` chains loading -> success/error states from a single promise. It returns the **original promise** so you can chain further.

- The first argument can be a `Promise<T>` **or a function** `() => Promise<T>` (useful for lazy execution).
- `success` and `error` can be static options or callbacks that receive the resolved/rejected value.
- The optional `action` field, when provided, replaces the success toast with an action-state toast.

```tsx
type User = { name: string };

const result = await sileo.promise<User>(createUser(data), {
  loading: { title: "Creating account..." },
  success: (user) => ({
    title: `Welcome, ${user.name}!`,
  }),
  error: (err: any) => ({
    title: "Signup failed",
    description: err?.message ?? "Unknown error",
  }),
});
// `result` is the resolved User object
```

**With lazy promise (function):**

```tsx
sileo.promise(() => fetch("/api/data").then((r) => r.json()), {
  loading: { title: "Fetching data..." },
  success: { title: "Data loaded" },
  error: { title: "Failed to load" },
});
```

**With action replacing success:**

```tsx
sileo.promise<{ url: string }>(uploadFile(file), {
  loading: { title: "Uploading..." },
  success: { title: "Uploaded" }, // Ignored when `action` is present
  error: { title: "Upload failed" },
  action: (data) => ({
    title: "File ready",
    description: "Click to open",
    button: {
      title: "Open",
      onClick: () => window.open(data.url),
    },
  }),
});
```

### `SileoPromiseOptions<T>`

```ts
interface SileoPromiseOptions<T = unknown> {
  loading: SileoOptions;
  success: SileoOptions | ((data: T) => SileoOptions);
  error: SileoOptions | ((err: unknown) => SileoOptions);
  action?: SileoOptions | ((data: T) => SileoOptions);
  position?: SileoPosition;
}
```

---

## Positions

Six positions available. Set a default on `<Toaster />`, or override per toast:

```ts
type SileoPosition =
  | "top-left"
  | "top-center"
  | "top-right"     // default
  | "bottom-left"
  | "bottom-center"
  | "bottom-right";
```

```tsx
<Toaster position="bottom-center" />

// Override for a specific toast
sileo.success({ title: "Saved", position: "top-left" });
```

The `SILEO_POSITIONS` constant array is also exported for iteration:

```ts
import { SILEO_POSITIONS } from "sileo"; // Not exported from index (internal)
```

---

# Toaster (Viewport Component)

`<Toaster />` is the viewport component that renders toasts. Add it **once** at your root layout.

```tsx
import { Toaster } from "sileo";
```

## Props

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `children` | `ReactNode` | -- | App content to render alongside toasts |
| `position` | `SileoPosition` | `"top-right"` | Default position for all toasts |
| `offset` | `number \| string \| { top?, right?, bottom?, left? }` | -- | Distance from viewport edges |
| `options` | `Partial<SileoOptions>` | -- | Default options merged into every toast |
| `theme` | `"light" \| "dark" \| "system"` | -- | Automatic fill based on color scheme. `"system"` follows OS preference |

## Theme

The `theme` prop automatically sets the toast `fill` color based on the selected scheme, saving you from manually configuring dark/light fills:

- `"light"` -> fill is `#1a1a1a` (dark toast on light backgrounds) + light description text
- `"dark"` -> fill is `#f2f2f2` (light toast on dark backgrounds) + dark description text
- `"system"` -> Follows `prefers-color-scheme` media query, reactively updates on OS change

```tsx
<Toaster position="top-right" theme="system" />
```

When `theme` is set, the viewport renders `data-theme="light"` or `data-theme="dark"` which CSS uses to auto-style description text opacity.

> If you set both `theme` and `fill` on individual toasts, the per-toast `fill` takes precedence.

## Offset

Accepts a number (px), a CSS string, or a per-side object:

```tsx
<Toaster offset={20} />
<Toaster offset="1.5rem" />
<Toaster offset={{ top: 20, right: 16 }} />
```

## Default Options (global)

```tsx
<Toaster
  options={{
    fill: "#171717",
    styles: { description: "text-white/75!" },
  }}
/>
```

Every toast will inherit these defaults. Per-toast options override them. The `styles` object is shallow-merged (per-toast styles overlay global styles).

---

# Styling

Sileo looks great out of the box. When customization is needed, there are several escape hatches.

## Fill Color

`fill` sets the SVG background color of the toast shape. Default: `"#FFFFFF"`.

For dark toasts, use a dark `fill` and pair it with light text via `styles`:

```tsx
sileo.success({
  title: "Dark toast",
  fill: "#171717",
  styles: {
    title: "text-white!",
    description: "text-white/75!",
  },
});
```

## Style Overrides (`styles`)

Override CSS classes on individual sub-elements. When using Tailwind, add `!` for specificity.

### `SileoStyles`

```ts
interface SileoStyles {
  title?: string;       // The heading text
  description?: string; // The body/description area
  badge?: string;       // The icon badge circle
  button?: string;      // The action button
}
```

### Available Data-Attribute Selectors

| Key | Element | CSS Selector |
| --- | --- | --- |
| `title` | Heading text | `[data-sileo-title]` |
| `description` | Body/description area | `[data-sileo-description]` |
| `badge` | Icon badge circle | `[data-sileo-badge]` |
| `button` | Action button | `[data-sileo-button]` |

Additional data-attributes available for CSS targeting:

| Selector | Description |
| --- | --- |
| `[data-sileo-toast]` | The outermost toast element (a `<button>`) |
| `[data-sileo-toast][data-state="success"]` | Toast filtered by state |
| `[data-sileo-toast][data-expanded="true"]` | Expanded toast |
| `[data-sileo-toast][data-exiting="true"]` | Toast in exit animation |
| `[data-sileo-viewport]` | The fixed viewport `<section>` |
| `[data-sileo-viewport][data-position="top-right"]` | Viewport filtered by position |
| `[data-sileo-viewport][data-theme="dark"]` | Viewport with theme applied |
| `[data-sileo-canvas]` | The SVG canvas wrapper |
| `[data-sileo-svg]` | The inner SVG element |
| `[data-sileo-pill]` | Animated collapsed pill rect |
| `[data-sileo-body]` | Animated expanded body rect |
| `[data-sileo-header]` | The header row container |
| `[data-sileo-content]` | The expandable content area |

### Example: Full dark theme with Tailwind

```tsx
sileo.success({
  title: "Custom styled",
  fill: "black",
  styles: {
    title: "text-white!",
    description: "text-white/75!",
    badge: "bg-white/20!",
    button: "bg-white/10!",
  },
});
```

## Custom Icons

Pass any React node as `icon` to replace the default state icon:

```tsx
sileo.info({
  title: "Custom icon",
  icon: <MyIcon />,
});
```

Pass `icon: null` to render no icon at all.

Default icons by state (Lucide-style SVG inlined):
- `success` -> checkmark
- `error` -> X
- `warning` -> circle with exclamation
- `info` -> life buoy
- `loading` -> spinning circle (CSS animation)
- `action` -> arrow right

## Custom Description (JSX)

`description` accepts JSX, enabling rich content inside the expanded area:

```tsx
sileo.info({
  title: "Rich content",
  description: (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      <span>Multiple elements supported</span>
      <img src="/preview.png" alt="Preview" width={120} />
    </div>
  ),
});
```

## Roundness

Control the border radius via `roundness` (default `16`):

```tsx
sileo.success({ title: "Sharp", roundness: 8 });   // Sharper corners
sileo.success({ title: "Pill", roundness: 24 });    // More pill-like
```

> **Performance:** Higher `roundness` increases the SVG blur radius for the gooey morph effect (`blur = roundness * 0.5`), which is more expensive to render. The recommended value is `16`.

## Autopilot

By default, toasts auto-expand after ~150ms and collapse ~4 seconds before dismissing. Control this behavior:

```tsx
// Disable entirely (hover to expand, click away to collapse)
sileo.info({ title: "Manual", autopilot: false });

// Custom timing (milliseconds)
sileo.info({
  title: "Custom timing",
  autopilot: { expand: 250, collapse: 300 },
});
```

Internal defaults (derived from `DEFAULT_TOAST_DURATION` of 6000ms):
- `AUTO_EXPAND_DELAY` = 150ms (6000 * 0.025)
- `AUTO_COLLAPSE_DELAY` = 4000ms (6000 - 2000)

When `autopilot` is `false` or `duration` is `null`/`0`, auto expand/collapse is disabled.

## Dismiss / Clear

```tsx
// Dismiss a specific toast
const id = sileo.success({ title: "Will dismiss" });
sileo.dismiss(id);

// Clear all toasts
sileo.clear();

// Clear only toasts at a specific position
sileo.clear("bottom-center");
```

Toasts can also be **swiped vertically** (30px threshold) to dismiss them. This is built-in pointer-event swipe gesture behavior.

## Sticky Toasts

Set `duration: null` to prevent auto-dismissal. The toast stays until dismissed programmatically or swiped:

```tsx
sileo.warning({
  title: "Requires attention",
  description: "This won't go away on its own.",
  duration: null,
});
```

---

## Global Defaults (Consistent Dark Theme)

```tsx
<Toaster
  position="top-right"
  options={{
    fill: "#171717",
    roundness: 16,
    styles: {
      title: "text-white!",
      description: "text-white/75!",
      badge: "bg-white/10!",
      button: "bg-white/10! hover:bg-white/15!",
    },
  }}
/>
```

---

## CSS Variables

Sileo exposes CSS custom properties for global overrides. Override them in `:root` or any parent element:

```css
:root {
  /* State colors (oklch format) */
  --sileo-state-success: oklch(0.723 0.219 142.136);
  --sileo-state-loading: oklch(0.556 0 0);
  --sileo-state-error: oklch(0.637 0.237 25.331);
  --sileo-state-warning: oklch(0.795 0.184 86.047);
  --sileo-state-info: oklch(0.685 0.169 237.323);
  --sileo-state-action: oklch(0.623 0.214 259.815);

  /* Dimensions */
  --sileo-width: 350px;
  --sileo-height: 40px;

  /* Animation */
  --sileo-duration: 600ms;
}
```

**Example: custom brand success color:**

```css
:root {
  --sileo-state-success: oklch(0.7 0.2 200);
}
```

### Internal CSS Variables (per-toast, set via inline styles)

These are computed per-toast and set as CSS custom properties on `[data-sileo-toast]`:

| Variable | Description |
| --- | --- |
| `--_h` | Current toast height (collapsed or expanded) |
| `--_pw` | Pill width |
| `--_px` | Pill X offset |
| `--_ht` | Header transform (translate + scale) |
| `--_co` | Content opacity (0 or 1) |

### Internal Color Variables (per-state, set via CSS)

| Variable | Description |
| --- | --- |
| `--sileo-tone` | The resolved state color for badge/title |
| `--sileo-tone-bg` | The state color at 20% opacity for badge background |
| `--sileo-btn-color` | Button text color (equals state color) |
| `--sileo-btn-bg` | Button background (state color at 15%) |
| `--sileo-btn-bg-hover` | Button hover background (state color at 25%) |

---

## TypeScript Exports

All types are exported from `"sileo"`:

```ts
import type {
  SileoButton,
  SileoOptions,
  SileoPosition,
  SileoState,
  SileoStyles,
} from "sileo";

// SileoState = "success" | "loading" | "error" | "warning" | "info" | "action"
```

The `SileoPromiseOptions<T>` type is also exported from the toast module.

---

## Accessibility

- The viewport uses `<section>` with `aria-live="polite"` so screen readers announce new toasts without interrupting the user.
- The toast root element is a `<button>` for keyboard focusability.
- Each SVG icon has a `<title>` element for screen reader labeling.
- Sileo respects `prefers-reduced-motion: reduce` by disabling all animations and transitions when the OS preference is set.

---

## Architecture (Internal Details)

Understanding Sileo's internals helps when debugging or deeply customizing:

1. **Global store:** A module-level singleton (`store`) holds all active toasts and notifies React via a listener `Set`. The `Toaster` component subscribes to this store and re-renders when toasts change.

2. **Toast IDs:** When no `id` is provided by the user, toasts use `"sileo-default"` as their id. This means calling `sileo.success(...)` repeatedly without an `id` will **replace** the previous toast (same-id update behavior). Provide a unique `id` for multiple simultaneous toasts of the same state.

3. **SVG Gooey Effect:** Each toast renders an `<svg>` with:
   - A `<filter>` containing `feGaussianBlur` (stdDeviation = `roundness * 0.5`) + `feColorMatrix` + `feComposite`
   - Two `<motion.rect>` elements (pill + body) animated via `motion/react` spring transitions
   - The gooey filter creates the organic blob-merging effect between pill and expanded card

4. **Spring Physics:** Animations use `motion/react`'s spring transition with `bounce: 0.25` and computed `duration` (default 0.6s). CSS transitions use a `linear()` easing approximation of the same spring curve.

5. **Expand Direction:** Toasts at `top-*` positions expand downward; toasts at `bottom-*` positions expand upward (via CSS `scaleY(-1)` transform on the canvas).

6. **Timer Management:** Each Toaster instance manages auto-dismiss timers per toast. Hovering over any toast pauses **all** timers; leaving resumes them. This hover-pause behavior is Toaster-level, not per-toast.

7. **Header Morphing:** When a toast's state changes (e.g., loading -> success via promise), the header performs a blur-based crossfade animation between the old and new state, using two stacked layers (`current` + `prev`).

---

## Integration Checklist

- [ ] Install `sileo` (and ensure `motion` peer dep is available)
- [ ] Mount **one** `<Toaster />` at the root layout
- [ ] Use `sileo.success/error/warning/info/show/action` based on context
- [ ] For async flows, prefer `sileo.promise(...)`
- [ ] For theming, either use `theme` prop or manual `fill` + `styles` + CSS variables
- [ ] For programmatic dismissal, use `dismiss(id)` or `clear(...)`
- [ ] Provide unique `id` values when multiple toasts should coexist simultaneously

---

## Common Patterns

### Form submission feedback

```tsx
const handleSubmit = async (data: FormData) => {
  await sileo.promise(saveForm(data), {
    loading: { title: "Saving..." },
    success: { title: "Form saved" },
    error: (err: any) => ({
      title: "Save failed",
      description: err?.message,
    }),
  });
};
```

### Undo action toast

```tsx
const id = sileo.action({
  title: "Item deleted",
  description: "This action can be undone",
  duration: 8000,
  button: {
    title: "Undo",
    onClick: () => {
      restoreItem(itemId);
      sileo.dismiss(id);
    },
  },
});
```

### Multiple simultaneous toasts

```tsx
// Use unique ids to prevent replacement
sileo.info({ title: "Downloading file 1...", id: "download-1", duration: null });
sileo.info({ title: "Downloading file 2...", id: "download-2", duration: null });

// Dismiss individually
sileo.dismiss("download-1");
sileo.dismiss("download-2");
```
