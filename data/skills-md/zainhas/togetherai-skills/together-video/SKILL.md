---
name: together-video
description: Generate videos from text and image prompts via Together AI. 15+ models including Veo 2/3, Sora 2, Kling 2.1, Hailuo 02, Seedance, PixVerse, Vidu. Supports text-to-video, image-to-video, keyframe control, and reference images. Use when users want to generate videos, create video content, animate images, or work with any video generation task.
---

# Together Video Generation

## Overview

Generate videos asynchronously — submit a job, poll for completion, download the result.

- Endpoint: `/v2/videos`
- Async workflow: create job → poll status → download video
- 15+ models from Google, OpenAI, MiniMax, Kuaishou, ByteDance, PixVerse, Vidu

## Installation

```shell
# Python (recommended)
uv init  # optional, if starting a new project
uv add together
```

```shell
# or with pip
pip install together
```

```shell
# TypeScript / JavaScript
npm install together-ai
```

Set your API key:

```shell
export TOGETHER_API_KEY=<your-api-key>
```

## Quick Start

### Text-to-Video

```python
import time
from together import Together
client = Together()

job = client.videos.create(
    prompt="A serene sunset over the ocean with gentle waves",
    model="minimax/video-01-director",
    width=1366,
    height=768,
)
print(f"Job ID: {job.id}")

# Poll until completion
while True:
    status = client.videos.retrieve(job.id)
    if status.status == "completed":
        print(f"Video URL: {status.outputs.video_url}")
        break
    elif status.status == "failed":
        print("Failed")
        break
    time.sleep(5)
```

```typescript
import Together from "together-ai";
const together = new Together();

const job = await together.videos.create({
  prompt: "A serene sunset over the ocean with gentle waves",
  model: "minimax/video-01-director",
  width: 1366, height: 768,
});

// Poll until completion
while (true) {
  const status = await together.videos.retrieve(job.id);
  if (status.status === "completed") {
    console.log(`Video URL: ${status.outputs.video_url}`);
    break;
  } else if (status.status === "failed") break;
  await new Promise(r => setTimeout(r, 5000));
}
```

```shell
# Create a video generation job
curl -X POST "https://api.together.xyz/v2/videos" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "minimax/video-01-director",
    "prompt": "A serene sunset over the ocean with gentle waves",
    "width": 1366,
    "height": 768
  }'

# Poll for completion (replace $JOB_ID with the id from the create response)
curl -X GET "https://api.together.xyz/v2/videos/$JOB_ID" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

### Image-to-Video (Keyframes)

```python
import base64, requests

image_url = "https://example.com/photo.jpg"
img_data = base64.b64encode(requests.get(image_url).content).decode("utf-8")

job = client.videos.create(
    prompt="Smooth camera zoom out",
    model="minimax/hailuo-02",
    frame_images=[{"input_image": img_data, "frame": 0}],
)
```

```typescript
import * as fs from "fs";
import Together from "together-ai";
const together = new Together();

// Load and encode your image
const imageBuffer = fs.readFileSync("keyframe.jpg");
const base64Image = imageBuffer.toString("base64");

const job = await together.videos.create({
  prompt: "Smooth camera zoom out",
  model: "minimax/hailuo-02",
  frame_images: [{ input_image: base64Image, frame: 0 }],
});

// Poll until completion
while (true) {
  const status = await together.videos.retrieve(job.id);
  if (status.status === "completed") {
    console.log(`Video URL: ${status.outputs.video_url}`);
    break;
  } else if (status.status === "failed") break;
  await new Promise(r => setTimeout(r, 5000));
}
```

```shell
# Create an image-to-video job (replace $BASE64_IMAGE with your base64-encoded image)
curl -X POST "https://api.together.xyz/v2/videos" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "minimax/hailuo-02",
    "prompt": "Smooth camera zoom out",
    "frame_images": [{"input_image": "$BASE64_IMAGE", "frame": 0}]
  }'

# Poll for completion (replace $JOB_ID with the id from the create response)
curl -X GET "https://api.together.xyz/v2/videos/$JOB_ID" \
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

### Reference Images

```python
job = client.videos.create(
    prompt="A cat dancing energetically",
    model="minimax/hailuo-02",
    reference_images=["https://example.com/cat.jpg"],
)
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `prompt` | string | Text description (required for all models except Kling) | - |
| `model` | string | Model ID (required) | - |
| `width` | int | Video width | 1366 |
| `height` | int | Video height | 768 |
| `seconds` | int | Duration (1-10) | 5-6 |
| `fps` | int | Frames per second | 24-25 |
| `steps` | int | Diffusion steps | varies |
| `guidance_scale` | float | Prompt adherence (6-10) | varies |
| `seed` | int | Random seed | random |
| `negative_prompt` | string | What to exclude | - |
| `frame_images` | array | Keyframe images (base64) | - |
| `reference_images` | array | Style reference URLs | - |
| `output_format` | string | "MP4" or "WEBM" | "MP4" |
| `output_quality` | int | Bitrate/quality (lower = higher quality) | 20 |

## Job Status Flow

| Status | Description |
|--------|-------------|
| `queued` | Waiting in queue |
| `in_progress` | Generating |
| `completed` | Done — video URL available |
| `failed` | Check `info.errors` |
| `cancelled` | Job cancelled |

## Guidance Scale Tips

- **6-7**: Creative, more interpretation
- **7-9**: Balanced (recommended)
- **9-10**: Strict prompt adherence
- **>12**: Avoid — causes artifacts

## Key Models

| Model | API String | Duration | Dimensions |
|-------|-----------|----------|------------|
| Veo 3.0 | `google/veo-3.0` | 8s | 1280x720, 1920x1080 |
| Veo 3.0 + Audio | `google/veo-3.0-audio` | 8s | 1280x720, 1920x1080 |
| Sora 2 | `openai/sora-2` | 8s | 1280x720 |
| Hailuo 02 | `minimax/hailuo-02` | 10s | 1366x768, 1920x1080 |
| Kling 2.1 Master | `kwaivgI/kling-2.1-master` | 5s | 1920x1080 |
| Seedance 1.0 Pro | `ByteDance/Seedance-1.0-pro` | 5s | Multiple |
| PixVerse v5 | `pixverse/pixverse-v5` | 5s | Multiple |
| Vidu 2.0 | `vidu/vidu-2.0` | 8s | Multiple |

See [references/models.md](references/models.md) for the complete model table.

## Resources

- **Full model details**: See [references/models.md](references/models.md)
- **Runnable script**: See [scripts/generate_video.py](scripts/generate_video.py) — async video generation with polling helper (v2 SDK)
- **Runnable script (TypeScript)**: See [scripts/generate_video.ts](scripts/generate_video.ts) — minimal OpenAPI `x-codeSamples` extraction for create/retrieve video (TypeScript SDK)
- **Official docs**: [Videos Overview](https://docs.together.ai/docs/videos-overview)
- **API reference**: [Create Video API](https://docs.together.ai/reference/create-videos)
