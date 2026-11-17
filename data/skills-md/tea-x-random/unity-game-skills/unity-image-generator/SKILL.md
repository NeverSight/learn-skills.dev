---
name: unity-image-generator
description: "Generate and edit STATIC non-pixel 2D image assets for Unity casual games using Google's Gemini image API, then import them as sprites/textures/UI. Use for exploratory/concept art, style boards, non-pixel static sprites, backgrounds, tile/ground art, tiling textures, UI panels, buttons, icons, logos, title/menu art, particle textures, material/texture references, and high-quality image-to-3D references. For PIXEL ART final assets (low-res sprites, tilesets, directional sheets, animation strips), use unity-pixel-art/PixelLab instead; Gemini may only explore concepts. For non-pixel ANIMATED/motion assets prefer Tripo (unity-3d-generator) to rig + animate, then pre-render only for high-res/painterly 2D — never downscale 3D into pixel art. Covers Unity 2D import: Sprite mode, pixels-per-unit, filtering, sprite atlas, and ASTC for iOS."
---

# Unity Image Generator

Generate **static non-pixel** 2D art with Gemini, then import it into Unity correctly for sprites, UI, or textures. This is the skill for **static 2D concepts, non-pixel textures/grounds, backgrounds, UI/icons, and reference images**. For **pixel art final assets**, route to `unity-pixel-art` (PixelLab) after Gemini exploration. Anything that **moves** in a non-pixel/high-res 2D style can be produced with **Tripo** (`unity-3d-generator`: rig + animate; pre-render to sprite frames), with Gemini providing the high-quality references that condition those Tripo models.

## Gemini vs PixelLab vs Tripo — pick the right tool (library-wide rule)

> **Pixel art → PixelLab final. Non-pixel static/concept → Gemini. Non-pixel 3D/motion → Tripo.**

- **Pixel-art final assets → `unity-pixel-art` (PixelLab):** low-res sprites, tilesets, directional sheets, animation strips, icons, and any final asset that should read as deliberate pixel clusters. Gemini may explore references; it must not be the final pixel-art producer.
- **Gemini (this skill) → exploration and static non-pixel art:** concepts, tiling ground/textures, backgrounds, UI, icons, logos, and high-quality reference images that condition Tripo or PixelLab.
- **Non-pixel motion / high-res 2D pre-render → Tripo** (`unity-3d-generator`): rig + animate, then render to sprite frames for painterly/high-res 2D. This is **not** the pixel-art route.
- **Never create pixel art by Tripo/3D → downscale.** Pixel art needs native canvas control, fixed palettes, crisp silhouettes, and anchor-first variants; use `unity-pixel-art`.
- **Gemini frame-by-frame animation DRIFTS** (each independently generated frame loses identity) and is a fallback only for throwaway concepts or when both the pixel/3D final route is blocked.

## API key & script

Key resolution: `--api-key`, then `GEMINI_API_KEY`. Probe first:
```bash
bash $UNITY_GAME_SKILLS_HOME/unity-game-director/scripts/probe_asset_credentials.sh   # GEMINI_API_KEY=SET|MISSING
```
```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/generate_image.py \
  --prompt "..." --filename Assets/<Game>/Art/Source/coin.png --resolution 2K \
  --art-spec Assets/<Game>/Art/_ArtDirection/art-spec.yaml
```
Flags: `--prompt/-p`, `--filename/-f` (write under `Assets/`), `--input-image/-i` (REPEATABLE — edit/reference inputs), `--input-role` (repeatable; pairs with `-i` by position, e.g. "character identity", "art style" — sent to Gemini as interleaved text parts, there is no native role param), `--resolution/-r {1K,2K,4K}` (default: auto from the largest input image, else 1K; an EXPLICIT value always wins — hi-res reference sheets no longer inflate the output), `--art-spec PATH` / `--no-art-spec`, `--character <id>` (attaches that character's `canon_sheet` from the art-spec and injects its frozen `identity_string` verbatim), `--no-spec-anchors`, `--api-key/-k`.

**Art-spec rule (production calls):** the script resolves `art-spec.yaml` via `--art-spec` → `$UNITY_ART_SPEC` → the canonical/legacy roots (`Assets/*/Art/_ArtDirection/art-spec.yaml`, `Assets/GameArt/...`, `Assets/Art/...`), then injects the spec's verbatim style paragraph + light direction into the prompt and auto-attaches its `conditioning.style_anchor_images`. If no spec resolves, the call **fails** — exploratory/concept work must opt out explicitly with `--no-art-spec`. The same rule applies to `validate_sprite.py` and `critique_image.py`.

## Production assets MUST be conditioned on canon references (discovery step)

A text-only prompt is an independent dice roll — the literal mechanism behind cross-asset drift. Before generating any production 2D asset, DISCOVER the project's canon:

1. Resolve the art-spec (above); read its `conditioning` block (`style_anchor_images`, `golden_assets`) and `characters` block (`canon_sheet`, `identity_string`) — `unity-asset-designer` writes these.
2. Check the approved registry (`Assets/<Game>/Art/Approved/registry.yaml`) for the asset's family golden.
3. Probe `Assets/<Game>/Art/_ArtDirection/sheets/` and `Assets/**/Art/Refs/` for canon/turnaround sheets.

If canon artifacts exist they MUST be attached: `--character <id>` for a recurring character; `-i <family_golden> --input-role "art style"` for family members; spec anchors attach automatically. Generating production art for a project that has canon sheets WITHOUT attaching them is invalid. Concepts/style boards may skip (via `--no-art-spec`).

**Alpha is preserved by default — never flatten foreground sprites onto white.** `generate_image.py` writes real PNG alpha unless you ask otherwise:
- `--alpha-mode preserve` (default) — keep the model's RGBA verbatim. Use for sprites the model already returned with transparency.
- `--alpha-mode chroma-key [--chroma-key-color magenta|cyan|r,g,b] [--chroma-key-threshold N] [--chroma-key-defringe N]` — generate the subject on a solid matte, then key it to real alpha + autocrop + uniform pad. `--chroma-key-defringe` (default 1) erodes the anti-aliased edge ring to remove the matte-color halo; raise it if a fringe survives, set 0 to disable. This is the reliable transparency path (see "Transparency" below).
- `--alpha-mode opaque` — flatten onto white. ONLY for assets that must be opaque: the iOS app icon, full-bleed backgrounds, seamless tiling textures.

> A prior version of this script always composited RGBA onto white, producing white-matted sprites and pale edge halos after import. That is fixed; do not reintroduce it. For any gameplay-facing foreground object, leave alpha-mode at `preserve` or use `chroma-key`, then run the validator gate below.

## Dependencies & quota gotchas (check these FIRST)

The script needs `google-genai` and `pillow`. On modern macOS the system Python is
externally-managed (PEP 668), so install into a venv rather than `pip install --user`:

```bash
python3 -m venv .artvenv && ./.artvenv/bin/pip install google-genai pillow
# run the script with .artvenv/bin/python ...
```

`ModuleNotFoundError: No module named 'google'` means this step was skipped.

**Image gen needs billing on; once it is, the pipeline works.** The script calls
`gemini-3-pro-image-preview` (`scripts/generate_image.py --prompt "..." --filename out.png --resolution 1K|2K|4K`).
One-time setup: `python3 -m venv .artvenv && .artvenv/bin/pip install google-genai pillow`. With
billing **enabled** on the Google AI / Gemini API project, generation succeeds and PNGs import via the
project's ArtImporter (Sprite + iOS ASTC). On a **free-tier** key it (and `gemini-2.5-flash-image`)
returns `429 RESOURCE_EXHAUSTED ... limit: 0` — NOT transient rate-limiting; retrying and
model-swapping both fail. If the probe shows a key but every image 429s with `limit: 0`, report it as a
billing blocker (an allowed asset-sourcing skip) and fall back to procedural/placeholder art — do not
loop on retries.

**Exporting an interactive-only key to a non-interactive tool process.** If `GEMINI_API_KEY` lives in
`~/.zshrc` (sourced only for interactive shells), a tool/agent shell won't have it. macOS has no
`timeout`, and `zsh -lc` does NOT source `~/.zshrc` — you must use `-i`:
```bash
export GEMINI_API_KEY="$(zsh -ic 'printf %s "$GEMINI_API_KEY"' | tail -1)"
```

## What to generate for casual games

- **Sprites / characters / props:** request transparent background, single centered subject, consistent style, clean edges. If the requested finish is **pixel art**, stop here after concept exploration and route final generation to `unity-pixel-art` / PixelLab.
- **Sprite sheets:** for non-pixel assets, request an evenly-spaced grid of frames on transparent background; slice in Unity (Sprite Editor / Grid By Cell). For **pixel-art sheets**, use `unity-pixel-art` anchor-first PixelLab generation instead of Gemini strips or 3D downscales. For **non-pixel animated assets**, Tripo rig + pre-render remains the default when identity/angles matter.
- **Backgrounds / parallax layers:** request seamless or full-bleed layers sized to portrait phone aspect (e.g. 1080×1920 framing).
- **UI:** buttons, panels, frames, progress bars, currency/HUD icons, settings glyphs — flat, high-contrast, readable at small size, transparent background. Keep a consistent icon family.
- **Logos / title art / app icon:** bold silhouette, legible at thumbnail size, no tiny text. The iOS app icon must be square with no transparency.
- **Texture/material references and image-to-3D concepts:** front/side/back T-pose sheets, tiling material swatches — these feed `unity-3d-generator`. **When the concept will be rigged/animated via Tripo, generate a clean full-body T-pose (or A-pose)** — arms away from the torso, legs apart, no props crossing the body — because auto-rigging fails on action poses; generate the action (e.g. a bow-draw) later as animation clips, not in the static concept (see `../unity-3d-generator/SKILL.md` → "Riggable characters need a clean full-body T-pose").

## Style is the user's, never the skill's (READ FIRST)

This skill is a **neutral pipeline**. Every style token — line weight, outline color, palette, shading model, fidelity, finish — comes from the **user's stated aesthetic** or a **user-provided reference**. The skill must **never inject a house style**: no default "cozy", "storybook", "cute", "AAA", "painterly", "thick ink", "high-detail". There is **no such thing as a default look** here, and **flat/minimal is exactly as valid a target as high-detail rendered** — neither is "better".

- **If the user gave an aesthetic, transmit it faithfully.** Build the prompt from THEIR words, not your priors.
- **If the user gave a reference, MEASURE it (don't vibe it)** — see "Match a reference" below.
- **If neither was given, ASK** for one (a sentence of direction or one example image) before generating. A guessed style is the #1 cause of "looks nothing like what I wanted" churn — and the failure is silent, because self-graded art always "looks fine."

> Real failure this codifies: a flat, muted, thin-line puzzle game (Pup Champs) was generated from injected adjectives ("cozy storybook thick-ink, warm palette"). Result: gorgeous but *completely wrong* — heavy black ink, saturated, painterly, dominant background, invisible grid. The skill, not the user, had supplied the style.

## Prompt engineering (match the TARGET fidelity — high or flat)

One-line prompts produce one-line art. A production prompt names, in order: **subject**; **view/framing** (top-down, 3/4, side, centered); **art style** (from the brief/reference — name touchstones only if the user did); **shape language** (chunky, rounded, angular); **palette** with explicit tokens (hex or named, sampled from the reference); **shading model** *as the target dictates* — flat single-tone, cel, soft-gradient, or fully rendered with AO — these are CHOICES, not a ladder; **fidelity/detail density** *as the target dictates* (minimal-and-clean is a legitimate target, not a failure); **output spec** (transparent OR seamless tiling, single subject, no text/UI); and a **negative prompt built from the axes where the target differs from the generator's default** (next paragraph).

**Counter-steer the generator's defaults — but ONLY on the axes where your MEASURED target differs.** Gemini (and most image models) bias toward over-rendering: gradient/glossy shading, busy detail, and sometimes muddy or washed color. Negate an axis **only when your measured target sits opposite the model's drift on THAT axis** — never paste a blanket list, and never negate an axis your reference actually has. Worked examples on the same flat reference:
- Its **fill** is flat but its **outline is bold** and **palette saturated** and pieces have **drop shadows** → negate `NOT gradient shading, NOT glossy, NOT busy` (to hold flatness/cleanness) but DO NOT negate outline, saturation, or shadow — prompt FOR a "bold dark outline", "saturated", "soft drop shadow" instead. (Negating `NOT saturated`/`NOT drop shadow` here — as a naive "it's flat so make everything light" would — actively breaks the match.)
- A high-detail painterly target → steer the other way: `NOT flat single-color fill, NOT MS-Paint, NOT jagged edges`.

The list is built **per measured axis**, every time. (The old fixed `NOT: flat single-color fill` sabotaged a flat target; a naive `NOT saturated, NOT drop shadow` sabotaged the *corrected* attempt at the SAME target. Both came from a blanket list instead of per-axis measurement.)

For template scaffolding and per-genre exemplars see `../unity-aaa-graphics/references/prompt-library.md` — but treat its high-fidelity examples as ONE point on the spectrum, and rewrite its negatives to your target.

## Match a reference (measure INDEPENDENT axes — never slide one "heavy/light" knob)

The biggest, most expensive mistake here: collapsing a reference into a single gestalt vibe ("heavy storybook" / "soft flat-minimal") and dialing that one knob. **Style is multi-dimensional, and the axes are INDEPENDENT.** A reference can be *flat-filled* **and** *bold-outlined* **and** *saturated* **and** *drop-shadowed* all at once — sliding one knob can never reach that mix. "Flat" describes ONLY the fill; it implies nothing about outline weight, color, shadows, or saturation. Two real misses on the SAME game (Pup Champs): pass 1 over-heavy (thick black ink, painterly), pass 2 over-corrected to light on *every* axis (thin outline, muted, no shadow, no grid) — when the truth was flat-fill + **bold** dark outline + **saturated** palette + **drop shadows** + **visible grid**.

When given a reference image (or a named shipped game), do NOT describe it from memory. **Open it, zoom in (crop the key pieces 3×), and SAMPLE PIXELS.** Measure each axis SEPARATELY and write each as its own explicit token. Do not let any axis inherit a value from your overall impression:

1. **Fill / shading:** flat single-tone · cel (1 shadow) · soft-gradient · fully-rendered. (Many cozy mobile games are **flat** — measure, don't assume rendered.)
2. **Outline weight:** none · thin · **bold**. Measure it in px relative to the asset, on a zoomed crop. This is independent of fill.
3. **Outline color:** true-black · dark-tinted (e.g. dark brown) · colored.
4. **Character treatment:** plain · **sticker-halo** (a thick white/cream border around characters — a very common mobile signature; easy to miss, defines the look).
5. **Grounding:** none · **drop shadow** · contact AO. (If the reference has soft shadows under every piece, you MUST add them — do NOT negative-prompt "drop shadow" away.)
6. **Saturation & contrast:** sample 4–7 actual hexes off the pixels. Muted-grey vs **saturated** is a measurement, not a feeling — getting this from memory is how a saturated reference becomes a washed-out copy.
7. **Detail density:** minimal/iconic vs busy.
8. **Perspective/framing + focal hierarchy:** in a board/puzzle game **the grid/board is the hero** and the background is subordinate (generate the bg low-contrast so it recedes). If the reference shows a **grid**, the grid is a first-class element — see the engine note below.

Reuse ONE measured token-set across the whole asset family. **Then validate PER-AXIS against the reference, not gestalt:** chroma-key the pieces, composite onto the bg in the reference's own layout, place it **side-by-side with the actual reference**, and check EACH axis explicitly — "is my outline as bold? is my red as saturated? do my pieces have the shadow? the halo? the grid?" A gestalt "looks close" is exactly how both wrong passes shipped. (This out-of-engine check is also immune to a flaky MCP bridge.)

> **What you mock must be what the ENGINE renders.** A Pup Champs miss: the grid was drawn in the PIL validation mock but never built into the Unity scene, so the "validated" layout didn't exist in-game. If a feature appears in your validation composite (grid lines, shadows, halos), it must be produced by the scene builder / shaders too — otherwise the mock is validating a lie. Either build it in-engine or don't put it in the mock.

## Transparency: Gemini fakes it — chroma-key instead

Asking Gemini for a "transparent background" often yields a painted **checkerboard** (fully opaque) or a colored fill, not real alpha. Reliable path: generate the subject **alone on a solid chroma background** — magenta `RGB(255,0,255)` (use cyan if the subject itself is pink/red/magenta) — then key it out: sample the corner color, drop pixels within a distance threshold, cut alpha, and autocrop. (A reusable keyer pattern lives in the field notes / scratch scripts.)

Recommended command for a foreground prop:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/generate_image.py \
  --prompt "single centered <SUBJECT>, solid magenta background, clean non-overlapping silhouette, no shadow baked into the matte, <STYLE TOKENS>" \
  --filename Assets/<Game>/Art/Source/meadow_tree_a.png \
  --resolution 2K \
  --art-spec Assets/<Game>/Art/_ArtDirection/art-spec.yaml \
  --alpha-mode chroma-key \
  --chroma-key-color magenta
```

### Sprite QA gate — required before Unity import

Run `validate_sprite.py` on every generated 2D foreground object before import. It writes a machine-readable QA report and exits non-zero on failure:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/validate_sprite.py \
  Assets/<Game>/Art/Source/meadow_tree_a.png \
  --require-alpha \
  --min-padding 4 \
  --max-width 2048 --max-height 2048 \
  --art-spec Assets/<Game>/Art/_ArtDirection/art-spec.yaml \
  --json-report Assets/<Game>/Art/Source/QA/meadow_tree_a.sprite-qa.json
```

`--art-spec` fills `--palette` (all spec palette hexes) and `--expected-finish` (from `craft.finish`) — never hand-type the palette on production checks; a per-family CLI `--palette` override is allowed when the family legitimately uses a sub-palette. For hard palette locks (pixel-adjacent or strict flat styles) use the deterministic modes: `--palette-mode exact` (per-pixel palette membership, tolerant of AA edges via `--max-offpalette-ratio`) and `--max-distinct-colors N` (exact color-count gate).

Reject and regenerate/fix the asset if any of these fail:
- **non-transparent corners** when transparency is required (painted checkerboard or matte background);
- **white/green/blue/magenta/cyan edge halo** around the silhouette (flattened or poorly keyed matte);
- **alpha bounding box too loose** or wildly inconsistent padding around the sprite;
- **silhouette occupancy outside the target range** (tiny dot in a giant canvas, or cropped/clipped subject);
- **resolution / texture-memory cap** exceeded for the intended device tier;
- **palette distance** too far from the locked project palette.

The Unity import gate should consume the JSON report as evidence; do not allow a generated foreground sprite into a runtime prefab without a passing alpha QA report.

For tiles/backgrounds, use tile mode instead of alpha mode:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/validate_sprite.py \
  Assets/<Game>/Art/Source/tile_grass.png \
  --tile --square --power-of-two \
  --art-spec Assets/<Game>/Art/_ArtDirection/art-spec.yaml --fail-over-render \
  --json-report Assets/<Game>/Art/Source/QA/tile_grass.sprite-qa.json
```

For a target that is explicitly flat/cel, `--expected-finish flat|cel` warns (or fails with `--fail-over-render`) when the asset drifts into glossy gradients or painterly rendering.

### Vision critique gate — catch what pixel metrics miss

Self-grading by the generating agent is unreliable — broken art silently "looks fine." After alpha QA, run `critique_image.py`, which shows the rendered image back to a vision model and scores it against the STATED intent. This catches the failures `validate_sprite.py` cannot: **wrong subject** (a "rock" that generated as a planet Earth), **over-rendered shading vs a flat brief**, outline-weight/palette drift, **floating objects / baked-in fake shadows**, **busy backgrounds that should recede**, and edge halos.

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/critique_image.py \
  Assets/<Game>/Art/Source/prop_rock.png \
  --subject "a cute mossy grey rock boulder" \
  --role foreground_prop --outline bold \
  --art-spec Assets/<Game>/Art/_ArtDirection/art-spec.yaml \
  --reference Assets/<Game>/Art/Approved/rock_family/rock_golden.png \
  --json-report Assets/<Game>/Art/Source/QA/prop_rock.critique.json
```

`--art-spec` fills palette/finish/light-direction intent from the spec. **On-model gate:** pass `--reference <canon sheet / family golden>` (repeatable) so the judge can SEE the canon — it scores an `on_model_vs_reference` axis (0–3; N/A→3 without a reference). Critiquing a character/family production asset without its reference attached leaves identity drift invisible — always attach it when canon exists.

**Scene mode (whole-screen coherence):** `--scene-mode` scores a composed-scene screenshot on `focal_read` / `layer_contrast` / `grounding` / `cohesion` (+ `on_model_vs_reference` vs a golden screen via `--reference`). Numeric composition budgets (density cost, occlusion %, screen-height %) are measured deterministically from Unity scene data via MCP (`unity-scene-composition`) — never asked of the VLM. Calibration: low scene scores trigger re-roll/review, not a hard block.

It exits non-zero on `fail` and lists `blocking_issues` + `top_fixes`. Feed those fixes back into a **rewritten** prompt (don't reroll the same one). Needs `GEMINI_API_KEY`; if missing, do a documented manual review instead and say so — never claim a critique that did not run. Use `--dry-run` to inspect the request without calling the API.

> Future work (deliberately not built): a CLIP-embedding family-similarity gate was evaluated and demoted — heavy new dependency, semantics-dominated and noisy on small game sprites, uncalibrated threshold. Prefer the deterministic checks (`validate_sprite.py --palette-mode exact`, `--max-distinct-colors`) plus the `--reference` critique axis.

## Generate per visual LAYER — recessive vs focal (most-missed rule)

The #1 reason a scene of individually-fine assets "feels weak" is that **ground/background art was generated with the same bold-ink, saturated, high-detail DNA as the heroes**, so it competes instead of receding and nothing pops. Style tokens are NOT uniform across layers — split them by composition role (the layer comes from `unity-scene-composition`'s `composition.yaml`):

- **Hero / gameplay / foreground props** → full style DNA: bold outline, full saturation, one clear highlight, readable focal detail. Generate at **2K masters** (see below).
- **Midground props** → slightly reduced: thinner outline, slightly lower saturation, less internal detail than heroes.
- **Background / ground tiles** → **deliberately recessive**: thin or NO outline, **lower saturation and contrast**, **sparse** detail, even flat value. The ground is a stage, not a subject. A busy, fully-ink-outlined, saturated grass tile is the classic mistake — it reads as foreground and buries the characters.

Concrete counter-steer for a recessive ground tile (note the opposite negatives to a hero):
```
seamless tiling top-down <STYLE> grass ground, LOW contrast, muted desaturated <PALETTE>,
soft even value, sparse subtle detail, thin or no outlines, recessive background surface
— NOT busy, NOT high-contrast, NOT bold black outlines on every blade, NOT saturated, NOT a focal subject, no text
```
Validate the recede with the critique gate using `--role background_tile --must-recede`.

## Resolution: 2K masters for anything the player looks at

Generate hero/foreground/character/prop masters at **2K** (retina iOS is 2x–3x). 1K is for fast composition checks and truly tiny/recessive elements only. The batch-script habit of generating everything at 1K and never refining produces soft, low-detail in-game assets. Workflow: 1K to lock composition → rewrite prompt if wrong → refine at 2K via `--input-image` with verbatim style tokens → downscale in Unity per device tier, never upscale.

## Tiling ground/terrain textures (square, seamless, validated)

Tiles are not sprites — different rules, and they are easy to get wrong:
- Request a **square** tile and key it to a **power-of-two** size (512/1024) — a 1408×768 "tile" will not tile cleanly.
- **Verify seamlessness**, don't trust the prompt: `validate_sprite.py <tile> --tile --square --power-of-two` checks opposite-edge continuity and dimensions.
- Import with `wrapMode = Repeat` and **mipmaps ON** (opposite of UI sprites).
- **Size the tile to the world grid**, not the canvas — a tile must repeat several times per screen; a single 1K image stretched across the screen reads as one giant blob and exposes the repeat.
- Keep tiles recessive (see layer rule above).

## Grounding: never bake shadows into the cutout

Floating "sticker" objects are a top cause of a cheap look. The contact shadow belongs to the **scene/prefab**, not the asset:
- Generate foreground props/characters on the solid matte with **no ground shadow** in the matte (the `CHROMA` prompt should say "no ground shadow").
- Add grounding in Unity as a separate **soft blob-shadow sprite** or contact AO with a **consistent light direction** across the whole family (owned by `unity-scene-composition` shadow rules + `unity-asset-pipeline` `shadow_profile`).
- A baked-in, asset-specific shadow fights every other asset's light direction once composited — the critique gate penalizes it.

## Verify in the ENGINE, not in a browser or a PIL mock

A `style-guide/index.html` page or a Python/PIL composite is a **concept preview, not proof**. Assets that look acceptable in an HTML grid routinely fall apart in Unity (wrong scale, no real lighting, floating, busy ground, seams). The acceptance test is an in-engine screenshot at device resolution through `unity-mcp-bridge` + the `unity-asset-pipeline` BeautyCell gate. Do not present a browser/PIL composite as evidence the art is game-ready.

## Environment & terrain textures (most-missed assets)

Top-down and side games need **real ground and paths that read as a surface, not a single flat fill** — this removes most of the "amateur" look in tower-defense / top-down maps. Generate **seamlessly tiling** ground / path / tileset textures. The `<STYLE>` and `<PALETTE>` slots below are filled **from the user's brief / measured reference** — the example uses a painterly fill only to show the shape; swap it for whatever the target style is (flat-cel, pixel, painterly, …):

```
seamless tiling <STYLE> grass ground texture, top-down, <PALETTE e.g. #6Fae5a / #4f8a3e>,
subtle variation and clumps, even soft lighting, clean edges, no seams, no subject, no text
— <NEG built for the target style>
```

Import tiling textures with `wrapMode = TextureWrapMode.Repeat` and **mipmaps ON** for material/3D use (the opposite of UI sprites). Apply to a material's albedo and set tiling so the pattern repeats across the surface.


## Candidate batches: generate best-of-N, not first-pass canon

For production assets, do not accept the first plausible image. Generate **3–6 candidates** at 1K from the same shared `art-spec.yaml` + `composition.yaml` + family brief, run `validate_sprite.py` and `critique_image.py` on each, then select with:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/select_best_candidate.py \
  --candidates Assets/<Game>/Art/Source/QA/<asset_id>.candidates.json \
  --json-report Assets/<Game>/Art/Source/QA/<asset_id>.best.json
```

Only the selected candidate gets refined to 2K and promoted into `unity-asset-pipeline`. This “best-of-N + keep-best” pattern is adapted from image-extension workflows and prevents weak first passes from becoming canon. For the full adapted workflow, read `references/image-extender-findings.md` when doing batch art generation, tilesets, sprite sheets, or outpainted backgrounds.

## Sheets / atlases need engine-safe padding

When generating a family sheet, tile sheet, or sprite sheet, repack it with duplicated edge pixels before import to prevent texture bleeding after filtering/mipmaps/atlas packing:

```bash
python3 $UNITY_GAME_SKILLS_HOME/unity-image-generator/scripts/extrude_atlas.py \
  --input Assets/<Game>/Art/Source/meadow_tiles_raw.png \
  --rows 4 --cols 4 --extrude 2 --padding 2 \
  --output Assets/<Game>/Art/Source/meadow_tiles_extruded.png \
  --manifest Assets/<Game>/Art/Source/meadow_tiles_extruded.json
```

Slice using the manifest's `atlas_rect` (excluding the extruded border), then record the final `sprite_atlas` / `atlas_group` in the asset contract.

## Refine loop (regenerate, don't just reroll)

Generate at **1K** first to check composition. If framing/subject is wrong, **rewrite the prompt** (don't just reroll the same one). Once composition is right, refine at **2K** via `--input-image`, reusing **verbatim style tokens** (style name, touchstones, palette) to avoid drift across passes. Use the prompt-library's per-asset rubric to judge each pass. Iterating via `--input-image` also handles recolors, edge cleanup, and variants.

## Import into Unity (via unity-mcp-bridge)

After writing the PNG under `Assets/`, `refresh_unity(scope="assets", wait_for_ready=true)`, then set import settings with `execute_code` (`TextureImporter`) — Unity's default `textureType` may not match intent:

```csharp
var ti = (UnityEditor.TextureImporter)UnityEditor.AssetImporter.GetAtPath("Assets/<Game>/Art/Approved/coin/coin.png");
ti.textureType = UnityEditor.TextureImporterType.Sprite;     // Sprite (2D and UI)
ti.spritePixelsPerUnit = ppuFromArtSpec;                     // READ from art-spec.yaml craft.pixels_per_unit (project PPU SSOT; contract runtime.pixels_per_unit when no spec exists) — never a locally picked number
ti.spriteImportMode = UnityEditor.SpriteImportMode.Single;   // or .Multiple for sheets, then slice
ti.filterMode = UnityEngine.FilterMode.Bilinear;             // For pixel art, route to unity-pixel-art and use Point
ti.mipmapEnabled = false;                                    // off for UI/2D sprites
// iOS compression
var s = new UnityEditor.TextureImporterPlatformSettings {
    name="iPhone", overridden=true,
    format=UnityEditor.TextureImporterFormat.ASTC_6x6, maxTextureSize=2048, compressionQuality=100 };
ti.SetPlatformTextureSettings(s);
ti.SaveAndReimport();
return "imported sprite";
```

Then:
- **Sprites in scene:** `manage_gameobject` with a `SpriteRenderer`, assign the sprite.
- **UI:** UI Toolkit (background-image in USS) via `manage_ui`, or uGUI `Image` via `manage_gameobject`+`manage_components`. See `unity-ui-designer`.
- **Atlas:** group related sprites into a **Sprite Atlas** by family/layer/use-case to cut texture swaps/draw calls (big win on mobile). In production this is not optional metadata: record `atlas_group` / `sprite_atlas` in the `unity-asset-pipeline` asset contract and validate membership before approval.
- **Import defaults:** for real projects, prefer Unity Import Presets + an `AssetPostprocessor` for sprite/tile/UI folders so TextureImporter settings are defaults rather than something every agent must remember. The contract/import validator still remains the gate.

## Quality & mobile rules

- **Real generated art is the default for primary visible surfaces** (characters, props, ground, paths, backgrounds, UI). Procedural placeholder art is a *fallback only* when the key is MISSING or quota-blocked (see the billing-blocker note above) — not a first choice.
- Keep a consistent art-direction across a family (same lighting, outline, palette).
- Pack sprites into atlases; power-of-two max sizes; mipmaps off for crisp 2D, on for 3D textures.
- Use ASTC on iOS; cap max texture size to the smallest that still looks sharp on device.
- **Non-Latin text needs a font that covers the script.** Unity's default LiberationSans SDF has no glyphs for many scripts (CJK, Cyrillic, Arabic, etc.), so those labels render as blank "tofu" boxes. Import a TMP font asset that covers your target script (e.g. an appropriate Noto family font); until it exists, fall back to a supported script. (Also relevant to `unity-ui-designer`.)
- Report prompts, output paths, import settings applied, and where each asset is used.

## Field notes & lessons

- **Art-spec + canon plumbing landed (deep-review R5/R8a/R13/R14).** `generate_image.py` now takes repeated `--input-image`/`--input-role` (role-interleaved text parts), `--art-spec` (verbatim style paragraph + light direction injected; style anchors auto-attached; fail-unless-`--no-art-spec`), `--character <id>` (canon sheet + frozen identity_string), and a fixed resolution sentinel (explicit `-r` always wins; hi-res inputs no longer inflate output). `validate_sprite.py`/`critique_image.py` default palette/finish from the spec; `critique_image.py` gained `--reference` + `on_model_vs_reference` (0–3 scale, unchanged thresholds for `select_best_candidate.py`) and `--scene-mode` (focal read / layer contrast / grounding / cohesion — numeric budgets stay deterministic, measured from scene data). `validate_sprite.py` gained `--palette-mode exact` + `--max-distinct-colors` as the deterministic identity/palette gate (CLIP family gate deliberately demoted to future work).
- **Policy: Pixel art → PixelLab final; static non-pixel/concept → Gemini; non-pixel motion/3D → Tripo.** Gemini is for static art, textures, grounds, backgrounds, UI/icons, and concept/reference images; PixelLab (`unity-pixel-art`) is for final pixel-native sprites/sheets; Tripo is for runtime 3D and high-res/painterly pre-rendered motion. Gemini frame-by-frame animation drifts and is fallback/concept only.
- Gemini image pipeline confirmed working once billing is on (`gemini-3-pro-image-preview` via `generate_image.py`, `.artvenv` with google-genai+pillow); added the interactive-only key export trick for non-interactive tool shells (`zsh -ic`, not `-lc`; no `timeout` on macOS); noted non-Latin text needs a matching TMP font (default LiberationSans has no glyphs for many scripts) — fall back to a supported script until imported.
- **Style-neutrality + per-axis measurement is the law here (learned the hard way, TWICE on one game).** Pass 1: a flat puzzle game generated from *injected* adjectives ("cozy storybook thick-ink, warm") → beautiful but wrong (heavy ink, painterly, dominant bg). Pass 2 *over-corrected* by sliding every axis to "light" (thin outline, muted, no shadow, no grid) → still wrong. Truth (measured): flat fill + **bold** dark-brown outline + white **sticker-halo** + **drop shadows** + **saturated** palette + **visible grid**. The lesson: (1) all style tokens come from the user/reference, never the skill's priors; (2) **style is multi-axis and the axes are INDEPENDENT — measure each separately by zooming + sampling pixels; never collapse to one "heavy/light" knob** ("flat" constrains only the fill); (3) counter-steer the model only on axes where the measured target differs; (4) validate **per-axis** side-by-side with the actual reference; (5) what the mock shows, the engine must render (the grid was mocked but never built). See "Match a reference" above.
