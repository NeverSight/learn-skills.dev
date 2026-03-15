---
name: sora-video
description: Generate videos using Sora via lnapi.com.
---

# Sora Video Generation

Use the `lnapi.com` API to generate videos with Sora. Supports text-to-video and image-to-video.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/main.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

## Usage

```bash
# Text-to-Video
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A golden retriever running on the beach" --output video.mp4

# Image-to-Video
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Animate this image" --image input.jpg --output video.mp4

# Specify duration and size
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "City at night" --seconds 15 --size 1280x720 --output video.mp4
```

## Options

- `--prompt <text>`, `-p`: Prompt text (required)
- `--promptfiles <files...>`: Read prompt from files
- `--image <path>`: Input image path (for image-to-video)
- `--output <path>`: Output video path (required)
- `--model <id>`: Model ID (default `sora-2`)
- `--seconds <n>`: Duration in seconds (10 or 15, default `10`)
- `--size <WxH>`: Resolution (1280x720, 720x1280, 720x720, default `720x1280`)
- `--poll <ms>`: Polling interval in ms (default `5000`)
- `--json`: JSON output
- `-h, --help`: Show help

## Fixed Config

- Base URL: `https://lnapi.com`
- API Key: `LNAPI_KEY` (Required in environment)
