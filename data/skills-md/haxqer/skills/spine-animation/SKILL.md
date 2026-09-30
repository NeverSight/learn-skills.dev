---
name: "spine-animation"
description: "Rig and animate 2D characters as Spine skeletal animations from existing art — separated body-part PNGs, a texture atlas, or a single full-character image — and export Spine 4.2 .json + .atlas + .png plus a self-contained HTML5 preview. Use when Codex needs to build a Spine skeleton, auto-position parts onto a bone hierarchy, author idle/walk/run/wave/jump/attack or custom keyframe animations, pack a Spine atlas, deconstruct a full character into parts, render a Spine Web Player preview, or correct an existing skeleton's offsets and draw order. Triggers on: Spine animation, 2D rigging, skeletal/bone/cutout animation, 'animate this character', 'make a walk cycle', or uploads of character body parts to be animated."
---

# Spine Animation

Turn existing 2D character art into a rigged, animated, previewable Spine skeleton.
The bundled `scripts/` do the heavy numerical work (part positioning, JSON
assembly, atlas packing, preview rendering); your job is to drive them, judge the
visual result, and correct it.

This skill produces **Spine-compatible export files** (`.json` + `.atlas` + `.png`)
and an offline HTML preview. Generating the files does not require a Spine
license, and the output loads in the official Spine editor and runtimes (Unity,
Godot, Phaser, web). The preview embeds the Spine Web Player runtime, which is
covered by the Spine Runtimes License — see Step 6.

## Setup

The scripts are plain Python and run from where they live — no copying to a fixed
path. Set a convenience variable and install dependencies once per session:

```bash
SPINE="$(pwd)/scripts"   # adjust to this skill's scripts/ directory
pip install opencv-python Pillow numpy           # core pipeline
pip install google-genai                         # only for the Gemini split backend
```

`opencv-python`, `Pillow`, and `numpy` cover positioning, atlas packing, and
preview. `google-genai` is only needed if you deconstruct a full image with the
Gemini backend (OpenAI-compatible backends use plain HTTP, no SDK).

## What to get from the user

Confirm two things before starting: **which assets** they have, and **which
animations** they want (idle, walk, run, wave, jump, attack, or something custom).

| Asset set | Path through the pipeline |
|-----------|---------------------------|
| Separated part PNGs **+ assembled reference image** | Best case → auto-position (Step 2) |
| Separated part PNGs only | You place parts from vision/part names; skip auto-position |
| Texture atlas + spritesheet PNG | Parse the `.atlas` for regions/sizes, then rig |
| Single full-character image | Deconstruct into parts first (Step 1), then rig |
| Existing Spine `.json` | Parse it; add/modify animations or correct offsets |

## Pipeline

```
[full image] → split → parts → [+reference] → position → build skeleton → atlas → preview → correct
```

Read a reference doc only when you reach the step that needs it:

- `references/spine-json-format.md` — Spine 4.2 JSON + `.atlas` grammar (read before hand-writing or debugging skeleton JSON)
- `references/rigging-and-coordinates.md` — bone hierarchy, the pixel→Spine coordinate math, and how `position_parts.py` works (read for Steps 2–3)
- `references/animation-presets.md` — what each preset does, the 12 principles, custom-animation and adjustment formats (read for Step 4 and for corrections)

### Step 1 — Deconstruct a full image into parts (only if needed)

If the user has just one assembled image, generate a flat "separated parts" atlas
and segment it into individual transparent PNGs:

```bash
python "$SPINE/split_character.py" character.png --output-dir parts/
# pick a backend/model explicitly when needed:
python "$SPINE/split_character.py" character.png --backend openai --model gpt-image-2 --output-dir parts/
```

It is **provider-agnostic** and shares config conventions with the `game-asset-gen`
skill (`--backend auto|openai|openai-responses|gemini`, `--base-url`, `--model`,
and `OPENAI_API_KEY`/`IMAGE_API_KEY` or `GEMINI_API_KEY`/`GOOGLE_API_KEY`; a nearby
`.env` is auto-loaded). If the user is already producing art with `game-asset-gen`,
prefer generating clean separated layers there and skip this step.

After segmentation, **rename the generic `part_NN.png` files to meaningful names**
(`head.png`, `torso.png`, `left-upper-arm.png`, …) — the rig and the animation
presets key off these names. Inspect the atlas first; if parts merged or split
badly, regenerate or tune `--min-area` / `--bg-threshold` with `--segment-only`.

### Step 2 — Auto-position parts (when a reference image exists)

```bash
python "$SPINE/position_parts.py" \
  --reference assembled_character.png \
  --parts parts/ \
  --output layout.json \
  --debug debug/
```

This recovers each part's position, scale, rotation, and the draw order via SIFT +
RANSAC with an occlusion-voting z-order pass. **Open `debug/comparison.png` and
verify it visually** — recomposited parts vs. the reference. Without a reference
image, place parts from their names and your reading of the art instead. The
algorithm and correction workflow are detailed in `references/rigging-and-coordinates.md`.

### Step 3 — Build the Spine skeleton JSON

Author a build config describing the skeleton, bones, slots, attachments, and the
requested animations, then generate valid Spine 4.2 JSON:

```bash
python "$SPINE/build_spine_json.py" --config config.json --output skeleton.json
```

Construct `config.json` from the layout: derive bone positions (relative to parent)
and attachment offsets (relative to bone) using the coordinate math in
`references/rigging-and-coordinates.md`. Bones must be listed parent-before-child;
slot order is the draw order. List preset names under `animations`, and put any
bespoke motion under `custom_animations`.

### Step 4 — Author animations

The presets (`idle`, `walk`, `run`, `wave`, `jump`, `attack`) are generated by
naming them in the config — see `references/animation-presets.md` for what each
does and the principles behind them. For anything custom, add a `custom_animations`
block of valid timeline JSON. Looping animations must return to their start values.

### Step 5 — Pack the texture atlas

```bash
python "$SPINE/make_atlas.py" --parts parts/ --output . --name character_name
```

Outputs `character_name.png` (spritesheet) + `character_name.atlas` (metadata).
Region names come from the PNG filenames, so they must match the attachment names
used in the skeleton.

### Step 6 — Generate a preview

A self-contained HTML file using the official Spine Web Player — opens in any
browser, plays/loops, and lets the user switch animations. Both the assets and
the player runtime are embedded, so the file works with no network:

```bash
python "$SPINE/generate_spine_player.py" \
  --skeleton skeleton.json \
  --atlas character_name.atlas \
  --atlas-image character_name.png \
  --output preview.html \
  --animation idle
```

The runtime is downloaded once (~600 KB) and cached under
`~/.cache/spine-animation/`, so only the first ever run needs network; the
generated file itself never does. This makes the preview about 850 KB.

| Flag | Use |
|------|-----|
| *(default)* | Embed the runtime — preview opens offline |
| `--cdn-runtime` | Link unpkg instead; ~24 KB file, but needs internet every open |
| `--runtime-js` + `--runtime-css` | Embed from a local copy, for fully offline generation |
| `--runtime-version` | Pin a different Spine Web Player build |

If the download fails and nothing is cached, the script warns and falls back to
the CDN rather than failing the run — read the output, because the preview is
then no longer offline-capable.

**Licensing:** the embedded runtime is covered by the Spine Runtimes License,
which requires the copyright notice to travel with any redistributed copy. The
generator inserts that notice automatically. Anyone you hand the HTML to needs
their own Spine Editor license, so use `--cdn-runtime` if you would rather link
the runtime than ship it.

### Step 7 — Inspect and correct

Compare the preview against the reference with your own vision. Common fixes:
misplaced attachments (adjust `x`/`y`), wrong layering (reorder slots), or jittery
motion (check that loop endpoints match). Apply corrections to the config or the
skeleton JSON and regenerate — iterating on the preview is the fastest way to
converge. For interactive hand-tuning, an HTML editor that exports an adjustment
file is described in `references/animation-presets.md`.

## Working principles

- **Verify visually at every stage.** The numbers (SIFT matches, occlusion votes)
  are a strong first guess, not ground truth. The `debug/` images and the preview
  are how you actually confirm the rig is right.
- **Names are contracts.** Part filenames → atlas region names → attachment names,
  and bone names → animation presets. Keep them consistent end to end.
- **Regenerate, don't hand-patch.** Prefer editing the config/layout and re-running
  a script over editing generated JSON by hand; it keeps everything in sync.
- **Don't reinvent art generation.** For creating or iterating the source art and
  separated layers, defer to the `game-asset-gen` skill rather than duplicating it.
