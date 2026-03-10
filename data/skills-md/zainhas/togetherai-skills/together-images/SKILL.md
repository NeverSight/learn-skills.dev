---
name: together-images
description: Generate and edit images via Together AI's image generation API. Models include FLUX.1 (schnell/dev/pro), FLUX.2, Kontext (image editing with reference images), Seedream, Stable Diffusion, and more. Use when users want to generate images from text, edit existing images, create AI art, use LoRA adapters for custom styles, or work with any image generation task.
---

# Together Image Generation

## Overview

Generate images from text prompts and edit existing images via the Together AI API.

- Endpoint: `/v1/images/generations`
- Response: URL or base64-encoded image
- Models: FLUX.1 family, Kontext, Seedream, Stable Diffusion, and more

## Installation

```shell
# Python (recommended)
uv init  # optional, if starting a new project
uv add together
```

```shell
# or with pip
pip install together
```

```shell
# TypeScript / JavaScript
npm install together-ai
```

Set your API key:

```shell
export TOGETHER_API_KEY=<your-api-key>
```

## Quick Start

### Text-to-Image

```python
from together import Together
client = Together()

response = client.images.generate(
    prompt="A serene mountain landscape at sunset with a lake reflection",
    model="black-forest-labs/FLUX.1-schnell",
    steps=4,
)
print(f"Image URL: {response.data[0].url}")
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.images.generate({
  prompt: "A serene mountain landscape at sunset with a lake reflection",
  model: "black-forest-labs/FLUX.1-schnell",
  steps: 4,
});
console.log(response.data[0].url);
```

```shell
curl -X POST "https://api.together.xyz/v1/images/generations" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"black-forest-labs/FLUX.1-schnell","prompt":"A serene mountain landscape","steps":4}'
```

### Image Editing (Kontext)

Transform existing images using a reference:

```python
response = client.images.generate(
    model="black-forest-labs/FLUX.1-kontext-pro",
    prompt="Transform this into a watercolor painting",
    image_url="https://cdn.pixabay.com/photo/2020/05/20/08/27/cat-5195431_1280.jpg",
    width=1024,
    height=768,
)
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.images.generate({
  model: "black-forest-labs/FLUX.1-kontext-pro",
  width: 1024,
  height: 768,
  prompt: "Transform this into a watercolor painting",
  image_url: "https://cdn.pixabay.com/photo/2020/05/20/08/27/cat-5195431_1280.jpg",
});
```

```shell
curl -X POST "https://api.together.xyz/v1/images/generations" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "black-forest-labs/FLUX.1-kontext-pro",
    "width": 1024,
    "height": 768,
    "prompt": "Transform this into a watercolor painting",
    "image_url": "https://cdn.pixabay.com/photo/2020/05/20/08/27/cat-5195431_1280.jpg"
  }'
```

### Multiple Variations

```python
response = client.images.generate(
    prompt="A cute robot assistant",
    model="black-forest-labs/FLUX.1-schnell",
    n=4,
    steps=4,
)
for i, img in enumerate(response.data):
    print(f"Variation {i+1}: {img.url}")
```

### Base64 Response

```python
response = client.images.generate(
    model="black-forest-labs/FLUX.1-schnell",
    prompt="a cat in outer space",
    response_format="base64",
)
print(response.data[0].b64_json)
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.images.generate({
  model: "black-forest-labs/FLUX.1-schnell",
  prompt: "a cat in outer space",
  response_format: "base64",
});
console.log(response.data[0].b64_json);
```

```shell
curl -X POST "https://api.together.xyz/v1/images/generations" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "black-forest-labs/FLUX.1-schnell",
    "prompt": "a cat in outer space",
    "response_format": "base64"
  }'
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `prompt` | string | Text description (required) | - |
| `model` | string | Model ID (required) | - |
| `width` | int | Width in pixels | 1024 |
| `height` | int | Height in pixels | 1024 |
| `n` | int | Number of images (1-4) | 1 |
| `steps` | int | Diffusion steps (more = better quality) | varies |
| `seed` | int | Random seed for reproducibility | random |
| `negative_prompt` | string | What to exclude | - |
| `response_format` | string | "url" or "base64" | "url" |
| `image_url` | string | Reference image (Kontext) | - |
| `aspect_ratio` | string | For Schnell/Kontext models | - |
| `disable_safety_checker` | bool | Disable NSFW filter | false |

Notes:
- Schnell and Kontext models use `aspect_ratio`; FLUX.1 Pro/Dev use `width`/`height`
- Dimensions should be multiples of 8

## Common Dimensions

| Use Case | Width | Height |
|----------|-------|--------|
| Square (social media) | 1024 | 1024 |
| Landscape (banners) | 1344 | 768 |
| Portrait (mobile) | 768 | 1344 |

## Steps Guide

- **1-4 steps**: Fast preview (Schnell)
- **6-12 steps**: Good quality
- **20-30 steps**: High quality
- **30-50 steps**: Maximum quality (diminishing returns)

## Resources

- **Supported models**: See [references/models.md](references/models.md)
- **API parameter details**: See [references/api-reference.md](references/api-reference.md)
- **Runnable script**: See [scripts/generate_image.py](scripts/generate_image.py) — generate, save, and edit images with FLUX models (v2 SDK)
- **Runnable script (TypeScript)**: See [scripts/generate_image.ts](scripts/generate_image.ts) — minimal OpenAPI `x-codeSamples` extraction for image generation (TypeScript SDK)
- **Official docs**: [Images Overview](https://docs.together.ai/docs/images-overview)
- **Official docs**: [FLUX Quickstart](https://docs.together.ai/docs/quickstart-flux)
- **API reference**: [Image Generation API](https://docs.together.ai/reference/post-images-generations)
