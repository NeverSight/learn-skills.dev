---
name: lovart
description: Lovart API for AI-powered design generation. Use when user mentions "Lovart", "AI design", "generate image", "generate video", "AI art", "product photography", "marketing design", or visual content creation.
---

## Troubleshooting

If requests fail, run `okou doctor check-connector --env-name LOVART_ACCESS_KEY` or `okou doctor check-connector --url https://lgw.lovart.ai/v1/openapi/mode/query --method POST`

## Authentication

All requests use AK/SK HMAC-SHA256 signature authentication. Each request requires five signed headers:

| Header | Value |
|---|---|
| `X-Access-Key` | `$LOVART_ACCESS_KEY` |
| `X-Timestamp` | Current Unix timestamp |
| `X-Signature` | HMAC-SHA256 of `{METHOD}\n{PATH}\n{TIMESTAMP}` using `$LOVART_SECRET_KEY` |
| `X-Signed-Method` | HTTP method (e.g. `POST`) |
| `X-Signed-Path` | Request path (e.g. `/v1/openapi/chat`) |

## Environment Variables

| Variable | Description |
|---|---|
| `LOVART_ACCESS_KEY` | Lovart access key (format: `ak_...`) |
| `LOVART_SECRET_KEY` | Lovart secret key (format: `sk_...`) |

## Key Endpoints

Base URL: `https://lgw.lovart.ai`

### 1. Generate Design (Chat)

`POST /v1/openapi/chat`

Send a natural-language prompt to generate images, videos, or other visual content. Returns a `thread_id` for tracking.

```bash
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "POST\n/v1/openapi/chat\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s -X POST "https://lgw.lovart.ai/v1/openapi/chat" --header "Content-Type: application/json" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: POST" --header "X-Signed-Path: /v1/openapi/chat" -d @/tmp/lovart_chat.json
```

Write to `/tmp/lovart_chat.json`:

```json
{
  "prompt": "<your-design-description>",
  "project_id": "<your-project-id>"
}
```

To continue a conversation, add `"thread_id": "<your-thread-id>"`.

To attach reference images, add `"attachments": ["<cdn-url>"]`.

To specify a preferred model, add `"tool_config": {"prefer_tool_categories": {"IMAGE": ["generate_image_flux_2_max"]}}`.

To force a specific tool (e.g. upscale), add `"tool_config": {"include_tools": ["upscale_image"]}`.

Response: `{"thread_id": "..."}`

### 2. Check Generation Status

`GET /v1/openapi/chat/status?thread_id=<thread-id>`

```bash
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "GET\n/v1/openapi/chat/status\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s "https://lgw.lovart.ai/v1/openapi/chat/status?thread_id=<your-thread-id>" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: GET" --header "X-Signed-Path: /v1/openapi/chat/status"
```

Response includes `status` (`running`, `done`, `pending_confirmation`, `failed`) and `progress` (0-100).

### 3. Get Generation Result

`GET /v1/openapi/chat/result?thread_id=<thread-id>`

```bash
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "GET\n/v1/openapi/chat/result\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s "https://lgw.lovart.ai/v1/openapi/chat/result?thread_id=<your-thread-id>" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: GET" --header "X-Signed-Path: /v1/openapi/chat/result"
```

Response includes `items` with generated artifacts (image URLs, video URLs) and `thread_id`.

### 4. Confirm High-Cost Operation

`POST /v1/openapi/chat/confirm`

When status is `pending_confirmation`, confirm to proceed with high-cost operations (e.g. video generation).

```bash
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "POST\n/v1/openapi/chat/confirm\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s -X POST "https://lgw.lovart.ai/v1/openapi/chat/confirm" --header "Content-Type: application/json" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: POST" --header "X-Signed-Path: /v1/openapi/chat/confirm" -d @/tmp/lovart_confirm.json
```

Write to `/tmp/lovart_confirm.json`:

```json
{
  "thread_id": "<your-thread-id>"
}
```

### 5. Create Project

`POST /v1/openapi/project/save`

```bash
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "POST\n/v1/openapi/project/save\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s -X POST "https://lgw.lovart.ai/v1/openapi/project/save" --header "Content-Type: application/json" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: POST" --header "X-Signed-Path: /v1/openapi/project/save" -d @/tmp/lovart_project.json
```

Write to `/tmp/lovart_project.json`:

```json
{
  "project_id": "",
  "project_name": "<your-project-name>",
  "project_type": 3
}
```

Response includes `project_id`. Use the returned ID in subsequent chat requests.

### 6. Set Generation Mode

`POST /v1/openapi/mode/set`

Switch between fast mode (costs credits, no queue) and unlimited mode (free, may queue).

```bash
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "POST\n/v1/openapi/mode/set\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s -X POST "https://lgw.lovart.ai/v1/openapi/mode/set" --header "Content-Type: application/json" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: POST" --header "X-Signed-Path: /v1/openapi/mode/set" -d @/tmp/lovart_mode.json
```

For fast mode, write to `/tmp/lovart_mode.json`:

```json
{
  "unlimited": false
}
```

For unlimited mode, write to `/tmp/lovart_mode.json`:

```json
{
  "unlimited": true
}
```

### 7. Query Generation Mode

`POST /v1/openapi/mode/query`

```bash
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "POST\n/v1/openapi/mode/query\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s -X POST "https://lgw.lovart.ai/v1/openapi/mode/query" --header "Content-Type: application/json" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: POST" --header "X-Signed-Path: /v1/openapi/mode/query" -d '{}'
```

## Available Models

Use model names in `tool_config.prefer_tool_categories` or `tool_config.include_tools`:

**IMAGE:** `generate_image_midjourney`, `generate_image_nano_banana_pro`, `generate_image_nano_banana_2`, `generate_image_nano_banana`, `generate_image_gpt_image_1_5`, `generate_image_seedream_v5`, `generate_image_seedream_v4_5`, `generate_image_seedream_v4`, `generate_image_imagen_v4`, `generate_image_flux_2_max`, `generate_image_flux_2_pro`

**VIDEO:** `generate_video_seedance_v2_0`, `generate_video_seedance_v2_0_fast`, `generate_video_seedance_pro_v1_5`, `generate_video_kling_v3`, `generate_video_kling_v3_omni`, `generate_video_kling_v2_6`, `generate_video_kling_omni_v1`, `generate_video_veo3_1`, `generate_video_veo3_1_fast`, `generate_video_veo3`, `generate_video_sora_v2_pro`, `generate_video_sora_v2`, `generate_video_wan_v2_6`, `generate_video_hailuo_v2_3`, `generate_video_vidu_q2`

**3D:** `generate_3d_tripo`

**UTILITY:** `upscale_image`

## Common Workflows

### Generate an Image and Retrieve the Result

```bash
# Step 1: Send chat request
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "POST\n/v1/openapi/chat\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s -X POST "https://lgw.lovart.ai/v1/openapi/chat" --header "Content-Type: application/json" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: POST" --header "X-Signed-Path: /v1/openapi/chat" -d '{"prompt": "A modern logo design with gradient blue to purple", "project_id": "<your-project-id>"}'

# Step 2: Poll status until done (replace <thread-id> from Step 1)
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "GET\n/v1/openapi/chat/status\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s "https://lgw.lovart.ai/v1/openapi/chat/status?thread_id=<your-thread-id>" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: GET" --header "X-Signed-Path: /v1/openapi/chat/status"

# Step 3: Get result when status is "done"
TIMESTAMP=$(date +%s) && SIGNATURE=$(echo -ne "GET\n/v1/openapi/chat/result\n${TIMESTAMP}" | openssl dgst -sha256 -hmac "$LOVART_SECRET_KEY" | awk '{print $NF}') && curl -s "https://lgw.lovart.ai/v1/openapi/chat/result?thread_id=<your-thread-id>" --header "X-Access-Key: $LOVART_ACCESS_KEY" --header "X-Timestamp: ${TIMESTAMP}" --header "X-Signature: ${SIGNATURE}" --header "X-Signed-Method: GET" --header "X-Signed-Path: /v1/openapi/chat/result"
```

### Upscale an Image

Use `include_tools` to force the upscale tool:

Write to `/tmp/lovart_chat.json`:

```json
{
  "prompt": "upscale this image to 4K",
  "project_id": "<your-project-id>",
  "attachments": ["<your-image-cdn-url>"],
  "tool_config": {
    "include_tools": ["upscale_image"]
  }
}
```

## Guidelines

1. **Signature freshness**: The HMAC signature includes a timestamp — recompute `TIMESTAMP` and `SIGNATURE` for every request, as the server rejects stale signatures
2. **Signed path must match**: The `X-Signed-Path` header must exactly match the request path (without query string), e.g. `/v1/openapi/chat` not `/v1/openapi/chat?thread_id=xxx`
3. **Polling**: Image generation typically takes 10-30s; video generation can take minutes — poll `chat/status` until `status` is `done`
4. **Pending confirmation**: When status is `pending_confirmation`, call `chat/confirm` before the generation proceeds — do NOT auto-confirm, ask the user first as it may cost credits
5. **Thread reuse**: Pass `thread_id` to continue a conversation — the Agent remembers prior context and can iterate on designs
6. **Project required**: All chat requests need a `project_id` — create one with `project/save` first or reuse an existing one
7. **Mode affects cost**: Fast mode (`unlimited: false`) uses credits for priority processing; unlimited mode (`unlimited: true`) is free but may queue

## API Reference

- Documentation: https://lovart.info/lovart-api
- Developer Guide: https://lovart.info/lovart-ai-code
