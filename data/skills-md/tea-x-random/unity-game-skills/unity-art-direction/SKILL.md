---
name: unity-art-direction
description: "Establish and enforce one art-direction system for a Unity game. Use to choose a style, write/approve art-spec.yaml, define style_id, camera, shape language, palette, materials, lighting, scale, triangle/texture/bone budgets and acceptance gates, create AssetBriefs, select golden assets, generate families with controlled variants, or diagnose inconsistent AI art. Routes pixel work through PixelLab anchors and non-pixel/3D work through approved turnarounds, technical cleanup, contracts, Unity validation scenes and quality gates. Owns the style preset/spec templates and coordinates unity-asset-designer, unity-aaa-graphics, generators, unity-asset-pipeline and unity-graphics."
---

# Unity art direction

Produce an **art-directed game**, not a folder of individually attractive AI assets. Every generated asset is a member of **one visual language**, defined once in `art-spec.yaml` and obeyed by every image, mesh, material, VFX, UI element, and screenshot.

> **AAA quality means** a coherent hierarchy, strong silhouettes, controlled materials, polished lighting, readable gameplay, and deliberate composition. It does **NOT** mean ultra-dense meshes, photoreal textures, or expensive post. A solo iOS team hits "premium" through *coherence and discipline*, not scope.

This skill is the **system**: the locked spec, the style-preset catalog, the mobile budgets, and the production discipline. It complements the other art skills:
- **`unity-art-direction`** (here) — the `art-spec.yaml` SSOT, style presets, budgets, the golden-asset/family pipeline, quality gates.
- **`unity-asset-designer`** — the on-model reference/turnaround/icon sheets craft that this pipeline's "approved multi-view" step calls for.
- **`unity-aaa-graphics`** — per-surface "generate everything" sourcing, the AAA prompt library/genre kits, and the visual scorecard that fails amateur scenes.
- **`unity-asset-pipeline`** — the hard gate from generated source art to approved runtime prefabs: asset contracts, import QA, prefab factory, BeautyCell screenshots, and the approved-asset registry.
- **`unity-scene-composition`** — the screen-space composition contract: camera profile, layers, focal path, density, color zoning, occlusion, and screenshot acceptance.
- **`unity-graphics`** — the URP render lock (lighting/material/post) that produces the final on-device look.

## Non-negotiable rules

1. **Never generate a production asset without an approved `art-spec.yaml` and a chosen `style_id`.**
2. **References are broad direction, never clones.** Never request a direct copy of a specific living artist, game, character, or proprietary asset — translate intent into the project's own shape/palette/material/lighting rules.
3. **Keep style ≠ genre ≠ camera distinct.** (Style: painterly cel fantasy. Genre: cozy puzzle. Camera: orthographic 3/4.)
4. **One asset, one primary material language.** Don't mix glossy realism, flat toon, hand-painted gradient, and noisy PBR arbitrarily.
5. **The Unity screenshot is the acceptance test.** A gorgeous source image that fails in the real camera, lighting, or device budget is **rejected** — capture it in `ArtValidationScene` and score it.
6. **Use 3D only where it earns its cost.** On iOS, prefer 2D cards/decals/billboards/baked backgrounds unless parallax, animation, interactivity, silhouette, or depth materially improves the game. Distinguish **runtime 3D** from **production 3D used to pre-render premium non-pixel 2D sprites/animation**. For **pixel art**, do not pre-render/downscale 3D; use PixelLab through `unity-pixel-art` so native pixel clusters, palettes, and silhouettes are intentional.

## The art spec — single source of truth

Before the first production asset, write and approve `Assets/<Game>/Art/_ArtDirection/art-spec.yaml` (canonical path — `docs/PIPELINE_CONVENTIONS.md`; when resuming an existing project also probe the legacy roots `Assets/GameArt/` and `Assets/Art/`). It captures `style_id` (canonical form `<preset>_v<N>`), `camera`, `craft` (`finish` — ALWAYS set, skills branch on it; `pixels_per_unit` — the project-wide PPU SSOT; pixel-only: `base_render_resolution`, `tile_size`, `char_tiles`, `outline_style`, `light_direction`, `dithering_policy`), `shape_language`, `palette` (dominant/neutrals/accent + semantic `roles` + hue-shifted `ramps`), `conditioning` (master palette, style anchors, golden assets), `characters` (THE authoritative per-character canon index), `derived_artifacts`, `materials`, `lighting`, `rendering` (shared shader family + post), `scale` (metric), `mobile_budget` (triangle/texture budget, material caps per tier + target fps), and `acceptance` gates. Then write `Assets/<Game>/Art/_ArtDirection/composition.yaml` with `unity-scene-composition` to lock camera profile, visual layers, focal path, density, color zoning, occlusion, and screenshot tests. **Make intentional choices, then lock them** — don't leave values generic. Full template + an `AssetBrief` template + recommended mobile budgets: `references/art-spec-template.yaml`.

**One style stack.** `art-spec.yaml` is the single style SSOT. `style-guide.md`, `GameTheme.cs`, and UI design tokens are **derived views** — regenerated FROM the spec (paths recorded in `derived_artifacts`), never hand-edited into divergence, and never a competing SSOT. Equality rule, **colors only**: `GameTheme.cs` color hexes MUST equal art-spec palette hexes (`palette.roles` + the palette arrays); typography/spacing/radii are GameTheme-native and have no art-spec source (machine-checked by `unity-asset-pipeline/scripts/validate_asset_manifest.py`). When the spec changes, regenerate the derived views in the same session.

**Legal writers of the spec.** This skill owns and approves `art-spec.yaml`, but `unity-asset-designer` is a **legal writer** of a bounded field set when its step 1/2 funnel finds them missing: `palette.roles`/`palette.ramps`, `shape_language`, `craft.light_direction`, `conditioning.style_anchor_images`, and the `characters` block (canon sheets + frozen identity strings). Those writes go into THE spec — never into a competing document — and this skill reviews them at the next spec approval. Everything else (style_id, camera, craft finish/PPU, materials, lighting, rendering, scale, budgets, acceptance) is written here only.

### Build the master palette (spec approval step, before any PixelLab call)

Emit the `color_image`-compatible swatch `Assets/<Game>/Art/_ArtDirection/palettes/master-palette.png` from the union of `palette.ramps` (dedup, ramp order preserved) and record its path in `conditioning.master_palette_png`. Pixel track: ramps + this file are **required** — any PixelLab call without it is invalid (enforced in `unity-pixel-art`); derived frames/rotations may use the anchor's extracted sub-palette (a subset — never new colors). Non-pixel games: still emit it as the palette-drift QA reference. **The palette block is the hex SSOT:** `validate_asset_manifest.py` computes `palette_valid` from the FULL art-spec palette subtree (roles + arrays + ramps), so every hex any contracted asset may use must live in the palette block — master-palette.png is the conditioning swatch derived from the ramps, never an independent color source. Build it with the art venv (`.artvenv` with `pyyaml pillow`):

```bash
.artvenv/bin/python - "Assets/<Game>/Art/_ArtDirection/art-spec.yaml" <<'EOF'
import os, sys, yaml
from PIL import Image
spec = yaml.safe_load(open(sys.argv[1]))
hexes = list(dict.fromkeys(h for ramp in (spec["palette"].get("ramps") or {}).values() for h in ramp))
assert hexes, "palette.ramps is empty — fill hue-shifted ramps before building the master palette"
img = Image.new("RGB", (len(hexes), 1))
for i, h in enumerate(hexes):
    img.putpixel((i, 0), tuple(int(h.lstrip("#")[j:j+2], 16) for j in (0, 2, 4)))
out = spec["conditioning"]["master_palette_png"]
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
img.resize((len(hexes) * 8, 8), Image.NEAREST).save(out)
print(f"{out}: {len(hexes)} colors")
EOF
```

## Choose a style preset

**The style is the user's choice, not the skill's.** Derive `style_id` from the user's stated aesthetic or a reference they provide — if they gave a reference image/game, **measure its DNA** (line weight, flat-vs-rendered shading, sampled palette hexes, contrast, detail density, focal hierarchy) and pick the preset that fits, recording the measured tokens in the spec. If the user gave **no** direction, present 2–3 candidate presets and **ask** — don't silently default. The preset is a starting scaffold to fill with the user's tokens, never a house style imposed on them.

Pick **exactly one** primary `style_id` (optionally one named secondary influence) from the 12-preset library in `references/style-presets.md`, which lists each preset's reference language, best camera, visual grammar, good-fit genres, and per-style generation do/don'ts. Candidates for a typical casual iOS project (illustrative, not a ranking — flat is as valid as rendered):
- **`cozy_toy_diorama`** — puzzles, idle, social, broadly-appealing (rounded forms, matte materials, soft bevels).
- **`heroic_handpainted_fantasy`** — an approachable "premium game" feel with strong collectible/UI potential.
- **`clean_graphic_casual`** — premium mobile puzzle/word/match (near-flat materials, 2–4 dominant colors, maximum readability).

Avoid `cinematic_pbr_realism` on a solo iOS team unless the game is intentionally sparse — it carries the highest asset, lighting, texture-memory, and animation burden.

## Production pipeline (per asset)

1. **AssetBrief** — write the per-asset spec (type, gameplay role, importance/rarity, scale_m, required views, material slots, animation, collision, texture budget, negative constraints) and resolve its `conditioning:` sub-block from the spec — family golden, master palette, and for characters `canon_sheet` + `identity_string` copied VERBATIM from `characters.<id>` — as resolvable paths, not prose. Template in `references/art-spec-template.yaml`.
2. **Gemini concept** — generate a beauty concept for *reference control*, not as the final runtime asset: isolated object, neutral background, clear material separation, gameplay-readable silhouette, no environment/characters/text. (Use `unity-image-generator`; AAA prompt structure in `unity-aaa-graphics/references/prompt-library.md`.)
3. **Pixel-art branch: PixelLab anchor first** — if `craft.finish == "pixel"`, create one anchor sprite with `unity-pixel-art` at the tile-derived canvas (`craft.tile_size` × `craft.char_tiles` — never ad hoc), conditioned on the family golden (`conditioning.golden_assets`) and the master palette, validate alpha/palette/silhouette/import, then derive variants, directions, and animation frames from that anchor. **Do not use Tripo/3D downscales for pixel art.**
4. **Non-pixel / 3D branch: approved turnaround / multi-view** — produce a 5-panel (front/left/back/right/top) sheet that preserves silhouette, proportions, colors, and material blocks exactly. This is the preferred input for 3D. (Owned by `unity-asset-designer`.) If the asset will be rigged/animated, the approved multi-view must be a clean **T-pose/A-pose** (Tripo's auto-rig requires it; action poses fail — see `unity-3d-generator`). **Do not make variants until the base is approved in Unity** — reference drift multiplies fast.
5. **Tripo 3D** — for runtime 3D or non-pixel pre-render, generate from the approved multi-view: one watertight object, clean silhouette, no floaters, simple readable forms, single UV set, within budget, pivot at base center, Y-up, scaled to metric. (Use `unity-3d-generator`.)
6. **Mesh cleanup & Unity ingest** — AI geometry is never auto-production-ready (see checklist below).
7. **Prefab with shared shader** — make a named prefab using the project's shared stylized material, in the standard directory.
8. **Asset contract + prefab factory** — write `asset-contract.yaml` and run `unity-asset-pipeline`: validate source QA, apply import settings, generate the runtime prefab, and stamp contract provenance.
9. **ArtValidationScene + BeautyCell** — render the prefab in all five standard framings (gameplay camera, neutral studio, bright outdoor, dim indoor, thumbnail/reward-card) and in `BeautyCell_01` using the locked `composition.yaml`.
10. **Quality gate + registry** — score 0–2 per dimension; needs ≥10/12 and no zeros, all machine validators green, and a recorded screenshot. Only then add the prefab to the approved-asset registry. Scene builders may use only registry assets.

### Mesh cleanup & ingest checklist
Mesh integrity (remove floaters, non-manifold, interior faces) · silhouette preserved from the game camera · metric scale + correct pivot · topology reduced where unseen + LODs as needed · materials reduced to the project shader grammar (don't keep random generated PBR maps) · textures compressed/sized to `mobile_budget` · primitive/simplified colliders (never a raw high-poly collision mesh) · named prefab in the standard directory.

## Generate by families, not object-by-object

Approve one **golden asset** per family first, then derive variants by preserving ~80% of the golden asset's language and changing only ~20% (silhouette category, accent color, attachment, damage state, size tier). Record every approved golden in `conditioning.golden_assets` — key `game` is the game golden (the only from-scratch roll; on the pixel track, the only text-only pixflux call); family goldens derive from it, and family members condition on their family golden. Recommended order: camera+lighting test scene → one focal object → three core props → one modular environment kit → one interactable/reward asset → UI icon/card family → VFX family → controlled variants.

## Unity visual lock

The scene — not the model — creates the final feel. Maintain **one** global visual kit: one URP renderer config, one lighting rig per biome/time-of-day, one exposure/tonemapping policy, one shared material/shader family, one camera framing rule per mode, one small VFX library (sparkle/dust/hit/reward/ambience). Expose only project-approved controls on the shared stylized shader (base color, top/bottom gradient, ramp strength, rim strength/color, AO strength, emissive color/intensity) so no asset introduces a bespoke look — a small material vocabulary is what makes a generated world look *authored*. (Render mechanics: `unity-graphics`.)

## Quality gates

Score each 0–2; a production asset needs **≥10/12 and no zeros**: **silhouette** (clear at gameplay scale) · **style compliance** (clearly belongs to this game) · **camera composition** (designed for the actual camera) · **material language** (matches the shared shader grammar) · **mobile budget** (inside caps) · **technical usability** (clean prefab/collider/LOD).

**Scorecard hierarchy (one chain, no dueling gates):** these 0–2 gates are the **per-asset feeder** for `unity-aaa-graphics`' visual scorecard — assets must pass here first, then the composed screen passes there. The aaa-graphics scorecard is the FINAL whole-screen visual authority; `unity-game-director`'s Step 2.6 rubric applies only until this spec exists.

Reject immediately: near-duplicate assets that make a set feel copy-pasted · detail only visible in the source image, not in gameplay · texture noise that flickers at mobile res · mismatched outline weights · random neon emissives as decoration · high-poly collision meshes · a bespoke "special" lighting setup for a single asset.

## Agent workflow

When asked to create/modify a visual asset: (1) read `art-spec.yaml` + existing golden assets; (2) identify the family + closest approved analog; (3) write the AssetBrief with its resolved `conditioning:` block; (4) Gemini concept from style anchors; (5a) if `craft.finish == "pixel"`, PixelLab anchor-first via `unity-pixel-art` (golden-conditioned, master palette on every call), validate, then derive variants/frames; (5b) otherwise approved turnaround/multi-view → Tripo when 3D/non-pixel pre-render is needed; (6) cleanup + import as a prefab with the shared shader/import profile; (7) render in `ArtValidationScene`; (8) score the quality gates; (9) only then place it in gameplay. **Never silently change the project style** — if a request conflicts with `art-spec.yaml`, surface the conflict and propose either a constrained variation or an explicit spec revision; on an approved revision, regenerate the derived views (`derived_artifacts`) and rebuild the master palette.

## Field notes & lessons

- A locked `art-spec.yaml` is the single highest-leverage artifact — it turns "make nice art" into a testable contract, and is what stops the one-hero-asset-amid-flat-everything-else look.
- Generate **families** with a golden asset + 80/20 variants; object-by-object generation drifts and feels copy-pasted.
- AI meshes always need cleanup (floaters, scale, pivot, collider, material reduction) — budget for it; raw Tripo output is an input, not a prefab.
- A small shared shader vocabulary + one lighting rig makes a generated world look authored; bespoke per-asset shaders/lighting are the fastest way to look incoherent.
- The in-engine screenshot, scored against the gate, is the only acceptance test that matters — beauty renders lie about camera, lighting, and device budget.
