---
name: video-style-extractor
description: Extract complete editing styles from video files for programmatic recreation. Analyzes visual design (colors, fonts, layout, mascot characters), editing patterns (cuts, transitions, timing), motion/animation, audio production, and storytelling structure using Gemini video analysis + scene-aware frame extraction + pixel-art mascot profiling + marketing psychology. Use when asked to "extract a style," "analyze videos," "reverse-engineer a video style," "pull mascot design," or any request to understand and document how a video was made for recreation purposes. Produces STYLE-GUIDE.md (cohort invariants) and optionally MASCOT-KIT/ (reference images + per-generator prompts) for driving AI image and image-to-video generators.
---

# Video Style Extractor

Extract the complete editing style from one or more videos, including pixel-art mascot profiles when present, and produce artifacts ready for AI image generators and image-to-video generators.

## Prerequisites

- **Gemini API key** in the environment as `GEMINI_API_KEY`. Set it with `export GEMINI_API_KEY="your-key"` (add the line to your shell profile to make it stick).
- **google-genai** Python SDK
- **ffmpeg** and **yt-dlp** on your PATH
- Python deps from `scripts/requirements.txt`:
  ```bash
  pip install -r "${CLAUDE_SKILL_DIR}/scripts/requirements.txt"
  ```

All local helpers live under `scripts/` and are invoked as `python -m scripts.<module>` from the skill directory (`cd "${CLAUDE_SKILL_DIR}"`).

## Workflow

### Step 1: Acquire videos

Create a working directory:

```bash
mkdir -p <working-dir>/per-video
```

Accept **either**: a folder of `.mp4`/`.mov` files, **or** a list of URLs. `yt-dlp` covers YouTube and most public video hosts. For Instagram and TikTok, use whatever downloader you already have available (a scraping service such as Apify works if you have an account; otherwise download the files by hand and point the skill at the folder).

For each source video, create a slug folder:

```bash
mkdir -p <working-dir>/per-video/<slug>/{frames,mascot-raw}
```

### Step 2: Scene segmentation

For each video, detect cuts with PySceneDetect:

```bash
python -m scripts.scene_detect <video> <working-dir>/per-video/<slug>/scenes.json
```

### Step 3: Scene-aware frame sampling

```bash
python -m scripts.scene_aware_sample <video> \
  <working-dir>/per-video/<slug>/scenes.json \
  <working-dir>/per-video/<slug>/frames/
```

Emits `frames/frame_NNNN.jpg` plus `frames/manifest.json`.

### Step 3b: Contact sheets (optional, when the output feeds a recreation)

If the extraction is destined for a programmatic recreation (for example the `remotion-video-builder` skill), also tile each scene's frames into one **contact sheet**: a start-to-end grid collage. Text-only models cannot watch video, so a contact sheet encodes the motion arc as a single readable image and is the highest-leverage artifact for downstream agents.

```bash
# per scene, from the frames already sampled in Step 3
ffmpeg -pattern_type glob -i '<slug>/frames/scene03_*.jpg' \
  -vf "scale=480:-1,tile=4x2" -frames:v 1 <slug>/frames/scene03-sheet.jpg
```

Pair each sheet with a per-scene recreation prompt from Gemini, describing what has to happen between the first and last cell.

### Step 4: Audio metrics

```bash
python -m scripts.audio_metrics <video> <working-dir>/per-video/<slug>/audio-metrics.json
```

### Step 5: Gemini Pass A, cohort visual invariants

Upload **frames only** (not full videos). Budget: 1 keyframe per scene, capped at 20 per video, capped at 200 total. Downsample proportionally if the cohort exceeds the cap.

Use the **Pass A** prompt from `references/gemini-prompts.md`. Save to `<working-dir>/cohort-analysis.md`.

### Step 6: Gemini Pass B, per-video transcript and cadence

For each video, upload the full video via Files API. Use the **transcription** prompt from `references/gemini-prompts.md`. Save to `per-video/<slug>/gemini-transcript.md`.

### Step 7: Gemini Pass C, mascot detection

For each video, run the Pass C prompt from `references/mascot-prompts.md`. Save results. If `>=1` video returns `mascot_present: true`, activate the **Mascot Track** (Step 8).

If the user supplies `--force-mascot <hint-image>`, skip detection and activate Mascot Track with the hint as seed.

### Step 8: Mascot Track

Only runs if pass C activated it.

**M1. Dense extraction**: re-sample at 4fps within the mascot-containing ranges only:

```bash
# For each mascot-bearing video, for each flagged range:
ffmpeg -ss <start> -t <duration> -i <video> -vf "fps=4" -q:v 2 <slug>/mascot-raw/raw_%04d.jpg
```

**M2. Bounding boxes**: use the M2 prompt from `references/mascot-prompts.md`. Drop frames with confidence < 0.6.

**M3. Crop + bg-remove**: for each kept frame:

```bash
# Pillow crop to bbox+10% (inline python or small helper)
python -m scripts.bg_remove <cropped>.png <slug>/mascot-raw/iso_NNNN.png <slug>/mascot-raw/iso_NNNN.meta.json
```

**M4. Native resolution**

```bash
python -m scripts.native_resolution <slug>/mascot-raw/iso_0001.png <slug>/native-res.json
```

**M5. Palette quantization** (pool all isolated mascot PNGs across the cohort):

```bash
python -m scripts.palette_quantize <slug>/mascot-raw/iso_*.png MASCOT-KIT/palette.json
```

Also emit `palette.gpl` and `palette-swatch.png` (use Pillow inline).

**M6. Native fps** (use the mascot bbox from M2):

```bash
python -m scripts.native_fps_detect <video> <slug>/native-fps.json <x> <y> <w> <h>
```

**M7. Pose clustering**: use M7 prompt. Save pose_map JSON.

**M8. Consistency check**: use M8 prompt. If variants exist, write `MASCOT-VARIANTS.md` and proceed with the dominant variant only.

**M9. Canonical frame selection**: use M9 prompt. Copy selected file to `MASCOT-KIT/canonical-reference.png`.

**M10. Sprite sheet**

```bash
python -m scripts.sprite_sheet <pose_map.json> MASCOT-KIT/sprite-sheet.png
```

**M11. Constraints**: use M11 prompt. Save as structured JSON into `mascot-profile.json`.

**M12. Prompt distillation**: use M12a and M12b prompts. Save as `MASCOT-KIT/STATIC-PROMPT.md` and `MASCOT-KIT/ANIMATED-PROMPT.md`.

**Write `MASCOT-KIT/mascot-profile.json`** aggregating all mascot-track outputs per the schema in `references/pipeline-design.md`.

**Write `MASCOT-KIT/MASCOT-EVIDENCE.md`**, where every claim traces to a specific frame path.

### Step 9: Frame verification (main thread)

Using the Read tool, inspect keyframes per video:
- frame at 10%, 25%, 50%, 75%, 90% of duration (scene-snapped)
- every frame cited by Pass A as hex/typography evidence
- 3 random mascot-containing frames per mascot-bearing video

Append YAML corrections to `per-video/<slug>/corrections.md`:

```yaml
- claim_id: pass_A#palette#accent_1
  original: "#FF6A3D"
  corrected: "#FF5A33"
  evidence_frame: frames/frame_0034.jpg
```

### Step 10: Synthesizer subagent

Dispatch a subagent with the prompt from `references/synthesizer-subagent-prompt.md`. It produces `STYLE-GUIDE.md`.

### Step 11: Detailed single-video guide (optional)

If the run was a single video and you want the deeper per-video breakdown (timeline map, script template, Remotion token block), also produce `STYLE-GUIDE-DETAILED.md` using the template at `references/detailed-guide-template.md`.

### Step 12: Run log

Throughout the workflow, call `scripts.run_log` at every major step to append status, cost, and warnings to `<working-dir>/run-log.md`. At the end, emit a summary block with:
- total Gemini cost (USD)
- mascot track activation
- low-confidence flags raised
- bg-removal method used per video

## Output structure

See `references/pipeline-design.md` for the canonical structure and JSON schemas. Primary deliverables:

- `STYLE-GUIDE.md`: cohort invariants
- `MASCOT-KIT/STATIC-PROMPT.md` + `ANIMATED-PROMPT.md`: prompts
- `MASCOT-KIT/canonical-reference.png` + `sprite-sheet.png` + `poses/`: reference images
- `MASCOT-KIT/palette.json` + `palette.gpl` + `palette-swatch.png`
- `MASCOT-KIT/mascot-profile.json`: canonical machine-readable profile

## Key rules

1. **Always use `gemini-2.5-pro`**. Flash misses subtle details.
2. **Visually verify keyframes** with the Read tool. Gemini gets hex values wrong by 10 to 20% routinely.
3. **For cohort analysis**, upload FRAMES ONLY, not full videos. Stay under the 200-frame budget.
4. **Variants are flagged, not blended.** If the mascot has design variants across videos, record them in `MASCOT-VARIANTS.md` and proceed with the dominant variant.
5. **Low-confidence fields must be flagged**, not silently substituted. The prompt distillation (M12) uses qualitative fallbacks when confidence is "low".
6. **Cite every claim.** Every hex, every font, every timing is traceable to a frame path.
