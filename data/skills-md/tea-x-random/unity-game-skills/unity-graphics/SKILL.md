---
name: unity-graphics
description: "Take a basic-looking Unity casual-iOS scene to a premium, intentional look. Use for URP setup, mobile rendering, lighting (baked lighting, light probes, reflection probes), materials and shaders (URP/Lit, URP/Unlit, GPU instancing, SRP batcher), post-processing (Volume, bloom, color adjustments, vignette), draw calls, batches, overdraw, quality settings, tiered quality, visual polish, art direction, and render quality. Triggers when screenshots look flat/primitive or the user asks for premium, stylized, polished, AAA-on-mobile, or less-basic 3D visuals on iOS."
---

# Unity Graphics (Casual iOS)

Own the render/visual pass for casual iOS games in Unity. Convert flat, primitive-looking screenshots into an intentional, stylized, performance-safe look that still hits 60fps on phones.

## The AAA visual bar (don't ship flat)

A premium look requires three things, and missing any one reads as amateur ("MS Paint"):

1. **Real textured surfaces, not flat fills.** Solid-color ground/background and procedural blobs are placeholders, not a look.
2. **Cohesive generated art across all primary surfaces** — ground, backdrop, hero props, and UI share one art direction.
3. **A properly LIT and composed scene.** A scene of raw sprites/meshes on a solid color stays flat until it is lit + composed.

Division of labor: **art direction, per-surface asset sourcing, and the visual scorecard are owned by `unity-aaa-graphics`** (the sibling skill that decides what art to generate and gates the result). **This skill provides the render-pipeline mechanics** — URP, lighting, materials, post — that you MUST actually apply on top of that art. Generating real art is necessary but not sufficient: raw assets dropped on a solid color still look flat until this skill's lighting + composition pass runs.

**Amateur anti-patterns to refuse:**
- Flat solid-color ground or background (use a textured surface + designed backdrop/gradient).
- Procedural SDF blobs standing in for primary surfaces or hero props (procedural is a fallback skin and for UI shapes — see below — not a substitute for real art).
- No lighting and no shadows — an unlit scene reads flat regardless of asset quality.
- A hard-oval vignette used as the only "lighting." Vignette is mood trim, not light.

## Core Doctrine (same spine as the rest of the unity-* set)

1. **Bias to a verified, screenshot-proven result, not docs.** A change is "done" when a `manage_scene` screenshot looks intentional and `manage_graphics` render stats stay in budget — not when a setting matches a tutorial.
2. **Keep gates lean.** Decide art direction and the URP/quality tier once, then proceed with sensible mobile defaults. Don't prompt at every slider.
3. **Edit through MCP, never raw YAML.** `.mat`, `.shader`, URP assets, lighting data, and `Volume` profiles are GUID/fileID YAML — hand-editing corrupts references. Go through `manage_graphics`, `manage_material`, `manage_texture`, `manage_shader`, `manage_scene`, and `execute_code`.
4. **Unity 6 render APIs differ from memory.** The model's built-in knowledge is ~Unity 2022.3. On Unity 6 (6000.x), RenderGraph, URP Volume components, and Renderer Features changed. Before writing any shader or render C#, verify against the live Editor with `unity_reflect` / `unity_docs` (enable the `docs` group). Trust order: reflection > project assets > docs > memory.
5. **Verify with two signals every pass:** a `manage_scene(action="screenshot")` AND `manage_graphics(action="stats_get")` render stats (draw calls / batches / SetPass / tris). One without the other is not verification.

## Step 0 — Confirm the pipeline before touching visuals

Read `mcpforunity://project/info` and check `renderPipeline`.

- **Casual iOS uses URP.** Not HDRP (too heavy for phones), not Built-in (no SRP Batcher, dated). If it reports HDRP or Built-in, flag it and plan a switch to URP.
- If `renderPipeline` is empty/Built-in and you want URP: install `com.unity.render-pipelines.universal` (via `manage_packages`), create a URP asset + Universal Renderer, and assign it in Graphics + Quality settings. Do this through `execute_code` driving `UniversalRenderPipelineAsset` + `GraphicsSettings.defaultRenderPipeline`, then `refresh_unity`. See `references/urp-mobile-recipes.md`.
- The `manage_graphics`, `manage_material`, `manage_texture`, `manage_shader` tools live in the `vfx` / core groups. If a call says the tool is unavailable, run `manage_tools(action="enable_group", group="vfx")` first. Volume / post-FX actions require URP (or HDRP) to be the active pipeline.

## Explicit input — art-spec.yaml drives palette, lighting, and post

When the project has an `art-spec.yaml` (canonical path + legacy roots in `docs/PIPELINE_CONVENTIONS.md`), this skill CONSUMES it — never improvise a scene-local look:

- **Palette:** materials, backdrop/skybox, and fog colors come from the spec's `palette` (semantic `palette.roles` first). `GameTheme.cs` color hexes MUST equal art-spec palette hexes exactly — colors only (typography/spacing/radii are GameTheme-native, no art-spec source).
- **Lighting:** implement the spec's `lighting` block (key/fill/rim/shadow/fog qualities). The key light's direction MUST match `craft.light_direction`, which equals composition.yaml `shadow_and_contact.key_light_direction` — ONE light direction shared by baked-in art, contact shadows, and the realtime sun. Do not invent a second source of truth for light direction.
- **Post & shaders:** the global Volume implements `rendering.post`; materials follow `rendering.shader_family`.

No art-spec (exploratory/prototype)? Proceed with this skill's defaults, flag the look as unlocked, and route to `unity-art-direction` before production art.

## Mobile-first lighting

Lighting is REQUIRED for a premium scene, not optional polish: raw sprites/meshes on a solid color
stay flat until they are lit and grounded with shadows. Never leave the scene unlit. That said,
realtime per-pixel lighting is the most common framerate killer on phones — default to baked.

- **Bake static lighting.** Mark static geometry, set lights to **Baked** (or Mixed only when you truly need a realtime caster), and bake lightmaps via `manage_graphics(action="bake_lighting")`. Baked GI gives soft, premium shading for free at runtime.
- **At most one realtime light**, ideally a single **directional** sun. Every extra realtime light multiplies draw cost; point/spot realtime lights on mobile are a last resort.
- **Light Probes** for moving/dynamic objects so they pick up the baked ambience instead of looking flat and detached. Place a probe group across the playable area.
- **Reflection Probes** sparingly — one baked probe for a shiny hero object is fine; blanketing the scene is not. Prefer baked, low-resolution.
- Shadows: keep one shadow-casting light, low cascade count (1), tight shadow distance, and hard or low-res soft shadows. Most casual scenes look great with baked AO and a single blob/contact shadow instead of full realtime shadows.

## Materials

- **URP/Lit** for surfaces that need real shading; **URP/Unlit** for stylized flat-color/gradient art. Unlit is the cheapest path and looks intentional for hyper-casual — lean on it.
- Enable **GPU Instancing** on every shared material (`enableInstancing`) so repeated props batch.
- Keep materials **SRP Batcher compatible** (URP shaders are by default; custom shaders must use a CBUFFER `UnityPerMaterial` block). SRP Batcher + GPU instancing are how you keep draw calls low.
- Keep **material and texture variants low** — fewer unique materials = fewer SetPass calls. Share one atlas/material across many objects.
- Author with `manage_material` (create, set shader, set `_BaseColor`/`_BaseMap`/`_Smoothness`/`_Metallic`, toggle instancing). Compress textures with `manage_texture` (ASTC for iOS).

## Post-processing on mobile (conservative)

A premium frame is lit AND tone-mapped: apply a mobile-safe post pass — don't leave the scene raw.
Post is a force-multiplier for "premium" but only if you stay cheap. (Vignette is mood trim layered
on top of real lighting, never the lighting itself.)

- Use **one global `Volume`** with a profile. Enable post on the renderer asset and tick **Post Processing** on the Camera.
- **Safe, cheap-ish:** Bloom (low threshold, modest intensity), Color Adjustments / White Balance / Tonemapping (ACES or Neutral), Vignette, slight Lift/Gamma/Gain. These define the mood.
- **Avoid on low-end phones:** SSAO, Depth of Field, Motion Blur, Chromatic Aberration at strength, full-res Bloom. They cost fill rate the GPU doesn't have.
- Tonemapping on a clean color palette does most of the work. Add bloom last, sparingly, on emissive accents only.

## Performance-safe visual detail (look premium cheaply)

Detail you can afford on a phone:

- **Stylized flat-color / gradient** palette instead of PBR realism — reads as "designed," batches well, no heavy textures.
- **Bake AO into textures / vertex colors** so shading looks grounded with zero realtime cost.
- **Vertex colors** for cheap per-object tinting and gradients without extra materials.
- **Fog** (linear/exponential) for depth and to hide draw distance — a strong, near-free mood tool.
- **Billboards / impostors** for distant detail (trees, clouds, crowds) instead of real geometry.
- **Particle pops / juice** (collect, land, win bursts) for perceived quality — small, short-lived, additive.
- A skybox or gradient backdrop + a clear focal palette beats any amount of glow on primitives.

Build forms and palette first; add bloom/particles last. Glow on primitives is not premium.

**Procedural sprites as a FALLBACK skin (2D, no art needed).** Real generated art (see
`unity-aaa-graphics`) is the default and the upgrade; this procedural path is the PLACEHOLDER for
when an asset-generator key is MISSING or quota-blocked. It is also legitimately useful for **UI
shapes** (rounded cards, buttons, dividers) even alongside real art. A rounded-rect sprite from a
signed-distance field into a `Texture2D` (soft anti-aliased alpha edge), created once and reused via
a 9-slice `Image` (`Sprite.Create(..., border)` + `Image.type = Sliced`), gives crisp rounded
corners at any size. Tint comes from `Image.color`, so highlights still work. Pair with the warm
palette above and the board/buttons read as designed cards, not flat rectangles. Swap in generated
art through the same `Image.sprite` slot as soon as a generator key is available.

When art is genuinely blocked (no image-gen key / quota), the same SDF approach yields a **coherent
placeholder skin** with zero external assets: rounded-rect 9-slice tiles/buttons **and recognizable
icon tokens** — e.g. a simple character/mascot face composited from circle/ellipse SDFs with proper
**alpha-over blending**. **Cache each generated `Sprite` in a static field (generate once)** so you
pay the rasterization cost a single time, and tint per-use via `Image.color`. This keeps a colorful,
cohesive board on screen with no external assets — but treat it as a stopgap, NOT a premium look.
Flat fills and procedural blobs are not a substitute for real textured, lit art; restore the
generated-art path (`unity-aaa-graphics`) the moment the generator is unblocked.

**Procedural icon library for action bars / HUD (fallback when art is blocked).** Beyond shapes, you can
draw a clean vector-style **icon set** at runtime — lightbulb, undo arrow, trash, home, heart — at ~256px
from SDF primitives (circle, rounded box, thick segment/capsule, plus union/subtract), rendered
**white-on-transparent** so each tints via `Image.color` and is anti-aliased by edge coverage. Cache each
once in a static field. This reads like a real game-icon set with **no external assets** and is a solid
stand-in for HUD/icon glyphs when a generator key is missing — prefer generated icon art
(`unity-aaa-graphics`) when available. Present them as **themed icon buttons** — palette-tinted rounded
tile + dark icon + label — which read far better than plain white buttons for near-zero cost.

**Region/grid borders (Queens/Sudoku/region-map puzzles).** Draw **bold dark dividers only on region
BOUNDARIES** — an edge where a cell's 4-neighbor is a different region or the board edge — and thin
light gridlines elsewhere; this contrast is what makes a colored region read as one solid blob
instead of loose cells. Implementation that works: per-cell thin `Image` strips on boundary edges
only, each strip's **pivot CENTERED on the edge** so it straddles the cell-spacing gap and meets the
neighbor's strip as one continuous thick line — no global texture alignment needed. Only boundary
edges get strips, so it stays perf-friendly.

**Cohesive themed art direction (when asked for ANY named look).** A theme-neutral recipe that reads as
intentional, regardless of the aesthetic requested: a single unified **GROUND** treatment + a single
unified **PANEL** treatment + a deliberately limited, coherent **palette** (chosen so gameplay regions
stay distinguishable for puzzle readability) + generous **negative space** + one or two **signature
motifs**, with **gloss and saturation dialed to match the chosen theme** (high gloss/candy for playful,
low gloss/muted for minimal). The recipe is the same across themes — only the tokens change: e.g.
zen-minimal, neon-retro, watercolor-storybook, or flat-pastel all plug the same slots (ground, panels,
palette, motif). Because the whole look flows from the palette, a token swap in **one theme
ScriptableObject reskins the entire game instantly** — author themes as data, not per-element color.

**Flat-2D depth kit (fallback that lifts a flat board off "MS Paint" with zero art).** Three cheap
procedural overlays, each generated once and cached in a static field: (a) a vertical **2-stop
gradient backdrop** (a tiny `Texture2D` stretched full-screen) instead of a flat fill; (b) a radial
**vignette** overlay (transparent center → dark edges, ~0.5 strength), full-screen and non-raycast;
(c) soft **drop shadows** = an offset dark rounded-rect `Image` inserted directly BEHIND a panel via
`SetSiblingIndex(targetIndex)`. Together they add depth and focus on a 2D uGUI board when no art is
available. The gradient backdrop is a baseline minimum (never ship a flat solid fill), but this kit
is a fallback, not the premium target — generated backdrop/surface art (`unity-aaa-graphics`) plus a
lit, composed scene is the upgrade.

## Quality settings & tiered quality

- Define quality tiers (e.g. **Low** for old devices, **High** for recent) differing in shadow distance/resolution, MSAA, render scale, pixel light count, and post-FX enabled.
- On iOS, gate by device class at startup and pick the tier (`QualitySettings.SetQualityLevel` via `execute_code`).
- Old-device tier: render scale < 1.0, no MSAA or 2x, shadows off or blob-only, post = tonemap + vignette only. New-device tier: render scale 1.0, MSAA 2–4x, baked shadows, bloom on.

## Budgets & verification (target 60fps)

- Pull stats with `manage_graphics(action="stats_get")` — watch **draw calls / batches / SetPass calls / triangles / overdraw**.
- Casual-iOS rough budgets: keep batches low (tens, not hundreds), SetPass calls minimal via SRP Batcher + instancing, tris modest, and overdraw under control (transparent/particle overlap is the usual culprit).
- Every visual change: `manage_scene(action="screenshot", include_image=true)` to confirm it looks intentional, then `stats_get` to confirm it stays in budget. If a screenshot is dominated by primitives or flat planes, it's not done.

## Basic scene → premium casual look (recipe)

Premium = real generated art (sourced via `unity-aaa-graphics`) ON the surfaces, with ALL of the
mechanics below actually applied on top. Skipping the lighting/backdrop/post steps leaves the scene
flat even with good art.

1. Confirm URP active (Step 0); enable `vfx` group.
2. Set the palette from art-spec `palette.roles`/arrays (no spec: a deliberate 3–6 color choice): stylized **URP/Unlit** or **URP/Lit** flat-color materials, GPU instancing on.
3. One directional light aimed per the spec's `craft.light_direction` / composition `key_light_direction`, **Baked** + Light Probes for movers; `bake_lighting`.
4. Add **fog** for depth and a gradient/skybox backdrop.
5. Add a global **Volume**: Tonemapping (ACES), gentle Color Adjustments, Vignette, low Bloom on emissive accents only.
6. Add **particle pops** on key gameplay events for juice.
7. Screenshot + `stats_get`; trim materials/overdraw until 60fps and the frame looks designed, not primitive.

## References

- `references/urp-mobile-recipes.md` — ordered MCP / `execute_code` recipes: URP install + asset/renderer, mobile-friendly URP asset (shadows/HDR/MSAA tradeoffs), stylized unlit material, baked lighting workflow, conservative post Volume.
- `references/checklists/mobile-render-quality.md` — render-quality gate before claiming premium.
- `references/checklists/perf-safe-visual-detail.md` — cheap-but-premium technique checklist.

## Final Response

Report the pipeline confirmed (URP), lighting approach (baked + probes), material/instancing/SRP-batcher state, post-FX used (and what was deliberately avoided), before/after render stats, and the verifying screenshot. State "loaded" vs "executed" precisely. Do not claim premium without a real, non-primitive screenshot plus in-budget stats.

## Field notes & lessons

- Framed procedural-SDF guidance as a FALLBACK skin (key missing / quota-blocked), not a premium path — rounded-rect 9-slice tiles/buttons plus icon tokens (e.g. a simple character face) composited from circle/ellipse SDFs with alpha-over blending, statically cached (generate once), tinted via `Image.color`. Real generated art (`unity-aaa-graphics`) is the default and the upgrade.
- Added region/grid borders (bold dividers only on region boundaries via edge-centered-pivot `Image` strips) and a flat-2D depth kit (gradient backdrop + radial vignette + behind-panel drop shadow, statically cached).
- Added procedural icon library (lightbulb/undo/trash/home/heart from SDF primitives, white-on-transparent so they tint via `Image.color`, statically cached) and themed icon buttons (tinted tile + dark icon + label) over plain white buttons.
- AAA-casual action buttons are LAYERED, not flat. Recipe: SoftDisc drop-shadow (dark, offset down) + tintable ShadedCircle "ball" (grayscale with a top→bottom value gradient so a flat `Image.color` reads as 3D) + a SEPARATE white TopGloss specular overlay (key: multiply-tint can't brighten past the tint, so bake the specular as its own white low-alpha sprite on top) + bold white icon + label. This layered round-glossy-button-with-shadow recipe gives a dimensional, "made-by-a-studio" button when that's the look you want (keep buttons flat rects if the direction is minimal).
- Added a cohesive themed art-direction recipe (theme-neutral: ground + panels + limited palette + negative space + signature motif; gloss/saturation matched to the theme); the look flows from the palette so one theme-object swap reskins the whole game.
