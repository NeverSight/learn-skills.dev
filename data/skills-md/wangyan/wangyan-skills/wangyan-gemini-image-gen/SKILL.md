---
name: wangyan-gemini-image-gen
description: >-
  Generate, edit, and compose images using Gemini models. Activate when user asks to generate images, draw, create logos/posters/icons/banners, edit/modify photos, combine images, or any image creation task.
  画图、生成图片、做图、P图、修图、合成图、做logo、做海报、做图标、做封面、品牌视觉、Nano Banana、Banana。

metadata:
  openclaw:
    emoji: "🎨"
    category: creative
    homepage: "https://github.com/wangyan/wangyan-skills"
    requires:
      bins:
        - python3
        - uv
      env:
        - GEMINI_API_KEY
        - GEMINI_BASE_URL
    primaryEnv: GEMINI_API_KEY
    tags:
      - image-generation
      - image-editing
      - image-composition
      - text-to-image
      - logo-design
      - poster-design
      - brand-visual
      - gemini
      - nano-banana
      - nano-banana-pro
      - openai-compatible

---

# Gemini Image Generator

通过 `Nano Banana` 实现文生图、图片编辑与多图合成，支持 OpenAI 兼容和 Google 原生两种 API 格式，可自定义端点和密钥。

---

## 🎯 触发判断

1. **触发词**：画图、生成图片、做logo/海报/图标/封面、P图、修图、合成图、draw/generate/create image/logo/banner  
2. **不触发**：图片分析、OCR、格式转换、图片搜索、图片评价

---

## 📦 安装依赖

本技能需要 `python3` 和 `uv` 环境。

### 安装 Python 3

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

#CentOS/RHEL
sudo yum install python3 python3-pip
```

### 安装 uv

`uv` 是一个极速的 Python 包管理器，用于运行脚本和管理依赖。

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 使用 pip
pip install uv

# 确保 `uv` 在 PATH 中可用
uv --version
```

---

## 📦 安装技能

### 使用 skills CLI 安装（推荐）

```bash
# github 镜像源
npx skills add https://github.com/wangyan/wangyan-skills/tree/main/skills/wangyan-gemini-image-gen

# gitcode 镜像源 (推荐国内用户使用)
npx skills add https://gitcode.com/wang_yan/wangyan-skills.git
```

### 使用 Clawhub CLI 安装

```bash
# 使用 Clawhub CLI 安装
npx clawhub@latest install wangyan-gemini-image-gen

# 使用腾讯 skillhub 安装 (推荐国内用户使用)
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash  -s -- --no-skills
skillhub install wangyan-gemini-image-gen
```

---

## ⚙️ 环境变量

在技能调用时，OpenClaw 会自动将配置文件中的环境变量注入。

```json
{
  "skills": {
    "entries": {
      "wangyan-gemini-image-gen": {
        "enabled": true,
        "apiKey": "your-api-key",
        "env": {
          "GEMINI_API_KEY": "your-api-key",
          "GEMINI_BASE_URL": "https://api.example.com/v1",
          "GEMINI_MODEL": "gemini-3.1-flash-image-preview",
          "GEMINI_API_FORMAT": "openai",
          "GEMINI_TIMEOUT": "300",
          "GEMINI_RESOLUTION": "1K",
          "GEMINI_OUTPUT_DIR": "output/images"
        }
      }
    }
  }
}
```

优先级：命令行参数 > 环境变量

| 参数 | 环境变量 | 说明 |
|------|---------|------|
| `--api-key` / `-k` | `GEMINI_API_KEY` | API 密钥（必填） |
| `--base-url` / `-b` | `GEMINI_BASE_URL` | API 端点 URL（必填） |
| `--model` / `-m` | `GEMINI_MODEL` | 模型名称（默认自动轮询） |
| `--api-format` / `-F` | `GEMINI_API_FORMAT` | `openai`（默认）或 `google` |
| `--timeout` / `-t` | `GEMINI_TIMEOUT` | 超时秒数（默认 300） |
| `--resolution` / `-r` | `GEMINI_RESOLUTION` | `1K`（默认）、`2K`、`4K` |
| `--output-dir` / `-o` | `GEMINI_OUTPUT_DIR` | 输出目录（默认 `output/images`） |

可选参数：

- `--input-image` / `-i`：输入图片路径（可重复，最多 14 张）
- `--quality`：`standard`（默认）或 `hd`
- `--style`：`natural`（默认）或 `vivid`
- `--aspect-ratio` / `-a`：宽高比（如 `1:1`、`16:9`、`9:16`、`4:3`、`3:4`）
- `--verbose` / `-v`：输出详细调试

---

## 🚀 使用方法

### 生成图片

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "图片描述" --filename "output.png"
```

### 编辑图片（单图）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "编辑指令" --filename "edited.png" -i "/path/input.png" --resolution 2K
```

### 合成多张图片（最多 14 张）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "合成指令" --filename "composed.png" -i img1.png -i img2.png -i img3.png
```

### 自定义端点

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "描述" --filename "output.png" \
  --base-url "https://example.com/v1" --api-key "sk-xxx" --model "gemini-3.1-flash-image-preview"
```

### 使用 Google 原生格式

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "描述" --filename "output.png" --api-format google
```

---

## 🤖 模型自动轮询

脚本内置模型自动轮询机制，当首选模型不可用时，会自动尝试备选模型：

**轮询顺序：**
1. `gemini-3.1-flash-image-preview`（默认首选）
2. `gemini-3-pro-image-preview`（备选1）
3. `gemini-2.5-flash-image`（备选2）

**触发条件：**
- 模型返回 404/400 错误
- 模型返回 "model not found" / "not available" / "not supported" 等错误

**自定义模型：**
如果通过 `--model` 指定了自定义模型，脚本会先尝试该模型，失败后再按上述顺序轮询。

---

## 📝 注意事项

- 文件名使用时间戳格式：`yyyy-mm-dd-hh-mm-ss-name.png`
- 脚本输出 `MEDIA:` 行供 OpenClaw 自动附件到聊天
- 不要回读图片内容，只报告保存路径
- 输出目录默认为工作目录下的 `output/images`，支持相对路径和绝对路径（含 `~` 会自动展开）  
- 编辑模式下未指定分辨率时，自动根据输入图片尺寸推断  
- 内置 429 限流和超时自动重试（最多 3 次）  
- API 响应格式详见 [references/api-formats.md](references/api-formats.md)
