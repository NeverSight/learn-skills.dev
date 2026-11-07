---
name: openrouter-video-generate
description: Generate and download videos through OpenRouter's dedicated asynchronous Video API. Use this skill whenever the user wants to create, render, generate, poll, resume, or save an OpenRouter video, including text-to-video, first/last-frame image-to-video, reference-to-video, choosing or listing video models, setting duration/resolution/aspect ratio/audio/seed, checking job status, downloading completed outputs, configuring callbacks, or passing provider-specific video options. Prefer the bundled Python script so asynchronous jobs and API options are handled consistently.
---

# OpenRouter Video Generation

Use this skill to submit asynchronous OpenRouter video jobs, poll them to a terminal state, and save completed video files.

## Default workflow

1. Use the OpenRouter API key from the current environment first. If it is missing, rely on the bundled script's automatic lookup of the nearest project `.env` file containing `OPENROUTER_API_KEY`, unless the user explicitly provides another environment variable name or env file path.
2. Pick a model from the user's request. If no model is specified, use `bytedance/seedance-2.0` and mention that the user can override it. Use model discovery before assuming support for unusual resolutions, aspect ratios, audio, images, or provider options.
3. Use `scripts/openrouter_video_generate.py` rather than constructing requests and polling loops manually.
4. Save generated videos to a user-visible output directory, defaulting to the current working directory if the user did not specify one.
5. Do not print API keys or put them directly on the command line because shell history may capture them.

## Bundled script

Submit, wait, and download in one command:

```bash
python scripts/openrouter_video_generate.py generate \
  --prompt "a slow cinematic push-in on a neon cafe sign in the rain" \
  --model "bytedance/seedance-2.0" \
  --duration 5 \
  --resolution 1080p \
  --aspect-ratio 16:9 \
  --output-dir ./outputs
```

The script reads `OPENROUTER_API_KEY` from the current environment first. If it is not set, it searches from the current working directory upward for the nearest `.env`. Use `--api-key-env MY_OPENROUTER_KEY` for another variable name or `--env-file ./path/to/.env` to force a particular file.

Generation is asynchronous. The command prints the job ID immediately, polls every 30 seconds by default, and downloads all returned outputs after completion. Use `--submit-only` to return after submission, then resume later with `status` or `download`.

## Common generation options

Pass only options the user requests or that the selected model supports:

- `--prompt TEXT` is required.
- `--model MODEL_ID` defaults to `bytedance/seedance-2.0`.
- `--duration SECONDS` sets the clip duration.
- `--resolution 480p|720p|768p|1080p|1K|2K|4K` sets a normalized resolution.
- `--aspect-ratio 16:9|9:16|1:1|4:3|3:4|3:2|2:3|21:9|9:21` sets the output ratio.
- `--size WIDTHxHEIGHT` is interchangeable with resolution plus aspect ratio; do not combine them.
- `--first-frame PATH_OR_URL` and `--last-frame PATH_OR_URL` provide exact boundary frames for image-to-video.
- `--reference PATH_OR_URL` can be repeated for style or content guidance. Local images are converted to data URLs.
- `--generate-audio` or `--no-generate-audio` explicitly controls audio when the model supports it. Omit both to use the API/model default.
- `--seed INTEGER` requests deterministic generation where supported.
- `--callback-url HTTPS_URL` sets a per-request webhook. Pair it with `--submit-only` when another service will handle completion.
- `--provider-options-json '{"google-vertex":{"parameters":{"negativePrompt":"blurry"}}}'` passes provider-specific options under `provider.options`.
- `--provider-options-file options.json` is safer for larger provider options.
- `--raw-json payload.json` merges additional OpenRouter-compatible request fields into the payload.
- `--poll-interval 30` controls polling frequency and `--timeout 1800` limits total waiting time. A timeout does not cancel the remote job.
- `--dry-run` prints the request payload without making a network call.

`frame_images` take precedence over `input_references` in OpenRouter. Prefer one mode per request so the user's references are not silently ignored.

## Model discovery and job recovery

List video models and their supported resolutions, aspect ratios, sizes, passthrough fields, and pricing:

```bash
python scripts/openrouter_video_generate.py models
```

Inspect or resume a submitted job:

```bash
python scripts/openrouter_video_generate.py status --job-id JOB_ID --json
python scripts/openrouter_video_generate.py download --job-id JOB_ID --output-dir ./outputs
```

Use `download --index 0` to fetch one output from a multi-output job. `download` first checks that the job completed, then uses the returned content URLs and authenticates same-origin OpenRouter endpoints when required. Authentication is removed before any cross-origin redirect.

## Output and metadata

One output is saved as `<output-prefix>.<ext>`; multiple outputs are saved as `<output-prefix>_001.<ext>`, `<output-prefix>_002.<ext>`, and so on. The extension is inferred from the response content type and defaults to `.mp4`.

The script writes `<output-prefix>_metadata.json` by default. It records the request with base64 image bodies omitted, the latest job response, and downloaded file paths. Use `--metadata-file PATH` to choose another path or `--no-metadata` to skip it.

If local waiting is interrupted or times out, keep the printed job ID and use `status` or `download`; the OpenRouter job continues independently.

## Safety, cost, and retention

Video generation can bill the user's OpenRouter account, and higher duration or resolution usually costs more. Before submitting a real job, make sure the model, duration, resolution, audio choice, and output mode match the user's intent. Use `models` or `--dry-run` when uncertain.

OpenRouter video generation is not eligible for Zero Data Retention because asynchronous results must be retained temporarily for retrieval. If ZDR enforcement is enabled at the account level or through a request field, the request will not be routed. Tell the user when this conflicts with their privacy requirements.

For webhook receivers, verify `X-OpenRouter-Signature` against the exact raw request body using HMAC-SHA256, reject stale timestamps, and deduplicate deliveries with `X-OpenRouter-Idempotency-Key`.

## Troubleshooting

- A long `pending` or `in_progress` state can be normal; video generation may take several minutes. Continue polling at a reasonable interval.
- On `failed`, `cancelled`, or `expired`, report the returned `error` and preserve the job metadata rather than repeatedly resubmitting.
- For model or parameter errors, run `models --json` and verify the model ID and advertised capabilities.
- If image-guided generation fails, verify that URLs are reachable or local files exist and use supported image formats.
- A local polling timeout does not mean generation failed. Resume by job ID instead of creating a duplicate billable job.
