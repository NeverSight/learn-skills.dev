---
name: nano-banana-pro
description: "Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). Use when you need to: (1) generate images from text descriptions, (2) edit existing images with AI, (3) compose multiple images into one scene. Supports 1K/2K/4K resolutions and up to 14 input images for composition."
category: file-generation
tags:
  - image
  - ai
  - gemini
  - generation
  - editing
version: 1.0.0
skillId: skp-ud4d5kijwrf8k18muzmhwv9y
workflowId: c-g6emwcpi1wpalsz6j4gyi3d9
installationId: skpi-h9kpmts9ho1kl9l1sohaloeu
triggers:
  - generate image
  - edit image
  - AI image generation
  - Gemini image
  - 图片生成
  - AI绘图
  - 编辑图片
  - 文生图
  - 图生图
---

# Nano Banana Pro

Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). Use when you need to: (1) generate images from text descriptions, (2) edit existing images with AI, (3) compose multiple images into one scene. Supports 1K/2K/4K resolutions and up to 14 input images for composition.

## Input

Provide input as JSON:

```json
{
  "prompt": "Detailed description for image generation or editing (e.g., 'a cute cat playing in a garden')",
  "resolution": "Image resolution: 1K, 2K, or 4K (default: 1K)",
  "aspect_ratio": "Image aspect ratio: 16:9, 1:1, 9:16, 5:4, or 4:3 (default: 1:1)",
  "input_image": "<file-id>"
}
```

**Note on File Input:**
- `input_image` is optional and requires a **file ID** (format: `df-xxxxx`)
- **How to get file ID:**
  1. Upload your image using `refly file upload <file-path>`
  2. Copy the returned file ID from the upload response
  3. Use this file ID in the input JSON
- Omit `input_image` for pure text-to-image generation
- Provide `input_image` for image editing or transformation

## API Request Structure

This skill uses **Gemini 3 Pro Image API** with the following structure:

### Text-to-Image (Pure Generation)
```json
{
  "contents": [{
    "parts": [
      {"text": "Your prompt here"}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "1:1",
      "imageSize": "2K"
    }
  }
}
```

### Image-to-Image (With Reference)
```json
{
  "contents": [{
    "parts": [
      {"text": "Your editing prompt"},
      {"inline_data": {"mime_type": "image/png", "data": "<BASE64_DATA>"}}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "2K"
    }
  }
}
```

**Notes:**
- Images are automatically converted to base64 format
- Supports up to 14 input images for composition
- `imageSize` maps to resolution: 1K, 2K, or 4K
- `aspectRatio` determines output dimensions

## Execution (Pattern A: File Generation)

### Step 0 (Optional): Upload Input Image

```bash
# Upload an image if you want to edit or transform an existing image
INPUT_RESULT=$(refly file upload /path/to/your/image.jpg)
INPUT_FILE_ID=$(echo "$INPUT_RESULT" | jq -r '.payload.fileId')
echo "Input image file ID: $INPUT_FILE_ID"
```

### Step 1: Run the Skill and Get Run ID

**Example 1: Text-to-Image Generation**
```bash
RESULT=$(refly skill run --id skpi-h9kpmts9ho1kl9l1sohaloeu --input '{
  "prompt": "a cute cat playing in a garden",
  "resolution": "2K",
  "aspect_ratio": "16:9"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

**Example 2: Image Editing with Reference**
```bash
# Use the INPUT_FILE_ID from Step 0
RESULT=$(refly skill run --id skpi-h9kpmts9ho1kl9l1sohaloeu --input '{
  "prompt": "transform this image into watercolor painting style",
  "input_image": "'"$INPUT_FILE_ID"'",
  "resolution": "2K",
  "aspect_ratio": "1:1"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-g6emwcpi1wpalsz6j4gyi3d9"
# Use RUN_ID (we-xxx), not installationId or skillId
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Download and Show Result

```bash
# Get files from this run (use RUN_ID)
FILES=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.files[]')

# Download and open each file
echo "$FILES" | jq -c '.' | while read -r file; do
  FILE_ID=$(echo "$file" | jq -r '.fileId')
  FILE_NAME=$(echo "$file" | jq -r '.name')
  if [ -n "$FILE_ID" ] && [ "$FILE_ID" != "null" ]; then
    OUTPUT_PATH="$HOME/Desktop/${FILE_NAME}"
    refly file download "$FILE_ID" -o "$OUTPUT_PATH"
    open "$OUTPUT_PATH"
  fi
done
```

## Expected Output

- **Type**: Image
- **Format**: .png/.jpg image file (1K/2K/4K resolution)
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
