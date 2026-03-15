---
name: pollo-ai-video-generator
description: Generate AI videos using the Pollo AI API. Supports 13 leading models (Kling, Sora, Runway, Veo, Pixverse, Hailuo, Vidu, Luma, Pika, Wan, Seedance, Hunyuan, Pollo) with 50+ versions. It also supports task polling, credit cost estimation, and credit balance checks. Use this skill whenever the user wants to generate an AI video from text or image, use any AI video model, check Pollo credits, or mentions Pollo AI, pollo.ai, or any of the supported model names. Even if the user just says "generate a video" or "make me a short clip" without mentioning Pollo, this skill should be used.
---

# Pollo AI API Skill

Generate AI videos by calling the Pollo AI REST API directly.

## Friendly Onboarding (Conditional)

When the user's request is **vague or open-ended** (e.g., "make me a video", "I want to try AI video", "generate something cool", no specific model/prompt/parameters), show a brief, friendly guide **before** asking for details. Do NOT show this guide if the user already has a clear request (e.g., specifies a model, gives a prompt, or provides an image).

Use this template (adapt naturally to match the user's language, keep it concise and professional):

```
I can help you generate AI videos with Pollo AI.

- **Text to Video**: Create a video from a written prompt
- **Image to Video**: Animate an image into a video
- **Credit Check**: Check your available API credits

I support 13 model brands, including Kling, Sora, Runway, Veo, and Pixverse. If you do not have a preferred model, I can recommend one.

What would you like to create? For example:
- "A cat playing piano in a jazz club, cinematic lighting"
- "Turn this image into a video" (attach an image)
- "Use Kling v2.6 to generate a 10s ocean wave video"
```

Rules for this section:
- **Skip entirely** if the user provides a specific prompt, model name, or image — go straight to execution.
- **Skip entirely** if the user only asks about credits or config — just answer directly.
- Keep the tone warm but brief. Never dump the full model table on the user unprompted.
- After showing the guide, wait for the user's input before proceeding.

## First-Time Setup

Store the API key locally in `~/.pollo/config.toml`. After setup, do not show it again in later replies.

**Important:** Do not ask the user to run scripts or commands. All script execution is done by the AI. If setup is needed, ask the user to create a key on the website and paste it into the chat.

**Security rule:** Never include the API key in any bash command or script argument. Always use the Write tool to create config files containing credentials.

The API key can also be provided via the `POLLO_API_KEY` environment variable, which takes priority over the config file. If set, skip config file setup entirely.

### Check if already configured

```bash
python3 scripts/pollo_config.py
```

If this prints the config summary (from env var or config file), the key is already set up. Skip to Key Validation.

### New setup

If config is not found (exit code 2 or error), follow this flow:

1. **Tell the user** they need an API Key, in a friendly tone. Example:

   > I need your Pollo API key once before I can generate videos.
   >
   > 1. Open https://pollo.ai/api-platform/keys
   > 2. Click **Add Key**, save it, and paste the key here
   >
   > I will validate it and store it locally so you do not need to paste it again.

   Adapt the language to match the user's language. Keep it brief, friendly, and non-technical.

   If the user already gave a concrete video request, briefly acknowledge that request before asking for the key.

2. **Wait for the user to paste the key.** Do NOT proceed until the user provides it.

3. **Write the config file directly** using the Write tool (NOT a bash command):

   Write the following content to `~/.pollo/config.toml`:

   ```toml
   [api]
   key = "<the-key-user-pasted>"
   base_url = "https://pollo.ai/api/platform"
   ```

4. **Validate the key** by checking credit balance:

   ```bash
   python3 scripts/pollo_api.py GET /credit/balance
   ```

5. **Report the result** in user-friendly language:
   - Success → "Setup is complete. You have X credits available. Send me a prompt whenever you are ready."
   - Invalid key → "That key does not appear to be valid. Please copy a new key from https://pollo.ai/api-platform/keys and paste it here."
   - Network error → "I couldn't reach the API right now. Please try again in a moment."

**Never** show the user raw script paths, command-line syntax, or error stack traces.

### Key Validation (Required)

**Before any generation task**, validate the key by checking the credit balance:

```bash
python3 scripts/pollo_api.py GET /credit/balance
```

Handle the response:

| Response | Meaning | Action |
|----------|---------|--------|
| `{ "code": "SUCCESS", "data": { "availableCredits": N, "totalCredits": M } }` | Key is valid | Read credits from `data`. If `availableCredits` is 0, tell user: "Your available balance is 0 credits. Please top up at https://pollo.ai/api-platform/pricing before generating videos." |
| `{ "code": "NOT_FOUND" }` | Key is invalid or does not exist | Tell user: "That API key does not appear to be valid. Please create a new one at https://pollo.ai/api-platform/keys and paste it here." |
| `{ "code": "UNAUTHORIZED" }` | Key format wrong or missing | Tell user: "The API key format doesn't look right. Keys usually start with `pollo_`. Please copy it again and paste it here." |
| Exit code 2 | Config not found | Trigger the **New setup** flow above. Do NOT tell the user to run any commands. |
| Network error / timeout | API unreachable | Tell user: "I couldn't reach the API right now. Please try again in a moment." |

**Do NOT proceed to any generation task until the key is validated successfully.** This prevents wasted time on tasks that will fail due to invalid keys or zero balance.

## Core Workflow

The standard flow for any generation task:

1. **Validate key** — If not yet validated this session, check `GET /credit/balance` first (see Key Validation above)
2. **Create task** — POST to the model endpoint with parameters
3. **Handle creation errors** — Check the response for errors (see Error Handling below). If `"Not enough credits"`, stop and guide to recharge.
4. **Notify user** — Tell the user the task was submitted with a brief summary (model, prompt, duration, etc.)
5. **Poll status** — Run `poll_task.py` **synchronously** (NOT in background) until completion
6. **Return result** — Parse the JSON output and give the user the video URL

### Request Body Structure

All generation endpoints wrap parameters inside an `"input"` object:

```json
{
  "input": {
    "prompt": "...",
    "aspectRatio": "16:9",
    "length": 5
  }
}
```

### Creating a Generation Task

Use `pollo_api.py` to POST to the model endpoint. Example for Pollo v2.0 text-to-video:

```bash
python3 scripts/pollo_api.py POST /generation/pollo/pollo-v2-0 \
  --data '{"input":{"prompt":"A cat playing piano in a jazz club","aspectRatio":"16:9","length":5,"resolution":"720p"}}'
```

Response: `{ "code": "SUCCESS", "data": { "taskId": "xxx", "status": "waiting" } }`

Extract `taskId` from `data`.

### Polling for Results

After getting the taskId:

1. **Tell the user** what's happening with a brief summary (model, prompt, params), so they know the task is in progress.
2. **Run the bundled polling script synchronously** — do NOT use `run_in_background`:

```bash
python3 scripts/poll_task.py <taskId> --interval 5 --timeout 300
```

The script reads the API key from `~/.pollo/config.toml` automatically. Run it from the skill directory, or otherwise resolve `scripts/poll_task.py` relative to this skill's root. Set `timeout: 300000` on the Bash tool call to allow up to 5 minutes. The script runs silently and outputs a single JSON result to stdout when done.

3. **Parse the result** and present it to the user immediately.

## Preflight Checklist

Before calling any generation or tool endpoint, quickly lock down the minimum required inputs:

1. **Task type** — confirm whether this is text-to-video, image-to-video, or credit check
2. **Model choice** — use the user's requested model, or pick a default based on the guidance below
3. **Source assets** — for image-to-video, confirm whether the input is already a public URL or needs upload first
4. **Core params** — fill in `prompt`, `length`, `aspectRatio`, `resolution`, and audio-related flags only if the chosen model supports them
5. **Compatibility check** — if the user asks for a combination the model does not support, correct it before sending the request instead of letting the API reject it

Keep this step brief. The goal is to avoid preventable validation failures, not to interrogate the user when sensible defaults already exist.

### Handling Local Images (Image-to-Video)

When the user has a local image file instead of a URL, upload it first:

1. **Get a signed upload URL**:
   ```bash
   python3 scripts/pollo_api.py POST /file/sign \
     --data '{"action":"putObject","filename":"photo.jpg","type":"image/jpeg"}'
   ```
   Response includes a `signedUrl` (for uploading) and a `fileUrl` (the final HTTPS URL).

2. **Upload the file**:
   ```bash
   python3 scripts/pollo_api.py PUT "<signedUrl>" \
     --upload /path/to/photo.jpg --content-type image/jpeg
   ```

3. **Use the `fileUrl`** — Pass it as the `image` parameter in the generation request.

## Supported Models

Below is the quick reference. When the user picks a brand/model, read the corresponding reference file for full parameter details.

### Video Generation Brands

| Brand | Models | Reference File |
|-------|--------|---------------|
| Pollo | pollo-v1-5, pollo-v1-6, pollo-v2-0 (3 models) | `references/brands/pollo.md` |
| Kling AI | kling-v1, v1-5, v1-6, v2, v2-1, v2-1-master, v2-5-turbo, v2-6, video-o1 (9 models) | `references/brands/kling-ai.md` |
| Google Veo | veo2, veo3, veo3-fast, veo3-1, veo3-1-fast (5 models) | `references/brands/google.md` |
| Sora | sora-2, sora-2-pro (2 models) | `references/brands/sora.md` |
| Runway | runway-gen-3-turbo, runway-gen-4-turbo (2 models) | `references/brands/runway.md` |
| Pixverse | pixverse-v3-5, v4, v4-5, v5, v5-5 (5 models) | `references/brands/pixverse.md` |
| Hailuo | video-01, video-01-live2d, minimax-hailuo-02, minimax-hailuo-2.3, minimax-hailuo-2.3-fast (5 models) | `references/brands/minimax.md` |
| Pika | pika-v2-1, pika-v2-2 (2 models) | `references/brands/pika.md` |
| Vidu | vidu-q1, vidu-v1-5, vidu-v2-0, viduq2-pro, viduq2-turbo, viduq3-pro (6 models) | `references/brands/vidu.md` |
| Luma | luma-ray-1-6, luma-ray-2-0, luma-ray-2-0-flash (3 models) | `references/brands/luma.md` |
| Wan | wanx-v2-1, wan-v2-2-flash, wan-v2-2-plus, wan-v2-5-preview, wan-v2-6 (5 models) | `references/brands/wanx.md` |
| Seedance | seedance, seedance-pro, seedance-pro-fast, seedance-1-5-pro (4 models) | `references/brands/bytedance.md` |
| Hunyuan | hunyuan (1 model) | `references/brands/hunyuan.md` |

### Other Endpoints

| Function | Details |
|----------|---------|
| Task Status | `GET /generation/{taskId}/status` |
| Credit Cost | `POST /credit` |
| Credit Balance | `GET /credit/balance` |
| File Upload | `POST /file/sign` |

For details, read `references/common.md`.

## How to Pick a Model

**Default**: When the user has no preference, use **Pollo v2.0** — good quality, supports audio (generateAudio), up to 10s, up to 1080p, and cost-effective.

When the user has specific needs:

- **Best quality**: Google Veo 3.1, Kling v2.6, Sora 2 Pro
- **Fast & affordable**: Pollo v2.0, Pixverse v5.5, Wan v2.2 Flash
- **Audio generation**: Pollo v2.0 (generateAudio), Google Veo 3+, Kling v2.6, Pixverse v5+, Seedance 1.5 Pro, Vidu Q3 Pro, Wan v2.6
- **Long videos (10s+)**: Seedance 1.5 Pro / Pro Fast (up to 12s), most models support 10s
- **High resolution (1080p)**: Pollo v2.0, Kling v2.6, Seedance, most models support up to 1080p
- **Image to video**: All models support this — need an image URL (not base64)

## Error Handling

**Every API call response must be checked for errors before proceeding.** The API returns errors in this format:

```json
{ "message": "Human-readable error", "code": "ERROR_CODE" }
```

### Error Code Reference

| Error Code | Message Pattern | Meaning | What to Do |
|------------|----------------|---------|------------|
| `FORBIDDEN` | `"Not enough credits. Please add more."` | Account has insufficient credits | **Stop immediately.** Tell user: "Your account does not have enough credits. Please top up at https://pollo.ai/api-platform/pricing and try again." |
| `FORBIDDEN` | `"PERMISSION_ERROR"` | Key lacks permission for this endpoint | Check if the key is valid. If file upload fails with this, the key may not have upload permissions — suggest the user use image URLs directly instead. |
| `NOT_FOUND` | `"NOT_FOUND_ERROR"` | Invalid API key or wrong endpoint | Tell user: "That API key does not appear to be valid. Please create a new one at https://pollo.ai/api-platform/keys and paste it here." |
| `UNAUTHORIZED` | — | Missing or malformed API key | Tell user: "The API key format doesn't look right. Keys usually start with `pollo_`. Please copy it again and paste it here." |
| `BAD_REQUEST` | `"Input validation failed"` | Invalid request parameters | Check the `issues` array in the response for specific field errors. Fix and retry. |

### Critical: Insufficient Credits

This is the most common failure. When you see **any** of these signals:
- Response contains `"Not enough credits"`
- Response code is `FORBIDDEN` after a generation request
- Balance check shows `availableCredits: 0`

**Always respond with (adapt to the user's language):**
> Your Pollo AI account does not have enough credits for this request. Please visit https://pollo.ai/api-platform/pricing to top up, then try again.

**Never** retry the same request, try a different model, or attempt workarounds when credits are insufficient.

## Key Rules

- **Use `pollo_api.py` for all API calls** — never construct raw `curl` commands with API keys. The wrapper reads the key from `~/.pollo/config.toml` automatically and adds all required headers (`X-API-KEY`, `Content-Type`, `User-Agent`).
- **Store key locally after setup** — once configured, keep the API key in `~/.pollo/config.toml` and do not show it again in later replies.
- **Response wrapper** — all successful API responses are wrapped in `{ "code": "SUCCESS", "message": "success", "data": { ... } }`. Always extract the actual payload from the `data` field.
- **Body wrapper** — generation endpoints use `{ "input": { ... } }`
- **Image inputs as URLs** — when using image-to-video, the image must be an HTTPS URL, never base64. For local files, use the file upload flow above.
- **Prompt length** — varies by model (typically 1000-2500 chars), check the brand reference
- **Video storage** — generated videos are kept for 14 days only
- **Webhook alternative** — instead of polling, pass `webhookUrl` in the request body
- **Each model has its own endpoint** — the path pattern is `/generation/{brand}/{model}`
- **Validate key first** — always run the Key Validation step before any generation. Never skip it.

## Reference Files

Read these as needed (don't load all at once):

Resolve all bundled resources relative to this skill's root. Do not assume any machine-specific absolute path or a particular repo layout.

| File | When to Read |
|------|-------------|
| `references/brands/<brand>.md` | When generating with a specific brand's model |
| `references/common.md` | For auth, status polling, credits, webhooks, errors |
| `references/models-index.md` | For the full model→endpoint mapping table |
