---
name: z-image
description: ModelScope Z-Image-Turbo text-to-image generation with 24+ visual style presets, auto style detection, and CLI support
license: MIT
metadata:
  version: 1.0.0
  model: Tongyi-MAI/Z-Image-Turbo
  api: ModelScope Inference API
---

# Z-Image - ModelScope 通义万相图片生成

统一的 Z-Image-Turbo 文生图能力，内置 24+ 种视觉风格模板，支持自动风格检测。

## Quick Start

```bash
# 基础文生图
python ~/.claude/skills/z-image/scripts/generate.py "一个程序员在深夜写代码"

# 指定风格
python ~/.claude/skills/z-image/scripts/generate.py "武侠少年仗剑天涯" --style anime_shonen

# 自动检测风格
python ~/.claude/skills/z-image/scripts/generate.py "纳瓦尔的智慧哲学" --auto-style

# 批量生成
python ~/.claude/skills/z-image/scripts/generate.py prompts.txt --batch --style neon_wisdom

# 列出所有风格
python ~/.claude/skills/z-image/scripts/generate.py --list-styles
```

## Triggers

- `生成图片` / `生图` / `做图`
- `z-image generate`
- `用万相生成`
- `text to image`
- `generate image with style`

## Quick Reference

| Feature | Detail |
|---------|--------|
| API | ModelScope `api-inference.modelscope.cn` |
| Model | `Tongyi-MAI/Z-Image-Turbo` |
| Cost | ~$0.01/image |
| Styles | 24+ presets in 7 categories |
| Auto-detect | Keyword chain + LLM fallback |
| Output | PNG, 1024x1024 default |
| Async | Submit + poll pattern |

## How It Works

```
用户输入 (prompt + style)
    │
    ▼
┌─────────────────────────────┐
│ 1. Style Resolution         │
│  • 指定风格 → 直接使用       │
│  • --auto-style → 检测链     │
│    Keyword → LLM fallback   │
│  • 默认 → anime_japanese    │
├─────────────────────────────┤
│ 2. Prompt Enhancement       │
│  • base_style + colors      │
│  • lighting + modifiers     │
│  • negative prompt          │
├─────────────────────────────┤
│ 3. API Call (Async)         │
│  • POST /v1/images/gen      │
│  • Poll task status         │
│  • Download result          │
├─────────────────────────────┤
│ 4. Post-processing          │
│  • Resize to target         │
│  • Save to output dir       │
└─────────────────────────────┘
```

## Style Categories

| Category | Styles | Best For |
|----------|--------|----------|
| **Anime** (5) | anime_japanese, anime_chibi, anime_shonen, anime_iyashikei, anime_cyberpunk | 故事/角色/动漫内容 |
| **Neon** (6) | neon_wisdom, neon_tech, neon_wealth, neon_contrast, neon_timeline, neon_mindmap | 知识/商业/哲理内容 |
| **Tech** (2) | tech_dark, tech_light | 科技/产品展示 |
| **Documentary** (3) | documentary, vintage_50s, vintage_80s | 传记/历史/纪录片 |
| **Art** (3) | watercolor, ink_chinese, comic_style | 艺术/文化内容 |
| **Minimal** (2) | minimal_white, flat_design | 简约/解释类内容 |
| **Mood** (2) | warm_cozy, dark_dramatic | 氛围/情感内容 |

## Commands

| Command | Description |
|---------|-------------|
| `generate.py "prompt"` | 生成单张图片 |
| `generate.py "prompt" --style X` | 指定风格生成 |
| `generate.py "prompt" --auto-style` | 自动检测风格 |
| `generate.py prompts.txt --batch` | 批量生成 |
| `generate.py --list-styles` | 列出所有风格 |
| `generate.py --list-styles --category anime` | 按分类列出 |
| `generate.py "prompt" --size 1920x1080` | 指定尺寸 |
| `generate.py "prompt" --output ./my-images/` | 指定输出目录 |

## Configuration

API Key 配置优先级：
1. `--api-key` 命令行参数
2. `MODELSCOPE_API_KEY` 环境变量
3. `~/.claude/skills/z-image/config/secrets.md` 文件

```bash
# 方式1: 环境变量
export MODELSCOPE_API_KEY="ms-xxxxx"

# 方式2: 配置文件
echo "API_KEY=ms-xxxxx" > ~/.claude/skills/z-image/config/secrets.md
```

## Scripts

### `scripts/generate.py` - CLI 入口

主要的图片生成脚本，支持单张和批量模式。

```bash
# 单张生成
python scripts/generate.py "赛博朋克城市夜景" --style anime_cyberpunk --output ./output/

# 批量生成（从文件读取 prompt）
python scripts/generate.py prompts.txt --batch --style neon_tech

# 自动风格检测
python scripts/generate.py "纳瓦尔谈财富自由" --auto-style
```

Exit codes: 0=success, 1=failure, 10=API error, 11=style not found

### `scripts/style_templates.py` - 风格模板库

24+ 种视觉风格定义和自动检测逻辑。可独立导入使用：

```python
from style_templates import get_style_prompt, auto_detect_style, STYLES

# 获取增强后的 prompt
enhanced = get_style_prompt("一个少年在山顶", "anime_shonen")

# 自动检测风格
style = auto_detect_style("纳瓦尔的智慧与幸福哲学")  # → "neon_wisdom"

# 列出所有风格
for sid, s in STYLES.items():
    print(f"{sid}: {s.name} - {s.description}")
```

## Integration

其他 skill 可以直接调用 z-image：

```python
import sys
sys.path.insert(0, str(Path.home() / ".claude/skills/z-image/scripts"))
from generate import ZImageClient

client = ZImageClient(api_key="ms-xxx")
result = await client.generate("prompt", style="neon_wisdom")
print(result)  # 图片路径
```

## Dependent Skills

以下 skill 依赖 z-image 能力：

| Skill | Usage |
|-------|-------|
| video-skill | 视频封面和帧图生成 |
| image-fenjing | 分镜图片生成 |
| videofree | Profile-based 视频图片 |
| voice-first-video | 语音视频配图 |
| novel-to-video | 网文转视频插图 |
| hunhe-video | 混合视频图片生成 |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| 硬编码 API Key | 安全风险 | 用环境变量或 secrets.md |
| 跳过风格增强 | 生成质量差 | 始终使用 style template |
| 同步等待 API | 阻塞进程 | 用 async + polling |
| 忽略 negative prompt | 出现瑕疵 | 每个风格都有专属 negative |

## Verification

- [ ] `python scripts/generate.py --list-styles` 输出 24+ 种风格
- [ ] `python scripts/generate.py "test" --dry-run` 输出增强后的 prompt
- [ ] API Key 配置正确（环境变量或 secrets.md）
- [ ] 生成图片保存到指定目录
