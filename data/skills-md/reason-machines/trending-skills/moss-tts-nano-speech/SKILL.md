---
name: moss-tts-nano-speech
description: Expert skill for using MOSS-TTS-Nano, a 0.1B parameter multilingual real-time TTS model that runs on CPU with voice cloning support.
triggers:
  - generate speech with MOSS TTS
  - text to speech with voice cloning
  - moss tts nano inference
  - run MOSS-TTS-Nano locally
  - multilingual TTS CPU inference
  - clone voice with MOSS
  - streaming audio generation python
  - tiny TTS model deployment
---

# MOSS-TTS-Nano Speech Generation Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

MOSS-TTS-Nano is an open-source multilingual tiny TTS model (0.1B parameters) from MOSI.AI and the OpenMOSS team. It uses an Audio Tokenizer + LLM autoregressive pipeline to generate 48 kHz stereo speech in real time, supports 20 languages, voice cloning, streaming inference, and runs on CPU without a GPU.

## Installation

### Conda (recommended)

```bash
conda create -n moss-tts-nano python=3.12 -y
conda activate moss-tts-nano

git clone https://github.com/OpenMOSS/MOSS-TTS-Nano.git
cd MOSS-TTS-Nano

pip install -r requirements.txt
pip install -e .
```

### Fix WeTextProcessing if it fails

```bash
conda install -c conda-forge pynini=2.1.6.post1 -y
pip install git+https://github.com/WhizZest/WeTextProcessing.git
```

After `pip install -e .` the `moss-tts-nano` CLI command is available in the active environment.

## Model Weights

Models are auto-downloaded from Hugging Face on first run:
- TTS model: `OpenMOSS-Team/MOSS-TTS-Nano`
- Audio tokenizer: `OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano`

ModelScope mirrors are available at `openmoss/MOSS-TTS-Nano` and `openmoss/MOSS-Audio-Tokenizer-Nano`.

## CLI Commands

### Generate speech (voice clone mode)

```bash
moss-tts-nano generate \
  --prompt-speech assets/audio/zh_1.wav \
  --text "欢迎关注模思智能、上海创智学院与复旦大学自然语言处理实验室。"
```

Output defaults to `generated_audio/moss_tts_nano_output.wav`.

### Generate from a text file (long-form)

```bash
moss-tts-nano generate \
  --prompt-speech assets/audio/zh_1.wav \
  --text-file my_script.txt \
  --output output.wav
```

### Launch local web demo

```bash
moss-tts-nano serve
# or directly:
python app.py
```

Opens at `http://127.0.0.1:18083` — model stays loaded in memory for fast repeated requests.

### Direct Python entrypoint

```bash
python infer.py \
  --prompt-audio-path assets/audio/zh_1.wav \
  --text "Hello, this is a test of MOSS-TTS-Nano."
```

Output: `generated_audio/infer_output.wav`

## Python API Usage

### Basic voice clone inference

```python
from infer import MossTTSNanoInference

# Initialize once (downloads weights on first run)
tts = MossTTSNanoInference()

# Voice clone: synthesize text in the style of the reference audio
audio = tts.infer(
    text="欢迎使用MOSS语音合成系统。",
    prompt_audio_path="assets/audio/zh_1.wav",
)

# Save output
import soundfile as sf
sf.write("output.wav", audio, samplerate=48000)
```

### English voice clone

```python
from infer import MossTTSNanoInference

tts = MossTTSNanoInference()

audio = tts.infer(
    text="Welcome to MOSS TTS Nano, a tiny but capable text to speech model.",
    prompt_audio_path="assets/audio/en_sample.wav",
)

import soundfile as sf
sf.write("english_output.wav", audio, samplerate=48000)
```

### Streaming inference (low latency)

```python
from infer import MossTTSNanoInference
import soundfile as sf
import numpy as np

tts = MossTTSNanoInference()

chunks = []
for audio_chunk in tts.infer_stream(
    text="This sentence is generated chunk by chunk for low latency playback.",
    prompt_audio_path="assets/audio/en_sample.wav",
):
    chunks.append(audio_chunk)
    # process or play chunk in real time here

full_audio = np.concatenate(chunks)
sf.write("streamed_output.wav", full_audio, samplerate=48000)
```

### Long-text synthesis with chunked voice cloning

```python
from infer import MossTTSNanoInference

tts = MossTTSNanoInference()

long_text = """
MOSS-TTS-Nano supports long-form synthesis through automatic chunking.
Each chunk uses the same reference voice, producing consistent speaker identity
across the entire output even for multi-paragraph documents.
"""

audio = tts.infer(
    text=long_text,
    prompt_audio_path="assets/audio/en_sample.wav",
)

import soundfile as sf
sf.write("long_form_output.wav", audio, samplerate=48000)
```

### FastAPI HTTP endpoint usage

When the server is running (`moss-tts-nano serve` or `python app.py`):

```python
import requests
import base64
import soundfile as sf
import io
import numpy as np

# Read reference audio as base64
with open("assets/audio/zh_1.wav", "rb") as f:
    ref_audio_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://127.0.0.1:18083/generate",
    json={
        "text": "你好，这是一个语音合成测试。",
        "prompt_audio_base64": ref_audio_b64,
    },
)

data = response.json()
audio_bytes = base64.b64decode(data["audio_base64"])

audio_array, sr = sf.read(io.BytesIO(audio_bytes))
sf.write("api_output.wav", audio_array, samplerate=sr)
```

### Streaming HTTP response (real-time web playback)

```python
import requests

with open("assets/audio/zh_1.wav", "rb") as f:
    ref_audio_b64 = __import__("base64").b64encode(f.read()).decode()

with requests.post(
    "http://127.0.0.1:18083/generate_stream",
    json={
        "text": "流式语音合成示例，适合实时播放场景。",
        "prompt_audio_base64": ref_audio_b64,
    },
    stream=True,
) as resp:
    with open("stream_output.wav", "wb") as out:
        for chunk in resp.iter_content(chunk_size=4096):
            out.write(chunk)
```

## Supported Languages

| Code | Language   | Code | Language  | Code | Language |
|------|-----------|------|-----------|------|----------|
| zh   | Chinese   | en   | English   | de   | German   |
| es   | Spanish   | fr   | French    | ja   | Japanese |
| it   | Italian   | hu   | Hungarian | ko   | Korean   |
| ru   | Russian   | fa   | Persian   | ar   | Arabic   |
| pl   | Polish    | pt   | Portuguese| cs   | Czech    |
| da   | Danish    | sv   | Swedish   | el   | Greek    |
| tr   | Turkish   |      |           |      |          |

The language is inferred automatically from the input text and the reference audio. No explicit language code parameter is required for basic usage.

## Architecture Overview

- **Pipeline**: Audio Tokenizer + LLM (pure autoregressive)
- **Audio Tokenizer**: MOSS-Audio-Tokenizer-Nano (~20M params), CNN-free causal Transformer (Cat architecture)
- **Output**: 48 kHz, 2-channel (stereo)
- **Token rate**: 12.5 Hz token stream
- **Codebooks**: RVQ with 16 codebooks (0.125 kbps – 2 kbps)
- **LLM**: ~0.1B parameters total

## Key CLI Flags

| Flag | Alias | Description |
|------|-------|-------------|
| `--prompt-audio-path` | — | Path to reference WAV for voice cloning (`infer.py`) |
| `--prompt-speech` | — | Same purpose in `moss-tts-nano generate` CLI |
| `--text` | — | Input text string |
| `--text-file` | — | Path to plain text file for long-form synthesis |
| `--output` | — | Output WAV file path (default varies by entrypoint) |

## Common Patterns

### Pattern: Batch synthesis with one reference voice

```python
from infer import MossTTSNanoInference
import soundfile as sf

tts = MossTTSNanoInference()
ref = "assets/audio/zh_1.wav"

sentences = [
    "第一句话，用于批量合成测试。",
    "第二句话，保持相同的音色。",
    "第三句话，输出独立的音频文件。",
]

for i, sentence in enumerate(sentences):
    audio = tts.infer(text=sentence, prompt_audio_path=ref)
    sf.write(f"output_{i:02d}.wav", audio, samplerate=48000)
    print(f"Saved output_{i:02d}.wav")
```

### Pattern: Real-time playback with sounddevice

```python
import sounddevice as sd
import numpy as np
from infer import MossTTSNanoInference

tts = MossTTSNanoInference()

buffer = []
for chunk in tts.infer_stream(
    text="Real-time playback example using sounddevice.",
    prompt_audio_path="assets/audio/en_sample.wav",
):
    buffer.append(chunk)

audio = np.concatenate(buffer)
sd.play(audio, samplerate=48000)
sd.wait()
```

### Pattern: Gradio integration

```python
import gradio as gr
import soundfile as sf
import numpy as np
import io
from infer import MossTTSNanoInference

tts = MossTTSNanoInference()

def synthesize(reference_audio_path: str, text: str):
    audio = tts.infer(text=text, prompt_audio_path=reference_audio_path)
    # Return as (sample_rate, numpy_array) tuple for Gradio Audio component
    return (48000, audio)

demo = gr.Interface(
    fn=synthesize,
    inputs=[
        gr.Audio(type="filepath", label="Reference Voice"),
        gr.Textbox(label="Text to synthesize"),
    ],
    outputs=gr.Audio(label="Generated Speech"),
    title="MOSS-TTS-Nano Voice Clone",
)

demo.launch()
```

## Troubleshooting

### WeTextProcessing install fails

```bash
# Use conda to get pynini, then install from source
conda install -c conda-forge pynini=2.1.6.post1 -y
pip install git+https://github.com/WhizZest/WeTextProcessing.git
```

### Model download is slow or fails

Set `HF_ENDPOINT` to a mirror if Hugging Face is unreachable:

```bash
export HF_ENDPOINT=https://hf-mirror.com
python infer.py --prompt-audio-path assets/audio/zh_1.wav --text "测试"
```

Or use ModelScope:

```bash
pip install modelscope
```

Then point model paths to `openmoss/MOSS-TTS-Nano` and `openmoss/MOSS-Audio-Tokenizer-Nano`.

### Out of memory on CPU

- Use streaming inference (`infer_stream`) to reduce peak memory.
- Reduce chunk size for long text inputs — the model handles chunked voice cloning automatically.
- Close other applications; the model needs ~1–2 GB RAM.

### Audio output is silent or corrupt

- Ensure the reference WAV is a clean mono or stereo file, 16-bit or float32, any sample rate (it will be resampled).
- Minimum reference audio duration: ~3–5 seconds for reliable voice cloning.
- Avoid reference audio with heavy background noise.

### `moss-tts-nano` command not found

```bash
# Re-run editable install inside the active conda env
pip install -e .
which moss-tts-nano   # should resolve now
```

### Port conflict for web demo

```bash
# Default port is 18083; check what occupies it
lsof -i :18083
# Kill if needed, then relaunch
moss-tts-nano serve
```

## Output Defaults

| Entrypoint | Default output path |
|---|---|
| `python infer.py` | `generated_audio/infer_output.wav` |
| `moss-tts-nano generate` | `generated_audio/moss_tts_nano_output.wav` |
| `python app.py` / `moss-tts-nano serve` | returned via HTTP response |

The `generated_audio/` directory is created automatically if it does not exist.
