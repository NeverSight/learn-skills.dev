---
name: lightx2v-ai-video-generation
description: Use when generating images, videos, digital humans, audio-video clips, TTS speech, cloned voices, or reusable LightX2V workflows from an agent or command line.
allowed-tools: Bash(lightx2v *)
---

# LightX2V AI Video Generation

Use the `lightx2v` CLI to submit LightX2V tasks, poll results, create/run workflows, synthesize speech, and manage cloned voices.

## Start Here

1. Authenticate: use `LIGHTX2V_API_KEY`, `LIGHTX2V_CLOUD_API_KEY`, or `lightx2v login`.
2. Set backend if needed: `LIGHTX2V_BASE_URL=https://x2v.light-ai.top` or a local server such as `http://127.0.0.1:8081`.
3. Discover live models before guessing names: `lightx2v models --json`.
4. Prefer direct `lightx2v run` for one model task. Use `lightx2v workflow ...` for multi-node graphs, saved user workflows, or generated TTS -> digital-human pipelines.
5. Before creating or editing workflow JSON, read `references/workflow-nodes.md` for node ids, ports, data fields, and graph patterns.
6. Before discovering inputs, running, monitoring, or cancelling a saved workflow, read `references/workflow-api.md`.
7. Before using TTS or voice clone, read `references/voice-tts.md` for voice discovery, parameters, clone commands, and workflow `tts` nodes.
8. Never print API keys, bearer tokens, or long signed media URLs in shared output.

Install:

```bash
curl -fsSL https://raw.githubusercontent.com/ModelTC/lightx2v-studio-cli/main/install.sh | sh
```

## Command Map

| Goal | Command |
| --- | --- |
| List models | `lightx2v models --json` |
| Submit one generation task | `lightx2v run TASK/MODEL --prompt "..." ...` |
| Query/download task | `lightx2v query TASK_ID`, `lightx2v result TASK_ID -o out.mp4` |
| List owned workflows | `lightx2v workflow list --json` |
| Inspect/create workflow | `lightx2v workflow get WORKFLOW_ID --json`, `lightx2v workflow create --input @workflow.json --json` |
| Discover workflow inputs | `lightx2v workflow inputs WORKFLOW_ID --json` |
| Run workflow | `lightx2v workflow run WORKFLOW_ID --inputs @inputs.json --input-file node_id=./file.png --poll` |
| Monitor workflow | `lightx2v workflow runs WORKFLOW_ID --status running`, `lightx2v workflow stream WORKFLOW_ID RUN_ID` |
| Workflow outputs | `lightx2v workflow outputs WORKFLOW_ID RUN_ID --json` |
| Cancel workflow work | `lightx2v workflow cancel WORKFLOW_ID RUN_ID`, `lightx2v workflow cancel-node WORKFLOW_ID RUN_ID NODE_ID` |
| TTS | `lightx2v voices`, `lightx2v tts ...`; details in `references/voice-tts.md` |
| Voice clone | `lightx2v voice-clone create/list/tts/delete ...`; details in `references/voice-tts.md` |

## Direct Generation Tasks

Use exact `task/model_cls` values from `lightx2v models --json`.

```bash
lightx2v run t2i/Qwen-Image-2512 \
  --prompt "watercolor portrait of a curious astronaut, soft morning light" \
  --aspect-ratio 16:9 \
  -o portrait.png

lightx2v run i2v/Wan2.2_I2V_A14B_distilled \
  --prompt "The subject slowly turns toward camera and smiles" \
  --image ./start.png \
  -o motion.mp4

lightx2v run s2v/SekoTalk-V3 \
  --prompt "Natural talking-head delivery, relaxed expression" \
  --image ./portrait.png \
  --audio ./speech.wav \
  -o avatar.mp4

lightx2v run t2av/MiniMax-H3 \
  --prompt "A 15-second vertical product film with synchronized sound" \
  --aspect-ratio 9:16 \
  --resolution-level 768p \
  --duration 15 \
  -o product.mp4
```

Common task meanings:

| Task | Inputs | Notes |
| --- | --- | --- |
| `t2i` | prompt | Text to image |
| `i2i` | prompt + image(s) | Edit/restyle/reference image |
| `t2v` | prompt | Text to silent video |
| `i2v` | prompt + image | Image to silent video |
| `s2v` | image/video + audio | Digital-human/lip-sync |
| `t2av` | prompt | Text to audio-video |
| `i2av` | prompt + image(s) | Image/keyframes to audio-video |
| `ref2av` | prompt + reference image/video/audio | Multi-reference audio-video |
| `vsr` | video or image | Super-resolution |
| `animate` | reference image + driving video | Motion transfer |

Important run flags: `--prompt`, `--input JSON|@file.json`, `--image`, `--video`, `--audio`, `--shape H,W`, `--resolution-level`, `--aspect-ratio`, `--duration`, `--quote`, `--json`, `--no-download`, `-o`.

For MiniMax-H3, use `--resolution-level 544p|768p` to select the output tier. If the
user requests 768P, include `--resolution-level 768p` on every submitted task. Do not
substitute `--shape 1344,768` for the tier: an omitted `resolution_level` uses the
platform default (`544p`). Do not claim that MiniMax-H3 is limited to 544P or add a VSR
step unless the user explicitly requests upscaling.

When writing a batch script against `POST /api/v1/task/submit`, use the same canonical
fields as the CLI. A MiniMax-H3 768P request looks like this:

```json
{
  "task": "t2av",
  "model_cls": "MiniMax-H3",
  "prompt": "A 15-second vertical product film with synchronized sound",
  "aspect_ratio": "9:16",
  "resolution_level": "768p",
  "video_duration_seconds": 15
}
```

Reuse the exact same model, aspect ratio, resolution tier, duration, and media fields
for quote and submit. The server derives the compatible pixel canvas (for example,
9:16 768P becomes `[1344, 768]` in `custom_shape`). Do not infer a downgrade from that
internal size, and do not omit `resolution_level` after quoting it.

## Workflow Basics

For workflow creation/editing details, read `references/workflow-nodes.md`. For the saved-workflow runtime contract and the complete discover -> run -> monitor -> outputs SOP, read `references/workflow-api.md`.

A workflow is a graph of nodes and connections. Input nodes are special:

- `text-input` emits `out-text`.
- `image-input` emits `out-image`.
- `audio-input` emits `out-audio`.
- `video-input` emits `out-video`.

Discover required inputs with `workflow inputs` for the same run scope, then pass run-time values with `workflow run --inputs`, keyed by input node id. Do not patch an Input node's stored `data.value` just to run once. Use `--save-as-default` only when changing workflow defaults.

Text and URL inputs:

```json
{
  "script_input": "大家好，我是 LightX2V 生成的数字人。",
  "image_input": "https://example.com/portrait.png"
}
```

Local media files:

```bash
lightx2v workflow run WORKFLOW_ID \
  --inputs '{"script_input":"大家好，我是 LightX2V 生成的数字人。"}' \
  --input-file portrait_input=./portrait.png \
  --poll
```

`--input-file NODE_ID=PATH` is repeatable. The CLI converts local image/audio/video files to `data:<mime>;base64,...`. Values already accepted in `--inputs` include HTTP(S) URLs, `studio:...`, `task:.../output/...`, and data URLs.

## Create A Digital-Human Workflow

Use this pattern for "make a digital human from portrait + script": `text-input -> tts -> avatar-gen`, plus `image-input -> avatar-gen`. Full node JSON and port rules are in `references/workflow-nodes.md`.

Create and run:

```bash
lightx2v workflow create --input @workflow.json --json

lightx2v workflow run WORKFLOW_ID \
  --inputs '{"script_input":"大家好，我是 LightX2V 生成的数字人。祝你今天开心！"}' \
  --input-file portrait_input=./portrait.png \
  --poll \
  --json

lightx2v workflow outputs WORKFLOW_ID RUN_ID --json
```

If polling times out but status is still `running`, keep the `run_id` and continue with `workflow status`.

## TTS And Voice Clone

For full TTS/voice-clone parameters, workflow `tts` node shape, and troubleshooting, read `references/voice-tts.md`.

List voices first; use `voice_type` and `resource_id` from the same row together.

```bash
lightx2v voices --limit 10

lightx2v tts \
  --text "你好，欢迎使用 LightX2V。" \
  --voice-type zh_female_vv_uranus_bigtts \
  --resource-id seed-tts-2.0 \
  -o speech.mp3
```

Clone and use a voice:

```bash
lightx2v voice-clone create ./voice_sample.wav --save-name "My voice"
lightx2v voice-clone tts --speaker-id SPEAKER_ID --text "你好。" -o cloned.wav
```

## Key Constraints

- API channel credits may differ from web UI; use `--quote` for expensive jobs.
- Prompt max length is usually around `5000` characters.
- Max image upload is usually around `20MB`.
- Large media is better as URL input than huge base64 JSON.
- For `i2v` and `s2v`, assume one primary image unless live model metadata says otherwise.
- Multi-person lip-sync in one image is not a simple API submit; use the web Free Mode workflow if role-track pairing is required.
- For `i2av` multi-keyframe, use one wrapper: `{"input_image":{"type":"base64"|"url","data":[...]}}` plus `image_keyframe_times` and `image_strength`. Do not send an array of mixed media wrapper objects unless the live API explicitly supports it.

## Troubleshooting

- `401`: API key missing, expired, or route not allowed. Re-run `lightx2v login` or check `LIGHTX2V_API_KEY`.
- Local `127.0.0.1` request goes through a proxy: set `NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost`.
- Public/community workflow cannot be run with the account API key: copy or recreate it in the authenticated account first.
- Workflow run returns before final output: query `lightx2v workflow status WORKFLOW_ID RUN_ID --json`, then `workflow outputs`.
- TTS fails with a built-in voice: confirm the voice's paired `resource_id` from `lightx2v voices`; see `references/voice-tts.md`.
- Model name fails: refresh with `lightx2v models --json`; model display names and `model_cls` are not interchangeable.
