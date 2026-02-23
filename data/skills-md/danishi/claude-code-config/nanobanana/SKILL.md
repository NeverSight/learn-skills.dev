---
name: nanobanana
description: >
  Generate and edit images using Google Gemini 3 Pro Image (Nano Banana Pro).
  Supports text-to-image generation, image editing with reference images,
  configurable aspect ratios, 1K/2K/4K output, Google Search grounding,
  and batch generation. Works with both Gemini Developer API and Vertex AI.
---

# Nano Banana - AI Image Generation Skill

Use the Python scripts in `scripts/` to generate and edit images via
Google's **Nano Banana Pro** model (`gemini-3-pro-image-preview`).

## Prerequisites

### 1. Install dependencies

```bash
pip install google-genai Pillow
```

### 2. Configure API credentials (one of the following)

#### Option A: Gemini Developer API (recommended for personal use)

Set the `GEMINI_API_KEY` environment variable.
Get a key at https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY="your-api-key"
```

#### Option B: Vertex AI API (for Google Cloud users)

Set `GOOGLE_CLOUD_PROJECT` and optionally `GOOGLE_CLOUD_LOCATION`.
Requires a GCP project with the Vertex AI API enabled and
Application Default Credentials configured (`gcloud auth application-default login`).

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"   # optional, defaults to us-central1
```

> **Priority:** If both `GOOGLE_CLOUD_PROJECT` and `GEMINI_API_KEY` are set,
> Vertex AI is used.

### 3. Optional environment variables

| Variable | Default | Description |
|---|---|---|
| `NANOBANANA_MODEL` | `gemini-3-pro-image-preview` | Override the model name |
| `IMAGE_OUTPUT_DIR` | `./nanobanana-images` | Default output directory |
| `NANOBANANA_NO_SSL_VERIFY` | _(unset)_ | Set to `1` / `true` / `yes` to disable SSL certificate verification |

---

## Scripts

### `scripts/generate.py` - Single image generation / editing

#### Text-to-image

```bash
python scripts/generate.py "a cute robot mascot, pixel art style" -o robot.png
```

#### Image editing (with reference image)

```bash
python scripts/generate.py "make the sky purple and add stars" -i photo.jpg -o edited.png
```

#### Multiple reference images (up to 14)

```bash
python scripts/generate.py "group photo of these people at a party" \
  -i person1.png -i person2.png -i person3.png -o group.png
```

#### With aspect ratio and resolution

```bash
python scripts/generate.py "cinematic landscape, dramatic lighting" \
  --ratio 21:9 --size 4K -o landscape.png
```

#### With Google Search grounding (for real-world accuracy)

```bash
python scripts/generate.py "photo of the Eiffel Tower at sunset" \
  --search -o eiffel.png
```

#### Disable SSL verification (for corporate proxies or self-signed certs)

```bash
python scripts/generate.py "abstract art" --no-ssl-verify -o art.png
```

#### JSON output (for programmatic use)

```bash
python scripts/generate.py "abstract art" --json -o art.png
```

#### Full options

```
usage: generate.py [-h] [-o OUTPUT] [-i INPUTS] [-r RATIO] [-s SIZE]
                   [--search] [-v] [--json] [--no-ssl-verify] prompt

Arguments:
  prompt              Text prompt for image generation

Options:
  -o, --output PATH   Output file path (auto-generated if omitted)
  -i, --input PATH    Input image for editing (repeatable, up to 14)
  -r, --ratio RATIO   Aspect ratio: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  -s, --size SIZE     Resolution: 1K, 2K, 4K
  --search            Enable Google Search grounding
  -v, --verbose       Show detailed output
  --json              Output result as JSON
  --no-ssl-verify     Disable SSL certificate verification
```

---

### `scripts/batch_generate.py` - Batch image generation

Generate multiple image variations from a single prompt.

#### Basic batch

```bash
python scripts/batch_generate.py "pixel art logo" -n 20 -d ./logos -p logo
```

#### High-res batch with aspect ratio

```bash
python scripts/batch_generate.py "product photo, white background" \
  -n 10 --ratio 1:1 --size 4K -d ./products
```

#### Parallel execution (faster)

```bash
python scripts/batch_generate.py "icon set" -n 20 --parallel 5 -d ./icons
```

#### Full options

```
usage: batch_generate.py [-h] [-n COUNT] [-d DIR] [-p PREFIX] [-r RATIO]
                         [-s SIZE] [--search] [--delay DELAY]
                         [--parallel N] [-q] [--json] [--no-ssl-verify] prompt

Arguments:
  prompt              Text prompt for image generation

Options:
  -n, --count N       Number of images (default: 10)
  -d, --dir DIR       Output directory (default: ./nanobanana-images)
  -p, --prefix STR    Filename prefix (default: image)
  -r, --ratio RATIO   Aspect ratio
  -s, --size SIZE     Resolution: 1K, 2K, 4K
  --search            Enable Google Search grounding
  --delay SECS        Delay between sequential requests (default: 3)
  --parallel N        Concurrent requests (default: 1, max recommended: 5)
  -q, --quiet         Suppress progress output
  --json              Output results as JSON
  --no-ssl-verify     Disable SSL certificate verification
```

---

## Aspect Ratio Guide

| Ratio | Typical use |
|---|---|
| `1:1` | Icons, avatars, social media posts |
| `4:3` | Presentations, traditional photos |
| `3:2` | Standard landscape photos |
| `2:3` | Portrait photos |
| `16:9` | Banners, YouTube thumbnails, widescreen |
| `9:16` | Phone wallpapers, Instagram stories |
| `21:9` | Cinematic ultra-wide |
| `4:5` | Instagram portrait posts |
| `5:4` | Group photos |
| `3:4` | Book covers, portrait art |

## Resolution Guide

| Size | Description |
|---|---|
| `1K` | Standard resolution |
| `2K` | High resolution |
| `4K` | Ultra high resolution (best for print and large displays) |

---

## Prompting Tips

Good prompts include:

1. **Subject** - What to generate ("a robot", "sunset over mountains")
2. **Style** - Art style ("pixel art", "watercolor", "photorealistic")
3. **Details** - Specific qualities ("warm lighting", "minimalist", "vibrant colors")

**Examples of effective prompts:**

- `"Professional product photo of wireless headphones on marble, soft studio lighting, 85mm lens"`
- `"Pixel art robot mascot, 8-bit style, blue and orange, transparent background"`
- `"Minimalist logo, geometric mountain shape, blue gradient, flat design, clean edges"`

See `references/prompts.md` for a comprehensive prompt reference with category-specific templates.

---

## Error Handling

| Error | Solution |
|---|---|
| `google-genai package not installed` | Run `pip install google-genai Pillow` |
| `No API credentials found` | Set `GEMINI_API_KEY` or `GOOGLE_CLOUD_PROJECT` |
| `Content blocked by safety filters` | Rephrase the prompt to avoid restricted content |
| `API rate limit reached` | Wait and retry; use `--delay` for batch operations |
| `Image file not found` | Verify the `-i` input path is correct |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Use `--no-ssl-verify` or set `NANOBANANA_NO_SSL_VERIFY=1` |
