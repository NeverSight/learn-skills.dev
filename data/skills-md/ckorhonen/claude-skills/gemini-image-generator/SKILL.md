---
name: gemini-image-generator
description: Generate images using Google's Gemini API. Use when creating images from text prompts, editing existing images, or combining reference images for AI-generated visual content.
---

# Gemini Image Generator

## Overview

Generate images using Google's Gemini API with support for text-to-image generation, image editing, and multi-image reference inputs. Supports both the fast Gemini 2.5 Flash model and the high-quality Gemini 3 Pro model with up to 4K resolution.

## When to Use

- Generating app icons, logos, and UI assets
- Creating marketing visuals and promotional graphics
- Prototyping UI designs with AI-generated placeholders
- Generating game sprites and 2D assets
- Creating concept art and mood boards
- Editing or modifying existing images with text prompts
- Style transfer using reference images

## Prerequisites

- Python 3.9+
- `google-genai` package
- `GEMINI_API_KEY` environment variable

## Installation

```bash
pip install google-genai
```

### Getting an API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and set it as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) for persistence:

```bash
echo 'export GEMINI_API_KEY="your-api-key"' >> ~/.zshrc
```

## Quick Start

Generate a simple image:

```bash
python scripts/generate_image.py -p "A fluffy orange cat sitting on a windowsill, warm sunlight, cozy atmosphere"
```

Generate with specific aspect ratio:

```bash
python scripts/generate_image.py -p "Modern tech startup banner" -a 16:9 -o banner.png
```

Edit an existing image:

```bash
python scripts/generate_image.py -p "Make the sky more dramatic with sunset colors" -i photo.jpg -o edited.png
```

## Command Reference

```
python scripts/generate_image.py [options]

Required:
  -p, --prompt TEXT         Text prompt describing the image

Optional:
  -o, --output PATH         Output file path (default: auto-generated)
  -m, --model MODEL         Model to use (default: gemini-3-pro-image-preview)
  -a, --aspect-ratio RATIO  Aspect ratio (default: 1:1)
  -s, --size SIZE           Image size: 1K, 2K, 4K (default: 1K, Pro only)
  -i, --input-image PATH    Input image for editing mode
  -r, --reference-images    Reference image(s), can be repeated (max 14)
  -v, --verbose             Show detailed progress
```

## Models

| Model | Resolution | Best For |
|-------|------------|----------|
| `gemini-3-pro-image-preview` | Up to 4K | Final assets, high quality, professional work |
| `gemini-2.5-flash-image` | 1024px | Quick iterations, prototyping, batch generation |

The Pro model is used by default. Use the Flash model for faster generation when quality is less critical:

```bash
python scripts/generate_image.py -p "Quick concept sketch" -m gemini-2.5-flash-image
```

## Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| `1:1` | App icons, profile pictures, thumbnails |
| `2:3` | Portrait photos, book covers |
| `3:2` | Landscape photos, postcards |
| `3:4` | Portrait photos, social media posts |
| `4:3` | Traditional photos, presentations |
| `4:5` | Instagram posts, portrait social media |
| `5:4` | Large format prints |
| `9:16` | Stories, vertical videos, mobile wallpapers |
| `16:9` | Widescreen banners, video thumbnails, headers |
| `21:9` | Ultrawide banners, cinematic headers |

## Image Sizes

Available for Gemini 3 Pro model only:

| Size | Resolution | Use Case |
|------|------------|----------|
| `1K` | 1024px | Web graphics, thumbnails |
| `2K` | 2048px | Print materials, detailed graphics |
| `4K` | 4096px | High-resolution prints, large displays |

```bash
python scripts/generate_image.py -p "Detailed landscape" -s 4K -o landscape_4k.png
```

## Prompt Engineering Guide

### Prompt Structure

Use this formula for effective prompts:

```
[Subject] + [Style] + [Details] + [Quality modifiers]
```

### Techniques

**1. Be Specific About the Subject**

```
Bad:  "a cat"
Good: "a fluffy orange tabby cat sitting on a windowsill"
```

**2. Specify Art Style**

- Photorealistic, cartoon, anime, oil painting, watercolor
- Digital art, 3D render, pixel art, vector illustration
- Specific styles: "in the style of Studio Ghibli", "cyberpunk aesthetic"

**3. Include Environment and Lighting**

- "golden hour lighting", "dramatic shadows", "soft ambient light"
- "neon-lit cityscape", "cozy interior", "misty forest"

**4. Add Quality Modifiers**

- "high quality", "detailed", "professional"
- "sharp focus", "studio lighting", "cinematic"

**5. Specify Composition**

- "centered composition", "rule of thirds"
- "close-up", "wide shot", "bird's eye view", "isometric"

### Example Prompts by Use Case

**App Icon**
```
Minimalist app icon for a weather app, blue gradient background,
white cloud with golden sun rays, flat design, rounded corners,
iOS style, clean and modern
```

**Marketing Banner**
```
Professional tech startup banner, abstract geometric shapes
flowing from left to right, purple and blue gradient,
modern and clean aesthetic, corporate style
```

**Game Sprite**
```
Pixel art character sprite, fantasy warrior with glowing sword,
32x32 style, transparent background, retro 16-bit game aesthetic,
vibrant colors
```

**Product Photo**
```
Professional product photo of wireless earbuds on white background,
soft shadows, studio lighting, minimalist composition,
commercial photography style
```

**Concept Art**
```
Futuristic city skyline at sunset, flying vehicles between
towering skyscrapers, neon lights reflecting on wet streets,
cyberpunk atmosphere, cinematic composition, detailed
```

**UI Mockup Asset**
```
Abstract gradient background for mobile app, soft purple to pink
transition, subtle geometric patterns, modern and minimal,
suitable for dark text overlay
```

## Generation Modes

### Text-to-Image

Generate images from text descriptions:

```bash
python scripts/generate_image.py -p "Your description here" -o output.png
```

### Image Editing

Modify an existing image with a text prompt:

```bash
python scripts/generate_image.py \
  -p "Change the background to a tropical beach at sunset" \
  -i original.jpg \
  -o edited.png
```

### Multi-Image Reference

Use up to 14 reference images to guide style or content:

```bash
python scripts/generate_image.py \
  -p "Create a new character in this art style" \
  -r style_ref1.png \
  -r style_ref2.png \
  -o new_character.png
```

## Examples

### Generate App Icons

```bash
# iOS-style weather icon
python scripts/generate_image.py \
  -p "Minimalist weather app icon, blue sky gradient, white fluffy cloud, sun peeking out, flat design, rounded square, iOS 17 style" \
  -a 1:1 \
  -o weather_icon.png

# Fitness app icon
python scripts/generate_image.py \
  -p "Fitness app icon, running figure silhouette, orange to red gradient background, energetic and dynamic, modern flat design" \
  -a 1:1 \
  -o fitness_icon.png
```

### Create Marketing Assets

```bash
# Website hero banner
python scripts/generate_image.py \
  -p "Abstract tech hero banner, flowing data visualization, dark blue background with glowing cyan accents, futuristic and professional" \
  -a 21:9 \
  -s 2K \
  -o hero_banner.png

# Social media post
python scripts/generate_image.py \
  -p "Motivational quote background, soft sunrise gradient, minimalist mountain silhouette, peaceful and inspiring" \
  -a 4:5 \
  -o social_post_bg.png
```

### Generate Game Assets

```bash
# Character sprite
python scripts/generate_image.py \
  -p "Pixel art hero character, knight with blue cape and silver armor, idle pose, transparent background, 16-bit retro style" \
  -a 1:1 \
  -o knight_sprite.png

# Environment tile
python scripts/generate_image.py \
  -p "Grass tile for top-down RPG, seamless pattern, vibrant green with small flowers, pixel art style, 32x32 aesthetic" \
  -a 1:1 \
  -o grass_tile.png
```

### Edit Photos

```bash
# Change background
python scripts/generate_image.py \
  -p "Replace background with a cozy coffee shop interior" \
  -i portrait.jpg \
  -o portrait_coffee_shop.png

# Style enhancement
python scripts/generate_image.py \
  -p "Enhance with dramatic cinematic color grading, increase contrast, add film grain" \
  -i landscape.jpg \
  -o landscape_cinematic.png
```

## Troubleshooting

### "GEMINI_API_KEY environment variable not set"

Set your API key:
```bash
export GEMINI_API_KEY="your-api-key"
```

### "Rate limit exceeded"

Wait a few minutes and try again. For batch operations, add delays between requests.

### "Content policy violation"

Modify your prompt to avoid content that violates Google's usage policies. Try:
- Using more generic descriptions
- Avoiding specific brand names or copyrighted characters
- Removing potentially sensitive content

### "No image in response"

The model sometimes returns text instead of an image. Try:
- Making your prompt more specific
- Adding "generate an image of" to your prompt
- Using a different aspect ratio

### "Unsupported image format"

Supported formats for input images: PNG, JPEG, WebP

### Size option not working

The size option (2K, 4K) is only available for `gemini-3-pro-image-preview`. The Flash model always generates 1024px images.

## Best Practices

- **Start simple**: Begin with clear, concise prompts and iterate
- **Use the right model**: Flash for speed, Pro for quality
- **Match aspect ratio to use case**: 16:9 for banners, 1:1 for icons
- **Save high-quality versions**: Use 4K when you need detailed assets
- **Iterate on prompts**: Small changes can significantly affect results
- **Use reference images**: For consistent style across multiple generations
- **Add quality modifiers**: "high quality", "detailed", "professional"
- **Specify what you don't want**: "no text", "simple background", "no people"
