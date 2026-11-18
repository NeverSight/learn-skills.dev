---
name: palette
title: Choose, build and repair a palette
description: Pick a palette that fits the request, build hue-shifted ramps, or clean up a sprite whose colours have sprawled. Use when the user asks about colour, wants a specific retro look, or when validate reports off-palette colours.
---

# Choose, build and repair a palette

## Choosing

Match the request, in this order of preference:

1. **The user named a palette or a game.** Use it. `palette op="preset"` for a
   bundled one, `op="load"` for a file they have, or
   `reference op="sample_palette"` to pull one out of a screenshot they gave you.
2. **The user described an era.** "8-bit" → PICO-8. "Game Boy" → gameboy.
   "NES" → build 12–16 colours by hand as 3–4 hues × 4 values.
3. **The sprite is joining an existing project.** `sprite_info` an existing
   asset and match it exactly. Consistency beats a nicer palette.
4. **Nothing said.** PICO-8. It is 16 colours, forgiving, and reads well.

`palette op="preset"` with no valid preset lists what is bundled and says that
anything else can be loaded from a file.

## Building ramps

A ramp is one material's run of colours. Build them hue-shifted:

```
palette op="ramp" base="#c04030" steps=5 spread=0.55
```

Shadows come out cooler, highlights warmer — the thing that separates pixel art
from a brightness slider. Three to five steps per material is plenty; more is
decisions you will not use.

Reuse steps across materials. Sharing the darkest colour between skin and
leather ties the sprite together and costs nothing.

## Repairing a sprawled palette

Symptom: `validate` reports off-palette colours, or the sprite has ninety
near-identical browns.

1. **Diagnose:**

   ```
   palette op="analyze"
   ```

   This reports off-palette colours in the art, near-duplicate palette entries
   (ΔE < 3 — the same colour to a viewer), unused slots and the lowest-contrast
   pair.

2. **Decide the target palette.** Either the existing one, minus the
   near-duplicates, or a fresh one.

3. **Snap the art onto it:**

   ```
   recolor op="snap" layer="…"
   ```

   Perceptual (CIELAB) nearest, applied per distinct colour in one pass. The
   result reports exactly which colour became which and how many pixels moved,
   so you can see whether a merge was wrong before the user does.

4. **Re-check.** `palette op="analyze"` again, then `look op="preview"`. Merging
   two colours that were doing different jobs is the risk here; look for a form
   that has gone flat.

**Or start over from the art:** `palette op="extract"` replaces the palette
with one quantized from the sprite's own colours (RGB sprites only,
`maxColors` default 16) — useful when the sprite came from a reference image
imported at full colour and never had a curated palette to snap onto.

## Contrast

Value contrast carries readability, not hue contrast. Check by running
`recolor op="desaturate"` on a copy — if the shapes stop reading in greyscale,
the palette's values are too close, and no amount of hue will fix it.

## Related

`rules://01-palette-and-color`, `rules://02-shading-and-light`,
`rules://20-color-for-pixel-art`, `rules://21-limited-and-platform-palettes`.
