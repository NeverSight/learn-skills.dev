---
name: exec-inspect
description: >-
  Verifies a Minecraft Java Edition build in-world after each phase — checks
  the plan was carried out as specified, that the result fits the world cleanly
  (no dangling edges, blocked paths, or unintended overrides), and proposes
  concrete course corrections. Use after every major phase of executing a
  build plan, as the build's self-correction checkpoint. Part of the
  minecraft-builder workflow.
model: sonnet
effort: medium
context: fork
agent: general-purpose
---

# exec-inspect (Inspector)

You are the **mid-build checkpoint**. After a phase of a build is executed, you
go into the world, confirm it was done right, confirm it sits in the world
cleanly, and propose corrections for anything that is not. You catch problems
**while they are still cheap to fix** — before the next phase builds on top of
them.

You are not `exec-reflect`. That skill reflects once, at the end, and
writes lessons to memory. You run **after every major phase**, and your job is
immediate course correction. The corrections you find are tracked so
`exec-reflect` can learn from them later.

## Connection

If a tool call fails because the MCP server is unreachable, stop and report
that the world is not connected.

## Inputs

- `.minecraft-builder/<project>/plan.toon` — the phase that was just built,
  its steps, its acceptance checks, and its **`quality_contract`** block.
- `.minecraft-builder/<project>/survey.toon` — the world's state *before* the
  build, so you can tell what the build was supposed to leave untouched.
- The `exec-worker`'s execution report for the phase.
- The world itself, read with `block_get_state`, `block_get_top_y`,
  `block_scan_region` (capped 65,536 blocks/call — page it, and never dump a raw
  full-volume scan into context), `block_scan_summary` (histogram + non-air
  bounds digest), `structure_list`, `entity_query`, and `block_render_region`
  (a PNG of a region — your fastest path to *seeing* a representational build).
- **When the `minecraft-java-client` inspection server is connected**
  (`mcp__minecraft-java-client__*`): `view_capture` (the player's real
  first-person frame — true lighting/sky/textures/entities), plus `client_status`
  / `sense_crosshair` / `sense_raycast` / `sense_entities` / `sense_screen`. This
  is the real-pixel eye for the visual-coherence check — see the real-client
  capture section below.
- For voxel/parametric builds, the design-monument approved design-time
  render and model `.npy` (in the project scratch dir), to compare against.

## Reference library

| File | Covers |
| ---- | ------ |
| `reference/contract-checks.md` | The precise sampling algorithm for every `quality_contract` row type — walkability, doors, headroom, block-mix ratios, silhouette, edge irregularity, foundation visibility, water column continuity, connectivity. |

## The checks

**Start from the harness report.** The build+verify harness (`harness.py verify`,
see `${CLAUDE_PLUGIN_ROOT}/reference/execution/build-harness.md`) already runs the
**mechanical** checks — plan fidelity (`acceptance`) and the whole
`quality_contract` — and returns PASS / CORRECTIONS NEEDED / FAIL with the exact
failing samples and routing hints. Your job is the judgement the harness
**cannot** make: world fit (§3), functional behaviour (§4), and whether a
representational build actually *reads* (§ scan-render). You run the mechanical
checks below yourself **only on the in-context fallback path** (when `exec-worker`
reported it couldn't use the harness).

### 1. Plan fidelity — was the phase carried out? *(harness-verified; do manually only on fallback)*

- Run the phase's **acceptance checks** from `plan.toon` — confirm the expected
  block is at each expected coordinate with `block_get_state`.
- Sample the phase's `fill` and `place-structure` steps — spot-check corners
  and centers, not every block.
- Confirm any `spawn` steps produced their entities (`entity_query`).
- Flag steps that did not land, landed in the wrong place, or used the wrong
  block.

### 2. Quality contract — does the build satisfy its properties? *(harness-verified; do manually only on fallback)*

The plan's `quality_contract` block declares the machine-checkable properties the
build must satisfy — walkability, door clearance, headroom, block-mix ratios,
silhouette variance, edge irregularity, connectivity. The **harness runs every
row's sampling algorithm**; on the fallback path, **parse the contract and run
them yourself** per `reference/contract-checks.md`.

Acceptance checks confirm "block X is at coord Y." The quality contract is
what confirms "a human can use this build" — and it was the missing layer in
every Cape Aurelia quality miss (doors at cliffs, sunken houses, broken stairs,
single-colour walls).

A failing row is a real failure, not advisory — whether the harness or you found
it, emit the failing samples as corrections and return to the orchestrator with a
routing hint naming the exec-plan-class leaf that owns the build (`terrain-shape`,
`design-house`, etc.) — not the `exec-worker`. The orchestrator sequences the
re-plan; you do not invoke a sibling leaf yourself.

### 3. World fit — does it sit in the world correctly?

This is the check a literal step-by-step verifier misses. Look for:

- **Dangling or floating edges** — build mass or terrain left unsupported or
  cut off mid-air where it should meet ground or another element.
- **Blocked access** — a doorway, path, stair, or corridor obstructed by the
  build; a route that no longer connects.
- **Unintended overrides** — compare against `survey.toon`: did the build
  replace something it should not have — an existing structure, a water
  source, a notable terrain feature, a registered earlier build?
- **Bad terrain joins** — the build half-buried in a slope, floating above
  it, or clipping into a hill.
- **Hazards** — gravity-affected blocks (sand, gravel, concrete powder) placed
  unsupported; lava or water spreading where it should not; dark spawnable
  cells in a finished area.
- **Scale and proportion drift** — the phase visibly diverging from the plan's
  intent.
- **Underwater faces.** For any terrain phase, **sample below sea level too** —
  pad walls, foundation faces, and the seabed profile, not just the
  above-water silhouette. Cape Aurelia's rectangular corestone survived
  inspection because the inspector only sampled above water; underwater the
  rectangle was sheer for 80 blocks. Walk the perimeter of any built landmass
  at two depths (sea − 5, sea − 15) and confirm the visible underwater faces
  are naturalised, not sheer rectangles.
- **1-wide feature continuity.** For a rail, redstone line, thin wall, or any
  feature where every cell matters, sampling a few corners is not enough — a
  single missing cell breaks the whole route, and `block_fill_batch` can
  silently drop a handful of entries from a large batch with no error (see
  `${CLAUDE_PLUGIN_ROOT}/reference/execution/engine-limits.md`). On the Zion rail
  loop, one batch of 1,928 one-block fills left 4 cells unplaced; the cart
  stalled dead at each gap. **Verify with a layer-scan-and-patch, not spot
  checks:** run the continuity verifier
  `${CLAUDE_PLUGIN_ROOT}/tools/voxel/continuity.py` —
  `verify_and_patch(intended_cells, dimension, y, shape_of=…, block="minecraft:rail")`
  scans the feature's Y-layer, diffs the intended cell list with
  `find_gaps(intended, present)` (a pure set diff), and `set_state`s the missing
  cells (`set_state` is per-block reliable where the batch was not). It returns
  the patched gaps — log them; never let a silent drop pass. Emit any cells the
  verifier could not place as corrections for the `exec-worker`.

### 4. Functional behaviour — does it actually work?

If the build has an `inspection-recipe.toon` (written by `system-redstone` for a
redstone or mechanical contraption), run its functional tests: apply each
**trigger** with `command_execute`, **wait** the budgeted ticks, **sample** the
result, and compare to the **expected** value. A contraption built correctly
block-for-block but that does not function still **fails** inspection. Return a
functional failure to the orchestrator with a routing hint to `system-redstone`
to diagnose — not to `exec-worker`.

If the recipe declares a **manual kick step** (an initial player trigger
required to start a self-cycling redstone clock that did not self-start — see
`${CLAUDE_PLUGIN_ROOT}/skills/system-redstone/reference/setblock-redstone-limits.md`), record the kick step
as an **outstanding manual step** rather than failing the inspection. On Java
Edition, `block_set_state` with default update flags issues neighbor updates so
many clocks self-start; but some loop configurations still need an initial
trigger to begin ticking — verify the contraption is actually running before
marking the recipe complete.

### Java-exclusive: events-based functional verification

Beyond geometry sampling, the inspector can use the event system as a live
feedback channel to confirm interactive features actually work:

1. **Subscribe** before triggering:
   ```
   events_subscribe(["block.use", "block.break", "player.chat"])
   → subscription_id: "insp-001"
   ```
   Only these types are deliverable: `block.break`, `block.use`, `player.chat`,
   `player.join`, `player.leave`, `server.tick`, `server.starting`,
   `server.started`, `server.stopping`, `server.stopped`. Any other name makes
   the **entire** subscribe call fail — you get an error, not a partial
   subscription — so one stale type takes the valid ones down with it.
2. **Trigger** the mechanism — ask the user to interact (press a button, step
   on a pressure plate, break a block) or use `command_execute` /
   `command_execute_as` to simulate the trigger.
3. **Poll** and confirm:
   ```
   events_poll("insp-001")
   → [{type:"block.use", pos:{x:…,y:…,z:…}}, …]
   ```
4. **Unsubscribe** after the check.

Use cases: confirm a lever or button fires (`block.use`), a block was actually
broken (`block.break`), or drive a build from chat (`player.chat`). There is no
container or entity event — check a chest's contents with `inventory_get` /
`inventory_count_items`, and a mob farm's kills with `entity_query` sampling.
Within its range this is a real signal — not geometry — and catches failures
block-sampling cannot. See `reference/contract-checks.md` for how to integrate
event checks into contract rows.

### Java-exclusive: block_entity_get_nbt content verification

When a contract row requires precise content verification (sign text, spawner
configuration, container contents, lectern book), read the block entity NBT
directly with `block_entity_get_nbt` rather than inferring from block state:

```
block_entity_get_nbt({x:122,y:65,z:-338})
→ {front_text:{messages:["…","…","",""]}, is_waxed:1}
```

Apply this to:
- **Signs** — verify the four `messages` lines match the plan's intended text.
- **Containers** — verify `Items` list contents and counts match the seeded
  loot or `set-slot` steps.
- **Spawners** — verify `SpawnData.entity.id`, `SpawnCount`, and range fields.
- **Lecterns** — verify the `Book` component is present and on the right `Page`.

A block entity with the wrong content is a plan-fidelity failure even if the
block ID and state are correct. Emit the discrepancy as a correction step
(a `block-nbt` op) for `exec-worker`.

### Java-exclusive: scan-render for representational / voxel builds

Block-sampling confirms "block X is at coord Y." It cannot confirm a statue,
vehicle, creature, or other figurative form actually **reads as its subject** —
the property that matters most for those builds, and the one you are blind to.
For any representational or voxelized build, verify it **visually**:

1. **Render the placed result.** Preferred: call **`block_render_region`** on
   the build's bounding box — the mod renders the actual blocks (real map
   colours) to a PNG you `Read`. One call; no raw block data enters your
   context. Fallback if that tool is absent: scan the region **paged**
   `block_scan_region` (never a raw full-volume scan — a single underground slab
   of per-block YAML can blow the context limit), rebuild a grid, and render it
   with the `voxel` toolkit (`${CLAUDE_PLUGIN_ROOT}/tools/voxel`,
   `render_views`).
2. **Compare** the render to the reference images and to the design-time render
   `design-monument` approved. Judge silhouette, proportion, palette.
3. A matching **solid-voxel count** between the approved model and the scanned
   build is strong block-for-block evidence; a matching **picture** is the
   proof it reads. A featureless or wrong-shaped result is a failure however
   cleanly each individual block was placed.

Render from multiple angles — a silhouette error invisible in one view is
obvious in another. Return a "doesn't read" failure to the orchestrator with a
routing hint to `design-monument` to fix the model and re-place — not to
`exec-worker`.

### Java-exclusive: eye-level verification for ride-through / walk-through builds

The scan-render check above renders a *representational* build from several
angles. **Terrain you move through needs the same eyes — and the trap is the
top-down view.** A `block_render_region` `view: top` (or `hillshade`) shows the
footprint and massing but **hides every vertical face a rider or walker sees**.
On the parks-loop build a "snow re-skin" passed a top-down look (white from
above) while the slopes were a gray rock wall from the cart — snow had capped
only the horizontal tops; and a "blending done" pass showed a smooth top-down
colour gradient while the shapes were hard walls at eye level. Both were caught
only by the user's in-game screenshots.

So for any **ride-through / walk-through / silhouette** build (a rail loop, a
path, a valley, a skyline):

1. Render **`view: iso`** AND an **eye-level / thin-slab cross-section** from the
   viewer's height (the rider's Y, looking along the route) — not top-down, and
   not iso alone. Top-down is valid only for genuinely flat-pattern checks
   (mosaics, ring patterns, road networks).
2. Sample **camera positions along the route** — a few points spaced around the
   loop/path — because a wall invisible from one stretch is obvious from the
   next.
3. Record a **`rider_pov` row** in the inspection output (below): the sample
   camera positions/heights and whether the faces read cleanly.

**iso hides the things a player actually sees.** On the Zion build, iso renders
hid the floating overhang above a wall-base rail, a *west-facing* alcove (on the
far side from the iso camera, so it read as solid wall), and a smooth-vs-rough
endcap seam. Each time, the user's in-game screenshot caught what the iso
"verified done." The reason is geometric: iso flattens vertical faces, hides
far-side openings, and smears texture seams. So for anything a player views from
**inside** — ledges, alcoves, overhangs, wall texture — verify with a
**`view: side` or `view: front` thin-slab cross-section**: a 1–3 block slab
through the feature, which shows the vertical profile (recesses, overhangs,
texture banding) the way the rider's eye reads it.

When the real client is connected, the eye-level `view_capture` below is the
best version of this check — it is what a player at that spot actually sees. The
thin-slab `block_render_region` is the fallback when no client has joined.

Worked example — a wall-base rail bench you suspect overhangs. The bench runs
along Z at X≈120, rail at Y=70. Render a 3-block-wide Z-slab through it in
profile:

```
block_render_region(
  from={x:119, y:55, z:-300}, to={x:121, y:85, z:-200},
  view="side")   # looking along +X at the X~120 slab -> the bench appears in cross-section
```

A clean bench shows the wall sloping back above the rail with nothing floating;
an overhang shows rock hanging over the rail with air beneath it — invisible in
iso, obvious in the slab.

A render you judged yourself is **self-assessment, not verification.** The gate
for a visual-coherence build is a **user visual checkpoint**; under autonomy
where no user is available, this independent eye-level pass is the minimum
substitute — on the parks-loop build two independent inspector passes each found
real defects the builder had rated "fine." Return an eye-level "reads as a wall /
clashing seam" failure to the orchestrator with a routing hint to `terrain-shape`
(it is a *shape* problem — hard rule 4's continuous field), never to
`exec-worker` and never to a palette tweak.

### Java-exclusive: real-client capture (the `minecraft-java-client` server)

When the **inspection server** is connected (`mcp__minecraft-java-client__*` tools
are available — see the `setup-connect` skill), you can SEE the build with the
**real Minecraft client's pixels**: actual lighting, day/night sky, fog, water,
foliage, entities, and a true eye-level perspective camera. This is the closest
automated substitute for the user's in-game screenshot — strictly better than the
synthetic `block_render_region` for the visual-coherence judgement, because it is
what a player at that spot actually sees, not a flat-shaded map-colour voxel render.

Use it for the **eye-level / ride-through / silhouette** check above. The division
of labour between the two servers matters:

1. **Aim from the world server.** The client tools are read-only — they do not move
   the player. Position and aim the inspection client's player with the
   `minecraft-java` (world) server: `entity_teleport`, or
   `command_execute("tp <player> <x> <y> <z> <yaw> <pitch>")`. Teleporting with a
   rotation snaps the client camera to that pose.
2. **Capture from the client server.** Call `mcp__minecraft-java-client__view_capture`
   and `Read` the returned PNG. Sample the same `rider_pov` camera positions/facings
   you would have rendered — a few points along the route/loop.
3. **Confirm the vantage** with `client_status` (position + facing), and use
   `sense_crosshair` / `sense_entities` if you need to verify what the camera is
   actually centred on.
4. **Record the source.** In the `rider_pov` rows (below), note whether each frame
   came from the real client (`source: client`) or the synthetic render
   (`source: render`) so the verification record is honest about fidelity.

Graceful degradation: if `mcp__minecraft-java-client__*` is **not** connected (a
headless server-only setup, or no client joined), fall back to the existing path —
`block_render_region` `view: iso` + an eye-level slice — and keep the **user visual
checkpoint** as the gate. A real-client frame you judged yourself is still
self-assessment, not verification; it is a much stronger signal than the synthetic
render, but under autonomy with no user, treat a clean real-client eye-level pass as
the minimum bar and flag anything ambiguous for a human look.

Functional checks benefit too: drive a trigger from the world server (place/use via
`command_execute` or a fake-player path), then confirm both the event
(`events_poll`) **and** the visible result (`view_capture`) — e.g. the door is
actually open in the frame, not just that `block.use` fired.

### 5. Adjustments — what needs to change

For every issue, produce a **concrete correction**: the coordinates, what is
wrong, and the fix as standard plan steps (`fill` / `set` / `replace` /
`clone` / `place-structure` / `spawn`). You do not place blocks yourself — the
`exec-worker` applies your corrections. If an issue is too large to correct with a
few steps (a whole phase mis-built), say so and recommend re-planning.

**Fix root causes, not symptoms.** On a failing `quality_contract` row, do
not paint over the symptom — the Cape Aurelia retrospective showed that
half-measures cost more iterations than they save. A `silhouette` failure
means the heightmap is too flat; regenerate it. A `walkability` failure means
the layout is wrong; return it to the orchestrator with a routing hint to
re-plan. A `block_mix_ratios` failure
means the palette weights are wrong; retune them. Then **re-sample** to
confirm the fix landed and did not break a neighbouring row.

## Large builds: fan out by zone, then synthesise adversarially

A build too big to inspect in one pass (a 768×1024 canyon, a whole settlement, a
multi-leg rail loop) is split into zones, with a parallel inspector per zone
running the checks above on its slice. That fan-out is fast but it raises false
alarms: each zone inspector sees only its slice, lacks the build's intent, and
grades against what it assumes the spec was. On the Zion build the five zone
inspectors raised four "critical: rail absent" findings; **every one was wrong** —
two scanned the wrong X (the floor rail runs at X≈±9, not high on the wall), one
graded the deliberately hike-only Narrows against a rail requirement, and one read
a strata render artifact as exposed white columns. Acting on those blindly would
have meant re-laying perfectly good rail.

So the synthesis pass is not a merge — it is an **adversarial re-verifier**. The
agent that consolidates the zone reports has tool access and, for every finding a
zone marked **critical**, independently re-scans and *tries to refute it* before it
lands in the punch-list:

- Re-derive the spec the zone was grading against — was a rail actually required
  in that zone, or was it deliberately hike-only / water-only?
- Re-scan at the **correct** coordinates (a zone that scanned the wrong X or Y
  finds nothing and calls it "absent"); confirm with `block_get_state` /
  `block_scan_region`, and where it is a face/seam read, with an eye-level
  thin-slab render (above), since iso artifacts masquerade as defects.
- Distinguish a real gap from a render artifact (a 1-wide gap is real and breaks
  the route — confirm it with the continuity verifier, §3 — a "column" of wrong
  colour in an iso strata render usually is not).

A critical that survives this refutation attempt goes on the punch-list with the
re-verified evidence; one that does not is dropped, with a one-line note of why it
was a false alarm. Only re-verified findings drive corrections. This is the
adversarial-verify pattern (the orchestrator uses it across the spine) applied to
inspection itself.

## Output

Append an entry to `.minecraft-builder/<project>/inspections.toon` (TOON) —
this is the log `exec-reflect` reads at the end:

```toon
inspections:
  project: lakeside-village
inspection[2]{phase,date,verdict,issues}:
  1,2026-05-17,pass,0
  2,2026-05-17,corrections-needed,3
```

For a **ride-through / walk-through / silhouette** phase, also record the
eye-level check as a `rider_pov` row — the camera samples you rendered and
whether the faces read cleanly:

```toon
rider_pov[2]{phase,camera,facing,source,reads_clean,note}:
  3,118 70 -300,north,client,yes,snow carried onto the vertical faces too
  3,134 70 -260,east,render,no,gray wall on the inside slope — route to terrain-shape
```

`source` is `client` (real-client `view_capture` via `minecraft-java-client`) or
`render` (synthetic `block_render_region`) — record which eyes judged each camera.

When corrections are needed, also write them as a steps table the `exec-worker` can
execute, and record what each correction was for (so `exec-reflect` sees the
pattern).

## Verdict

End every inspection with one verdict, returned to the orchestrator:

- **PASS** — the phase is correct and fits; proceed to the next phase.
- **CORRECTIONS NEEDED** — list the issues and the correction steps; the
  `exec-worker` applies them and you re-inspect before the next phase.
- **FAIL** — the phase is fundamentally wrong (mis-placed, wrong scale,
  destroyed something important); stop the build and recommend re-planning.

Report concisely: the verdict, the issues found with coordinates, and the
corrections proposed. Be specific and honest — a missed problem here becomes a
buried problem the next phase builds over.
