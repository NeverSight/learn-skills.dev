---
name: runpod
description: Cloud GPU processing via RunPod serverless. Use when setting up RunPod endpoints, deploying Docker images, managing GPU resources, troubleshooting endpoint issues, or understanding costs. Covers all 5 toolkit images (qwen-edit, realesrgan, propainter, sadtalker, qwen3-tts).
---

# RunPod Cloud GPU

Run open-source AI models on cloud GPUs via RunPod serverless. Pay-per-second, no minimums.

## Setup

```bash
# 1. Create account at https://runpod.io
# 2. Add API key to .env
echo "RUNPOD_API_KEY=your_key_here" >> .env

# 3. Deploy any tool with --setup
python tools/image_edit.py --setup
python tools/upscale.py --setup
python tools/dewatermark.py --setup
python tools/sadtalker.py --setup
python tools/qwen3_tts.py --setup
```

Each `--setup` command:
1. Creates a RunPod **template** from the Docker image
2. Creates a serverless **endpoint** with appropriate GPU
3. Saves the endpoint ID to `.env` (e.g. `RUNPOD_QWEN_EDIT_ENDPOINT_ID`)

## Available Images

All images are public on GHCR — no authentication needed.

| Tool | Docker Image | GPU | VRAM | Typical Cost |
|------|-------------|-----|------|-------------|
| image_edit | `ghcr.io/conalmullan/video-toolkit-qwen-edit:latest` | A6000/L40S | 48GB+ | ~$0.05-0.15/job |
| upscale | `ghcr.io/conalmullan/video-toolkit-realesrgan:latest` | RTX 3090/4090 | 24GB | ~$0.01-0.05/job |
| dewatermark | `ghcr.io/conalmullan/video-toolkit-propainter:latest` | RTX 3090/4090 | 24GB | ~$0.05-0.30/job |
| sadtalker | `ghcr.io/conalmullan/video-toolkit-sadtalker:latest` | RTX 4090 | 24GB | ~$0.05-0.15/job |
| qwen3_tts | `ghcr.io/conalmullan/video-toolkit-qwen3-tts:latest` | ADA 24GB | 24GB | ~$0.01-0.05/job |

**Total monthly cost:** Rarely exceeds $10 even with heavy use.

## How It Works

All tools follow the same pattern:

```
Local CLI → Upload input to cloud storage → RunPod API → Poll for result → Download output
```

1. **File transfer:** Tools use Cloudflare R2 when configured (`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`), falling back to free upload services
2. **RunPod API:** Tools call the `/run` endpoint, then poll `/status/{job_id}` until complete
3. **Cold vs warm start:** First request after idle spins up a worker (~30-90s). Subsequent requests are fast (~5-15s)

## Endpoint Management

### Workers

```
workersMin: 0    — Scale to zero when idle (no cost)
workersMax: 1    — Max concurrent jobs (increase for throughput)
idleTimeout: 5   — Seconds before worker scales down
```

Across all endpoints, you share a total worker pool based on your RunPod plan. If you hit limits, reduce `workersMax` on endpoints you're not actively using.

### Checking Endpoint Status

Each tool stores its endpoint ID in `.env`:

| Tool | Env Var |
|------|---------|
| image_edit | `RUNPOD_QWEN_EDIT_ENDPOINT_ID` |
| upscale | `RUNPOD_UPSCALE_ENDPOINT_ID` |
| dewatermark | `RUNPOD_DEWATERMARK_ENDPOINT_ID` |
| sadtalker | `RUNPOD_SADTALKER_ENDPOINT_ID` |
| qwen3_tts | `RUNPOD_QWEN3_TTS_ENDPOINT_ID` |

### Disabling an Endpoint

To free worker slots without deleting the endpoint, set `workersMax=0` via the RunPod dashboard or GraphQL API.

## Troubleshooting

### Force Image Pull

When you push a new Docker image version, RunPod may still use the cached old one. To force a pull:

1. Update the template's `imageName` to use `@sha256:DIGEST` notation
2. Wait for the worker to restart
3. Revert to `:latest` tag after confirming

### Cold Start Too Slow

- **qwen3-tts:** ~70s cold start, ~7s warm
- **sadtalker:** ~60s cold start, ~10s warm
- **image_edit:** ~90s cold start, ~15s warm

If cold starts are a problem, set `workersMin: 1` (costs money when idle).

### Job Fails with OOM

The model needs more VRAM than the GPU provides. Options:
- Use a larger GPU tier
- For dewatermark: reduce `--resize-ratio` (default 0.5 for safety)
- For image_edit: reduce `--steps`

### "No workers available"

You've hit your plan's concurrent worker limit. Either:
- Wait for a running job to finish
- Set `workersMax=0` on endpoints you're not using
- Upgrade your RunPod plan

## Docker Images

All Dockerfiles live in `docker/runpod-*/`. Images use `runpod/pytorch` as the base to share layers across tools.

Building for RunPod (from Apple Silicon Mac):
```bash
docker buildx build --platform linux/amd64 -t ghcr.io/conalmullan/video-toolkit-<name>:latest docker/runpod-<name>/
docker push ghcr.io/conalmullan/video-toolkit-<name>:latest
```

GHCR packages default to **private** — you must manually make them public for RunPod to pull them. Go to GitHub > Packages > Package Settings > Change Visibility.

## Cost Optimization

- Keep `workersMin: 0` on all endpoints (scale to zero)
- Only deploy endpoints you actively need
- Use `workersMax=0` to disable idle endpoints without deleting them
- Qwen3-TTS is significantly cheaper than ElevenLabs for voiceovers
- Check the RunPod dashboard for usage and billing
