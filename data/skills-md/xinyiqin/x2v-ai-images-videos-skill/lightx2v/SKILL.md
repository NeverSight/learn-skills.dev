---
name: lightx2v
title: X2V 图影
description: LightX2V cloud API for images (t2i, i2i), video (t2v, i2v, s2v, flf2v, animate), TTS, and voice clone. Use when the user asks to generate or edit images, create video from text or image, produce digital human (talking head) video, first-last frame video, convert text to speech, or clone a voice—and content is not adult/restricted (otherwise use lightx2v-local).
homepage: https://x2v.light-ai.top
metadata:
  openclaw:
    emoji: "🎬"
    displayName: "X2V Studio"
    requires:
      env: ["LIGHTX2V_CLOUD_TOKEN"]
    primaryEnv: "LIGHTX2V_CLOUD_TOKEN"
---

# LightX2V

Calls the LightX2V cloud API (base URL default `https://x2v.light-ai.top`, same token for all). Covers: (1) **Image/Video** — t2i, i2i, t2v, i2v, s2v, animate; (2) **TTS** — text-to-speech with preset voices; (3) **Voice clone** — clone voice from audio, then synthesize with cloned voice. Supported models include the **Wan2.2** series (video), **Qwen-2511** (image editing / i2i), and **Qwen-2512** (image generation / t2i). Requires `LIGHTX2V_CLOUD_TOKEN` (and optionally `LIGHTX2V_CLOUD_URL`) to be set.


## Setup

1. Get an access token from the LightX2V platform (e.g. https://x2v.light-ai.top).
2. Set environment variables: either in `skills.entries.lightx2v.env` in openclaw.json (recommended), or export in the shell before running:

```bash
# Optional: only if not using openclaw.json
export LIGHTX2V_CLOUD_TOKEN="your-token"
export LIGHTX2V_CLOUD_URL="https://x2v.light-ai.top"
```

**Auto-load:** The bundled scripts (e.g. `lightx2v_submit_and_poll.sh`, `tts_generate.sh`) automatically read `LIGHTX2V_CLOUD_TOKEN` and `LIGHTX2V_CLOUD_URL` from `~/.openclaw/openclaw.json` when they are not set in the environment. Configure once in openclaw.json and run the scripts directly; no need to export every time.

In OpenClaw config:

```json
"skills": {
  "entries": {
    "lightx2v": {
      "enabled": true,
      "env": {
        "LIGHTX2V_CLOUD_TOKEN": "your-cloud-token",
        "LIGHTX2V_CLOUD_URL": "https://x2v.light-ai.top"
      }
    }
  }
}
```

## API Overview

All calls use the same base URL and Bearer token.

**⚠️ CRITICAL: Authentication Header Required**
**ALL LightX2V API endpoints MUST include the Authorization header:**
```bash
-H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN"
```
Do NOT assume any endpoint works without authentication.

| Action | Endpoint | Purpose |
|--------|----------|---------|
| List models | `GET /api/v1/model/list` | Get available `task` + `model_cls` combinations |
| Submit task | `POST /api/v1/task/submit` | Submit a job; returns `task_id` |
| Query status | `GET /api/v1/task/query?task_id=<id>` | Poll until `status` is SUCCEED / FAILED / CANCELLED |
| Get result | `GET /api/v1/task/result_url?task_id=<id>&name=<name>` | Get download URL; name is `output_image` (t2i/i2i) or `output_video` (t2v/i2v/s2v/flf2v/animate) |
| TTS voices | `GET /api/v1/voices/list` | List preset voices (optional `?version=`) |
| TTS generate | `POST /api/v1/tts/generate` | JSON: text, voice_type, context_texts?, emotion?, emotion_scale?, speech_rate?, pitch?, loudness_rate?, resource_id; returns audio/mpeg (mp3) |
| Voice clone | `POST /api/v1/voice/clone` | multipart: file (audio), optional text; returns speaker_id |
| Voice clone TTS | `POST /api/v1/voice/clone/tts` | JSON: text, speaker_id; returns audio/wav |
| Voice clone list | `GET /api/v1/voice/clone/list` | List user's cloned voices |
| Voice clone save | `POST /api/v1/voice/clone/save` | JSON: speaker_id, name — save clone to collection |
| Voice clone delete | `DELETE /api/v1/voice/clone/{speaker_id}` | Remove a cloned voice |

## Task Types and Inputs

| task | Description | Required | Optional |
|------|-------------|----------|----------|
| **t2i** | Text-to-image | prompt | aspect_ratio |
| **i2i** | Image edit | prompt, input_image | aspect_ratio |
| **t2v** | Text-to-video | prompt | aspect_ratio |
| **i2v** | Image-to-video | prompt, input_image | aspect_ratio |
| **s2v** | Digital human (image + audio) | prompt, input_image, input_audio | — |
| **flf2v** | First–last frame video | `--input-image` (first frame) + `--input-last-frame` (last frame); see [examples/first-last-frame-video.md](examples/first-last-frame-video.md) | — |
| **animate** | Animate with ref video | prompt, input_image, input_video | — |

- `input_image`: one image (file path, URL, or base64 data URL). For i2i multi-image, API accepts array of images.
- `input_audio`: one audio file (WAV preferred; base64 or URL).
- `input_video`: one video file (for animate).
- `prompt`: non-empty text; use space `" "` if the task does not need a text prompt.
- `aspect_ratio`: e.g. `16:9`, `1:1`, `9:16`, `3:4`, `4:3`.

Submit payload shape (JSON):

```json
{
  "task": "t2i",
  "model_cls": "<from model list>",
  "stage": "single_stage",
  "seed": <random 0-999999>,
  "prompt": "user prompt text",
  "aspect_ratio": "16:9",
  "input_image": { "type": "base64", "data": "<base64>" },
  "input_audio": { "type": "base64", "data": "<base64>" }
}
```

For local files: read file, base64-encode, and set `{ "type": "base64", "data": "<base64>" }`. For HTTP(S) URLs use `{ "type": "url", "data": "<url>" }`.

## Workflow

1. **List models** — `GET $LIGHTX2V_CLOUD_URL/api/v1/model/list` with header `Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN`. Choose a `model_cls` whose `task` matches the user request (t2i, i2i, t2v, i2v, s2v, animate).
2. **Submit** — `POST /api/v1/task/submit` with JSON body as above. Remember `task_id` from the response.
3. **Poll** — Call `GET /api/v1/task/query?task_id=<task_id>` every 5–10 seconds until `status` is `SUCCEED`, `FAILED`, or `CANCELLED`. Video tasks (i2v, s2v, t2v, animate) can take several minutes; do not timeout too early. On `FAILED`, report `error` from the response.
4. **Result URL** — For success, call `GET /api/v1/task/result_url?task_id=<task_id>&name=output_image` (t2i/i2i) or `&name=output_video` (t2v/i2v/s2v/flf2v/animate). Return the `url` from the JSON to the user.

**Task progress checklist (image/video tasks):**

```
- [ ] List models and choose model_cls for the requested task (t2i, i2i, t2v, i2v, s2v, flf2v, animate)
- [ ] Submit task with correct payload; record task_id from response
- [ ] Poll task/query every 5–10 s until SUCCEED, FAILED, or CANCELLED
- [ ] On success, get result_url (name=output_image or output_video) and return URL to user
```

## Helper Script

Use the bundled script to submit, poll, and print the result URL:

```bash
# List models (no script; use curl)
curl -s -H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN" \
  "${LIGHTX2V_CLOUD_URL:-https://x2v.light-ai.top}/api/v1/model/list"

# T2I
{baseDir}/scripts/lightx2v_submit_and_poll.sh t2i "<model_cls>" "a cat on the beach" --aspect-ratio 1:1

# T2V (text to video, no image)
{baseDir}/scripts/lightx2v_submit_and_poll.sh t2v "<model_cls>" "a cat walking on the beach at sunset" --aspect-ratio 16:9

# I2I single image (one image + edit prompt)
{baseDir}/scripts/lightx2v_submit_and_poll.sh i2i "<model_cls>" "make it sunset style" --input-image /path/to/image.png --aspect-ratio 1:1

# I2I multi-image: pass --input-image multiple times; URLs use type=url, local paths are auto base64
{baseDir}/scripts/lightx2v_submit_and_poll.sh i2i "<model_cls>" "merge and stylize" --input-image /path/to/1.png --input-image /path/to/2.png --aspect-ratio 1:1

# I2V (image + prompt)
{baseDir}/scripts/lightx2v_submit_and_poll.sh i2v "<model_cls>" "camera pans slowly" --input-image /path/to/image.png

# S2V digital human (image + audio)
{baseDir}/scripts/lightx2v_submit_and_poll.sh s2v "<model_cls>" " " --input-image /path/to/face.png --input-audio /path/to/audio.wav
```

Script usage:

```bash
lightx2v_submit_and_poll.sh <task> <model_cls> <prompt> [--aspect-ratio RATIO] [--input-image PATH|URL [...]] [--input-last-frame PATH|URL] [--input-audio PATH] [--input-video PATH]
```

Output: prints the result URL (image or video) to stdout on success.

## Complete end-to-end examples

**Example 1: Text-to-image (t2i)**

Request: generate an image from the prompt “a cat on the beach at sunset”.

1. Export token: `export LIGHTX2V_CLOUD_TOKEN="<token>"` (and optionally `LIGHTX2V_CLOUD_URL`).
2. List models: `curl -s -H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN" "${LIGHTX2V_CLOUD_URL:-https://x2v.light-ai.top}/api/v1/model/list"` → pick a `model_cls` whose `task` is `t2i` (e.g. Qwen-2512).
3. Run script: `{baseDir}/scripts/lightx2v_submit_and_poll.sh t2i "<model_cls>" "a cat on the beach at sunset" --aspect-ratio 1:1`.
4. Outcome: script prints the result image URL to stdout; that URL is returned to the user.

**Example 2: TTS (preset voice)**

Request: synthesize “Hello, welcome.” with a female preset voice.

1. Export token (as above).
2. List voices: `{baseDir}/scripts/tts_voice_list.sh` or `curl -s -H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN" "${LIGHTX2V_CLOUD_URL:-https://x2v.light-ai.top}/api/v1/voices/list"` → choose a `voice_type` (e.g. `zh_female_vv_uranus_bigtts`).
3. Run script: `{baseDir}/scripts/tts_generate.sh "Hello, welcome." "zh_female_vv_uranus_bigtts" --output files/audio/hello.mp3`.
4. Outcome: script writes MP3 to `files/audio/hello.mp3`; that file path (or the saved file) is returned to the user.

**Example 3: Digital human (s2v) with scene image + TTS**

Request: talking-head video with a given face image and the line “Good morning.”

1. Export token. Get model list and pick `model_cls` for `s2v` (e.g. SekoTalk).
2. Scene image: use i2i (or t2i if no image) to get a scene/portrait image URL; e.g. `lightx2v_submit_and_poll.sh i2i "<model_cls>" "keep character consistent, portrait in warm lighting" --input-image /path/to/face.png --aspect-ratio 9:16`.
3. TTS: `tts_generate.sh "Good morning." "<voice_type>" --output files/audio/greeting.mp3` (optionally with `--context-texts "warm, friendly"` for v2.0).
4. S2V: `lightx2v_submit_and_poll.sh s2v "<s2v_model_cls>" " " --input-image <scene_image_url_or_path> --input-audio files/audio/greeting.mp3`.
5. Outcome: script prints the result video URL; that URL is returned to the user (or the video is downloaded to `files/video/` and the path is returned).

---

## TTS (Text-to-Speech)

Preset voices; same base URL and token.

**List voices:** `GET /api/v1/voices/list` (optional `?version=...`). Response: `{ voices: [...], emotions?: [...], languages?: [...] }`. Use `voice_type` from list for generate.

**Generate:** `POST /api/v1/tts/generate` with JSON:

```json
{
  "text": "Text to synthesize",
  "voice_type": "zh_female_1",
  "context_texts": "",
  "emotion": "",
  "emotion_scale": 3,
  "speech_rate": 0,
  "pitch": 0,
  "loudness_rate": 0,
  "resource_id": "seed-tts-2.0"
}
```

| Field | Description | Default |
|-------|-------------|--------|
| `text` | Text to synthesize | required |
| `voice_type` | From `GET /api/v1/voices/list` | required |
| `resource_id` | From voice list (script resolves automatically) | required |
| `context_texts` | Scene/tone/voice instructions (v2.0 preset voices only) | `""` |
| `emotion` | Emotion label | `""` |
| `emotion_scale` | Emotion intensity 1–5 | `3` |
| `speech_rate` | Speech rate offset (e.g. -2 to 2) | `0` |
| `loudness_rate` | Loudness offset | `0` |
| `pitch` | Pitch offset | `0` |

### Writing guidelines

- **`text` vs `context_texts`:**
  - **`text`** — Only the script to be read aloud. Do not put scene descriptions, tone, or voice-direction text here.
  - **Scene, tone, and voice direction** (e.g. “gently”, “lowered voice”, “with breath”, “as if whispering”) must go in **`context_texts`**. This keeps synthesis stable and lets the model separate “what to read” from “how to read”.
- **Pauses and rhythm:** Ellipses may be added where pauses are desired so the delivery has breathing room. Common approach: add ellipses after commas, full stops, and question marks (e.g. `...,`, `....`, `...?`), or use “…” / “……” after words where a pause is needed. See the my_boyfriend skill for dialogue and the `--add-pauses` behaviour.

### Notes

- **resource_id:** Each voice has a matching `resource_id` from the voice list. The script `tts_generate.sh` fetches the list and fills it automatically.
- **Voice instructions scope:** Only **v2.0 preset voices** support `context_texts` and in-text markers like `【gently】`. **v1.0 presets and cloned voices do not** — leave `context_texts` empty and do not rely on 【】 markers for those.
- **Binary response:** The generate endpoint returns **audio/mpeg (mp3)** binary. Do not capture it in a shell variable (e.g. `RESP=$(curl ...)`), or null bytes will truncate and corrupt the file. Redirect directly to a file: `curl ... > out.mp3`, then check the file is non-empty or has an ID3 header (e.g. `head -c 10 out.mp3 | grep -q ID3`). Using a variable can cause “ignored null byte in input” and broken audio.

Response is binary **audio/mpeg** (mp3). Save to a file (e.g. `--output out.mp3`) and return that path to the user.

**Helper script:**

```bash
# List voices
{baseDir}/scripts/tts_voice_list.sh
# or: curl -s -H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN" "${LIGHTX2V_CLOUD_URL:-https://x2v.light-ai.top}/api/v1/voices/list"

# Generate TTS (script auto-resolves resource_id from voice list)
{baseDir}/scripts/tts_generate.sh "Text to synthesize" "voice_type_from_list" [--output out.mp3] \
  [--context-texts "Scene/tone instructions"] [--emotion "emotion"] [--emotion-scale N] \
  [--speech-rate N] [--loudness-rate N] [--pitch N]
```

Script uses env: `LIGHTX2V_CLOUD_URL` (or base URL), `LIGHTX2V_CLOUD_TOKEN` (optional). Optional args: `--context-texts` (scene/tone), `--emotion`, `--emotion-scale` (default 3), `--speech-rate`, `--loudness-rate`, `--pitch` (default 0).

**Recommended voices for digital human / companion:** Male `zh_male_ruyayichen_saturn_bigtts`, Female `zh_female_vv_uranus_bigtts` (Vivi 2.0); both v2.0 and support `context_texts` (voice instructions). These are suggestions only — more voices are available via `tts_voice_list.sh` or `GET /api/v1/voices/list`; do not hardcode, choose from the list when needed.

---

## Voice Clone

Clone a voice from a short audio sample, then synthesize speech with that voice. Same base URL and token; requires auth.

1. **Clone:** `POST /api/v1/voice/clone` — **multipart/form-data**: `file` (audio file, WAV preferred), optional `text` (transcript; if omitted, server uses ASR). Response: `{ speaker_id, text, message }`. Use `speaker_id` for clone TTS and save.
2. **Synthesize with cloned voice:** `POST /api/v1/voice/clone/tts` — JSON: `{ text, speaker_id, style?: "normal", speed?: 1.0, volume?: 0, pitch?: 0, language?: "ZH_CN" }`. Response: binary **audio/wav**. **Note:** Voice cloning does NOT support voice instructions like 【gently】.
3. **Save to collection (optional):** `POST /api/v1/voice/clone/save` — JSON: `{ speaker_id, name }`.
4. **List clones:** `GET /api/v1/voice/clone/list` — returns `{ voice_clones: [...] }`.
5. **Delete clone:** `DELETE /api/v1/voice/clone/{speaker_id}`.

**Helper scripts:**

```bash
# Clone from audio file; prints speaker_id
{baseDir}/scripts/voice_clone.sh /path/to/audio.wav [--text "Transcript of the audio"]

# TTS with cloned voice; saves WAV to --output (default voice_clone_tts.wav)
{baseDir}/scripts/voice_clone_tts.sh <speaker_id> "Text to speak" [--output out.wav]

# List user's cloned voices
curl -s -H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN" \
  "${LIGHTX2V_CLOUD_URL:-https://x2v.light-ai.top}/api/v1/voice/clone/list"
```

---

## When to Use This Skill

Use **lightx2v** (cloud) only when the user’s request does **not** involve adult or restricted (NSFW) content. If it does, use **lightx2v-local** instead.

- User asks to **generate an image** from text (non-adult) → task `t2i`, get model from list.
- User asks to **edit or modify an image** (non-adult) → task `i2i`, require one input image + prompt.
- User asks to **generate a video** from text (non-adult) → task `t2v`.
- User asks to **animate an image** or **image to video** (non-adult) → task `i2v`, require input image + prompt.
- User asks for **digital human / talking head** video (face + voice, non-adult) → task `s2v`, require input_image + input_audio; prompt can be a space.
- User asks to **convert text to speech** or **TTS** with a preset voice → use `GET /api/v1/voices/list` to pick `voice_type`, then `POST /api/v1/tts/generate`; return the saved MP3 path or URL.
- User asks to **clone a voice** from an audio sample → `POST /api/v1/voice/clone` with the audio file; then use `speaker_id` for `POST /api/v1/voice/clone/tts` to synthesize with that voice. Optionally save with `/api/v1/voice/clone/save`.

`LIGHTX2V_CLOUD_TOKEN` (and optionally `LIGHTX2V_CLOUD_URL`) must be set before calling the API.

---

## Troubleshooting

### "Could not validate credentials" (401)

All LightX2V endpoints require the `Authorization: Bearer $TOKEN` header. This error usually means:

1. **Header missing** — Every curl/request must include `-H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN"`.
2. **Token not exported** — Values in openclaw.json are not auto-injected. Before running scripts or curl, run `export LIGHTX2V_CLOUD_TOKEN="..."` (or read from config and export).
3. **Token format** — No extra quotes or spaces; token may be expired or invalid.

**Quick check:**

```bash
echo "Token length: $(echo -n "$LIGHTX2V_CLOUD_TOKEN" | wc -c)"
curl -s -H "Authorization: Bearer $LIGHTX2V_CLOUD_TOKEN" \
  "${LIGHTX2V_CLOUD_URL:-https://x2v.light-ai.top}/api/v1/voices/list" | head -3
```

### TTS / "ignored null byte in input" or corrupted MP3

TTS returns **binary** data. Do not use command substitution:

```bash
# ❌ Wrong — corrupts audio
TTS_RESPONSE=$(curl ... /api/v1/tts/generate)
echo "$TTS_RESPONSE" > audio.mp3

# ✅ Correct — direct to file
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"text":"...","voice_type":"...","resource_id":"..."}' \
  "$BASE_URL/api/v1/tts/generate" > audio.mp3
```

Validate: `[ -s audio.mp3 ] && head -c 10 audio.mp3 | grep -q ID3`.

### Other

- **Model not found:** Call `GET /api/v1/model/list` and pick a `model_cls` that supports the task (t2i, i2i, s2v, etc.).
- **Voice / resource_id:** Each voice in voices/list has its own `resource_id`; use the one from the list for that `voice_type`.
- **Large result files:** Prefer returning the result **URL** from `result_url` (or local path) rather than embedding large files in messages; some clients have size limits.

## Additional resources

For multi-step workflows (first–last frame video, digital human video, one-sentence to video, virtual companion), see the **examples** in the skill directory:

- [examples/first-last-frame-video.md](examples/first-last-frame-video.md) — flf2v: first frame → i2i last frame → flf2v
- [examples/digital-human-video.md](examples/digital-human-video.md) — s2v: scene image + TTS → talking-head video
- [examples/one-sentence-to-video.md](examples/one-sentence-to-video.md) — t2i/i2i → i2v: one key image → short video
- [examples/virtual-boyfriend-video.md](examples/virtual-boyfriend-video.md) — virtual boyfriend/girlfriend: persona (SOUL.md); prompt user to upload character image, save to `avatar/`, prefer existing avatar for i2i; then scene + TTS/s2v or i2v