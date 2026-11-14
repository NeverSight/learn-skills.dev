---
name: whiteboard-video
description: Generate smooth hand-drawn whiteboard and story videos directly inside Codex from text scripts, GPT Image 2 color storyboards, scene plans, SVGs, line art, or local images. Supports 30 built-in visual styles, automatic recommendations, custom media recipes, natural-block coarse/detail drawing with block-local or whole-scene color reveal, local image-to-line-art extraction, stroke/path drawing, hand/pen-tip following, narration/TTS including Doubao Voice 2, and FFmpeg composition.
---

# Whiteboard Video

Use this skill to create local-first whiteboard videos without Canva. This skill is an adapter for the separately installed `whiteboard-video-engine` Python package. Uploaded photos and dense illustrations are converted to line art locally; do not use GPT Image 2 to generate final line art. For script-driven story videos, keep one registered asset pair per scene: GPT Image 2 creates the **color storyboard**, then a local neural extractor derives line art from that exact color file. The preferred stack is:

1. `gpt-image-2` for full-color storyboard frames only, never production line art or embedded captions.
2. `Informative Drawings` local model, preferably `anime_style`, for registered line-art extraction.
3. `Anime2Sketch` local model for illustration/anime-like sources or as the neural fallback.
4. Optional `vtracer` SVG vectorization when installed.
5. Optional Doubao Voice 2 (`seed-tts-2.0`) or Edge TTS for narration. Keep the default sidecar SRT for editing, or explicitly use `--burn-subtitles` for a ready-to-publish subtitled MP4.

There is no edge-detection fallback. If neither neural model is installed, `extract-lineart` and `render-photo` must fail instead of silently producing a weak outline.

## Quick Start

Install the engine before using this skill:

```bash
python3 -m pip install "git+https://github.com/gnipbao/whiteboard-video-engine.git"
```

For local engine development:

```bash
python3 -m pip install -e /path/to/whiteboard-video-engine
```

When the engine is installed in a virtual environment, invoke the wrapper with that environment's Python, or set `WHITEBOARD_ENGINE_PYTHON=/absolute/path/to/venv/bin/python`. The wrapper will re-exec only the explicitly configured interpreter.

Run commands from the project root that contains `tools/lineart`, but always call the installed Skill wrapper by absolute path. The wrapper delegates to the installed engine package while local model wrappers are auto-discovered from the current working directory.

Never call a project-local `whiteboard-video/scripts/whiteboard_cli.py`. Old project copies may prepend a bundled `src` directory and silently shadow the installed engine, causing stale defaults such as the procedural hand cursor to reappear.

```bash
MOCK=1 python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" run examples/ten-second-demo.md -o /tmp/whiteboard-demo.mp4 --scenes 2 --fps 30 --width 640 --height 360 --scene-assets direct-lineart --animation-preset block-speedpaint
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" extract-lineart photo.png -o lineart.png --provider auto
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" render-photo photo.png -o /tmp/photo-whiteboard.mp4 --duration 15 --fps 30 --lineart-provider auto --stroke-detail rich --hand asian
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" render-image lineart.png --source-image photo.png --source-fit exact --size-from-image --color-fill contour-wipe -o /tmp/color-fill-whiteboard.mp4 --duration 15 --fps 30 --tail-color 4.5 --hand asian
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" render-image examples/apple.svg -o /tmp/apple-whiteboard.mp4 --duration 2 --fps 24 --width 640 --height 360 --hand asian
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" render-image examples/apple.svg -o /tmp/multiline-text.mp4 --duration 6 --fps 24 --width 720 --height 960 --draw-text-file caption.txt --draw-text-position top --draw-text-align left --draw-text-reveal line-wipe --draw-text-order before --hand none
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" list-styles
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" recommend-styles story.md --limit 5
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" list-hands
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" doctor
```

## Visual Style Selection

The engine provides 30 versioned, media-named visual recipes. The stable default
is `warm-crayon-storybook`, also configurable with `WHITEBOARD_STYLE`. Style
selection belongs to `plan-script` and `run`: planning uses the semantic visual
guidance, while `run` also inherits the recipe's maintained renderer defaults:
`block_fill_style`, `color_fill_scope`, `stroke_detail`, `line_thickness`, line-art snap and its
threshold, preferred/capped block counts, overlap, and block order. The resolved
recipe and optional `--theme` are stored in `project.json`; their semantic fields
participate in planning and resume fingerprints.

Do not pass style-selection flags to `render-photo` or `render-image`; those
single-image commands do not resolve a recipe. They use explicit command defaults,
including `--line-thickness 0`, `--stroke-detail rich`,
`--block-fill-style crayon`, `--color-fill-scope block`, and `--block-overlap 0.08`, until their own flags
override them.

At the start of a new script-to-story job, run `recommend-styles` to inspect the
best local candidates. This is decision support, not a mandatory approval gate:

- Honor an explicitly named style without asking again.
- When the user requests automatic selection, pass `--style auto`; it chooses the
  first deterministic content-aware recommendation without a model or network call.
- When no visual preference is given, do not block on a 30-option question. Proceed
  with the stable default, or with one clearly better `native` recommendation when
  the user has delegated art direction; briefly report the choice.
- Prefer `native` for unattended final production. Use a short preview before an
  `adaptive` style, and explicitly flag `experimental` styles as source-dependent.

Compatibility groups:

- `native` (15): `warm-crayon-storybook`, `colored-pencil-diary`,
  `clean-whiteboard`, `minimal-line-explainer`, `marker-whiteboard`,
  `rough-diagram`, `pressure-ink-notes`, `semantic-ink`, `anime-graphite`,
  `bean-doodle-infographic`, `organic-contour-doodle`, `naive-marker-notes`,
  `notebook-pencil-doodle`, `inked-storybook`, `blueprint-pencil`.
- `adaptive` (9): `kid-crayon`, `raw-kid-crayon`,
  `emotional-watercolor-sketch`, `ink-wash-minimal`, `retro-gouache-concept`,
  `nordic-gouache-storybook`, `sunlit-storybook`, `editorial-portrait`,
  `real-crayon-paper`.
- `experimental` (6): `ballpoint-scribble`, `warm-flat-storybook`,
  `zine-riso-collage`, `manga-screentone`, `linocut-editorial`,
  `ms-paint-doodle`.

List or recommend recipes:

```bash
CLI="${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py"
python3 "$CLI" list-styles
python3 "$CLI" list-styles --compatibility native
python3 "$CLI" list-styles --json
python3 "$CLI" recommend-styles story.md --limit 5 --json
```

Choose a built-in recipe, use automatic selection, provide a bounded inline
description, or load a repeatable UTF-8 text/JSON recipe:

```bash
python3 "$CLI" run story.md -o /tmp/story.mp4 --style colored-pencil-diary
python3 "$CLI" run story.md -o /tmp/story.mp4 --style auto
python3 "$CLI" run story.md -o /tmp/story.mp4 \
  --custom-style "Loose blue-pencil travel sketch, one warm-orange accent, broad white space"
python3 "$CLI" run story.md -o /tmp/story.mp4 \
  --custom-style-file /absolute/path/to/style.json \
  --theme "Quiet early morning with restrained optimism"
```

`--style`, `--custom-style`, and `--custom-style-file` are mutually exclusive.
`--theme` is additive story-specific art direction and cannot replace the
production contract: complete subjects, extractable outlines, natural object
grouping, useful negative space, and no generated captions or pseudo-writing.
Custom JSON should normally use `extends` plus bounded `render` overrides; see
`references/pipeline.md` for the schema. An explicit custom JSON `id` must begin
with `custom-`. `provenance` is not an accepted author field; the engine marks
loaded recipes as user-authored itself. Visual recipes use generic media and
production-method names, not artist names, and include no third-party sample
images or brush assets.

Style 9, `anime-graphite`, defaults to `color_fill_scope=scene`. Its people and
props still draw as complete natural line-art blocks, but the registered color
frame—including snow, walls, streets, sky, and paper-toned washes—is revealed
only once across the full canvas. For this and similar full-bleed styles, make
the storyboard prompt describe one continuous, low-detail environmental
backdrop and reject panels, frames, rectangular scenic cutouts, or disconnected
background islands.

## Script to Story Video

The production scene pipeline is:

```text
script -> scene plan -> GPT Image 2 color frame -> local neural line art
       -> coarse natural blocks -> local details
       -> block-local color OR one whole-scene registered color/background pass
       -> optional sparse handwritten annotations -> silent or narrated MP4
       -> editable sidecar SRT -> optional final subtitle burn-in
```

`block-speedpaint` infers spatial drawing blocks for coarse contours and local details. With `--color-fill-scope block`, each block then receives its own local color beat. With `--color-fill-scope scene`, the same natural line blocks remain intact while the complete registered color frame and continuous background arrive in one full-width pass. Scene scope uses roughly the first 72% of the drawing interval for block lines; the global color pass starts near 68%, overlaps the last details by about 4%, and finishes at the end of the interval. A narrated run can use phrase timing cues to pace this same drawing clock: active speech advances the picture and meaningful pauses briefly hold it. The pipeline always writes an editable SRT beside the MP4 and leaves the picture clean by default; pass `--burn-subtitles` only when the requested deliverable needs narration subtitles baked into the final MP4. Optional annotations are short, positioned labels that never enter the GPT storyboard, extracted line art, or object grouping; the renderer intentionally adds them as late scene-video pixels, independently of the final SRT subtitle layer.

Configure credentials through the shell or a secret manager, never in scripts, prompts, `project.json`, or committed `.env` files:

- Images and automatic scene planning: `OPENAI_API_KEY`; optional `OPENAI_BASE_URL` must point to the intended trusted OpenAI-compatible endpoint. It is not required when both `--scene-plan` and `--storyboard-dir` are supplied.
- Silent master: use `--tts-provider none`; no speech credential is initialized or required.
- Doubao new console: `DOUBAO_TTS_API_KEY` (aliases: `DOUBAO_API_KEY`, `MODEL_SPEECH_API_KEY`).
- Doubao legacy console: set both `DOUBAO_TTS_APP_ID` and `DOUBAO_TTS_ACCESS_KEY` instead of the API key.
- Doubao defaults: `DOUBAO_TTS_RESOURCE_ID=seed-tts-2.0`, `DOUBAO_TTS_ENDPOINT=https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse`, `DOUBAO_TTS_VOICE=zh_female_vv_uranus_bigtts`, MP3 at 24 kHz. The provider requests Seed-TTS 2.0 subtitle timing and uses its sentence/word timestamps for animation and SRT timing. Use only a speaker ID enabled for the user's account and do not redirect credentials to another endpoint.

Run the real color-storyboard pipeline:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" run story.md \
  -o /tmp/story.mp4 \
  --scenes 6 --fps 30 --width 1920 --height 1080 \
  --style warm-crayon-storybook \
  --image-model gpt-image-2 --image-quality low \
  --scene-assets color-to-lineart --lineart-provider auto \
  --animation-preset block-speedpaint \
  --tts-provider none
```

Use `--image-quality low` for drafts and `medium` for a final render when the visual gain justifies the extra cost. The full `run` command defaults to 30 fps, `gpt-image-2`, no burned narration, and `block-speedpaint`. Its fill, fill scope, line, snap, and natural-block settings are not separate fixed CLI defaults: when omitted, they inherit the resolved style snapshot. The stable `warm-crayon-storybook` recipe currently resolves to automatic line width, rich stroke detail, crayon fill with `color_fill_scope=block`, at most four preferred natural blocks, and `0.16` overlap; selecting another style may change any of these values. Style 9 resolves to `color_fill_scope=scene`. Connected objects are never split merely to reach a count; use `--draw-blocks 0` for uncapped automatic grouping up to the resolved `max_draw_blocks`. Use `--tts-provider none` for a silent edit master, or select Doubao/Edge and pass `--voice <speaker-id>`. Both narrated and silent runs write `<video-name>.srt`. Add `--burn-subtitles` to render that SRT into the final `-o` MP4 while retaining the sidecar; style it with `--subtitle-font`, `--subtitle-font-size`, `--subtitle-margin-v`, and `--subtitle-outline`. The legacy `--captions` and `--no-captions` flags are deprecated no-ops and are mutually exclusive with `--burn-subtitles`. Scene annotations remain independent.

Only `run` treats the following as overrides of the selected style. Omit them to
inherit the recipe:

- `--block-fill-style crayon|clean|soft-wash|dry-brush`
- `--color-fill-scope block|scene`
- `--stroke-detail balanced|rich|max`
- `--line-thickness 0..16` (`0` requests automatic source-aware sizing)
- `--line-art-snap` / `--no-line-art-snap` and
  `--line-art-snap-threshold 1..254`
- `--max-draw-blocks N`, `--draw-blocks N` or `0` for automatic
  grouping, `--block-overlap 0..0.65`, and `--block-order reading|source`
- `--block-sequence 1,0,...` for an inspected explicit inferred-block order;
  this is a run-time ordering instruction rather than a recipe default

For a 16:9 Doubao Voice 2 delivery with burned narration subtitles:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" run story.md \
  -o /tmp/story-subtitled.mp4 \
  --scenes 6 --fps 30 --width 1920 --height 1080 \
  --image-model gpt-image-2 --image-quality low \
  --scene-assets color-to-lineart --lineart-provider auto \
  --animation-preset block-speedpaint --draw-blocks 4 --block-overlap 0.16 \
  --tts-provider doubao --voice zh_female_vv_uranus_bigtts \
  --burn-subtitles --subtitle-font "sans-serif" \
  --subtitle-font-size 16 --subtitle-margin-v 22 --subtitle-outline 1.6
```

FFmpeg/libass burns subtitles only after the clean scene composition and SRT have succeeded. The engine renders to a temporary sibling file and atomically replaces the requested MP4, so a subtitle-filter failure leaves the clean MP4 and SRT available for recovery.

With Doubao Voice 2, use valid provider subtitle timing as the preferred narration clock. Group returned word timestamps into short readable phrase beats; drawing advances at a steady rate while a phrase is spoken and briefly holds across real punctuation pauses. The measured narration duration, not the estimated scene-plan duration, controls a narrated scene; `duration_sec` remains the silent-render fallback. Persist provider timing beside cached audio as `scene_NN.alignment.json`, and clamp every SRT cue to the real audio endpoint so no subtitle leaks into the visual tail hold. If Doubao returns no valid timing, retain valid authored `timing_cues`; only when neither exists should the SRT use deterministic estimated phrases while drawing keeps its continuous clock. Narrated composition must have one audio file for every scene; never compact a partial audio list because that shifts later voices into earlier scenes.

If Codex or another tool already generated the color storyboards, preserve their scene order and name them `scene_01.png`, `scene_02.png`, and so on (`.webp`, `.jpg`, and `.jpeg` also work). Save the approved scene list as JSON with `id`, `narration`, `image_prompt`, and positive `duration_sec` fields. An optional `annotations` list may contain at most two objects with `text`, `x`, and `y`; coordinates are normalized top-left positions. Keep each label to 2–5 Chinese characters when possible, leave most scenes empty, and keep `y <= 0.72` so the lower area remains available for post-production subtitles. An optional ordered `timing_cues` list accepts `text`, local `start_sec`, local `end_sec`, and optionally cumulative `draw_to` progress ending at `1.0`; use it for a pre-aligned silent or imported-audio workflow. In a Doubao run, valid official timestamps replace authored cues; authored cues remain the fallback if the provider returns no usable timing. Then supply both assets to bypass OpenAI scene planning and image generation entirely:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" run story.md \
  -o /tmp/story-from-frames.mp4 \
  --scene-plan /absolute/path/to/scene-plan.json --fps 30 \
  --storyboard-dir /absolute/path/to/storyboards \
  --lineart-provider auto --animation-preset block-speedpaint --draw-blocks 4 \
  --tts-provider none
```

The scene-plan ids must be consecutive `1..N`; this locks each narration to `scene_01..scene_N` and makes `--scenes` unnecessary. In silent mode the engine initializes neither OpenAI nor a TTS provider when both the plan and storyboard directory are supplied.

For one color frame, inspect and tune block drawing independently:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" render-photo scene_01.png \
  -o /tmp/scene-01.mp4 --duration 8 --fps 30 \
  --lineart-provider auto --animation-preset block-speedpaint \
  --draw-text "出发" \
  --max-draw-blocks 6 --block-order reading --block-overlap 0.08 \
  --hand asian
```

Use `--draw-blocks <count>` as a preferred maximum when a scene contains many independent islands; it never authorizes cutting a connected person or prop. Use `--block-sequence 1,0` only after inspecting inferred block IDs; it reorders blocks and rejects duplicates or unknown IDs.

## Workflow

Before choosing providers or generating assets, inspect style recommendations
for every new story script and resolve one recipe using the non-blocking policy
above. Keep the stable default when the request supplies no useful art direction;
do not repeatedly ask the user to choose from the entire library.

1. Use `render-photo` for uploaded photos or dense illustrations. It extracts local line art first, then renders with the original image as the color-fill source.
2. Use `extract-lineart` when you want to inspect or reuse the line-art PNG before rendering.
3. Use `render-image` when the user already has a clean SVG or line-art PNG.
4. Use `plan-script` and `run` for script-driven scenes. In real `auto` mode, `run` generates a color scene with `gpt-image-2`, then extracts pixel-registered line art locally from that same file. Use `--scene-assets color-to-lineart` to make this choice explicit.
5. Use `analyze-image` to estimate stroke count and foreground density.
6. Use `compose` to concatenate rendered scene clips.
7. With `run` or `render-photo`, use `--lineart-provider auto|informative|anime2sketch|anime|manga`; the standalone `extract-lineart` command spells the selector `--provider`. `render-image` has no provider selector because its input is already line art. `auto` tries Informative Drawings first, then Anime2Sketch; `manga` is only a compatibility alias for Anime2Sketch.
8. Configure external deep extractors through environment variables:
   - `WHITEBOARD_INFORMATIVE_DRAWINGS_CMD`
   - `WHITEBOARD_ANIME2SKETCH_CMD`
   Commands may include `{input}` and `{output}` placeholders; otherwise input and output are appended as positional arguments.
9. Use `--svg-output <line.svg>` with `extract-lineart` or `render-photo` when `vtracer` is installed and you want SVG paths instead of raster skeleton tracing.
10. Use `--hand asian|black|children|white|procedural|none` to select the hand cursor. Built-in PNG hands keep a fixed orientation and only translate with the pen tip.
11. For `render-image`, use a color source with the exact same pixel size/aspect/crop as the line art whenever possible, then render with `--source-image <source> --source-fit exact --size-from-image --color-fill contour-wipe`. `render-photo` wires its input image as the registered color source automatically.
12. Before final color fill, the renderer snaps missing registered line-art pixels back to the redrawn canvas so small extracted-stroke omissions do not look unfinished. For `render-photo` and `render-image`, the fixed guide threshold defaults to `235`; use `--no-lineart-snap` and `--lineart-snap-threshold` only for single-image debugging. In `run`, snap behavior and threshold inherit the selected style unless explicitly overridden with `--line-art-snap` / `--no-line-art-snap` and `--line-art-snap-threshold`.
13. For `render-photo` and `render-image`, `--stroke-detail rich` is the fixed default; use `max` only when faces/logos/badges still lose too many short strokes. In `run`, omit `--stroke-detail` to inherit the style.
14. Treat narration, subtitles, and annotations as separate roles. Narration controls story/audio timing; the editable sidecar SRT is always preserved and may either stay on the post-production track or be burned into the final MP4 with `--burn-subtitles`; annotations are optional scene-plan labels and never copy narration.
15. For `block-speedpaint`, positioned annotations appear late using a per-character left-to-right pencil/typewriter reveal. They are not added to image strokes, so they cannot change inferred object blocks. `--draw-text` belongs only to standalone `render-photo` / `render-image` and should be used only for a deliberate short label or title. Use `--burn-subtitles`, not the deprecated `--captions`, when `run` narration subtitles must be baked into the deliverable.
16. On the single-image `render-photo` / `render-image` commands, crayon drawings that should begin as an uncolored sketch can use `--line-reveal detail-wipe --hand none`; the initial layer keeps heavy outer contours plus dense neutral-black areas such as hair, while leaving colored surfaces and fine internal texture blank. Remaining details arrive through a soft left-to-right mask. These flags are not `run` options.
17. On those same single-image commands, pair that mode with `--color-fill left-to-right-gradient` to restore the original crayon color from left to right. A strong 10-second starting point is `--tail-color 4 --base-line-opacity 0.76`; these are not style-recipe fields.
18. Prefer `--animation-preset block-speedpaint` for story scenes. In `block` color scope, each natural object progresses through coarse contours, local details, and left-to-right color. In `scene` scope, objects keep those natural coarse/detail blocks, then the complete registered color frame and background reveal once across the canvas; use this for continuous full-bleed environments and for style 9. Sparse annotations overlay late, during roughly the final 15% of the scene, and may overlap the drawing's last beats; they never delay the first stroke. Only the legacy standalone full-caption role may add a short pre-draw lead-in.
19. Use `--scene-plan <json> --storyboard-dir <dir>` for externally generated color frames named `scene_01.*`, `scene_02.*`, and so on. This skips OpenAI planning/image clients; the engine still extracts line art locally from every supplied frame.
20. Use `--tts-provider none` for a silent master, `--tts-provider doubao` for Doubao Voice 2, or `--tts-provider edge` for Edge TTS. Valid Doubao word timestamps are grouped into phrase beats that pace coarse lines, details, the selected block/scene color scope, and sparse annotations through one shared clock. Without valid provider timing, retain authored cues when present; only the no-provider-cue/no-authored-cue case uses estimated SRT phrases while preserving continuous drawing motion. `--burn-subtitles` consumes that same SRT after composition, so sidecar and picture timings stay identical. Cache provider timing in `audio/scene_NN.alignment.json`; invalidate it with changed narration, voice, or synthesis settings. Do not log, print, or commit provider credentials.
21. Real runs reject `--scene-assets direct-lineart`; it exists only for deterministic Mock previews. Production always keeps a GPT color source and locally extracted registered line art.
22. The pipeline normalizes color storyboards onto the project canvas before extraction and fingerprints the script plan, source, line art, audio, and render parameters so `--resume` cannot silently pair new content with stale layers.

Prefer `MOCK=1` for integration tests and low-cost previews. Real providers are lazy-loaded and require configured provider credentials only for script-to-scene image or narration generation, not for uploaded-photo line-art extraction.

## Local Line-Art Step

For uploaded photos:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" extract-lineart source.png \
  --provider auto \
  -o lineart.png
```

Then render:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" render-image lineart.png \
  --source-image source.png \
  --source-fit exact \
  --size-from-image \
  --color-fill contour-wipe \
  --stroke-detail rich \
  --line-thickness 1 \
  -o output.mp4 \
  --duration 15 --fps 30 --tail-color 4.5 --hand asian
```

Or use the one-step shortcut:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/whiteboard-video/scripts/whiteboard_cli.py" render-photo source.png \
  -o output.mp4 \
  --duration 15 --fps 30 \
  --lineart-provider auto \
  --stroke-detail rich \
  --hand asian
```

## Quality Rules

- Do not use GPT Image 2 for line-art conversion. `gpt-image-2` produces the color source only; local line-art extraction from that exact source is the source of truth.
- Prefer `Informative Drawings` `anime_style` for quality when installed.
- Prefer `Anime2Sketch` for illustration/anime-like inputs or when Informative Drawings is unavailable.
- Preserve Anime2Sketch tonal output: use its cleaned binary mask as the invisible motion guide and its surviving grayscale values as the visible line art. Do not flatten the presentation layer to solid black.
- Do not use Canny/XDoG/edge-only fallback for production outputs.
- Optional `vtracer` can convert extracted line-art bitmaps to SVG paths for smoother path sampling.
- Keep the original uploaded image as the color-fill source when dimensions match. Because the line art is extracted from that same image, no anti-shrink or source-alignment correction should be needed.
- Render quick previews at 640x360 and 12-24fps when speed matters; the full story pipeline defaults to 30fps, and final output should normally stay at 30fps unless 60fps is specifically needed.

## Implementation Notes

This skill does not vendor engine code. `scripts/whiteboard_cli.py` imports `whiteboard_skill.cli` from the installed `whiteboard-video-engine` package. Core engine modules live in the engine repository:

- `providers/lineart.py`: local line-art providers, Informative Drawings and Anime2Sketch wrappers, optional vtracer integration.
- `preprocess.py`: SVG parsing, raster binarization, Zhang-Suen skeletonization, 8-neighbor stroke tracing.
- `whiteboard.py`: classic stroke renderer plus `block-speedpaint`, hand/pen-tip cursor, line-art snap completion, separate text reveal, and block-local or whole-scene color fill.
- `pipeline.py`: resumable `work/<project_id>/` orchestration.
- `styles.py`: 30 built-in recipes, compatibility metadata, recommendation,
  constrained custom-style loading, prompt composition, and style fingerprints.
- `compose.py`: scene composition plus optional atomic FFmpeg/libass subtitle burn-in.
- `providers/`: mock, GPT Image 2/OpenAI, Edge TTS, and Doubao Voice 2 provider interfaces.

Read `references/pipeline.md` only when modifying or extending the full script pipeline.
