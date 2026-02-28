---
name: gemini-image-gen
description: "Generate images using Google's Gemini API — hero backgrounds, OG images, placeholder photos, textures, and style-matched variants. Uses free-tier models for drafts, paid for finals. No dependencies beyond Python 3. Trigger with 'generate image', 'gemini image', 'make a hero background', 'create placeholder photo', 'generate OG image', 'AI image', or 'need an image for'."
compatibility: claude-code-only
---

# Gemini Image Generator

Generate contextual images for web projects using the Gemini API. Produces hero backgrounds, OG cards, placeholder photos, textures, and style-matched variants.

## Setup

**API Key**: Set `GEMINI_API_KEY` as an environment variable. Get a key from https://aistudio.google.com/apikey if you don't have one.

```bash
export GEMINI_API_KEY="your-key-here"
```

## Workflow

### Step 1: Understand What's Needed

Gather from the user or project context:
- **What**: hero background, product photo, texture, OG image, placeholder
- **Style**: warm/cool/minimal/luxurious/bold — check project's colour palette (input.css, tailwind config)
- **Dimensions**: hero (1920x1080), OG (1200x630), square (1024x1024), custom
- **Count**: single image or multiple variants to choose from

### Step 2: Build the Prompt

Use concrete photography parameters, not abstract adjectives. Read [references/prompting-guide.md](references/prompting-guide.md) for the full framework.

**Quick rules**:
- Narrate like directing a photographer
- Use camera specs: "85mm f/1.8", "wide angle 24mm"
- Use colour anchors from the project palette: "warm terracotta (#C66A52) and cream (#F5F0EB) tones"
- Use lighting descriptions: "golden-hour light from the left, 4500K"
- Always end with: "No text, no watermarks, no logos, no hands"

### Step 3: Generate

```bash
python3 plugins/design-assets/skills/gemini-image-gen/scripts/generate-image.py \
  --prompt "Soft-focus atmospheric background, warm gold and cream botanical elements, luxury spa aesthetic, wide landscape" \
  --output public/images/hero.png \
  --model gemini-2.5-flash-image
```

Multiple variants:

```bash
python3 .../generate-image.py --prompt "..." --output public/images/hero.png --count 3
# Produces hero-1.png, hero-2.png, hero-3.png
```

Style matching from a reference image:

```bash
python3 .../generate-image.py \
  --prompt "Same warm lighting and colour palette, but showing a massage treatment room" \
  --reference public/images/existing-hero.jpg \
  --output public/images/services-bg.png \
  --model gemini-3-pro-image-preview
```

### Step 4: Post-Process (Optional)

Use the **image-processing** skill for resizing, format conversion, or optimisation:

```bash
python3 plugins/design-assets/skills/image-processing/scripts/process-image.py \
  optimise public/images/hero.png --output public/images/hero.webp --width 1920
```

### Step 5: Present to User

Show the generated images for review. Read the image files to display them inline if possible, otherwise describe what was generated and let the user open them.

## Presets

Starting prompts — enhance with project-specific context (colours, mood, subject):

| Preset | Base Prompt |
|--------|-------------|
| `hero-background` | "Wide atmospheric background, soft-focus, [colour tones], [mood], landscape 1920x1080" |
| `og-image` | "Clean branded card background, [brand colours], subtle gradient, 1200x630" |
| `placeholder-photo` | "Professional stock-style photo of [subject], natural lighting, warm tones" |
| `texture-pattern` | "Subtle repeating texture, [material], seamless tile, muted [colour]" |
| `product-shot` | "Product photography, [item] on [surface], soft studio lighting, clean background" |

## Model Selection

| Use case | Model | Cost |
|----------|-------|------|
| Drafts, quick placeholders | `gemini-2.5-flash-image` | Free (~500/day) |
| Final client assets | `gemini-3-pro-image-preview` | ~$0.04/image |
| Style-matched variants | `gemini-3-pro-image-preview` + `--reference` | ~$0.04/image |

Verify current model IDs if errors occur — they change frequently.

## Reference Files

| When | Read |
|------|------|
| Building effective prompts | [references/prompting-guide.md](references/prompting-guide.md) |
