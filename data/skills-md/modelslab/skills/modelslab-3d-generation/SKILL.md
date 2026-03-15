---
name: modelslab-3d-generation
description: Generate 3D models and objects from text prompts or images using ModelsLab's 3D API. Transform 2D images into 3D representations or create 3D objects from text descriptions.
---

# ModelsLab 3D Generation

Transform text descriptions and 2D images into 3D models using AI-powered 3D generation.

## When to Use This Skill

- Generate 3D models from text descriptions
- Convert 2D images to 3D representations
- Create 3D assets for games or applications
- Prototype 3D objects quickly
- Generate 3D product mockups
- Create 3D characters from photos

## Available Endpoints

### Text to 3D
`POST https://modelslab.com/api/v6/3d/text_to_3d`

### Image to 3D
`POST https://modelslab.com/api/v6/3d/image_to_3d`

## Text to 3D

```python
import requests
import time

def text_to_3d(prompt, api_key, num_inference_steps=50):
    """Generate a 3D object from a text prompt.

    Args:
        prompt: Text description of the 3D object
        api_key: Your ModelsLab API key
        num_inference_steps: Quality (higher = better, slower)

    Returns:
        URL of the 3D model file
    """
    response = requests.post(
        "https://modelslab.com/api/v6/3d/text_to_3d",
        json={
            "key": api_key,
            "prompt": prompt,
            "num_inference_steps": num_inference_steps
        }
    )

    data = response.json()

    if data["status"] == "error":
        raise Exception(f"Error: {data['message']}")

    if data["status"] == "success":
        return data["output"][0]

    # 3D generation is async - poll for results
    request_id = data["id"]
    print(f"3D generation started... Request ID: {request_id}")
    print(f"ETA: {data.get('eta', 'unknown')} seconds")

    return poll_3d_result(request_id, api_key)

def poll_3d_result(request_id, api_key, timeout=600):
    """Poll for 3D generation results."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        fetch = requests.post(
            f"https://modelslab.com/api/v6/3d/fetch/{request_id}",
            json={"key": api_key}
        )
        result = fetch.json()

        if result["status"] == "success":
            return result["output"][0]
        elif result["status"] == "failed":
            raise Exception(result.get("message", "Generation failed"))

        print(f"Status: processing... ({int(time.time() - start_time)}s elapsed)")
        time.sleep(10)

    raise Exception("Timeout waiting for 3D generation")

# Usage
model_url = text_to_3d(
    "A medieval sword with ornate handle and detailed engravings",
    "your_api_key",
    num_inference_steps=50
)
print(f"3D model ready: {model_url}")
```

## Image to 3D

```python
def image_to_3d(image_url, api_key):
    """Convert a 2D image into a 3D model.

    Args:
        image_url: URL of the 2D image
        api_key: Your ModelsLab API key

    Returns:
        URL of the generated 3D model
    """
    response = requests.post(
        "https://modelslab.com/api/v6/3d/image_to_3d",
        json={
            "key": api_key,
            "image": image_url
        }
    )

    data = response.json()

    if data["status"] == "error":
        raise Exception(f"Error: {data['message']}")

    if data["status"] == "success":
        return data["output"][0]

    # Poll for results
    request_id = data["id"]
    print(f"Converting image to 3D... Request ID: {request_id}")

    return poll_3d_result(request_id, api_key)

# Convert product photo to 3D
model_url = image_to_3d(
    "https://example.com/product-photo.jpg",
    "your_api_key"
)
print(f"3D model: {model_url}")
```

## Using Webhooks

```python
def generate_3d_with_webhook(prompt, api_key, webhook_url, track_id):
    """Generate 3D model and receive results via webhook."""
    response = requests.post(
        "https://modelslab.com/api/v6/3d/text_to_3d",
        json={
            "key": api_key,
            "prompt": prompt,
            "num_inference_steps": 50,
            "webhook": webhook_url,
            "track_id": track_id
        }
    )

    data = response.json()
    print(f"Request submitted: {data['id']}")
    return data["id"]

# Usage
request_id = generate_3d_with_webhook(
    "A futuristic sci-fi weapon",
    "your_api_key",
    "https://yourserver.com/webhook/3d",
    "model_001"
)
```

## Key Parameters

| Parameter | Description | Recommended Values |
|-----------|-------------|-------------------|
| `prompt` | Text description of 3D object | Be specific about shape, style, details |
| `image` | 2D image URL for conversion | Clear, well-lit product photo |
| `num_inference_steps` | Quality vs speed | 30 (fast), 50 (balanced), 100 (quality) |
| `webhook` | Async callback URL | Your server endpoint |
| `track_id` | Request identifier | Unique ID for tracking |

## Best Practices

### 1. Craft Effective 3D Prompts
```
✗ Bad: "a chair"
✓ Good: "A modern office chair with ergonomic design, armrests, five wheels, mesh back"

Include: Type, style, materials, key features, details
```

### 2. Image to 3D Requirements
- Use clear, well-lit images
- Single object on plain background works best
- Multiple angles help (if supported)
- High resolution input recommended

### 3. Set Realistic Expectations
- 3D generation takes 5-15 minutes
- Quality depends on input quality
- Complex objects may need refinement
- Best for simple to moderate complexity

### 4. Always Use Async Pattern
```python
# 3D generation is ALWAYS async
if data["status"] == "processing":
    result = poll_3d_result(data["id"], api_key)
```

### 5. Handle Long Wait Times
```python
# Use longer timeouts for 3D
poll_3d_result(request_id, api_key, timeout=900)  # 15 minutes

# Or use webhooks
generate_3d_with_webhook(prompt, api_key, webhook_url, track_id)
```

## Common Use Cases

### Game Assets

```python
# Generate weapon
sword = text_to_3d(
    "Fantasy sword with glowing blue blade, ornate gold handle, medieval style",
    api_key,
    num_inference_steps=75
)

# Generate character prop
shield = text_to_3d(
    "Round wooden shield with iron rim and clan emblem in center",
    api_key
)
```

### Product Prototyping

```python
# Create product mockup
prototype = text_to_3d(
    "Modern wireless earbuds with charging case, minimalist design, matte white finish",
    api_key,
    num_inference_steps=100
)
```

### E-commerce 3D Models

```python
# Convert product photo to 3D
def create_product_3d_view(product_image_url, api_key):
    """Generate 3D model from product photo."""
    model = image_to_3d(product_image_url, api_key)
    print(f"3D product view ready: {model}")
    return model

product_3d = create_product_3d_view(
    "https://example.com/product.jpg",
    api_key
)
```

### Architectural Elements

```python
# Generate furniture
furniture = text_to_3d(
    "Modern minimalist coffee table, glass top, wooden legs, Scandinavian design",
    api_key
)

# Generate decorations
vase = text_to_3d(
    "Ceramic vase with geometric pattern, blue and white colors, modern style",
    api_key
)
```

## Batch Generation

```python
def generate_multiple_3d_models(prompts, api_key):
    """Generate multiple 3D models in batch."""
    request_ids = []

    # Submit all requests
    for i, prompt in enumerate(prompts):
        response = requests.post(
            "https://modelslab.com/api/v6/3d/text_to_3d",
            json={
                "key": api_key,
                "prompt": prompt,
                "webhook": "https://yourserver.com/webhook/3d",
                "track_id": f"batch_{i}"
            }
        )
        request_ids.append(response.json()["id"])
        print(f"Submitted: {prompt}")

    print(f"All {len(prompts)} requests submitted")
    return request_ids

# Generate multiple assets
models = generate_multiple_3d_models([
    "Medieval sword",
    "Knight's helmet",
    "Wooden shield",
    "Battle axe"
], api_key)
```

## Error Handling

```python
try:
    model = text_to_3d(prompt, api_key)
    print(f"3D model generated: {model}")
except Exception as e:
    print(f"3D generation failed: {e}")
    # Log error, retry with simpler prompt, notify user
```

## Output Formats

The API returns 3D model files in common formats:
- `.glb` (glTF Binary)
- `.obj` (Wavefront OBJ)
- `.fbx` (Filmbox)

Check the response for specific format details.

## Performance Tips

1. **Use Webhooks**: Don't poll continuously
2. **Batch Similar Requests**: Generate multiple models together
3. **Cache Results**: Store generated models for reuse
4. **Start Simple**: Test with simple objects first
5. **Monitor Generation Time**: Track and optimize

## Enterprise API

For dedicated resources:

```python
# Enterprise endpoints
text_to_3d_url = "https://modelslab.com/api/v1/enterprise/3d/text_to_3d"
image_to_3d_url = "https://modelslab.com/api/v1/enterprise/3d/image_to_3d"
```

## Resources

- **3D API Documentation**: https://docs.modelslab.com/3d-api/overview
- **Text to 3D**: https://docs.modelslab.com/3d-api/text-to-3d
- **Image to 3D**: https://docs.modelslab.com/3d-api/image-to-3d
- **Get API Key**: https://modelslab.com/dashboard

## Related Skills

- `modelslab-image-generation` - Generate images for image-to-3D
- `modelslab-webhooks` - Handle async 3D generation
- `modelslab-sdk-usage` - Use official SDKs
