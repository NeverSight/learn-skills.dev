---
name: blender-vfx
description: Use when the user wants a game visual effect made in or exported from Blender, realistic or low-poly game-like - hit, slash, explosion, smoke, fire, magic, aura, shockwave, beam, trail, shield, lightning, glow, dust, destruction. Picks style and recipe, writes the FX spec with layers and routes to the vfx-* skills.
---
# VFX router + FX spec

## Requires
brief.md; `docs/blender/engine.md` section VFX; config.md (style, fx_style, platform).

## Inputs
Effect name | fx style (`fx=` or config.md `fx_style`) | trigger (loop / one-shot / on-hit) | duration | world size | palette | camera distance | platform.

## Steps
1. ENGINE: read engine.md VFX rows; mark each as [DOC], [RECALLED] or UNVERIFIED in the spec.
2. STYLE: fx_style = `fx=` argument, else config.md `fx_style`, else `style`. Read that column of `docs/blender/reference/vfx-styles.md` (shape language, alpha edges, colors, frames, triangles, motion).
3. RECIPE: find the effect in `references/cookbook.md`; take its layers and the style variant. No match: use the closest row and say which.
4. CLASSIFY with `references/effect-types.md`: choose the CHEAPEST type that reads at the camera distance: texture+mesh, then flipbook, trail, chunks, baked.
5. TIMING: effect-types.md section 2 [START] and the life curve: build 10-20 percent, peak 20-30, fade 50-70.
6. SPEC: copy `docs/blender/templates/fx-spec.md` to `blender-out/<fx>/FX_<Name>.spec.md`; fill type, style, trigger, duration, fps, palette, blend, the LAYERS table (each layer: kind, t-range, asset), engine recipe draft, budgets.
7. ROUTE: mesh -> blender-vfx-texture then blender-vfx-mesh; flipbook -> (blender-vfx-sim if volumetric and style is realistic) then blender-vfx-flipbook; trail -> blender-vfx-texture; chunks -> blender-vfx-sim; baked -> only if engine.md says supported, else flipbook.
8. PREVIEW: screenshots at t = 0, 0.1, 0.25, 0.5, 0.75, 1.0 of the lifetime, on a dark and a light background and at gameplay distance.
9. AUDIT: sub-skill audits; for every flipbook also `docs/blender/scripts/audit_fx_style.py` with STYLE set.
10. SHOWCASE (optional): blender-camera shot "vfx showcase" for a clean presentation render.

## Hard rules
| Rule | Detail |
|---|---|
| No Blender-only systems | particles, simulations, geometry nodes never ship: bake to textures/meshes + recipe |
| Style obeyed | vfx-styles.md limits (alpha edges, colors, frames, triangles) hold; low-poly and voxel use hard alpha and a tiny palette |
| Cheapest first | fewer, bigger, simpler shapes; overdraw is the main cost |
| Layers capped | pc 4-6, mobile 2-3 |
| Engine values | every engine value in the recipe is [DOC], [RECALLED] or UNVERIFIED |
| Readability | reads on dark and light backgrounds and at gameplay distance |
| Budgets | fx-mesh row in config.md; texture sizes per style table |

## Done when
Spec complete (every Engine recipe row filled or UNVERIFIED), assets pass their audits, style audit pass for flipbooks, readability screenshots saved.

## On fail
| Failure | Action |
|---|---|
| Engine cannot play the chosen type | next type in step 4 order |
| Looks muddy or inconsistent | vfx-styles.md section 4 fixes (cut colors, harden edges, match palette) |
| Peak too late or pops off | re-time the layers; audit_fx_style peak_position_ok / ends_clear |
| Unreadable | raise contrast and size, reduce layers, change blend |
| Over budget | simplify shapes, fewer frames, smaller textures |

## Next
blender-vfx-texture / -mesh / -flipbook / -sim, then blender-qa -> blender-export.
