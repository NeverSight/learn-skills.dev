---
name: grok-imagine-video
description: xAI Grok Imagine API integration for image generation, text-to-video, image-to-video, and editing via natural language. Use when you need to generate images or videos from text prompts, edit existing images, animate static images into videos, or edit existing videos with natural language instructions. Supports conversational generation across messaging platforms with async polling, progress updates, and automatic delivery.
metadata: {"openclaw": {"requires": {"env": ["XAI_API_KEY"]}, "primaryEnv": "XAI_API_KEY"}}
---

# Grok Imagine Video

Generate videos using xAI's Grok Imagine API directly from your messaging interface.

## Setup

**Important:** You need your own xAI API key. Get it from https://console.x.ai/

For full installation instructions, see [README.md](README.md)

Quick setup:
```bash
# Set your xAI API key (YOUR key, not pre-configured)
export XAI_API_KEY="your-api-key-here"
```

## Capabilities

- **Text-to-image**: Generate images from text descriptions (up to 10 variations)
- **Image editing**: Modify images using natural language
- **Text-to-video**: Create videos from text descriptions
- **Image-to-video**: Animate static images into motion
- **Video editing**: Modify videos using natural language
- **Async generation**: Handles long-running video jobs with polling
- **Auto-delivery**: Downloads and delivers images/videos via chat

## Workflow

### 1. Image Generation

User says: "Create an image of a cyberpunk cityscape at night"

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
result = client.generate_image("A cyberpunk cityscape at night, neon lights reflecting on wet streets")
print(f"Image URL: {result}")
EOF
```

Images are generated instantly (no polling needed). Download promptly as URLs are temporary.

### 1b. Image Editing

User says: "Edit this image — make it look like a watercolor"

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
result = client.edit_image(
    image_url="https://example.com/photo.jpg",
    prompt="Make it look like a watercolor painting"
)
print(f"Edited image: {result}")
EOF
```

### 2. Text-to-Video

User says: "Generate a video of a sunset over the ocean"

```bash
# Use the Python client
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
result = client.text_to_video("A beautiful sunset over the ocean", duration=10)
print(f"Job started: {result['job_id']}")
EOF
```

### 3. Wait for Video Completion

Video generation takes 1-3 minutes. Poll with progress:

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))

def progress(response):
    print(f"Polling... {'Done!' if 'video' in response else 'Pending'}")

final = client.wait_for_completion("request-id-here", progress_callback=progress)
print(f"Video ready: {final['video']['url']}")
EOF
```

### 4. Download and Deliver

Download the completed video to the workspace:

```bash
python3 - << 'EOF'
import os
import sys
sys.path.insert(0, 'scripts')
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(os.getenv("XAI_API_KEY"))
output = "/data/workspace/videos/sunset.mp4"
client.download_video(final, output)  # pass the full response dict
print(f"Downloaded: {output}")
EOF
```

## Image-to-Video

Animate an image:

```python
from grok_video_api import GrokImagineVideoClient

client = GrokImagineVideoClient(api_key)
result = client.image_to_video(
    image_url="https://example.com/photo.jpg",
    prompt="Make the clouds move slowly",
    duration=10
)
```

## Video Editing

Edit an existing video:

```python
result = client.edit_video(
    video_url="https://example.com/source.mp4",
    edit_prompt="Add a warm sunset filter and slow down to 50% speed"
)
```

## Configuration

**Important:** Get your own API key from https://console.x.ai/ - do NOT use pre-configured keys.

```bash
export XAI_API_KEY="sk-..."
```

For OpenClaw integration, add to workspace `.env` or manage via gateway config.

See [README.md](README.md) for complete setup instructions.

## Error Handling

Common errors and responses:

- **Unauthorized / API key not set**: → Get your key from https://console.x.ai/ and set `export XAI_API_KEY="your-key"` - See README.md for details
- **Rate limit**: "Too many requests" → Wait and retry
- **Content policy**: "Prompt violates content policies" → Rephrase prompt
- **Timeout**: Job took too long → Reduce duration or complexity

Always wrap API calls in try/except and provide user-friendly messages.

## Best Practices

**Prompt engineering (images):**
- Be descriptive: "A collage of London landmarks in a stenciled street-art style"
- Specify style: "Watercolor painting of a mountain lake at dawn"
- Use multiple variations (`n=4`) to explore interpretations

**Prompt engineering (videos):**
- Be specific: "A golden retriever running through a sunny meadow"
- Include camera movement: "Slow pan from left to right"
- Specify lighting: "Warm golden hour lighting"

**Performance:**
- Images generate instantly — no polling needed
- Use 480p for faster video generation, 720p for higher quality
- Keep videos under 10 seconds unless essential
- Start with text-to-video, then edit if needed

**User experience:**
- Images: deliver immediately after generation
- Videos: send progress updates: "Generating video... 45% complete"
- Estimate time for videos: "This takes about 2-3 minutes"
- Confirm delivery: "Here's your image/video!"

## Limits

- Images per request: 1-10
- Video duration: 1-15 seconds
- Video resolution: 480p (default) or 720p
- Rate limit: 60 requests/minute
- Max concurrent jobs: 15

See [references/api_reference.md](references/api_reference.md) for full API documentation.

## Integration with Other Skills

- Combine with `ffmpeg-video-editor` for post-processing (trimming, concatenation, filters)
- Use `fal-ai` for additional video effects
- Integrate with `image-generation` skills for source images

## Troubleshooting

**Job stuck in "pending"**: Check API key and quota

**Video generation slow**: Try 720p instead of 1080p

**Failed jobs**: Check error_code in response; see API reference

**Download errors**: Verify video_url is accessible and has not expired
