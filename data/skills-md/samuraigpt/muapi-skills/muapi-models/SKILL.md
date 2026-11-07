---
name: muapi-models
description: Discover, price and run AI models on Muapi (api.muapi.ai) — image, video, audio, lipsync, 3D, LLM text, SEO/data tools. Use when the user mentions Muapi or muapi.ai, asks "which Muapi model for X", "list Muapi models", "generate an image/video/song/voiceover with Muapi", wants a model's schema or price, or wants generated media saved into their project. Covers search, schema inspection, cost estimate, file upload, async submit, polling and downloading results.
---

# Muapi models

Muapi is one API (`x-api-key`) in front of 500+ models: image, video, audio and speech,
lipsync, 3D, LLM text, SEO/data tools, social publishing and utilities. Provider names are
hidden; you only see Muapi model names, categories, schemas and costs. Model names are read
live, so new models work immediately. Never rely on a remembered model list.

Workflow: **discover -> inspect -> estimate -> run -> poll -> download**.

## Setup

1. Create a key at https://muapi.ai/dashboard (or a free sandbox key, see below).
2. Export it and restart your agent from that same shell:
   - macOS/Linux: `export MUAPI_API_KEY=your_key`
   - Windows PowerShell: `$env:MUAPI_API_KEY = "your_key"` and `setx MUAPI_API_KEY "your_key"`
3. Keep the key in the environment only. Never write it into project files, commits or chat.

Sandbox key (returns mock outputs instantly, no credits spent), useful for testing a flow:

```bash
curl -s -X POST https://api.muapi.ai/api/v1/keys -H "Content-Type: application/json" -d '{"is_test": true}'
```

Auth is always the `x-api-key: $MUAPI_API_KEY` header. If the `muapi` CLI is installed
(`pip install muapi-cli` or `npm i -g muapi-cli`) prefer it, since it handles upload, polling and
`--output-json`. Otherwise use the HTTP calls below (`curl`; on Windows PowerShell use `curl.exe`).

## Rules

- User instructions first, then any tool they already configured, then Muapi.
- Always inspect before you run. Never guess fields or endpoint paths; schemas change.
- Estimate cost before spending credits on anything non-trivial; check balance if no budget was given.
- Submit, then poll every 3-10 seconds. Don't hold one long request open.
- On `failed`, show the `error` field verbatim. Don't silently retry.
- Name the model explicitly if the user did; otherwise state which model you picked and why.

## 1. Discover

```bash
curl -s "https://api.muapi.ai/api/v1/models?category=Text%20to%20Image"
curl -s "https://api.muapi.ai/api/v1/models?family=seo"
```

There is no free-text search param: fetch a category and filter client-side by name/description,
and try a few keyword variants. Categories: `Text to Image`, `Image to Image`, `Text to Video`,
`Image to Video`, `Video to Video`, `Audio to Video` (lipsync), `Text to Audio`, `Image to 3D`,
`Text to 3D`, `Text to Text` (LLMs and data tools), `Lora Support`, `Training`.
CLI: `muapi discover "cinematic image to video" --output-json`

## 2. Inspect

```bash
curl -s "https://api.muapi.ai/api/v1/models/{name}"
```

Returns the input schema (required fields, allowed values, defaults), pricing and the real
`endpoint` to POST to. CLI: `muapi inspect {name} --output-json`

## 3. Estimate cost

```bash
curl -s -X POST "https://api.muapi.ai/api/v1/models/{name}/estimate-cost" \
  -H "Content-Type: application/json" -d @payload.json
```

Same body you would send to run it. Balance: `GET /api/v1/account/balance`
(CLI: `muapi account balance`).

## 4. Upload input files

Models that take an image, video or audio need a hosted URL. Upload local files first:

```bash
curl -s -X POST https://api.muapi.ai/api/v1/upload_file \
  -H "x-api-key: $MUAPI_API_KEY" -F "file=@./input.png"
```

Limits: images 10MB, videos 50MB. CLI: `muapi upload file ./input.png --output-json`

## 5. Run

POST to the `endpoint` from step 2 (never a path you assumed):

```bash
curl -s -X POST "https://api.muapi.ai{endpoint}" \
  -H "x-api-key: $MUAPI_API_KEY" -H "Content-Type: application/json" -d @payload.json
# -> {"request_id": "...", "status": "processing"}
```

CLI: `muapi run {name} --input payload.json --no-wait --output-json`

## 6. Poll

```bash
curl -s "https://api.muapi.ai/api/v1/predictions/{request_id}/result" -H "x-api-key: $MUAPI_API_KEY"
```

`status` is `processing`, `completed` or `failed`. On `completed`, `outputs` is an array of URLs.
CLI: `muapi runs get {request_id} --wait --output-json`

## 7. Save results

Result URLs are kept for 30 days, then expire. As soon as a task completes, download every output to the
location the user asked for (for example `./public/hero.png`) and tell them the path:

```bash
curl -L -o ./public/hero.png "{output_url}"
```

If the user wants it in their app, write the integration code instead of just a file.

## Writing good requests

Ask for or infer: the output destination, a specific model if they have a preference, and key
parameters (aspect ratio, resolution, duration). Examples:
- "Make a 1:1 product photo of a white ceramic mug with Muapi, save to ./public/mug.png"
- "Generate a 30 second lo-fi background track with Muapi"
- "Turn README.md into a spoken intro with a Muapi speech model"

## Troubleshooting

| Problem | Fix |
|---|---|
| `MUAPI_API_KEY` missing | Export it and restart the agent from the same terminal |
| 401 | Check the key at https://muapi.ai/dashboard; header must be `x-api-key` |
| Insufficient credits | Top up in the dashboard, then rerun |
| `failed` task | Show `error`, adjust parameters from the schema, retry once |
| Expired result link (older than 30 days) | Re-run, and save outputs locally next time |
| `curl` rejects args on Windows | Use `curl.exe` |

## Other interfaces

OpenAPI: https://api.muapi.ai/openapi.json · MCP: https://muapi.ai/.well-known/mcp.json ·
Human docs: https://muapi.ai/agent-skills
