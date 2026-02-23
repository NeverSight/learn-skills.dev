---
name: qwen-image
description: Generate images using Qwen Image API (Alibaba Cloud DashScope). Use when users request image generation with Chinese prompts or need high-quality AI-generated images from text descriptions.
homepage: https://dashscope.aliyuncs.com/
metadata: {"openclaw":{"emoji":"🎨","requires":{"bins":["uv"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Qwen Image

Generate high-quality images using Alibaba Cloud's Qwen Image API (通义万相).

## Usage

Generate an image (returns URL only):
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "一副典雅庄重的对联悬挂于厅堂之中" --size "1664*928" --api-key sk-xxx
```

Generate and save locally:
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "一副典雅庄重的对联悬挂于厅堂之中" --size "1664*928" --api-key sk-xxx
```

With custom model:
Support `qwen-image-max-2025-12-30` `qwen-image-plus-2026-01-09` `qwen-image-plus`
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "a beautiful sunset over mountains" --model qwen-image-plus-2026-01-09 --api-key sk-xxx
```

## API Key
You can obtain the API key and run the image generation command in the following order.

- Get apiKey from `models.providers.bailian.apiKey` in `~/.openclaw/openclaw.json`
- Or get from `skills."qwen-image".apiKey` in `~/.openclaw/openclaw.json`
- Or get from `DASHSCOPE_API_KEY` environment variable
- Or Get your API key from: https://dashscope.console.aliyun.com/

## Options
**Sizes:**
- `1664*928` (default) - 16:9 landscape
- `1024*1024` - Square format
- `720*1280` - 9:16 portrait
- `1280*720` - 16:9 landscape (smaller)

**Additional flags:**
- `--negative-prompt "unwanted elements"` - Specify what to avoid
- `--no-prompt-extend` - Disable automatic prompt enhancement
- `--watermark` - Add watermark to generated image
- `--no-verify-ssl` - Disable SSL certificate verification (use when behind corporate proxy)

## Workflow

1. Execute the generate_image.py script with the user's prompt
2. Parse the script output and find the line starting with `MEDIA_URL:`
3. Extract the image URL from that line (format: `MEDIA_URL: https://...`)
4. Display the image to the user using markdown syntax: `![Generated Image](URL)`
5. Do NOT download or save the image unless the user specifically requests it

## Notes

- Supports both Chinese and English prompts
- By default, returns image URL directly without downloading
- The script prints `MEDIA_URL:` in the output - extract this URL and display it using markdown image syntax: `![generated image](URL)`
- Always look for the line starting with `MEDIA_URL:` in the script output and render the image for the user
- Default negative prompt helps avoid common AI artifacts
- Images are hosted on Alibaba Cloud OSS with temporary access URLs
