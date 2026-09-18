---
name: gpt-image
description: "Generate and edit images with OpenAI GPT-Image-2 via inference.sh CLI. Models: GPT-Image-2. Capabilities: text-to-image, image editing, inpainting, mask-based editing, multi-image reference, batch generation. Use for: product mockups, marketing visuals, image editing, concept art, inpainting, photo manipulation. Triggers: gpt image, gpt-image-2, openai image, chatgpt image, dall-e, dalle, openai image generation, gpt image edit, gpt inpainting, openai dall-e, gpt 4o image"
allowed-tools: Bash(belt *)
---

> **Install the belt CLI skill:** `npx skills add belt-sh/cli`

# GPT-Image-2

Generate and edit images with OpenAI's GPT-Image-2 via [inference.sh](https://inference.sh) CLI.

## Quick Start

> Requires inference.sh CLI (`belt`). [Install instructions](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

```bash
belt login

belt app run openai/gpt-image-2 --input '{"prompt": "a cat astronaut floating in space"}'
```


## Capabilities

GPT-Image-2 supports text-to-image generation, image editing with reference images, and mask-based inpainting — all through a single model.

| Feature | Description |
|---------|-------------|
| Text-to-Image | Generate images from text prompts |
| Image Editing | Edit images using reference images |
| Inpainting | Mask-based editing of specific regions |
| Batch Generation | Generate up to 10 images at once |
| Multiple Formats | PNG, JPEG, WebP output |
| Flexible Resolution | Any size in 32px increments (256–4096) |

## Examples

### Text-to-Image

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "professional product photo of sneakers on a white background, studio lighting",
  "quality": "high"
}'
```

### Multiple Images

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "minimalist logo design for a coffee shop",
  "n": 4,
  "quality": "medium"
}'
```

### Image Editing with Reference

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "change the background to a beach at sunset",
  "images": ["https://your-image.jpg"]
}'
```

### Multi-Image Reference

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "combine these two characters into one scene",
  "images": ["https://character1.jpg", "https://character2.jpg"]
}'
```

### Inpainting with Mask

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "replace with a red sports car",
  "images": ["https://street-scene.jpg"],
  "mask": "https://car-mask.png"
}'
```

### Custom Resolution

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "wide cinematic landscape, mountains at golden hour",
  "width": 1920,
  "height": 1080,
  "quality": "high"
}'
```

### Fast Drafts

```bash
belt app run openai/gpt-image-2 --input '{
  "prompt": "quick concept sketch of a robot",
  "quality": "low"
}'
```

## Pricing

| Quality | ~Price per Image |
|---------|-----------------|
| Low | $0.006 |
| Medium | $0.024 |
| High | $0.21 |

Larger resolutions cost more. See `belt app get openai/gpt-image-2` for full pricing details.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | required | Text prompt describing the image |
| `images` | array | - | Reference image(s) for editing |
| `mask` | string | - | Mask image for inpainting |
| `n` | integer | 1 | Number of images (1–10) |
| `quality` | string | - | low, medium, or high |
| `width` | integer | - | Output width (256–4096, multiples of 32) |
| `height` | integer | - | Output height (256–4096, multiples of 32) |
| `output_format` | string | png | png, jpeg, or webp |
| `output_compression` | integer | - | Compression level for jpeg/webp (0–100) |

## Related Skills

```bash
# Full platform skill (all apps)
npx skills add inference-sh/skills@infsh-cli

# All image generation models
npx skills add inference-sh/skills@ai-image-generation

# FLUX models
npx skills add inference-sh/skills@flux-image

# Pruna P-Image (fast & economical)
npx skills add inference-sh/skills@p-image
```

Browse all image apps: `belt app list --category image`

## Documentation

- [Running Apps](https://inference.sh/docs/apps/running) - How to run apps via CLI
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) - Real-time progress updates
