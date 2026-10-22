---
name: concentric
description: Install, set up and use the tailwindcss-concentric plugin to fix and prevent mismatched nested corner radii in Tailwind CSS v4 projects. Use when the user asks to add or set up tailwindcss-concentric, to audit or fix nested border radii, or when building or reviewing UI where a rounded element sits inside a padded or bordered rounded parent (cards with media, buttons in search bars or toolbars, segmented controls, selection rings, modals, input groups), when you see hard-coded inner radii such as rounded-[calc(...)], or when the user mentions concentric, nested, inner or outer corner radius.
---

# Concentric corners with tailwindcss-concentric

When a rounded element sits inside a rounded parent, the inner corner should follow the outer one:

```
inner radius = outer radius - gap        (gap = the distance between the two edges on that side)
```

`tailwindcss-concentric` computes this in CSS. Give the child `rounded-concentric` and it reads the radius, padding and border of its nearest rounded ancestor, the padding and border of a plain wrapper in between, its own margins, and for `absolute`/`fixed` children their insets. The math is in [references/rules.md](references/rules.md); before/after examples are in [references/examples.md](references/examples.md).

The package ships three things: the `rounded-concentric` utilities (a CSS import), an audit CLI (`npx tailwindcss-concentric audit [paths...] [--json]`), and `tailwindcss-concentric/merge` for tailwind-merge. Match the work to the request:

- **Set it up** ("install tailwindcss-concentric", "add concentric corners"): do step 1 and install whatever is missing. Then offer to run the audit.
- **Audit or fix existing UI**: do step 1, run the audit, then work through steps 2 to 5.
- **Build new UI**: do step 1, then follow steps 2 to 4 for every rounded element you nest inside another.

## 1. Check the setup first

1. **Tailwind v4 only.** The main CSS file has `@import "tailwindcss";`. If the project is on Tailwind v3 (a `tailwind.config.js` with `@tailwind base;` directives), stop and tell the user; the plugin does not support v3.
2. **Install and import.** `tailwindcss-concentric` must be in `package.json`. If it is missing and the user asked you to set up or use the plugin, install it with the project's package manager, picked from the lockfile (`npm i`, `pnpm add`, `yarn add` or `bun add tailwindcss-concentric`). If they only asked for a review, tell them it is missing and offer to install it. The CSS file that imports Tailwind must import the plugin right after it:
   ```css
   @import "tailwindcss";
   @import "tailwindcss-concentric";
   ```
3. **tailwind-merge.** If the project merges classes (`twMerge`, `extendTailwindMerge`, or a `cn()` helper built on them), register the plugin's classes. Otherwise `cn("rounded-lg", "rounded-concentric")` keeps both classes and `rounded-lg` wins:
   ```ts
   import { extendTailwindMerge } from "tailwind-merge";
   import { withConcentric } from "tailwindcss-concentric/merge";

   export const twMerge = extendTailwindMerge(withConcentric);
   // with your own config: extendTailwindMerge({ ...yourConfig }, withConcentric)
   ```
   Replace every `twMerge` import used by `cn()` with the extended one. Do this before relying on `rounded-concentric` in any component that merges class names.

## 2. Decide which elements should be concentric

Start with the audit when the plugin is installed: `npx tailwindcss-concentric audit [paths]` lists nested radii that do not match their parent, with the concentric value and the class to use. Treat its output as candidates. It reads markup, not layout, so it cannot tell whether a child really sits in its parent's corner, and it skips values it cannot evaluate (custom theme radii, CSS variables, variant classes). It also misses class names passed through component props across files. Review each candidate with the rules below, and still read the components yourself.

Use a concentric class when **all** of these hold:

- The element has a corner radius, and its parent (or the nearest ancestor that has a `rounded-*` class) is rounded too.
- The element's corner sits in the parent's corner: nothing else sits between that corner of the child and that corner of the parent, so the two curves are seen together.
- The two shapes are meant to read as one nested shape: an image in a card, the active tab in a segmented control, the button inside a search bar, a selection ring, a panel inside a bordered card.

Leave the element alone when:

- It is a shape in its own right: avatars, status dots, badges and tags (`rounded-full` pills), icons, chips in the middle of content.
- It does not touch the parent's corner: form fields below a heading, list items in the middle of a card, a grid of tiles whose container is not rounded.
- The gap is at least the outer radius (for example `rounded-lg p-6`). The formula gives 0 there, which squares the child. Apply it only if a square corner is wanted; otherwise keep the design radius and mention it in your report.
- The element is already correct (`rounded-concentric`, or a plain radius on purpose).

## 3. Pick the class

| Situation | Class |
|---|---|
| Child hugs all four corners | `rounded-concentric` |
| Child hugs only some corners (media flush with the top of a card, first/last item of a group) | side or corner variant: `rounded-t-concentric`, `rounded-b-concentric`, `rounded-s-concentric`, `rounded-e-concentric`, `rounded-tl-concentric`, `rounded-ss-concentric`, ... |
| Start/end of a horizontal group in an app that can run right-to-left | logical variants `rounded-s-concentric` / `rounded-e-concentric` (never `-l-`/`-r-` for start/end) |
| One plain wrapper with padding sits between the rounded parent and the child, or the child is `absolute inset-*`, or has margins (`-mx-4` bleed) | `rounded-concentric`; the plugin measures all of these |
| Two padded wrappers on the same side, or a wrapper with margins, sit in between | add `rounded-concentric` to the outer wrapper as well, so it joins the chain and passes everything inside it on |
| Space comes from inline styles or custom CSS | explicit gap: `rounded-concentric-{n}` (spacing scale, `rounded-concentric-2` = 0.5rem) or `rounded-concentric-[6px]` |
| Parent padding differs per axis (`px-4 py-2`) and the corner should follow both | add `concentric-elliptical` |
| Parent uses `corner-shape: squircle` | add `concentric-squircle` to the child (and to the parent, or `[corner-shape:squircle]`) |
| Deep nesting squares the innermost corners | set a minimum on any ancestor: `[--concentric-floor:2px]` |

Keep the rest of the child's classes. Replace only its radius class (`rounded-xl` → `rounded-concentric`, `rounded-t-lg` → `rounded-t-concentric`, `rounded-[calc(...)]` → `rounded-concentric`).

## 4. Know what the plugin cannot see

The radius comes from the **nearest element whose class contains `rounded`**. The gap comes from Tailwind classes only: padding (`p-*`, `px-*`, `ps-*`, ...) and border width (`border`, `border-x-4`, ...) on that element and on the nearest wrapper in between, margins (`m-*`, `-mt-4`, ...) on the child, and insets (`inset-*`, `top-*`, `start-*`, ...) on `absolute`/`fixed` children. So:

- **Each side counts one wrapper.** In `rounded-3xl > p-3 > p-2 > rounded-concentric`, the child sees only the `p-2` wrapper. Margins on wrappers are not counted either. Give the outer wrapper `rounded-concentric`: it has no visible effect unless the wrapper has a background, border or `overflow-hidden`, and it keeps working if the padding is responsive. An explicit gap also works.
- **Insets are measured from the rounded ancestor's padding edge.** That assumes it is the containing block (`relative`). If a `relative` wrapper in between is the containing block, use an explicit gap.
- **Padding from inline styles or custom CSS is not seen.** Use Tailwind classes, or an explicit gap.
- **Percentage radii (`rounded-[50%]`) are not supported.** Fraction insets (`inset-x-1/4`) fall back to the parent's padding, and `auto` margins count as 0.
- **`@apply` classes join only if the element's class attribute contains the text `rounded`.**
- **Direction comes from `dir` attributes**, including `dir="auto"` and any depth in browsers with `@scope` (Chrome 118, Safari 17.4, Firefox 146); older browsers read up to three nested levels. Direction set only through CSS `direction` is not detected.
- **Depth.** Nine stacked rounded elements are exact; deeper ones reuse the ninth level's value.
- **A plain `rounded-*` element starts a new chain.** Its children are measured from it, not from the outer concentric elements.

## 5. Verify

For each change, compute the expected radius by hand (see [references/rules.md](references/rules.md)) and, when you can run the app, check it in the browser console:

```js
getComputedStyle(document.querySelector("#el")).borderTopLeftRadius
```

Pills report a very large number (for example `3.35544e+07px`); that is expected.

Report which elements you changed and why, which ones you left alone on purpose, and any spot where the plugin cannot see the gap (and the class you used there).
