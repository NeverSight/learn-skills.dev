---
name: modelscope-api
description: This skill should be used when the user asks to "call ModelScope API", "generate images with ModelScope", "configure ModelScope", or mentions ModelScope API endpoints, authentication, async task polling, or image generation workflows. Provides comprehensive guidance for ModelScope image generation API integration.
---

# ModelScope API Integration

This skill provides comprehensive knowledge for integrating with ModelScope's image generation API, including authentication, async task handling, and error management.

## Core Concepts

ModelScope provides an async image generation API that requires:
1. API authentication via Bearer token
2. Async task submission and polling
3. Image retrieval and local storage

## API Endpoints

### Base URL
```
https://api-inference.modelscope.cn/
```

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/images/generations` | POST | Submit image generation task |
| `/v1/tasks/{task_id}` | GET | Poll task status |
| `/v1/tasks/{task_id}/result` | GET | Retrieve completed image |

## Authentication

All requests require the `Authorization` header:

```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
```

The API key is stored in `~/.modelscope-image-gen/modelscope-image-gen.local.md` configuration file.

## Image Generation Workflow

### Step 1: Submit Generation Request

Submit an async image generation request:

```python
response = requests.post(
    f"{base_url}v1/images/generations",
    headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
    data=json.dumps({
        "model": "Tongyi-MAI/Z-Image-Turbo",
        "prompt": "A golden cat"
    }, ensure_ascii=False).encode('utf-8')
)

task_id = response.json()["task_id"]
```

### Step 2: Poll Task Status

Continuously poll until completion:

```python
while True:
    result = requests.get(
        f"{base_url}v1/tasks/{task_id}",
        headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
    )
    data = result.json()

    if data.get("status") == "succeeded":
        break
    elif data.get("status") == "failed":
        raise Exception(data.get("error", "Generation failed"))

    time.sleep(2)
```

### Step 3: Retrieve Image

Extract and save the generated image:

```python
image_url = data["result"]["url"]
image_response = requests.get(image_url)
img = Image.open(BytesIO(image_response.content))
img.save(f"{output_dir}/{filename}.png")
```

## Request Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | ModelScope model ID (e.g., "Tongyi-MAI/Z-Image-Turbo") |
| `prompt` | string | Image generation prompt |

### Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | int | Image width (default: 1024) |
| `height` | int | Image height (default: 1024) |
| `num_inference_steps` | int | Number of inference steps |

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API token | Check token in configuration |
| 429 Rate Limit | Too many requests | Wait and retry |
| 500 Internal Error | Server error | Retry with exponential backoff |
| Timeout | Task taking too long | Increase timeout setting |

### Retry Strategy

Implement exponential backoff for retries:

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.post(...)
        break
    except requests.exceptions.RequestException as e:
        if attempt == max_retries - 1:
            raise
        wait_time = 2 ** attempt
        time.sleep(wait_time)
```

## Additional Resources

### Utility Scripts

The following scripts are available in this skill:
- **`scripts/image-gen.py`** - Complete image generation implementation with async polling and error handling

### Example Files

Working examples in `examples/`:
- **`batch-prompts.txt`** - Example batch generation prompts

## Configuration Management

Read configuration from `~/.modelscope-image-gen/modelscope-image-gen.local.md`:

```python
import yaml
import re
from pathlib import Path

def read_config():
    config_dir = Path.home() / ".modelscope-image-gen"
    config_path = config_dir / "modelscope-image-gen.local.md"

    with open(config_path, 'r') as f:
        content = f.read()

    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        config = yaml.safe_load(match.group(1))
        return config.get('api_key'), config.get('default_model', 'Tongyi-MAI/Z-Image-Turbo')

    raise Exception("Invalid configuration file")
```

## Best Practices

1. **Always use async mode** for image generation to handle long-running tasks
2. **Implement timeout handling** to prevent indefinite polling
3. **Save images immediately** after successful retrieval
4. **Handle rate limiting** with proper backoff strategies
5. **Validate prompts** before submission to avoid wasted API calls
6. **Log all API interactions** for debugging and monitoring
