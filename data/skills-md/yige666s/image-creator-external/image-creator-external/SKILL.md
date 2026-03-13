---
name: image-creator-external
description: "Generate images from text or reference images using ShortArt AI. ALWAYS use this skill when users mention: creating images, drawing, generating pictures, visualizing ideas, making artwork, image generation, or any visual content creation from text descriptions or reference photos. Also trigger on: 生成图片, 画一张, 帮我画, 制作图片, generate image, create image, draw, visualize, 图片生成, 文生图, 创作图像, image generation, make a picture, 以图生图, 修改图片, 编辑图片, Edit Image, image-to-image. Use this skill proactively whenever image creation is mentioned, even if the user doesn't explicitly ask for it."
allowed-tools: Bash(python3 *)
metadata: {"openclaw": {"emoji": "🎨"}}
---

# Image Creator

Generate images using ShortArt backend API, supporting text-to-image and image-to-image.

## Authentication Setup (Required for First Use)

image-creator requires a ShortArt API Key. There are two ways to configure it:

### Method 1: OpenClaw Config (Recommended)

Add it to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "image-creator-external": {
        "env": { "SHORTART_API_KEY": "paste_your_api_key_here" }
      }
    }
  }
}
```

### Method 2: Shell Environment Variable

Add to `~/.zshrc` (or `~/.bashrc` for bash):

```bash
export SHORTART_API_KEY="paste_your_api_key_here"
```

Then reload: `source ~/.zshrc`

> You can obtain the API Key from the ShortArt console.
>
> **Note for LLM**: When executing scripts, if API key is not found, try running with `source ~/.zshrc && python3 scripts/impl.py ...` to load environment variables from shell config.

## Parameter Quick Reference

| Parameter | Options | Default |
|------|------|------|
| `--model` | `seedream4.5` \| `nano-banana-pro` \| `nano-banana-2` | `nano-banana-pro` |
| `--count` | 1-4 | 1 |
| `--resolution` | `1k` \| `2k` \| `4k` (nano-banana-2 also supports `0.5k`) | `2k` |
| `--aspect-ratio` | `1:1` \| `16:9` \| `9:16` \| `1:1` |

## Execution Method

**IMPORTANT**: Always prefix commands with `source ~/.zshrc &&` to load environment variables.

Generate images by calling `scripts/impl.py`:

```bash
source ~/.zshrc && python3 scripts/impl.py "<prompt>" \
  --model {ModelName} \
  --count {Count} \
  --resolution {Resolution} \
  --aspect-ratio {AspectRatio}
```

**Image-to-image** (with reference image):

```bash
# Use existing OSS path
source ~/.zshrc && python3 scripts/impl.py "<prompt>" --image "images/20260121/.../filename.jpg"

# Upload local image
source ~/.zshrc && python3 scripts/impl.py "<prompt>" --upload /path/to/local/image.jpg
```

## Return Result

```json
{
  "status": "success",
  "project_id": "{projectId}",
  "credit": "{credit}",
  "sub_credit": "{subCredit}",
  "consumed_credit": "{consumedCredit}",
}
```

## Workflow

1. **Understand Requirements** — Confirm subject, style, dimensions, quantity
2. **Optimize Prompt** — Refer to [references/prompt-guide.md](references/prompt-guide.md) to expand description
3. **Select Parameters** — Choose model / resolution / aspectRatio based on use case
4. **Execute Script** — Run `scripts/impl.py` to get `project_id`, if failed with returned error, retry a maximum of two times
5. **Display Results** — Inform user that task is submitted

Task is asynchronous. After submission, `project_id` is returned immediately, and images are generated in the background.

## Reference Files

- **API Parameters & Response Format** → [references/api.md](references/api.md)
- **Prompt Writing Templates** → [references/prompt-guide.md](references/prompt-guide.md)
