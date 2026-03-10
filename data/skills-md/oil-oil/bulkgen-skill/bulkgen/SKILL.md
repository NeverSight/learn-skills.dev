---
name: bulkgen
description: >-
  Bulk AI image generation via the BulkGen API. Use whenever users ask to generate
  one or many AI images — even simple requests like "generate an image", "edit this image",
  "make variations", or "create AI art" should trigger this skill. Handles single images,
  grids, variations, reference-image editing, expiring result downloads, and HTML
  preview handoff pages. Works for English and Chinese requests like "生成图片", "批量生成",
  "图生图", "做一个 3x3 宫格", or "给我做九宫格变体".
---

# BulkGen Agent Skill

Generate AI images with BulkGen. Scripts are bundled at `~/.claude/skills/bulkgen/scripts/` — always use this full path.

**Language**: Always respond in the user's language. This skill is written in English for consistency, but all replies to the user should match their language.

---

## API Key

No environment variable setup needed. When the user asks to generate images:

1. Check if `BULKGEN_API_KEY` is already set in the environment.
2. If **not set**, ask the user in their language to share their key (format: `sk_live_...`). They can get one at bulk-gen.com → user menu → API Keys.
3. Once received, pass it inline — do not `export` it or persist it anywhere:

```bash
BULKGEN_API_KEY="sk_live_..." node $SCRIPTS/generate.js ...
```

If the user gets a 401 error, ask them to check their key or get a new one at bulk-gen.com.

---

## Workflow

1. **Clarify** → If parameters are ambiguous, ask ratio + mode before generating
2. **Generate** → Run `generate.js` with the user's key inline
3. **Preview** → Always run `build_preview.js` and `open` the HTML immediately after

---

## Before generating: clarify parameters

When the user asks for multiple images without specifying ratio or mode, ask before generating.

**Ask when**: User requests N images without specifying ratio or mode.

**Skip asking when**: Single image (solo mode), or all parameters already specified.

**When asking**, explain the two choices in the user's language:
- **Ratio**: square (1:1), portrait (9:16), landscape (16:9) — default square
- **Mode**: variation (one prompt, multiple styles) vs batch (different prompt per cell) — default variation

If the user says they don't mind or leaves it to you, use defaults (1:1 + variation) and confirm briefly.

---

## Quick start

```bash
SCRIPTS=~/.claude/skills/bulkgen/scripts
KEY="sk_live_..."   # key provided by the user

# Single image
BULKGEN_API_KEY=$KEY node $SCRIPTS/generate.js --prompts "a sunset" --mode solo

# 3x3 variations (same prompt, different styles)
BULKGEN_API_KEY=$KEY node $SCRIPTS/generate.js --prompts "cyberpunk city" --mode variation --cols 3 --rows 3 --canvas-ratio 1:1

# 2x2 batch (different prompts per cell)
BULKGEN_API_KEY=$KEY node $SCRIPTS/generate.js --prompts "cat" "dog" "bird" "fish" --cols 2 --rows 2

# Edit with reference image
BULKGEN_API_KEY=$KEY node $SCRIPTS/generate.js --prompts "watercolor style" --input ./photo.jpg

# Build preview and open (always do this after generating)
node $SCRIPTS/build_preview.js ./bulkgen-result.json ./bulkgen-preview.html && open ./bulkgen-preview.html
```

---

## Options

| Option | Values | Default |
|--------|--------|---------|
| `--mode` | solo, batch, variation | variation |
| `--cols`, `--rows` | Grid dimensions | auto |
| `--canvas-ratio` | 1:1, 16:9, 9:16, 4:5, 3:4, 3:2, 2:3, 4:3, 5:4, 21:9 | 1:1 |
| `--resolution` | 1K, 2K, 4K | 1K |
| `--input` | Reference image path | none |

---

## Modes

| Mode | Use when |
|------|----------|
| `solo` | Single image |
| `variation` | One prompt → multiple creative variants (same subject, different styles) |
| `batch` | Different prompts → each cell gets its own independent scene |

---

## Layouts

Valid: `1x1, 2x1, 1x2, 3x1, 1x3, 2x2, 3x2, 2x3, 4x2, 2x4, 3x3, 4x3, 3x4, 4x4`

`--canvas-ratio` is the aspect ratio of the **full grid**, not a single cell. Some layout/ratio combinations are unsupported — the script will error and suggest alternatives.

---

## Reference images

Use `--input` for style transfer or editing. Up to 14 images, 7 MB each. Formats: PNG, JPG, WebP, HEIC, HEIF.

---

## Post-generation

Image URLs expire in 12 hours — always build the preview immediately.

```bash
SCRIPTS=~/.claude/skills/bulkgen/scripts

# Build HTML preview (always run this)
node $SCRIPTS/build_preview.js ./bulkgen-result.json ./bulkgen-preview.html && open ./bulkgen-preview.html

# Download permanent local copies (only if user explicitly asks)
node $SCRIPTS/download_images.js ./bulkgen-result.json ./downloads
```

---

## Errors

| Status | Action |
|--------|--------|
| 401 | Invalid key — ask user to check or get a new one at bulk-gen.com |
| 402 | Insufficient credits — ask user to top up at bulk-gen.com |
| 400 | Invalid params — check layout/ratio compatibility |
| 500 | Server error — retry once |
