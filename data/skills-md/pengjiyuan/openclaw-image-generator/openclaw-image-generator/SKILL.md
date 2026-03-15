---
name: openclaw-image-generator
description: Generate professional images (covers, posters, illustrations) with Tiny Stable Diffusion AI. Supports pure background images or text-overlaid designs with customizable titles, subtitles, colors, and positioning. Use for blogs, videos, social media, presentations, documentation, or any visual project. Single or batch generation.
---

# OpenClaw Image Generator

Generate production-ready images using this pipeline:

1. Tiny Stable Diffusion generates background image
2. Pillow renders optional title/subtitle text with customizable styling
3. Output images can be used in any system (blogs, social media, presentations, documentation, etc.)

## Trigger Conditions

Use this skill when user intent includes:

**Image Generation:**

- "Generate/create covers, posters, illustrations"
- "Create cover images for articles, blogs, videos, or social media"
- "Generate background images for presentations or slides"
- "Generate pure background images (without text)"
- "Create branded or product promotional images"

**Text & Design Customization:**

- "Add title or text to images"
- "Adjust text color, size, and positioning"
- "Create multiple text style variations"
- "Improve text and background integration"

**Batch & Optimization:**

- "Batch regenerate visual assets"
- "Generate multiple images with different styles at once"
- "Improve AI image generation prompt quality"
- "Generate cover images for multiple topics"

**Technical:**

- "Tiny SD / Stable Diffusion + Pillow"
- "Generate high-quality images with AI"
- "Need fast image generation"

## Repository Assumptions

- Script path: `scripts/generate_image.py`
- Batch helper: `scripts/batch_generate.py`
- Jobs config: `scripts/jobs.showcase.json` (for batch mode)
- Output directory: customizable via `--output` parameter

If these paths differ, adapt commands to actual repository paths.

## Dependency Setup

Install dependencies from bundled requirements:

```bash
pip install -r scripts/requirements.txt
```

**Platform Support:**

- macOS with Apple Silicon: uses MPS (Metal Performance Shaders)
- NVIDIA GPUs: uses CUDA
- CPU fallback: supported but slower

Backend selection is automatic at runtime.

## Standard Workflow

### 1) Understand the visual requirements

For each image request, gather:

- Target subject or theme
- Desired mood, style, or atmosphere
- Key visual elements
- Text content (title, subtitle) if any

Then create a one-line summary:

- **What:** Main subject (e.g., "wildlife photography", "urban street", "modern architecture")
- **Action:** What's happening (e.g., "capturing a moment", "conveying motion", "showing details")
- **Visual style:** How to depict it (e.g., "cinematic", "photorealistic", "minimalist")
- **Mood:** Tone and atmosphere (e.g., "dramatic lighting", "warm and cozy", "dynamic energy")

### 2) Create an English language prompt

Always write prompts in English (Stable Diffusion models only understand English).

**Recommended structure:**

`[subject], [setting/environment], [lighting/mood], [style/quality], [composition details], no text, 4k`

**Example:**
`majestic deer in misty forest, golden morning light, photorealistic wildlife photography, bokeh background, 4k`

**Prompt best practices for Tiny SD:**

✅ DO:

- Use concrete, specific nouns ("red sports car", "turquoise ocean waves", "luxury modern house")
- Include lighting descriptions ("golden hour", "dramatic sunset", "cinematic lighting")
- Specify mood/atmosphere ("cozy", "dynamic", "serene", "energetic")
- Keep 5-8 key descriptive elements
- Always include `no text, 4k`

❌ AVOID:

- Chinese or non-English text in prompts
- Too many unrelated objects
- Conflicting visual styles
- Asking the model to render readable text
- Overly complex or abstract descriptions

Negative prompt is handled by the script; do not duplicate unless asked.

### 3) Generate the image

**Text overlay is optional:**

- Provide `--title` (and optional `--subtitle`) for text-overlaid images
- Omit both to generate background image only

**Required parameter:** `--prompt` (no built-in style templates)

**Single image with text overlaid:**

```bash
python3 scripts/generate_image.py \
  --prompt "<English prompt>" \
  --title "<Title text>" \
  --subtitle "<Optional subtitle>" \
  --output "outputs/image.png" \
  --steps 28 \
  --seed 42 \
  --position bottom
```

**Background image only:**

```bash
python3 scripts/generate_image.py \
  --prompt "tropical beach with turquoise water, white sand, palm trees, 4k" \
  --output "outputs/beach.png"
```

**With custom text styling:**

```bash
python3 scripts/generate_image.py \
  --prompt "modern luxury house, sunset lighting, contemporary architecture, 4k" \
  --title "Dream Home" \
  --title-color "255,200,50,255" \
  --title-size 60 \
  --outline-width 3 \
  --outline-color "0,0,0,200" \
  --output "outputs/house.png"
```

**Parameter tuning guide:**

| Parameter         | Default         | Recommended Range     | Purpose                                              |
| ----------------- | --------------- | --------------------- | ---------------------------------------------------- |
| `--steps`         | 28              | 25-30                 | Inference steps (higher = better quality but slower) |
| `--seed`          | 42              | any integer           | Random seed for reproducibility                      |
| `--position`      | bottom          | top / center / bottom | Text placement on image                              |
| `--title-size`    | auto            | 40-80                 | Font size for title                                  |
| `--title-color`   | 255,255,255,255 | RGBA values           | Title text color                                     |
| `--outline-width` | 3               | 0-6                   | Text outline stroke (0 = no outline)                 |
| `--outline-color` | 0,0,0,200       | RGBA values           | Outline color for readability                        |

### 4) Verify output quality

Inspect each generated image for:

- ✓ Text readability (good contrast with background)
- ✓ Text positioning (no overflow, proper alignment)
- ✓ Visual coherence (style consistency across batch)
- ✓ No artifacts or degradation
- ✓ Output file size and format

## Batch Generation Mode

For generating multiple images at once:

**Step 1:** Create a JSON configuration file (e.g., `jobs.json`):

```json
{
  "jobs": [
    {
      "name": "wildlife-photo",
      "prompt": "majestic deer in misty forest, golden morning light, photorealistic, 4k",
      "title": "Wild Beauty",
      "subtitle": "Nature's Elegance",
      "output": "outputs/01-wildlife.png",
      "seed": 101,
      "steps": 28,
      "position": "bottom"
    },
    {
      "name": "car-photo",
      "prompt": "red sports car on mountain road, sunset lighting, motion blur, 4k",
      "title": "Speed & Power",
      "output": "outputs/02-car.png",
      "seed": 202,
      "steps": 28,
      "position": "top"
    }
  ]
}
```

**Step 2:** Run batch generation:

```bash
python3 scripts/batch_generate.py \
  --jobs jobs.json
```

**Step 3:** Verify all outputs were generated successfully and report paths.

## Prompt Quality Rules

**✅ Effective prompt elements:**

- **Concrete subjects:** `majestic deer`, `luxury yacht`, `modern skyscraper`, `tropical beach`
- **Specific lighting:** `golden hour`, `dramatic sunset`, `volumetric light`, `cinematic glow`
- **Color palettes:** `deep blue and cyan`, `warm golden tones`, `emerald and teal`
- **Composition:** `wide angle`, `shallow depth of field`, `symmetrical framing`, `bokeh background`
- **Quality markers:** `photorealistic`, `4k`, `masterpiece`, `professional photography`

**❌ Things to avoid:**

- Non-English text in prompts
- Overly many unrelated objects
- Contradictory visual styles (e.g., "minimalist cyberpunk")
- Requesting readable text/numbers in images
- Generic descriptions without specifics

## Troubleshooting

**Issue: Generated image doesn't match prompt**

- ✓ Shorten the prompt and move main subject to the beginning
- ✓ Increase `--steps` to 30-35 for more detail
- ✓ Try different seeds: `42`, `101`, `202`, etc.
- ✓ Check that all words are spelled correctly and in English

**Issue: Text overlay looks misaligned or illegible**

- ✓ Keep `--position bottom` unless you need centered or top text
- ✓ Reduce `--title-size` if text is truncated
- ✓ Try `--outline-width 0` if outline is too thick
- ✓ Use a simpler background prompt (fewer objections)
- ✓ Ensure sufficient contrast between text color and background

**Issue: Colors or style incorrect**

- ✓ Verify `--title-color` and `--outline-color` RGBA values
- ✓ Re-check English prompt spelling and grammar
- ✓ Regenerate with different seed values

**Issue: File path not found**

- ✓ Verify `--output` path exists or use auto-creation (`os.makedirs`)
- ✓ Use absolute path or project-relative path consistently
- ✓ Check file permissions in output directory

## Response Style When Using This Skill

When generating images, provide clear feedback:

1. **Item summary** (1 line describing the image concept)
2. **Final prompt** used for generation
3. **Output path** where image was saved
4. **Configuration notes** (seed, steps, text styling applied)
5. **Status** (success/failure with any issues)

**Example output:**

```
✅ Wildlife Photography - Majestic deer in forest
Prompt: "majestic deer standing in misty forest, golden morning light..."
Output: outputs/01-wildlife.png
Config: seed=101, steps=28, title="Wild Beauty", position=bottom
```
