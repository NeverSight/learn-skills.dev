---
name: gpt-image-2-skill
description: GPT Image 2 prompt gallery, agentic skill, and CLI for OpenAI image generation and editing with curated prompts and reference workflows
triggers:
  - generate an image with GPT Image 2
  - create an AI image using OpenAI
  - use gpt-image CLI to make an image
  - edit an image with GPT Image 2
  - install gpt-image skill for Claude Code
  - use the image prompt gallery
  - text to image with OpenAI gpt-image-2
  - inpaint or mask an image with OpenAI
---

# GPT Image 2 Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A prompt gallery, CLI, and agentic skill for OpenAI's `gpt-image-2` model. Provides 162 curated prompts across categories (research figures, UI mockups, typography, photography, anime, maps, product shots), a full-featured CLI, and skill integrations for Claude Code, Codex, and other agent runtimes.

---

## Install

### CLI (fastest)

```bash
# Run without installing
uvx --from git+https://github.com/wuyoscar/gpt_image_2_skill gpt-image -p "a cat astronaut"

# Install to PATH permanently
uv tool install git+https://github.com/wuyoscar/gpt_image_2_skill
gpt-image -p "a cat astronaut"
```

### Claude Code

```text
/plugin marketplace add wuyoscar/gpt_image_2_skill
/plugin install gpt-image@wuyoscar-skills
```

### Codex

```text
$skill-installer install https://github.com/wuyoscar/gpt_image_2_skill/tree/main/skills/gpt-image
```

### Manual agent-skill install

```bash
git clone https://github.com/wuyoscar/gpt_image_2_skill.git
cd gpt_image_2_skill

export AGENT_SKILLS_DIR="/path/to/your/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
ln -s "$PWD/skills/gpt-image" "$AGENT_SKILLS_DIR/gpt-image"
```

---

## Configuration

The CLI and skill read your OpenAI key from the environment or `~/.env`:

```bash
export OPENAI_API_KEY="sk-..."
```

No other configuration is required.

---

## CLI Reference

### Text → Image (generation)

```bash
# Basic generation
gpt-image -p "a photorealistic convenience store at 10pm"

# With size, quality, and explicit output file
gpt-image -p "a neon-lit Tokyo alley at midnight" \
  --size portrait --quality high -f tokyo-alley.png

# Square, low quality (cheap draft)
gpt-image -p "watercolor mountains at sunrise" \
  --size 1k --quality low -f draft.png

# Batch: generates 4 variants, saved as out_0.png … out_3.png
gpt-image -p "product shot of a ceramic mug on white" \
  --size square --quality medium -n 4 -f out.png
```

### Text + Reference Image → Image (edit / restyle)

```bash
# Single reference restyle
gpt-image -p "Make it a winter evening with heavy snowfall" \
  -i chess.png --quality high -f chess-winter.png

# Multi-reference composite: dog from image 2, scene from image 1
gpt-image -p "Place the dog from image 2 next to the woman in image 1. \
Match the same lighting, composition, and background." \
  -i woman.png -i dog.png --size portrait --quality medium -f woman-with-dog.png
```

### Mask-based Inpainting

```bash
# opaque pixels = keep, transparent pixels = regenerate
gpt-image -p "replace sky with aurora borealis" \
  -i photo.jpg -m sky_mask.png -f aurora.png
```

### Full Parameter Reference

| Flag | Values | Default | Notes |
|---|---|---|---|
| `-p, --prompt` | string | required | Full prompt text |
| `-f, --file` | path | auto-timestamped `.png` | Output file path |
| `-i, --image` | path (repeatable) | — | Triggers `/v1/images/edits`; pass multiple for multi-ref |
| `-m, --mask` | path (PNG with alpha) | — | Requires `-i`; transparent = regenerate |
| `--size` | `1k` `2k` `4k` `portrait` `landscape` `square` `wide` `tall` or `1024x1024` | `1024x1024` | Literals must be 16-px multiples, max edge 3840 |
| `--quality` | `auto` `low` `medium` `high` | `high` | Budget dial: `low`=drafts, `high`=final/text-heavy |
| `-n, --n` | int | 1 | Batch count; suffixes files `_0`, `_1`, … |
| `--background` | `auto` `opaque` | API default | `opaque` disables transparency |
| `--moderation` | `auto` `low` | `low` | `low` for broader exploration |
| `--format` | `png` `jpeg` `webp` | `png` | Response encoding format |
| `--compression` | 0–100 | — | JPEG/WebP only |

**Exit codes:** `0` success · `1` API/refusal error · `2` bad args or missing key

---

## Python SDK Usage

### Text → Image

```python
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from environment

result = client.images.generate(
    model="gpt-image-2",
    prompt="A photorealistic ceramic mug on a white studio background, "
           "soft directional light, light shadow beneath",
    size="1024x1024",   # square
    quality="high",
)

# Save result
import base64
from pathlib import Path

image_bytes = base64.b64decode(result.data[0].b64_json)
Path("mug.png").write_bytes(image_bytes)
print("Saved mug.png")
```

### Portrait / Tall Generation

```python
result = client.images.generate(
    model="gpt-image-2",
    prompt="Minimalist event poster: 'Boston Spring Jazz Festival · April 2026' "
           "in bold serif, pastel cherry-blossom watercolor background, centered layout",
    size="1024x1536",   # portrait (3:4)
    quality="high",
)
```

### Image Edit (single reference)

```python
result = client.images.edit(
    model="gpt-image-2",
    image=open("chess.png", "rb"),
    prompt="Make it a winter evening with heavy snowfall, keep the chess pieces identical",
    size="1024x1024",
    quality="high",
)
```

### Multi-Reference Edit

```python
result = client.images.edit(
    model="gpt-image-2",
    image=[open("woman.png", "rb"), open("dog.png", "rb")],
    prompt="Place the dog from image 2 next to the woman in image 1. "
           "Match the same lighting, composition, and background. "
           "Do not change anything else.",
    size="1024x1536",
    quality="medium",
)
```

### Mask-Based Inpainting

```python
result = client.images.edit(
    model="gpt-image-2",
    image=open("photo.jpg", "rb"),
    mask=open("sky_mask.png", "rb"),   # transparent = regenerate
    prompt="Replace the sky with dramatic aurora borealis, keep everything below the horizon identical",
    size="1024x1024",
    quality="high",
)
```

### Batch Generation with Saving

```python
import base64
from pathlib import Path
from openai import OpenAI

def generate_batch(prompt: str, n: int = 4, size: str = "1024x1024",
                   quality: str = "medium", out_prefix: str = "variant") -> list[Path]:
    client = OpenAI()
    result = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
    )
    paths = []
    for i, item in enumerate(result.data):
        path = Path(f"{out_prefix}_{i}.png")
        path.write_bytes(base64.b64decode(item.b64_json))
        paths.append(path)
        print(f"Saved {path}")
    return paths

# Usage
variants = generate_batch(
    prompt="product shot of a blue glass water bottle, white background, studio lighting",
    n=4,
    quality="low",   # cheap sweep; rerun winner at high
)
```

---

## Prompt Engineering Patterns

### Structure template

```
[background/scene] → [subject] → [key details] → [constraints/intended use]
```

### Research paper figure

```bash
gpt-image -p "Clean scientific diagram: transformer architecture overview. \
White background, labeled encoder/decoder blocks with arrows, \
color-coded attention heads in teal and orange, \
sans-serif labels, publication-ready, 4K resolution" \
--size landscape --quality high -f transformer-diagram.png
```

### UI mockup

```bash
gpt-image -p "Mobile app UI mockup, iOS style, dark mode. \
Fitness tracking dashboard: circular progress ring in neon green, \
daily steps '8,432', heart rate '74 bpm', \
bottom nav with 4 icons, pixel-perfect, no lorem ipsum" \
--size portrait --quality high -f fitness-app.png
```

### Typography poster

```bash
gpt-image -p "Event poster. Text: 'SUMMER SONIC 2026' in bold condensed sans-serif. \
Subtext: 'Tokyo · August 9–10'. Vivid sunset gradient background (magenta to amber). \
Geometric grid overlay, high contrast, print-ready" \
--size portrait --quality high -f poster.png
```

### Photorealistic product shot

```bash
gpt-image -p "Photorealistic product photo: matte black insulated coffee thermos, \
condensation droplets, placed on dark slate surface, \
single soft key light from upper-left, shallow depth of field, \
shot on Canon 5D, 85mm lens, commercial quality" \
--size square --quality high -f thermos.png
```

### Put required text in quotes

```python
# Any text that must appear verbatim in the image — put in straight quotes in the prompt
prompt = '''Storefront sign reading "OPEN 24/7" in red neon. 
Below it: "Est. 1987" in smaller white block letters.
Realistic neon glow, night scene, rain-slicked pavement.'''
```

---

## Quality / Budget Strategy

| Stage | `--quality` | When to use |
|---|---|---|
| Exploration sweep | `low` | Generating 8–16 variants to find direction |
| Normal iteration | `medium` | Style probing, layout checks |
| Final / shipping | `high` | In-image text, dense diagrams, posters, paper figures |

**Rule of thumb:** start every new concept at `low`, run 4 variants, pick the best, then rerun at `high`.

```bash
# Step 1: cheap sweep
gpt-image -p "minimalist logo for a coffee brand" --quality low -n 4 -f logo.png

# Step 2: pick winner (e.g. logo_2.png), rerun at high
gpt-image -p "minimalist logo for a coffee brand" --quality high -f logo-final.png
```

---

## Size Reference

| Alias | Pixels | Ratio | Best for |
|---|---|---|---|
| `square` / `1k` | 1024×1024 | 1:1 | Social posts, icons, product shots |
| `portrait` | 1024×1536 | 2:3 | Mobile UI, posters, stories |
| `landscape` | 1536×1024 | 3:2 | Web banners, diagrams |
| `wide` | 1792×1024 | 7:4 | Cinematic, hero sections |
| `tall` | 1024×1792 | 4:7 | Long-form mobile content |
| `2k` | 2048×2048 | 1:1 | High-res assets |

---

## Common Patterns & Recipes

### Virtual try-on (multi-ref edit)

```python
# image 1 = person, image 2 = garment
result = client.images.edit(
    model="gpt-image-2",
    image=[open("person.png", "rb"), open("shirt.png", "rb")],
    prompt="Dress the person in image 1 wearing the shirt from image 2. "
           "Keep the person's face, pose, and background identical. "
           "Natural fabric draping and lighting.",
    size="1024x1536",
    quality="high",
)
```

### Billboard / signage mockup

```python
result = client.images.edit(
    model="gpt-image-2",
    image=open("billboard_photo.jpg", "rb"),
    mask=open("billboard_mask.png", "rb"),
    prompt='Replace the billboard face with: "SALE ENDS SUNDAY" '
           'in bold white text on solid red background. '
           'Match perspective and lighting of surrounding scene.',
    size="1536x1024",
    quality="high",
)
```

### Anime / manga style transfer

```bash
gpt-image -p "Anime key visual style (Studio Ghibli-inspired): \
young woman standing on a hillside overlooking a coastal town at golden hour, \
painterly backgrounds, soft cel shading, \
detailed environmental storytelling, cinematic composition" \
--size landscape --quality high -f anime-scene.png
```

### Translation / text replacement edit

```python
# Replace text in an existing image in a different language
result = client.images.edit(
    model="gpt-image-2",
    image=open("menu_english.png", "rb"),
    prompt='Replace all English text with Japanese translations. '
           'Keep the exact same layout, fonts, colors, and imagery. '
           'Translate "Grilled Salmon" → "グリルサーモン", '
           '"Caesar Salad" → "シーザーサラダ".',
    size="1024x1024",
    quality="high",
)
```

---

## Troubleshooting

### `OPENAI_API_KEY` not found

```bash
export OPENAI_API_KEY="sk-..."
# or add to ~/.env — the CLI reads it automatically
```

### Refusal / content policy error (exit code 1)

- Full API response is echoed to stderr
- Try rephrasing: be more descriptive and less ambiguous about intent
- Switch `--moderation auto` → `--moderation low` for broader exploration (already the CLI default)

### Text in image is garbled or wrong

- Always use `--quality high` for any prompt containing required text
- Wrap required text in straight quotes inside the prompt string
- Keep required text short (under ~6 words per element)

### Multi-ref edit ignores one image

- Be explicit: "the subject in **image 1**", "the object in **image 2**"
- Reduce to two input images; more than two can cause ambiguity

### Size rejected by API

- Dimensions must be multiples of 16
- Max edge: 3840px
- Max aspect ratio: 3:1
- Total pixels: 655,360–8,294,400

### `gpt-image-2` rejects `--input-fidelity`

- `input-fidelity` is a `gpt-image-1`/`1.5` parameter; the CLI drops it automatically for `gpt-image-2`

### Slow generation at `high` quality

Expected — `high` quality is significantly slower. Use `low` for drafts, `high` only for finals.

---

## Prompt Gallery Categories

The skill ships 162 prompts split across category files under `skills/gpt-image/references/`:

- `gallery-research-paper-figures.md` — diagrams, charts, architecture visuals
- `gallery-ui-ux-mockups.md` — mobile/web UI, dashboards, design systems
- `gallery-product-and-food.md` — product shots, food styling, e-commerce
- `gallery-typography.md` — posters, signage, lettering
- `gallery-photography.md` — portrait, landscape, macro, street
- `gallery-anime-manga.md` — key visuals, character design, backgrounds
- `gallery-maps.md` — illustrated maps, infographic cartography
- Start with `gallery.md` as a routing index to pick the right category file
