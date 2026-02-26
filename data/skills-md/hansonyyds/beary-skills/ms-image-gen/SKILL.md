---
name: ms-image-gen
description: "AI image generation using ModelScope API. Use when user requests to generate, create, draw, paint, or make images through natural language. Supports Chinese and English prompts. Handles async API tasks, batch generation, and automatic configuration management."
---

# ModelScope Image Generation

Generate AI images through ModelScope API with natural language support in Chinese and English.

## Quick Start

Generate an image directly:

```bash
python "${SKILL_ROOT}/scripts/image-gen.py" --prompt "A golden cat sitting on velvet"
```

Or with Chinese:

```bash
python "${SKILL_ROOT}/scripts/image-gen.py" --prompt "一只金色的猫坐在天鹅绒垫子上"
```

## Natural Language Triggers

This skill automatically activates when users say:

**Chinese:**
- "生成[描述]" - Generate [description]
- "画一个[描述]" - Draw a [description]
- "创建一张[描述]图片" - Create a [description] image
- "帮我画..." - Help me draw...
- "AI绘画..." - AI art...

**English:**
- "Generate [description]"
- "Draw a [description]"
- "Create a [description] image"
- "Make a picture of..."
- "Create an image of..."

## Configuration

### Setup API Token

Before generating images, configure your ModelScope API token:

1. Create config directory: `~/.modelscope-image-gen/`
2. Create `modelscope-image-gen.local.md`:

```yaml
---
api_key: your_modelscope_api_token_here
default_model: Tongyi-MAI/Z-Image-Turbo
default_width: 1024
default_height: 1024
poll_timeout: 300
output_dir: ./generated-images/
---
```

### Getting API Token

Visit [ModelScope](https://modelscope.cn/) to get your API token.

## Usage

### Single Image Generation

```bash
python "${SKILL_ROOT}/scripts/image-gen.py" \
  --prompt "A sunset over mountains" \
  --output ./generated-images/
```

### Batch Generation

Create a prompts file (one per line):

```bash
python "${SKILL_ROOT}/scripts/image-gen.py" \
  --batch examples/batch-prompts.txt \
  --output ./generated-images/
```

### Custom Parameters

```bash
python "${SKILL_ROOT}/scripts/image-gen.py" \
  --prompt "Futuristic city at night" \
  --model Tongyi-MAI/Z-Image-Turbo \
  --width 1024 \
  --height 1024 \
  --filename city-night \
  --timeout 300
```

### Multiple Images

```bash
python "${SKILL_ROOT}/scripts/image-gen.py" \
  --prompt "Abstract art" \
  --count 5 \
  --output ./generated-images/
```

## Script Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--prompt` | string | Yes* | Image generation prompt (required unless using --batch) |
| `--batch` | file | No | Batch prompts file (one per line) |
| `--model` | string | No | Model ID (default: from config or Tongyi-MAI/Z-Image-Turbo) |
| `--output` | path | No | Output directory (default: ./generated-images/) |
| `--filename` | string | No | Output filename without extension |
| `--width` | int | No | Image width (default: 1024) |
| `--height` | int | No | Image height (default: 1024) |
| `--count` | int | No | Number of images to generate (default: 1) |
| `--timeout` | int | No | Polling timeout in seconds (default: from config or 300) |

## How It Works

### Async Task Flow

1. **Submit Request**: POST to `/v1/images/generations` with async mode
2. **Poll Status**: GET `/v1/tasks/{task_id}` until completion
3. **Download**: Retrieve image from result URL

### Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError` | Config missing | Run setup to create config file |
| `401 Unauthorized` | Invalid API token | Check `api_key` in config |
| `429 Rate Limit` | Too many requests | Wait and retry |
| `TimeoutError` | Task too long | Increase `poll_timeout` |

## Examples

See `examples/batch-prompts.txt` for sample prompts to use with batch generation.

## Best Practices

1. **Validate prompts** before submission to avoid wasted API calls
2. **Use batch mode** for multiple generations to optimize throughput
3. **Set appropriate timeouts** based on prompt complexity
4. **Save images immediately** after successful generation
5. **Handle rate limits** with proper retry strategies
