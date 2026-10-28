---
name: parlor-on-device-ai
description: On-device, real-time multimodal AI voice and vision assistant powered by Gemma 4 E2B and Kokoro TTS, running entirely locally via FastAPI WebSocket server.
triggers:
  - "set up parlor on-device AI"
  - "run local voice AI with camera"
  - "configure parlor multimodal assistant"
  - "use Gemma 4 with Kokoro TTS locally"
  - "build real-time voice assistant on device"
  - "parlor websocket voice vision server"
  - "on-device speech and vision AI"
  - "run parlor with Apple Silicon"
---

# Parlor On-Device AI

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Parlor is a real-time, on-device multimodal AI assistant. It combines Gemma 4 E2B (via LiteRT-LM) for speech and vision understanding with Kokoro TTS for voice output. Everything runs locally — no API keys, no cloud calls, no cost per request.

## Architecture

```
Browser (mic + camera)
    │
    │  WebSocket (audio PCM + JPEG frames)
    ▼
FastAPI server
    ├── Gemma 4 E2B via LiteRT-LM (GPU)  →  understands speech + vision
    └── Kokoro TTS (MLX on Mac, ONNX on Linux)  →  speaks back
    │
    │  WebSocket (streamed audio chunks)
    ▼
Browser (playback + transcript)
```

Key features:
- **Silero VAD** in browser — hands-free, no push-to-talk
- **Barge-in** — interrupt AI mid-sentence by speaking
- **Sentence-level TTS streaming** — audio starts before full response is ready
- **Platform-aware TTS** — MLX backend on Apple Silicon, ONNX on Linux

## Requirements

- Python 3.12+
- macOS with Apple Silicon **or** Linux with a supported GPU
- ~3 GB free RAM
- [`uv`](https://github.com/astral-sh/uv) package manager

## Installation

```bash
git clone https://github.com/fikrikarim/parlor.git
cd parlor

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

cd src
uv sync
uv run server.py
```

Open [http://localhost:8000](http://localhost:8000), grant camera and microphone permissions, and start talking.

Models download automatically on first run (~2.6 GB for Gemma 4 E2B, plus TTS models).

## Configuration

Set environment variables before running:

```bash
# Use a pre-downloaded model instead of auto-downloading
export MODEL_PATH=/path/to/gemma-4-E2B-it.litertlm

# Change server port (default: 8000)
export PORT=9000

uv run server.py
```

| Variable     | Default                        | Description                                    |
|--------------|-------------------------------|------------------------------------------------|
| `MODEL_PATH` | auto-download from HuggingFace | Path to local `.litertlm` model file           |
| `PORT`       | `8000`                         | Server port                                    |

## Project Structure

```
src/
├── server.py              # FastAPI WebSocket server + Gemma 4 inference
├── tts.py                 # Platform-aware TTS (MLX on Mac, ONNX on Linux)
├── index.html             # Frontend UI (VAD, camera, audio playback)
├── pyproject.toml         # Dependencies
└── benchmarks/
    ├── bench.py           # End-to-end WebSocket benchmark
    └── benchmark_tts.py   # TTS backend comparison
```

## Key Components

### server.py — FastAPI WebSocket Server

The server handles two WebSocket connections: one for receiving audio/video from the browser, one for streaming audio back.

```python
# Simplified pattern from server.py
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for data in websocket.iter_bytes():
        # data contains PCM audio + optional JPEG frame
        response_text = await run_gemma_inference(data)
        audio_chunks = await run_tts(response_text)
        for chunk in audio_chunks:
            await websocket.send_bytes(chunk)
```

### tts.py — Platform-Aware TTS

Kokoro TTS selects backend based on platform:

```python
# tts.py uses platform detection
import platform

def get_tts_backend():
    if platform.system() == "Darwin":
        # Apple Silicon: use MLX backend for GPU acceleration
        from kokoro_mlx import KokoroMLX
        return KokoroMLX()
    else:
        # Linux: use ONNX backend
        from kokoro import KokoroPipeline
        return KokoroPipeline(lang_code='a')

tts = get_tts_backend()

# Sentence-level streaming — yields audio as each sentence is ready
async def synthesize_streaming(text: str):
    for sentence in split_sentences(text):
        audio = tts.synthesize(sentence)
        yield audio
```

### Gemma 4 E2B Inference via LiteRT-LM

```python
# LiteRT-LM inference pattern
from litert_lm import LiteRTLM
import os

model_path = os.environ.get("MODEL_PATH", None)

# Auto-downloads if MODEL_PATH not set
model = LiteRTLM.from_pretrained(
    "google/gemma-4-E2B-it",
    local_path=model_path
)

async def run_gemma_inference(audio_pcm: bytes, image_jpeg: bytes = None):
    inputs = {"audio": audio_pcm}
    if image_jpeg:
        inputs["image"] = image_jpeg
    
    response = ""
    async for token in model.generate_stream(**inputs):
        response += token
    return response
```

## Running Benchmarks

```bash
cd src

# End-to-end WebSocket latency benchmark
uv run benchmarks/bench.py

# Compare TTS backends (MLX vs ONNX)
uv run benchmarks/benchmark_tts.py
```

## Performance Reference (Apple M3 Pro)

| Stage                            | Time          |
|----------------------------------|---------------|
| Speech + vision understanding    | ~1.8–2.2s     |
| Response generation (~25 tokens) | ~0.3s         |
| Text-to-speech (1–3 sentences)   | ~0.3–0.7s     |
| **Total end-to-end**             | **~2.5–3.0s** |

Decode speed: ~83 tokens/sec on GPU.

## Common Patterns

### Extending the System Prompt

Modify the prompt in `server.py` to change the AI's persona or task:

```python
SYSTEM_PROMPT = """You are a helpful language tutor. 
Respond conversationally in 1-3 sentences.
If the user makes a grammar mistake, gently correct them.
You can see through the user's camera and discuss what you observe."""
```

### Adding a New Language for TTS

Kokoro supports multiple language codes. Set `lang_code` in `tts.py`:

```python
# Language codes: 'a' = American English, 'b' = British English
# 'e' = Spanish, 'f' = French, 'z' = Chinese, 'j' = Japanese
pipeline = KokoroPipeline(lang_code='e')  # Spanish
```

### Customizing VAD Sensitivity (index.html)

The Silero VAD threshold can be tuned in the frontend:

```javascript
// In index.html — lower positiveSpeechThreshold = more sensitive
const vad = await MicVAD.new({
  positiveSpeechThreshold: 0.6,   // default ~0.8, lower = triggers more easily
  negativeSpeechThreshold: 0.35,  // how quickly it stops detecting speech
  minSpeechFrames: 3,
  onSpeechStart: () => { /* UI feedback */ },
  onSpeechEnd: (audio) => sendAudioToServer(audio),
});
```

### Sending Frames Programmatically (WebSocket Client Example)

```python
import asyncio
import websockets
import json
import base64

async def send_audio_frame(audio_pcm_bytes: bytes, jpeg_bytes: bytes = None):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as ws:
        payload = {
            "audio": base64.b64encode(audio_pcm_bytes).decode(),
        }
        if jpeg_bytes:
            payload["image"] = base64.b64encode(jpeg_bytes).decode()
        
        await ws.send(json.dumps(payload))
        
        # Receive streamed audio response
        async for message in ws:
            audio_chunk = message  # raw PCM bytes
            # play or save audio_chunk
```

## Troubleshooting

### Model download fails
```bash
# Pre-download manually via huggingface_hub
uv run python -c "
from huggingface_hub import hf_hub_download
path = hf_hub_download('google/gemma-4-E2B-it', 'gemma-4-E2B-it.litertlm')
print(path)
"
export MODEL_PATH=/path/shown/above
uv run server.py
```

### Microphone/camera not working in browser
- Must access via `http://localhost` (not IP address) — browsers block media APIs on non-localhost HTTP
- Check browser permissions: address bar → lock icon → reset permissions

### TTS not loading on Linux
```bash
# Ensure ONNX runtime is installed
uv add onnxruntime
# Or for GPU:
uv add onnxruntime-gpu
```

### High latency or slow inference
- Verify GPU is being used: check for Metal (Mac) or CUDA (Linux) in startup logs
- Close other GPU-heavy applications
- On Linux, confirm CUDA drivers match installed `onnxruntime-gpu` version

### Port already in use
```bash
export PORT=8080
uv run server.py
# Or kill the existing process:
lsof -ti:8000 | xargs kill
```

### `uv sync` fails — Python version mismatch
```bash
# Parlor requires Python 3.12+
python3 --version
# Install 3.12 via pyenv or system package manager, then:
uv python pin 3.12
uv sync
```

## Dependencies (pyproject.toml)

Key packages installed by `uv sync`:
- `litert-lm` — Google AI Edge inference runtime for Gemma
- `fastapi` + `uvicorn` — async web/WebSocket server
- `kokoro` — Kokoro TTS ONNX backend
- `kokoro-mlx` — Kokoro TTS MLX backend (Mac only)
- `silero-vad` — voice activity detection (browser-side via CDN)
- `huggingface-hub` — model auto-download
