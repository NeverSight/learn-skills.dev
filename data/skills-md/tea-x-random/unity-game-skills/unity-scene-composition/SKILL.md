---
name: unity-scene-composition
description: "Define and enforce Unity scene composition before asset generation or assembly. Use for composition.yaml, camera projection/yaw/pitch/lens/framing, visual layers, focal path, negative space, big-medium-small rhythm, prop density/distribution, color zones, occlusion budgets, contact shadows, BeautyCell/golden screens, registry asset placement, or scenes that are mechanically correct but visually weak. Covers sprite-on-3D/2.5D pixel density, Y-axis billboarding, feet pivots, blob shadows and quarter-view framing; diagnoses pasted-on, floating or mismatched-chunkiness sprites; and runs deterministic scene measurements plus visual critique. Pair with unity-game-layout, unity-asset-pipeline, unity-art-direction, unity-graphics and unity-ui-designer."
---

# Unity scene composition

This skill owns the **visual hierarchy contract** for scenes. `unity-game-layout` makes coordinates/boards/grids correct; this skill makes the screen read like a finished game: clear focal path, controlled density, foreground/midground/background depth, deliberate color zones, and screenshot-tested composition.

> Do not generate production assets or assemble a scene until `composition.yaml` exists and agrees with `art-spec.yaml` and each asset's `camera_contract`. Asset contracts without a composition contract still let agents improvise scale, angle, density, and visual role.

## Inputs

- `Assets/<Game>/Art/_ArtDirection/art-spec.yaml` (`unity-art-direction`) — style_id, craft block (`finish`, `pixels_per_unit`, `light_direction`), palette, material, lighting, camera intent, mobile budgets. (Canonical paths per `docs/PIPELINE_CONVENTIONS.md`; probe legacy roots `Assets/GameArt/` and `Assets/Art/` on existing projects.)
- `Assets/<Game>/Art/Approved/registry.yaml` (`unity-asset-pipeline`) — approved prefabs and their composition roles/budgets (`composition.layer`, `visual_weight`, `density_cost`, `allowed_zones`, `target_screen_height_percent`).
- Level/gameplay requirements (`unity-gameplay-systems`, `unity-game-layout`) — playable path, grid/board, interactables, spawn zones, UI safe area.

## Output: `composition.yaml`

Create `Assets/<Game>/Art/_ArtDirection/composition.yaml` from `references/composition-template.yaml`. Its `style_id` must equal the art-spec `style_id` verbatim, and `shadow_and_contact.key_light_direction` must equal art-spec `craft.light_direction` — string inequality is a validation failure. It must define:

- **camera profile** — projection, yaw, pitch, lens/ortho size, framing, target device aspect;
- **visual layers** — background, far, midground, gameplay, foreground, UI;
- **focal path** — first/second/third read and how the eye travels;
- **shape rhythm** — big/medium/small ratio and silhouette spacing;
- **density rules** — interesting-object budget per screen and per layer;
- **color zoning** — quiet gameplay area vs saturated reward/focal area;
- **occlusion budget** — how much foreground can obscure play;
- **shadow/contact rules** — direction, softness, contact-darkening strength;
- **family distribution** — how many members/variants of each approved family per screen;
- **screenshot tests** — target frames and acceptance gates.

## Workflow

1. **Lock the camera first.** Choose a single gameplay camera profile for the BeautyCell and first playable slice. Record projection/yaw/pitch/lens/ortho size in `composition.yaml`; every asset `camera_contract` must match it unless explicitly marked UI/background.
2. **Assign visual layers.** Put gameplay-critical objects in `gameplay`; decoration in `midground`/`background`; atmospheric occluders in `foreground` with a strict occlusion budget; UI in safe-area-aware `ui`.
3. **Define the focal path.** Write three reads: (1) main gameplay goal, (2) next action/reward, (3) world flavor. If the first read is not gameplay, fix color/scale/light before adding more assets.
4. **Budget density.** Give each object a `density_cost` (small=1, medium=2, large/hero=3) and set a per-screen max. Do not solve an empty scene by scattering random props.
5. **Zone color and contrast.** Reserve highest saturation/contrast for interactables, rewards, and focal accents. Backgrounds and filler props must recede.
6. **Place only registry assets.** Read `unity-asset-pipeline` registry entries, filter by `composition.layer`, `visual_weight`, `allowed_zones`, and `density_cost`; never drag source art or unapproved prefabs into the scene.
7. **Normalize scale + grounding.** Set target screen-height percent per role and apply one shared `shadow_profile`/contact-darkening rule. Foreground actors/props without a consistent contact shadow read as floating stickers.
8. **Capture screenshots + run the automated pass — mandatory on EVERY composed-scene screenshot.** Capture via `unity-mcp-bridge` `manage_camera(screenshot)` or the BeautyCell renderer, then split the check:
   - **Numeric budgets are MEASURED from Unity scene data via MCP, never eyeballed and never VLM-scored:** sum registry `density_cost` of renderers in the gameplay-camera frustum vs `density_budget`; project renderer bounds to the viewport for foreground occlusion vs `occlusion_budget` and per-role screen-height % vs `shape_rhythm`; cross-check every visible renderer against `registry.yaml` (unmatched = unapproved unless flagged placeholder). Procedure + C# snippets: `references/scene-measurement.md`. A budget violation is a hard failure — fix per step 9.
   - **The VLM scores only qualitative dimensions** (focal read, layer contrast, grounding, cohesion): `critique_image.py <screenshot> --scene-mode --subject "<scene intent>" --reference <golden screen> --art-spec <spec>` (`unity-image-generator`). During calibration, a low scene score triggers a re-roll or manual review — not a hard block.
   Record both results per `references/screenshot-acceptance.md`.
9. **Iterate by moving/removing first, not generating more.** If composition fails, fix camera, scale, contrast, density, and layering before generating additional assets.

## Layer rules

- **Background:** low contrast, low detail, no hard edges competing with gameplay. Supports mood only.
- **Far:** depth hints/parallax shapes; never occludes play.
- **Midground:** readable props and obstacles; primary place for environment kit variation.
- **Gameplay:** path, units, player, enemies, puzzle pieces, interactables. Highest readability.
- **Foreground:** optional framing/vignette elements; strict occlusion budget (usually 0–8% of gameplay area).
- **UI:** safe-area aware; uses a related but more legible material/color treatment; never fights gameplay focal path.

## Big / medium / small shape ratio

A premium screen usually needs shape hierarchy: 1–2 big anchors, 3–6 medium supports, and many small details only where the eye can rest. If every prop is the same screen height, the scene reads like a sticker pile. Encode target screen-height ranges in `composition.yaml` and enforce through asset `target_screen_height_percent`.

## Layer contrast budget

Do not apply one identical prompt/style intensity to every layer. The background/ground must usually spend **less** contrast, outline, and saturation budget than gameplay:

- gameplay/interactables: highest contrast, strongest outline, most saturated accents;
- hero/foreground props: high readability, but fewer than gameplay-critical objects;
- midground/filler props: medium contrast, lower density;
- background/ground: low contrast, low saturation, sparse detail, thin/no outline.

If a ground tile has the same bold black outline and hot accent palette as characters, the screenshot will look busy even when each asset is well drawn. Fix layer contrast before adding post-processing.

## Repeating surfaces (scrolling games)

Two scorecard deductions that recur in side-scrollers/runners:

- **Repeating backgrounds:** a single background panel tiled 2x+ across the view exposes its internal features (star rows, cloud bands, silhouette clusters) as visible periodic banding — the eye locks onto the repeat immediately in motion. For scrolling games, generate **2+ background variant panels and alternate them A-B-A-B**, or require the panel's internal features to be non-periodic (no evenly spaced rows/bands) before approval.
- **Ground band proportion:** a uniform ground texture filling the lower quarter+ of the screen reads as empty dead space. Cap the flat ground band at **~1/6 of screen height**, or require a **top-edge accent row** (grass lip, highlight course, trim tiles) where the gameplay line meets the band so the boundary reads as designed, not truncated.

## Contact shadows / grounding

Every object that touches the world needs a consistent grounding treatment. Prefer a shared soft blob shadow or contact-AO prefab referenced by `shadow_profile`, with one global light/shadow direction. Do not rely on shadows baked into individual generated PNGs — they disagree once composited and break the BeautyCell.

## One pixel density (Rule 0 — sprite and 2.5D scenes)

The #1 amateur tell in sprite/2.5D scenes is mixing pixel resolutions: chunky point-filtered sprites standing on a smooth, high-res, bilinear ground. Each asset looks fine alone; the frame reads as two different games. Everything visible must share **one effective pixel size on screen**:

- **Ground texel size == sprite pixel size.** Tile ground textures so `texels_per_unit = textureWidthPx / (groundWorldUnits / tiling)` ≈ the project PPU (`art-spec.yaml:craft.pixels_per_unit` — never a local value), then fine-tune by screenshot. (Verified: a 2816px texture on a 50-unit plane needed `mainTextureScale ≈ 3` to match 100-PPU sprites.) Measured check: `references/scene-measurement.md`.
- **One filter mode.** Pixel track: point-filter EVERYTHING — sprites AND ground/tileset — mipmaps off. A bilinear ground under point sprites is the classic mismatch. (Import mechanics: `unity-pixel-art` / `unity-asset-pipeline`.)
- **One light model across sprites and 3D ground.** If sprites are unlit (flat, bright), make the ground unlit too (URP/Unlit); never light one and not the other. Record the choice in `composition.yaml:pixel_density.light_model`.

If a composed sprite scene "looks horrible," fix this before touching anything else.

## Sprite-on-3D (2.5D) assembly

For billboard sprites standing on 3D ground (Ragnarok/HD-2D look):

- **Billboard Y-axis ONLY** — the sprite yaws to face the camera but stays upright (`LookRotation(horizontal_dir_to_camera, up)`); never pitch it toward the camera or sprites lie down as the camera tilts.
- **Pivot at the feet** (bottom-center, from autocropped alpha — contract-enforced by `unity-asset-pipeline`) and place the actor at ground `y=0`, so the billboard rotates about the feet and stays planted.
- **Soft blob shadow** quad on the XZ plane under every actor, sorted below the sprite, using the shared `shadow_profile` — without it billboards read as pasted-on stickers.
- **Quarter-view framing:** orthographic camera, fixed downward pitch (~48°); the hero at ~25–30% of screen height — `orthographic_size ≈ heroWorldHeight / (2 × targetScreenFraction)` (keep it inside `shape_rhythm.target_screen_height_percent.hero`). Tight framing also hides ground-tiling repetition; a distant camera makes the hero a speck in wallpaper.

## Screenshot acceptance

Do not rely on prose. A composition pass includes screenshots at the target device aspect plus at least one alternate aspect, the deterministic scene measurement (`references/scene-measurement.md`), and the scene-mode VLM critique. Use `references/screenshot-acceptance.md` (measured gates vs scored dimensions) and record the screenshot paths + measurement JSON in the BeautyCell or scene QA report. A scene that only passes in Scene View is not approved.

## Relationship to other skills

- `unity-game-layout`: grid/board/world-coordinate correctness. Use first for collision/placement logic, then this skill for visual hierarchy.
- `unity-asset-pipeline`: approved registry + asset contracts; this skill consumes registry assets and writes composition constraints back into contracts.
- `unity-art-direction`: global style/palette/material/camera intent; this skill turns it into screen-space rules.
- `unity-graphics`: lighting/post/material implementation; this skill specifies what lighting must communicate.
- `unity-ui-designer`: UI readability/safe area; this skill allocates UI's visual role in the whole frame.
- `unity-pixel-art` / `unity-image-generator`: sprite production (transparency, pivots, import); this skill owns how those sprites sit in a scene (one pixel density, billboarding, grounding, framing) and the scene-mode critique gate.
- `unity-pixel-art` + `unity-graphics`: provide pixel-native assets and sprite-on-3D/HD-2D rendering while this skill owns density, billboarding, and grounding.
