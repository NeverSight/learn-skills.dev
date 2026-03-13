---
name: seedream
description: 使用火山引擎 Seedream-4.5 API 生成高质量图片。适用于文生图、图生图以及生成关联组图的场景。
---

# Seedream

本 Skill 封装了火山引擎（Volcengine）的 Seedream-4.5 图片生成能力，支持通过文本提示词或参考图生成高质量 AI 图像。

## 使用方法

### 文生图
生成单张图片（默认分辨率）：
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "一只赛博朋克风格的猫" --api-key YOUR_API_KEY
```

指定分辨率（如 2K, 4K 或具体像素）：
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "壮丽的山川日出" --size "2K" --api-key YOUR_API_KEY
```

### 图生图
提供参考图片 URL：
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "将其风格变为印象派" --image "https://example.com/input.jpg" --api-key YOUR_API_KEY
```

### 生成组图
生成一组内容关联的图片（最多 15 张）：
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "一个宇航员在不同行星上的探险经历" --sequential --max-images 4 --api-key YOUR_API_KEY
```

## API Key 配置

可以通过以下方式提供 API Key：
1. 命令行参数 `--api-key`
2. 环境变量 `VOLC_API_KEY`

## 参数说明

- `--prompt`: (必选) 图像生成的文本描述。
- `--model`: (可选) 模型 ID，默认为 `doubao-seedream-4-5-251128`。
- `--size`: (可选) 图像尺寸。支持 `2K`, `4K` 或 `2048x2048` 等格式。
- `--image`: (可选) 参考图 URL 或 Base64 编码。
- `--sequential`: (可选) 开启组图生成功能。
- `--max-images`: (可选) 组图生成的最大图片数量（1-15）。

## 工作流

1. 调用 `generate_image.py` 脚本。
2. 脚本会输出以 `MEDIA_URL: ` 开头的图片链接。
3. 提取链接并使用 Markdown 语法展示：`![Generated Image](URL)`。
4. 除非用户要求，否则无需下载图片。

## 注意事项

- Seedream-4.5 支持中英文提示词。
- 组图功能仅在 Seedream-4.5/4.0 模型中有效。
- 确保提供的图片 URL 可公开访问。
