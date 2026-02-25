---
name: fal-image
description: "Generate AI images using Fal.ai Flux models. Use when you need to: (1) create images from text prompts, (2) transform existing images with AI, or (3) generate photorealistic or artistic images quickly."
version: 1.0.0
skillId: skp-jxj7q39dzqppywoes536ht67
workflowId: c-we6qb7ch1cfpc47jvkidqidb
installationId: skpi-g7ydq91v0sdvpm3t53h961vg
category: file-generation
---

# Fal Image

Generate AI images using Fal.ai Flux models. Use when you need to: (1) create images from text prompts, (2) transform existing images with AI, or (3) generate photorealistic or artistic images quickly.

## Input

Provide input as JSON:

```json
{
  "prompt": "Text description of the image you want to generate (e.g., 'a serene mountain landscape at sunset with vibrant colors')",
  "reference_image": "<file-id>",
  "image_size": "Image dimensions (e.g., 'square', 'landscape_16_9', 'portrait_9_16', or custom like '1024x768')",
  "num_images": "Number of images to generate (1-4)"
}
```

**Note on File Input:**
- `reference_image` is optional and requires a **file ID** (format: `df-xxxxx`) if provided
- **How to get file ID:**
  1. Upload your reference image to Refly using `refly file upload <file-path>`
  2. Copy the returned file ID from the upload response
  3. Use this file ID in the input JSON
- Omit `reference_image` for pure text-to-image generation

## Execution (Pattern A: File Generation)

### Step 0 (Optional): Upload Reference Image

```bash
# Upload a reference image if you want to use one
REF_RESULT=$(refly file upload /path/to/reference.jpg)
REF_FILE_ID=$(echo "$REF_RESULT" | jq -r '.payload.fileId')
echo "Reference image file ID: $REF_FILE_ID"
```

### Step 1: Run the Skill and Get Run ID

**Example 1: Text-to-Image (No Reference)**
```bash
RESULT=$(refly skill run --id skpi-g7ydq91v0sdvpm3t53h961vg --input '{
  "prompt": "a serene mountain landscape at sunset with vibrant colors",
  "image_size": "landscape_16_9",
  "num_images": "1"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

**Example 2: Image-to-Image (With Reference)**
```bash
# Use the REF_FILE_ID from Step 0
RESULT=$(refly skill run --id skpi-g7ydq91v0sdvpm3t53h961vg --input '{
  "prompt": "transform this into a watercolor painting style",
  "reference_image": "'"$REF_FILE_ID"'",
  "image_size": "landscape_16_9",
  "num_images": "1"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-we6qb7ch1cfpc47jvkidqidb"
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

- **Type**: Image
- **Format**: .png/.jpg image file
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
