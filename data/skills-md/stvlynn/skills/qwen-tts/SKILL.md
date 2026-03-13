---
name: qwen-tts
description: Text-to-speech using Qwen3-TTS CustomVoice MLX model. Supports 9 speakers and multiple emotion/style instructions. Optimized for Apple Silicon. Use when user wants audio speech output.
---

# Qwen TTS Skill

Text-to-speech using [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) CustomVoice model, running locally on Apple Silicon via MLX.

## Overview

- **Model**: `mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-4bit` (4-bit quantized, ~600MB)
- **Runtime**: MLX (Apple Silicon GPU acceleration)
- **Speakers**: 9 built-in voices
- **Output**: WAV audio files
- **Auto-cleanup**: Files older than 24 hours are removed automatically

---

## First-time Deployment

### Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.10+

### 1. Create virtual environment

```bash
cd /path/to/skills/skills/qwen-tts
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

模型从 ModelScope 镜像下载（国内更快）：

```bash
pip install -r scripts/requirements.txt
```

### 3. Pre-download model (optional)

首次运行时会自动下载模型。如需提前下载：

```bash
source venv/bin/activate
export HF_ENDPOINT="https://hf-mirror.com"
python3 -c "from mlx_audio.tts.utils import load_model; load_model('mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-4bit')"
```

### 4. Verify

```bash
source venv/bin/activate
python3 scripts/tts.py "你好，这是一段测试语音。" --output /tmp
# Should produce a WAV file in /tmp/
```

### Troubleshooting

| 问题 | 解决方法 |
|------|----------|
| `ModuleNotFoundError: mlx` | 确认使用 Apple Silicon Mac，MLX 不支持 Intel Mac |
| 模型下载缓慢 | 设置 `export HF_ENDPOINT="https://hf-mirror.com"` |
| 内存不足 | 4-bit 模型约需 1.5GB 内存，关闭其他大型应用 |
| 无声音输出 | 检查输出文件是否为 0 字节，可能是文本过短 |

---

## Configuration

> ⚠️ 以下为示例默认值。请根据实际使用场景修改 speaker 和 instruct。

- **Speaker**: `Serena`（示例）
- **Instruct**: `撒娇语气`（示例）
- **Language**: `Chinese`
- **Speed**: `1.0`

## Available Speakers

| Speaker | Language |
|---------|----------|
| `Serena` | Chinese |
| `Vivian` | Chinese |
| `Uncle_Fu` | Chinese |
| `Eric` | Chinese |
| `Dylan` | Chinese |
| `Ryan` | English |
| `Aiden` | English |
| `Ono_Anna` | Japanese |
| `Sohee` | Korean |

## Available Instructs (emotion/style)

- `撒娇语气` — coquettish
- `冷静分析` — calm analysis
- `惊讶` — surprised
- `兴奋` — excited
- `神秘` — mysterious
- `开心` — happy
- `委屈` — wronged/sad

Also supports free-form natural language instructions, e.g. `用特别愤怒的语气说`.

## Usage

```bash
# Default settings
python3 scripts/tts.py "你好！"

# Custom speaker
python3 scripts/tts.py "Hello!" --speaker Ryan --language English

# Custom emotion
python3 scripts/tts.py "其实我真的有发现..." --instruct 冷静分析

# Full customization
python3 scripts/tts.py "哥哥，你回来啦！" \
  --speaker Serena \
  --instruct 撒娇语气 \
  --speed 1.0

# Custom output directory
python3 scripts/tts.py "测试" --output /tmp

# Skip auto-cleanup of old files
python3 scripts/tts.py "测试" --no-cleanup
```

## Audio Output

- **Default directory**: `~/tts-output/` (override with `$QWEN_TTS_OUTPUT_DIR`)
- **File naming**: `tts_{timestamp}_{index}.wav`
- **Auto-cleanup**: Files older than 24 hours removed on each run (disable with `--no-cleanup`)

## Integration

1. Generate audio using the TTS script
2. Send the audio file as a voice message (Telegram, etc.)
3. Old files are cleaned up automatically
