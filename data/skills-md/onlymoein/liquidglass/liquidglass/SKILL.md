---
name: liquidglass
description: Build React UIs with @onlymoein/liquidglass, an iOS 27-style glass component library for the web (and @onlymoein/liquidglass-native for React Native and Expo). Use when a project imports @onlymoein/liquidglass or liquidglass-native, when asked for iOS-style or "liquid glass" UI in React, or when glass components look wrong, don't bend, don't show up, or slow a page down.
---

# liquidglass

`@onlymoein/liquidglass` is glass for React 18+: a frosted, rim-lit surface that bends what's
behind its edge, and iOS 27's controls built from it. Components bring their own CSS the first
time they render, so there is nothing to set up. They're client components (`"use client"` is in
the bundle), safe to import from a Next.js server component file.

```bash
npm install @onlymoein/liquidglass
```

```tsx
import { Button, Glass, Switch } from "@onlymoein/liquidglass";

<Glass style={{ borderRadius: 28, padding: 20 }}>Anything on glass</Glass>
<Switch aria-label="Wi-Fi" defaultChecked />
<Button variant="filled">Continue</Button>
```

To load every component's CSS up front instead, import `@onlymoein/liquidglass/styles.css` once.

## Before writing any glass

- **Glass needs something behind it.** It blurs, lifts and saturates its backdrop and bends the
  edge. Over a flat white page it reads as a faint grey card. Put it over a photo, a gradient,
  colourful content or content that scrolls under it, as iOS does.
- **Check the ancestors.** An ancestor with `filter`, `opacity` below 1, `mask`, `clip-path`,
  `mix-blend-mode`, `backdrop-filter`, or `will-change` naming one of those, becomes the glass's
  backdrop root. The glass then sees only what's inside that ancestor. Put such effects on
  siblings or below the glass, and fade glass in on the glass itself, not on a wrapper.
- **Don't nest glass in glass.** Glass is a `backdrop-filter`, so glass inside glass sees only
  the outer pane. Put text and icons on a `Glass`. For several buttons on one pane, use a
  `ToolbarGroup`, where buttons give up their own glass and share the group's (a `filled`
  button keeps its fill). For separate pieces that flow together, use a `GlassGroup`.
- **Shape comes from CSS.** Size, padding and `border-radius` are yours. The glass measures its own
  box and radius, and draws continuous (iOS-style) corners and a lens to fit. It refits whenever
  its size changes.
- **Every control is controlled or uncontrolled.** Pass `value`/`checked`/`open` with
  `onValueChange`/`onCheckedChange`/`onOpenChange`, or `defaultValue`/`defaultChecked`/`defaultOpen`.
  The handler names are `on…Change`, never `onChange`.
- **Label anything without text.** An icon-only `Button`, a `Switch`, a `Slider` and a `Menu` need
  `aria-label` (`Menu` requires it).

## Components

| Component | Use it for | Key props |
| --- | --- | --- |
| `Glass` | A plain piece of glass to put anything on | any `div` props |
| `Button` | Glass or filled button | `variant: "glass" \| "filled"`, `size: "small" \| "regular" \| "large"` (28/36/52 pt), `icon`, `tint` (any CSS colour), `destructive` |
| `Toolbar`, `ToolbarGroup` | A bar of actions that sticks to the top of what scrolls and frosts as content passes under | `edge: "uniform" \| "soft" \| "none"`. Buttons in one `ToolbarGroup` share one piece of glass |
| `NavigationBar` | A screen's top bar: back button, actions, large title that slides into the bar | `title` (required), `onBack`, `backLabel`, `leading`, `trailing`, `large` (default true), `level` |
| `TabBar` | Tabs with a lens that follows the finger | `items: { value, label, icon?, href? }[]`, `value`, `onValueChange`, `minimized`, `onExpand`, `link` (e.g. Next.js `Link`) |
| `Switch` | On/off | `checked`, `defaultChecked`, `onCheckedChange` |
| `Slider` | A number on a track | `value`, `onValueChange`, `min`, `max`, `step` |
| `Stepper` | Minus/plus buttons | `value`, `onValueChange`, `min`, `max`, `step` |
| `SegmentedControl` | One of a few choices | `items: { value, label, disabled? }[]`, `value`, `onValueChange` |
| `Input`, `SearchField` | Text fields | `value`, `onValueChange`, `icon`, `variant: "glass" \| "fill"` |
| `Menu` | A pull-down that grows out of its trigger | `aria-label` (required), `items`, `label` (pill trigger), `icon`, `align`, `chevron`, `trigger` (props for the trigger `Button`) |
| `ContextMenu` | Hold down or right-click something to lift it and open a menu | `items`, `children` (what's held) |
| `Sheet` | Bottom sheet with detents | `open`, `onOpenChange`, `detents: ("medium" \| "large")[]`, `aria-label` |
| `Alert` | A modal question | `title`, `message`, `actions: { label, role?: "cancel" \| "destructive", onSelect? }[]` |
| `PageControl` | Page dots | `count`, `value`, `onValueChange`, `glass` |
| `Progress`, `Spinner` | Progress bar (`value` 0–1), activity indicator | |
| `GlassGroup` | Glass that flows together when pieces come close | `spacing` (points) |

Menu items are `{ label, icon?, onSelect?, href?, checked?, keepOpen?, destructive?, disabled? }`,
`{ heading }`, or `"separator"`. `href` makes an item a link: `onSelect` runs instead if given,
for a router's navigate, and ⌘, Ctrl, Shift or the middle button opens a new tab. Use
`checked` with `keepOpen: true` for settings like a theme picker.

```tsx
<Toolbar aria-label="Notes">
  <ToolbarGroup aria-label="Navigation">
    <Button aria-label="Back" icon={<ChevronLeft />} />
  </ToolbarGroup>
  <ToolbarGroup aria-label="Actions">
    <Button>Share</Button>
    <Button>Edit</Button>
  </ToolbarGroup>
</Toolbar>

<Menu
  aria-label="Sort"
  label="Sort"
  items={[
    { heading: "Order" },
    { label: "Newest", checked: sort === "new", keepOpen: true, onSelect: () => setSort("new") },
    { label: "Oldest", checked: sort === "old", keepOpen: true, onSelect: () => setSort("old") },
    "separator",
    { label: "Delete all", destructive: true, onSelect: clear },
  ]}
/>

<Sheet aria-label="Details" open={open} onOpenChange={setOpen} detents={["medium", "large"]}>
  {details}
</Sheet>
```

Placement rules that matter:

- `Toolbar` and `NavigationBar` go **first inside the element that scrolls**; they stick to its
  top. Don't wrap them in `position: fixed`.
- `Menu`, `Sheet`, `Alert` and `ContextMenu` open in the top layer, so clipping and `z-index`
  around them don't matter.
- In a `Sheet`, drags that start on a slider, a text field, or anything marked
  `data-lg-no-sheet-drag` stay with that element.
- A popup from another library (Radix, Base UI) gets the menu's grow-in spring with the class
  `lg-grow`. It runs on `data-open` and `data-closed`, from the popup's `transform-origin`.

## Look and theme

- Light and dark follow the system. Pin one with `data-theme="light"` or `data-theme="dark"` on any
  ancestor.
- `--lg-transparency`, set anywhere above the glass: `0` fully tinted, `0.5` regular (default),
  `1` clear. Reduced transparency and increased contrast settings make glass fully tinted.
- Colours to override in your CSS: `--lg-fill` (accent of filled buttons and sliders), `--lg-on`
  (switch on), `--lg-glass-tinted` (the tint below 0.5), `--lg-shine` (rim strength, 1 = iOS),
  and `--lg-contrast`/`--lg-brightness`/`--lg-saturate` (with `-small` variants for glass 60 pt or
  less). The last group is what the glass does to its backdrop.
- Lens shape on a single piece of glass: `--lg-bezel` (px of edge that bends), `--lg-thickness`
  (how far it bends), `--lg-zoom` (above 1 magnifies), `--lg-refraction` (0 turns the bend off).
  These are read **when the glass is measured**. Set them before it renders, or in a class
  present at mount. Changing them later takes effect only after the glass next changes size.

## Browsers

- **Chromium:** glass bends the live backdrop, as on iOS.
- **Safari:** same colour, blur and rim, but the edge doesn't bend. No page can bend a live
  backdrop in Safari, and that's not fixable from your side. Don't add workarounds.
- **Firefox:** same as Safari, unless you mark what's behind the glass with
  `data-liquidglass-backdrop` (a wallpaper, a hero image). Glass over it then bends a copy of it.
  Mark a small subtree, not the whole page: every element in it is copied for each glass over it.

```tsx
<img data-liquidglass-backdrop src="/wallpaper.jpg" alt="" />
```

## Performance and CSP

- Lens maps and rims are drawn in a Web Worker and reach the page as `blob:` image URLs. Glass
  is frosted at once and gains its lens a moment later. With a Content Security Policy, allow
  `worker-src blob:` and `img-src blob: data:`. Without the worker the glass draws on the page
  instead, and needs `data:`.
- Each glass holds its lens while it uses it; sizes it has left are freed. Resizing is cheap
  and doesn't leak.
- Every glass is a `backdrop-filter` layer. Dozens of large pieces over moving content cost GPU
  time on phones. Prefer a few bars and controls over a wall of glass cards.
- The repo's checks are `npm run size`, `npm run perf:lighthouse` and `npm run perf:frames`.

## When something looks wrong

| Symptom | Likely cause |
| --- | --- |
| Glass is invisible or plain grey | Nothing colourful behind it, an ancestor with `filter`/`opacity`/`mask`/`backdrop-filter` is the backdrop root, or it's nested in other glass |
| Edge doesn't bend | Safari or Firefox (expected); in Chromium, a CSP blocking `blob:` images, or `--lg-refraction: 0` |
| Lens doesn't match a new `--lg-*` value | Those are read at measure time; resize or remount the glass |
| Toolbar doesn't stick or frost | It isn't the first child of the scrolling element |
| A drag inside a `Sheet` moves the sheet | Mark the element `data-lg-no-sheet-drag` |
| Styles missing in a test or SSR snapshot | Styles are inserted on first client render; import `@onlymoein/liquidglass/styles.css` |

## React Native and Expo

`@onlymoein/liquidglass-native` has the same component names (`Glass`, `GlassGroup`, `Button`,
`Menu`, `Switch`, `Slider`, `Stepper`, `SegmentedControl`, `TabBar`), plus `Backdrop`, `Text` and
`ScrollView`. It needs Expo SDK 54+ and `expo-glass-effect`. On iOS it renders Apple's own UIKit
glass and controls. On Android it draws its own glass, which shows what's inside a `Backdrop`.
Read its README in `node_modules/@onlymoein/liquidglass-native/README.md` before using it. Its
props differ from the web package's in places (e.g. `Glass` takes `variant`, `tint` and
`interactive`).
