---
name: gemini-image-generator
description: Generate, edit, or transform images with Gemini Nano Banana using bundled Python scripts (Flash or Pro) including aspect ratio, resolution, image-to-image edits, logo overlays, and reference images. Use when users request image generation, image edits, image-to-image transformations, logo placement, or specific aspect ratios or resolutions.
---

# Gemini Image Generator

Use this skill to turn a user prompt (and optional images) into Gemini image generation calls via the bundled Python scripts.

## Workflow

1. Collect the user prompt and any images (local paths or URLs).
2. Infer the operation mode and translate parameters into CLI flags.
3. Run the appropriate script to generate or edit images.
4. Return the output file paths.

## Defaults and Rules

- Default model: `gemini-2.5-flash-image` (CLI value `flash`).
- Default aspect ratio: `9:16`.
- Default count: `1` (max `3`).
- Default image size: `1K`, but only apply it for the Pro model.
- If the user specifies a size (`1K|2K|4K`), switch to Pro (`gemini-3-pro-image-preview`).
- If the user explicitly asks for Pro or higher quality, use Pro.
- If the user supplies multiple reference images (2+), switch to Pro.
- Logo overlay always uses Pro (even if the user asks for Flash).
- Only set `--size` when using Pro.

## Allowed Values

- Aspect ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`.
- Image sizes (Pro only): `1K`, `2K`, `4K`.
- Reference images (Pro): up to 14 total. Gemini guidance: up to 6 object images + up to 5 human images.

## Script

## Scripts

### Text-to-image

Run:

```bash
python scripts/generate_image.py \
  --prompt "<user prompt>" \
  --aspect 9:16 \
  --count 1 \
  --model flash \
  --out-dir outputs
```

Only add flags when the user asks for them. The script reads `GEMINI_API_KEY` from the environment.

### Image editing / image-to-image

Use when the user supplies a base image to edit or transform.

Run:

```bash
python scripts/edit_image.py \
  --input /path/to/base.png \
  --prompt "<edit instructions>" \
  --reference /path/to/ref1.png \
  --reference https://example.com/ref2.png \
  --aspect 9:16 \
  --count 1 \
  --model flash \
  --out-dir outputs
```

### Logo overlay

Use when the user wants to place a logo onto a base image.

Run:

```bash
python scripts/logo_overlay.py \
  --base /path/to/base.png \
  --logo /path/to/logo.png \
  --aspect 9:16 \
  --count 1 \
  --model pro \
  --out-dir outputs
```

## Examples

User: "Generate a portrait of a dancer in a foggy forest."
Claude:
- Use defaults (flash, 9:16, count 1).
- Run:
  `python scripts/generate_image.py --prompt "Generate a portrait of a dancer in a foggy forest."`

User: "Make a 2K 16:9 cinematic still of a neon city, give me 3 options."
Claude:
- Use Pro with size 2K, aspect 16:9, count 3.
- Run:
  `python scripts/generate_image.py --prompt "Make a 2K 16:9 cinematic still of a neon city" --aspect 16:9 --size 2K --count 3 --model pro`

User: "Edit this image to remove the background and make it studio white." (with one image)
Claude:
- Use edit script with Flash.
- Run:
  `python scripts/edit_image.py --input /path/to/image.png --prompt "Remove the background and make it studio white."`

User: "Put this logo on the shirt in the photo." (with base + logo images)
Claude:
- Use logo overlay script (Pro).
- Run:
  `python scripts/logo_overlay.py --base /path/to/photo.png --logo /path/to/logo.png`

## Notes

- If the script fails with a missing module, install `google-genai` and retry.
- Dependencies live in `scripts/requirements.txt` (install with `pip install -r scripts/requirements.txt`).
- Output files are written into the `outputs/` directory using timestamped names.
- For prompt best practices and templates, read `references/prompt-guide.md`.
- For logo-specific guidance, read `references/logo-overlay.md`.
- For edit/image-to-image guidance, read `references/image-editing.md`.
- For watermarking guidance, read `references/watermarking.md`.
