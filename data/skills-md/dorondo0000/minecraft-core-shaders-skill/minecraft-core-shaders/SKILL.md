---
name: minecraft-core-shaders
description: Build vanilla-Minecraft "core shader" resource packs — GLSL packs that add features the game has no API for (HUDs, minimaps, waypoints, SSAO, bloom, colored lights, portals, GUI player models, video players, FPS view models, Shadertoy ports). Use when the task mentions core shaders, vanilla shaders, .vsh/.fsh in a resource pack, post_effect / post effect pipelines, moj_import, rendertype_* shaders, data markers, lightmap uniforms, map-based HUDs, BetterHUD/BetterModel/objmc/ItemsAdder shader overlays, or "do X in Minecraft without a client mod".
---

# Minecraft Core Shaders

## What this is

Minecraft's Java client compiles the GLSL under `assets/<ns>/shaders/` from the active
resource pack. A resource pack can therefore **replace the renderer's own shaders**. That is
the only sanctioned client-side programmability in vanilla Minecraft, and an entire
engineering discipline has grown around it: because the pack cannot receive any new data
from the game, everything is done by **smuggling data through channels the vanilla renderer
already has** (texture pixels, vertex colors, world coordinates, the lightmap, game time,
render-target pixels) and by **hijacking geometry** the game was going to draw anyway.

Two hard truths shape every design:

1. **You get no new inputs.** No custom uniforms from the server, no compute shaders, no
   SSBOs, no `imageStore`, no reading back to the CPU. Every "new" value must ride in on an
   existing uniform, vertex attribute, texture, or framebuffer.
2. **The syntax is version-locked.** Between 1.20.4 and 26.3, Mojang changed the shader
   file layout, the include names, the uniform delivery mechanism, the post-effect JSON
   schema, and even the vertex-index builtin — several times. A shader that is correct for
   1.21.1 will not compile on 1.21.6. **Fixing the target version is step zero of every
   task.**

## Step zero, always: pin the version

Before writing a single line, establish the target Minecraft version and its
`pack_format`. If the user did not say, **ask** — do not guess. Then read
`references/version-matrix.md` and work only inside that generation's rules.

Quick orientation (full table in the matrix file):

| Gen | pack_format | MC | Uniform delivery | Core `.json` in pack? | Post-effect schema |
|---|---|---|---|---|---|
| G1 | ≤41 | 1.20.x–1.21.1 | loose `uniform` + per-rendertype `.json` | yes | `shaders/post/*.json`, `targets` **array**, `intarget`/`outtarget`/`auxtargets` |
| G2 | 42–55 | 1.21.2–1.21.5 | loose `uniform` + `.json`, `defines` added, `ChunkOffset`→`ModelOffset`, namespaced imports | yes | `post_effect/*.json`, `targets` **object**, `program` + `inputs` |
| G3 | 56–68 | 1.21.6–1.21.8 | **UBO includes**, fog API rewritten | **no** | `post_effect/*.json`, `vertex_shader`/`fragment_shader`, UBO `uniforms` |
| G4 | 69–~80 | 1.21.9–26.1 | G3 + `chunksection.glsl`, `PER_FACE_LIGHTING` | no | as G3 |
| G5 | ~81–93+ | 26.2–26.3 | G3 + `gl_VertexIndex`, `layout(location=)` in post | no | as G3, plus server-toggleable named post effects |

## How to work

1. **Pin the version** (above) and write it into `pack.mcmeta`.
2. **Get the vanilla shader source for that version.** Overriding a core shader means
   shipping a complete file, so you need the original. If it is not already at hand, **ask
   the user to fetch a core-shader template pack for the exact target version** (they are
   published for every release) or to extract `assets/minecraft/shaders/` from the client
   jar. One request up front removes all the guesswork that follows.
3. **Place the effect on the frame timeline.** `references/frame-anatomy.md`. This decides
   what is possible at all — a post pass cannot touch the hand or the GUI, a data marker
   must be drawn before it is read, and post pipelines need Fabulous graphics.
4. **Check feasibility.** `references/limits.md` for the hard "never" list and the cost
   class. Say "impossible" or "this needs an extra scene render" early, not late.
5. **Pick the carrier.** Which render type will you hijack, and what attributes does it give
   you? `references/rendertype-inventory.md`.
6. **Pick the data channel.** What must the shader know that it cannot see?
   `references/data-channels.md` — choose the cheapest channel that carries enough bits.
7. **Start from a working skeleton.** `references/worked-examples.md`. Get it running and
   verified *before* adding your own logic.
8. **Write the shader for that generation only.** Boilerplate from
   `references/version-matrix.md`, transforms from `references/spaces-and-uniforms.md`.
   Never adapt boilerplate from another generation from memory.
9. **Build the server half** if the effect needs one: `references/server-side.md`.
10. **Keep features from colliding** once there are more than two or three:
    `references/composition.md`.
11. **Measure anything you are unsure about** rather than guessing:
    `references/instrumentation.md`.
12. **Multi-version support, if asked:** `overlays` plus stub includes — see "Shipping one
    pack for many versions" in `references/version-matrix.md`.
13. **Run the checks** in `references/pitfalls.md` and the shipping checklist in
    `references/new-projects.md` before declaring done.


## Reference index

Read the file that matches the sub-problem; do not read all of them.

**Foundations — read these before designing anything.**

| File | Read it when |
|---|---|
| `references/version-matrix.md` | **Always.** Per-version file layout, includes, uniforms, JSON schemas, boilerplate for every generation. |
| `references/frame-anatomy.md` | **Always.** What is drawn when, which target it lands in, which hook can reach it. Decides what is even possible. |
| `references/spaces-and-uniforms.md` | **Always.** Coordinate spaces, what each uniform actually contains, pass detectors. The largest source of silent bugs. |
| `references/rendertype-inventory.md` | Choosing which render type to hijack, what attributes it gives you, and how to reproduce the vanilla shader you are overriding. |

**Doing the work.**

| File | Read it when |
|---|---|
| `references/techniques-index.md` | **Read early on anything non-trivial.** The complete idea catalog — 140+ numbered tricks with code, from data smuggling and rasteriser abuse to preprocessor DSLs, shading methods and numerical robustness. Browse before designing; grep when stuck. |
| `references/worked-examples.md` | Starting a pack. Three complete, compilable skeletons (G3 HUD, G2 data marker + post, G5 toggleable post effect). Copy one, verify it runs, then mutate. |
| `references/data-channels.md` | Getting a value into a shader: data markers, lightmap packing, GameTime, magic pixels, vertex color, coordinate encoding, map colors, post-effect toggles, cross-frame state. |
| `references/geometry-hijacking.md` | Drawing something the game wasn't going to draw there: screen-space HUDs, waypoints, billboards, voxelization, fullscreen canvases. |
| `references/encodings.md` | Packing floats/ints/colors into RGBA8; LogLuv HDR; YCoCg; map-palette bytes; precision tiers; tone mapping; dithering. |
| `references/postfx-cookbook.md` | Building a post pipeline: SSAO, bloom, motion blur, temporal reprojection, portals, shadows, voxel colored lighting, minimaps, mip pyramids. |
| `references/gpu-ui.md` | Drawing text/UI entirely in GLSL: bitmap fonts, seven-segment digits, panel layout, anchoring, DPI scaling, text-effect systems. |
| `references/mesh-tricks.md` | Arbitrary meshes and models: objmc, raytraced player models, marker models, atlases, item-model plumbing per version. |
| `references/composition.md` | The pack has more than two or three features. Feature-module contract, dispatch ordering rules, the varying budget and how to compress it, magic-value registry, per-feature `#define` isolation, shared state, merging with plugin-generated packs. |
| `references/server-side.md` | The other half: display entities, `custom_model_data` per version, maps, bossbars, fog control, timing and latency, what belongs server-side. |

**Verifying, diagnosing, deciding.**

| File | Read it when |
|---|---|
| `references/instrumentation.md` | **Anything doesn't work and you can't see why.** Frame capture with RenderDoc/Nsight (injected by a Fabric mod) — the real debugger: full draw list, every render target at every step, live uniform values, post-vertex positions, pixel history. Plus in-shader instrumentation, bisection, reading an unfamiliar pack, measuring a new MC version, and performance attribution. |
| `references/limits.md` | Judging feasibility: hard "never" list, texture/target ceilings, per-pass and per-vertex budgets, channel bandwidth, compatibility ceilings. |
| `references/pitfalls.md` | Something doesn't render, flickers, breaks on Sodium/Iris, or works only on NVIDIA. |
| `references/architectures.md` | Case studies of ten real shipping projects — what each is, how it works, what it cost. |
| `references/new-projects.md` | Designing a brand-new pack: feasibility triage, channel/carrier selection, worked designs, effort estimates. |

## Optional: reference material on disk

This skill is self-contained. Every technique, kernel and constant table is written out in
the references; nothing here requires files on disk.

Two things are still worth asking for once per task, because they remove guesswork:

1. **The vanilla shader source for the target version** — a core-shader template pack, or
   `assets/minecraft/shaders/` extracted from the client jar. Required to override a core
   shader correctly (`rendertype-inventory.md § 4`).
2. **Any reference packs the user already has.** Useful as ground truth for version-specific
   syntax and as a source of binary assets (noise textures, palettes, sprite sheets) that
   cannot be written out as text. Read them with `instrumentation.md § 4`.

If neither is available, proceed — the references stand alone.

## Non-negotiables

- **Never mix generations.** `#moj_import <fog.glsl>` and `#moj_import <minecraft:fog.glsl>`
  belong to different eras; `linear_fog` and `apply_fog` do too. Mixing produces a silent
  black screen or a compile error dumped only to `latest.log`.
- **Never invent uniforms.** If a uniform is not in that version's built-in set (or, on
  pre-1.21.6, declared in the pipeline `.json`), it does not exist. The list is in the
  matrix file.
- **Never assume a render target is cleared.** Post targets keep last frame's contents
  unless written. This is a bug source *and* the basis of all cross-frame state.
- **Always guard magic values.** Any "magic pixel" or "magic color" test must be exact
  (`ivec` comparison after `round`), and any decoded state must be validated against a
  known constant before use, or garbage will be interpreted as data.
- **Respect other people's code.** The techniques here are described so they can be
  reimplemented, not copied. If you do lift a block of GLSL from a specific pack, check its
  licence and keep its attribution comments.
