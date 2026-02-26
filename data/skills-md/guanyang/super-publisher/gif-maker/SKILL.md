---
name: gif-maker
description: 将序列帧图片或精灵表（Sprite Sheet）转换为高质量 GIF 动画。支持自定义 FPS、布局切分及循环播放。
---

# GIF 动画生成器 (GIF Maker)

本 Skill 旨在帮助用户快速将一组序列帧图片或单张精灵表（Sprite Sheet）转换为 GIF 动画。

## 核心功能

*   **序列帧转 GIF**：支持读取文件夹内的 `png`, `jpg` 序列，按文件名排序合成 GIF。
*   **精灵表转 GIF**：支持读取单张 Grid 图片（如 4x4 精灵表），自动切分并合成为 GIF。
*   **智能压缩**：支持通过 `--max-size` 参数指定目标文件大小（如 950KB），自动调整压缩参数以满足微信表情包等平台的体积限制。
*   **参数控制**：
    *   `--fps`：指定每秒帧数（默认为 12）。
    *   `--layout`：指定精灵表布局（如 `4x4`），仅在这个模式下需要。
    *   `--loop`：默认永久循环。
    *   `--max-size`: 指定最大体积 (KB)。

## 使用指南

### 1. 快速开始

无需手动安装依赖，直接运行脚本即可。工具会自动创建虚拟环境 (`.venv`) 并安装所需依赖。

```bash
# 基本用法 1：从文件夹读取序列帧
./skills/gif-maker/scripts/run.sh /path/to/frame_folder --output my_anim.gif

# 基本用法 2：从单张精灵表生成 (需要指定布局)
./skills/gif-maker/scripts/run.sh /path/to/sheet.png --layout 4x4 --output my_sheet_anim.gif

# 常用选项：
# - 指定 FPS (例如 24)
./skills/gif-maker/scripts/run.sh /path/to/folder --fps 24

# - 开启自动压缩 (限制文件大小在 950KB 以内)
./skills/gif-maker/scripts/run.sh /path/to/folder --max-size 950
```

### 2. (可选) 手动安装

如果您希望手动管理环境（注意：压缩功能依赖 `gifsicle` 工具，请确保系统已安装）：
- macOS: `brew install gifsicle`
- Ubuntu: `sudo apt-get install gifsicle`

```bash
python3 -m venv skills/gif-maker/.venv
source skills/gif-maker/.venv/bin/activate
pip install -r skills/gif-maker/requirements.txt
python3 skills/gif-maker/scripts/make_gif.py ...
```

## 参数说明

*   `source`: 输入路径。可以是包含图片的文件夹，也可以是单张图片文件。
*   `--output` (`-o`): 输出 GIF 文件名，默认为 `output.gif`。
*   `--fps`: 帧率，默认为 12。
*   `--layout`: 仅当 `source` 为单文件时使用，格式为 `行数x列数` (如 `4x4`)。
*   `--max-size`: (可选) 启用 GIF 压缩，指定目标文件最大大小 (KB)。仅当原始文件超过此大小时才会尝试压缩。

## 示例

假设你有一个文件夹 `frames/` 包含 `01.png`, `02.png` ... `10.png`：

```bash
./skills/gif-maker/scripts/run.sh frames/ -o animation.gif --fps 15
```

假设你有一张 `sheet.png` 是 4x4 的动作序列，且需要生成符合微信表情包规范（<1MB）的 GIF：

```bash
./skills/gif-maker/scripts/run.sh sheet.png --layout 4x4 -o action.gif --max-size 950
```
