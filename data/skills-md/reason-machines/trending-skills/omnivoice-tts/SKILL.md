---
name: omnivoice-tts
description: Expert skill for OmniVoice, a massively multilingual zero-shot TTS model supporting 600+ languages with voice cloning and voice design capabilities.
triggers:
  - clone a voice with OmniVoice
  - text to speech 600 languages
  - OmniVoice voice cloning
  - multilingual TTS python
  - generate speech with voice design
  - omnivoice batch inference
  - zero-shot TTS voice cloning python
  - OmniVoice installation and usage
---

# OmniVoice TTS Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OmniVoice is a state-of-the-art zero-shot TTS model supporting 600+ languages, built on a diffusion language model-style architecture. It supports voice cloning (from reference audio), voice design (via text attributes), and auto voice generation with RTF as low as 0.025.

---

## Installation

### Requirements
- Python 3.9+
- PyTorch 2.8+
- CUDA (recommended) or Apple Silicon (MPS) or CPU

### pip (recommended)

```bash
# Step 1: Install PyTorch for your platform

# NVIDIA GPU (CUDA 12.8)
pip install torch==2.8.0+cu128 torchaudio==2.8.0+cu128 --extra-index-url https://download.pytorch.org/whl/cu128

# Apple Silicon
pip install torch==2.8.0 torchaudio==2.8.0

# Step 2: Install OmniVoice
pip install omnivoice

# Or from source (latest)
pip install git+https://github.com/k2-fsa/OmniVoice.git

# Or editable dev install
git clone https://github.com/k2-fsa/OmniVoice.git
cd OmniVoice
pip install -e .
```

### uv

```bash
git clone https://github.com/k2-fsa/OmniVoice.git
cd OmniVoice
uv sync
# With mirror: uv sync --default-index "https://mirrors.aliyun.com/pypi/simple"
```

### HuggingFace Mirror (if blocked)

```bash
export HF_ENDPOINT="https://hf-mirror.com"
```

---

## Core Concepts

| Mode | What you provide | Use case |
|---|---|---|
| **Voice Cloning** | `ref_audio` + `ref_text` | Clone a speaker from a short audio clip |
| **Voice Design** | `instruct` string | Describe speaker attributes (no audio needed) |
| **Auto Voice** | nothing extra | Model picks a random voice |

---

## Python API

### Load the Model

```python
from omnivoice import OmniVoice
import torch
import torchaudio

# NVIDIA GPU
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16
)

# Apple Silicon
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="mps",
    dtype=torch.float16
)

# CPU (slower)
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cpu",
    dtype=torch.float32
)
```

### Voice Cloning

```python
# With manual reference transcription (faster, more accurate)
audio = model.generate(
    text="Hello, this is a test of zero-shot voice cloning.",
    ref_audio="ref.wav",
    ref_text="Transcription of the reference audio.",
)

# Without ref_text — Whisper auto-transcribes ref_audio
audio = model.generate(
    text="Hello, this is a test of zero-shot voice cloning.",
    ref_audio="ref.wav",
)

# audio is a list of torch.Tensor, shape (1, T) at 24kHz
torchaudio.save("out.wav", audio[0], 24000)
```

### Voice Design

```python
# Describe speaker via comma-separated attributes
audio = model.generate(
    text="Hello, this is a test of zero-shot voice design.",
    instruct="female, low pitch, british accent",
)
torchaudio.save("out.wav", audio[0], 24000)
```

**Supported attributes:**
- **Gender**: `male`, `female`
- **Age**: `child`, `young`, `middle-aged`, `elderly`
- **Pitch**: `very low pitch`, `low pitch`, `high pitch`, `very high pitch`
- **Style**: `whisper`
- **English accents**: `american accent`, `british accent`, `australian accent`, etc.
- **Chinese dialects**: `四川话`, `陕西话`, etc.

### Auto Voice

```python
audio = model.generate(text="This is a sentence without any voice prompt.")
torchaudio.save("out.wav", audio[0], 24000)
```

### Generation Parameters

```python
audio = model.generate(
    text="Hello world.",
    ref_audio="ref.wav",
    ref_text="Reference text.",
    num_step=32,      # diffusion steps; use 16 for faster (slightly lower quality)
    speed=1.2,        # speaking rate multiplier (>1 faster, <1 slower)
    duration=8.0,     # fix output duration in seconds (overrides speed)
)
```

### Non-Verbal Symbols

```python
# Insert expressive non-verbal sounds inline
audio = model.generate(
    text="[laughter] You really got me. I didn't see that coming at all."
)
```

**Supported tags:**
`[laughter]`, `[sigh]`, `[confirmation-en]`, `[question-en]`, `[question-ah]`,
`[question-oh]`, `[question-ei]`, `[question-yi]`, `[surprise-ah]`, `[surprise-oh]`,
`[surprise-wa]`, `[surprise-yo]`, `[dissatisfaction-hnn]`

### Pronunciation Control

```python
# Chinese: pinyin with tone numbers (inline, uppercase)
audio = model.generate(
    text="这批货物打ZHE2出售后他严重SHE2本了，再也经不起ZHE1腾了。"
)

# English: CMU dict pronunciation in brackets (uppercase)
audio = model.generate(
    text="You could probably still make [IH1 T] look good."
)
```

---

## CLI Tools

### Web Demo

```bash
omnivoice-demo --ip 0.0.0.0 --port 8001
omnivoice-demo --help  # all options
```

### Single Inference

```bash
# Voice Cloning (ref_text optional; omit for Whisper auto-transcription)
omnivoice-infer \
    --model k2-fsa/OmniVoice \
    --text "This is a test for text to speech." \
    --ref_audio ref.wav \
    --ref_text "Transcription of the reference audio." \
    --output hello.wav

# Voice Design
omnivoice-infer \
    --model k2-fsa/OmniVoice \
    --text "This is a test for text to speech." \
    --instruct "male, British accent" \
    --output hello.wav

# Auto Voice
omnivoice-infer \
    --model k2-fsa/OmniVoice \
    --text "This is a test for text to speech." \
    --output hello.wav
```

### Batch Inference (Multi-GPU)

```bash
omnivoice-infer-batch \
    --model k2-fsa/OmniVoice \
    --test_list test.jsonl \
    --res_dir results/
```

**JSONL format** (`test.jsonl`):

```jsonl
{"id": "sample_001", "text": "Hello world", "ref_audio": "/path/to/ref.wav", "ref_text": "Reference transcript"}
{"id": "sample_002", "text": "Voice design example", "instruct": "female, british accent"}
{"id": "sample_003", "text": "Auto voice example"}
{"id": "sample_004", "text": "Speed controlled", "ref_audio": "/path/to/ref.wav", "speed": 1.2}
{"id": "sample_005", "text": "Duration fixed", "ref_audio": "/path/to/ref.wav", "duration": 10.0}
{"id": "sample_006", "text": "With language hint", "ref_audio": "/path/to/ref.wav", "language_id": "en", "language_name": "English"}
```

**JSONL field reference:**
| Field | Required | Description |
|---|---|---|
| `id` | ✅ | Unique identifier |
| `text` | ✅ | Text to synthesize |
| `ref_audio` | ❌ | Path to reference audio (voice cloning) |
| `ref_text` | ❌ | Transcript of ref audio |
| `instruct` | ❌ | Speaker attributes (voice design) |
| `language_id` | ❌ | Language code, e.g. `"en"` |
| `language_name` | ❌ | Language name, e.g. `"English"` |
| `duration` | ❌ | Fixed output duration in seconds |
| `speed` | ❌ | Speaking rate multiplier (ignored if duration set) |

---

## Common Patterns

### Full Voice Cloning Pipeline

```python
from omnivoice import OmniVoice
import torch
import torchaudio
from pathlib import Path

def clone_voice(ref_audio_path: str, texts: list[str], output_dir: str):
    model = OmniVoice.from_pretrained(
        "k2-fsa/OmniVoice",
        device_map="cuda:0",
        dtype=torch.float16
    )
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for i, text in enumerate(texts):
        audio = model.generate(
            text=text,
            ref_audio=ref_audio_path,
            # ref_text omitted: Whisper auto-transcribes
            num_step=32,
            speed=1.0,
        )
        out_path = f"{output_dir}/output_{i:04d}.wav"
        torchaudio.save(out_path, audio[0], 24000)
        print(f"Saved: {out_path}")

clone_voice(
    ref_audio_path="speaker.wav",
    texts=["Hello world.", "Second sentence.", "Third sentence."],
    output_dir="outputs/"
)
```

### Batch Processing from a List

```python
import json
from omnivoice import OmniVoice
import torch
import torchaudio

model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)

items = [
    {"id": "s1", "text": "English sentence.", "instruct": "female, american accent"},
    {"id": "s2", "text": "Another sentence.", "ref_audio": "ref.wav"},
    {"id": "s3", "text": "Auto voice.", },
]

for item in items:
    kwargs = {"text": item["text"]}
    if "ref_audio" in item:
        kwargs["ref_audio"] = item["ref_audio"]
    if "ref_text" in item:
        kwargs["ref_text"] = item["ref_text"]
    if "instruct" in item:
        kwargs["instruct"] = item["instruct"]

    audio = model.generate(**kwargs)
    torchaudio.save(f"{item['id']}.wav", audio[0], 24000)
```

### Voice Design Combinations

```python
designs = [
    "male, elderly, low pitch",
    "female, child, high pitch",
    "male, whisper",
    "female, british accent, high pitch",
    "male, american accent, middle-aged",
]

for design in designs:
    audio = model.generate(
        text="The quick brown fox jumps over the lazy dog.",
        instruct=design,
    )
    safe_name = design.replace(", ", "_").replace(" ", "-")
    torchaudio.save(f"design_{safe_name}.wav", audio[0], 24000)
```

### Fast Inference (Lower Diffusion Steps)

```python
# Default: num_step=32 (high quality)
# Fast: num_step=16 (slightly lower quality, ~2x faster)
audio = model.generate(
    text="Fast inference example.",
    ref_audio="ref.wav",
    num_step=16,
)
```

---

## Output Format

- **Sample rate**: 24,000 Hz
- **Type**: `list[torch.Tensor]`, each tensor shape `(1, T)`
- **Save**: use `torchaudio.save(path, audio[0], 24000)`

---

## Troubleshooting

### HuggingFace download fails
```bash
export HF_ENDPOINT="https://hf-mirror.com"
```

### CUDA out of memory
```python
# Use float16 (not float32)
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
# Or reduce batch size / text length in batch inference
```

### Whisper ASR not available for ref_text auto-transcription
```bash
pip install openai-whisper
```

### Wrong pronunciation in Chinese
Use inline pinyin with tone numbers directly in the text string:
```python
# Format: PINYINTONE_NUMBER within the sentence
text = "这批货物打ZHE2出售"
```

### Audio quality issues
- Increase `num_step` to 32 or 64
- Provide `ref_text` manually instead of relying on auto-transcription
- Use a clean, noise-free reference audio clip (3–15 seconds recommended)

### Apple Silicon (MPS) issues
```python
# Use mps device explicitly
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
```

---

## Model & Resources

| Resource | Link |
|---|---|
| HuggingFace Model | `k2-fsa/OmniVoice` |
| HuggingFace Space | https://huggingface.co/spaces/k2-fsa/OmniVoice |
| Paper (arXiv) | https://arxiv.org/abs/2604.00688 |
| Demo Page | https://zhu-han.github.io/omnivoice |
| Supported Languages | `docs/languages.md` in repo |
| Voice Design Attributes | `docs/voice-design.md` in repo |
| Generation Parameters | `docs/generation-parameters.md` in repo |
| Training/Eval Examples | `examples/` in repo |
