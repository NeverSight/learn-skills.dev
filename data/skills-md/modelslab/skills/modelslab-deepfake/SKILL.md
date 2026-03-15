---
name: modelslab-deepfake
description: Face swap and deepfake generation using ModelsLab's Deepfake API. Swap faces in images and videos with high-quality AI-powered face replacement technology.
---

# ModelsLab Deepfake & Face Swap

Swap faces in images and videos using advanced AI-powered deepfake technology.

## When to Use This Skill

- Swap faces in photos
- Replace faces in videos
- Create personalized video content
- Generate character variations
- Build face swap applications
- Create entertainment content

## Available Endpoints

### Image Face Swap
- **Specific Face Swap**: `POST https://modelslab.com/api/v6/deepfake/specific_face_swap`
- **Multiple Face Swap**: `POST https://modelslab.com/api/v6/deepfake/multiple_face_swap`

### Video Face Swap
- **Single Video Swap**: `POST https://modelslab.com/api/v6/deepfake/single_video_swap`
- **Specific Video Swap**: `POST https://modelslab.com/api/v6/deepfake/specific_video_swap`

## Specific Face Swap (Image)

```python
import requests

def swap_face(target_image, face_to_use, api_key):
    """Swap a face in an image.

    Args:
        target_image: URL of the image containing face to replace
        face_to_use: URL of the image with face to swap in
        api_key: Your ModelsLab API key

    Returns:
        URL of the face-swapped image
    """
    response = requests.post(
        "https://modelslab.com/api/v6/deepfake/specific_face_swap",
        json={
            "key": api_key,
            "init_image": target_image,
            "target_image": face_to_use
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(f"Error: {data.get('message', 'Unknown error')}")

# Usage
result = swap_face(
    "https://example.com/target-photo.jpg",  # Photo to modify
    "https://example.com/face-to-swap.jpg",  # Face to insert
    "your_api_key"
)
print(f"Face swapped image: {result}")
```

## Multiple Face Swap (Image)

```python
def swap_multiple_faces(image_with_faces, face_to_use, api_key):
    """Swap all faces in an image with the same face.

    Args:
        image_with_faces: URL of image with multiple faces
        face_to_use: URL of face to swap in
    """
    response = requests.post(
        "https://modelslab.com/api/v6/deepfake/multiple_face_swap",
        json={
            "key": api_key,
            "init_image": image_with_faces,
            "target_image": face_to_use
        }
    )

    data = response.json()

    if data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Swap all faces in group photo
result = swap_multiple_faces(
    "https://example.com/group-photo.jpg",
    "https://example.com/celebrity-face.jpg",
    "your_api_key"
)
```

## Single Video Face Swap

```python
import time

def swap_video_faces(video_url, face_image, api_key, output_format="mp4"):
    """Swap all faces in a video.

    Args:
        video_url: URL of the video
        face_image: URL of face to swap in
        output_format: "mp4" or "gif"

    Returns:
        URL of the face-swapped video
    """
    response = requests.post(
        "https://modelslab.com/api/v6/deepfake/single_video_swap",
        json={
            "key": api_key,
            "init_video": video_url,
            "target_image": face_image,
            "output_format": output_format,
            "watermark": False  # Set to True for watermark
        }
    )

    data = response.json()

    if data["status"] == "error":
        raise Exception(f"Error: {data['message']}")

    if data["status"] == "success":
        return data["output"][0]

    # Video processing is async
    request_id = data["id"]
    print(f"Video processing... Request ID: {request_id}")

    return poll_deepfake_result(request_id, api_key)

def poll_deepfake_result(request_id, api_key, timeout=900):
    """Poll for video face swap results."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        fetch = requests.post(
            f"https://modelslab.com/api/v6/deepfake/fetch/{request_id}",
            json={"key": api_key}
        )
        result = fetch.json()

        if result["status"] == "success":
            return result["output"][0]
        elif result["status"] == "failed":
            raise Exception(result.get("message", "Failed"))

        print(f"Processing... ({int(time.time() - start_time)}s)")
        time.sleep(10)

    raise Exception("Timeout")

# Usage
swapped_video = swap_video_faces(
    "https://example.com/video.mp4",
    "https://example.com/face.jpg",
    "your_api_key"
)
print(f"Face-swapped video: {swapped_video}")
```

## Specific Video Face Swap

```python
def swap_specific_video_face(video_url, new_face, reference_face, api_key):
    """Swap a specific face in a video (when multiple faces present).

    Args:
        video_url: URL of the video
        new_face: URL of the face to swap in
        reference_face: URL of the specific face to replace
    """
    response = requests.post(
        "https://modelslab.com/api/v6/deepfake/specific_video_swap",
        json={
            "key": api_key,
            "init_video": video_url,
            "target_image": new_face,
            "source_image": reference_face,
            "output_format": "mp4",
            "watermark": False
        }
    )

    data = response.json()

    if data["status"] == "processing":
        return poll_deepfake_result(data["id"], api_key)
    elif data["status"] == "success":
        return data["output"][0]
    else:
        raise Exception(data.get("message"))

# Swap only one person's face in multi-person video
result = swap_specific_video_face(
    "https://example.com/interview.mp4",
    "https://example.com/new-face.jpg",
    "https://example.com/face-to-replace.jpg",
    "your_api_key"
)
```

## Using Webhooks

```python
def deepfake_with_webhook(video_url, face_image, api_key, webhook_url, track_id):
    """Process video face swap with webhook notification."""
    response = requests.post(
        "https://modelslab.com/api/v6/deepfake/single_video_swap",
        json={
            "key": api_key,
            "init_video": video_url,
            "target_image": face_image,
            "output_format": "mp4",
            "webhook": webhook_url,
            "track_id": track_id
        }
    )

    data = response.json()
    print(f"Request submitted: {data['id']}")
    return data["id"]

# Usage
request_id = deepfake_with_webhook(
    "https://example.com/video.mp4",
    "https://example.com/face.jpg",
    "your_api_key",
    "https://yourserver.com/webhook/deepfake",
    "video_001"
)
```

## Key Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `init_image` | Target image to modify | Image URL |
| `init_video` | Target video to modify | Video URL |
| `target_image` | Face to swap in | Image URL with clear face |
| `source_image` | Specific face to replace | Image URL (for specific swap) |
| `output_format` | Video output format | `mp4` or `gif` |
| `watermark` | Add watermark | `true` or `false` |
| `webhook` | Async callback URL | Your server endpoint |
| `track_id` | Request identifier | Unique tracking ID |

## Best Practices

### 1. Use High-Quality Face Images
```
✓ Good: Clear, well-lit frontal face photo
✓ Good: High resolution (at least 512x512)
✓ Good: Neutral expression works best

✗ Avoid: Blurry or low-resolution images
✗ Avoid: Extreme angles or profiles
✗ Avoid: Heavy shadows or poor lighting
```

### 2. Video Face Swap Requirements
- Clear, visible faces in the video
- Good lighting conditions
- Frontal or near-frontal angles work best
- Shorter videos process faster

### 3. Handle Async Operations
```python
# Video face swaps are ALWAYS async
if data["status"] == "processing":
    result = poll_deepfake_result(data["id"], api_key)
```

### 4. Set Appropriate Timeouts
```python
# Video processing takes time
poll_deepfake_result(request_id, api_key, timeout=900)  # 15 minutes
```

### 5. Use Webhooks for Long Videos
```python
# Don't poll for long videos, use webhooks
deepfake_with_webhook(video_url, face, api_key, webhook_url, track_id)
```

## Common Use Cases

### Profile Picture Generator

```python
def create_profile_variations(base_photo, face_images, api_key):
    """Generate multiple profile picture variations."""
    variations = []

    for i, face in enumerate(face_images):
        result = swap_face(base_photo, face, api_key)
        variations.append(result)
        print(f"Variation {i+1} created: {result}")

    return variations

# Create variations
profiles = create_profile_variations(
    "https://example.com/professional-photo.jpg",
    [
        "https://example.com/style1-face.jpg",
        "https://example.com/style2-face.jpg",
        "https://example.com/style3-face.jpg"
    ],
    api_key
)
```

### Video Personalization

```python
def personalize_video(template_video, user_face, api_key):
    """Create personalized video with user's face."""
    personalized = swap_video_faces(
        template_video,
        user_face,
        api_key,
        output_format="mp4"
    )
    print(f"Personalized video: {personalized}")
    return personalized

# Create custom greeting video
greeting = personalize_video(
    "https://example.com/greeting-template.mp4",
    "https://example.com/user-photo.jpg",
    api_key
)
```

### Character Variations

```python
def generate_character_variations(character_image, face_options, api_key):
    """Generate different character variations."""
    characters = []

    for face in face_options:
        char = swap_face(character_image, face, api_key)
        characters.append(char)

    return characters
```

### Group Photo Editing

```python
# Replace one person in group photo
edited_group_photo = swap_specific_video_face(
    "https://example.com/group-video.mp4",
    "https://example.com/replacement-face.jpg",
    "https://example.com/person-to-replace.jpg",
    api_key
)
```

## Error Handling

```python
try:
    result = swap_face(target, face, api_key)
    print(f"Face swap successful: {result}")
except Exception as e:
    print(f"Face swap failed: {e}")
    # Check image quality, try different images, or notify user
```

## Performance Tips

1. **Use Webhooks**: For videos, always use webhooks
2. **Optimize Face Images**: Use clear, high-quality faces
3. **Batch Process**: Submit multiple requests together
4. **Cache Results**: Store generated content
5. **Monitor Processing Time**: Track and optimize

## Ethical Considerations

⚠️ **Important**: Use face swap technology responsibly
- Obtain consent before using someone's face
- Don't create misleading or harmful content
- Follow local laws and regulations
- Respect privacy and image rights
- Add disclaimers when sharing deepfake content

## Enterprise API

For dedicated resources:

```python
# Enterprise endpoints
url = "https://modelslab.com/api/v1/enterprise/deepfake/specific_face_swap"
url = "https://modelslab.com/api/v1/enterprise/deepfake/single_video_swap"
```

## Resources

- **Deepfake API Docs**: https://docs.modelslab.com/deepfake-api/overview
- **Face Swap Image**: https://docs.modelslab.com/deepfake-api/specific-face-swap
- **Video Face Swap**: https://docs.modelslab.com/deepfake-api/single-video-swap
- **Get API Key**: https://modelslab.com/dashboard

## Related Skills

- `modelslab-video-generation` - Generate videos
- `modelslab-webhooks` - Handle async operations
- `modelslab-sdk-usage` - Use official SDKs
