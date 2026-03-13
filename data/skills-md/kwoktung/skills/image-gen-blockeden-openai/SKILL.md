---
name: image-gen-blockeden-openai
description: Generates AI images using the BlockEden OpenAI proxy (DALL-E 3 / DALL-E 2 / gpt-image-1). Use this skill whenever the user wants to generate, create, draw, make, or produce an image, picture, photo, illustration, artwork, or visual — even if they don't say "DALL-E" or "BlockEden". Trigger on phrases like "generate an image of", "create a picture of", "make me an illustration", "draw a scene", "visualize this", "I want an image", or "generate based on this image/URL". Requires the BLOCKEDEN_ACCESS_KEY environment variable to be set.
argument-hint: [describe the image you want, optionally with a reference image URL, e.g. "a sunset over mountains in watercolor style" or "same style as https://example.com/ref.jpg but with a dragon"]
---

# Generate an Image via BlockEden OpenAI Proxy

You are helping the user generate an AI image using the BlockEden OpenAI proxy, which is fully compatible with the OpenAI Images API (DALL-E 3 / DALL-E 2 / gpt-image-1).

## Prerequisites

The `BLOCKEDEN_ACCESS_KEY` environment variable must be set. If it's missing, tell the user:
> Please set the `BLOCKEDEN_ACCESS_KEY` environment variable before using this skill.

## How to generate an image

Use the bundled script at `scripts/generate_image.py` (relative to this SKILL.md):

```bash
python <skill_dir>/scripts/generate_image.py "<prompt>" [options]
```

### Options

| Flag | Default | Choices | Notes |
|------|---------|---------|-------|
| `--reference-image` | `None` | any URI | Reference image URL to base generation on. Uses `gpt-image-1` via `/v1/responses`. |
| `--size` | `1024x1024` | `1024x1024`, `1792x1024`, `1024x1792` | Landscape: `1792x1024`, Portrait: `1024x1792` |
| `--quality` | `standard` | `standard`, `hd` | `hd` gives finer detail, costs more (text-only mode only) |
| `--model` | `dall-e-3` | `dall-e-3`, `dall-e-2` | Model for text-only generation. Ignored when `--reference-image` is set. |
| `--style` | `vivid` | `vivid`, `natural` | DALL-E 3 only. `vivid` = dramatic, `natural` = realistic |
| `--output-dir` | `.` | any path | Directory where the PNG will be saved |

### Example: text-only generation

```bash
python /path/to/skill/scripts/generate_image.py \
  "a cozy coffee shop on a rainy day, impressionist painting style" \
  --size 1792x1024 \
  --quality hd \
  --style natural \
  --output-dir ~/Desktop
```

### Example: reference image generation

```bash
python /path/to/skill/scripts/generate_image.py \
  "same composition but set at night with neon lights" \
  --reference-image "https://example.com/my-photo.jpg" \
  --output-dir ~/Desktop
```

## After generation

### Text-only mode output
```json
{
  "filepath": "/path/to/image_1234567890.png",
  "revised_prompt": "...",
  "model": "dall-e-3",
  "size": "1024x1024",
  "quality": "standard",
  "style": "vivid"
}
```

### Reference image mode output
```json
{
  "filepath": "/path/to/image_1234567890.png",
  "model": "gpt-image-1",
  "reference_image": "https://example.com/my-photo.jpg",
  "prompt": "same composition but set at night with neon lights"
}
```

Once the image is saved:
1. Tell the user the file path so they can open it.
2. Show the `revised_prompt` if DALL-E rewrote it — this helps the user refine future prompts.
3. Offer to regenerate with different parameters if the user wants to iterate.

## Interpreting the user's request

- Extract the core visual description from what the user says and use it as the prompt.
- If the user provides a reference image URL/URI, pass it via `--reference-image`. The model switches automatically to `gpt-image-1`.
- If the user specifies an aspect ratio (wide, tall, square), map it to the appropriate `--size`.
- If the user says "high quality", "detailed", or "HD", add `--quality hd` (text-only mode only).
- If the user says "realistic" or "photorealistic", use `--style natural`.
- If the user says "artistic", "dramatic", or "vivid", use `--style vivid` (the default).
- If the user provides an output location, pass it via `--output-dir`.
- If no output location is given, save to the current working directory.

## Prompt crafting tips

Good image prompts are specific and visual. If the user's request is vague, enhance it slightly:
- Add a medium/style if none given (e.g., "digital art", "watercolor", "photorealistic")
- Add lighting or atmosphere if it feels generic (e.g., "golden hour lighting", "moody atmosphere")
- Don't over-engineer — keep the user's intent central
