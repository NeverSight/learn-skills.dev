---
name: image-resizer
description: 图片尺寸调整和压缩工具技能。用于按指定像素宽高、比例或最大尺寸限制调整图片大小，并支持智能压缩到指定文件大小。适用于需要批量处理图片、生成特定尺寸缩略图、压缩图片以满足文件大小限制等场景。
---

## 技能概述

**技能名称：** image-resizer  
**核心功能：** 图片尺寸调整和压缩，支持按像素宽高、比例、最大尺寸进行调整，以及智能压缩到指定文件大小  
**适用场景：**

- 按指定像素尺寸调整图片（如 800×600）
- 按比例缩放图片（如 50% 缩小、200% 放大）
- 限制最大尺寸（保持比例，如最大 1920×1080）
- 指定宽高比裁剪（如 16:9、4:3）
- 压缩图片到指定大小（如压缩到 ≤500KB）
- 批量处理多张图片

## 脚本使用说明

### 安装依赖

```bash
cd scripts
npm install
```

### 基本用法

```bash
node resize_image.js <输入图片> [选项]
```

### 选项说明

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--width` | `-w` | 目标宽度（像素） | `-w 800` |
| `--height` | `-h` | 目标高度（像素） | `-h 600` |
| `--scale` | `-s` | 缩放比例 | `-s 0.5` |
| `--max-width` | - | 最大宽度（保持比例） | `--max-width 1920` |
| `--max-height` | - | 最大高度（保持比例） | `--max-height 1080` |
| `--quality` | `-q` | 输出质量 1-100 | `-q 80` |
| `--size` | `-S` | 目标文件大小（KB），自动压缩 | `-S 500` |
| `--format` | `-f` | 输出格式：png\|jpg\|webp\|original | `-f webp` |
| `--output` | `-o` | 输出路径 | `-o output.png` |
| `--aspect-ratio` | `-a` | 目标宽高比 | `-a 16:9` |
| `--fit` | - | 适应模式 | `--fit cover` |

### 适应模式说明

| 模式 | 说明 |
|------|------|
| `cover` | 填充整个区域（可能裁剪，默认） |
| `contain` | 完整放入区域内（可能留白） |
| `fill` | 拉伸填充 |
| `inside` | 完整放入（仅缩小） |
| `outside` | 完全覆盖（仅放大） |

## 使用示例

### 示例 1：按指定尺寸调整

```bash
node resize_image.js input.png -w 800 -h 600 -o output.png
```

### 示例 2：按比例缩放

```bash
node resize_image.js input.png -s 0.5 -o output.png
```

### 示例 3：压缩到指定大小

```bash
node resize_image.js input.png -S 500 -o output.jpg
```

### 示例 4：指定宽高比裁剪

```bash
node resize_image.js input.png -a 16:9 -o output.png
```

### 示例 5：最大尺寸限制（保持比例）

```bash
node resize_image.png input.png --max-width 1920 --max-height 1080 -o output.png
```

### 示例 6：转换为 WebP 并压缩

```bash
node resize_image.js input.png -f webp -q 80 -o output.webp
```

## 典型工作流程

### 流程 1：生成网站缩略图

1. 读取原始图片
2. 限制最大宽度为 1200px，保持比例
3. 压缩到 ≤300KB
4. 输出为 JPEG 格式

```bash
node resize_image.js photo.jpg --max-width 1200 -S 300 -f jpg -o thumbnail.jpg
```

### 流程 2：生成社交媒体图片

1. 读取原始图片
2. 调整为 1080×1080 正方形
3. 压缩到 ≤500KB

```bash
node resize_image.js input.png -w 1080 -h 1080 -S 500 -o instagram.png
```

### 流程 3：生成 16:9 横版图片

1. 读取原始图片
2. 按 16:9 比例裁剪（居中）
3. 压缩到 ≤200KB

```bash
node resize_image.js input.png -a 16:9 -S 200 -o 16_9.jpg
```

## 技能文件结构

```
image-resizer/
├── SKILL.md                    # 技能主文件
└── scripts/
    ├── resize_image.js         # 图片处理脚本
    └── package.json            # 依赖配置
```

## 依赖说明

- **sharp**: 图片处理库，支持 PNG、JPEG、WebP 等格式的转换、裁剪和压缩
