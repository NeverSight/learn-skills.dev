---
name: fal-generate
description: Generate AI images, videos, audio and 3D content using fal.ai's 500+ models. Supports Kling V3, FLUX.2, Grok Imagine, Veo 3.1, MiniMax, Hunyuan 3D, OpenRouter LLMs and more via queue-based generation.
---

# fal-generate Skill

## Overview

This skill enables AI content generation through fal.ai's latest models using a queue-based system. It supports:

- **Text-to-Image** - Generate images from text prompts
- **Image-to-Image** - Edit and transform existing images
- **Text-to-Video** - Create videos from text descriptions
- **Image-to-Video** - Animate images into videos
- **Text-to-Speech** - Generate natural speech from text
- **Speech-to-Text** - Transcribe audio to text
- **Text-to-3D** - Create 3D models from text
- **Image-to-3D** - Convert images to 3D models
- **LLM / VLM / ALM** - Run any LLM, vision, audio or video model via OpenRouter

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate.sh` | Main generation tool with queue management |
| `scripts/upload.sh` | Upload files to fal CDN (returns URL) |
| `scripts/poll.sh` | Poll queue status until completion |
| `scripts/models.sh` | Search and discover models |

## Prerequisites

```bash
export FAL_KEY="your-api-key"
```

## Output Format

All generation scripts output **JSON** to stdout when using `--wait`. The JSON contains URLs to the generated content:

- **Images**: `{"images": [{"url": "https://fal.media/files/...", "width": 1024, "height": 1024}]}`
- **Videos**: `{"video": {"url": "https://fal.media/files/...mp4"}}`
- **Audio/TTS**: `{"audio": {"url": "https://fal.media/files/...mp3"}}` or `{"audio_url": "https://..."}`
- **3D Models**: `{"model_mesh": {"url": "https://fal.media/files/...glb"}}`
- **Transcription**: `{"text": "transcribed content..."}`
- **OpenRouter**: `{"output": "LLM response text..."}`

Without `--wait`, prints the request ID. With `--async`, prints only the request ID for later polling.

---

## Examples by Category

### Text-to-Image

```bash
# Basic image generation
./scripts/generate.sh -m fal-ai/kling-image/v3/text-to-image \
  -p "A majestic mountain at sunrise, cinematic lighting" -w

# With aspect ratio and seed
./scripts/generate.sh -m fal-ai/flux-2/klein/9b \
  -p "Professional headshot, studio lighting" \
  --aspect-ratio "1:1" --seed 42 -w

# Ultra-fast generation
./scripts/generate.sh -m fal-ai/z-image/turbo \
  -p "Quick concept sketch of a robot" -w

# With custom parameters (inference steps, guidance scale)
./scripts/generate.sh -m fal-ai/flux-2/klein/9b \
  -p "Detailed portrait of a scientist" \
  --param num_inference_steps=28 --param guidance_scale=3.5 -w
```

### Image-to-Image (Edit/Transform)

```bash
# Upload local image first
IMAGE_URL=$(./scripts/upload.sh ~/photos/portrait.jpg)

# Edit with instructions
./scripts/generate.sh -m fal-ai/qwen-image-max/edit \
  --image-url "$IMAGE_URL" \
  -p "Make the background a sunset beach" -w

# Style transfer
./scripts/generate.sh -m fal-ai/glm-image/image-to-image \
  --image-url "$IMAGE_URL" \
  -p "Convert to oil painting style" -w
```

### Text-to-Video

```bash
# Cinematic video with audio (Kling V3 Pro)
./scripts/generate.sh -m fal-ai/kling-video/v3/pro/text-to-video \
  -p "A butterfly emerging from a cocoon in slow motion, macro lens" \
  --duration 5 -w

# Fast video generation
./scripts/generate.sh -m fal-ai/ltx-2-19b/distilled/text-to-video \
  -p "Drone shot flying over a city at golden hour" -w

# Google Veo 3.1 with sound
./scripts/generate.sh -m fal-ai/veo3.1 \
  -p "A cat playing piano, realistic" -w
```

### Image-to-Video (Animate Images)

```bash
IMAGE_URL=$(./scripts/upload.sh ~/photos/landscape.jpg)

# Animate a still photo
./scripts/generate.sh -m fal-ai/kling-video/o3/pro/image-to-video \
  --image-url "$IMAGE_URL" \
  -p "Gentle wind moving through the trees, clouds drifting" -w

# Lip-sync avatar from image + audio
AUDIO_URL=$(./scripts/upload.sh ~/audio/speech.mp3)
./scripts/generate.sh -m fal-ai/longcat-multi-avatar/image-audio-to-video \
  --image-url "$IMAGE_URL" --audio-url "$AUDIO_URL" -w
```

### Text-to-Speech

```bash
# High-quality TTS (MiniMax)
./scripts/generate.sh -m fal-ai/minimax/speech-2.8-hd \
  -t "Hello! Welcome to the future of AI-generated content." -w

# Fast TTS
./scripts/generate.sh -m fal-ai/minimax/speech-2.8-turbo \
  -t "This is a quick test of fast speech generation." -w

# Custom voice with Qwen-3 TTS
./scripts/generate.sh -m fal-ai/qwen-3-tts/text-to-speech/1.7b \
  -t "Custom voice synthesis with natural intonation." -w
```

### Voice Cloning

```bash
# Upload a voice sample (10+ seconds recommended)
VOICE_URL=$(./scripts/upload.sh ~/audio/voice-sample.wav)

# Clone and generate speech
./scripts/generate.sh -m fal-ai/qwen-3-tts/clone-voice/1.7b \
  --audio-url "$VOICE_URL" \
  -t "This sentence will be spoken in the cloned voice." -w
```

### Speech-to-Text (Transcription)

```bash
AUDIO_URL=$(./scripts/upload.sh ~/recordings/meeting.mp3)

# Fast transcription
./scripts/generate.sh -m fal-ai/nemotron/asr \
  --audio-url "$AUDIO_URL" -w

# Accurate transcription with timestamps
./scripts/generate.sh -m fal-ai/elevenlabs/speech-to-text/scribe-v2 \
  --audio-url "$AUDIO_URL" -w
```

### Text-to-3D

```bash
# Detailed 3D model from text
./scripts/generate.sh -m fal-ai/hunyuan-3d/v3.1/pro/text-to-3d \
  -p "A detailed medieval sword with ornate handle" -w

# Fast 3D generation
./scripts/generate.sh -m fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d \
  -p "Simple wooden chair" -w
```

### Image-to-3D

```bash
IMAGE_URL=$(./scripts/upload.sh ~/photos/object.jpg)

# Convert image to 3D model
./scripts/generate.sh -m fal-ai/hunyuan-3d/v3.1/rapid/image-to-3d \
  --image-url "$IMAGE_URL" -w

# High-fidelity geometry
./scripts/generate.sh -m fal-ai/ultrashape \
  --image-url "$IMAGE_URL" -w
```

### OpenRouter — Run Any LLM

```bash
# Text chat with any LLM (GPT-5, Claude, Gemini, Llama 4, etc.)
./scripts/generate.sh -m openrouter/router \
  -p "Explain quantum computing in simple terms" \
  --param model=google/gemini-2.5-flash -w

# Vision — analyze an image
IMAGE_URL=$(./scripts/upload.sh ~/photos/chart.png)
./scripts/generate.sh -m openrouter/router/vision \
  --image-url "$IMAGE_URL" \
  -p "Describe what you see in this image" \
  --param model=google/gemini-2.5-flash -w

# Audio — process audio with an ALM
AUDIO_URL=$(./scripts/upload.sh ~/audio/podcast.mp3)
./scripts/generate.sh -m openrouter/router/audio \
  --audio-url "$AUDIO_URL" \
  -p "Summarize the key points discussed" \
  --param model=google/gemini-2.5-flash -w

# Video — analyze a video
VIDEO_URL=$(./scripts/upload.sh ~/videos/demo.mp4)
./scripts/generate.sh -m openrouter/router/video \
  --video-url "$VIDEO_URL" \
  -p "Describe what happens in this video" \
  --param model=google/gemini-2.5-flash -w
```

---

## Usage Patterns

### Queue Mode (Default) — submit and poll

```bash
./scripts/generate.sh -m fal-ai/flux-2/klein/9b -p "Portrait" --wait
```

### Async Mode — get ID, poll later

```bash
REQUEST_ID=$(./scripts/generate.sh -m fal-ai/kling-video/v3/pro/text-to-video \
  -p "Drone flying over a city" --async)
./scripts/poll.sh fal-ai/kling-video/v3/pro/text-to-video $REQUEST_ID
```

### File Upload — local files to fal CDN

```bash
IMAGE_URL=$(./scripts/upload.sh ~/photos/portrait.jpg)
./scripts/generate.sh -m fal-ai/kling-video/o3/pro/image-to-video \
  --image-url "$IMAGE_URL" -p "Gentle wind blowing through hair" -w
```

## Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-m, --model` | Model endpoint (required) | `fal-ai/kling-image/v3/text-to-image` |
| `-p, --prompt` | Text description | `"A sunset over mountains"` |
| `-t, --text` | Text for TTS models | `"Hello world"` |
| `--image-url` | Input image URL | `"https://..."` |
| `--video-url` | Input video URL | `"https://..."` |
| `--audio-url` | Input audio URL | `"https://..."` |
| `--aspect-ratio` | Output ratio | `"16:9"`, `"9:16"`, `"1:1"` |
| `--duration` | Video length (sec) | `5`, `10` |
| `--seed` | Reproducibility | `12345` |
| `-w, --wait` | Poll until done | (flag) |
| `-a, --async` | Return ID only | (flag) |
| `--param` | Extra param (repeatable) | `num_inference_steps=28` |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FAL_KEY` | Yes | API authentication key |
| `FAL_WEBHOOK` | No | Webhook URL for callbacks |

## Tips

1. **Always use `--wait` or `--async`** — Without either, you get the request ID + a manual curl command
2. **Use `--param` for advanced control** — Pass any model-specific parameter: `--param guidance_scale=7.5`
3. **Check model schema** — `./scripts/models.sh --schema <endpoint>` to see all available params
4. **Upload files first** — Use `./scripts/upload.sh` for local images/audio/video before generation
5. **Use seeds** — Same seed = same output for reproducible results
6. **Pro vs Standard** — Pro = better quality + longer generation; Standard = cost-effective
7. **Flash/Turbo/Distilled** — Best for previews and fast iterations

---

## Model Catalog

### Image Generation — February 2026

| Endpoint | Description |
|----------|-------------|
| `fal-ai/kling-image/v3/text-to-image` | Kling V3: Latest Kling image model |
| `fal-ai/kling-image/v3/image-to-image` | Kling V3 image transformation |
| `fal-ai/kling-image/o3/text-to-image` | Kling Omni 3: Top-tier consistency |
| `fal-ai/kling-image/o3/image-to-image` | Kling Omni 3 image editing |
| `xai/grok-imagine-image` | xAI Grok Imagine: Highly aesthetic |
| `xai/grok-imagine-image/edit` | Grok Imagine editing |
| `fal-ai/hunyuan-image/v3/instruct/text-to-image` | Hunyuan 3.0 Instruct |
| `fal-ai/hunyuan-image/v3/instruct/edit` | Hunyuan 3.0 editing |
| `fal-ai/qwen-image-max/text-to-image` | Qwen Image Max: Enhanced realism |
| `fal-ai/qwen-image-max/edit` | Qwen Image Max editing |
| `fal-ai/z-image/base` | Z-Image Base: 6B fast model |

### Image Generation — January 2026

| Endpoint | Description |
|----------|-------------|
| `fal-ai/flux-2/klein/9b` | FLUX.2 Klein 9B: Photorealism & text |
| `fal-ai/flux-2/klein/9b/edit` | FLUX.2 Klein 9B editing |
| `fal-ai/flux-2/klein/9b/base/lora` | FLUX.2 Klein 9B with LoRA |
| `fal-ai/flux-2/klein/4b` | FLUX.2 Klein 4B: Lightweight |
| `fal-ai/glm-image` | GLM Image: Accurate text rendering |
| `bria/fibo-edit/edit` | Bria Fibo Edit: Multi-tool editing |
| `bria/fibo-edit/blend` | Bria Fibo composition |
| `bria/fibo-edit/relight` | Bria Fibo relighting |
| `bria/fibo-edit/restyle` | Bria Fibo artistic styles |
| `bria/fibo-lite/generate` | Bria Fibo Lite: Fast generation |
| `imagineart/imagineart-1.5-pro-preview/text-to-image` | ImagineArt 1.5 Pro: 4K |

### Image Generation — December 2025

| Endpoint | Description |
|----------|-------------|
| `fal-ai/flux-2-max` | FLUX.2 Max: State-of-the-art |
| `fal-ai/flux-2/turbo` | FLUX.2 Turbo: Fast generation |
| `fal-ai/flux-2/flash` | FLUX.2 Flash: Ultra-fast |
| `fal-ai/gpt-image-1.5` | GPT Image 1.5: Strong prompt adherence |
| `fal-ai/bytedance/seedream/v4.5/text-to-image` | Seedream 4.5: ByteDance |
| `fal-ai/z-image/turbo` | Z-Image Turbo: 6B super fast |
| `fal-ai/qwen-image-2512` | Qwen Image 2512 |

---

### Video Generation — February 2026

| Endpoint | Description |
|----------|-------------|
| `fal-ai/kling-video/v3/pro/text-to-video` | Kling 3.0 Pro: Cinematic + audio |
| `fal-ai/kling-video/v3/standard/text-to-video` | Kling 3.0 Standard |
| `fal-ai/kling-video/v3/pro/image-to-video` | Kling 3.0 Pro I2V |
| `fal-ai/kling-video/v3/standard/image-to-video` | Kling 3.0 Standard I2V |
| `fal-ai/kling-video/o3/pro/text-to-video` | Kling O3 Pro: Realistic |
| `fal-ai/kling-video/o3/pro/image-to-video` | Kling O3 Pro I2V |
| `fal-ai/kling-video/o3/pro/reference-to-video` | Kling O3 character consistency |
| `xai/grok-imagine-video/text-to-video` | Grok Video with audio |
| `xai/grok-imagine-video/image-to-video` | Grok Video I2V |

### Video Generation — January 2026

| Endpoint | Description |
|----------|-------------|
| `fal-ai/vidu/q3/text-to-video` | Vidu Q3 T2V |
| `fal-ai/vidu/q3/image-to-video` | Vidu Q3 I2V |
| `fal-ai/pixverse/v5.6/text-to-video` | Pixverse V5.6 T2V |
| `fal-ai/pixverse/v5.6/image-to-video` | Pixverse V5.6 I2V |
| `fal-ai/ltx-2-19b/text-to-video` | LTX-2 19B: Video + audio |
| `fal-ai/ltx-2-19b/image-to-video` | LTX-2 19B I2V |
| `fal-ai/ltx-2-19b/distilled/text-to-video` | LTX-2 Distilled: Fast |
| `fal-ai/longcat-multi-avatar/image-audio-to-video` | LongCat: Lip-sync avatar |

### Video Generation — December 2025

| Endpoint | Description |
|----------|-------------|
| `fal-ai/veo3.1` | Veo 3.1: Google's best + sound |
| `fal-ai/veo3.1/fast` | Veo 3.1 Fast |
| `fal-ai/veo3.1/image-to-video` | Veo 3.1 I2V |
| `fal-ai/veo3.1/extend-video` | Veo 3.1 Extend: Up to 30s |
| `fal-ai/hunyuan-video-v1.5/text-to-video` | Hunyuan Video 1.5 T2V |
| `fal-ai/bytedance/seedance/v1.5/pro/text-to-video` | Seedance 1.5 Pro |
| `fal-ai/kandinsky5-pro/text-to-video` | Kandinsky 5 Pro |
| `fal-ai/live-avatar` | Live Avatar: Real-time |
| `clarityai/crystal-video-upscaler` | Crystal Video Upscaler |
| `fal-ai/creatify/aurora` | Creatify Aurora: Studio avatars |

---

### Audio — February 2026

| Endpoint | Description |
|----------|-------------|
| `fal-ai/minimax/speech-2.8-hd` | MiniMax 2.8 HD: Best TTS |
| `fal-ai/minimax/speech-2.8-turbo` | MiniMax 2.8 Turbo: Fast TTS |

### Audio — January 2026

| Endpoint | Description |
|----------|-------------|
| `fal-ai/qwen-3-tts/text-to-speech/1.7b` | Qwen-3 TTS 1.7B: Custom voices |
| `fal-ai/qwen-3-tts/text-to-speech/0.6b` | Qwen-3 TTS 0.6B: Lightweight |
| `fal-ai/qwen-3-tts/clone-voice/1.7b` | Qwen-3 Voice Clone: Zero-shot |
| `fal-ai/qwen-3-tts/clone-voice/0.6b` | Qwen-3 Voice Clone Light |
| `fal-ai/qwen-3-tts/voice-design/1.7b` | Qwen-3 Voice Design |
| `fal-ai/nemotron/asr` | Nemotron ASR: Fast STT |
| `fal-ai/nemotron/asr/stream` | Nemotron ASR Streaming |
| `fal-ai/elevenlabs/voice-changer` | ElevenLabs Voice Changer |
| `fal-ai/elevenlabs/speech-to-text/scribe-v2` | ElevenLabs Scribe V2 |
| `fal-ai/deepfilternet3` | DeepFilterNet3: Noise removal |

### Audio — December 2025

| Endpoint | Description |
|----------|-------------|
| `fal-ai/sam-audio/separate` | SAM Audio: Text-guided separation |
| `fal-ai/elevenlabs/music` | ElevenLabs Music |
| `fal-ai/maya/batch` | Maya: Expressive voice |
| `fal-ai/demucs` | Demucs: SOTA stemming |
| `fal-ai/index-tts-2/text-to-speech` | Index TTS 2.0 |

---

### 3D Generation — February 2026

| Endpoint | Description |
|----------|-------------|
| `fal-ai/hunyuan-3d/v3.1/pro/text-to-3d` | Hunyuan 3D V3.1 Pro: Text to 3D |
| `fal-ai/hunyuan-3d/v3.1/pro/image-to-3d` | Hunyuan 3D V3.1 Pro: Image to 3D |
| `fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d` | Hunyuan 3D Rapid: Fast |
| `fal-ai/hunyuan-3d/v3.1/rapid/image-to-3d` | Hunyuan 3D Rapid I2-3D |
| `fal-ai/ultrashape` | UltraShape: High-fidelity geometry |

### 3D Generation — December 2025

| Endpoint | Description |
|----------|-------------|
| `fal-ai/trellis-2` | Trellis 2: Versatile 3D |
| `fal-ai/hunyuan3d-v3/text-to-3d` | Hunyuan 3D V3 |
| `fal-ai/hunyuan-motion` | Hunyuan Motion: 3D animation |
| `fal-ai/meshy/v6-preview/text-to-3d` | Meshy V6 Preview |

---

## OpenRouter Endpoints

Access 100+ LLMs via OpenRouter. Use `--param model=<provider/model>` to select the model.

### Text (LLM)

| Endpoint | Description |
|----------|-------------|
| `openrouter/router` | Any LLM: GPT-5, Claude, Gemini, Llama 4, Mistral |
| `openrouter/router/stream` | LLM with streaming |
| `openrouter/router/enterprise` | Enterprise LLM (enhanced SLA) |
| `openrouter/router/enterprise/stream` | Enterprise LLM streaming |

### Vision (VLM)

| Endpoint | Description |
|----------|-------------|
| `openrouter/router/vision` | Any VLM: Image analysis with GPT-5, Gemini, Claude |
| `openrouter/router/vision/stream` | Vision streaming |
| `openrouter/router/vision/enterprise` | Enterprise vision |
| `openrouter/router/vision/enterprise/stream` | Enterprise vision streaming |

### Audio (ALM)

| Endpoint | Description |
|----------|-------------|
| `openrouter/router/audio` | Any ALM: Audio analysis with Gemini |
| `openrouter/router/audio/stream` | Audio streaming |
| `openrouter/router/audio/enterprise` | Enterprise audio |
| `openrouter/router/audio/enterprise/stream` | Enterprise audio streaming |

### Video (VLM)

| Endpoint | Description |
|----------|-------------|
| `openrouter/router/video` | Any Video LM: Video analysis with Gemini |
| `openrouter/router/video/stream` | Video streaming |
| `openrouter/router/video/enterprise` | Enterprise video |
| `openrouter/router/video/enterprise/stream` | Enterprise video streaming |

### OpenAI-Compatible

| Endpoint | Description |
|----------|-------------|
| `openrouter/router/openai/v1/chat/completions` | OpenAI Chat Completions API |
| `openrouter/router/openai/v1/responses` | OpenAI Responses API |
| `openrouter/router/openai/v1/embeddings` | OpenAI Embeddings API |

---

## Model Selection Guide

| Use Case | Recommended |
|----------|-------------|
| Best image | `fal-ai/kling-image/o3/text-to-image` |
| Fastest image | `fal-ai/z-image/turbo` |
| Photorealistic | `fal-ai/flux-2/klein/9b` |
| Image editing | `fal-ai/qwen-image-max/edit` |
| Best video | `fal-ai/kling-video/v3/pro/text-to-video` |
| Fastest video | `fal-ai/ltx-2-19b/distilled/text-to-video` |
| Video + audio | `xai/grok-imagine-video/text-to-video` |
| Animate image | `fal-ai/kling-video/o3/pro/image-to-video` |
| Best TTS | `fal-ai/minimax/speech-2.8-hd` |
| Voice clone | `fal-ai/qwen-3-tts/clone-voice/1.7b` |
| Transcription | `fal-ai/nemotron/asr` |
| 3D from text | `fal-ai/hunyuan-3d/v3.1/pro/text-to-3d` |
| 3D from image | `fal-ai/hunyuan-3d/v3.1/rapid/image-to-3d` |
| Any LLM | `openrouter/router` |
| Vision/Audio | `openrouter/router/vision` or `/audio` |