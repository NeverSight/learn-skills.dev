---
name: grok-api
description: Call Grok LLM models (grok-3, grok-3-fast, grok-3-mini, etc.) and generate images/videos via an OpenAI-compatible API proxy. Use this skill whenever the user wants to chat with Grok, generate text, create images, or generate videos.
---

# Grok API (via grok2api)

OpenAI-compatible Grok API proxy hosted at `https://mc.agaii.org/grok`. Use this skill whenever the user asks you to call Grok models, generate text with Grok, or interact with the Grok API.

## Overview

- **Base URL:** `https://mc.agaii.org/grok/v1`
- **Auth header:** `Authorization: Bearer <app_key>`
- **Protocol:** OpenAI-compatible (drop-in replacement for `openai` SDK)
- **Admin panel:** `https://mc.agaii.org/grok/admin/login`

The API supports chat completions, streaming, and all standard OpenAI-compatible parameters.

## Step 0: Confirm Credentials

Before making any call, confirm the app key is available. The key is used as a Bearer token:

```bash
# Verify the key works
curl -s https://mc.agaii.org/grok/v1/models \
  -H "Authorization: Bearer <app_key>"
```

A successful response lists available Grok models.

## Step 1: Choose a Model

Use `GET /v1/models` to list available models, or pick from the well-known ones:

| Model | Description |
|-------|-------------|
| `grok-3` | Most capable, best for complex reasoning |
| `grok-3-fast` | Fast variant of Grok-3 |
| `grok-3-mini` | Lightweight, efficient |
| `grok-3-mini-fast` | Fastest, lowest latency |
| `grok-2-vision-1212` | Vision-capable model |

```bash
curl -s https://mc.agaii.org/grok/v1/models \
  -H "Authorization: Bearer <app_key>" | python3 -m json.tool
```

## Step 2: Chat Completions

### Non-streaming

```bash
curl -s -X POST https://mc.agaii.org/grok/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <app_key>" \
  -d '{
    "model": "grok-3",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain quantum entanglement in simple terms."}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
  }'
```

**Response shape:**
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "grok-3",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

### Streaming

```bash
curl -s -X POST https://mc.agaii.org/grok/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <app_key>" \
  -d '{
    "model": "grok-3",
    "messages": [{"role": "user", "content": "Write a haiku about the sea."}],
    "stream": true
  }'
```

Streaming returns `text/event-stream` Server-Sent Events. Each chunk is:
```
data: {"id":"...","object":"chat.completion.chunk","choices":[{"delta":{"content":"..."}}]}
```
The stream ends with `data: [DONE]`.

## Step 3: Using the Python Script

A ready-to-use Python script is available at `scripts/grok_api.py` in this skill directory.

Find it:
```bash
# If installed via npx skills add
ls .cursor/skills/GrokAgentSkill/scripts/grok_api.py
```

### Run examples

```bash
# Simple chat
python scripts/grok_api.py chat "What is the capital of France?"

# Chat with a specific model
python scripts/grok_api.py chat "Write a poem" --model grok-3-mini

# Streaming chat
python scripts/grok_api.py chat "Tell me a story" --stream

# Multi-turn conversation (JSON file)
python scripts/grok_api.py file scripts/example_messages.json

# List models
python scripts/grok_api.py models
```

Set the app key via environment variable (recommended):
```bash
export GROK_API_KEY=<app_key>
python scripts/grok_api.py chat "Hello"
```

Or pass inline:
```bash
python scripts/grok_api.py chat "Hello" --key <app_key>
```

## Step 4: Using the OpenAI Python SDK

The API is a drop-in replacement. Install: `pip install openai`

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://mc.agaii.org/grok/v1",
    api_key="<app_key>",
)

response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2 + 2?"},
    ],
)
print(response.choices[0].message.content)
```

### Streaming with SDK

```python
stream = client.chat.completions.create(
    model="grok-3",
    messages=[{"role": "user", "content": "Count to 5 slowly."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

### Async usage

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://mc.agaii.org/grok/v1",
    api_key="<app_key>",
)

async def main():
    response = await client.chat.completions.create(
        model="grok-3-fast",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## API Reference

### POST /v1/chat/completions

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model ID (e.g. `grok-3`) |
| `messages` | array | Yes | Array of `{role, content}` objects |
| `stream` | boolean | No | Enable SSE streaming (default: false) |
| `temperature` | float | No | Sampling temperature 0–2 (default: 1.0) |
| `max_tokens` | integer | No | Max tokens to generate |
| `top_p` | float | No | Nucleus sampling (default: 1.0) |
| `frequency_penalty` | float | No | -2.0 to 2.0 |
| `presence_penalty` | float | No | -2.0 to 2.0 |
| `stop` | string/array | No | Stop sequences |
| `n` | integer | No | Number of completions |
| `user` | string | No | End-user identifier |

### Message roles

| Role | Description |
|------|-------------|
| `system` | Sets assistant behavior/persona |
| `user` | Human turn |
| `assistant` | Previous assistant turn (for multi-turn) |

### GET /v1/models

Returns list of available models. No body required.

### Error codes

| Code | Meaning |
|------|---------|
| 401 | Invalid or missing API key |
| 429 | No available tokens / rate limited |
| 500 | Internal server error |

## Admin API

All admin endpoints require `Authorization: Bearer <app_key>`.

### List tokens
```bash
curl https://mc.agaii.org/grok/v1/admin/tokens \
  -H "Authorization: Bearer <app_key>"
```

### Add / update tokens
```bash
curl -X POST https://mc.agaii.org/grok/v1/admin/tokens \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <app_key>" \
  -d '{"ssoBasic": [{"token": "<sso_token>", "status": "active", "quota": 10, "created_at": 0, "use_count": 0, "fail_count": 0, "tags": [], "note": ""}]}'
```

### Refresh token quota
```bash
curl -X POST https://mc.agaii.org/grok/v1/admin/tokens/refresh \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <app_key>" \
  -d '{"token": "<sso_token>"}'
```

## Common Patterns

### System prompt + user message
```python
messages = [
    {"role": "system", "content": "You are an expert Python developer. Be concise."},
    {"role": "user", "content": "How do I read a file line by line in Python?"},
]
```

### Multi-turn conversation
```python
messages = [
    {"role": "user", "content": "My name is Alice."},
    {"role": "assistant", "content": "Nice to meet you, Alice!"},
    {"role": "user", "content": "What is my name?"},
]
```

### Low-latency use case
Use `grok-3-mini-fast` with `max_tokens` set to limit response length:
```python
client.chat.completions.create(
    model="grok-3-mini-fast",
    messages=[{"role": "user", "content": "Summarize in one sentence: ..."}],
    max_tokens=100,
)
```

### Structured output (JSON mode)
```python
client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "system", "content": "Always respond with valid JSON only."},
        {"role": "user", "content": "List 3 fruits with their colors as JSON."},
    ],
    temperature=0,
)
```

## Image Generation

Use model `grok-imagine-1.0` to generate images from a text prompt.

```bash
curl -s -X POST https://mc.agaii.org/grok/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <app_key>" \
  -d '{
    "model": "grok-imagine-1.0",
    "messages": [{"role": "user", "content": "A photorealistic red apple on a wooden table"}]
  }'
```

The response content will contain an `<img>` tag with a `src` URL pointing to the generated image.

**Parse the image URL from the response:**
```python
import re
content = response["choices"][0]["message"]["content"]
match = re.search(r'src="([^"]+)"', content)
image_url = match.group(1) if match else None
```

### Image editing

Use model `grok-imagine-1.0-edit` with an existing image URL in the prompt:

```bash
-d '{"model": "grok-imagine-1.0-edit", "messages": [{"role": "user", "content": "Make the apple golden. Image: https://..."}]}'
```

---

## Video Generation

Use model `grok-imagine-1.0-video` to generate short videos from a text prompt.

**Important:** The API streams progress updates as SSE chunks (percent complete), then delivers the final video URL embedded in HTML at 100%. You MUST stream the response and parse the final chunk for the video URL.

### Step-by-step workflow

**1. Submit the request (streaming required):**
```bash
curl -s -X POST https://mc.agaii.org/grok/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <app_key>" \
  -d '{
    "model": "grok-imagine-1.0-video",
    "messages": [{"role": "user", "content": "<your video prompt>"}]
  }' > /tmp/video_response.txt
```

**2. Extract the video URL from the streamed output:**
```bash
grep -oP 'src=\\"https://[^"]+\.mp4\\"' /tmp/video_response.txt | head -1 | grep -oP 'https://[^"\\]+'
```

Or in Python:
```python
import re, subprocess, json

# Run curl and capture all SSE lines
output = subprocess.check_output([
    "curl", "-s", "-X", "POST",
    "https://mc.agaii.org/grok/v1/chat/completions",
    "-H", "Content-Type: application/json",
    "-H", f"Authorization: Bearer {api_key}",
    "-d", json.dumps({
        "model": "grok-imagine-1.0-video",
        "messages": [{"role": "user", "content": prompt}]
    })
], timeout=300).decode()

# Extract video URL
match = re.search(r'src=\\"(https://[^"\\]+\.mp4)\\"', output)
video_url = match.group(1) if match else None
print("Video URL:", video_url)
```

**3. Download the video:**
```bash
wget -O output.mp4 "<video_url>"
# or
curl -L -o output.mp4 "<video_url>"
```

### Using the bundled script

```bash
GROK_API_KEY=<key> python scripts/grok_api.py video "A glowing figure rotating in the dark"
```

This will print the video URL when generation completes (typically takes 20–60 seconds).

### Progress tracking

During generation the API streams lines like:
```
正在生成视频中，当前进度1%
正在生成视频中，当前进度25%
...
正在生成视频中，当前进度100%
<video id="video" ...><source src="https://.../generated_video.mp4" ...></video>
```

The final content after 100% contains the `<video>` HTML with the mp4 URL and a preview image (poster).

### Preview image

The poster/thumbnail URL is also embedded:
```
poster="https://mc.agaii.org/grok/v1/files/image/.../preview_image.jpg"
```

Extract with:
```python
match = re.search(r'poster=\\"(https://[^"\\]+)\\"', output)
preview_url = match.group(1) if match else None
```

### Tips for good video prompts

- Describe **subject**, **motion**, **camera movement**, and **lighting** explicitly
- Mention **tone** (cinematic, futuristic, elegant, etc.)
- Keep prompts under 300 words
- Dark backgrounds with glowing elements tend to render well
- Specify duration feel with pacing words ("slowly pulls back", "quick cut", etc.)

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 429 "No available tokens" | Token pool empty or all cooling | Add more SSO tokens via admin API |
| 401 Unauthorized | Wrong app key | Check `Authorization: Bearer <key>` header |
| Connection refused | Server not running | Check service on port 15125 |
| Blank content in response | Model returned empty | Try again or reduce temperature |
| Token refresh returns `false` | SSO token expired | Remove token and add a fresh one |
