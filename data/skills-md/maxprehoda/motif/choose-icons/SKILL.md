---
name: choose-icons
description: "Lists the icons a product needs, checks which icon libraries actually have them, then installs one library and replaces every existing icon, inline SVG and emoji with it. Use after the design-system pipeline, or when an app mixes icons from several sources."
---

# Choose Icons

Work out which icons the product needs, check that a library has all of them, then use that one library everywhere.

Check what a library has before choosing it. A library picked for its looks will be missing specific icons, and the gaps get filled with hand-drawn ones that don't match.

## Step 1: List the icons the product needs

Find what the code uses now:

```bash
grep -rhoE '<(svg|Icon)[^>]*|lucide-|react-icons|@heroicons|phosphor' src --include="*.svelte" --include="*.tsx" | head -40
grep -rn -E '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' src --include="*.svelte" --include="*.tsx" | head -20
```

Then look through the product: navigation, buttons and actions, empty states, status indicators, file types, integrations.

Write the list as ideas, not icon names. Write "export", "merge", "webhook", "billing", not "arrow-down-tray". You check libraries against the ideas. Every library has home, user and settings, so the specific ones are what decide it.

## Step 2: Check which libraries have them

For each candidate library, look up every idea on the list, especially the ones specific to this product.

| Library | Roughly how many icons | Style |
|---|---|---|
| Lucide | 1,600 | 2px outline, geometric |
| Phosphor | 9,000 | 6 weights |
| Heroicons | 300 | outline and solid |
| Radix Icons | 300 | drawn on a 15x15 grid |
| Tabler | 5,800 | 2px outline |

These counts go out of date. Check each library's current catalog.

Report how many ideas each library covers, and name what's missing: "Phosphor 34 of 34. Lucide 31 of 34, missing webhook, merge and oauth."

Choose in this order:

1. Coverage. Missing icons turn into hand-drawn ones.
2. One library only. Different line weights and grid sizes look wrong next to each other.
3. A line weight that matches the rest of the UI.
4. A library that lets you import icons one at a time, not the whole set.

Show the user the top two with their coverage and let them choose.

## Step 3: Size icons to match the text

Icons usually sit next to text, so their size comes from the font sizes in `DESIGN.md`, not from a separate icon scale.

| Next to | Icon size |
|---|---|
| `text-sm` | 16px |
| `text-base` | 20px |
| `text-lg` | 24px |
| on its own | 24 to 32px |

Line icons up with the height of the capital letters, not the whole text box. This usually takes a 1px nudge.

Set icon color to `currentColor` so each icon takes the color of the text around it.

## Step 4: Replace the icons

```bash
npm install <library>
```

Replace icons one component at a time, not one icon at a time. Replace inline SVGs and emoji too, since emoji look different on every platform.

Remove any imports and SVG files that are no longer used.

## Report

The library, its coverage ("34 of 34"), how many icons you replaced from each source (old library, inline SVG, emoji), and how the bundle size changed. List any idea that has no good icon.
