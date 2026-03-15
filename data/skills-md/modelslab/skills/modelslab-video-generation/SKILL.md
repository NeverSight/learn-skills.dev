---
name: modelslab-video-generation
description: Generate videos from text prompts or animate static images using ModelsLab's v7 Video Fusion API. Supports text-to-video, image-to-video, video-to-video, lip-sync, and motion control with 40+ models including Seedance, Wan, Veo, Sora, Kling, and Hailuo.
---

# ModelsLab Video Generation

Generate AI videos from text descriptions, animate static images, or transform existing videos using state-of-the-art video generation models.

## When to Use This Skill

- Generate videos from text descriptions
- Animate static images
- Transform existing videos (video-to-video)
- Lip-sync audio to video
- Apply motion control from reference videos
- Create short-form content
- Build video marketing materials

## Available APIs (v7)

### Video Fusion Endpoints
- **Text to Video**: `POST https://modelslab.com/api/v7/video-fusion/text-to-video`
- **Image to Video**: `POST https://modelslab.com/api/v7/video-fusion/image-to-video`
- **Video to Video**: `POST https://modelslab.com/api/v7/video-fusion/video-to-video`
- **Lip Sync**: `POST https://modelslab.com/api/v7/video-fusion/lip-sync`
- **Motion Control**: `POST https://modelslab.com/api/v7/video-fusion/motion-control`
- **Fetch Result**: `POST https://modelslab.com/api/v7/video-fusion/fetch/{id}`

> **Note**: v6 endpoints (`/api/v6/video/text2video`, etc.) still work but v7 is the current version.

## Discovering Video Models

```bash
# Search all video models
modelslab models search --feature video_fusion

# Search by name
modelslab models search --search "seedance"
modelslab models search --search "wan"
modelslab models search --search "veo"

# Get model details
modelslab models detail --id seedance-t2v
```

## Text to Video

```python
import requests
import time

def generate_video(prompt, api_key, model_id="seedance-t2v"):
    """Generate a video from a text prompt.

    Args:
        prompt: Text description of the video
        api_key: Your ModelsLab API key
        model_id: Video model to use
    """
    response = requests.post(
        "https://modelslab.com/api/v7/video-fusion/text-to-video",
        json={
            "key": api_key,
            "model_id": model_id,
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, static, distorted"
        }
    )

    data = response.json()

    if data["status"] == "error":
        raise Exception(f"Error: {data['message']}")

    if data["status"] == "success":
        return data["output"][0]

    # Video generation is async - poll for results
    request_id = data["id"]
    print(f"Video processing... Request ID: {request_id}")
    print(f"Estimated time: {data.get('eta', 'unknown')} seconds")

    return poll_video_result(request_id, api_key)

def poll_video_result(request_id, api_key, timeout=600):
    """Poll for video generation results."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        fetch = requests.post(
            f"https://modelslab.com/api/v7/video-fusion/fetch/{request_id}",
            json={"key": api_key}
        )
        result = fetch.json()

        if result["status"] == "success":
            return result["output"][0]
        elif result["status"] == "failed":
            raise Exception(result.get("message", "Generation failed"))

        print(f"Status: processing... ({int(time.time() - start_time)}s elapsed)")
        time.sleep(10)

    raise Exception("Timeout waiting for video generation")

# Usage
video_url = generate_video(
    "A spaceship flying through an asteroid field, cinematic, 4K",
    "your_api_key",
    model_id="seedance-t2v"
)
print(f"Video ready: {video_url}")
```

## Image to Video (Animate Images)

```python
def animate_image(image_url, prompt, api_key, model_id="seedance-i2v"):
    """Animate a static image based on a motion prompt.

    Args:
        image_url: URL of the image to animate
        prompt: Description of desired motion/animation
        model_id: Video model for image-to-video
    """
    response = requests.post(
        "https://modelslab.com/api/v7/video-fusion/image-to-video",
        json={
            "key": api_key,
            "model_id": model_id,
            "init_image": [image_url],  # v7 expects array
            "prompt": prompt,
            "negative_prompt": "static, still, low quality, blurry"
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_video_result(data["id"], api_key)
    else:
        raise Exception(data.get("message", "Unknown error"))

# Animate a landscape
video = animate_image(
    "https://example.com/landscape.jpg",
    "The clouds moving slowly across the sky, birds flying in the distance",
    "your_api_key",
    model_id="seedance-i2v"
)
print(f"Animated video: {video}")
```

## Video to Video

```python
def transform_video(video_url, prompt, api_key, model_id="wan2.1"):
    """Transform an existing video with a new style or content.

    Args:
        video_url: URL of the source video
        prompt: Description of desired transformation
    """
    response = requests.post(
        "https://modelslab.com/api/v7/video-fusion/video-to-video",
        json={
            "key": api_key,
            "model_id": model_id,
            "init_video": [video_url],  # v7 expects array
            "prompt": prompt
        }
    )

    data = response.json()
    if data["status"] == "processing":
        return poll_video_result(data["id"], api_key)
    elif data["status"] == "success":
        return data["output"][0]
```

## Lip Sync

```python
def lip_sync(video_url, audio_url, api_key, model_id="lipsync-2"):
    """Sync lip movements to audio.

    Args:
        video_url: URL of the video with a face
        audio_url: URL of the audio to sync to
    """
    response = requests.post(
        "https://modelslab.com/api/v7/video-fusion/lip-sync",
        json={
            "key": api_key,
            "model_id": model_id,
            "init_video": video_url,
            "init_audio": audio_url
        }
    )

    data = response.json()
    if data["status"] == "processing":
        return poll_video_result(data["id"], api_key)
    elif data["status"] == "success":
        return data["output"][0]
```

## Popular Video Model IDs

### Text to Video
- `seedance-t2v` - Seedance text-to-video (BytePlus)
- `seedance-1.0-pro-fast-t2v` - Seedance Pro Fast
- `wan2.6-t2v` - Wan 2.6 text-to-video (Alibaba)
- `wan2.1` - Wan 2.1 (ModelsLab in-house)
- `veo2` - Google Veo 2
- `veo3` - Google Veo 3
- `sora-2` - OpenAI Sora 2
- `Hailuo-2.3-t2v` - Hailuo 2.3 (MiniMax)
- `kling-v2-5-turbo-t2v` - Kling V2.5 Turbo

### Image to Video
- `seedance-i2v` - Seedance image-to-video
- `seedance-1.0-pro-i2v` - Seedance Pro
- `wan2.6-i2v` - Wan 2.6 image-to-video
- `Hailuo-2.3-i2v` - Hailuo 2.3
- `kling-v2-1-i2v` - Kling V2.1

### Lip Sync
- `lipsync-2` - Sync Labs Lipsync 2

### Motion Control
- `kling-motion-control` - Kling Motion Control
- `omni-human` - OmniHuman (BytePlus)

Browse all models: https://modelslab.com/models

## Key Parameters

| Parameter | Description | Recommended Values |
|-----------|-------------|-------------------|
| `model_id` | Video generation model (required) | See model tables above |
| `prompt` | Text description of video content | Be specific about motion and scene |
| `negative_prompt` | What to avoid | "static, low quality, blurry" |
| `init_image` | Source image for i2v (array) | `["https://..."]` |
| `init_video` | Source video for v2v (array) | `["https://..."]` |
| `init_audio` | Audio for lip-sync/video | URL string |
| `width` / `height` | Video dimensions (512-1024) | 512, 768, 1024 |
| `duration` | Video length in seconds | 4-30 |
| `aspect_ratio` | Aspect ratio | "16:9", "9:16", "1:1" |
| `webhook` | Async notification URL | URL string |
| `track_id` | Custom tracking identifier | Any string |

## Best Practices

### 1. Write Motion-Focused Prompts
```
Bad: "A cat"
Good: "A cat walking through a garden, looking around curiously, sunlight filtering through trees"

Include: Action, movement, camera motion, atmosphere
```

### 2. Set Realistic Expectations
- Videos are 4-30 seconds typically
- Generation takes 30 seconds to several minutes depending on model
- Best for short clips, not full productions

### 3. Handle Async Operations
```python
# Video generation is ALWAYS async
# Always implement polling or use webhooks
if data["status"] == "processing":
    video = poll_video_result(data["id"], api_key)
```

### 4. Use Webhooks
```python
payload = {
    "key": api_key,
    "model_id": "seedance-t2v",
    "prompt": "...",
    "webhook": "https://yourserver.com/webhook/video",
    "track_id": "video_001"
}
```

## Error Handling

```python
try:
    video = generate_video(prompt, api_key, model_id="seedance-t2v")
    print(f"Video generated: {video}")
except Exception as e:
    print(f"Video generation failed: {e}")
```

## Resources

- **API Documentation**: https://docs.modelslab.com/video-api/overview
- **Model Browser**: https://modelslab.com/models
- **Model Selection Guide**: https://docs.modelslab.com/guides/model-selection
- **Get API Key**: https://modelslab.com/dashboard
- **Webhooks Guide**: See `modelslab-webhooks` skill

## Related Skills

- `modelslab-model-discovery` - Find and filter models
- `modelslab-image-generation` - Generate images for img2video
- `modelslab-audio-generation` - Generate audio for lip-sync
- `modelslab-chat-generation` - Chat with LLM models
- `modelslab-webhooks` - Handle async operations efficiently
