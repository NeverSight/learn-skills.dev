---
name: image-upscale
description: Upscales an image using AI super-resolution to increase resolution with detail generation. Use when you need to enlarge images, improve low-resolution photos, or prepare images for large-format display.
---

# Image Upscale

Upscales an image using AI super-resolution models, increasing resolution while generating realistic detail.

## Command

```bash
agent-media image upscale --in <path> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input file path or URL |
| `--scale` | No | Scale factor (2 or 4, default: 2) |
| `--out` | No | Output path, filename or directory (default: ./) |
| `--provider` | No | Provider to use (local, fal, replicate) |
| `--model` | No | Model to use (overrides provider default) |

## Output

Returns a JSON object with the upscaled image path:

```json
{
  "ok": true,
  "media_type": "image",
  "action": "upscale",
  "provider": "local",
  "output_path": "upscaled_123_abc.png",
  "mime": "image/png",
  "bytes": 456789
}
```

## Examples

Upscale an image (default 2x):
```bash
agent-media image upscale --in photo.jpg
```

Upscale 4x with specific provider:
```bash
agent-media image upscale --in photo.jpg --scale 4 --provider fal
```

Upscale with custom output:
```bash
agent-media image upscale --in photo.jpg --out ./upscaled
```

## Providers

### local

Runs locally on CPU using [Transformers.js](https://huggingface.co/docs/transformers.js), no API key required.

- Uses `Xenova/swin2SR-compressed-sr-x4-48` model (~1.3MB)
- Always outputs 4x upscale regardless of `--scale` (model architecture limitation)
- Models downloaded on first use
- You may see a `mutex lock failed` error — ignore it, the output is correct if `"ok": true`

```bash
agent-media image upscale --in photo.jpg --provider local
```

### fal

- Requires `FAL_API_KEY`
- Uses `fal-ai/esrgan` (Real-ESRGAN) model
- Supports 2x and 4x scale

### replicate

- Requires `REPLICATE_API_TOKEN`
- Uses `nightmareai/real-esrgan` model
- Supports 2-10x scale
