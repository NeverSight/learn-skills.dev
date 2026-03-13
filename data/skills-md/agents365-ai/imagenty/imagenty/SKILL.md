---
name: imagenty
description: Use when generating images with Alibaba Cloud Bailian API, especially for Chinese text rendering or photorealistic images
author: Agents365-ai
created: 2024-12-01
updated: 2025-02-21
---

# ImagenTY - Alibaba Cloud Bailian Text-to-Image Skill

## Overview

Generate images using Alibaba Cloud Bailian API. **Default endpoint is China region**.

Supports two model families:
- **Qwen-Image**: Excellent at rendering complex Chinese/English text
- **Wan Series**: Photorealistic images and photography-grade visuals

**Cross-platform support**: Windows, macOS, Linux

## When to Use This Skill

Automatically activate this skill when:
- User requests image generation with Chinese text or calligraphy
- Need photorealistic images or photography-style visuals
- Creating commercial posters, illustrations, or digital art
- User explicitly requests Alibaba Cloud / Bailian / Qwen / Wan models
- Any task where AI-generated image with strong Chinese support would be helpful

## Models

### Qwen-Image - Text Rendering Specialist

| Model | Description |
|-------|-------------|
| `qwen-image-plus` | **Default**. Best for Chinese/English text, posters, illustrations |

### Wan Series - Photorealistic Generation

| Model | Description |
|-------|-------------|
| `wan2.6-t2i` | **Recommended**. Latest version, flexible sizing |
| `wan2.5-t2i-preview` | High quality, up to 768x2700 |
| `wan2.2-t2i-flash` | Speed-optimized |
| `wan2.2-t2i-plus` | Professional tier |
| `wanx2.1-t2i-turbo` | Fast execution |
| `wanx2.1-t2i-plus` | Professional tier |
| `wanx2.0-t2i-turbo` | Earlier generation |

## Usage

### Basic Usage

```bash
# Default model (qwen-image-plus)
python ~/.claude/skills/imagenty/scripts/generate_image.py "A cute cat" output.png

# Photorealistic with Wan model
python ~/.claude/skills/imagenty/scripts/generate_image.py --model wan2.6-t2i "Realistic photo of mountains at sunset" photo.png
```

### Size Options

```bash
# Use ratio preset
python ~/.claude/skills/imagenty/scripts/generate_image.py --size 16:9 "Wide landscape" landscape.png

# Use exact dimensions
python ~/.claude/skills/imagenty/scripts/generate_image.py --size 1280*720 "Custom size" custom.png
```

### Size Presets

**Qwen-Image:**
- `16:9` -> 1664x928
- `9:16` -> 928x1664
- `1:1` -> 1024x1024
- `4:3` -> 1216x912
- `3:4` -> 912x1216

**Wan Series:**
- `1:1` -> 1024x1024
- `1:1-large` -> 1280x1280
- `16:9` -> 1280x720
- `9:16` -> 720x1280
- `4:3` -> 1200x900
- `3:4` -> 900x1200
- `2:1` -> 1440x720

### Advanced Options

```bash
# With negative prompt
python ~/.claude/skills/imagenty/scripts/generate_image.py --negative "blurry, low quality" "High quality portrait" portrait.png

# List all models
python ~/.claude/skills/imagenty/scripts/generate_image.py --list-models
```

## Requirements

```bash
pip install dashscope requests
```

## Environment Variables

```bash
# Required - Alibaba Cloud Bailian API Key
export DASHSCOPE_API_KEY="your_api_key"

# Optional - Set default model
export DASHSCOPE_MODEL="wan2.6-t2i"

# Optional - Set API endpoint (default: China)
export DASHSCOPE_API_BASE="cn"  # or full URL
```

Get API Key: https://bailian.console.aliyun.com/

## API Endpoints

| Region | Alias | URL |
|--------|-------|-----|
| **China** (default) | `cn` | `https://dashscope.aliyuncs.com/api/v1` |
| Singapore | `sg` | `https://dashscope-intl.aliyuncs.com/api/v1` |
| Virginia | `us` | `https://dashscope-us.aliyuncs.com/api/v1` |

```bash
# Switch to Singapore endpoint
export DASHSCOPE_API_BASE="sg"

# Or use full URL
export DASHSCOPE_API_BASE="https://dashscope-intl.aliyuncs.com/api/v1"
```

## Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| Chinese text/calligraphy | `qwen-image-plus` |
| English text on images | `qwen-image-plus` |
| Posters with typography | `qwen-image-plus` |
| Photorealistic photos | `wan2.6-t2i` |
| Portrait photography | `wan2.6-t2i` |
| Fast generation | `wan2.2-t2i-flash` |
| High quality art | `wan2.5-t2i-preview` |

## Comparison with Imagen (Gemini)

| Feature | ImagenTY (Bailian) | Imagen (Gemini) |
|---------|-------------------|-----------------|
| Chinese text rendering | Excellent | Good |
| English text rendering | Excellent | Good |
| Photorealistic images | Excellent | Good |
| Speed | Medium | Fast |
| Model variety | 8 models | 3 models |
| Max resolution | 1440x1440 | 2K |

## Examples

### Chinese New Year Poster
```bash
python ~/.claude/skills/imagenty/scripts/generate_image.py \
  "A beautiful Chinese New Year poster with red background, golden text, fireworks and firecrackers" \
  new_year_poster.png
```

### Photorealistic Landscape
```bash
python ~/.claude/skills/imagenty/scripts/generate_image.py \
  --model wan2.6-t2i \
  --size 16:9 \
  "Breathtaking sunset over mountain range, golden hour, professional photography" \
  landscape.png
```

### Product Shot
```bash
python ~/.claude/skills/imagenty/scripts/generate_image.py \
  --model wan2.6-t2i \
  "Professional product photography of a coffee cup on marble surface, studio lighting" \
  product.png
```
