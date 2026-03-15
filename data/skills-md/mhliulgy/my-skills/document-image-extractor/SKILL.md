---
name: document-image-extractor
description: 从 Word (.docx) 和 PDF (.pdf) 文档中提取图片并保存到指定文件夹。使用场景包括：(1) 从 Word 文档提取图片，(2) 从 PDF 文档提取图片，(3) 批量提取多个文档的图片，(4) 提取文档中的所有图片素材
---

# Document Image Extractor

从 Word 和 PDF 文档中提取图片的 skill。

## 依赖安装

使用前需要安装依赖（默认用户已安装）：

```bash
conda run -n claude-code pip install python-docx pymupdf
```

## 使用方法

### 基本命令

```bash
conda run -n claude-code python scripts/extract_images.py <文档路径> [-o <输出目录>]
```

### 参数说明

- `文档路径`：Word (.docx) 或 PDF (.pdf) 文件路径
- `-o, --output`：输出目录（可选，默认在文档同目录创建 `<文件名>_images` 文件夹）
- `--dpi`：PNG 转换 DPI（可选，默认 150，越高越清晰）
- `--keep-emf`：保留原始 EMF/WMF 文件（Word 矢量图专用）
- `--convert-svg`：将 EMF/WMF 转换为 SVG（Word 矢量图专用）

### 示例

```bash
# 从 Word 文档提取图片（默认只输出 PNG）
conda run -n claude-code python scripts/extract_images.py document.docx

# 提取图片并保留 EMF 源文件
conda run -n claude-code python scripts/extract_images.py document.docx --keep-emf

# 提取图片并转换为 SVG 格式
conda run -n claude-code python scripts/extract_images.py document.docx --convert-svg

# 提取图片并同时保留 EMF 和转换为 SVG
conda run -n claude-code python scripts/extract_images.py document.docx --keep-emf --convert-svg

# 指定更高 DPI 以获得更清晰的 PNG
conda run -n claude-code python scripts/extract_images.py document.docx --dpi 300

# 从 PDF 提取图片
conda run -n claude-code python scripts/extract_images.py document.pdf

# 指定输出目录
conda run -n claude-code python scripts/extract_images.py document.docx -o ./my_images
```

## 输出格式

- 图片命名：`image_001.png`, `image_002.jpg`, ...
- PDF 图片会标注来源页面：`image_001.png (page 1)`

## 支持的图片格式

### Word 文档
- PNG, JPEG, JPG, GIF, BMP, TIFF, WebP, SVG
- EMF/WMF 矢量图（可转换为 PNG/SVG）

### PDF 文档
- PNG, JPEG, JPG, GIF, BMP, TIFF
- 注：PDF 矢量图形无法单独提取（PDF 内置为绘制指令，非独立对象）

## 注意事项

- Word 文档：提取嵌入的图片、媒体文件和 SVG
- PDF 文档：仅提取嵌入的位图图像
- 如果文档中没有图片，将提示 "No images found"
