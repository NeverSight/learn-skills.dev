---
name: modelslab-image-generation
description: Generate high-quality AI images from text prompts or transform existing images using ModelsLab's v7 API with 50,000+ models including FLUX, Realtime, and Community models. Supports text-to-image, image-to-image, inpainting, and ControlNet.
---

# ModelsLab Image Generation

Generate stunning AI images using ModelsLab's extensive library of models and powerful generation endpoints.

## When to Use This Skill

- Generate images from text descriptions
- Transform or modify existing images
- Fill in masked parts of images (inpainting)
- Use ControlNet for precise control
- Need fast generation (Realtime API)
- Need highest quality (Community/FLUX models)
- Create product images, marketing graphics, or artwork

## Available APIs (v7)

### 1. Text to Image
- `POST https://modelslab.com/api/v7/images/text-to-image`
- 50,000+ models available

### 2. Image to Image
- `POST https://modelslab.com/api/v7/images/image-to-image`
- Transform existing images with a prompt

### 3. Inpainting
- `POST https://modelslab.com/api/v7/images/inpaint`
- Fill masked regions of an image

### 4. Fetch Result
- `POST https://modelslab.com/api/v7/images/fetch/{id}`
- Poll for async generation results

> **Note**: v6 endpoints (`/api/v6/images/text2img`, etc.) still work but v7 is the current version.

## Discovering Image Models

```bash
# Search image models by name
modelslab models search --feature imagen

# Search specific models
modelslab models search --search "flux"
modelslab models search --search "midjourney"

# Get model details
modelslab models detail --id flux
```

## Quick Start: Text to Image

```python
import requests
import time

def generate_image(prompt, api_key, model_id="flux"):
    """Generate an image from text.

    Args:
        prompt: Text description of the image
        api_key: Your ModelsLab API key
        model_id: Model to use (flux, midjourney, sdxl, imagen-3, etc.)
    """
    response = requests.post(
        "https://modelslab.com/api/v7/images/text-to-image",
        json={
            "key": api_key,
            "model_id": model_id,
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, distorted",
            "width": 1024,
            "height": 1024,
            "samples": 1,
            "guidance_scale": 7.5
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_result(data["id"], api_key)
    else:
        raise Exception(f"Error: {data.get('message')}")

def poll_result(request_id, api_key, timeout=300):
    """Poll for async generation results."""
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.post(
            f"https://modelslab.com/api/v7/images/fetch/{request_id}",
            json={"key": api_key}
        )
        data = resp.json()

        if data["status"] == "success":
            return data["output"][0]
        elif data["status"] == "failed":
            raise Exception(data.get("message", "Failed"))

        time.sleep(5)
    raise Exception("Timeout")

# Usage
image_url = generate_image(
    "A futuristic cityscape at sunset, cyberpunk style, 8k, highly detailed",
    "your_api_key",
    model_id="flux"
)
print(f"Image: {image_url}")
```

## Image to Image Transformation

```python
def transform_image(init_image, prompt, api_key, model_id="flux", strength=0.7):
    """Transform an existing image based on a prompt.

    Args:
        init_image: URL of the input image
        prompt: How to transform the image
        model_id: Model to use (flux models don't need scheduler, SD models do)
        strength: 0.0-1.0, higher = more change
    """
    payload = {
        "key": api_key,
        "model_id": model_id,
        "prompt": prompt,
        "init_image": [init_image],  # v7 expects array
        "strength": strength,
        "width": 512,
        "height": 512
    }

    response = requests.post(
        "https://modelslab.com/api/v7/images/image-to-image",
        json=payload
    )

    data = response.json()
    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_result(data["id"], api_key)

# Transform a photo into a painting
result = transform_image(
    "https://example.com/photo.jpg",
    "An oil painting in Van Gogh style",
    "your_api_key",
    model_id="flux",
    strength=0.8
)
```

## Inpainting (Fill Masked Regions)

```python
def inpaint_image(image_url, mask_url, prompt, api_key, model_id="flux"):
    """Fill in masked parts of an image.

    Args:
        image_url: Original image URL
        mask_url: Mask image URL (white = inpaint, black = keep)
        prompt: What to generate in masked area
        model_id: Model to use
    """
    response = requests.post(
        "https://modelslab.com/api/v7/images/inpaint",
        json={
            "key": api_key,
            "model_id": model_id,
            "init_image": image_url,
            "mask_image": mask_url,
            "prompt": prompt,
            "negative_prompt": "blurry, low quality"
        }
    )

    data = response.json()
    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_result(data["id"], api_key)

# Replace object in image
result = inpaint_image(
    "https://example.com/room.jpg",
    "https://example.com/mask.jpg",
    "A modern red sofa",
    "your_api_key",
    model_id="flux"
)
```

## Popular Model IDs

### Premium / Fast
- `flux` - Flux Dev (fast, high-quality, no scheduler needed)
- `imagen-3` - Google Imagen 3 (photorealistic)
- `imagen-4` - Google Imagen 4 (latest)

### Photorealistic
- `realistic-vision-v13` - High-quality realistic images
- `deliberate-v2` - Versatile realistic style
- `absolute-reality-v1.6` - Ultra-realistic outputs

### Artistic/Stylized
- `midjourney` - MidJourney-style images (most popular)
- `dreamshaper-8` - Artistic and versatile
- `openjourney` - Open-source MidJourney alternative

### Anime/Illustration
- `anything-v5` - Anime style
- `counterfeit-v2.5` - Anime portraits
- `meinamix` - High-quality anime art

Browse all models: https://modelslab.com/models

## Key Parameters

| Parameter | Description | Recommended Values |
|-----------|-------------|-------------------|
| `model_id` | Model to use (required) | `flux`, `midjourney`, `sdxl`, etc. |
| `prompt` | Text description of desired image | Be specific and detailed |
| `negative_prompt` | What to avoid | "blurry, low quality, distorted" |
| `width` / `height` | Dimensions (512-1024) | 512, 768, 1024 |
| `samples` | Number of images | 1-4 |
| `guidance_scale` | Prompt adherence | 7-8 (balanced), 10-15 (strict) |
| `seed` | Reproducibility | `null` (random) or number |
| `strength` | img2img change amount | 0.3 (subtle), 0.7 (moderate), 0.9 (heavy) |
| `webhook` | Async notification URL | URL string |
| `track_id` | Custom tracking identifier | Any string |

## Best Practices

### 1. Craft Effective Prompts
```
Bad: "a car"
Good: "A red Ferrari sports car, studio lighting, highly detailed, 4k, photorealistic"

Include: Subject, style, lighting, quality descriptors
```

### 2. Use Negative Prompts
```python
negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, extra limbs"
```

### 3. Choose Right Model
- **flux**: Fast, high quality, good default choice
- **midjourney**: Artistic, stylized outputs
- **imagen-3/4**: Premium photorealistic (Google)
- **sdxl**: Versatile base with many fine-tunes

### 4. Handle Async Operations
```python
# Always check status and poll if needed
if data["status"] == "processing":
    result = poll_result(data["id"], api_key)
```

### 5. Use Webhooks for Long Operations
```python
payload = {
    "key": api_key,
    "prompt": "...",
    "webhook": "https://yourserver.com/webhook",
    "track_id": "unique-identifier"
}
```

## Error Handling

```python
try:
    image = generate_image(prompt, api_key)
    print(f"Success: {image}")
except Exception as e:
    print(f"Generation failed: {e}")
    # Log error, retry, or notify user
```

## Resources

- **API Documentation**: https://docs.modelslab.com/image-generation/overview
- **Model Library**: https://modelslab.com/models
- **Model Selection Guide**: https://docs.modelslab.com/guides/model-selection
- **Get API Key**: https://modelslab.com/dashboard
- **Community**: https://discord.gg/modelslab

## Related Skills

- `modelslab-model-discovery` - Find and filter models
- `modelslab-image-editing` - Edit and enhance images
- `modelslab-video-generation` - Generate videos from images
- `modelslab-chat-generation` - Chat with LLM models
- `modelslab-webhooks` - Async operation handling
- `modelslab-sdk-usage` - Use official SDKs
