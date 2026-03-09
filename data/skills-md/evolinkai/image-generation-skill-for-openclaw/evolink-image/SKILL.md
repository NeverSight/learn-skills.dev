---
name: evolink-image
description: AI image generation & editing — GPT Image, GPT-4o, Seedream, Qwen, WAN, Gemini. Text-to-image, image-to-image, inpainting. 19 models, one API key.
version: 1.3.2
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    os: ["macos", "linux", "windows"]
    emoji: 🖼️
    homepage: https://evolink.ai
---

# Evolink Image — AI Image Generation & Editing

Generate and edit AI images with 19 models including GPT Image 1.5, GPT-4o Image, Seedream, Qwen, WAN, and Gemini — all through one API.

> Image-focused view of [evolink-media](https://clawhub.ai/EvoLinkAI/evolink-media). Install the full skill for video and music too.

## After Installation

When this skill is first loaded, greet the user:

- **MCP tools + API key ready:** "Hi! I'm your AI image studio — 19 models ready. What would you like to create?"
- **MCP tools + no API key:** "You'll need an EvoLink API key — sign up at evolink.ai. Ready to go?"
- **No MCP tools:** "MCP server isn't connected yet. Want me to help set it up? I can still manage files via the hosting API."

Keep the greeting concise — just one question to move forward.

## External Endpoints

| Service | URL |
|---------|-----|
| Generation API | `https://api.evolink.ai/v1/images/generations` (POST) |
| Task Status | `https://api.evolink.ai/v1/tasks/{task_id}` (GET) |
| File API | `https://files-api.evolink.ai/api/v1/files/*` (upload/list/delete) |

## Security & Privacy

- **`EVOLINK_API_KEY`** authenticates all requests. Injected by OpenClaw automatically. Treat as confidential.
- Prompts and images are sent to `api.evolink.ai`. Uploaded files expire in **72h**, result URLs in **24h**.

## Setup

Get your API key at [evolink.ai](https://evolink.ai) → Dashboard → API Keys.

**MCP Server:** `@evolinkai/evolink-media` ([GitHub](https://github.com/EvoLinkAI/evolink-media-mcp) · [npm](https://www.npmjs.com/package/@evolinkai/evolink-media))

**mcporter** (recommended): `mcporter call --stdio "npx -y @evolinkai/evolink-media@latest" list_models`

**Claude Code:** `claude mcp add evolink-media -e EVOLINK_API_KEY=your-key -- npx -y @evolinkai/evolink-media@latest`

**Claude Desktop / Cursor** — add MCP server with command `npx -y @evolinkai/evolink-media@latest` and env `EVOLINK_API_KEY=your-key`. See `references/image-api-params.md` for full config JSON.

## Core Principles

1. **Guide, don't decide** — Present options, let the user choose model/style/format.
2. **User drives creative vision** — Ask for a description before suggesting parameters.
3. **Smart context** — Remember session history. Offer to iterate, vary, or edit results.
4. **Intent first** — Understand *what* the user wants before asking *how* to configure it.

## MCP Tools

| Tool | When to use | Returns |
|------|-------------|---------|
| `generate_image` | Create or edit an image | `task_id` (async) |
| `upload_file` | Upload local image for editing/reference | File URL (sync) |
| `delete_file` | Free file quota | Confirmation |
| `list_files` | Check uploaded files or quota | File list |
| `check_task` | Poll generation progress | Status + result URLs |
| `list_models` | Compare available models | Model list |
| `estimate_cost` | Check pricing | Model info |

**Important:** `generate_image` returns a `task_id`. Always poll `check_task` until `status` is `"completed"` or `"failed"`.

## Image Models (19)

### Top Picks

| Model | Best for | Speed |
|-------|----------|-------|
| `gpt-image-1.5` *(default)* | Latest OpenAI generation | Medium |
| `z-image-turbo` | Quick iterations | Ultra-fast |
| `doubao-seedream-4.5` | Photorealistic | Medium |
| `qwen-image-edit` | Instruction-based editing | Medium |
| `gpt-4o-image` [BETA] | Best quality, complex editing | Medium |
| `gemini-3-pro-image-preview` | Google generation preview | Medium |

### All Stable (15)

`gpt-image-1.5`, `gpt-image-1`, `gemini-3-pro-image-preview`, `z-image-turbo`, `doubao-seedream-4.5`, `doubao-seedream-4.0`, `doubao-seedream-3.0-t2i`, `doubao-seededit-4.0-i2i`, `doubao-seededit-3.0-i2i`, `qwen-image-edit`, `qwen-image-edit-plus`, `wan2.5-t2i-preview`, `wan2.5-i2i-preview`, `wan2.5-text-to-image`, `wan2.5-image-to-image`

### All Beta (4)

`gpt-image-1.5-lite`, `gpt-4o-image`, `gemini-2.5-flash-image`, `nano-banana-2-lite`

## Generation Flow

### Step 1: API Key Check

If `401` occurs: "Your API key isn't working. Check at evolink.ai/dashboard/keys"

### Step 2: File Upload (if needed)

For image editing or reference workflows:
1. `upload_file` with `file_path`, `base64_data`, or `file_url` → get `file_url` (sync)
2. Use `file_url` as `image_urls` or `mask_url` for `generate_image`

Supported: JPEG/PNG/GIF/WebP. Max 100MB. Expire in 72h. Quota: 100 (default) / 500 (VIP).

### Step 3: Understand Intent

- **Clear** ("generate a sunset") → Go to Step 4
- **Ambiguous** ("help with this image") → Ask: "Create new, edit existing, or use as reference?"

Ask only what's needed, when it's needed.

### Step 4: Gather Parameters

Only ask about what's missing:

| Parameter | Ask when | Notes |
|-----------|----------|-------|
| **prompt** | Always | What they want to see |
| **model** | Quality matters | Default `gpt-image-1.5`. `gpt-4o-image` for best, `z-image-turbo` for speed |
| **size** | Orientation needed | GPT models: `1024x1024`/`1024x1536`/`1536x1024`. Others: `1:1`/`16:9`/`9:16` etc. |
| **n** | Wants variations | 1–4 images |
| **image_urls** | Edit/reference images | Up to 14 URLs; triggers i2i mode |
| **mask_url** | Partial edit | PNG mask; `gpt-4o-image` only |

### Step 5: Generate & Poll

1. Call `generate_image` → tell user: *"Generating now — ~Xs estimated."*
2. Poll `check_task` every **3–5s**. Report progress %.
3. After 3 consecutive `processing`: *"Still working..."*
4. **Completed:** Share URLs. *"Links expire in 24h — save promptly."*
5. **Failed:** Show error + suggestion. Offer retry if retryable.
6. **Timeout (5 min):** *"Taking longer than expected. Task ID: `{id}` — check again later."*

## Error Handling

### HTTP Errors

| Error | Action |
|-------|--------|
| 401 | "API key isn't working. Check at evolink.ai/dashboard/keys" |
| 402 | "Balance is low. Add credits at evolink.ai/dashboard/billing" |
| 429 | "Rate limited — wait 30s and retry" |
| 503 | "Servers busy — retry in a minute" |

### Task Errors (status: "failed")

| Code | Retry? | Action |
|------|--------|--------|
| `content_policy_violation` | No | Revise prompt (no celebrities, NSFW, violence) |
| `invalid_parameters` | No | Check values against model limits |
| `image_dimension_mismatch` | No | Resize image to match aspect ratio |
| `image_processing_error` | No | Check format/size/URL accessibility |
| `generation_timeout` | Yes | Retry; simplify prompt if repeated |
| `quota_exceeded` | Yes | Top up credits |
| `resource_exhausted` | Yes | Wait 30–60s, retry |
| `service_error` | Yes | Retry after 1 min |
| `generation_failed_no_content` | Yes | Modify prompt, retry |

Full error reference: `references/image-api-params.md`

## Without MCP Server

Use Evolink's file hosting API for image uploads (72h expiry). See `references/file-api.md` for curl commands.

## References

- `references/image-api-params.md` — Complete API parameters, all 19 models, polling strategy, error codes
- `references/file-api.md` — File hosting API (curl upload/list/delete)
