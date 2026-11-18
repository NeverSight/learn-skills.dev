---
name: schematica
description: "Schematica is a Python toolkit and interactive REPL for building Minecraft Java Edition schematics, exposed as an AI skill. Use this skill when the user asks to build, generate, design, or export Minecraft structures, schematics, .schem/.schematic/.litematic files, voxel maps, or 3D builds programmatically; when the user wants a procedural or creative toolkit for Minecraft builds; when the user mentions shapes, polygons, geometry, heightmaps, meshes, sessions, previews, Sponge schematics, MCEdit schematics, or Litematica; or when the user wants to script Minecraft map construction from Python or a REPL with undo/redo, block palettes, and multi-view PNG previews. Also use for tasks involving minecraft-data block catalogs, blockstate validation, trimesh/shapely geometry voxelization, Perlin terrain, or 3D-noise cave carving. Use for professional map design tasks: themed block palettes, terrain-draped roads/rivers, MST road networks, plazas, towers, battlements, bridges, ruins, lighting passes, seeded forests, and texture-derived block-color previews. The AI agent is the creative driver: it composes shapes, blocks, and generators from this toolkit to realize the user's request."
---

# Schematica - Minecraft Schematic Toolkit (AI Skill)

## Purpose

Schematica is a Python 3.11+ toolkit and interactive REPL for constructing
Minecraft Java Edition structures as 3D voxel grids and exporting them as
Sponge `.schem`, legacy MCEdit `.schematic`, or Litematica `.litematic` files.
It is packaged as an AI skill: the agent loading this skill becomes the
creative director, composing geometry primitives, shapely polygons, trimesh
meshes, heightmaps, boolean ops, transforms, and procedural generators into
the build the user asked for. A session model supports incremental appends,
undo/redo, block palettes, versioned block catalogs, and multi-view PNG
previews for the agent to verify its work.

Two storage backends are supported:
- **Dense** (`VoxelGrid`, default): a single contiguous `np.uint16` array. Best
  for small/medium builds (up to ~256³) where you want maximum speed and
  simplicity.
- **Chunked** (`ChunkedGrid`): sparse chunk-backed storage that only allocates
  chunks containing non-air voxels. Use for **big maps** (100+ chunks, terrain,
  full biomes) so memory cost scales with built volume, not grid extent. A
  160×64×160 map with a 20-voxel cube uses 12 chunks (~98 KB) instead of 3.2 MB
  dense; a 1600×320×1600 mega-map is addressable without OOM.

## Map design quality standard

Treat every map request as a professional design task, not a quick primitive
demo. A useful schematic should look intentional from multiple views, include
scale-aware composition, and carry enough detail to meet veteran Minecraft map
design expectations.

Before building, define the map's purpose, target Minecraft version, scale,
theme, layout, landmarks, player paths, sightlines, terrain treatment, and
material palette. Use the full block catalog available for the target version:
solid blocks, slabs, stairs, walls, fences, gates, panes, trapdoors, doors,
carpets, lights, foliage, fluids, and blockstate variants when supported. If the
requested version or fallback registry does not support a detail block, choose a
version-valid substitute instead of emitting an invalid blockstate.

Use texture hacks deliberately: weighted material mixes, noise-driven texture
palettes, dithering, gradients, mossy/cracked/weathered variants, orientation
changes such as log axes or stair/slab facing, thin overlays such as carpets,
trapdoors and panes, and WFC/replace/retexture passes. These are visual tricks
built from real blocks and valid blockstates, not fake texture names.

For real maps, prefer layered detail over large flat fills: varied materials,
trim, depth changes, supports, roofs, edges, gradients, organic terrain,
landscaping, lighting, interiors, roads, signage, and negative-space carving.
Verify with previews from top/front/right/iso views and revise weak silhouettes,
empty areas, repetitive surfaces, or unresolved transitions before exporting.

## When to use this skill

Trigger this skill whenever the user:

- Asks to "build", "generate", "design", or "export" a Minecraft structure, schematic, `.schem`, or voxel map.
- Wants a programmatic / scripted Minecraft map builder.
- Mentions shapes: box, sphere, cylinder, dome, cone, pyramid, torus, ellipsoid, helix, arch, staircase, spiral, line, wedge, plane, polygon, mesh, heightmap.
- Mentions hollow shapes or WorldEdit-style `hsphere`/`hcyl`/`hbox` shortcuts.
- Mentions booleans (union/subtract/intersect/xor) or transforms (rotate/mirror/array/noise-deform/shell).
- Wants previews / screenshots of a build from top/front/right/iso views.
- Wants to use minecraft-data block catalogs with per-version blockstate validation.
- Asks for procedural terrain, trees, villages, or other generated structures.
- Needs a session-based workflow: "create session, append shape, undo, export".

Do **not** use this skill for Minecraft Bedrock, runtime world editing via
protocol packets, or rendering/export of `.mcstructure` (Bedrock). The toolkit
targets Java Edition schematic-style files, not live server/world mutation.

## Big-map support (chunked backend)

For maps spanning 100+ chunks (terrain, biomes, large settlements), create
the session in chunked mode. Only chunks containing non-air voxels are
allocated; shape `add`/`subtract`/`paint` evaluate the mask chunk-by-chunk
using each shape's `bounds()` so per-op cost scales with touched chunks, not
total grid volume. The Sponge exporter streams chunked grids without ever
materialising a full dense array.

```python
# Library
s = Session.new((160, 64, 160), chunked=True, chunk_size=16)
```
```
# CLI
session.new size=160x64x160 chunked=true chunk_size=16
```

`stats` reports `chunks`, `chunk_size`, and `memory_bytes` for chunked
sessions. The dense and chunked backends produce byte-identical `.schem`
output for the same build (verified by `test_export_chunked_matches_dense`).

## How to use this skill

### Install the toolkit (bundled)

The skill ships the `scripts/schematica/` Python package as its bundled
toolkit, with install metadata in `scripts/pyproject.toml`. From the
`scripts/` directory, install it editable plus dev deps:

```bash
cd scripts
pip install -e ".[dev]"
```

Or install runtime deps only from `scripts/requirements.txt`:

```bash
pip install -r scripts/requirements.txt
```

Optional extra (amulet-core multi-format backend, Python 3.11-3.13 only):

```bash
cd scripts
pip install -e ".[amulet]"
```

For full per-version block catalogs (instead of the built-in fallback), vendor
the PrismarineJS minecraft-data repo into the skill root, which is the
directory containing `SKILL.md`:

```bash
git clone https://github.com/PrismarineJS/minecraft-data minecraft_data
# or set SCHEMATICA_MINECRAFT_DATA to any minecraft-data clone path
```

Alternatively, use the bundled downloader to fetch a single version's
`blocks.json` on demand (no git clone required, stdlib `urllib` only):

```bash
python -m schematica.blocks.download 1.20.1          # fetch + cache blocks.json
python -m schematica.blocks.download --list          # list upstream versions
python -m schematica.blocks.download 1.20.1 --force   # re-download
```

The downloader writes to `<cache_root>/data/pc/<version>/` (same layout the
registry loader searches), so a successful download is immediately visible to
`BlockRegistry.for_version` without any further setup.

The loader checks `SCHEMATICA_MINECRAFT_DATA`, then `<skill_root>/minecraft_data`,
then `scripts/minecraft_data`. Without a full catalog it uses a fallback block
list that covers common structural blocks plus colored wool, stained glass,
terracotta, and concrete.

### Version and legacy caveats

- Modern Java versions (1.13+) work best because Sponge and Litematica use
  flattened blockstate strings such as `minecraft:red_wool`.
- Pre-flattening targets (1.7-1.12, including 1.8) use numeric IDs plus metadata.
  Use `export.mcedit` / `write_mcedit` for legacy colored blocks because it
  writes common metadata values for wool, stained glass, terracotta, concrete,
  stone variants, planks, logs, and red sand.
- Sponge export warns when `data_version < 1451` and the palette contains modern
  flattened names or blockstate properties. Treat that warning as a signal to
  switch to MCEdit or target a post-1.13 data version.

### Live data & configuration (no hardcodes)

Package data is bundled as editable JSON and resolved live:

| What | Bundled file | Override |
|---|---|---|
| Fallback block catalog | `scripts/schematica/blocks/data/fallback_blocks.json` | `SCHEMATICA_FALLBACK_BLOCKS` |
| Preview block colors (~987, texture-derived) | `scripts/schematica/data/block_colors.json` | `SCHEMATICA_BLOCK_COLORS` |
| Design palettes + tree kinds | `scripts/schematica/data/design_palettes.json` | `SCHEMATICA_PALETTES` |
| Default MC version | `1.20.1` | `SCHEMATICA_MC_VERSION` |

`python -m schematica.blocks.download <version>` fetches a live full block
catalog; `python -m schematica.blocks.colors <version>` fetches that version's
true texture colors for previews. Both cache under the minecraft-data root.

### Two entry points

1. **Library API** — import and script directly. See `references/library_api.md`.
2. **REPL / script mode** — `python -m schematica` for interactive, or
   `python -m schematica --script build.txt` for batch. See `references/cli_reference.md`.
   Set `PYTHONPATH=scripts` (or `pip install -e scripts/`) so the package resolves.

### Choosing CLI vs code (read `references/workflow_guide.md` for detail)

**Prefer the CLI** when the build uses only registered commands (box, sphere,
cylinder, dome, helix, arch, staircase, clone.translate, clone.cardinal,
subtract, paint, replace, etc.). The CLI has a validation layer that catches
inverted bounds, negative radii, unknown blocks, and other common mistakes
before they execute. It is the fastest and safest path for structural builds.

**Switch to Python** when the build needs:
- Loops or conditionals beyond simple clone repetition/symmetry (e.g. "place 20 trees at random positions")
- Procedural generation (`apply_terrain`, `apply_tree`, Perlin noise)
- Custom shapes not in the command table (fractals, WFC, `NoiseDeformed`)
- Mesh import (`load_mesh("model.obj")`)
- Polygon extrusion (`extrude_polygon(shapely_polygon, ...)`)

**Use inline `-c`** only for quick one-liners and sanity checks.

**Hybrid**: build structure in CLI → `save` session → `load` in Python for
procedural detail. This combines CLI validation with Python flexibility.

### Core workflow

1. Create a `Session` with a target grid size and MC version.
2. Append/erase shapes via `session.add(shape, block)` / `session.subtract(shape)`.
3. Replace, paint, transform, undo/redo as needed.
4. Render previews with `preview(grid, out_dir)`.
5. Export Sponge, MCEdit, or Litematica schematics with the matching writer.
6. Save/load the full session (grid + palette + history) as JSON.

### Key references

Load these on demand for detailed information:

- `references/design_playbook.md` — **read this for any real map request**: composition, palette/color theory grounded in live texture data, roads/rivers/roofs/forests workflow, detailing order, and the preview-driven verification loop.
- `references/advanced_techniques.md` — pattern/mask language (WorldEdit-grounded), WFC C1/C2 usage theory, and a goal->tool recipe table.
- `references/workflow_guide.md` — **read this first before building**: CLI vs Python vs inline decision tree, advanced recipes for each mode, hybrid workflow, verification steps.
- `references/agent_cli_guide.md` — **read this if driving the CLI**: execution pattern, argument rules, real captured output, error recovery, anti-patterns, validation codes.
- `references/architecture.md` — full module layout, data model, design choices.
- `references/library_api.md` — every public class/method with examples.
- `references/cli_reference.md` — full command table and REPL usage.
- `references/shapes_catalog.md` — every shape, its args, and mask semantics.
- `references/generators.md` — procedural generator recipes (terrain, trees).
- `references/sponge_format.md` — Sponge `.schem` v2 NBT layout and encoder details.
- `references/block_registry.md` — minecraft-data loading, fallback catalog, blockstate strings.
- `references/preview_rendering.md` — matplotlib voxel renderer and per-block colors.
- `references/roadmap.md` — phases done vs remaining.

### Bundled toolkit (scripts/)

`scripts/schematica/` is the toolkit (not a reference doc). Run it; do not read
it into context unless patching. Key modules:

- `schematica.blocks` — `Block`, `BlockRegistry`, `BlockDef`, `BlockStateSchema`; `schematica.blocks.download` — on-demand minecraft-data fetcher; `schematica.blocks.colors` — texture-derived block-color fetcher (`python -m schematica.blocks.colors <version>`)
- `schematica.design` — themed palettes; terrain-draped paths/rivers; gable/hip roofs; trees/forests; layout (`apply_flatten`, `apply_plaza`, `apply_road_network`); buildings (`apply_tower`, `apply_battlements`, `apply_bridge`); decay (`apply_ruin`); lighting; cave carving. Data-driven from `schematica/data/design_palettes.json`
- `schematica.patterns` — WorldEdit-style weighted pattern parser (`parse_pattern`) used by `replace.mix`
- `schematica.config` — `default_version()` (env `SCHEMATICA_MC_VERSION`); `schematica.resources` — env-overridable JSON data loading
- `schematica.core` — `VoxelGrid`, `Palette`, `ChunkedGrid` (sparse big-map backend)
- `schematica.shapes.primitives` — `Box`, `Sphere`, `Ellipsoid`, `Cylinder`, `Cone`, `Pyramid`, `Torus`, `Dome`, `Helix`, `Arch`, `Spiral`, `Staircase`, `Plane`, `Wedge`, `Line`, `BezierCurve` (16 shapes)
- `schematica.shapes.boolean` — `Union`, `Intersect`, `Subtract`, `Xor`
- `schematica.shapes.transforms` — `Translated`, `Mirror`, `Rotated90`, `Rotated` (arbitrary angle), `Array`, `NoiseDeformed`, `Shell`
- `schematica.shapes.sdf` — `SDFShape`, `SmoothUnion`, `SmoothIntersect`, `SmoothSubtract` (signed-distance-field blending)
- `schematica.shapes.polygon` — `Extrude`, `extrude_polygon` (shapely + SVG path ``d`` strings)
- `schematica.shapes.mesh` — `MeshShape`, `load_mesh` (trimesh-backed)
- `schematica.shapes.heightmap` — `Heightmap`, `from_image`
- `schematica.generators` — `perlin2d`, `fbm2d`, `apply_terrain`, `apply_tree`, `terrain_heightmap`; `schematica.generators.wfc` — `WFC`, `Tile`, `TileSet`, `run_wfc`, `tileset_wildcard` for caller-generated palettes
- `schematica.render.preview` — `preview` (PNG previews)
- `schematica.export.sponge` — `write_sponge` (`.schem` writer)
- `schematica.export.mcedit` — `write_mcedit` (legacy `.schematic` writer)
- `schematica.export.litematic` — `write_litematic` (`.litematic` writer)
- `schematica.session` — `Session`, `History`, `CommandSpec` (40+ commands); Session supports `enable_symmetry`/`disable_symmetry` (live mirror), `enable_radial_symmetry`/`enable_quad_symmetry` (live rotational cloning via `Rotated90`), and `resample_subregion` (scale a sub-box to a new size).
- `schematica.cli.repl` — `dispatch`, `run_script`, `repl_main`
- `schematica.cli.validation` — `CheckResult` + 29 `check_*` functions

### Concrete examples

#### Example 1 — "Build a 24x24 stone plaza with a glass dome and a log pillar"

Library:

```python
from schematica.session.session import Session
from schematica.shapes.primitives import Box, Sphere, Cylinder

s = Session.new((24, 24, 24), version="1.20.1")
s.add(Box(0, 0, 0, 23, 0, 23), "minecraft:stone")
s.add(Sphere(12, 14, 12, 5), "minecraft:glass", )  # dome
s.add(Cylinder(12, 1, 12, 1.0, 0, 8), "minecraft:oak_log")
from schematica.export.sponge import write_sponge
write_sponge(s.grid, "plaza.schem")
```

REPL script (`plaza.txt`):

```
session.new size=24x24x24 version=1.20.1
add.box frm=0,0,0 to=23,0,23 block=minecraft:stone
add.sphere center=12,14,12 r=5 block=minecraft:glass
add.cylinder center=12,1,12 r=1 h=8 block=minecraft:oak_log
export path=plaza.schem
preview out_dir=previews
```

Run: `python -m schematica --script plaza.txt`

#### Example 2 — "Carve a tunnel through a hill and replace dirt with grass"

```python
s = Session.new((32, 32, 32))
from schematica.shapes.primitives import Box
from schematica.generators.templates import apply_terrain
apply_terrain(s, seed=42, amplitude=6)
s.subtract(Box(0, 8, 15, 31, 14, 17))   # horizontal tunnel
s.replace("minecraft:dirt", "minecraft:grass_block")
```

#### Example 3 — "Extrude a star polygon into a brick tower"

```python
from shapely.geometry import Polygon
from schematica.shapes.polygon import extrude_polygon
from schematica.session.session import Session

star = Polygon([(5,0),(6,3),(10,3),(7,5),(8,9),(5,7),(2,9),(3,5),(0,3),(4,3)])
shape = extrude_polygon(star, origin=(0,0,0), extrude_axis="y", length=12)
s = Session.new((12, 12, 12))
s.add(shape, "minecraft:bricks")
```

#### Example 4 — "Voxelize an OBJ model into the grid"

```python
from schematica.shapes.mesh import load_mesh
from schematica.session.session import Session
shape = load_mesh("castle.obj", origin=(0,0,0), scale=1.0)
s = Session.new((64, 64, 64))
s.add(shape, "minecraft:stone_bricks")
```

#### Example 5b — "Terrain + road + river + house + forest (design CLI)"

```
session.new size=64x28x64 version=1.20.1
generate.terrain seed=11 amplitude=5
road points=4,4;28,16;60,56 width=3 palette=rustic_oak border=minecraft:oak_log smooth=4 seed=2
river points=2,40;30,34;62,46 width=3 depth=3 bed=minecraft:gravel smooth=4
add.hbox frm=24,12,24 to=36,22,36 block=minecraft:stone_bricks
roof.gable frm=24,22,24 to=36,22,36 axis=x palette=medieval_stone stairs=minecraft:stone_brick_stairs
paint.ramp palette=deepslate_dungeon frm=24,12,24 to=36,22,36 axis=y blend=0.15
forest frm=2,0,2 to=20,0,20 density=0.05 kinds=oak+birch seed=4
surface x=24 z=24
preview out_dir=previews
export path=town.schem
```

#### Example 5 — "Build a castle with hollow walls, towers, and staircase (CLI)"

```
session.new size=32x32x32
add.hbox frm=2,1,2 to=29,12,29 block=minecraft:stone
add.hcylinder center=2,1,2 r=2 h=16 block=minecraft:stone
add.hcylinder center=29,1,2 r=2 h=16 block=minecraft:stone
add.hcylinder center=2,1,29 r=2 h=16 block=minecraft:stone
add.hcylinder center=29,1,29 r=2 h=16 block=minecraft:stone
add.dome center=2,17,2 r=2 block=minecraft:purple_stained_glass
add.dome center=29,17,2 r=2 block=minecraft:purple_stained_glass
add.dome center=2,17,29 r=2 block=minecraft:purple_stained_glass
add.dome center=29,17,29 r=2 block=minecraft:purple_stained_glass
add.staircase corner=4,1,4 y1=12 step_width=2 step_depth=1 axis=x block=minecraft:oak_planks
subtract.box frm=14,1,2 to=17,5,2
add.arch center=15,6,2 z0=2 z1=2 r=3 block=minecraft:stone
stats
export path=castle.schem
preview out_dir=castle_previews
```

#### Example 6 — "Noise-deformed boulder and hollow shell (Python)"

```python
from schematica.session.session import Session
from schematica.shapes.primitives import Sphere
from schematica.shapes.transforms import NoiseDeformed, Shell
from schematica.export.sponge import write_sponge

s = Session.new((24, 24, 24))
boulder = NoiseDeformed(Sphere(12, 12, 12, 6), amplitude=3, scale=0.15, seed=42)
s.add(boulder, "minecraft:stone")
# Add a hollow obsidian shell around it
shell = Shell(Sphere(12, 12, 12, 8), thickness=1)
s.add(shell, "minecraft:obsidian")
write_sponge(s.grid, "boulder.schem")
```

### Important conventions

- **Coordinate system**: `grid[x, y, z]` with `y` up. Shape `mask(shape)`
  returns a boolean numpy array of the target grid's shape. Shapes also
  implement `bounds(grid_shape)` returning the inclusive bbox where their mask
  could be True, enabling the chunked backend to skip untouched chunks.
- **Palette index 0 is always air**; an all-zero grid is empty.
- **Blockstate strings**: `minecraft:oak_log[axis=y]`. `Block.parse` round-trips
  them. `BlockRegistry.resolve` strictly validates keys/values and fills
  defaults; `validate` rejects unknown explicit states.
- **Bulk drawing**: for generated maps with many cuboids or point details, prefer
  `Session.set_box(...)` and `Session.set_many(...)` over thousands of tiny
  shape operations.
- **No async**: the whole pipeline is synchronous (numpy + nbtlib + matplotlib).
