---
name: generate-image
description: AI image generation via Gemini. Use when the user wants to generate, create, or make an image, or when you need to create visual assets like logos, diagrams, or illustrations. Requires GEMINI_API_KEY or GOOGLE_API_KEY.
---

# generate-image - AI Image Generation

Uses Google Gemini to generate images from text prompts.

## Synopsis

```
codev generate-image "<prompt>" [options]
```

Note: this is a `codev` subcommand, not standalone.

## All flags

```
-o, --output <file>        Output file path (default: output.png)
-r, --resolution <res>     Resolution: 1K, 2K, 4K (default: 1K)
-a, --aspect <ratio>       Aspect ratio (default: 1:1)
--ref <image>              Reference image (repeatable, max 14)
```

## Aspect ratios

`1:1` | `16:9` | `9:16` | `3:4` | `4:3` | `3:2` | `2:3`

## Examples

```bash
codev generate-image "A sunset over mountains"
codev generate-image "A futuristic city" -r 4K -a 16:9 -o city.png
codev generate-image "Same style but with cats" --ref style.png --ref layout.png
codev generate-image prompt.txt -o result.png    # Prompt from .txt file
```

## Notes

- Prompt must be quoted if it contains spaces
- Prompt can be a `.txt` file path (auto-detected by extension)
- Reference images must exist on disk
- Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable
