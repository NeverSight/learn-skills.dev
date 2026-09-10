---
name: terrain-integrate
description: >-
  Grounds a finished build into the surrounding Minecraft Java world so it reads
  as belonging there, not dropped on — erodes an apron around the build's
  footprint while protecting the build itself, then re-materializes the apron to
  match the surrounding palette (the programmatic talus-skirt). Also naturalizes
  existing vanilla terrain. Runs as the required Integrate gate after any
  footprint-bearing build. Tier-3 leaf.
model: sonnet
effort: medium
context: fork
color: green
---

# terrain-integrate (Tier-3 leaf — the Integrate gate)

You remove the hard seam where a build meets untouched world. You are a forked
leaf: you receive the footprint (a `protect_box`) and the surrounding survey, and
you ground the build's edge. Read
`${CLAUDE_PLUGIN_ROOT}/reference/terrain/integration.md` (your method). This skill
is **GATE B** of the spine — every footprint-bearing build runs it before inspect.

## Method

1. **Footprint + survey ring.** Take the build's bounding box (`protect_box`) and
   survey a ring just outside it for the surrounding palette.
2. **Apron band.** Define a band of `apron_width` columns (8–24) outside the
   protect box; erosion strength tapers `smoothstep(0, apron_width, dist)` from
   full at the build edge to zero at the band's outer edge.
3. **Erode the apron, protect the build.** Thermal (+ light hydraulic) erosion
   over the apron only; the protect-box columns never change. Slumps the hard edge
   into a natural grade/talus.
4. **Re-materialize to the surrounding palette.** Grass tracks the new surface,
   rock on newly-steepened faces, sediment/beach where it filled, water re-flood
   to sea level; blend build-palette → surrounding-palette across the taper.
5. **Dry-run → check → apply.** ALWAYS run erosion with `dry_run: true` first.
   The dry-run returns height-delta stats (`max_delta`, `mean_abs_delta`,
   `moved`) — confirm the magnitude is sane (an apron slumps metres, not tens of
   metres) before re-running with `dry_run: false`. For a high-stakes seam, take
   the offline route instead (read → erode → `render_views` → apply) for a true
   visual pre-check. Under autonomy the dry-run check is the gate — no blind apply.

## Erosion tools (mod ≥ 0.4.0)

- **Thermal, synchronous — `block_erode_region`** (the default for aprons and
  foundations: deterministic talus collapse, sub-second). Region is `origin{x,z}`
  + `width`/`length` + `floor_y` (a column grid like `block_fill_columns`,
  ≤ 65,536 cols). Pass `protect_box{x0,z0,x1,z1}` = the build footprint, `apron` =
  taper width (the smoothstep band), `surface` + `subsurface` = the dominant
  surveyed blocks, and `dry_run: true` first.
- **Hydraulic, async — `block_erode_hydraulic_start` → `_status` → `_result`**
  (for naturalising larger/coarser terrain with carved drainage). `start` returns
  a `job_id`; poll `block_erode_hydraulic_status` until state is `DONE`, then read
  `block_erode_hydraulic_result`. Same `protect_box`/`apron`/`dry_run`; region
  default 256×256, hard cap 512×512 (tile larger client-side).
- **Offline route (any mod, or for a true visual pre-check):** read apron heights
  via `block_get_top_y`/`block_scan_region`, build a HeightField, `erode_thermal`
  + `blend.weld`/`pad_crop_smooth` over the apron in `tools/terrain`,
  `render_views` to verify, then materialise via `block_fill_columns` and repaint
  biomes with `level_fill_biome`.

**Current tool limits.** The server erosion tools re-cap with a single
`surface`/`subsurface` block and clear-above on lowered columns — they do not yet
infer a multi-block palette, expose rock on newly-steepened faces, or re-flood
water. For a seam that needs colour-blending, rock exposure, or water, use the
offline route (until the 0.4.x erosion-depth upgrade lands).

## Also: naturalize existing terrain

With no `protect_box`, the same flow naturalizes vanilla worldgen or a coarse
placement — read, erode, re-materialize from the *inferred* (sampled) palette.

## Carving a ledge into a wall: the sloped-back bench

A ledge cut for a path or wall-base rail is the same problem this skill exists to
fix — geometry that reads as unnatural where built work meets rock. Cutting a
plain horizontal tube into a vertical face leaves the rock above the cut
overhanging with nothing beneath it; it reads as "floating." Carve the ledge as a
**bench whose outward wall recedes ~0.85 blocks per block of height**, so the
wall slopes back above the cut with no overhang, while the canyon/valley side
stays open for the view. The receding wall is the talus principle applied to a
cut face: a slumped grade above, not a vertical lip.

One ordering caveat decides whether the bench survives the placement. **Run all
the carve/clear fills first, then all the ledge/rail fills** — never per-cell
`[clear, rail]`. A per-cell order lets cell `i+1`'s wider clear wipe cell `i`'s
just-placed ledge content before it sets, disconnecting the result along jogs and
turns.

```python
carves, fills = [], []
for cell in path:
    carves.extend(bench_clear(cell))   # ledge + sloped-back air (receding wall)
    fills.append(ledge_fill(cell))
batch(carves)   # ALL clears first ...
batch(fills)    # ... THEN all fills
```

Verify a carved bench in profile, not from iso: render a thin `view: side|front`
slab through it so the overhang (or its absence) and the receding wall are
visible — iso hides vertical faces. For batch caps and the separate silent-drop
hazard (`block_fill_batch` can drop a few entries from a large batch, so re-scan
a 1-wide feature after placing), see
`${CLAUDE_PLUGIN_ROOT}/reference/execution/engine-limits.md`. The rail mechanics
for a wall-base loop (boosters, square U-turns, continuity-patch) live in
`skills/system-transit`.

Return: the apron region, the erosion job summary, and a `seam` quality_contract
row so `exec-inspect` (GATE C) can confirm no hard build↔world edge remains.
