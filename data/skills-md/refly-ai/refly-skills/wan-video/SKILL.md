---
name: wan-video
description: "Generate AI videos using Alibaba Wan 2.6 video models. Use when you need to: (1) create videos from text descriptions, (2) animate static images into videos, or (3) transform and enhance existing videos with AI style transfer."
version: 1.0.0
skillId: skp-jm9hu0hnfh76iidfqbtubvrf
workflowId: c-m5xfkpdxe4rdwjaha71kx3z4
installationId: skpi-x144phjklvf12gqkqftc7ysa
category: file-generation
---

# Wan Video

Generate AI videos using Alibaba Wan 2.6 video models. Use when you need to: (1) create videos from text descriptions, (2) animate static images into videos, or (3) transform and enhance existing videos with AI style transfer.

## Input

Provide input as JSON:

```json
{
  "generation_mode": "Video generation mode: text-to-video, image-to-video, or video-to-video",
  "text_prompt": "Text description for video generation (supports Chinese and English). Describe the scene, actions, style, and mood you want in the video.",
  "input_image": "<file-id>",
  "input_video": "<file-id>",
  "video_duration": "Desired video duration in seconds (5-15 seconds supported)",
  "aspect_ratio": "Video aspect ratio: 16:9 (landscape), 9:16 (portrait), or 1:1 (square)",
  "resolution": "Output video resolution: 720p or 1080p (default: 720p)"
}
```

**Note on File Inputs:**
- `input_image` and `input_video` require a **file ID** (format: `df-xxxxx`)
- **How to get file ID:**
  1. Upload your file to Refly first using `refly file upload <file-path>`
  2. Copy the returned file ID from the upload response
  3. Use this file ID in the input JSON
- For text-to-video mode, you can omit `input_image` and `input_video`
- For image-to-video mode, provide `input_image`
- For video-to-video mode, provide `input_video`

## Execution (Pattern A: File Generation)

### Step 0 (Optional): Upload Files for Image/Video-to-Video Modes

If you want to use image-to-video or video-to-video mode, upload your files first:

```bash
# Upload an image
IMAGE_RESULT=$(refly file upload /path/to/your/image.jpg)
IMAGE_FILE_ID=$(echo "$IMAGE_RESULT" | jq -r '.payload.fileId')
echo "Image file ID: $IMAGE_FILE_ID"

# Or upload a video
VIDEO_RESULT=$(refly file upload /path/to/your/video.mp4)
VIDEO_FILE_ID=$(echo "$VIDEO_RESULT" | jq -r '.payload.fileId')
echo "Video file ID: $VIDEO_FILE_ID"
```

### Step 1: Run the Skill and Get Run ID

**Example 1: Text-to-Video**
```bash
RESULT=$(refly skill run --id skpi-x144phjklvf12gqkqftc7ysa --input '{
  "generation_mode": "text-to-video",
  "text_prompt": "Ocean waves crashing on a rocky shore at sunset",
  "video_duration": "5",
  "aspect_ratio": "16:9",
  "resolution": "720p"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

**Example 2: Image-to-Video**
```bash
# Use the IMAGE_FILE_ID from Step 0
RESULT=$(refly skill run --id skpi-x144phjklvf12gqkqftc7ysa --input '{
  "generation_mode": "image-to-video",
  "text_prompt": "Add motion: camera slowly zooming in",
  "input_image": "'"$IMAGE_FILE_ID"'",
  "video_duration": "5",
  "aspect_ratio": "16:9",
  "resolution": "720p"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-m5xfkpdxe4rdwjaha71kx3z4"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Download and Show Result

```bash
# Get files from this run
FILES=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.files[]')

# Download and open each file
echo "$FILES" | jq -c '.' | while read -r file; do
  FILE_ID=$(echo "$file" | jq -r '.fileId')
  FILE_NAME=$(echo "$file" | jq -r '.name')
  if [ -n "$FILE_ID" ] && [ "$FILE_ID" != "null" ]; then
    refly file download "$FILE_ID" -o "$HOME/Desktop/${FILE_NAME}"
    open "$HOME/Desktop/${FILE_NAME}"
  fi
done
```

## Expected Output

- **Type**: Video
- **Format**: .mp4 video file
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
