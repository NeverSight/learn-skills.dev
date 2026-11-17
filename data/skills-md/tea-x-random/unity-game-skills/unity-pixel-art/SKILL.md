---
name: unity-pixel-art
description: "Generate production-ready PIXEL-NATIVE 2D game sprites, sprite sheets, tilesets, icons, rotations, and animation frames for Unity using PixelLab for final art, with Gemini only for exploratory concepts/style boards. Use when the requested game art is pixel art, low-res sprite art, tilemaps, top-down/side-view 2D sprites, directional character sheets, animation strips, or any final 2D pixel asset. Enforces golden-anchor-first production at the GAME level (bitforge conditioning on approved goldens), a master-palette color_image lock on every call, art-spec-driven generation, tile-derived canvas sizes, transparent backgrounds, Unity point-filter import, pixel-perfect camera compatibility, alpha/palette/sheet QA plus a deterministic frame-vs-anchor diff gate, and explicitly forbids Tripo/3D-render downscaling as the source of pixel art."
---

# Unity Pixel Art

Create **pixel-native** game assets for Unity. Use Gemini for exploration only; use **PixelLab** for final pixels.

## Routing rule

- **Gemini → exploration:** mood boards, rough silhouettes, palette exploration, UI/style-guide thumbnails, non-final reference sheets.
- **PixelLab → final pixel art:** characters, props, tilesets, icons, directional sheets, animation frames, variants, and recolors.
- **Do not make pixel art by rendering Tripo/3D and downscaling it.** 3D pre-render is acceptable for high-res/painterly 2D, but pixel art must be authored/generatively produced at the target pixel canvas so silhouettes, clusters, outlines, and palette choices are deliberate.

If another skill routes a **pixel-art** asset to `unity-image-generator` or `unity-3d-generator`, override it here: Gemini may provide concept references; PixelLab produces the approved source sprites.

## Required references

Read only the branch you need:

- `references/pixellab-api.md` — PixelLab models, script usage, endpoint/SDK notes.
- `references/pixel-import.md` — Unity import settings, slicing, and pixel-perfect camera snippets.

## Anchor-first production workflow

**Golden-anchor-first at the GAME level (hard rules):**

- **Only the game golden** (`art-spec conditioning.golden_assets.game`) — or an explicitly approved golden reroll — may be generated text-only with `pixflux`. **Every subsequent character/prop SUBJECT MUST be `bitforge` conditioned on the appropriate golden anchor via `--init-image`.**
- **Conditioning channel (verified live 2026-07-01):** bitforge's `style_image`/`--style-strength` produces **structured noise at every strength** on the live API — do not use it. The working channel is **`--init-image` + `--init-image-strength` (1–999)**: the golden is a structural/style init and the description re-subjects it. Calibration: **cross-subject derivation ~75–150** (110 is the script's autofill default; 175+ bleeds the anchor's identity — helmet/outfit/colors leaking into the new subject); **same-asset variants/recolors 250–400**. QA every cross-subject result for **anchor-subject bleed**.
- Family model (aligns with unity-art-direction): the game golden seeds each **family golden** (`conditioning.golden_assets.<family>`); family members condition on their family golden. Pass `--family <name>` and the script auto-fills `--init-image` from the spec (bitforge only; the reference is auto crop/padded — never resampled — to the target canvas, which the API requires to match).
- **Canvas class per subject:** `craft.char_tiles` is the STANDARD character footprint; short subjects (grunts, critters) use their own smaller footprint (e.g. 1×1 tile) — a short subject forced onto a tall canvas comes back as stacked duplicates.
- **Field assets (tiles/textures) do not init on a subject golden** — a character init forces object-ness onto what should be a flat field. Tiles/textures: palette lock + prompt tokens carry coherence, `--outline lineless --shading "flat shading"`, description says *"edge-to-edge full bleed, no border, no outline, no frame, no objects"*. The FIRST approved tile becomes the terrain family golden; later tiles may init on IT (same asset class) at moderate strength. Best-of-N and keep the best `tile.edge_wrap` score — seams vary strongly between rolls.
- **Large-canvas escape hatch:** for approved 128+ boss/set-piece canvases, `pixflux` with the master palette + locked outline/shading enums + the frozen `identity_string`, then vision-QA the result against the game golden.

1. **Resolve the art contract.** Every production call runs under `art-spec.yaml` — the script resolves it (`--art-spec`, `$UNITY_ART_SPEC`, or probed `Assets/*/Art/_ArtDirection/art-spec.yaml` + legacy roots) and auto-fills the master palette, golden anchor, outline enum, tile-derived canvas (`--canvas tile|character`), and PPU provenance. **Production calls without a resolvable spec FAIL**; spec-less exploration requires an explicit `--no-art-spec`.
2. **Explore cheaply with Gemini if needed.** Generate concept boards or silhouette sheets only. Do not approve Gemini pixels as final pixel-art assets.
3. **Generate the anchor sprite in PixelLab.** Game golden → `pixflux`; everything else → `bitforge` on its golden (rules above). Use a tile-derived native canvas, transparent/no-background output, and the master palette as `color_image`. This anchor becomes the only source of truth for the asset.
4. **QA the anchor before variants.** Run alpha/padding/palette/silhouette checks with `unity-image-generator/scripts/validate_sprite.py`. **For goldens and canon sprites a VISION check is MANDATORY, not optional** — the deterministic gates cannot see subject errors: a duplicated/stacked subject (a tall canvas often comes back as a big+small character or stacked duplicates) passes every alpha/palette check. Verify single subject, full body visible, correct subject, no anchor-subject bleed — via `critique_image.py` or direct image inspection, BEFORE approving. Prompt-side prevention: phrase goldens as "exactly one <subject>, full body, head to feet visible, single character only, no duplicates" and pass `--coverage-percentage 80` on character canvases. **Recurring characters — register the pixel canon now:** the pixel-track canon sheet is the approved anchor plus its `rotate`-derived directional views composited into one PNG at `Assets/<Game>/Art/_ArtDirection/sheets/<char_id>_canon.png` (a 3-line PIL paste of the anchor + rotations side by side; for a single-view game the approved anchor alone, copied to the canon path, is the blessed canon). Never use a Gemini turnaround as pixel canon. Register `characters.<id>.{canon_sheet,anchor_sprite,identity_string}` in the art-spec before generating any derived asset.
5. **Derive frames/rotations/variants from the anchor.** Keep one base sprite driving directions, walk/idle/attack strips, damage states, and palette variants:
   - **Directions →** `rotate` (set `--from-direction`/`--to-direction`).
   - **Animation →** the **skeleton workflow** (`estimate-skeleton` → author per-frame poses → `animate-skeleton`). This is structurally consistent across frames. `animate-text` is the drift-prone fallback; never author each frame independently.
   - **Recolors / damage states / edits →** BitForge conditioned on the anchor (`--init-image` with `--init-image-strength 250–400`), or `inpaint` for local fixes.
   - **Derived frames/rotations use the anchor's extracted sub-palette** (a subset of the master — never the full game palette, which permits cross-asset color borrowing; never new colors). Emit the swatch from the approved anchor (`compare_frames_to_anchor.py --anchor <anchor.png> --emit-subpalette <id>_subpalette.png`) and pass it via `--color-image`; omitting `--color-image` falls back to the full master palette, which this rule forbids for derived frames.
6. **Gate frames with `scripts/compare_frames_to_anchor.py`** (palette-membership + baseline/bbox + loose silhouette-IoU vs the anchor) before slicing. Manual eyeballing does not replace it.
7. **Repack sheets with padding/extrusion.** Use `extrude_atlas.py` before Unity slicing so point filtering and atlas packing do not bleed neighboring cells.
8. **Import with pixel settings.** Point filter, no compression, no mipmaps, PPU from `art-spec craft.pixels_per_unit`, multiple-sprite slicing for sheets, SpriteAtlas family grouping, and Pixel Perfect Camera settings.
9. **Promote only approved assets.** The final artifact must include the sprite PNG/sheet, QA reports, manifest, Unity import contract, prefab, and BeautyCell screenshot before it enters the approved registry.

## Canvas and style rules

- Derive canvases from the spec's tiles (`craft.tile_size` × `craft.char_tiles`), never ad hoc; sanity-band by readability: icons `16–32`, pickups/props `32–64`, characters `32–128`, bosses/large set pieces `128+` only when the camera supports it.
- Generate at the **final pixel canvas**, not a high-res illustration to shrink later.
- State the exact view using a real `CameraView` enum: `side`, `low top-down`, or `high top-down` (there is no plain `top-down`/`3/4`/`isometric` view — isometric is the `--isometric` flag). Pick `direction` from the 8-way compass set (`south`, `south-east`, `east`, …). State pivot/baseline.
- **Any PixelLab call without the palette lock is invalid.** Every call carries a `color_image`: the game's `master-palette.png` for anchors/goldens, the anchor's extracted **sub-palette** for derived frames/rotations. `--palette` hex lists are for exploration only.
- Keep animation frame counts small and game-readable: idle `4–6`, walk/run `6–8`, attack `6–10`, hit `2–4`, death `6–10`.
- Prefer one row per clip (`idle`, `walk`, `attack`) or a documented grid (`rows=clips`, `cols=frames`) with a sidecar manifest.

## PixelLab helper script

Use the bundled script for final generation. It resolves keys as `--api-key` → `PIXEL_LABS_API_KEY`, and the art-spec as `--art-spec` → `$UNITY_ART_SPEC` → probed project paths. With a resolved spec it auto-attaches the **master palette** (`conditioning.master_palette_png` → `color_image`), the **golden anchor** (`conditioning.golden_assets.<--family|game>` → `--init-image`, bitforge only, default strength 110), the outline enum, and the per-game default view/shading enums (`craft.view` / `craft.shading` → `--view`/`--shading`; explicit CLI flags win); production calls without a spec (or without a palette lock) fail. Exploration only: add `--no-art-spec`.

Game golden — the ONLY text-only roll (everything after conditions on a golden):

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py pixflux \
  --description "pixel art knight hero, side view, single color black outline, transparent background" \
  --canvas character --no-background --view side --direction east \
  --output "Assets/<Game>/Art/Source/SourceImages/hero_knight_golden.png" \
  --manifest "Assets/<Game>/Art/Source/SourceImages/hero_knight_golden.pixellab.json"
```

Every subsequent subject — `bitforge` init-conditioned on its golden. **`--init-image-strength` is a 1–999 scale.** NEW subjects from a golden ~75–150 (autofill default 110; higher bleeds the anchor's identity into the new subject); same-asset variants/recolors 250–400. (`--style-image`/`--style-strength` are traps on the live API — noise at every strength.)

```bash
# new family member: --family picks conditioning.golden_assets.<family> as --init-image
# (short subject -> its own footprint, not the standard char canvas)
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py bitforge \
  --description "pixel art goblin grunt, single small goblin, same game style, side view, transparent background" \
  --width 32 --height 32 --family enemies \
  --no-background --view side --direction east \
  --output "Assets/<Game>/Art/Source/SourceImages/goblin_grunt.png" \
  --manifest "Assets/<Game>/Art/Source/SourceImages/goblin_grunt.pixellab.json"

# same-asset variant: condition on the asset's own anchor, sub-palette lock
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py bitforge \
  --description "same coin, cracked damaged variant, same palette, same silhouette center" \
  --width 32 --height 32 \
  --init-image "Assets/<Game>/Art/Approved/coin/coin.png" --init-image-strength 320 \
  --color-image "Assets/<Game>/Art/Approved/coin/coin_subpalette.png" \
  --no-background \
  --output "Assets/<Game>/Art/Source/SourceImages/coin_damaged.png"

# field asset (tile/texture): NO subject init — palette + tokens + lineless/flat
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py pixflux \
  --description "pixel art grass ground texture, flat field viewed from directly above, edge-to-edge full bleed, no border, no outline, no objects, seamless tileable" \
  --canvas tile --view "high top-down" --outline lineless --shading "flat shading" \
  --output "Assets/<Game>/Art/Source/SourceImages/grass_tile.png"
```

### Animation: skeleton-first (structural consistency)

Image models drift frame-to-frame. For a character that must keep its identity across a walk/idle/attack cycle, drive frames with a **posed skeleton**, not text. Reuse ONE keypoint template per humanoid archetype (`art-spec characters.<id>.skeleton_template`, e.g. `_ArtDirection/sheets/biped_48.skeleton.json`) so the whole cast shares proportions:

```bash
# 1. rest-pose skeleton from the approved anchor -> editable JSON template
#    (save/reuse it as the game's biped template for every humanoid)
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py estimate-skeleton \
  --image "Assets/<Game>/Art/Approved/hero_knight/hero_knight.png" \
  --output "Assets/<Game>/Art/_ArtDirection/sheets/biped_48.skeleton.json"

# 2. author per-frame poses in knight_walk_frames.json (a list of frames —
#    each either a bare keypoint list [{"x","y","label","z_index"},...] or
#    {"keypoints":[...]}; the script normalizes both), then:
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py animate-skeleton \
  --skeleton-json knight_walk_frames.json \
  --view side --direction east \
  --reference-image "Assets/<Game>/Art/Approved/hero_knight/hero_knight.png" \
  --color-image "Assets/<Game>/Art/Approved/hero_knight/hero_knight_subpalette.png" \
  --output "Assets/<Game>/Art/Source/SourceImages/knight_walk.png"   # -> _00.png… + _strip.png
```

**Attack/action animation doctrine (field-verified 2026-07-01):**

- **Animate the FRONT limb — and mirror correctly.** Keypoint LEFT/RIGHT labels are the CHARACTER's anatomical sides (COCO convention), not the viewer's: facing east, the character's LEFT limbs are the camera-front/travel side (rest-pose x tells you — the front limb has the larger x when facing east). A slash authored on the back arm plays "correctly" and reads as NOTHING. Check rest-pose x before authoring. **Deriving a mirrored facing = negate x AND swap every LEFT/RIGHT label pair** (shoulder/elbow/arm, hip/knee/leg, eye/ear) — mirroring x alone silently attacks with the back arm. Pre-flight: the `--view`/`--direction` passed to animate-skeleton MUST equal the reference anchor's stored facing (asset-contract) — a mismatched skeleton degrades pose adherence without erroring.
- **Use ABSOLUTE extreme poses, not small offsets — phase grammar, not evenly-spaced swing positions.** ±0.05 normalized offsets read as nothing at 32–64px. Frames are DISTINCT phases (Dead Cells: keys first, "never in-between"): 4-frame attack = windup (wrist pulled back OPPOSITE the strike, torso counter-twisted) → strike-smear → follow-through (forward-down) → recover; 3-frame player attack DROPS the windup (strike/follow/recover — player anticipation reads as input lag; enemies instead HOLD the windup ≥0.3s in clip timing). Magnitudes at a 64px canvas: striking wrist travels ≥0.25 normalized (≥16px, ~90–180° about the shoulder) between windup and strike, ending PAST anatomical reach (~0.95–1.0 forward extent, elbow ~0.85 — elongation/exaggeration is doctrine); NOSE/NECK lean +0.04–0.07; both HIPs shift 0.02–0.03; front knee lunges. The whole SILHOUETTE must change — at this size the arm alone is 2px wide. On the strike frame prompt for the smear ("angular motion smear on the weapon arc") and accept detail loss — legibility of movement beats detail parity. Offset all keypoints ~20–25% toward the trailing canvas edge so the strike side has empty space for the model to draw effect pixels (PixelLab's own attack guidance); compensate at the import pivot. Set fixed-head OFF for attack strips (the head must lean); ON for idle/walk. Wrist travel IS the weapon-arc control — the 18-keypoint schema has no weapon joint.
- **Poses vs timing are separate artifacts.** PixelLab owns POSES; Unity clip keyframe times own TIMING (attack clips are non-uniform — strike 50–70ms, holds carry the weight; table in unity-animation). Never regenerate a strip because it "feels slow/fast" — that is a free keyframe edit. Near-identical frames from a correct-looking pose set is a KNOWN pose-conditioned-diffusion failure mode (regression to the reference), which is why the motion gate is permanent; pre-flight the keypoints (wrist delta ≥0.25 normalized) before spending credits, and repair failing frames with `--init-images` freeze, not rerolls.
- **The model animates the BODY, not the weapon.** Pose-conditioned generation will not draw a blade arc — a hip-level sword stays a hip-level detail. **Weapon attacks REQUIRE a separate slash/impact VFX overlay sprite**: generate it standalone (`pixflux`, `--outline lineless --shading "flat shading" --no-background`, "curved crescent slash trail, motion effect only, no character"), contract it as role `vfx` (free-sized, exempt from tile-multiple), and code-animate the overlay (0.15s scale 0.7→1.15 + rotate + fade) in front of the character, plus ~0.05s hitstop on contact. The overlay carries the read; the body strip supports it (gate the strip at `--min-inter-frame-motion 0.25` when paired with an overlay, 0.35 solo).
- PixelLab canvases carry transparent padding rows below the feet (3-11px measured) — the FEET, not the canvas bottom, are the baseline; import pivots must be alpha-derived (see unity-asset-pipeline).

Canvas defaults to the reference image; identity/pose adherence is governed by the live API's single `guidance_scale` (server default 4.0), tunable via `--guidance-scale`. **Live-endpoint constraints (all auto-handled by the script, 2026-07-01):** the whole command runs over **raw HTTP** — SDK 1.0.5 is incompatible (it nulls absent `inpainting_images`/`mask_images`, which the API rejects, and can't send `guidance_scale`); the canvas must be **square 16/32/64/128/256** (non-square characters are padded baseline-preserving and frames cropped back); each call takes an **exact pose count set by the canvas** (e.g. 3 at 64×64 — longer clips are batched automatically); `z_index` must be an integer (estimate-skeleton emits fractional ones; the script rounds). Use `rotate` to spin the base/keyframes into other directions. **Fix single bad frames instead of re-rolling the strip:** `inpaint` (white mask) on that frame, or re-run `animate-skeleton` with `--init-images` freezing the approved frames. `animate-text` exists as a fallback when no skeleton can be authored, but it drifts more. Gate every strip with `compare_frames_to_anchor.py` before slicing.

Before a paid batch, check credits and use `--dry-run` to verify dimensions, prompt, and conditioning inputs:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py balance
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/generate_pixel_art.py --dry-run bitforge --description "..." --canvas character --family enemies --output /tmp/preview.png
```

(`--dry-run` obeys the same art-spec gate, so it previews the exact production payload; spec-less exploration adds `--no-art-spec` there too.)

## QA gates

Run after every final PixelLab output:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/validate_sprite.py \
  "Assets/<Game>/Art/Source/SourceImages/coin_anchor.png" \
  --art-spec "Assets/<Game>/Art/_ArtDirection/art-spec.yaml" \
  --require-alpha --min-padding 1 --max-width 128 --max-height 128 \
  --json-report "Assets/<Game>/Art/Source/QA/coin_anchor.sprite-qa.json"
```

(Tile-aligned characters whose baseline sits on the bottom canvas edge use `--min-padding 0` — per-sprite edge padding is an atlas concern and is added by `extrude_atlas.py` at repack, not at generation. With an art-spec, exact palette membership is checked against the **master-palette.png swatch pixels** — the same artifact generation conditioned on — not the spec hex lists.)

**MANDATORY for every animation strip / rotation set** — deterministic frame-vs-anchor identity diff (palette membership, baseline/bbox drift, loose silhouette-IoU identity-swap floor). **Add `--action` for attack/hit/death clips** — it additionally requires visible inter-frame MOTION (≥0.35 pixel-change between at least one frame pair; calibrated live: a slash that read as broken in-game measured 0.27, a real run cycle 0.78). Identity gates alone pass near-identical standing poses that play "correctly" in the Animator yet read as nothing. Two additional required checks for attack strips: the LARGEST inter-frame delta must land on the windup→strike pair (a strip peaking on the recover frame is mis-authored — pass `--strike-pair`), and the silhouette (alpha-mask) must change between frames — raw pixel change passes recolor/AA shimmer that reads as nothing. Exit 1 = do not slice; repair the failing frame (`inpaint` / `--init-images` freeze) instead of re-rolling the strip:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-pixel-art/scripts/compare_frames_to_anchor.py \
  --anchor "Assets/<Game>/Art/Approved/hero_knight/hero_knight.png" \
  --strip "Assets/<Game>/Art/Source/SourceImages/knight_walk_strip.png" --cols 8 \
  --json-report "Assets/<Game>/Art/Source/QA/knight_walk.frame-diff.json"
```

For tilesets:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/validate_sprite.py \
  "Assets/<Game>/Art/Source/SourceImages/grass_tile.png" \
  --art-spec "Assets/<Game>/Art/_ArtDirection/art-spec.yaml" \
  --tile --square --power-of-two --expected-finish flat \
  --json-report "Assets/<Game>/Art/Source/QA/grass_tile.sprite-qa.json"
```

Gate the wrap axes by the tile's ROLE: `--wrap-axes horizontal` for a side-scroller ground band (repeats only left-right; the top edge is the visible surface), `--wrap-axes both` (default) for open tilemap ground. Seams vary strongly between rolls — best-of-N and keep the best wrap score.

Reject pixel assets for:

- **any PixelLab call made without the palette lock** (`color_image` — master palette, or anchor sub-palette for derived frames);
- a production SUBJECT generated without init-conditioning on its golden anchor (pixflux is legal only for the game golden, family-golden seeds for asset classes that can't derive from a subject anchor — e.g. the first terrain tile — and the large-canvas escape hatch);
- any bitforge call using `--style-image`/`--style-strength` as the conditioning channel (live API returns noise — use `--init-image`);
- generated at the wrong native canvas (canvas not derived from `craft.tile_size`/`char_tiles`);
- anti-aliased/high-res painted edges that are not pixel-native;
- palette drift outside the approved palette;
- inconsistent baseline/pivot across frames (`compare_frames_to_anchor.py` exit 1);
- loose alpha padding or non-transparent corners;
- animation frames that change identity, outfit, proportions, or weapon placement — including cross-subject **anchor-subject bleed**;
- imported with bilinear filtering, compression, mipmaps, or wrong PPU.

## Unity import summary

Use `references/pixel-import.md` for snippets. Minimum settings:

- `TextureImporterType.Sprite`
- `FilterMode.Point`
- `TextureImporterCompression.Uncompressed`
- `mipmapEnabled = false`
- `SpriteImportMode.Multiple` for sheets
- `spritePixelsPerUnit` = `art-spec craft.pixels_per_unit` (project PPU SSOT; contract `runtime.pixels_per_unit` is the no-spec fallback)
- Pixel Perfect Camera (`com.unity.2d.pixel-perfect`) when the game camera renders pixel art.

## Handoff to other skills

- `unity-image-generator`: concept boards, non-pixel static art, UI mockups, vision critique, sprite validators.
- `unity-animation`: Animator setup, frame timing, events, slicing; source frames come from this skill for pixel art.
- `unity-asset-pipeline`: asset contract, prefab factory, registry, BeautyCell gate.
- `unity-scene-composition`: screen-space scale, readability, layer density, camera contract.
