---
name: creating-sprites
description: Guides pixel-art sprite creation via OpenAI gpt-image-1.5 image generation with automated processing. Covers sizing, prompting, transparency verification, downscaling, and cropping. Use when creating game sprites or pixel art assets
---

# Creating Sprites

Generate pixel-art game sprites via OpenAI's gpt-image-1.5 model with native transparent background support, then process them into game-ready assets with correct dimensions and proper anchoring.

## Reference Files

| File | Read When |
|------|-----------|
| `references/sprite-sizes.md` | Choosing target size, generation size, crop mode, or fake pixel math for a sprite type |
| `references/prompt-guide.md` | Constructing or refining a generation prompt, choosing style keywords, or writing per-type prompts |
| `references/troubleshooting.md` | A generation fails, transparency check fails, style doesn't match, or API returns errors |

## Prerequisites

- **`OPENAI_API_KEY`** — an OpenAI API key
  - The generate script auto-loads from: `--api-key` flag → `OPENAI_API_KEY` env var → `.env` file in current directory
- **Python dependencies**: `openai` and `Pillow` (installed via `requirements.txt` in the skill's `scripts/` directory)

## Script Paths

All `scripts/` paths in this skill are **relative to the skill directory**, not the project directory. Resolve them to absolute paths before running. For example, if the skill is installed at `~/.claude/skills/creating-sprites/`, then `scripts/generate_sprite.py` means `~/.claude/skills/creating-sprites/scripts/generate_sprite.py`.

## Workflow Checklist

```
- [ ] Phase 0: Verify prerequisites
- [ ] Phase 1: Determine sprite requirements
- [ ] Phase 2: Prepare reference images
- [ ] Phase 3: Construct prompt
- [ ] Phase 4: Generate candidates
- [ ] Phase 5: Validate candidates
- [ ] Phase 6: Process chosen sprite
- [ ] Phase 7: Save and update plan
```

## Phase 0: Verify Prerequisites

Before doing any work, verify the environment is ready. Handle what you can; only ask the user for things you can't resolve yourself.

1. **Check API key** — check all three sources:
   ```bash
   python -c "
   import os
   from pathlib import Path
   key = os.environ.get('OPENAI_API_KEY', '')
   if not key:
       env = Path('.env')
       if env.exists():
           for line in env.read_text().splitlines():
               if line.strip().startswith('OPENAI_API_KEY'):
                   key = line.partition('=')[2].strip().strip('\"').strip(\"'\")
   print('OK' if key else 'MISSING')
   "
   ```
   - If `MISSING`: ask the user to add `OPENAI_API_KEY=their-key` to a `.env` file in the project root, or export it as an environment variable
   - Do NOT proceed past this phase without a valid key

2. **Install Python dependencies** (do this yourself, don't ask the user):
   `pip install -r <skill-dir>/scripts/requirements.txt`

Only the API key requires user action. Everything else you should handle yourself.

## Phase 1: Determine Sprite Requirements

Identify what to create and look up its parameters.

1. Determine the entity type: item, enemy, decoration, structure, UI icon, player, pet, animal, boss, terrain tile
2. Read `references/sprite-sizes.md` for common size examples, generation size, and crop mode — use these as a starting point and adjust based on the specific entity
3. Record these values:
   - `target_width` and `target_height` (e.g., 32x32)
   - `generation_size` (1024x1024 default)
   - `crop_mode` (bottom-anchor, center, or none)
4. Identify the destination path in the project for the final sprite
5. Identify 1-3 existing sprites that could serve as style references

## Phase 2: Prepare Reference Images

Existing sprites are tiny and must be upscaled for the AI model to interpret them. Reference images are passed directly to the API via `--reference` flags for style matching.

For each reference sprite, run:
```bash
python scripts/upscale_reference.py --input path/to/sprite.png --output temp/sprite_upscaled.png
```

The script auto-calculates the best integer multiplier to reach 500-1024px using nearest-neighbor interpolation (preserves pixel crispness).

If no reference sprites exist (first sprite in the project), skip this phase.
The prompt alone will define the style.

## Phase 3: Construct Prompt

Read `references/prompt-guide.md` for the base template, style keywords, and per-type examples.

Every prompt must specify:
- Pixel-art style with era/palette keywords (derived from reference analysis in Phase 2)
- Target fake-pixel dimensions ("a 32x32 pixel art sprite")
- **Transparent background** (gpt-image-1.5 supports this natively)
- ONE sprite only, centered in frame
- No border, no shadow, no text, no grid
- Subject description
- Anchoring: "touching the bottom of the image" for entities, "centered" for items
- "Match the style of the provided reference images" when references are included

## Phase 4: Generate and Validate (Max 3 Attempts)

You get **at most 3 generation attempts** per sprite. Each attempt produces 4 candidates. **Never delete candidates from previous attempts** — you will pick the best sprite across ALL attempts at the end.

The `--name` flag sets the base filename. Use a short, descriptive slug for the sprite (e.g. `slime`, `health_potion`, `oak_tree`). Use a **versioned suffix** to prevent overwrites across attempts: `slime_v1`, `slime_v2`, `slime_v3`.

### Attempt 1 — Initial Generation

Generate with the prompt from Phase 3. The script always requests a transparent background natively, whether or not reference images are provided.

```bash
python scripts/generate_sprite.py \
  --prompt "A 32x32 pixel art ..." \
  --output-dir ./sprites-wip \
  --reference temp/ref1_upscaled.png \
  --reference temp/ref2_upscaled.png \
  --count 4 \
  --name slime_v1
```

Outputs: `slime_v1_001.png` through `slime_v1_004.png`.

**Validate** (run on every attempt):

1. **Programmatic check** — run on each candidate:
   ```bash
   python scripts/check_transparency.py --input ./sprites-wip/slime_v1_001.png
   ```
   Output format:
   ```
   FILE: slime_v1_001.png
   FORMAT: PNG
   ALPHA_CHANNEL: yes
   TRANSPARENT_PIXELS: 45.2%
   CHECKERBOARD_DETECTED: no
   RESULT: PASS
   ```
   - **PASS**: At least 10% transparent pixels, no checkerboard pattern
   - **FAIL**: No alpha channel, 0% transparency, checkerboard detected, or not PNG

2. **Visual inspection** — use the Read tool to view each passing candidate.
   Check: single sprite? Correct orientation? Right proportions? Matches game style?

If any candidate passes both checks → skip to **Pick the Best** below.

### Attempts 2 and 3 — Diagnose Then Fix

Before each retry, **diagnose the failure type** from previous attempts. The fix depends on the problem:

#### Background problems (use prompt refinement, then chromakey)

Symptoms: colored background instead of transparency, checkerboard pattern, unwanted scenery (grass, forest, inventory frame, etc.)

- **Attempt 2**: Strengthen transparency language in prompt: "isolated sprite on transparent background, no checkerboard pattern, actual PNG transparency, no scenery, no environment"
- **Attempt 3 (if background problems persist)**: Switch to **chromakey fallback**:
  - Pick a safe background color not present in the subject (see `references/troubleshooting.md`)
  - Add to prompt: "solid flat [COLOR] background, no gradients, no patterns, no shadows"
  - After generation, process with: `process_sprite.py remove-bg --chroma-color HEXCODE`

#### Subject problems (use prompt refinement only — NOT chromakey)

Symptoms: wrong proportions, wrong style, multiple sprites, missing details, wrong pose/orientation — but transparency is fine.

- **Attempts 2 and 3**: Refine the prompt and/or adjust style keywords. See `references/troubleshooting.md`. Chromakey does not help here — the problem is the subject, not the background. Keep iterating on prompt wording and style descriptions.

#### Mixed problems (both background and subject issues)

- Prioritize fixing the subject first (prompt refinement), since chromakey can always fix the background later
- If subject looks good by Attempt 2 but background is still wrong, use chromakey for Attempt 3

```bash
python scripts/generate_sprite.py \
  --prompt "Refined prompt ..." \
  --output-dir ./sprites-wip \
  --count 4 \
  --name slime_v2   # then slime_v3 for attempt 3
```

Validate the same way after each attempt.

### Pick the Best (across ALL attempts)

After completing your attempts, review **all** candidates from every attempt — not just the latest batch. A sprite from Attempt 1 may be better than one from Attempt 3.

Use the Read tool to compare the top candidates side-by-side and select the single best one for processing.

### If All 3 Attempts Fail

Create a manual creation task in the implementation plan and move on. Don't block progress on one asset. Save the best attempt as a reference for future manual work.

## Phase 6: Process Chosen Sprite

Run the full pipeline on the selected candidate:

```bash
python scripts/process_sprite.py pipeline \
  --input ./sprites-wip/slime_002.png \
  --output ./sprites/slime.png \
  --target-width 32 --target-height 32 \
  --crop-mode bottom-anchor
```

If chromakey was used, add `--chroma-color HEXCODE --tolerance 30`.

Pipeline steps (can also run individually):
1. **Remove background** (if chromakey): `remove-bg --chroma-color HEXCODE`
2. **Downscale**: nearest-neighbor from generation size to target dimensions
3. **Crop** per crop mode: bottom-anchor trims sides/top; center and none leave canvas as-is

**Post-chromakey re-check**: If chromakey was used, run `check_transparency.py` on the output.
If it fails or the visual check shows artifacts, create a manual task in the implementation plan and skip this sprite.

Read the final sprite to verify: correct dimensions, clean transparency, pixel-art preserved, appropriate crop.

## Phase 7: Save and Update Plan

1. Move the final sprite to the correct project folder
2. Clean up temporary upscaled references (temp/)
3. **Keep all candidates in `sprites-wip/`** — do NOT delete any, from ANY attempt. The versioned filenames (`slime_v1_001.png`, `slime_v2_003.png`, etc.) make it easy to revisit rejected candidates later
4. Update the implementation plan with integration tasks (add to asset registry, create entity config, etc.)

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Generating without reference images | Always use 1-3 style references when available |
| Passing tiny 32px sprites as references | Upscale references to 500-1024px with nearest neighbor first |
| Bilinear/bicubic downscaling | Always nearest-neighbor to preserve pixel crispness |
| Multiple sprites in one image | ONE sprite per image, 4 separate API calls |
| Only visual transparency check | Always run check_transparency.py script first |
| Green chromakey for plant sprites | Pick a chromakey color not present in the subject |
| Skipping visual validation | Always Read the image to inspect after programmatic checks |
| Cropping items | Items stay centered in canvas; only crop entities |
| Giving up after 1 failed generation | Up to 3 attempts; diagnose failure type and apply the right fix each time |
| Using chromakey for subject problems | Chromakey fixes backgrounds only; for wrong style/proportions, refine the prompt |
| Deleting candidates from earlier attempts | Keep ALL candidates; pick the best across all attempts at the end |
| Reusing the same `--name` across attempts | Use versioned names (`slime_v1`, `slime_v2`, `slime_v3`) to prevent overwrites |
| Using generic style keywords | Derive style keywords from studying the project's existing sprites |

## Dependency Note

This skill requires `openai` and `Pillow`. Phase 0 handles installation automatically.
This is an approved exception to the standard-library-only rule for scripts.
