---
name: silicon-paddle-ocr
description: OCR skill using PaddleOCR model via SiliconFlow API. This skill should be used when the user asks to "recognize text from an image", "extract text from a photo", "OCR this image", "read text from screenshot", or mentions "PaddleOCR", "image text recognition", "text extraction from images".
license: MIT
metadata:
  author: aotenjou
  version: "1.0.0"
---

# OCR - Image Text Recognition

Use PaddleOCR to extract text content from images. Supports single image or batch processing.

## Overview

This skill provides optical character recognition (OCR) capabilities using the PaddlePaddle/PaddleOCR-VL-1.5 model via the SiliconFlow API. Extract text from JPG, PNG, WebP, BMP, and GIF images.

## When to Use

Invoke this skill when:
- User wants to extract text from an image
- User asks to OCR a screenshot or photo
- User needs to read text from an image file
- User mentions text recognition from images

## How to Use

### Prerequisites

Ensure the `SILICONFLOW_API_KEY` environment variable is set:
```bash
export SILICONFLOW_API_KEY="your_api_key"
```

### Basic Usage

Execute the OCR script:
```bash
python3 scripts/ocr_skill.py [options] image_path
```

### Arguments

| Argument | Description |
|----------|-------------|
| `images` | Image file path(s) or glob pattern (required) |
| `-k, --api-key` | API key (default: from SILICONFLOW_API_KEY env) |
| `-m, --model` | OCR model name (default: PaddlePaddle/PaddleOCR-VL-1.5) |
| `-p, --prompt` | Recognition prompt for custom behavior |
| `-j, --json` | Output results in JSON format |
| `-o, --output` | Save results to specified file |
| `--max-tokens` | Maximum tokens in response (default: 2000) |

### Examples

Single image:
```bash
python3 scripts/ocr_skill.py /path/to/image.jpg
```

Multiple images with glob:
```bash
python3 scripts/ocr_skill.py /path/to/images/*.png
```

JSON output format:
```bash
python3 scripts/ocr_skill.py --json /path/to/image.jpg
```

Custom prompt for table extraction:
```bash
python3 scripts/ocr_skill.py -p "Please identify and format table content as Markdown" /path/to/table.jpg
```

Save to file:
```bash
python3 scripts/ocr_skill.py --json --output results.json /path/to/images/*.jpg
```

### Output Format

**Text output** (default):
```
--- image.jpg ---
识别到的文字内容
识别到 X 处文字区域
```

**JSON output**:
```json
{
  "image.jpg": {
    "image_path": "/path/to/image.jpg",
    "image_size": [width, height],
    "texts": [
      {
        "text": "识别的文字",
        "box": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
      }
    ],
    "full_text": "所有文本的组合"
  },
  "image2.png": { ... }
}
```

**Coordinates Explanation:**
- LOC values are normalized coordinates converted to pixel coordinates
- Conversion: pixel = LOC × (image_size / LOC_max_value)
- LOC max_value is approximately 972 (may vary by model/image)
- The `box` field provides the four corner coordinates of each text region in pixel format

## Supported Image Formats

- JPG/JPEG
- PNG
- WebP
- BMP
- GIF

## Error Handling

If processing fails:
- Check that the image file exists
- Verify the SILICONFLOW_API_KEY is valid
- Ensure the API endpoint is reachable

Images that fail to process will show an error message, and other images will continue processing.

## Additional Resources

### Reference Files

- **`references/api-configuration.md`** - API configuration details

### Example Files

- **`examples/sample-usage.sh`** - Example usage script

### Scripts

- **`scripts/ocr_skill.py`** - The main OCR implementation
