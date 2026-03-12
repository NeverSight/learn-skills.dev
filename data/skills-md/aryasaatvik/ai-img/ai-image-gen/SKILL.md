---
name: ai-image-gen
description: "Generate or edit images using the ai-img CLI with AI SDK (multi-provider: OpenAI, Google, Fal). Use when: (1) Generating images from text prompts, (2) Editing existing images with AI, (3) Batch processing multiple prompts. Requires provider API key (OPENAI_API_KEY, GOOGLE_API_KEY, or FAL_API_KEY). Located at ~/Developer/ai-img."
---

# AI Image Generation Skill

Generate or edit images using the **ai-img** CLI with Vercel AI SDK.

## When to use
- Generate images from text prompts
- Edit existing images with AI (inpainting, style transfer)
- Batch process multiple image generation jobs

## Prerequisites

1. **Install CLI:**
   ```bash
   # Option 1: Install globally with Bun (recommended)
   bun add -g ai-img

   # Option 2: Clone and build
   git clone https://github.com/aryasaatvik/ai-img
   cd ai-img
   bun install
   bun run build
   ```

2. **Set API key** (choose one):
   - OpenAI: `export OPENAI_API_KEY=sk-...`
   - Google: `export GOOGLE_API_KEY=...`, `export GEMINI_API_KEY=...`, or `export GOOGLE_GENERATIVE_AI_API_KEY=...`
   - FAL AI: `export FAL_API_KEY=...`

## Quick Decision Tree

```
Image Generation?
├─ Generate new image → ai-img generate
├─ Edit existing image → ai-img edit
└─ Many images at once → ai-img batch
```

## Commands

### generate

Generate new images from text prompts.

```bash
# Basic
ai-img generate --prompt "A red cat"

# Multiple images
ai-img generate --prompt "A sunset" --count 3

# Specific provider/model
ai-img generate --prompt "A cat" --provider fal --model "fal-ai/flux/dev"

# With size and quality
ai-img generate --prompt "Landscape" --size 1536x1024 --quality high
```

### edit

Edit existing images with AI.

```bash
# Basic edit
ai-img edit --input photo.jpg --prompt "Make it vintage"

# With mask (partial edit)
ai-img edit --input photo.jpg --mask mask.png --prompt "Add sunglasses"

# Multiple input images
ai-img edit --input "product.jpg,background.jpg" --prompt "Place product in scene"
```

### batch

Process multiple jobs from JSONL file.

```bash
# Create jobs file (one JSON per line)
echo '{"prompt": "A red car", "out": "red-car.png"}
{"prompt": "A blue car", "out": "blue-car.png"}' > jobs.jsonl

# Run batch
ai-img batch --input jobs.jsonl --outDir ./output --concurrency 5
```

## Options Reference

| Flag | Description | Default |
|------|-------------|---------|
| `--prompt, -p` | Text prompt | Required |
| `--provider, -P` | AI provider: openai, google, fal | openai |
| `--model, -m` | Model ID | Provider default |
| `--size, -s` | Image size (WxH) | 1024x1024 |
| `--aspectRatio` | Aspect ratio (e.g., 16:9) - for Gemini | - |
| `--count, -c` | Number of images | 1 |
| `--seed` | Random seed | Random |
| `--quality` | Quality: low/medium/high/auto | auto |
| `--output, -o` | Output file path | output.png |
| `--outDir` | Output directory | Current dir |

## Providers & Models

| Provider | Default Model | Environment Variable |
|----------|---------------|---------------------|
| OpenAI | gpt-image-1.5 | OPENAI_API_KEY |
| Google | imagen-3.0-generate-002 | GOOGLE_API_KEY or GEMINI_API_KEY |
| FAL AI | fal-ai/flux/dev | FAL_API_KEY |

See `references/providers.md` for full model list.

## Prompting Tips

- Be specific about style: "photorealistic", "oil painting", "3D render"
- Include composition: "centered", "wide shot", "close-up"
- Specify mood/lighting: "golden hour", "dramatic shadows", "soft light"
- Add constraints: "no text", "no logos"

See `references/prompting.md` for detailed guidance.

## Examples

### Product Photography
```bash
ai-img generate --prompt "White ceramic mug on wooden table, product photography, soft natural light, clean background" --provider openai --size 1024x1024 --quality high
```

### Icon Generation
```bash
ai-img generate --prompt "Simple geometric rocket icon, flat design, blue and white, minimal" --provider fal --model "fal-ai/flux/dev" --size 512x512
```

### Background Replacement
```bash
ai-img edit --input product.jpg --prompt "Replace background with warm sunset gradient, keep product unchanged" --provider openai
```

## Troubleshooting

- **"Missing API key"**: Ensure your API key is set in the environment
- **"Invalid model"**: Check the model ID is valid for the provider
- **Rate limiting**: Reduce `--concurrency` for batch jobs

See `references/cli.md` for full CLI reference.
