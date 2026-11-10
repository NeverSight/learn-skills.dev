---
name: icon-set-generator
description: >-
  Create a new product-specific SVG icon system on a fixed visual specification. Use when the
  user explicitly requests a coherent batch of original icons and no target set exists,
  including requests that reject stock libraries. Use icon-set-extend when a target set exists.
compatibility: Any project. The bundled scripts need only standard-library python3.
---

> 中文版: [SKILL.zh-CN.md](SKILL.zh-CN.md)

# Generate a consistent icon set

One icon can survive improvisation. A set cannot. Small changes in stroke, optical size, gaps,
and recurring parts accumulate into drift. Freeze those decisions before drawing and validate
the batch against them.

## Workflow

### Step 1: Get the brief

Inspect the project for brand rules and usage sizes before asking questions. Collect only the
missing facts:

- Product, audience, and tone
- Smallest render size and every distinct size range
- Required icons and the screens where they appear
- Existing type, interface, or brand artwork the icons must sit beside

Use a 16 grid for 12 to 20px rendering and a 24 grid for 22px or larger. When both ranges
matter, draw separate small and large sets. The full range requires distinct drawings.

This step is complete when the grid, tone, inventory source, and adjacent visual system are
known or stated as explicit assumptions.

### Step 2: Confirm the inventory

Read `references/icon-inventory.md`. Walk the product surfaces in scope, then group the
proposed icons by use so omissions and duplicate concepts are visible. Reuse one drawing for
semantic aliases.

If the user supplied a complete list, confirm only conflicts or likely omissions. If they asked
you to choose the set, present the inventory before drawing.

This step is complete when every surface in scope has an icon or a deliberate exclusion and
each drawing has one filename plus any semantic aliases.

### Step 3: Freeze the specification

Read `references/style-presets.md`. Use the user's exact values when supplied. Otherwise,
recommend one preset with a concrete reason and confirm it before drawing.

Copy the confirmed preset values into `icons/style-spec.json`. Add the set name, diagonal
axis, and an empty `icons` array. Treat the file as frozen during drawing. If a form exposes a
bad rule, revise the specification once and apply the change to the whole set.

This step is complete when `style-spec.json` contains every root style value and the chosen
diagonal axis.

### Step 4: Build the element registry

List every part that recurs across the approved inventory. Draw each part once at final
coordinates and save it in `icons/elements.md`. Record its anchor point and allowed rotations.
Use `references/svg-patterns.md` as the format model.

Paste registry markup into complete icons instead of redrawing it. Translation uses whole
units. Rotation uses quarter turns unless the specification defines another rule.

This step is complete when every recurring part has one registry entry and every planned use
points back to that entry.

### Step 5: Draw anchors, then batches

Read `references/construction.md` before the first SVG. It is the single source for optical
envelopes, geometry, gap rules, dots, direction, terminals, and filled variants. Read the
relevant section of `references/svg-patterns.md` when a form resists the grid.

Choose one anchor for each optical envelope represented in the inventory. Compare the anchors
together at native size. Draw the rest in batches of about five, then compare each batch with
the anchors before continuing.

Write one lowercase kebab-case SVG per icon into `icons/`. This step is complete when every
approved icon exists and every batch has been checked at native size against the anchors.

### Step 6: Validate against the frozen specification

```bash
python3 scripts/validate_icons.py icons/
```

The validator automatically loads `icons/style-spec.json` when it exists. Pass `--spec` only
when the specification lives elsewhere. It reports errors for broken rules and warnings for
measurements that need visual judgment.

Fix every error and run the command again. Inspect every warning in the preview. Fix it or
record a concrete reason for keeping it.

This step is complete when validation exits successfully, reports zero errors, and every
warning has a recorded disposition.

### Step 7: Build the preview and deliver

```bash
python3 scripts/build_preview.py icons/ --out icons/preview.html
```

Inspect every icon at native size and twice native size on light and dark backgrounds. Update
the `icons` array in `style-spec.json`, rebuild the preview, and verify that it lists every SVG.

The final directory contains:

```text
icons/
|-- style-spec.json
|-- elements.md
|-- preview.html
|-- arrow-right.svg
`-- calendar.svg
```

The task is complete when the approved inventory, specification, registry, clean validation,
warning dispositions, and final preview all agree.

## SVG rules

- Use `currentColor` for every stylable color. Outline icons use `fill="none"` and
  `stroke="currentColor"`. Filled forms use `fill="currentColor"`.
- Put shared style attributes on the root `<svg>` and keep them identical across files.
- Use a child `stroke-width` only for a documented optical correction.
- Keep `id` and `class` off the root. Bake root transforms into coordinates.
- Use at most two decimal places. Prefer whole and half units.
- Choose the fewest SVG elements that express the form clearly.

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="1.5"
     stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 10.5 12 3l9 7.5"/>
  <path d="M5 9.5v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-10"/>
</svg>
```

## Reference files

- Read `references/icon-inventory.md` during Step 2.
- Read `references/style-presets.md` during Step 3.
- Read all of `references/construction.md` before Step 5.
- Read only the relevant form in `references/svg-patterns.md` when a specific drawing needs it.
