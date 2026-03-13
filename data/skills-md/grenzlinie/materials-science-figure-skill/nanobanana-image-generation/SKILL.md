---
name: nanobanana-image-generation
description: Use when the user wants to generate or edit images with Google's Nanobanana/Gemini image models using the official Gemini API shape. Prefer this skill for text-to-image, image-to-image editing, multi-image reference workflows, attachment-based recreations, or when the user wants publication-style figures such as materials-science paper schematics. Use it when the user asks for a materials-science figure, journal-style scientific illustration, graphical abstract, mechanism diagram, or paper-ready materials figure.
---

# Nanobanana Image Generation

## Overview

Use this skill for Gemini image generation and image editing through the official `generateContent` flow. Follow Google's official examples and replace:

- API key with the provider key
- base URL with the chosen Google-compatible Gemini endpoint

Do not use OpenAI-style `/images/generations` or `/images/edits` routes for this skill.

## Attachment-Only Inputs

If the image exists only as a chat attachment and the platform does not expose a local file path, do not claim the script can upload it directly.

Use this rule:

1. If the user needs an exact edit of the original uploaded pixels, ask for the local file path first.
2. If the user accepts a close recreation, analyze the attached image visually and generate a new image that preserves the original composition and style as closely as possible.

For requests like "replace the English text in this attached image with Chinese", the fallback recreation workflow is acceptable when exact pixel-preserving edit is impossible.

## Quick Start

Set environment variables:

```bash
export NANOBANANA_API_KEY="your-provider-key"
export NANOBANANA_BASE_URL="https://generativelanguage.googleapis.com"
export NANOBANANA_MODEL="gemini-3.1-flash-image-preview"
```

Optional third-party provider:

```bash
export NANOBANANA_BASE_URL="https://api.zhizengzeng.com/google"
export NANOBANANA_ALLOW_THIRD_PARTY=1
```

If you do not want the API key to appear in the command line, store it in a file and use:

```bash
export NANOBANANA_API_KEY_FILE="$PWD/.secrets/nanobanana_api_key"
```

Generate an image:

```bash
python3 scripts/generate_image.py "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
```

Edit an image:

```bash
python3 scripts/generate_image.py "Using the provided image, change only the blue sofa to a vintage brown leather Chesterfield sofa. Keep everything else exactly the same." --input-image ./living-room.png
```

Recreate an attached diagram with translated labels:

```bash
python3 scripts/generate_image.py "Recreate the attached pastel technical diagram with the same layout, icons, arrows, and hand-drawn style. Replace all visible English labels with natural Simplified Chinese. Keep the composition unchanged." --aspect-ratio 16:9 --image-size 2K
```

Safety note:

- `scripts/build_materials_figure_prompt.py` and `--print-prompt` are local-only and do not send data over the network.
- Actual prompt text, API keys, and user-provided input images are sent only when you run the generation scripts against the configured provider.
- Non-official Gemini-compatible endpoints require explicit confirmation via `--allow-third-party` or `NANOBANANA_ALLOW_THIRD_PARTY=1`.

## Workflow

1. Keep the official Gemini request shape.
   Use `POST /v1beta/models/{model}:generateContent` with `X-goog-api-key`.
2. Put prompt text and image inputs into `contents[].parts`.
   Text-only generation uses one text part. Image editing appends one or more inline image parts.
3. Put image options in `generationConfig.imageConfig`.
   Prefer `--aspect-ratio` and `--image-size`, matching the official docs.
4. For materials-science figures, prefer building the final prompt first.
   Use `python3 scripts/build_materials_figure_prompt.py --materials-figure ...` when you want to inspect or refine the prompt before sending any API request.
5. Save image outputs from `candidates[0].content.parts[].inlineData`.
   Save text parts too when returned.
6. If the source image is attachment-only, choose between exact edit and recreation.
   Ask for a local path for exact editing. Use recreation if the user wants the result and accepts a visually matched redraw.

## Environment

Required:
- `NANOBANANA_API_KEY`
- `NANOBANANA_BASE_URL`
  Must be set explicitly. Official Google endpoint: `https://generativelanguage.googleapis.com`

Optional:
- `NANOBANANA_MODEL`
  Default: `gemini-3.1-flash-image-preview`
- `NANOBANANA_TIMEOUT`
  Default: `120`
- `NANOBANANA_API_KEY_FILE`
  Path to a file containing the API key. Prefer this when you do not want the key shown in command history or command logs.
- `NANOBANANA_ALLOW_THIRD_PARTY`
  Set to `1` only when you intentionally want to send API keys and user-provided files to a non-official Gemini-compatible provider.

## Scripts

- `scripts/generate_image.py`
  Python CLI that follows the official Gemini `generateContent` request shape.
- `scripts/generate_image.js`
  Node.js CLI with the same request format.

Common options:
- `--input-image ./source.png`
- `--prompt-file ./background.md`
- `--aspect-ratio 16:9`
- `--image-size 2K`
- `--text-only`
- `--thinking-level high`
- `--include-thoughts`
- `--materials-figure mechanism-figure`
- `--lang zh`
- `--style-note "Nature Energy style"`
- `--print-prompt`
- `--allow-third-party`
- `--api-key-file ./.secrets/nanobanana_api_key`

Default output location:
- `./output/nanobanana/` relative to the current Codex working directory
- Override only when the user explicitly wants another folder

## Official Mapping

Official Google examples:
- `api_key="GEMINI_API_KEY"`
- `base_url="https://generativelanguage.googleapis.com"`

Third-party provider replacements:
- `api_key="your_provider_api_key"`
- `base_url="your_google_compatible_endpoint"`
- `allow_third_party=true`

Optional Zhizengzeng example:
- `api_key="your_zzz_api_key"`
- `base_url="https://api.zhizengzeng.com/google"`
- `allow_third_party=true`

Everything else should stay aligned with the official Gemini documentation.

## Prompting Rules

- For generation, describe the scene instead of dumping keywords.
- For editing, explicitly say what must stay unchanged.
- For multi-image workflows, describe the role of each reference image.
- Prefer English or `zh-CN` prompts when image fidelity matters.
- For attachment-only translation tasks, list each label that must be rewritten so the regenerated image does not miss text.
- If layout fidelity matters, explicitly say to preserve icon positions, arrows, spacing, hierarchy, and reading order.

## Materials Science Figure Shortcut

If the user asks for a materials-science paper figure, journal-style scientific schematic, graphical abstract, mechanism diagram, synthesis workflow figure, microstructure-property diagram, device architecture figure, or characterization-plan figure, use the bundled materials-science templates instead of writing the prompt from scratch.

Workflow:

1. Read [references/materials-science-figure-template.md](references/materials-science-figure-template.md).
2. Pick the closest subtype:
   - `graphical-abstract`
   - `mechanism-figure`
   - `device-architecture`
   - `processing-workflow`
3. Choose the output language:
   - `en`
   - `zh`
4. Insert the user's scientific content into the `Scientific Background` slot, or use the script shortcut directly.
5. Preserve the template's constraints about causality, palette, typography, layout, and avoiding unsupported claims.
6. If the user did not provide exact numbers, keep labels qualitative or explicitly use placeholders rather than fabricating data.
7. If the user wants a specific journal style, append that preference after the template rather than rewriting the template.
8. If the scientific background is long, put it in a markdown file and use `--prompt-file` or `scripts/build_materials_figure_prompt.py --background-file ...` instead of squeezing it into one shell argument.

Python shortcut:

```bash
python3 scripts/generate_image.py "paste the scientific background here" \
  --materials-figure mechanism-figure \
  --lang en \
  --style-note "Benchmark the figure against Nature Materials aesthetics." \
  --aspect-ratio 4:3 \
  --image-size 2K
```

JavaScript shortcut:

```bash
node scripts/generate_image.js "paste the scientific background here" \
  --materials-figure graphical-abstract \
  --lang zh \
  --aspect-ratio 4:3 \
  --image-size 2K
```

Prompt-only preflight:

```bash
python3 scripts/build_materials_figure_prompt.py \
  --materials-figure mechanism-figure \
  --lang en \
  --background-file ./background.md \
  --style-note "Nature Materials aesthetic with concise panel labels."
```

## Failure Handling

- If the API returns `401` or `403`, verify `NANOBANANA_API_KEY`.
- If the CLI says the base URL is missing, set `NANOBANANA_BASE_URL` or pass `--base-url`.
- If the CLI refuses a non-official endpoint, add `--allow-third-party` or set `NANOBANANA_ALLOW_THIRD_PARTY=1` only if that provider is intentional.
- If the API returns `404`, verify that the request is going to `/v1beta/models/{model}:generateContent`.
- If the provider says the model does not exist, verify the exact model name in the official docs and the provider's supported model list.
- If no image is returned, inspect `candidates[0].content.parts` and check whether the request asked for image output.
- If the user supplied only a chat attachment and no file path, do not describe the result as an exact edit unless the platform actually exposed the attachment bytes.

## References

- Read [references/api-reference.md](references/api-reference.md) for the official request shape.
- Read [references/prompt-templates.md](references/prompt-templates.md) for generation and editing prompt scaffolds.
- Read [references/materials-science-figure-template.md](references/materials-science-figure-template.md) when generating materials-science paper figures.
