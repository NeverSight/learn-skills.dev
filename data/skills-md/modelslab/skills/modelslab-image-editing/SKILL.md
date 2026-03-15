---
name: modelslab-image-editing
description: Edit and enhance images using ModelsLab's Image Editing API. Features background removal, super resolution upscaling, outpainting, object removal, and AI-powered editing tools.
---

# ModelsLab Image Editing

Professional image editing tools powered by AI including background removal, upscaling, outpainting, and object manipulation.

## When to Use This Skill

- Remove backgrounds from images
- Upscale images (2x, 4x super resolution)
- Extend images beyond their borders (outpainting)
- Remove unwanted objects from images
- Create professional product photos
- Enhance image quality
- Edit images with AI assistance

## Available Endpoints

### Background Removal
`POST https://modelslab.com/api/v6/image_editing/removebg`

### Super Resolution (Upscaling)
`POST https://modelslab.com/api/v6/image_editing/super_resolution`

### Outpainting
`POST https://modelslab.com/api/v6/image_editing/outpainting`

### Object Removal
`POST https://modelslab.com/api/v6/image_editing/object_removal`

### Mask Creator
`POST https://modelslab.com/api/v6/image_editing/create_mask`

### Qwen Image Edit (AI Editing)
`POST https://modelslab.com/api/v6/image_editing/qwen_edit`

## Background Removal

```python
import requests

def remove_background(image_url, api_key):
    """Remove background from an image.

    Args:
        image_url: URL of the image
        api_key: Your ModelsLab API key

    Returns:
        URL of image with transparent background
    """
    response = requests.post(
        "https://modelslab.com/api/v6/image_editing/removebg",
        json={
            "key": api_key,
            "image": image_url
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(f"Error: {data.get('message', 'Unknown error')}")

# Usage
result = remove_background(
    "https://example.com/product-photo.jpg",
    "your_api_key"
)
print(f"Image without background: {result}")
```

## Super Resolution (Upscaling)

```python
def upscale_image(image_url, api_key, scale=4):
    """Upscale an image to higher resolution.

    Args:
        image_url: URL of the image to upscale
        scale: Upscale factor (2 or 4)

    Returns:
        URL of upscaled high-resolution image
    """
    response = requests.post(
        "https://modelslab.com/api/v6/image_editing/super_resolution",
        json={
            "key": api_key,
            "image": image_url,
            "scale": scale  # 2x or 4x
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Upscale to 4x resolution
hd_image = upscale_image(
    "https://example.com/low-res.jpg",
    "your_api_key",
    scale=4
)
print(f"HD image: {hd_image}")
```

## Outpainting (Extend Images)

```python
def extend_image(image_url, prompt, api_key, width=1024, height=768):
    """Extend an image beyond its original boundaries.

    Args:
        image_url: Original image URL
        prompt: Description of how to extend the image
        width: New width (larger than original)
        height: New height (larger than original)
    """
    response = requests.post(
        "https://modelslab.com/api/v6/image_editing/outpainting",
        json={
            "key": api_key,
            "image": image_url,
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_result(data["id"], api_key)

# Extend a landscape image
extended = extend_image(
    "https://example.com/landscape.jpg",
    "Continue the mountain landscape with more peaks and valleys",
    "your_api_key",
    width=1024,
    height=768
)
```

## Object Removal

```python
def remove_object(image_url, object_name, api_key):
    """Remove a specific object from an image.

    Args:
        image_url: URL of the image
        object_name: Name of object to remove (e.g., "person", "car", "sign")
    """
    response = requests.post(
        "https://modelslab.com/api/v6/image_editing/object_removal",
        json={
            "key": api_key,
            "image": image_url,
            "object_name": object_name
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_result(data["id"], api_key)

# Remove person from photo
cleaned = remove_object(
    "https://example.com/photo.jpg",
    "person in background",
    "your_api_key"
)
```

## AI-Powered Image Editing (Qwen)

```python
def edit_image_with_ai(image_url, edit_instruction, api_key):
    """Edit image using AI instructions.

    Args:
        image_url: URL of the image to edit
        edit_instruction: Natural language editing instruction
    """
    response = requests.post(
        "https://modelslab.com/api/v6/image_editing/qwen_edit",
        json={
            "key": api_key,
            "image": image_url,
            "prompt": edit_instruction,
            "negative_prompt": "low quality, distorted",
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    elif data["status"] == "processing":
        return poll_result(data["id"], api_key)

# AI-powered editing
edited = edit_image_with_ai(
    "https://example.com/portrait.jpg",
    "Make the background more blurred and add warm sunset lighting",
    "your_api_key"
)
```

## Create Mask

```python
def create_object_mask(image_url, object_description, api_key):
    """Create a mask for a specific object in an image.

    Args:
        image_url: URL of the image
        object_description: What to mask (e.g., "person", "car", "background")

    Returns:
        URL of mask image (white = selected, black = not selected)
    """
    response = requests.post(
        "https://modelslab.com/api/v6/image_editing/create_mask",
        json={
            "key": api_key,
            "image": image_url,
            "object": object_description
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]

# Create mask for person
mask_url = create_object_mask(
    "https://example.com/group-photo.jpg",
    "person in red shirt",
    "your_api_key"
)
```

## Polling Helper

```python
import time

def poll_result(request_id, api_key, timeout=300):
    """Poll for async editing results."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        fetch = requests.post(
            f"https://modelslab.com/api/v6/image_editing/fetch/{request_id}",
            json={"key": api_key}
        )
        result = fetch.json()

        if result["status"] == "success":
            return result["output"][0]
        elif result["status"] == "failed":
            raise Exception(result.get("message", "Failed"))

        time.sleep(5)

    raise Exception("Timeout")
```

## Common Workflows

### E-commerce Product Photos

```python
def prepare_product_image(image_url, api_key):
    """Complete product photo workflow."""

    # Step 1: Remove background
    no_bg = remove_background(image_url, api_key)
    print(f"Background removed: {no_bg}")

    # Step 2: Upscale to high resolution
    hd_image = upscale_image(no_bg, api_key, scale=4)
    print(f"Upscaled: {hd_image}")

    return hd_image

product_image = prepare_product_image(
    "https://example.com/product.jpg",
    "your_api_key"
)
```

### Photo Cleanup

```python
def cleanup_photo(image_url, unwanted_objects, api_key):
    """Remove multiple unwanted objects from photo."""

    cleaned_image = image_url

    for obj in unwanted_objects:
        cleaned_image = remove_object(cleaned_image, obj, api_key)
        print(f"Removed: {obj}")

    # Upscale final result
    final = upscale_image(cleaned_image, api_key, scale=2)

    return final

result = cleanup_photo(
    "https://example.com/vacation.jpg",
    ["power lines", "trash can", "stranger in background"],
    "your_api_key"
)
```

### Extend and Enhance

```python
def extend_and_enhance(image_url, extension_prompt, api_key):
    """Extend image and upscale result."""

    # Extend the image
    extended = extend_image(
        image_url,
        extension_prompt,
        api_key,
        width=1920,
        height=1080
    )

    # Upscale for maximum quality
    final = upscale_image(extended, api_key, scale=2)

    return final
```

## Best Practices

### 1. Background Removal
- Works best with clear subject separation
- Good lighting in original image helps
- High-quality input = better output

### 2. Super Resolution
- Use 2x for moderate upscaling
- Use 4x for maximum quality boost
- Don't upscale already high-res images
- Best results with clear, focused images

### 3. Outpainting
- Be specific in extension prompts
- Match style of original image
- Consider composition when extending
- Test different sizes

### 4. Object Removal
- Be specific about object location
- Works best with simple backgrounds
- May need multiple passes for complex scenes

### 5. Use Webhooks for Batch Operations
```python
# Process many images
for image in image_list:
    response = requests.post(
        endpoint,
        json={
            "key": api_key,
            "image": image,
            "webhook": "https://yourserver.com/callback",
            "track_id": f"img_{image_id}"
        }
    )
```

## Common Use Cases

### Professional Headshots
```python
# Remove background and upscale
headshot = remove_background(original, api_key)
hd_headshot = upscale_image(headshot, api_key, scale=4)
```

### Real Estate Photos
```python
# Remove unwanted items
clean_room = remove_object(
    room_photo,
    "personal items and clutter",
    api_key
)

# Extend to show more space
wider_view = extend_image(
    clean_room,
    "Continue the modern living room with more furniture",
    api_key,
    width=1920,
    height=1080
)
```

### Social Media Graphics
```python
# Upscale for quality
high_res = upscale_image(graphic, api_key, scale=2)

# Extend to different aspect ratios
instagram_square = extend_image(
    high_res,
    "Extend background",
    api_key,
    width=1080,
    height=1080
)
```

## Error Handling

```python
try:
    result = remove_background(image_url, api_key)
    print(f"Success: {result}")
except Exception as e:
    print(f"Editing failed: {e}")
    # Log error, retry, or notify user
```

## Resources

- **API Documentation**: https://docs.modelslab.com/image-editing/overview
- **Background Removal**: https://docs.modelslab.com/image-editing/removebg-createmask
- **Super Resolution**: https://docs.modelslab.com/image-editing/super-resolution
- **Get API Key**: https://modelslab.com/dashboard

## Related Skills

- `modelslab-image-generation` - Generate images to edit
- `modelslab-webhooks` - Handle async operations
- `modelslab-sdk-usage` - Use official SDKs
