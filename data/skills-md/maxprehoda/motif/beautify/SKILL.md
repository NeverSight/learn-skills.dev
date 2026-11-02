---
name: beautify
description: "Fixes small mistakes in an existing UI without changing its design: spacing and font sizes that are off the scale in DESIGN.md, lines of text that are too long, icons that look off-center, text that clips or overflows, small tap targets and missing focus styles. Use when the user wants an existing UI cleaned up rather than redesigned."
---

# Beautify

Fix small mistakes in an existing UI. Don't redesign it.

## Before you start

```bash
test -f DESIGN.md || echo "MISSING, run design-system first"
```

Stop if `DESIGN.md` is missing. This pass moves values onto the scales in `DESIGN.md`. Without those scales there's no definition of correct, and every change becomes a matter of taste.

## What to fix

| Problem | Fix |
|---|---|
| Spacing off the scale | Use the nearest spacing token, if it's less than half a step away |
| Font size off the scale | Use the nearest size in the type scale |
| Lines too long | Keep body text between 45 and 75 characters per line |
| Icons look off-center | Center icons on the height of capital letters, not the whole text box. Usually a 1px nudge |
| Overflow | Fix text that gets cut off, wraps badly, or spills out of its box at any screen width |
| Line height | Follow the line-height rule in `DESIGN.md`: tight for big headings, looser for body text |
| Uneven gaps | Give sections at the same level the same gap |
| Long user content | Limit user-entered text, like names or titles, that could break the layout if it's very long |
| Small tap targets | Make anything clickable at least 24x24px |
| Focus styles | Add `focus-visible` styles where they're missing |

## What not to touch

Don't change colors (except swapping a Tailwind color for its named role), layout, which components are used, shadows, gradients, borders, fonts, images or copy.

Don't add decoration of any kind.

## How to tell if a change belongs here

Compare the before and after. If it looks like a different design decision, it doesn't belong in this pass. If it looks like the same design with a mistake fixed, it does.

If you can't tell, leave it alone and list it under "noticed, not changed".

## Steps

### 1. Find values that are off the scale

```bash
npm run design-lint -- --json > /tmp/design-lint.json
```

Then read the files with the most findings. The linter catches numbers that are off the scale. Line length and icon alignment only show up when you read the markup.

### 2. Check three screen widths

If a dev server is available, check at 375px, 768px and 1440px. Overflow and line-length problems show up at the smallest and largest widths and are easy to miss at a normal desktop size.

### 3. Fix one component at a time

Read a component, fix everything in it, then move to the next. Don't find-and-replace a class across the whole repo. The same value can mean different things in different components.

### 4. Report

```
src/routes/about/+page.svelte
  line length  text was 118 characters wide -> max-w-prose (65 characters)
  spacing      pb-[15px] -> pb-4
  alignment    icon nudged 1px down to line up with its label
```

Give the total number of changes. Say clearly that no colors, layout or components were changed.
