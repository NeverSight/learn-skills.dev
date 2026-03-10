---
name: ultimate-ai-media-generator-skill
description: Generate and monitor CyberBara Public API v1 image and video tasks end-to-end. Use when work involves CyberBara `/api/v1` endpoints for listing models, uploading reference images, quoting credits, creating generation tasks, polling task status, or checking credits balance and usage.
---

# Ultimate-AI-Media-Generator-Skill

## Overview

Use this skill to call CyberBara APIs reliably, create image/video generation tasks, and return final media URLs with credit-aware flow.

## Implementation Architecture

The runtime uses a layered Python architecture:

- `scripts/cyberbara_api.py`: thin entrypoint only
- `src/cyberbara_cli/cli.py`: command parsing and command routing
- `src/cyberbara_cli/usecases/`: flow orchestration (generation + polling)
- `src/cyberbara_cli/policies/`: safety and policy rules (credits quote + formal confirmation)
- `src/cyberbara_cli/gateways/`: raw CyberBara API client
- `src/cyberbara_cli/config.py`: API key discovery and local persistence
- `src/cyberbara_cli/constants.py`: fixed base URL and shared constants

When extending behavior, keep business rules in `usecases/` or `policies/`, not in `scripts/`.

## Set Up Runtime Inputs

The script uses fixed base URL:

```text
https://cyberbara.com
```

API key lookup order:

1. `--api-key`
2. environment variable `CYBERBARA_API_KEY`
3. local cache file `~/.config/cyberbara/api_key`
4. interactive prompt (if running in terminal)

Recommended one-time setup command:

```bash
python3 scripts/cyberbara_api.py setup-api-key "<api-key>"
```

Or save from environment variable:

```bash
export CYBERBARA_API_KEY="<api-key>"
python3 scripts/cyberbara_api.py setup-api-key --from-env
```

If API key is missing, the script immediately asks for it and shows where to get one:

```text
https://cyberbara.com/settings/apikeys
```

When you provide API key via `--api-key` or interactive prompt, it is saved to:

```text
~/.config/cyberbara/api_key
```

Future runs reuse this cached key, so users do not need to provide it every time.

## Run The Standard Generation Flow

1. Discover available models.
2. Upload reference images when task scene needs image inputs.
3. Quote credits before creating a generation task.
4. Create image or video generation task and wait for final output.
5. Automatically save generated media locally and open it.
6. Check usage records when needed.

Reference commands:

```bash
# 1) List video models
python3 scripts/cyberbara_api.py models --media-type video

# 2) Upload local reference images
python3 scripts/cyberbara_api.py upload-images ./frame.png ./style.jpg

# 3) Estimate credits
python3 scripts/cyberbara_api.py quote --json '{
  "model":"sora-2",
  "media_type":"video",
  "scene":"text-to-video",
  "options":{"duration":"10"}
}'

# 4) Create a video task (default behavior: wait for success, save outputs to ./media_outputs, auto-open)
python3 scripts/cyberbara_api.py generate-video --json '{
  "model":"sora-2",
  "prompt":"A calm drone shot over snowy mountains at sunrise",
  "scene":"text-to-video",
  "options":{"duration":"10","resolution":"standard"}
}'

# 5) Existing task: wait + save/open outputs
python3 scripts/cyberbara_api.py wait --task-id <TASK_ID> --interval 5 --timeout 900
```

Image and video generation are confirmation-gated by default:

```bash
# Single image request: script auto-quotes, then asks you to type CONFIRM
python3 scripts/cyberbara_api.py generate-image --json '{
  "model":"nano-banana-pro",
  "prompt":"A cinematic portrait under neon rain",
  "scene":"text-to-image",
  "options":{"resolution":"1k"}
}'

# Batch image requests (JSON array): script auto-quotes each request and prints total estimated credits
python3 scripts/cyberbara_api.py generate-image --file ./image-requests.json
```

`image-requests.json` format:

```json
[
  {
    "model": "nano-banana-pro",
    "prompt": "A cinematic portrait under neon rain",
    "scene": "text-to-image",
    "options": { "resolution": "1k" }
  },
  {
    "model": "nano-banana-pro",
    "prompt": "A product still life with dramatic side light",
    "scene": "text-to-image",
    "options": { "resolution": "1k" }
  }
]
```

Only use `--yes` after explicit user approval has been obtained:

```bash
python3 scripts/cyberbara_api.py generate-image --file ./image-requests.json --yes
python3 scripts/cyberbara_api.py generate-video --json '{
  "model":"sora-2",
  "prompt":"A calm drone shot over snowy mountains at sunrise",
  "scene":"text-to-video",
  "options":{"duration":"10","resolution":"standard"}
}' --yes
```

Control auto-save and open behavior:

```bash
# keep waiting but do not auto-open media
python3 scripts/cyberbara_api.py generate-image --file ./image-requests.json --yes --no-open

# custom output directory
python3 scripts/cyberbara_api.py generate-video --json '{...}' --yes --output-dir ./downloads

# submit only (no wait/save/open)
python3 scripts/cyberbara_api.py generate-video --json '{...}' --yes --async
```

## Use Script Capabilities

`scripts/cyberbara_api.py` supports:

- `setup-api-key` to persist API key into local cache
- `models` to list public models (`--media-type image|video` optional)
- `upload-images` to upload local image files to `/api/v1/uploads/images`
- `quote` to estimate credit cost from JSON request body
- `generate-image` to auto-quote credits, compute total for batch requests, require formal confirmation, create task(s), wait, then save/open outputs
- `generate-video` to auto-quote credits, compute total for batch requests, require formal confirmation, create task(s), wait, then save/open outputs
- `task` to fetch task snapshot by task ID
- `wait` to poll task until `success`, `failed`, or `canceled`, then save/open outputs
- `balance` and `usage` to inspect credits
- `raw` for direct custom endpoint calls

Use `--file request.json` instead of `--json` for long payloads.

## Enforce API Payload Rules

- Send auth via API key (`Authorization: Bearer <key>` or `x-api-key`).
- Send public request fields under `options.*` only.
- Prefer explicit `scene` to avoid inference ambiguity.
- Include `options.image_input` for `image-to-image` and `image-to-video`.
- Include `options.video_input` for `video-to-video`.
- Poll `/api/v1/tasks/{taskId}` until final status; only `success` guarantees output URLs.
- Before every image or video generation submission, obtain quote first and get explicit user confirmation.
- For multiple image/video requests, calculate and present total estimated credits before submission.
- Save output files under `media_outputs/` by default and auto-open them unless disabled.

## Navigate Detailed Model Options

Use the reference file for full model matrices and examples:

- `references/cyberbara-api-reference.mdx`

For fast lookup in large reference:

```bash
rg '^## |^### ' references/cyberbara-api-reference.mdx
rg 'kling-2.6|sora-2|veo-3.1|seedance' references/cyberbara-api-reference.mdx
```

## Handle Common Failures

- `invalid_api_key` or `api_key_required`: verify key and headers.
- `insufficient_credits`: quote first or recharge credits.
- `invalid_scene` or `scene_not_supported`: choose scene supported by model.
- `invalid_request`: verify `prompt` and `options` requirements by model.
- `task_not_found`: verify task ID and environment domain.
