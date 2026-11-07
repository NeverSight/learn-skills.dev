---
name: annotating-screenshots
description: Use when the user wants a screenshot or other PNG annotated (arrows pointing at UI elements, boxes or ovals around them, private data blurred, erased or redacted, text highlighted, one area spotlighted, numbered step badges, short text labels, or lines), or wants a previous annotation adjusted. Draws the annotations deterministically with the markshot CLI.
compatibility: Requires the markshot CLI 0.4.0 or later (macOS, Linux or Windows) on PATH, a POSIX-style shell for the examples, and the ability to view PNG images.
metadata:
  cli: markshot
  version: "1.5"
---

# Annotating screenshots

`markshot` draws annotations on a PNG from a JSON spec. The same input, spec and binary always give the same PNG bytes, so you fix a render by editing values and rendering again.

```
markshot render <in.png> --spec <spec.json | -> -o <out.png> [--dpr N]
markshot grid   <in.png> -o <grid.png> [--step N] [--region X,Y,W,H]
markshot schema        # every spec field, its range and default
```

If `markshot` is not on PATH, ask the user where it is installed, or offer to install it (https://github.com/hypn4/markshot#how-do-i-install-it); don't draw the annotations some other way. `markshot --version` must print 0.4.0 or later.

## Workflow

Copy this checklist and tick it off:

```
- [ ] 1. Image size: echo '{"annotations": []}' | markshot render in.png --spec - -o /tmp/size.png   (prints width, height, dpr; a "no DPI" warning means you set "dpr", see references/spec.md)
- [ ] 2. Locate each target. Unsure? markshot grid in.png -o grid.png, then read the labels; on a large screenshot add --region X,Y,W,H around the target to read it at full size.
- [ ] 3. Write the spec (Pick a tool, below) and render it from the ORIGINAL input.
- [ ] 4. View out.png at every target and read every warning. Zoom in with markshot grid out.png --region X,Y,W,H -o check.png: the lines show how much room is left.
- [ ] 5. Something off? Edit the stdout spec (Fixing a render, below) and render again from the original.
```

## Coordinates

- Pixels of the input image; origin top-left, y grows down. A point is `[x, y]`, a rect `[x, y, width, height]`.
- Numbers read off `grid` labels are already image pixels: use them as they are. With `--region`, leave out `--step`: the default keeps the labels apart.
- Coordinates estimated on a downscaled view (many image viewers shrink large screenshots; compare the width you saw with step 1): add `"coords": {"space": "scaled", "width": W, "height": H}` with the size you saw.
- Clipping, normalized coordinates, limits, draw order and dpr: [references/spec.md](references/spec.md).

## Pick a tool

| The user wants to… | `type` | Key fields |
|---|---|---|
| point at something | `arrow` | `from`, `to`; `via` to curve; `style` |
| frame or circle something | `rect`, `oval` | `rect`, or for an oval `around` (the target's box; markshot sizes the oval and, with `size` left out, its line); `fill`: `sketch`, `outline`, `semi`, `solid` |
| hide private data | `blur` | `rect`; `mode`: `pixelate`, `erase` (an opaque box: `rect` with `"fill": "solid"`) |
| mark text like a highlighter | `highlight` | `from`/`to`, or `points` |
| focus on one area, dim the rest | `spotlight` | `rect`; `shape`; top-level `spotlight_dim` |
| frame something and dim the rest | `rect`, `oval` | `"spotlight": true` on the frame, not a second spotlight |
| number the steps | `counter` | `at` (where the tail points), `angle` (`"auto"` finds a free side); `style`; `number`; `ring` (a white ring, for a badge on a frame line) |
| draw a line or divider | `line` | `from`, `to`; `dash`; `start_cap`, `end_cap` |
| add a few words of explanation | `text` | `at` (top-left), `text`; `style`: `label`, `plain` (Latin, Greek and Cyrillic only) |
| show only part of the screenshot | top-level `crop` | `[x, y, width, height]`, in the same coordinates ([references/spec.md](references/spec.md)) |

Every tool's fields, behaviour and a working example: [references/tools.md](references/tools.md).

## Fixing a render

`render` prints `{"width", "height", "dpr", "spec", "warnings"}`. That `spec` is fully resolved (ids, seeds, numbers, dpr and pixel coordinates are filled in), so edit only the values that are off and everything else stays identical.

When the user asks for a change to an earlier render, the edit is exactly what they asked for: those values change and every other value stays as it was. If the change causes a new problem (a bigger badge now covers a label, say), render it as asked anyway, then tell the user and name the edit that would fix it (e.g. `"angle": -45`).

- Render from the original input, never from the previous `out.png`, or the old annotations stay underneath.
- Annotations skipped with a warning are not in the stdout spec; add them back with corrected values.
- An oval fitted with `around` comes back as a fixed `rect`, `size` and `seed`. To refit after an oval-fit warning, use the original `around` spec with `size` omitted. If editing the stdout spec, replace `rect` with the ORIGINAL target's `around`, then remove `size`; the fitted `rect` is not the target box. Restore the original seed choice too: leave `seed` out if the original omitted it, but keep a seed the original specified. Removing only `size` from a resolved `rect` does not run fitting again.
- A counter comes back as its badge's `center`. Before changing its `size` or `angle`, replace `center` with the tail tip `at`, computed from the stdout values, or the tip moves off its target:
  `at = center + 1.65 * R * (cos θ, sin θ)` with θ = `angle` in degrees (0 right, 90 down), R = D[`size`] / 2 * `dpr`, D = [22, 28, 36, 48, 64, 84, 112, 150]. For `"style": "circle"`, `at` = `center`.
- `fill_alpha` is listed only if you set it, so switching a rect's `fill` gives the new fill's default opacity.
- Give annotations an `id` so you can find them in the stdout spec.

An invalid spec exits with code 1, writes nothing, and prints `error: <path>: <message>`, e.g. `error: annotations[0].size: must be 0 to 7, got 9`. What each warning means: [references/warnings.md](references/warnings.md).

## Common mistakes

| Mistake | Fix |
|---|---|
| Coordinates read on a downscaled view used as pixels: annotations land up-left of the target or are "entirely outside" | Add `scaled` coords with the viewed size, or take positions from `grid` |
| Rendering onto the previous output | Always render from the original input |
| A blur rect cut tight to the text | Leave a few pixels around it; use `erase` on flat backgrounds |
| A grey, white or black highlighter on a mid or dark background renders navy | Pick a hue, and tell the user why |
| Putting a blur last to draw it on top | Blurs are always drawn first, under everything |
| A spotlight on the same area as a frame: a bright rim shows beside a hand-drawn line | One frame with `"spotlight": true` |
| An oval's `rect` set to the target's box, or guessed around it: the line crosses the target's corners or the text next to it | Give `around` (the target's box) instead of `rect` |
| Leaving dpr at 1 on a Retina capture without DPI: thin lines, small badges | Set `"dpr": 2` when the report warns about a missing DPI and the UI text is double size |
