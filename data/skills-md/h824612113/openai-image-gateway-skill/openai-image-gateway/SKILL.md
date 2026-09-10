---
name: openai-image-gateway
description: Use an OpenAI-compatible image gateway for text-to-image or reference-image generation with one-time local config. Trigger when the user asks to generate an image through a configured gateway, use a reference image, test gateway connectivity, update gateway settings, or save generated output to a specified local path.
---

# OpenAI Image Gateway

Use this skill when the user wants a reusable local image-generation workflow backed by an **OpenAI-compatible** gateway.

## What this skill does

- Stores `base_url`, `api_key`, and default `model` once in a local config file
- Keeps Images and Responses model preferences separate
- Resolves a usable model from the provider model list or conservative image-model candidates
- Diagnoses endpoint reachability without changing explicit endpoint choices
- Records `last_successful_mode` only after a real image is returned
- Generates an image from text and saves it to a user-specified local path
- Generates a new image from a reference image and prompt

## Common Chinese invocations

- `用 openai-image-gateway 生成图片，输出到 /path/to/file.png`
- `用 /path/to/reference.png 做参考图，生成白底商品渲染图，保存到 /path/to/product.png`
- `编辑这张图 /path/to/reference.png，改成赛博朋克风格，保存到 /path/to/output.png`

- `用 openai-image-gateway 生图，输出到 /path/to/file.png`
- `用图片网关生图，保存到 /path/to/file.png`
- `生成图片并输出到 /path/to/file.png`
- `用 openai-image-gateway 测一下连接`
- `用 openai-image-gateway 重新配置 url 和 key`

## Files

- Config: `local_config.json`
- Example config: `local_config.example.json`
- Script: `scripts/openai_image_gateway.py`

## Rules

- Do not print the full API key in chat.
- Keep real keys only in `local_config.json`.
- Save outputs only to paths the user asked for or clearly approved.

## Commands

First-time config:

```bash
python3 /Users/hanhao/.codex/skills/openai-image-gateway/scripts/openai_image_gateway.py config \
  --base https://example.com/ \
  --model gpt-image-2 \
  --responses-model gpt-5.4 \
  --endpoint-mode images
```

Omit `--key` to enter it through a hidden terminal prompt. Use `endpoint_mode: images|responses` for an operator override. Use `auto` only when automatic diagnostic selection is wanted.

Connectivity test:

```bash
python3 /Users/hanhao/.codex/skills/openai-image-gateway/scripts/openai_image_gateway.py test
```

`test` performs a read-only `GET /models` gateway and authentication check; it does not verify an image-generation route and never changes `endpoint_mode`.

To deliberately probe the Images and Responses generation routes without creating an image, use:

```bash
python3 /Users/hanhao/.codex/skills/openai-image-gateway/scripts/openai_image_gateway.py test \
  --probe-generation-route
```

This sends a zero-prompt diagnostic POST marked with `X-Image-Gateway-Probe: 1`. Gateways that support this marker can keep it out of image-generation failure alerts. A 400/422 response proves only route reachability.

To convert `auto` into the first reachable diagnostic candidate, opt in explicitly:

```bash
python3 /Users/hanhao/.codex/skills/openai-image-gateway/scripts/openai_image_gateway.py test --select
```

`--select` never overrides an explicit `images` or `responses` setting. A diagnostic selection is not proof that image generation works.

Generate to a target path:

```bash
python3 /Users/hanhao/.codex/skills/openai-image-gateway/scripts/openai_image_gateway.py generate \
  --prompt "一只西瓜在跳舞" \
  --out /Users/hanhao/Downloads/output_images/watermelon.png
```

Optional generation overrides:

- `--image /path/to/reference.png`
- `--size 1024x1024`
- `--quality low|medium|high|auto`
- `--format png|jpeg|webp`
- `--compression 0-100`
- `--model MODEL_NAME`
- `--idempotency-key KEY` (reuse a key after an ambiguous async Images submission)
- `--timeout SECONDS`
- `--background` (use the async Images/Responses route and poll until completion)
- `--stream` (responses endpoint only; stream progress and save only the final image)

When `endpoint_mode` is `images`, the CLI uses Image2's synchronous route by
default, matching gateways that expose Images at the configured base URL:

- Text-to-image: `POST <base_url>/images/generations`.
- Image-to-image: `POST <base_url>/images/edits`.
- The default JSON/form fields include `model`, `prompt`, `n=1`,
  `quality=low`, and `output_format=png`.

Pass `--background` to opt into the async route:

- Text-to-image: `POST <base_url>/images/generations?async=true`.
- Image-to-image: `POST <base_url>/images/edits?async=true`.
- A `202` response returns a task ID. Poll `<base_url>/images/tasks/{id}` no faster
  than every five seconds, using the same API key, until `completed` or
  `failed`.
- A completed task returns `result.data[0].url`; the signed result URL is
  downloaded without an `Authorization` header. Compatible Base64 responses
  are also accepted. If the completed URL briefly returns `429`/`5xx` or a
  transport error, the client retries that same URL at most twice; it never
  submits another generation request. A final download error identifies only
  the result host and tells the caller not to resubmit the completed task.

- Image requests forward `model`, `prompt`, `size`, and selected Image2 options
  (`quality`, `output_format`, `output_compression`, `image_size`).
- The CLI sends `quality=low` and `output_format=png` by default, and sends
  `output_compression` or ratio `image_size` only when explicitly selected.
- Image edits accept a local reference file (`image` multipart field) or a
  public HTTP(S) URL (`images`). If the gateway returns the explicit
  `images[].image_url is required` validation error, the URL is retried in the
  object form `{"image_url": "..."}`.
- Synchronous Images requests try the next configured image model after HTTP
  or transport failures. Async requests keep the same task/idempotency key and
  never switch models after a submission becomes ambiguous.

Images requests do not force `response_format`; the parser accepts either URL
or Base64 output. `--background` explicitly enables async mode and is accepted
for both endpoints.

## Workflow

1. If `local_config.json` is missing or incomplete, run `config` and choose `images`, `responses`, or `auto` deliberately.
2. Run `test` for read-only gateway and authentication diagnostics. Use `test --probe-generation-route` only when you need image-route reachability; treat HTTP 400/422 from that explicit diagnostic as route reachability only, not image-generation capability.
3. Run `generate` when the user gives a prompt and target path. Explicit endpoint modes are always honored.
4. In `auto`, prefer a fingerprint-matched `last_successful_mode`; otherwise probe once and use one reachable candidate without caching it as successful.
5. After real image bytes are extracted, cache `last_successful_mode` and the accepted model.
6. Add `--image /path/to/reference.png` when the user wants to use a reference image.
7. If a provider explicitly rejects a model (`model_not_found`, `unsupported_model`, or an equivalent 400/404 response), try the next candidate. For async Images submissions, retry one transient `429/502/503/504` or transport failure with the exact same body and `Idempotency-Key`; if it remains ambiguous, stop and report the key and request fingerprint. Do not switch endpoints or models after an ambiguous response.
8. If no candidate is accepted, report the endpoint and attempted models.

## Notes

- The script normalizes `base_url` so both `https://host` and `https://host/v1` work.
- The script supports both `b64_json` responses and URL-based image responses.
- `test` uses a read-only model-list request and cannot initiate image generation. `test --probe-generation-route` probes the configured Images route and identifies it with `X-Image-Gateway-Probe: 1`.
- `test` does not write configuration unless `--select` is present, and explicit endpoint modes are immutable to testing.
- HTTP 400/422 from a safe probe means the route exists; it never means the route can generate images.
- `endpoint_mode` stores operator intent. `last_successful_mode` is runtime-owned evidence written only after a real generation succeeds.
- A generation call uses one endpoint only. Async Images submission recovery is limited to one same-key replay; it never falls back to another model or endpoint after an ambiguous failure.
- Model discovery is read-only when `/models` is available. Model fallback only continues after a definitive model rejection; it never retries uncertain generation states.
- Passing `generate --model MODEL_NAME` bypasses optional `/models` discovery and sends that model directly to the configured generation endpoint.
- The first accepted model is cached with a configuration fingerprint and reused until the base URL, API key, or endpoint mode changes.
- `responses_model` is tried before the Images `model` when the Responses endpoint is selected.
- Success caches are bound to a SHA-256 fingerprint of the configured base URL and API key.
- For the Images endpoint, the script uses synchronous requests by default,
  sends the gateway-compatible `n=1`, `quality=low`, and PNG fields, and uses
  multipart upload for local `/images/edits` references.
- Polling `429` or `5xx` responses retries the existing task only. Before a
  task ID is returned, one initial `429/502/503/504` or transport failure is
  replayed with the same idempotency key; a second ambiguous result stops and
  leaves `pending_image_request.json` with only the key and fingerprint.
- Result-image download failures happen after task completion. They get a
  bounded retry on the same signed URL and never trigger a new POST, preventing
  duplicate generation or billing when a provider CDN is unavailable.
- `--stream` remains Responses-only; `--background` is the opt-in for async
  Images/Responses execution.
- Partial preview images from `--stream` are never written to disk. If a stream ends before the final image, the script fails instead of saving an unfinished picture.
