---
name: reduce-draw-calls
description: Use when a PlayCanvas application submits too many draw calls or frame time is CPU-bound — repeated meshes, dense grids, always-on interface elements — before hand-writing mesh merging or custom renderers.
---

# Cut draw calls, ranked by cost

Work the ladder in order and stop at the first rung that clears the budget. Each rung trades away
less flexibility than the next; skipping straight to a custom renderer or hand-written mesh merge
costs more engineering time than the draw calls it saves.

## Measure first

Read `app.stats.drawCalls.total` (or the `forward`/`depth`/`shadow` breakdown) before changing
anything, or drop in `MiniStats` for a live overlay. Every rung below is proved against this number,
not against intuition about what "looks expensive."

Draw count alone does not identify the bottleneck. Test sensitivity to pixel cost by halving the
effective pixel ratio (`Math.min(graphicsDevice.maxPixelRatio, window.devicePixelRatio)`) and calling
`app.resizeCanvas()`. Verify the backbuffer shrank and compare frame times at the same scene state.
If frame time improves materially, prioritize resolution, multisampling and per-pixel shader cost.
Otherwise profile CPU and GPU work before choosing a rung; restore the original ratio after the test.

## Rung 1: stop drawing invisible things

An element at opacity 0 still submits a draw call — its mesh instance exists and is still in a
layer, so the GPU processes it every frame for no visible result. Toggle `enabled` on the entity to
actually skip it. Check every element that is ever fully transparent, not only the ones on screen
when you're profiling — this rung is easy to skip precisely because nothing looks wrong.

## Rung 2: `BatchManager` — merge without touching shaders

`app.batcher.addGroup(name, dynamic, maxAabbSize)`, then set `batchGroupId` on each member's
component (render, sprite, or UI element). Use `dynamic: false` for geometry that never moves.

Contract: the `batchGroupId` setter only inserts into the batcher while `entity.enabled` is true,
and that flag requires both the local enable state and hierarchy attachment — set `batchGroupId`
after the entity is parented into the live tree, not before, or the member silently drops out of the
group. `BatchManager.generate()` runs once automatically on the app's first rendered frame; if group
membership changes afterward, call `app.batcher.markGroupDirty(id)` (or `generate([id])`) yourself.
An Engine-only app without the full `Application` bootstrap must register the class via
`AppOptions.batchManager` before it can batch anything.

## Rung 3: hardware instancing — merge without touching layout

Reach for this once distinct materials or per-frame transform updates would defeat `BatchManager`.
Build a per-instance vertex buffer with `VertexFormat.getDefaultInstancingFormat(device)` (one mat4
per instance), call `meshInstance.setInstancing(vb)`, and set `instancingCount`. A custom vertex
chunk needs its own `INSTANCING` code path with an identity-matrix fallback for the non-instanced
case (cross-reference `override-shader-chunks`).

Culling trade-off: instanced meshes cull as one unit against a single bounding volume — an
off-screen instance inside an otherwise-visible group still draws unless you opt in. Pass
`setInstancing(vb, true)` and set a `RenderComponent#customAabb` spanning every instance's world
extent so the renderer has something correct to cull against instead of culling nothing or
culling the whole group by one instance's bounds.

Adapt the official recipes rather than deriving the buffer layout or vertex-shader wiring from
memory: `graphics/instancing-basic` for the format/buffer contract, `graphics/instancing-custom` for
the vertex-shader side. Locate both at the installed engine version via `find-examples`.

## Prove and report

Verify the rendered image is unchanged with `verify-pixels` before calling the change done —
merging or instancing must not move a single pixel. Re-measure `app.stats.drawCalls` afterward and
state the before/after counts in the change description; "fewer draw calls" without numbers is not
a result.
