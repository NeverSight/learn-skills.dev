---
name: create-sticker
description: Generate LINE-style stickers of a character with background removal. Creates creative, unique poses with consistent character design via Google Gemini, removes solid background to transparent PNG. Use when user asks for sticker, 贴纸, LINE sticker.
---

# Create Sticker Skill

## Overview

Generate LINE-style character stickers. Each sticker has a creative, unique pose with consistent character appearance. Generates on light gray background, then auto-removes background to produce transparent PNG ready for messaging platforms.

## Workflow

1. **Generate** — Call Google Gemini with character reference + sticker prompt
2. **Save raw** — Save image with gray background
3. **Remove background** — Flood fill gray to transparent (preserves white border + clothing)
4. **Center & fill** — Center content and scale up until edges touch canvas boundary
5. **Send** — Send to user for review

## API Configuration

- **SDK:** `google-genai` (Google Gemini native SDK)
- **Model:** `gemini-3-pro-image-preview` (default, configurable via `--model`)
- **Authentication:** `GEMINI_API_KEY` environment variable
- **Reference Image:** `assets/example-character.jpeg`

### Environment Setup

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key at: https://aistudio.google.com/apikey

## Usage

```bash
python3 scripts/create_sticker.py "pose and expression description"
python3 scripts/create_sticker.py --ideas
python3 scripts/create_sticker.py "pose" --no-remove-bg
python3 scripts/create_sticker.py "pose" --model gemini-3.1-flash-image-preview
python3 scripts/create_sticker.py "pose" --aspect 1:1 --size 2K
```

## File Storage & Naming

### Working Files
- **Raw (gray bg):** `$STICKER_OUTPUT_DIR/raw/{name}.png` (default: `~/stickers/raw/`)
- **Final (transparent):** `$STICKER_OUTPUT_DIR/{name}.png` (default: `~/stickers/`)
- **Naming:** lowercase English, underscores, max 60 chars

### Gallery (approved)
- **Location:** `~/Pictures/lynn-stickers/`

### Telegram Sticker Pack
- **Pack dir:** `~/Pictures/lynn-stickers/lynn_stickers_by_lynn_ai_bot/`
- **Push:** `cd ~/Pictures/lynn-stickers/lynn_stickers_by_lynn_ai_bot && tsticker push`

## Character Setup

> ⚠️ **以下角色设定为示例。** 这是一个示例，需要向用户获取真实角色设定提示词后填入此 SKILL.md 以持久化。实际使用时请替换为你自己的角色设定。

### Example Character Base Prompt

```
Chibi sticker of the character in the reference image.
Keep the shading and rendering style of the reference (NOT flat coloring), but in chibi proportions (large head, small body, 2.5 head ratio).
MUST include the character's dark beret (exactly as shown in reference image) AND round thin gold-framed glasses. These two accessories are essential.
Upper body framing. Thin delicate outlines.
Solid flat light gray background RGB(240,240,240). No extra decorations, no border.
```

### Example Reference Image

> ⚠️ `assets/example-character.jpeg` 是示例资产。请替换为你自己的角色参考图。

## Prompt DOs and DON'Ts

### ✅ DO
- Keep action prompts **short and focused** on pose + expression + energy
- Describe **specific facial expressions** (half-lidded eyes, puffed cheeks, squinting)
- Use **dynamic verbs** (tilting, peeking, squeezing, leaning)
- Let the reference image drive character appearance — don't over-describe features
- Mention key accessories explicitly if the model tends to forget them

### ❌ DON'T
- Don't write long paragraphs describing every color and accessory — model has the reference image
- Don't use flat/cel-shaded style — keep the OC's shading and rendering quality
- Don't request full body — upper body framing only
- Don't use thick/bold outline style — thin delicate lines only

## Background Removal

- Flood fill from edges — only removes gray, preserves white (model's outline + clothing)
- Does NOT use AI-based removal (rembg over-removes white areas)
- After removal: add white outline, center content and scale up to fill canvas edge-to-edge

## Post-Processing Pipeline

```
Raw image (gray bg)
  → Flood fill gray to transparent
  → Add 12px white outline
  → Find content bounding box
  → Center & scale up to fill canvas (4px margin)
  → Save final PNG
```
