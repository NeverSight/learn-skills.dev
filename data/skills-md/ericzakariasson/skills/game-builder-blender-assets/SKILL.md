---
name: game-builder-blender-assets
description: Authors camera-critical 3D assets for a homage game (hero characters, first-person weapon viewmodels, hero vehicles or set pieces) in Blender and exports GLB, one asset per specialist subagent at high craft, with an orchestrator-owned turnaround gate before the game binds the mesh. Companion to game-builder. Use only when the locked reference shots are 3D and a hero or close-up asset would otherwise be built from in-engine primitives. Prefer 2D sprites whenever the references are 2D or a 2D path can reach the visual bar. Not for props, distant background objects, or pixel-art games.
license: MIT
compatibility: Requires Blender (headless Python works) and a game engine or renderer that loads glTF 2.0 GLB files.
---

# Game builder Blender assets

Companion to the `game-builder` skill. Use it only when a homage game needs authored 3D meshes. Never build hero characters as in-engine procedural primitives (parented boxes, cylinders, debug foot discs, floating eye spheres).

## Rule

Only use 3D if needed. Prefer 2D, pixel art, or sprites whenever the locked refs are 2D or a 2D path can hit the Visual Bar, and use 3D only when the refs demand it. Do not default every camera hero to Blender and GLB.

When 3D is needed, go Blender-first for heroes and other camera-critical 3D characters. Author mesh, UVs, and a simple rig in Blender in isolation, export GLB, then bind the existing game systems (gait, AI, LOD). Keep in-engine procedural geometry only for props, crops, distant NPCs, billboards, and greybox while the Blender asset is in flight.

Author the final hero in Blender (headless Python is fine), not as raw Three.js or engine mesh code. Turnaround gates belong to the Orchestrator alone: never hand a visual PASS or FAIL to a peer agent.

## One asset per specialist

Do not batch camera-critical 3D models inside the game Builder. Each important mesh gets its own subagent whose only job is that asset.

| Role | Owns |
|---|---|
| Builder (from `game-builder`) | World, systems, loading and binding, Critic loop. Consumes finished GLBs |
| Asset specialist A | One hero body or character |
| Asset specialist B | One hero weapon or viewmodel (for example, a first-person rifle) |
| Asset specialist C | One camera-critical prop, vehicle, or set piece |

Rules:

1. One GLB brief per specialist. The prompt names a single noun ("the hero's rifle viewmodel", not "soldier, rifle, and watchtower").
2. High-definition craft relative to the locked-ref tier at camera distance: readable materials, correct silhouette, no stacked-primitive greybox as final. Sphere-mitten hands and slab guns are FAIL even if called "stylized".
3. The specialist ships an isolation turnaround and the GLB only. No game edits, no Critic, no world.
4. The Orchestrator gates each asset alone. Only after PASS does the Builder bind that GLB.
5. Run specialists in parallel where possible. Never serialize five meshes inside one Builder punch round.

## High-definition bar

For first-person viewmodels, walking heroes, and other assets that fill a large fraction of the frame:

- The silhouette reads as the real object class at a glance. A rifle has barrel, receiver, magazine, stock, and grip, not a grey bar.
- Hands have fingers, or clear glove mitts with the thumb wrapped around the control surfaces, not clusters of spheres.
- Surfaces carry painted albedo breakup (metal, wood, fabric) and edge wear, not flat fill.
- The triangle budget follows the locked-ref craft, not "as few boxes as possible". Around 5k to 40k triangles suits a hero viewmodel when the refs are near-photoreal first-person shooters; go lower only when `art/LOOK.md` locks a toy or low-poly look.
- A studio turnaround plus a still from the locked in-game camera (for example, the aim-down-sights crop) is required before PASS.

## When this skill applies

Decide from the locked refs' medium, not from genre alone. Skip by default unless 3D is clearly required.

| Situation | Path |
|---|---|
| Locked refs are pixel art or 2D, or 2D can hit the bar | Skip this skill. Use sprites, tile atlases, or generated 2D art. Do not force a GLB hero |
| Locked refs are 3D and the brief locks a 3D camera on a walking or tracked hero | Blender-first with this skill |
| Mixed refs, for example a pixel-art farming sim next to a 3D life sim | Prefer 2D unless the Orchestrator or user explicitly locks 3D |
| Uncertain | Skip Blender and ask the Orchestrator. Do not start a GLB pass "to be safe" |
| Hero weapon or vehicle silhouette at a locked 3D camera | Blender-first, only if the game is already 3D |
| Crates, fences, tools, billboard crops, background animals | In-engine procedural geometry or a generation pass is fine |
| Temporary greybox while a justified Blender hero is in flight | In-engine is fine; ledger it as `placeholder` |

If Stage C or a Diagnoser steer would sculpt a 3D hero from primitives inside the renderer, stop and run this skill, but only if 3D is needed. If the open failure is "looks like a bad 3D toy next to pixel-art refs", pivot the game to 2D instead of starting or continuing a Blender pass.

## Pipeline for a 3D hero

Do these steps in order. Do not retarget gait or ship walk stills until the turnaround gate passes.

### 1. Isolate in Blender

- Mesh, UVs, a simple humanoid rig, and a walk-ready bind pose.
- No world, no gait code, no game lighting in Blender.
- Headless Blender Python is fine when the host supports it.

### 2. Style target

- Match the game's 3D locked-ref craft tier (for example, readable low-poly at roughly 2k to 8k triangles for a cozy life-sim look), not a pixel-art SxS unless the game is actually 2D.
- Readable silhouette at the locked camera distance: large head, clear hat brim or hair, thick boots wider than the calves, a jacketed torso. Not a MetaHuman-style cinematic human unless the locked refs are that tier.
- Continuous skin at joints, with no air gaps between limb parts. Soften toy-brick and boxy silhouettes. On camera-critical assets (first-person gun, hero body), a toy-brick, boxy, or sphere-mitten result is an automatic FAIL.
- Palette from `art/LOOK.md`. Original names only. Never use franchise terms, and never feed refs as image-to-image input.

### 3. Export

- Prefer a single GLB (glTF 2.0) file: mesh plus skin, and optionally an idle clip.
- Skeleton: hips, spine, chest, neck, head; left and right clavicle, upper arm, forearm, and hand; left and right upper leg, leg, and foot (plus toe). Document the remap if bone names differ from the game's gait rig.
- Textures: a 512 or 1024 albedo atlas, plus an optional ORM map. Power-of-two sizes. Painted fabric, leather, or straw breakup, not flat fill plus grain alone.
- LOD: LOD0 alone is fine for a single gameplay camera. Add an optional LOD1 at half the triangles for crowds later.

### 4. Turnaround gate (before retarget)

Save these to the game's `artifacts/` folder:

- A bind-pose still (T-pose or A-pose)
- A turnaround: front, side, back
- Optional: 2 or 3 3D style refs in an internal SxS, for review only and never in the build. Prefer refs in the same medium; a pixel-art SxS is not the craft bar for a 3D hero.

The Orchestrator alone passes or fails this gate before any gait work. Do not ask a peer agent or another specialist for the verdict. PASS means that from the locked camera distance the asset reads as the intended class at high craft for that camera: not stacked primitives, sphere mitts, slab guns, or debug geometry.

### 5. Consume in the game

1. Load the GLB with `loadGLB(...)` or the engine equivalent.
2. Bind the existing continuous gait or animation system to the exported bones (retarget). Do not rewrite gait continuity to "fix" a bad mesh.
3. Delete the procedural or placeholder hero mesh.
4. Recapture the walk strip and key stills on the same mesh used for idle and walk.
5. Update `art/LEDGER.md` and `art/GENERATION-LOG.md` (source: the Blender GLB path, no model identifiers).

## Out of scope

- Forcing Blender or GLB on a 2D or pixel-art game. Use sprites.
- High-poly Unreal-style cinematic humans unless the locked refs demand that tier.
- Asking a peer agent for the turnaround PASS or FAIL.
- Rewriting gait continuity, or the whole world, to hide a bad mesh.
- Shipping a prettier idle mesh while the walk still uses the old procedural box-and-disc hero.
- Embedding franchise refs in the asset or the build.
- Batching several camera-critical meshes inside the game Builder.

## Orchestrator checklist

- [ ] Medium decided from the locked refs: 3D uses this skill; pixel art or 2D uses sprites and skips it
- [ ] The hero went Blender-first only because the game is 3D
- [ ] Each camera-critical mesh owned by its own specialist subagent
- [ ] GLB and bone remap documented
- [ ] Turnaround gate PASS by the Orchestrator alone, before retarget
- [ ] Idle and walk use the same mesh
- [ ] Ledger updated; Publish still LOCKED until the `game-builder` Critic WIN and harsh visual rules pass

## Relation to game-builder stages

- Stage A: lock the medium with the refs (2D pixel art or 3D). Do not plan a GLB hero for a pixel-art brief.
- Stage B: a greybox or placeholder hero is fine.
- Stages C3 and C5: camera-critical 3D characters go through this skill before the Critic's ART-PASS on those units.
- Stage D: punches that ask to "fix the mannequin in the renderer" escalate to this skill only if the game is 3D; otherwise escalate to sprite art.
