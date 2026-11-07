---
name: roblox-map
description: "Build Roblox maps, terrain, levels, and arenas from JSON specifications. Prove reachability, falls, sightlines, placement, and budgets before emitting geometry and Studio build artifacts. Use for level generation or layout validation."
---

# Roblox maps, headless

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

A map is not a pile of parts. It is a **playable volume**, and the only
questions worth automating about it have right answers: can you get there, can
you get back, can you see across it, how long do you fall.

```
map.json
  -> resolve to ONE tree
       |-> plan.png     annotated top-down + elevation, drawn from the tree
       |-> prove        P checks (parts) + T checks (terrain), from raycasts and the movement profile
       |-> terrain/     heightfield, material map, preview (terrain maps)
       |-> build.lua    execute_luau, small maps
       |-> map.rbxmx    Insert from File, large maps
       |-> serve_map    HTTP payload for scripts/luau/build.lua (parts, meshes, terrain, tide)
  -> Studio -> verify the PLACE -> playtest the spawn -> look
```

The plan, the report and every builder come from the same resolved tree. The
preview cannot disagree with what ships.

**Scope.** This skill makes and proves the layout: greybox parts, terrain,
spawns, boundaries, lighting presets. It does not make props, buildings, trees
or textures. Place your own models in the spec as parts that carry a `mesh`
name (see "Meshes: placing your own"), or generate them with the separate
`roblox-3d-model` skill. Greybox is the stage the prover is for: prove the
layout first, then dress it.

Needs Python 3 with `numpy`, `scipy` and `Pillow`. The Studio steps use the
Roblox Studio MCP (`execute_luau`).

---

## Quick start

```bash
python scripts/prove.py minimal                         # START HERE: the smallest valid spec, copy it for your own
python scripts/prove.py sky_citadel                     # check a spec: under a second, no Studio
python scripts/plan.py  sky_citadel --prove -o plan.png # look at it
python scripts/build_map.py meadow_island               # prove + plan + terrain, into work/MeadowIsland/
python scripts/build_map.py sky_citadel --serve         # ...then serve it to Studio and print the bootstrap
python scripts/emit.py  duel_arena --lua build.lua      # small map, paste into execute_luau
python scripts/emit.py  duel_arena --rbxmx Arena.rbxmx  # large map, Insert from File
python scripts/verify_map.py                            # self-test: sabotage a map, the prover must catch it
python scripts/checks_terrain.py --selftest             # self-test the terrain checks
```

A spec is found by path, or by name in `specs/`. The shipped specs:

| Spec | What it shows |
|---|---|
| `specs/minimal.json` | the smallest valid spec: two decks and a jumpable gap. WARNs only on P11 (empty space), which is expected for a test map. Copy this to start |
| `specs/sky_citadel.json` | a greybox sky arena: floating islands, a raised plaza, stair bridges, towers. PASSes |
| `specs/meadow_island.json` | a TERRAIN map: island, beaches, terraces, mesa, a graded road to a flattened pad, a swim-only islet. WARNs on T8 (no cliff panels on the steep rim, since this free version ships no dressing) |
| `specs/duel_arena.json` | a wall-running knockback arena on a custom movement profile. FAILs P9 on purpose (read its FIX line); it is the `verify_map.py` baseline |

`prove.py` exits 0 on PASS and 1 on WARN or FAIL, so read the RESULT line, not
the exit code. Prove first. It runs in under a second with no Studio, so there is no reason to
build a map you have not checked.

---

## The one thing to understand first

**Do not use PathfindingService to decide whether a map is walkable.**

Measured against a live Studio edit session:

| Probe | Result |
|---|---|
| 1.5-stud step | `Success`, 39 waypoints |
| 3.0-stud step | `Success`, 39 waypoints |
| **12-stud unclimbable wall** | **`Success`, 39 waypoints** |
| empty void, nothing to stand on | `NoPath` |
| solid wall across the route | `NoPath` |
| **wide-open doorway** | **`NoPath`** |

The edit-mode navmesh lags geometry edits by more than two seconds and does not
reliably rebuild, so it will tell you a wall is walkable and a corridor is not.
A confident pass on an unclimbable wall is precisely the failure this skill
exists to prevent. Reachability is therefore computed here from raycasts and the
movement profile. Raycasting in edit mode is exact and was verified the same
session (`HIT Ground y=0.00`).

---

## The spec

Geometry plus **intent**. Intent is what makes the prover possible: without it
the only question available is "is this map good", which has no answer.

```json
{
  "name": "DuelArena",
  "profile": "wallrun_example",
  "ground_is_parts": "a floating sky arena: the deck IS the movement design",
  "volume": { "bounds": [[-110,-40,-110],[110,80,110]],
              "killPlane": -40, "ringOutOffset": 10, "lift": 8 },
  "parts": [
    { "id": "Deck", "size": [140,12,140], "pos": [0,-6,0],
      "roles": ["arena_floor","wallride","ringout_edge"] },
    { "id": "Ramp", "size": [20,26,40], "pos": [0,13,-40], "ramp": "+z",
      "roles": ["core_access"], "grounded": true },
    { "id": "Ledge", "size": [26,3,14], "pos": [78,-15.5,0], "ring": 4,
      "roles": ["crouch_anchor","pocket"] }
  ],
  "spawns": [[0,0,55]],
  "anchors": { "grapple": ["Spine","Post*","Core"] },
  "intent": {
    "reachable": ["Deck","Ramp","Core","Ledge*"],
    "transit": ["Post*"],
    "reachableOnlyBy": { "Spine": "recoil", "Outrigger*": "grapple" },
    "ringOut": { "counterplay": "grapple", "minWindow": 1.0,
                 "from": ["Deck","Ledge*"] }
  },
  "sightlines": { "minClearFraction": 0.30, "maxClearFraction": 0.85 }
}
```

- **`roles` is mandatory.** A part with no declared role is rejected at resolve
  time, not flagged later. This is the "what is this ramp doing in here" defect
  made unrepresentable.
- **`ring: N`** rotates N copies about the map's Y axis (through the origin).
  Symmetry becomes a property of the spec rather than something to remember.
- **`ramp: "+z"`** makes a WedgePart. Measured in Studio: a WedgePart's surface
  rises along its own local **+Z** and is flat across X. Other axes are emitted
  by rotating and swapping the X/Z extents.
- **`transit`** marks a part whose top is not a destination - a post you
  wall-ride, a wall you climb. Without it the prover judges its 4x4 top as a
  floor and complains that nobody can stand there.
- **`reachableOnlyBy`** names the tech a surface is gated behind. If that tech
  is not in the movement profile the prover reports **UNVERIFIABLE**, never PASS
  and never FAIL.

Optional part keys: `yaw`, `shape` (`block`, `cylinder` upright, `ball`),
`material`, `color`, `themeRole` (takes colour and material from the spec's
`theme`), `solid`, `visible`, `grounded`, `decor` (greeble: real for raycasts,
never a destination), `barrier` (an invisible boundary wall, P16), `facing`
(door direction, P12), `terrainWater` + `lobes` + `organic` (a lobed terrain
water body, P14), `mesh` + `meshScale` + `biome` (place one of your models, P21),
`dressing_exempt` (with a reason, P13).

**Stairs.** `{"id": "Stair", "kit": "stairs", "roles": [...], "params": {"pos":
[x, y, z], "rise": 14, "run": 22, "width": 16, "step": 1.5, "yaw": 0}}` builds
half-height treads, each extruded to the base, climbing toward local +Z (`yaw`
180 climbs toward -Z). The resolver refuses a `step` above the profile's
auto-step, because every step would be an unclimbable ledge. `stairs` is the
only built-in kit; write everything else as plain parts.

Spec-level opt-outs, each needing a written reason and never allowed by silence:
`ground_is_parts` (see "Ground is terrain"), `parts_are_deliberate` (see "Mesh
first"), `open_edges` (a map with no boundary wall, P16).

---

## The movement profile

`profiles/<name>.json`. `default` is stock Roblox R15 (gravity 196.2, jump apex
6.37); `wallrun_example` is a custom-movement game at gravity 120 with wall
climb, wall jump, slide jump and trimp. Copy one and fill in your own game's
numbers. Every value carries a `src`:

| src | meaning |
|---|---|
| `config` | read straight out of the game's own config file |
| `derived` | computed from a config value plus physics, working shown |
| `measured` | produced by `scripts/luau/calibrate.lua` in a real playtest |
| `assumed` | **not verified** - the report lists these every run |
| `design` | a design intent, not a fact about the running game |

Abilities carry `shipped`. An ability with `shipped: false` is design intent
only, and anything depending on it comes back UNVERIFIABLE. That is how the
duel arena's grapple, dash and double jump are handled: they are in the arena
design and not in the game's movement config.

Run `scripts/luau/calibrate.lua` as a LocalScript in play mode to replace the
assumed values with measured ones. It reports through `print`, because
LogService via the playtest output is the only channel out of a running game
the MCP can read. The derivations, the stairs number and the ring-out
arithmetic are in `references/movement-numbers.md`; layout guidance (POI
spacing, landmarks, cover) is in `references/map-design.md`.

---

## The checks

`prove.py` runs every P check on every map, and the T checks on any spec with a
`terrain` block.

| | Check | Catches |
|---|---|---|
| P1 | Grounding | a platform declared grounded that floats |
| P2 | Standable surface | a top face with nowhere to actually stand |
| P2b | Recovery margin | a return climb that spends the whole wall budget |
| P3 | Intent match | unreachable high ground, **reachable-but-undeclared**, pockets with no way out |
| P4 | Anchor legitimacy | anchors that are invisible, non-solid, or out of range |
| P5 | Sightlines | an arena too enclosed to duel in or too open to hide in |
| P6 | Overlap | interpenetrating parts |
| P7 | Role coverage | a shipped movement tech with nowhere to use it |
| P8 | Symmetry | a ring of congruent parts that is not evenly spaced |
| P9 | Ring-out counterplay | a fall shorter than the ragdoll it is supposed to allow you to recover from |
| P10 | Coplanar surfaces | two overlapping faces at one height (they flicker) |
| P11 | Empty space | too much of the map with nothing within reach |
| P12 | Entrances | a door that faces nothing you can walk to |
| P13 | Feature dressing | a landmark or water body with a bare edge |
| P14 | Props in water | a prop standing in a lake |
| P15 | Clear routes | a prop blocking a declared route |
| P16 | Enclosure | a boundary with a gap, a barrier you can hop, or no boundary and no `open_edges` reason |
| P21 | Performance budget | too many unique meshes or textures per biome, a mesh over its triangle class budget, too many instances or shadow casters |

**Reachability is tri-state and must stay that way.** Any envelope model is an
approximation, and the two questions want the error to point opposite ways:
"can I reach the ledge" wants a conservative envelope, "can I reach outside the
map" wants a generous one. So both are run. `DEFINITE` means the conservative
envelope gets there, `MAYBE` means only the generous one does, `NO` means
neither. Never collapse MAYBE into either neighbour.

**On `--res`.** Surface sampling defaults to 4 studs (the duel arena: 1376
nodes, 0.9s; at 2.5 studs, 3552 nodes and 2.0s). Verdicts are stable across 5.0
down to 2.5, but a *marginal* surface can move `NO` -> `MAYBE` as resolution
rises, because a finer grid puts a node slightly nearer the edge it is jumping
from. On the duel arena the posts do exactly this: the nearest deck node is 20.0
studs away at res 4 and 19.25 at res 2.5, against a 19.75-stud slide-speed
envelope. That is information, not noise - a surface whose reachability depends
on where you stand to within a stud is one a player will fail half the time.
Re-run at a finer resolution before trusting any `NO` you were hoping would be
`MAYBE`.

**P21 needs triangle counts.** Give them in the spec's `"meshes"` table (or a
JSON file named by `"meshesFile"`), keyed by mesh name:
`{"tree_oak": {"tris": 812, "kind": "tree", "textures": ["oak_atlas"]}}`.
Class budgets: grass 120, rock 300, building 800, palm 1200, cliff 1500, tree
2500, landmark 3000-8000; at most 40 unique meshes and 12 unique textures per
biome. A placed mesh with no measured triangle count is UNVERIFIABLE, never
PASS. Raise a budget per map in `"budget"`, with a reason.

---

## GROUND IS TERRAIN. IT IS PROVEN ORGANIC, NOT PROMISED.

"A ground plane level for more than 120 studs is a bug" sat in bold in this
file while three maps in a row shipped on flat Part slabs. Prose does not stop a
flat map, so this is code:

- **`spec.py` refuses slab ground.** A ground-role part 64+ studs on a side is
  rejected unless the spec states `"ground_is_parts": "<reason>"` (a floating
  sky arena is the legitimate case; `sky_citadel` and `duel_arena` say so).
- **`scripts/terrain.py`** builds ground as Roblox SMOOTH VOXEL TERRAIN from a
  heightfield. A spec's `terrain` block declares LANDFORMS - a shape (lobed,
  domain-warped ellipse or polyline), a PROFILE of `[inside-distance, height]`
  points and an op (`smax` rise, `smin` cut, `set`, `terrace`) - plus graded
  PATHS, flattened building PADS, 3D CAVES, ZONES with an access rule (`always`,
  `swim`, `lowTideOnly`), and TIDE levels and gates. Output: heightfield,
  material map, masks, `terrain.json` and a preview PNG, all from one spec.
  `specs/meadow_island.json` is a worked example. **Outside a landform's first
  profile point it does not exist** (np.interp clamps; the first smoke run lifted
  the whole sea to 90 studs).
- **`scripts/checks_terrain.py`** runs inside `prove.py`, and each check FAILS
  the map it was written for (`--selftest` proves it on a flat map, a boxy map
  and an organic one):

  | | Check | Fails |
  |---|---|---|
  | T1 | Flatness | a plain over 120 studs across outside pads/paths, >10% flat land, pads over 25% of land |
  | T2 | Relief | under 48 studs of land relief, or fewer than 3 gentle ground LEVELS (beaches, shelves, terrace treads, plateau tops) |
  | T3 | Boxiness | any cliff REGION more than 50% aligned to the X/Z axes - the fingerprint of a rectangle |
  | T4 | Tides | a zone not reachable (or still reachable) as declared at LOW and HIGH tide; anyone stranded when the tide rises |
  | T5 | Caves | radius under 1.6x character height, grades over the design slope, a mouth that never meets daylight, a tide-gated cave the tide does not gate |
  | T6 | Coast | WARNs on a coastline without both cliffs and beaches |
  | T7 | Earthworks | a road needing more than 32 studs of fill or cut |
  | T8 | Cliff cover | WARNs on a lot of bare steep voxel cliff (see fact 2 below) |
  | T9 | Empty land | once the map is dressed (any part with a `mesh` or the `prop` role), over 35% of 64-stud dry land cells with nothing within 56 studs. P11 samples parts, so on a terrain map it defers here |
  | T10 | Spawn | no spawn, or one under water at high tide, on ground over 20 degrees, buried in the terrain, or dropped from high above it |

  T2 and T3 were each wrong on first contact and the reasons are in their
  docstrings: a histogram of all heights has no peak on a steady slope, and a
  map-wide average dilutes a local box below any limit.
- **Studio:** `serve_map.py` serves the heightfield as 3-byte-per-column binary
  chunks; `scripts/luau/build_terrain.lua` writes them with WriteVoxels (partial
  top-voxel occupancy is what makes it smooth), carves caves with Air, then fills
  water below the tide line. It runs as a BACKGROUND task and reports through
  `workspace.Terrain` attributes, because a big map outlasts an execute_luau call.
  `scripts/luau/tide.lua` moves the water between the tide levels one voxel band
  at a time and turns every `TideGate`-tagged volume into an undertow at high
  tide - the same rule T4 proves with. `scripts/luau/verify_terrain.lua` checks
  the BUILT voxels against the heightfield by numbers (on a real island build:
  484 columns, worst error 2.31 studs, every sea column wet, both caves carved) -
  it needs no screenshot, so it works with Studio in the background.

**Studio facts about terrain, all measured:**

1. **Smooth terrain's surface sits about 2 studs ABOVE heightfield + lift**
   (half a voxel; 1.9-2.3 at 11 probed points). Anything placed at the raw
   heightfield value is buried 2 studs deep. T10 checks spawns against it; give
   a part or a mesh standing on terrain the same 2 studs.
2. **Detail noise on a cliff becomes a field of tiny triangles.** Roblox meshes
   the heightfield at 4-stud voxels, so roughness on steep ground reads as
   crushed crystal, never as a clean rock face. `terrain.py` smooths steep
   ground instead of roughening it. To get faceted cliffs, cover them with your
   own cliff models.
3. **Terrain water ends in a hard square at the map edge.** Filling voxels to
   the horizon is millions of voxels; `horizon_ocean.lua` rings the map with a
   shallow band of real terrain water over a dark floor, so it matches by
   construction, and `tide.lua` moves it with the tide.
4. **An inland map has no water.** With the tide below every column the water
   fill region inverted and failed with "Region is too large" after the ground
   was built; `build_terrain.lua` now skips water when the tide is below the
   lowest ground.
5. `Terrain.Decoration` is not a scriptable member from plugin context.

---

## Building it in Studio

**The runbook is a file.** `scripts/build_map.py <spec> [--out folder]
[--serve] [--asset-ids ids.json]` runs prove -> plan -> terrain in order, writes
`report.json`, `plan.png` and `terrain/`, and stops on a FAIL. With `--serve` it
starts `serve_map.py` and prints the bootstrap and the loaders. Then, through
`execute_luau`:

1. **The bootstrap** (`scripts/luau/build.lua` with the port filled in): parts,
   meshes, spawns, the kill plane, folders; removes the place's template
   SpawnLocation and Baseplate. On a terrain map it leaves the voxels alone.
2. **`/build_terrain.lua`**, **`/horizon_ocean.lua`**, **`/tide.lua`** for a
   terrain map: background tasks, poll their attributes.
3. **Prove the spawn in a playtest.** `scripts/luau/spawn_probe.server.lua` as
   a ServerScriptService Script, start a playtest, read the `SPAWN_PROBE ok|FAIL`
   lines (floor material, humanoid state, drop), stop. An edit-mode check can say
   the spawn is on dry, flat, reachable ground and a player can still fall
   through the world: a new place's template SpawnLocation at (0, 0.5, 0) sat 85
   studs inside an island's ground with every terrain check green, and it was
   the only spawn after the whole map was built. **A playtest does not start
   while the PC is locked or on remote control**: start_playtest reported
   running and the output log had no play session at all.
4. **Verify the place** (below), then **look** at it.

Two transports, chosen by size:

| | Use | Why |
|---|---|---|
| `emit.py --lua` | small maps | paste into `execute_luau`; the map appears in the session you are driving |
| `emit.py --rbxmx` | large maps | Insert from File. Asking Studio to run 20,000 `Instance.new` calls parsed out of a multi-megabyte string takes minutes and can hang the plugin thread; the XML goes through Studio's native deserialiser |
| `serve_map.py` | terrain, meshes, anything big | the geometry goes over HTTP as JSON and the builder fetches it; HttpService works from plugin context |

`scripts/blockout.py --map design/map.json --out src/workspace/Map` is the
smallest playable placeholder for a game's `layout` block (plots on a ring, or a
tower-defense trail with `start` and `goal` markers): plain anchored Parts,
deliberately ugly, written as an `.rbxmx` under the Rojo-synced folder so the
core loop can be PLAYED before any art exists. A placeholder must be visibly one.

**Screenshots for a human:** `capture_receiver.py` + `luau/capture_views.lua`.
When you are away from the PC (remote control), the MCP capture only reaches the
agent and desktop grabs fail unless Studio is foreground. Run the receiver in
the background, emit the tour with `capture_receiver.py --emit-lua views.json`,
run it through execute_luau, poll `workspace:GetAttribute("CaptureTour")`, then
look at the PNGs. Camera, capture and pixel read live in one script, so frames
cannot come back one view late. A capture can also hand back a STALE frame;
`luau/sample_view.lua` proves freshness with a 6-bit witness of neon cubes and
reads rendered colours at world points as numbers.

---

## Placement verification

Three checks, and they answer different questions. Only the third can catch a
prop in the wrong place.

| Check | Question |
|---|---|
| `prove.py` | is the SPEC playable? |
| `luau/verify_build.lua` | is the PLACE well formed - anchored, foldered, spawns grounded, no default-grey parts, collidable meshes colliding? |
| **`luau/verify_placement.lua`** | **does the place match the spec, instance by instance?** |

`verify_placement.lua` re-fetches the payload the map was built from and diffs
every instance against it, reporting missing, misplaced, floating and clipping
props. Set `PORT` to the `serve_map.py` port. `luau/verify_ground.lua` checks
that nothing - part or terrain voxel - sits on y=0. **Verify after every build.**
Target is `MISPLACED=0, worstDelta=0.000`.

**Meshes are why placement verification exists.** A Part is placed by CFrame and
is either right or obviously wrong. A Model is placed by its PIVOT, and:

> **A Model's pivot is its bounding-box centre ONLY while it has no
> PrimaryPart.** Set one and the pivot silently becomes that part's centre, so
> every placement shifts by however far that part sits from the middle.

Setting `PrimaryPart` on the cached assets put **all 176 mesh props out by up to
16 studs**, with nothing erroring and every part correct. A wide screenshot did
not show it. The fix is to never trust the pivot: orient the model, read
`GetBoundingBox()`, then translate the measured difference.

```lua
inst:PivotTo(CFrame.Angles(0, math.rad(yaw), 0))
local cf, size = inst:GetBoundingBox()
inst:PivotTo(inst:GetPivot() + (target - cf.Position))
```

The same run also caught four market stalls floating 12.8 studs over the plaza -
a height carried over from a different map's spec - and seven props clipping
into other props, which `_prune_scatter_collisions` in `spec.py` now removes at
resolve time.

### Measure in world space

`Model:GetBoundingBox()` returns the box **in the model's own frame**. Rotating
a model does not change the `size` it reports. Auditing a boundary ring with it
"proved" that every east and west segment had a 21-stud gap between it and its
neighbour, and that the ring was unrotated. Both were false: in world space the
segments measure 17.7 x 43.0, correctly turned, and overlap by 4 studs.

To audit a placement you must build the **world AABB** from part corners:

```lua
for _, d in ipairs(model:GetDescendants()) do
    if d:IsA("BasePart") then
        for _, sx in ipairs({-0.5, 0.5}) do  -- and sy, sz
            local w = d.CFrame:PointToWorldSpace(Vector3.new(
                d.Size.X * sx, d.Size.Y * sy, d.Size.Z * sz))
```

A wrong measurement is worse than no measurement: it sends you rewriting code
that was already correct. **And beware bucketing by proximity.** Classifying
segments into sides with `math.abs(c.Z + 226) < 40` puts the corner segments of
the east side into the north bucket, which makes one side look short and another
look long. If a per-side statistic looks lopsided, suspect the classifier first.

---

## Traps, all measured

1. **PathfindingService lies in edit mode.** See the table above.
2. **A WedgePart rises along its own +Z.** Verified by raycasting a 10x10x10
   wedge at five z values: `z=-4.5 -> y=0.50` through `z=+4.5 -> y=9.50`, flat
   across x.
3. **`capture_screenshot` needs the Studio window RESTORED, not merely running.**
   A minimised window fails with a message blaming *viewport colour*. Check
   `IsIconic` before believing anything else.
4. **Aim the edit camera by writing `Camera.Focus` AND `Camera.CFrame`
   together.** Studio re-derives orientation from Focus every frame, so a bare
   CFrame write moves the eye and then re-points it at the stale focus.
5. **The default Baseplate's top face is at y=0.** A deck whose top is also at
   y=0 is coplanar with it and the two z-fight. The builder removes it.
6. **Auto-step does not apply along a continuous ramp.** Sampling the duel-arena
   ramp at 4 studs gives a 2.6-stud rise per node, which read as eight
   unclimbable steps and split one ramp into eight components. Same-part
   neighbours are judged on surface slope instead.
7. **A wall jump throws you AWAY from the wall.** Without a direction test the
   envelope allowed a jump off a ramp's side face to travel 30 studs backwards
   over the wall onto a post - and, because the spurious route depended on
   nearby geometry, it made a perfectly symmetric 4-fold ring return asymmetric
   answers. Asymmetric results on symmetric geometry always mean a bug.
8. **Probe walls at two heights, not one.** A player on a ledge at y=-14 must
   climb the deck's side face, which spans y=-12..0, so a single probe at +1.5
   passes underneath the very wall the recovery depends on.
9. **Boundary detection must count only nodes you could WALK to.** Counting
   every nearby node at any height let a platform hovering over the deck fill
   the deck's grid, so the deck edge beside it stopped registering as an edge
   and no jump was ever tested from there. Found by the self-test, not by
   inspection.
10. **Size the kill plane off the LOWEST ring-out edge.** Solving from the
    highest one sized the plane off the outriggers and left the deck 0.26s
    short.
11. **The kill plane is not the play volume.** Sized off `bounds` it was exactly
    the play volume, so a player launched out of the arena fell past its edge
    forever. `emit.py` sizes it at three times the play volume plus 400 studs.
12. **Stairs are half-height.** Auto-step is about 2 studs; a 3-stud step is an
    unclimbable ladder (`references/movement-numbers.md`). The resolver refuses
    stairs whose step exceeds the profile's `autoStep`.
13. **Asset upload needs credentials the MCP does not have by default.**
    `upload_decal` fails with *No auth configured*; it wants `ROBLOSECURITY` or
    `ROBLOX_OPEN_CLOUD_API_KEY`, and reports "no auth configured" even when a
    perfectly good `ROBLOX_API_KEY` is set. Upload with roblox-3d-model's
    `upload_asset.py` (Open Cloud, `ROBLOX_API_KEY`) instead.

---

## NEVER LET ANYTHING SIT ON y=0

**This bug has shipped twice. Verify it after every single build.**

Studio draws its editor grid at exactly `y = 0`. Any surface landing there gets
the grid painted across it - the "weird square pattern". It is editor-only and
never appears in a published game, but it makes finished work look broken.
Run `scripts/luau/verify_ground.lua` (paste into execute_luau) after every build.

**Occurrence 1:** a 470-stud ground slab had its top at y=0. Fixed by lifting
the whole map 0.5 studs.

**Occurrence 2:** every PART was correctly above zero and the LAKE was not. A
part-only check passed. The cause:

> **TERRAIN QUANTISES TO A 4-STUD VOXEL GRID.** A 0.5 stud lift is rounded away
> entirely. Terrain cannot be nudged by fractions of a stud.

**Occurrence 3:** the lift was only ever applied on the serve route, so maps
built with `emit.py` sat on the grid whatever the spec said (a farm map declared
lift 8 and verify_ground found 30 surfaces at exactly y=0.00). The lift is now
applied to the resolved tree, spawns included, so every transport agrees.

Rules, all needed:

1. **`volume.lift` must exceed one voxel (4 studs).** Default is **8** in every
   builder, and it should stay a multiple of 4 so parts and terrain agree. The
   spec stays authored around y=0; the map is raised at build time.
2. **Plan every terrain surface on an exact multiple of 4.** Not "about 2 studs
   down" - exactly 4, or 8. `terrain.py` refuses tide levels that are not.
3. **Two materials must never share a voxel band.** They do not blend, they
   fight, and the solid one wins whole voxels. A rock basin and its water
   overlapping by less than a voxel put grey slabs through the lake surface, and
   later flattened the whole lake to rock. The working layout is:

   | Band | Content |
   |---|---|
   | -4 .. 4 | rock basin |
   | 4 .. 8 | water, surface at 8 |
   | 8 | ground plane top (`lift`) |

`verify_ground.lua` reads the terrain voxels as well as the parts, because the
second occurrence was invisible to a part-only check.

---

## MOST MAPS ARE BOUNDED - BUILD THE BOUNDARY AS TWO THINGS

Almost every Roblox map is an arena with an edge, and the edge is the piece most
likely to look like a boundary rather than like scenery. Build it as **two
separate things**:

- **scenery** is what the player looks at: your own cliff or wall models, or
  terrain, turned to face inward
- the **invisible wall** is what stops them: one part per side with
  `"barrier": true`, `"visible": false`, running the full length of the declared
  bounds and overlapping at the corners

**Never contain a player with mesh collision.** A tiled ring has a seam at every
segment and mesh collision is per-triangle: a player will find the seam that
lets them through, and the mesh gives them footholds to climb on the way. P16
walks the whole perimeter in 4-stud steps looking for a gap in the BARRIER and
ignores the scenery entirely. It also fails a barrier with ground built up
beside it: a 12-stud wall with a 10-stud terrace against it is a 2-stud wall.

What placing the scenery got wrong first, each caught by looking rather than by
a check:

1. **The ring must stand ON the ground.** Placed at 248 when the ground stopped
   at 235, the whole boundary hung off the edge. Every check passed, because
   boundary scenery is decor and decor is exempt from grounding. There is no
   ground outside the boundary by definition, so nothing may be placed there.
2. **Sink the ring about 7 studs.** Sitting it exactly on the surface leaves
   slivers of open sky under the segments, visible as a bright line along the
   foot of the cliff from anywhere inside the map.
3. **`ScaleTo` is UNIFORM - scale from what you care about.** Scaling a segment
   to fill its span applied the same factor to its height, producing a 63-stud
   cliff from a declared 30. Decide the scale from the dimension that matters
   (here, height), overlap the segments and keep the scale near 1.

**Judge a boundary from INSIDE, at head height.** The outside view is not a view
any player will ever have, and it is the one that looks most alarming. An open
map with no wall at all (a sky arena whose edge is the ring-out) declares
`"open_edges": "<reason>"`.

---

## Meshes: placing your own

A mesh placement is a part that names a `mesh`. **It is still a Box in the
resolved tree** - it has to be, or the prover goes blind and a forest stops
blocking sightlines. Give it the model's MEASURED size; the builder clones the
model, scales it by `meshScale`, and puts its base on the box's bottom face.

```json
{ "id": "Oak1", "mesh": "tree_oak", "size": [14, 22, 14], "pos": [40, 11, -30],
  "yaw": 35, "roles": ["prop"], "decor": true }
```

Mesh ids come from your own `{name: assetId}` JSON: `build_map.py --asset-ids`,
`serve_map.py --asset-ids`, or the spec's `"assetIdsFile"` (relative to the
spec). A mesh with no id is reported as MISSING at build time, never silently
skipped. `build.lua` loads each asset once into a `ServerStorage` cache keyed by
its `AssetId` attribute and clones per placement (176 props from 12 `LoadAsset`
calls); a regenerated mesh gets a new id, which is what invalidates the cache.
For meshes installed in edit mode from your own placement list, use
`luau/install_dressing.lua` and save the place.

What the builder depends on, all measured:

| Fact | Why it matters |
|---|---|
| Stud scale: 1 Blender unit imports as exactly 1 stud | sizes in the spec are the model's real size |
| Origin at the **base centre** | an asset drops at a ground position with no per-asset offset |
| **The front of an imported asset is Roblox -Z** | a door modelled on Blender -Y lands at local -Z. Measure a new model's front before trusting it: clone, `PivotTo(CFrame.new())`, print the door part's offset |
| Parts named `asset__role` (`cottage__stone_light`) | the theme colours each part by role on arrival. Match the role with `"__([%a_]+)"` - `%a+` stops at the underscore, the palette lookup misses SILENTLY and the mesh keeps default grey (that shipped 361 grey parts) |
| **Roblox names an imported MeshPart after the glTF MESH DATA, not the object** | set `obj.data.name = obj.name` before export, or every part arrives as `Cube.114` and no role resolves |
| Upload as `Model`, never `Mesh`; textures as `Image`, never `Decal` | both wrong choices succeed and come back Approved, and only one of each works |

**NEVER TYPE AN ASSET BOUND.** A bounds table carried a comment saying the
numbers were "measured from the generated glbs". They were not - they were typed
from the generator's parameters. An audit against the real exports found:

| asset | declared | measured | drift |
|---|---|---|---|
| mound | 60 x 6.2 x 60 | 53 x 11.7 x 52.7 | **47%** |
| cliff | 40 x 34 x 16 | 42.3 x 53.8 x 17.4 | **37%** |
| lilypad | 4.1 x 0.3 x 4.3 | 4.1 x 0.25 x 4.3 | 20% |

The mound had been REGENERATED taller and nobody updated the table, so every
placement, overlap test and density sample had been reasoning about a shape that
no longer existed. Measure the exported file. **A guessed bound is a wrong
position.**

**MESH COLLISION IS ON BY DEFAULT, WITH A NAMED EXCEPTION LIST.** The asset
cache once set `CanCollide = false` on every part of every mesh, so a player
walked through every tree, house, market stall and the entire boundary cliff.
Nothing errored, nothing looked wrong in any screenshot, and no check covered
it - it is only discoverable by walking into something. `build.lua` sets
collision **per instance**, hardcoded rather than a spec option:

```lua
local WALK_THROUGH = {lilypad = true, veg_patch = true, crop = true,
                      grass = true, flower = true}
```

Everything not named there collides, with `CollisionFidelity.Box`. Wrong in the
permissive direction makes a map unplayable; wrong in the strict direction just
trips someone on a lilypad. `verify_build.lua` fails on any collidable-class
mesh part with collision off.

**Static scenery lives in the place, not in a runtime script.** A map's 336
meshes cloned by a server service at boot worked and passed every gate, but the
world was empty in edit mode and nothing was in the saved place. And never put
runtime-made instances inside a Rojo-managed subtree: a runtime dresser placed
897 meshes perfectly, then Rojo reconnected and every tree vanished, because
Rojo reconciles `Workspace.Map` against its source and deletes what is not
there. That is Rojo working correctly, and it reads exactly like Rojo being
broken. `MeshId` is not settable from a Rojo `.model.json`; in an `.rbxmx` it is
an ordinary `<Content>` property, so bake meshes into the map's `.rbxmx` (edit
it with an XML parser, never a regex: a part carrying a PointLight has a nested
`<Item>`), or install them in edit mode and save.

---

## THE TWO RULES THAT MATTER MOST FOR LOOKS

The prover checks whether the map WORKS; it has nothing to say about whether it
looks like a game anyone would open. Judge that from a wide screenshot before
calling a stage done.

### 1. Build from a reference image, never from imagination

Search for a reference, **download it, and actually look at it**, then build to
what it shows.

```bash
# find one, download it, then READ it - do not describe it from memory
curl -sL -o refs/cottage.jpg "<image url>"
```

Reasoning about what a cottage looks like produced a box with a lid, three times
running. One reference produced six concrete corrections in a single look: the
roof is as tall as the walls, the gable faces front, half-timbering carries the
character, windows are round and arched rather than rectangles, nothing is
plumb, and the building meets the ground on a mound. The cost is one search and
one `curl`; the alternative is several rounds of guessing. `scripts/theme.py
extract refs/*.png --name my_map` turns reference images into a palette theme.

### 2. Mesh first. Parts are the exception, not the default

**This is GATED, not advised.** `spec.py` refuses to load a spec that builds a
mesh-class kit (tree, treeline, pine, rock, boulder, scatter, cottage, house,
hut, stall, cart, mound) out of parts. Opt out per spec with
`"parts_are_deliberate": "<reason>"` - never by silence.

Why it is a gate: a shipped map had `grep -c mesh design/map.json` returning
**zero** - 75 scatter entries, 16 trees, 7 treelines and a cottage, all parts.
The prover passed all 16 checks the whole time - reachable, sealed and lit are
all things a map made entirely of boxes does perfectly. Every rule was already
written down. Being written down was not enough.

| Use a mesh for | Because |
|---|---|
| trees, bushes, rocks, boulders | organic shapes; also 1 instance instead of 5 |
| houses, stalls, carts, fences | detail that parts can only fake |
| ground mounds, lake beds | a squashed dome is not expressible as a part at all |
| anything repeated more than a few times | instance count is the performance lever |

**A worked example of why.** A wide shallow ground dome sized (60, 11, 60) was
built as a `Ball` part. A Roblox Ball takes its diameter from the **smallest** of
the three size components, so that "60-stud dome" was an 11-stud sphere. There
is no part that makes a squashed dome.

A greybox is the exception the gate allows for: boxes standing in for buildings
while the layout is proven. A placeholder must be visibly one, and it is an open
debt until a mesh replaces it.

---

## Lighting

`scripts/lighting.py` - five presets, applied as generated Luau. A theme's own
`lighting` block is layered on top.

```bash
python scripts/lighting.py --list
python scripts/lighting.py golden_hour --theme sky_citadel -o lighting.lua
```

| Preset | Use |
|---|---|
| `stylised_day` | bright cartoon outdoors, the default |
| `golden_hour` | low warm sun, long shadows - the thumbnail preset |
| `flat_cartoon` | unshaded retro. Needs `CastShadow` off on every part |
| `overcast` | neutral and unflattering, for judging form not mood |
| `moonlit` | cold night. Needs light sources IN the map or it is just dark |

**Measured the hard way:**

1. **Atmosphere does nothing without a Sky.** Roblox requires at least one
   `Sky` in Lighting for Atmosphere to affect the scene. Every preset carries one.
2. **`Lighting.Technology` cannot be set OR READ from plugin context** -
   "lacking capability RobloxScript". Everything else writes fine. Each property
   is wrapped in its own pcall and the applier reports what it could not set.
   Set Technology by hand; without `Future` the scene renders noticeably flatter.
3. **Roblox Atmosphere is far stronger than a palette suggests.** Density 0.36
   with Haze 1.7, derived from a sky colour, turned a 300-stud map into a blue
   fog bank. Outdoor presets sit at 0.08-0.15.
4. **A saturated `ColorCorrection.TintColor` multiplies the whole frame** and
   must stay near-white unless a strong grade is the actual intent.
5. **`ColorShift_Top` is ADDITIVE, not a tint.** Set to a near-white
   (255,244,224) it bleached a whole test scene pale icy blue. Working values
   are around (12,10,6) to (18,14,8).
6. **Blue ambient times blue albedo compounds.** With a blue-tinted
   OutdoorAmbient, blue-grey stone in shade rendered as saturated navy. Keep
   ambient near-neutral and let the surface colour carry the hue.
7. **Clear the place's OWN instances by CLASS, not by name.** Roblox places ship
   with their own `Sky`, `Atmosphere`, `Bloom`, `SunRays` and `DepthOfField`; an
   applier that only deletes what it named itself leaves two of each, fighting.

```lua
for _, c in ipairs(Lighting:GetChildren()) do
    if c:IsA("Sky") or c:IsA("Atmosphere") or c:IsA("PostEffect") then c:Destroy() end
end
```

Change one lighting value at a time and compare; do not hand a feedback loop a
knob you have not measured the response of. `ExposureCompensation` is the dial
worth knowing beyond the presets: a negative value with a raised `Brightness`
gives the "crispy" look developers use to kill neon glare.

`scripts/luau/ambient.lua` is installed by the builder: slow, small motion on
tagged instances. **TweenService cannot tween a Model** - only its PrimaryPart
moves; weld to the PrimaryPart or tween a CFrameValue and `PivotTo`.

---

## Round geometry and organic water

Roblox `Part.Shape` supports `Cylinder` and `Ball` at the same cost as a
`Block`, so a plaza, silo or well should never be a rectangle. Three measured
facts, and mixing any two of them causes a visible bug:

| Thing | Axis / rule |
|---|---|
| `Part.Shape = Cylinder` | axis along the part's **X**; diameter from `min(Y, Z)`. An upright cylinder needs a 90 degree roll about Z and swapped extents (the builder does this for `"shape": "cylinder"`) |
| `Part.Shape = Ball` | diameter from the **smallest** of the three components. **A squashed dome is impossible** - use a mesh |
| `Terrain:FillCylinder` | axis along the CFrame's **UP (Y)**. Do NOT rotate it |

The last two conventions disagree, and that cost two renders: rotating a
`FillCylinder` by 90 degrees to match the Part convention tipped a lake basin on
its side and pushed a grey dome up through the water. The prover treats every
shape as its bounding box, which is conservative.

A rectangular lake never reads as natural. Keep Terrain water - it has waves,
reflection, buoyancy and swimming that no part can fake - but fill it as a
**ring of overlapping cylinders around a lobed outline** (`"terrainWater": true,
"organic": true, "lobes": 7` on a part), not one `FillBlock`:

```lua
wob = 1 + 0.18*sin(a*lobes + 0.7) + 0.10*sin(a*(lobes+2) + 2.1)
```

**Fill the basin FIRST, as one piece, ending below the water.** Filling a rock
ring per lobe let each lobe's rock intrude into its neighbour's water and punch
grey slabs through the surface.

**One outline, not three copies.** `scripts/outline.py` owns the lake shape.
The builder fills it, whatever dresses the bank places props around it, and P14
checks nothing stands in it - and when each carried its own constants they
disagreed twice in one afternoon: the bank was placed at 0.43-0.49 of the pond
size while the water reached 0.51, so every rock sank; and the builder ignored
the pond's yaw while the bank applied it, so a 12 degree disagreement on a lobed
outline sank the props on one side and stripped the other bare. Derive positions
by MARCHING (`outline.bank_point`), not by arithmetic: adjacent discs bulge
outward between sampled angles, so the true edge is always further out than the
single-disc formula says.

**Flat things block props too.** Water (an invisible, non-solid marker sunk below
the ground) and paths (under a stud thick) both fail a "solid and taller than
the clearance" blocker test, so trees stood in the lake and boulders landed on a
walking route. Both are judged in PLAN now (`_overlaps_plan`, `outline.in_water`)
and checked by P14 and P15. Exempt what belongs there: `outline.FLOATS`
(lilypads) is shared by the prune and by P14, because a second copy of the list
once reported an emptied lake as passing.

---

## How this skill is kept honest

**WHEN A HUMAN FINDS A DEFECT, WRITE A CHECK.** If someone looking at the map
finds something wrong, the fix is **not** to correct that map - it is to add the
check that would have caught it, then fix the map. P1-P9 ask "is the built
geometry what the spec declared", and every one of them can pass on a map that
is obviously wrong to a person. P10-P13 exist because a human had to point each
of them out:

| Check | The complaint it came from |
|---|---|
| **P10 Coplanar surfaces** | the central circle looked glitchy: a plaza deck and rim both topping at y=1.20 flickered |
| **P11 Empty space** | a lot of empty space, and players have short attention spans |
| **P12 Entrances** | a door should face a position that a path can reach |
| **P13 Feature dressing** | the corners of the lake were empty, where there had been rocks |

P13 is the sharpest lesson: switching a pond to Terrain water **silently removed
the rock ring around it**. Every geometry check still passed.

**Tuning a check is not the same as weakening it.** P10 was correctly noisy at
first and needed three genuine exemptions - trim thinner than 30% of the face it
sits on, a shared area under 12 studs squared (invisible in game), and walkable
route surfaces, which are *meant* to meet at one height. Each is a stated reason,
not a threshold nudged until the number went green. Where a threshold really is
wrong for the genre, say so in the spec rather than quietly editing it. Expect
the checks to pull against each other: adding props to satisfy P11 pushed P5
sightlines below its floor. That tension is the design space.

**SCOPE A NEW CHECK BEFORE TRUSTING IT.** P15's first version reported eight
failures, all deliberate architecture; P14's first version reported 216 false
positives. A check that fires on correct work will be ignored, and then it is
worse than no check. Narrow it to the defect it was written for, and say in the
docstring what it deliberately does not look at.

**VERIFIERS MUST FIND THEIR OWN TARGET.** `verify_build.lua` once had a map name
hardcoded at the top; a later map had another name, so every run returned "not
found" and was skipped - while 361 mesh parts sat in the map wearing default
grey. The check for exactly that defect was already written, inside the file
that could not run. The verifiers now locate the map themselves.

**THE PIPELINE MUST LIVE IN FILES, NOT IN THE CONVERSATION.** For most of this
skill's life the real builder was typed inline into `execute_luau` and never
written down; recovering it from a chat transcript recovered a PRE-FIX version,
which put the lake back on its side. The builder is `scripts/luau/build.lua` and
the runbook is `scripts/build_map.py`. If you find yourself pasting geometry
code into a tool call, stop and put it in the file first.

**What this skill takes from the common "building maps" convention:** a folder
hierarchy, not a flat Model (`Terrain/Structures/Landmarks/Props/Spawns` under
one root, with an `Origin` part at (0,0,0) as PrimaryPart), and verification of
the PLACE, not just the spec. Deliberately not adopted: "all structures must
connect to the ground plane" (a sky map is the counter-example, and a common
genre), and the stateful chunked build-in-Studio process (the spec file IS the
state, so Studio is written once from a description that can be re-emitted).

---

## Known gaps

- **Dressing is not part of this skill.** It builds and proves layout; props,
  buildings, trees, materials and textures are yours to place (`mesh` parts).
- **Only `stairs` is a built-in kit.** Everything else is written as plain parts.
- **P1 grounds against parts only.** A part standing on terrain takes its y from
  the terrain output (pad heights in `terrain.json`, `height.npy`) plus the
  ~2-stud surface bias; leave `grounded` off it.
- **Rotation is yaw-only.** Roblox greybox is overwhelmingly axis-aligned or
  Y-rotated; arbitrary rotation would need a full SAT for nothing.
- **The wall-tech envelope is an over-approximation** even in the conservative
  pass, because climb budget is modelled as a height allowance rather than as
  the time-based resource it actually is. This is why MAYBE exists.
- **`ragdollRecovery` cannot be measured by `calibrate.lua`** - it belongs to
  the game's own ragdoll code. Time it by hand; P9 is directly sensitive to it.
- **Nothing here judges whether a map is fun.** By design.

## Files

| File | Role |
|---|---|
| `scripts/spec.py` | load, validate and resolve a spec into one tree; the slab-ground and mesh-first gates; built-in stairs |
| `scripts/prove.py` | P1-P9, plus the design checks (`checks_design.py`), budget (`checks_budget.py`) and terrain checks (`checks_terrain.py`) |
| `scripts/reach.py`, `geom.py`, `outline.py` | reachability envelopes, raycasts, the shared lake outline |
| `scripts/plan.py`, `preview.py` | the annotated plan PNG; a quick 3D look |
| `scripts/terrain.py` | heightfield, materials, caves, preview |
| `scripts/emit.py`, `serve_map.py`, `build_map.py` | Luau / rbxmx emitters, the HTTP server for Studio, the runbook |
| `scripts/blockout.py` | a playable placeholder from a game's `layout` block |
| `scripts/theme.py`, `lighting.py` | palettes from reference images; lighting presets |
| `scripts/capture_receiver.py` | receives screenshots from `luau/capture_views.lua` |
| `scripts/verify_map.py` | prover self-test (11 sabotages) |
| `scripts/luau/build.lua` | THE builder (bootstrap) |
| `scripts/luau/build_terrain.lua`, `tide.lua`, `horizon_ocean.lua` | terrain voxels, tides, the ocean ring |
| `scripts/luau/verify_build.lua`, `verify_placement.lua`, `verify_ground.lua`, `verify_terrain.lua` | verify the place |
| `scripts/luau/spawn_probe.server.lua`, `calibrate.lua` | playtest probes |
| `scripts/luau/ambient.lua`, `install_dressing.lua`, `sample_view.lua`, `capture_views.lua` | ambient motion, edit-mode mesh install, rendered-colour sampling, screenshot tour |
