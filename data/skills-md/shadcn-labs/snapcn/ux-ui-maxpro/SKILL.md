---
name: ux-ui-maxpro
description: >
  Replicate a reference UI pixel-for-pixel and build polished, token-driven site chrome.
  Use when the task is to match a screenshot or live site exactly, redesign a page to look
  like a design reference, or build a masonry/gallery/grid layout that must feel like the
  source. Triggers include "pixel perfect", "exact replica", "not a single change", "match
  this design", "like this screenshot", "masonry grid", "design gallery", "redesign the
  overview", "same spacing", "same design fashion", "clone this layout", and any request that
  pairs a UI target image with "make it exactly like that". Also activate when measuring
  spacing/typography off a reference before writing CSS.
---

# ux-ui-maxpro

A playbook for reproducing a reference UI exactly, on this repo's design system, without
drifting into approximation or fabricated content. Optimized for the snapcn stack
(Next.js App Router + Tailwind v4 + token-driven `app/globals.css`, DESIGN.md rules), but the
method is stack-agnostic.

## The one rule

**Measure before you type.** Never eyeball a reference straight into code. Extract a written
spec first; code against the spec. Guessing produces "close-ish", and "close-ish" is exactly
what the user rejects when they say "not even a single change".

## 1. Extract a spec from the reference

Read the screenshot(s) like a design system and write down concrete numbers before touching
any file:

- **Structure**: how many regions (top bar, sidebar, content), and each region's width/height.
  Note whether the top bar has a border/shadow/blur or is flush with the page background.
- **Grid**: column count at the widest breakpoint, gutter size, and how it steps down
  (4 → 3 → 2 → 1). For masonry, note whether card heights vary and by how much — that varied
  rhythm is usually the whole point.
- **Cards / tiles**: corner radius, surface color, border vs borderless, shadow vs flat,
  overlay elements (avatars, buttons) with their size and inset from the corner.
- **Type**: size, weight, and color for each text role (title, tagline, meta, nav link). Note
  when two roles sit inline on one baseline (e.g. bold title + gray tagline).
- **Pills / controls**: capsule height, horizontal padding, gap, and the active-vs-inactive
  treatment (a black/white inversion is common).
- **Color**: sample the exact surface grays and accents. They are rarely pure `#fff`/`#000`.

Keep this spec next to you; every class you write should trace back to a measured number.

## 2. Map every element to honest data

For each reference element, decide its real-data equivalent in this project. **Never fabricate
live-looking numbers** (this repo's standing rule): a "63 online" indicator becomes a real
derived count (e.g. total components); a "Last updated 11h ago" becomes a real timestamp from
an API with a graceful fallback, not a hardcoded string. If there is no honest equivalent,
drop the element rather than fake it. Preserve accessibility affordances the reference lacks —
`aria-label`/`title` on icon-only links, `aria-pressed` on filter pills.

## 3. Style through tokens, never hex

Per DESIGN.md, components must not hardcode colors, radii, or shadows. Any new surface the
reference needs (e.g. a gallery card gray) becomes a **new semantic token** in
`app/globals.css`:

- Add the raw value to both `:root` (light) and `.dark` (dark) — a dark peer is mandatory,
  even when the reference is light-only; tune the dark value by eye.
- Register it under `@theme inline` (`--color-<name>: var(--<name>)`) so a `bg-<name>` /
  `text-<name>` utility exists.
- If the exact look requires a documented deviation from DESIGN.md (capsule buttons, blur
  chips, a borderless card), add a short amendment to DESIGN.md so the next contributor does
  not "fix" it back.

## 4. Masonry recipes

- **CSS columns** (`columns-N`, children `break-inside-avoid mb-*`) is the default: it packs
  top-to-bottom per column, SSRs with zero layout shift, and — crucially — keeps every card in
  **one DOM parent**, so a stable React `key` preserves a card's mounted state across filtering
  and sorting. Use it unless the design truly needs left-to-right row order.
- **JS balanced columns** (measure heights, place into the shortest column) gives row-major
  order but costs a first-paint measurement pass and remounts children across column parents.
  Only reach for it when row order is a hard requirement.
- **Manufacturing a varied rhythm**: when the source media is uniform (e.g. all 16:9), assign
  each card a deterministic tile shape by a stable function of its index/slug so the shape never
  changes when the list is filtered or reordered. Center the real media *contained* on the
  tile's surface (never crop unless the user opts into cropping) — compute which dimension binds
  from the static tile-ratio vs media-ratio comparison.

## 5. Heavy-media grids

A grid of 100+ live players/videos cannot mount eagerly. Reuse this repo's load-bearing
pattern: lazy-mount each preview via `IntersectionObserver` (`rootMargin: "200px 0px"`), keep a
placeholder before mount, and **pause playback when the card scrolls offscreen** so only a
handful render at once. When filtering unmounts cards, their players are freed automatically;
keep keys stable so survivors are not needlessly remounted.

## 6. Verify by overlay, in both themes

Being "done" means it matches — prove it:

- Run the app and screenshot the built page at the reference's exact breakpoints.
- Overlay the two at ~50% opacity (or place side by side) and check every measured number: bar
  height, baseline alignment, pill height and gaps, gutters, card radius, overlay size/inset.
- Resize through each breakpoint boundary and confirm the column count steps as specified.
- Toggle light/dark and confirm every new token reads correctly in both.
- Tab through the keyboard path (pills → controls → cards) and confirm focus rings + ARIA.
- Open the sibling pages you did **not** intend to change and confirm they are byte-identical —
  shared chrome edits leak easily.

Only call it done after the overlay matches and the siblings are untouched.
