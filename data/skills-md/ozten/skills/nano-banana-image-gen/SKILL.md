---
name: nano-banana-image-gen
description: Generate images using the `imagen` CLI (Gemini and OpenAI models). Use when the user says "nano banana", "generate an image", "create an image", "make me a picture", "image gen", "draw", "illustrate", or wants to create images from text prompts.
---

# Image Generation with imagen CLI

Generate images using the `imagen` CLI — a unified interface for Google Gemini and OpenAI image models. Supports text prompts, multiple aspect ratios, output formats, batch generation, and more.

## Prerequisites

1. **imagen CLI**: Install via `curl -fsSL https://raw.githubusercontent.com/ozten/imagen/main/scripts/install.sh | bash`
2. **API Keys**: Configure via environment variables or config file (see below)

## Quick Start

```bash
# Basic generation (uses default nano-banana / gemini-3-pro-image-preview)
imagen "A cat wearing a top hat" -o cat.jpg

# With aspect ratio
imagen "Mountain panorama" --aspect-ratio 16:9 -o mountains.jpg

# Using OpenAI model
imagen "Cyberpunk cityscape" -m gpt-1.5 -o city.png

# Multiple images
imagen "Abstract art" -n 3 -o art.jpg

# Higher resolution
imagen "Detailed landscape" --size 2K -o landscape.jpg

# Read prompt from file
imagen --prompt-file prompt.txt -o result.jpg
```

## Models

| Alias | Model ID | Provider |
|-------|----------|----------|
| `nano-banana` (default) | `gemini-3-pro-image-preview` | Gemini |
| `gpt-1.5` | `gpt-image-1.5` | OpenAI |
| `gpt-1` | `gpt-image-1` | OpenAI |
| `gpt-1-mini` | `gpt-image-1-mini` | OpenAI |

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `-m, --model` | see Models table | `nano-banana` | Image generation model |
| `-a, --aspect-ratio` | 1:1, 16:9, 9:16, 4:3, 3:4, etc. | 1:1 | Output aspect ratio |
| `-s, --size` | 1K, 2K, 4K | 1K | Image resolution |
| `-q, --quality` | auto, low, medium, high | auto | Quality (OpenAI models only) |
| `-f, --format` | jpeg, png, webp | jpeg | Output format |
| `-o, --output` | path | auto-generated | Output file path |
| `-n, --count` | integer | 1 | Number of images to generate |
| `-p, --prompt-file` | path | none | Read prompt from file |
| `-v, --verbose` | flag | off | Verbose output |

## Workflow

If the user provides `$ARGUMENTS`, treat them as the image prompt. Otherwise ask what they'd like to generate.

### Step 0: Check imagen is installed

Before generating, verify `imagen` is available:

```bash
which imagen
```

**If `imagen` is NOT found:**
1. Tell the user that the `imagen` CLI is required but not installed
2. Ask them: "Would you like me to install the `imagen` CLI? It's a lightweight Rust binary from https://github.com/ozten/imagen"
3. If they agree, run:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/ozten/imagen/main/scripts/install.sh | bash
   ```
4. After installation, verify it worked: `imagen --version`

**If API keys are NOT configured:**

Check for API keys:
```bash
# Check env vars
echo "${GEMINI_API_KEY:+gemini_ok}" "${OPENAI_API_KEY:+openai_ok}"

# Check config file
cat ~/.config/imagen/config.toml 2>/dev/null
```

If no keys are found for the provider needed by the chosen model:
1. Tell the user which API key is needed (Gemini for nano-banana, OpenAI for gpt-* models)
2. Ask them to set up keys via environment variable or config file:
   - **Environment variable**: `export GEMINI_API_KEY="your-key"` or `export OPENAI_API_KEY="your-key"`
   - **Config file** (`~/.config/imagen/config.toml`):
     ```toml
     [keys]
     gemini = "your-gemini-api-key"
     openai = "your-openai-api-key"
     ```
3. Do NOT proceed with generation until at least one relevant key is configured

### Step 1: Generate the image

Determine the prompt, output path, model, aspect ratio, and other options, then run:

```bash
imagen "PROMPT" \
    --model MODEL \
    --aspect-ratio ASPECT_RATIO \
    --size SIZE \
    --format FORMAT \
    --output OUTPUT_PATH
```

Only include flags that differ from defaults.

### Step 2: Report results

Report the output file path and parameters used. If generation fails, check:
- API key is configured for the chosen provider
- Prompt doesn't violate content policies
- Model alias is valid

## Batch Generation

For multiple images, either use `-n` for the same prompt or run `imagen` multiple times with different prompts:

```bash
# Same prompt, multiple variations
imagen "Abstract art" -n 3 -o abstract.jpg

# Different prompts in sequence
imagen "Panel 1: A sunny beach" -o panel_1.jpg
imagen "Panel 2: Same beach at sunset" -o panel_2.jpg
```

## Integration

Other skills and pipelines can delegate image generation to this skill by invoking the `imagen` CLI directly.
