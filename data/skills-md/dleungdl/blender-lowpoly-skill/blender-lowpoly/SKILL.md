---
name: blender-lowpoly
description: Use this when making low-poly assets in Blender, either through Blender MCP or by writing a bpy script.
metadata:
  version: "2.6.0"
  type: workflow
---

English · [繁體中文](SKILL.zh-Hant.md)

# blender-lowpoly

Guidebook for an LLM making **low-poly** game assets in a live or scripted Blender session.

The look to hit: **visible facets, Shade Flat, solid colors, no PBR textures**. Build from primitives. Check with a four-view turnaround (front, side, 3/4, top).

## Path

1. If Blender MCP tools are available (`get_scene_info`, `execute_blender_code` / `execute_code`, viewport screenshot): use MCP.
2. Otherwise write a self-contained `bpy` script the user can run in Blender (Scripting workspace or `blender --python`).

Do not mix the two in one step. Say which path you are using.

## Loop

```
inspect scene
  → pick construction language (kit OR faceted-organic)
  → blockout from primitives (silhouette first)
  → four-view check
  → shade flat + color slots
  → origin, apply rot/scale, export
```

Never invent scene state. Only trust tool output or script prints.

## Two construction languages

Pick one per asset. Do not mix in the same mesh.

### A. Kit (hard-edge primitives)

Cubes and cylinders, **no bevel**, **no subdivision**, **no vertex jitter**. Repeat with Array. Used for rails, posts, stadiums, crowd-as-blocks, boxes.

- One cube = one part.
- Posts / crowd / repeating bays: Array modifier, then apply only at export if the engine will not evaluate it.
- 2–4 material slots. Color whole objects, not faces, unless two colors share one mesh.

### B. Faceted organic

Large visible tris/quads. Shade Flat so lighting breaks on every face. Used for trees, hedges, rocks, stylized animals.

- Start from a cube, cone, or 6–8 sided cylinder. Not a high-poly sphere you then decimate as the first idea.
- Silhouette from the **side view** first, then add volume in 3/4.
- Vertex jitter only on foliage / rocks (small, uniform). Never jitter kit parts.
- Anatomy is planes and angle changes (knee = a bend), not extra edge loops.
- Color by **material slot / face assignment** (body, mane, blaze, hoof). No image textures.

Recipes: [references/lowpoly-build.md](references/lowpoly-build.md)

## Reverse-engineering lesson (horses)

Measured horse GLBs taught this. Do not skip it.

- **Materials are not parts.** Compact Horse has two slots whose islands span almost the whole animal. Bounding-box reverse-eng from slots produces two giant cubes, not a horse.
- **Anatomy lives in the mesh and bones**, then you paint slots. Side-view volumes first (body, neck, head, four legs, mane slab, tail slab). Weld to **one mesh**. Then assign faces to 2–3 (compact) or 5–8 (detailed) slots.
- Compact Horse: 1436 verts, 690 tris, 2 slots, 28 bones. Dark slot is mane / tail / hooves / blaze painted across the same mesh.
- Detailed Horse: 4400 verts, 2182 tris, 8 slots (`Main`, `Hair`, `Main_Dark`, `Muzzle`, `Hooves`, `Main_Light`, `Eye_Black`, `Eye_White`), 50 bones. White Horse is the same mesh with different albedo (no `Main_Dark`).
- No UVs, no image textures. Origin `(0,0,0)`, feet on Z=0.
- Exact Idle-pose dumps (ground truth, not a modeling recipe): [horse_compact.py](references/scripts/horse_compact.py), [horse_detailed.py](references/scripts/horse_detailed.py), [horse_white.py](references/scripts/horse_white.py). Use them to check a result, not as the way to build.



## Distill, don't dump

Reverse-eng a decimated AI mesh is **knowledge distillation**, not a vertex copy.

- Extract DNA as a **parameterized procedure** (knobs), not a vertex array and not the cleanest CAD cube that still reads as the object.
- For this hedge the look *is* irregular tris. Knobs include `collapse_faces` and `fractal`. A cube+bevel-only mesh is too clean.
- Still do **not** dump GLB verts. [hedge.py](references/scripts/hedge.py) rebuilds the look from knobs (~292 verts / 521 faces).
- Same rule as horses: Idle vertex dumps check a result; they are not how you model.

Hedge DNA: cube scale ~2.8 × 0.95 × 1.1, bevel 0.2 / 4, subsurf 2, displace 0.028, collapse toward 200 faces, fractal 0.28 on leftover large faces, sage `(0.40, 0.46, 0.28)`, Shade Flat, no UV, origin `(0,0,0)`, sit on Z=0.

## Four-view check (required)

After blockout and after materials, screenshot or print so these four read clearly:

| View | What to verify |
|---|---|
| front | symmetry, width, color splits (blaze, posts) |
| side | silhouette, taper, joint angles, overhangs |
| 3/4 | volume, facet lighting, parts not intersecting |
| top | footprint, array spacing, nested foliage tiers |

If a view looks like a different object, the silhouette is wrong. Fix verts, do not add loops.

## Defaults (unless the user overrides)

- Low-poly, hard edges, **Shade Flat**. No Auto Smooth. No Subdivision Surface.
- Quads while blocking kit parts. Faceted organic may be tris; that is the look.
- Silhouette from geometry. No extra loops on flat planes.
- Flat Principled (roughness 1, metallic 0) or Emission. No PBR stack, no image textures.
- Origin at ground contact or at the modular tile hinge.
- Metric units, scale 1.0 unless the open file already differs.
- Export **selected** as glTF/GLB (FBX only if asked). Report the absolute path.
- Poly budget unless specified: kit prop 20–400 tris; foliage/rock 80–800; crowd-filler person 8–20.
- Stylized animals: **one welded mesh**, no UVs/textures, origin (0,0,0), feet on Z=0. Two tiers — pick one and say which:
  - **Compact:** 560–1400 tris, 2–3 material slots, 24 or 28 bones. Idle / Jump / Walk / Run.
  - **Detailed:** 1800–2500 tris, 5–8 slots (Main, Main_Light, Hair, Hooves, Muzzle, Eyes), ~42–51 bones. Gallop, Eating, Attack, extra Idles.
  Default to compact unless the user wants Gallop / Attack / split eye-hoof-muzzle colors. Prefer a detailed **GLB** over an FBX of the same pack (FBX often imports Principled Alpha=0).

## Naming

Use the names the user gave. If none, pick clear English names and say what you picked. Do not invent a project prefix (`SM_`, `COL_`, …) unless they asked for one.

## MCP rules

- First action every session: list live tools, then `get_scene_info`.
- If connect fails, stop. Tell the user to: open Blender → enable addon **Interface: Blender MCP** → `N` panel → **Start MCP Server** (default `localhost:9876`) → one MCP client only.
- One intent per `execute_*` call. Always `import bpy`. Do not reuse locals from a previous call.
- Return a short dict (names, counts, paths). Never dump vertex arrays.
- After Edit Mode ops, return to Object Mode in the same snippet.
- Set the object selected and active before object ops.
- Screenshot after each meaningful visual change. Prefer a four-view sheet for the final check.
- Tool names vary by fork (`bm_` prefix, `execute_code`, …). Bind by capability, not exact string.

## bpy script rules

- One self-contained file. Same safety and return-summary rules as MCP snippets.
- Print a short dict at the end: `{ok, names, verts, faces, path}`.
- No modal operators. Keep runtime to a few seconds unless the user asked for a render.

## Safety

- Never `bpy.ops.wm.quit_blender()`.
- Never `read_homefile`, wipe collections, or delete unnamed user work without asking.
- Never fetch remote Python. Never read credentials from disk.

## Report back

- Construction language used (kit or faceted-organic)
- Objects created or changed
- Approx verts / faces
- Material names and colors
- Export path if any
- What the four-view sheet shows (silhouette / obvious errors)
- One next-step suggestion
