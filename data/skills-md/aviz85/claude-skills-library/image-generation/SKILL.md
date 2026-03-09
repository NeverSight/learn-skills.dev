---
name: image-generation
description: "Generate images with Gemini (default) or fal.ai FLUX.2 klein 4B (--cheap for fast/low-cost). Generate videos with Grok Imagine (default) or fal.ai LTX-2 (--cheap). Use for: create image, generate visual, AI image generation, poster, video generation."
version: "1.0.0"
author: aviz85
tags: [image, video, AI, generation, Gemini, fal.ai, poster]
---

# Image Generation

Generate images using Google's Gemini model (default) or fal.ai FLUX.2 klein 4B (cheap mode).

## Quick Start

**MANDATORY:** Always use `-d` (destination) flag to specify output path. This avoids file management issues with `poster_0.jpg` in the scripts folder.

```bash
cd ~/.claude/skills/image-generation/scripts

# ALWAYS specify destination with -d flag
npx tsx generate_poster.ts -d /tmp/my-image.jpg "A futuristic city at sunset"

# Cheap mode: fal.ai FLUX.2 klein 4B (fast, lower cost)
npx tsx generate_poster.ts --cheap -d /tmp/city.jpg "A futuristic city at sunset"

# With aspect ratio
npx tsx generate_poster.ts -d /tmp/landscape.jpg --aspect 3:2 "A wide landscape poster"
npx tsx generate_poster.ts --cheap -d /tmp/story.jpg -a 9:16 "A vertical story format"

# With reference assets (image editing)
npx tsx generate_poster.ts -d /tmp/banner.jpg --assets "/path/to/avatar.jpg" "Create banner with character"
npx tsx generate_poster.ts --cheap -d /tmp/photo.jpg --assets "/path/to/image.jpg" "Turn this into a realistic photo"
```

**Why `-d` is mandatory:**
- Output goes to predictable location (e.g., `/tmp/` for temp images)
- Avoids hunting for `poster_0.jpg` in scripts folder
- Enables immediate use without file renaming

## Providers

| Provider | Flag | Use Case | Cost |
|----------|------|----------|------|
| **Gemini** | (default) | High quality, best results | Higher |
| **fal.ai klein 4B** | `--cheap` | Fast, budget-friendly | ~$0.003/image |

### Cheap Mode (`--cheap`)

Uses fal.ai FLUX.2 klein 4B - a distilled FLUX model optimized for speed and cost.

**Why use cheap mode?**
- **Cost**: ~$0.003 per image (vs Gemini's higher cost)
- **Speed**: Fast 4-step inference (~2-4 seconds)
- **Quality**: Good enough for drafts, social media, iterations
- **Batch friendly**: Generate many variations quickly

**Endpoints:**
- **Text-to-image**: `fal-ai/flux-2/klein/4b`
- **Image editing** (with --assets): `fal-ai/flux-2/klein/4b/edit`

**Best for:**
- Quick iterations and previews
- Social media content
- Concept exploration
- Batch generation (10+ images)

**Use Gemini instead for:**
- Final production assets
- Complex compositions
- Text-heavy images (especially Hebrew)

## Quality

Control image resolution with `--quality` or `-q`:

| Quality | Resolution | Use Case |
|---------|------------|----------|
| `1K` | 1024px | **Default** - fast, good for web |
| `2K` | 2048px | High quality - print, detailed posters |

```bash
npx tsx generate_poster.ts -q 2K "High quality poster"
```

## Aspect Ratio

**IMPORTANT:** Always use the default 3:2 aspect ratio unless the user explicitly requests a different format (like "vertical", "story", "square", etc.). Do NOT change the aspect ratio on your own.

Control image dimensions with `--aspect` or `-a`:

| Ratio | Use Case |
|-------|----------|
| `3:2` | Horizontal **(DEFAULT - use this unless user specifies otherwise)** |
| `1:1` | Square - Instagram, profile pics |
| `2:3` | Vertical - Pinterest, posters |
| `16:9` | Wide - YouTube thumbnails, headers |
| `9:16` | Tall - Stories, reels, TikTok |

```bash
npx tsx generate_poster.ts --aspect 3:2 "Your prompt"
npx tsx generate_poster.ts -a 16:9 "Your prompt"
```

## Adding Assets (Reference Images)

Use `--assets` with full paths to include reference images:

```bash
# Single asset
npx tsx generate_poster.ts --assets "/full/path/to/image.jpg" "Your prompt"

# Multiple assets (comma-separated)
npx tsx generate_poster.ts --assets "/path/a.jpg,/path/b.png" "Use both images"

# With cheap mode - uses fal.ai edit endpoint
npx tsx generate_poster.ts --cheap --assets "/path/to/image.jpg" "Turn this into a painting"
```

**Supported formats:** `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`

**IMPORTANT:** Assets are NOT automatically included. You must explicitly pass them via `--assets`.

## Destination (MANDATORY)

**ALWAYS** use `--destination` or `-d` to specify output path:

```bash
# REQUIRED: Always specify destination
npx tsx generate_poster.ts -d /tmp/poster.jpg "My poster"

# If file exists, auto-adds suffix: poster_1.jpg, poster_2.jpg, etc.
```

**Features:**
- Auto-creates parent directories if needed
- Collision avoidance: if file exists, adds `_1`, `_2`, etc.
- Use `/tmp/` for temporary images that will be uploaded elsewhere

## API Configuration

Create `scripts/.env`:
```
GEMINI_API_KEY=your_gemini_api_key
FAL_KEY=your_fal_api_key
XAI_API_KEY=your_xai_api_key
```

## Hebrew/RTL Content

**IMPORTANT:** When the image contains Hebrew text, you MUST add the following sentence to the prompt:

```
"CRITICAL: Layout is RTL (right-to-left). All text in Hebrew. Visual flow, reading order, and panel sequence go from RIGHT to LEFT."
```

Copy this exact sentence and paste it at the BEGINNING of your prompt. Without it, the image will render left-to-right which is wrong for Hebrew content.

## WOW Mode

When user asks for "wow mode" or wants maximum visual impact, add these epic elements to the prompt:

```
"EPIC CINEMATIC WOW: Amazed expression, mind-blown reaction, intense VFX - shattered glass particles, explosive energy bursts, volumetric light rays, dramatic lens flares, particle explosions, motion blur streaks, holographic glitches, electric sparks, cinematic color grading, dramatic rim lighting, depth of field bokeh, anamorphic lens effects. Maximum visual spectacle."
```

## Output

- Files saved to path specified by `-d` flag (MANDATORY)
- Aspect ratio: Configurable via `--aspect` (default: 3:2)
- Quality: 1K (1024px on longest edge)

---

# Video Generation

Generate videos using xAI Grok Imagine Video (default) or fal.ai LTX-2 (cheap mode).

## Quick Start

```bash
cd ~/.claude/skills/image-generation/scripts

# Text-to-video (Grok Imagine - high quality, 720p)
npx tsx generate_video.ts -d /tmp/video.mp4 "A futuristic city at sunset, cinematic drone shot"

# Cheap mode: fal.ai LTX-2 (fast, low cost)
npx tsx generate_video.ts --cheap -d /tmp/video.mp4 "A futuristic city at sunset"

# Image-to-video (animate a still image)
npx tsx generate_video.ts -d /tmp/animated.mp4 --image /path/to/image.jpg "Slow zoom with particles floating"
npx tsx generate_video.ts --cheap -d /tmp/animated.mp4 --image /path/to/image.jpg "Gentle camera movement"

# Custom duration and aspect ratio
npx tsx generate_video.ts -d /tmp/long.mp4 -t 10 -a 9:16 "Vertical video for stories"
```

## Video Providers

| Provider | Flag | Quality | Duration | Resolution | Cost |
|----------|------|---------|----------|------------|------|
| **Grok Imagine** | (default) | High, cinematic | 1-15s | 480p/720p | Per-second billing |
| **fal.ai LTX-2** | `--cheap` | Good, fast | 1-10s | ~480p | Budget-friendly |

## Video Options

| Option | Flag | Default | Description |
|--------|------|---------|-------------|
| Prompt | (positional) | required | Text description of the video |
| Destination | `-d` | required | Output file path (.mp4) |
| Duration | `-t` | 5 | Duration in seconds |
| Aspect ratio | `-a` | 16:9 | 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3 |
| Resolution | `-r` | 720p | 480p or 720p (Grok only) |
| Image source | `--image` | none | Source image for image-to-video |
| Cheap mode | `--cheap` | false | Use LTX-2 instead of Grok |
