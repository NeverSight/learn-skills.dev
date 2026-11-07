---
name: budge
description: Use when making single-property CSS or Tailwind visual changes in Next.js App Router projects. Presents a floating control widget on the page so the user can tweak the value before it is persisted. Covers atomic style changes, live preview, and cleanup. Triggers on single CSS value or single Tailwind utility class modifications.
---

# Budge

**Proactive skill. Next.js App Router only.** If a task results in a single CSS property or Tailwind class change, follow this skill automatically. The user should never need to say "use budge."

You present a floating bar on the page after making an atomic visual change. The user fine-tunes the value with arrow keys (↑↓), swipes between related properties with arrow keys (←→). **With the current runtime, complete your turn immediately after making the visual change — no browser interaction, no waiting, and no manual config unless the fallback below is needed.**

The runtime is a self-contained IIFE loaded from `https://www.budge.design/budge.iife.js` via `next/script`. On local/dev hosts it stays on the page, watches HMR-driven `class`/`style` DOM changes, infers the latest numeric visual property change, marks the changed element, and mounts Budge automatically. It also uses React Grab primitives for manual selection: press `Cmd+E`, select an element, and Budge opens. It still supports the explicit `data-budge` config element as a fallback. Everything is handled client-side: live preview on `[data-budge-target]` elements, arrow key stepping, slide navigation, audio feedback, submit (Enter — copies an edit prompt to clipboard), and cancel (Escape — reverts).

**In scope:** Raw CSS property values, inline styles, Tailwind utility class changes, SVG presentation attributes (`fill`, `stroke`, etc.).
**Out of scope:** Sass/Less variables, CSS custom property definitions (`--spacing`), CSS-in-JS theme tokens. Proceed normally for these.

## Installation

Grep for `budge.iife.js` in `app/layout.tsx`. If found, make the requested visual change and stop. Otherwise, read `references/INSTALL.md` and follow its instructions.

## Default Flow

For a single raw CSS value or Tailwind class token change, just make the source edit. The always-on runtime should attach Budge to the resulting DOM change after HMR. Tell the user: "I've changed X to Y. Use ↑↓ to fine-tune, ←→ to switch properties."

Use the manual steps below only if the bar does not appear or the change cannot be inferred from one numeric `class`/`style` DOM mutation.

---

## Troubleshooting — bar does not appear

1. **Script missing:** Confirm `<Script src="https://www.budge.design/budge.iife.js" strategy="afterInteractive" />` is in `app/layout.tsx`.
2. **Auto-detect disabled:** Auto-detect runs by default on local/dev hosts. Force it with `data-budge-autodetect="true"` on the script tag, or disable it with `"false"`.
3. **No inferable DOM change:** The fallback bar only appears when a `<div data-budge="..." hidden />` element with a non-empty `slides` array is in the DOM.
4. **Target not found:** The element with `data-budge-target` must be in the DOM after hydration.

---

## Manual Fallback — Trigger Test

After making a change, apply this mechanical test. Do NOT use subjective judgment.

> **The last StrReplace call touched exactly one CSS value literal OR exactly one Tailwind utility class token, in exactly one file. The change is not a variable, mixin, or theme token.**

**Pass:** `padding: 8px` → `padding: 16px` | `className="p-2 m-4"` → `className="p-4 m-4"`
**Fail:** two values changed, token added/removed, Sass variable, multiple StrReplace calls, structural change.

Fail → skip budge, proceed normally. Pass → continue to Step 2. The mechanical test is the only gate.

## Step 2 — Build Slides

Build a `slides` array. The **first slide** is the property you changed. Additional slides are related properties the user might want to tweak.

Each slide has this shape:

```ts
{
  label: string;      // display name shown above bar
  property: string;   // CSS property to apply to [data-budge-target]
  min: number;        // minimum numeric value
  max: number;        // maximum numeric value
  value: number;      // current value (the one you set)
  original: number;   // value before your change
  unit: string;       // "px", "%", "em", etc.
  type?: "color";     // only set for color properties
}
```

### Slide generation rules

1. **Primary slide** (index 0): the property you changed. `value` = new value, `original` = old value.
2. **Related slides** (index 1+): pick 2–3 related properties from the same element. Read their current computed/declared values. Use sensible min/max ranges.

**Example — agent changed `padding-top: 8px` → `padding-top: 16px`:**

```ts
[
  { label: "padding-top", property: "padding-top", min: 0, max: 64, value: 16, original: 8, unit: "px" },
  { label: "padding-bottom", property: "padding-bottom", min: 0, max: 64, value: 8, original: 8, unit: "px" },
  { label: "padding-left", property: "padding-left", min: 0, max: 64, value: 12, original: 12, unit: "px" },
  { label: "padding-right", property: "padding-right", min: 0, max: 64, value: 12, original: 12, unit: "px" },
]
```

**Example — agent changed `font-size: 14px` → `font-size: 16px`:**

```ts
[
  { label: "font-size", property: "font-size", min: 8, max: 72, value: 16, original: 14, unit: "px" },
  { label: "line-height", property: "line-height", min: 12, max: 80, value: 24, original: 22, unit: "px" },
  { label: "letter-spacing", property: "letter-spacing", min: -2, max: 10, value: 0, original: 0, unit: "px" },
]
```

**Example — agent changed `color: #333` → `color: #1a1a1a`:**

Use the `type: "color"` slide with hue degrees:

```ts
[
  { label: "color", property: "color", min: 0, max: 360, value: 0, original: 0, unit: "°", type: "color" },
]
```

### Related property suggestions

| Changed property | Related slides |
|---|---|
| `padding-top` | `padding-bottom`, `padding-left`, `padding-right` |
| `padding` | `padding-top`, `padding-bottom` |
| `margin-top` | `margin-bottom`, `margin-left`, `margin-right` |
| `font-size` | `line-height`, `letter-spacing` |
| `gap` | `padding`, `margin-top` |
| `width` | `height`, `max-width` |
| `border-radius` | `padding`, `border-width` |
| `opacity` | `font-size` |

### Tailwind resolution

Resolve Tailwind classes to CSS properties and pixel values (multiply spacing scale × 4):

| Tailwind class | Primary slide property | Value |
|---|---|---|
| `p-4` | `padding` | 16px |
| `px-4` | `padding-left` (also set `padding-right`) | 16px |
| `py-4` | `padding-top` (also set `padding-bottom`) | 16px |
| `pt-4` | `padding-top` | 16px |
| `mt-4` | `margin-top` | 16px |
| `gap-4` | `gap` | 16px |
| `text-[14px]` | `font-size` | 14 |
| `rounded-lg` | `border-radius` | 8px |

For axis shorthands (`px-*`, `py-*`, `mx-*`, `my-*`), set the primary slide to one axis property but include both as slides.

For Tailwind classes, also add an inline style override on the target element so the runtime can manipulate the value directly:

```jsx
<div data-budge-target className="py-4" style={{ paddingTop: '16px', paddingBottom: '16px' }}>
```

### Design token snapping

If the project defines design tokens as CSS custom properties on `:root` or `@theme` (Tailwind v4, Shadcn, plain CSS vars), the runtime automatically snaps ↑/↓ stepping through them by matching property to scale:

| Property match | Discovered prefix |
|---|---|
| `padding*`, `margin*`, `gap` | `--spacing-*` |
| `font-size` | `--text-*` |
| `border-radius*` | `--radius-*` |
| `color`, `*-color` | `--color-*` (no snap yet — palette cycling is a follow-up) |

When a token matches the current value, the widget shows its name (e.g. `16px · md`) and Enter emits `Set \`padding\` to \`var(--spacing-md)\`` instead of a raw px value. Users can still type digits to escape to arbitrary px.

You don't need to specify `scale` on slides — it's auto-detected from `property`. Pass `scale: null` to disable snapping for a slide, or `scale: "spacing" | "text" | "radius" | "color"` to override. Pass `tokens: [{ name, value, numeric }]` to override discovery entirely. Use `unit: "px"` when relying on token snapping (the runtime applies the token's raw value so rem/em tokens resolve correctly regardless).

## Step 3 — Mark Target Element

Add `data-budge-target` to the changed element in source:

```jsx
<div data-budge-target style={{ paddingTop: '16px' }}>
```

## Step 4 — Activate

Use `StrReplace` to add a config element to `app/layout.tsx` inside `<body>`, passing the slides as JSON:

```tsx
<div data-budge={JSON.stringify({ slides: [
  { label: "padding-top", property: "padding-top", min: 0, max: 64, value: 16, original: 8, unit: "px" },
  { label: "padding-bottom", property: "padding-bottom", min: 0, max: 64, value: 8, original: 8, unit: "px" },
  { label: "padding-left", property: "padding-left", min: 0, max: 64, value: 12, original: 12, unit: "px" },
] })} hidden />
```

## Step 5 — Complete

**Your turn is done.** Do NOT open a browser, verify the panel, or wait for the user. Next.js HMR delivers the change.

Tell the user: "I've changed X to Y. Use ↑↓ to fine-tune, ←→ to switch properties."

When the user pastes the submitted prompt, it reads as a normal edit instruction — make the edit and remove the `data-budge` config element.
