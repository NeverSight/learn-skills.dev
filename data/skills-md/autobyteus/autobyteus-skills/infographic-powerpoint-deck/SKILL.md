---
name: infographic-powerpoint-deck
description: Create image-based PowerPoint decks by (1) designing a slide plan, (2) generating one 16:9 infographic slide image per slide with all text baked into the image (Chinese/English supported), and (3) assembling an images-only .pptx that simply concatenates those images full-screen. Use when the user wants polished, consistent visuals with extensible style packs (cinematic, editorial, warm pastoral, tech, youth social, academic, corporate), prefers not to hand-layout PPT objects, or wants a repeatable prompt workflow to iterate over time.
---

# Infographic PowerPoint Deck

## Quick start (default: images-only deck, style-pack architecture)

1. Pick one **style pack folder** (required) from `references/style-pack-catalog.md`.
   - If user does not specify style, default to `editorial-light`.
2. Compose the style block bundle:
   - Run `scripts/compose_style_pack_blocks.py --pack-id <id>` (or manually read the style-pack files).
   - This yields a consistent block set: profile + motif + consistency + scene bias.
3. Draft a slide list (8–20 slides): title, quote(s), key points, scene ID.
   - Scene IDs come from `references/scene-catalog.md`.
   - If you need fast defaults, reuse presets from `references/scene-preset-library.md`.
   - If you already have a reasoning artifact (recommended): convert `slide_extraction.md` rows into slides.
   - If `slide_extraction.md` already includes `Recommended style pack ID` / `Scene ID` / `Layout hint`, use those fields directly.
4. For each slide, fill `references/prompt_template.md`:
   - Paste the composed style block bundle.
   - Paste exact required text (verbatim).
   - Add slide-specific scene layer details and icons.
5. Generate each slide as one **16:9 image**.
   - In the slide prompt text, explicitly include a ratio lock sentence (e.g., `画布比例硬约束：16:9 横版（宽屏），禁止方图。`).
   - In the tool call, explicitly set ratio config when supported (e.g., `generation_config` with `aspect_ratio: "16:9"`).
6. QA readability + text accuracy; regenerate only failed slides.
   - If any slide is not 16:9 or has text defects, regenerate the image directly.
   - Do **not** crop, pad, resize, or post-process generated images unless the user explicitly asks.
7. Assemble images-only PPTX with `scripts/build_images_only_pptx.py`.

Outputs to produce in the user’s workspace:
- `slides_plan.md` (slide-by-slide content + visuals)
- `prompts.md` (the exact prompts used for each slide)
- `slides/slide01.png ...` (final 16:9 images)
- `deck_images_only.pptx` (concatenated images)

## Recommended upstream artifact (thinking before slides)

For higher-quality decks, start from a logically structured article + extraction table:
- Use the `deep-research-article` skill to produce `article.md` and `slide_extraction.md`.
- Prefer the deep-research handoff-contract columns (style pack ID, scene ID, layout hint, text budget) so each row maps directly to one slide prompt.
- If the extraction table is legacy/simple format, normalize it using `references/deep_research_handoff_mapping.md` before prompt writing.

## Prompt stack (minimal vs full)

- Minimal stack (recommended for most decks):
  - `references/style-pack-catalog.md` (choose pack ID)
  - `references/style-pack-system.md` (load order + composition rules)
  - `references/style-packs/<pack-id>/` (pack-local blocks)
  - `references/typography_spacing_lock.md`
  - `references/text_fidelity_block.md`
  - `references/negative_prompt_block.md`
- Full stack (use when you want maximum narrative + visual control):
  - Minimal stack +
  - `references/storyboard_library.md`
  - `references/shot_mood_library.md`
  - `references/scene-catalog.md`
  - `references/scene_library.md`
  - `references/layout_library.md`
  - `references/chinese_quote_compression.md` (when quotes are long)

## Style-pack system (modular and scalable)

Use folderized style packs so each style is self-contained:
- Each style pack lives in `references/style-packs/<pack-id>/`.
- Each pack has its own `manifest.toml` and block files that define the look.
- Packs can inherit from `base-core` to reuse shared constraints.
- Prompts are composed as: **base-core + chosen pack + slide-specific content**.
- This avoids cross-file mismatch and makes new style creation deterministic.

Note: despite the Bible-themed examples, this workflow works for any topic. Swap scenes/props in `references/scene_library.md` to match your domain (product, research, training, etc.).

## Slide prompt recipe (copy/paste template)

Read `references/prompt_template.md` and fill it per slide. Keep it extremely explicit:
- Put **all required on-slide text** under a “必须出现文字（逐字准确）” section.
- For visuals, describe **scene layers** (far/mid/foreground), plus 3–8 concrete objects.
- Specify what must be **subtle/low-contrast** so text stays readable.

If you need inspiration for “更有画面感”的场景素材与道具库, read `references/scene_library.md`.
If you need stable scene IDs + tags for selection/filtering, read `references/scene-catalog.md`.
If you need copy-ready visual scene blocks, read `references/scene-preset-library.md`.
If you need fast, reliable infographic compositions, read `references/layout_library.md`.
If you need “镜头语言/时间天气/光影情绪” presets, read `references/shot_mood_library.md`.
If you need style modularity, read `references/style-pack-system.md` and use `scripts/compose_style_pack_blocks.py`.
If you want fewer typos and more readability, paste these into every slide prompt: `references/typography_spacing_lock.md`, `references/text_fidelity_block.md`, `references/negative_prompt_block.md`.
If you want “像分镜一样”的观看节奏，read `references/storyboard_library.md`.
If you have long verse blocks, read `references/chinese_quote_compression.md` and split quotes across slides (do not paraphrase).

## Quality bar (and how to iterate)

For each slide:
- **Readability first**: text never overlaps busy imagery; use a dedicated text panel.
- **No hallucinated text**: forbid extra words/logos/watermarks.
- **Chinese accuracy**: if any characters are wrong, regenerate that slide with:
  - shorter quote blocks,
  - “逐字准确，不得改写，不得增删标点/空格”,
  - simpler backgrounds.
- **Engagement**: add background scenes + textures + icon clusters, but keep them low-contrast.

Common failure fixes:
- Tool call fails/intermittent errors: retry after a short wait; keep prompt stable; reduce scene complexity only if repeats.
- Text too small: reduce bullet count; split into two slides; demand “大字号、舒适行距”.
- Too busy: force “背景低对比、仅右侧画面、左侧纯净面板”.
- Deck too dark: switch to `editorial-light` or `airy-relaxed`, disable vignette, force daylight scene IDs, and add brightness override.
- Ratio mismatch: regenerate that slide with stricter 16:9 constraint in prompt; do not crop or otherwise post-process.
  - Ensure both prompt text and tool-call config specify 16:9 in the same retry.

## Operating mode (be patient; avoid “probe images”)

- Image generation can be **slow**. Prefer generating the real slides directly.
- Avoid generating test/probe images (e.g. blank backgrounds) unless the user explicitly asks for diagnostics.
- If an image call fails intermittently, retry the same slide prompt after a brief pause; do not change multiple variables at once.
- Default delivery mode is **raw outputs**: keep generated images as-is and assemble the PPT directly from them.

## Tooling constraints (important)

Some image tools only allow writing output images to specific directories (often `~/Downloads` or a workspace path). When blocked:
1. Generate images into an allowed directory (e.g. `~/Downloads/<deck_id>/`).
2. Copy images into the project/workspace output folder.

## Bundled scripts

### `scripts/compose_style_pack_blocks.py`
- Compose inherited style-pack blocks into one paste-ready bundle.
- Use before prompt writing to prevent style mismatch.

Run:
```bash
python3 scripts/compose_style_pack_blocks.py --pack-id editorial-light
```

### `scripts/create_style_pack.py`
- Scaffold a new style pack folder with manifest + block templates.
- Use when existing packs are not enough and you need fast extension.

Run:
```bash
python3 scripts/create_style_pack.py --pack-id warm-minimal --display-name "Warm Minimal" --keywords "温暖,平衡" --scene-tags "warm,clean"
```

### `scripts/build_images_only_pptx.py`
- Assemble an images-only PPTX by concatenating `slide*.png` full-screen in filename order.
- Use when the user wants “PPT = concatenated images”, with no PPT text boxes.

Dependencies (install if missing):
```bash
python3 -m pip install python-pptx
```

Run:
```bash
python3 scripts/build_images_only_pptx.py --images-dir /path/to/slides --out /path/to/deck.pptx
```

## References
- Read `references/prompt_template.md` when you need a high-detail prompt skeleton that produces the “rich background infographic” style reliably.
- Read `references/style-pack-system.md` for composition rules and how to add new style packs.
- Read `references/style-pack-catalog.md` for intent-to-style routing and pack selection.
- Read `references/style-packs/` for self-contained style definitions.
- Read `references/style_profile_library.md` for legacy style aliases (backward compatibility).
- Read `references/deep_research_handoff_mapping.md` to normalize upstream `slide_extraction.md` fields from `deep-research-article`.
- Read `references/scene-catalog.md` for reusable scene IDs and tags.
- Read `references/scene-preset-library.md` for ready-to-paste scene visual blocks.
- Read `references/scene-entry-template.md` when adding new scene IDs to the catalog.
- Read `references/scene_library.md` to quickly add “场景化/电影感” elements (locations + props) without making the slide messy.
- Read `references/layout_library.md` to choose a layout that matches your text density (so slides stay readable).
- Read `references/shot_mood_library.md` for cinematic shot + lighting + time-of-day presets.
- Read `references/motif_pack.md` to make the whole deck feel like a single cohesive series.
- Read `references/deck_consistency_block.md` to lock margins/light direction/texture/icon style across the whole deck.
- Read `references/typography_spacing_lock.md` to prevent tiny text and keep spacing consistent.
- Read `references/text_fidelity_block.md` to reduce Chinese typos and forbid any extra words.
- Read `references/negative_prompt_block.md` to avoid common generator artifacts (watermarks/English/UI).
- Read `references/storyboard_library.md` to give the whole deck a narrative arc.
- Read `references/chinese_quote_compression.md` to split long quotes without paraphrasing (keeps fonts large).
