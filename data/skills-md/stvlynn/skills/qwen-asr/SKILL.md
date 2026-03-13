---
name: qwen-asr
description: Speech-to-text using Qwen3-ASR-0.6B-4bit MLX model via a local FastAPI service. Transcribes audio files and URLs. Optimized for Apple Silicon. Use when user sends voice messages or audio that needs transcription.
---

# Qwen ASR Skill

Speech-to-text using [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) model, running locally on Apple Silicon via a FastAPI service.

## Overview

- **Model**: `mlx-community/Qwen3-ASR-0.6B-4bit` (4-bit quantized, ~400MB)
- **Runtime**: MLX (Apple Silicon GPU acceleration via MPS)
- **Service**: FastAPI on `http://localhost:8100`
- **Languages**: Chinese, English, Japanese, Korean, and more

---

## First-time Deployment

### Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.10+
- Docker is **not** required (runs natively)

### 1. Create virtual environment

```bash
cd /path/to/skills/skills/qwen-asr
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

模型从 ModelScope/HuggingFace 镜像下载（国内更快）：

```bash
pip install -r service/requirements.txt
```

### 3. Start the service

```bash
bash service/start.sh
```

首次启动时会自动从 hf-mirror.com 下载模型（约 400MB），后续启动使用本地缓存。

### 4. Verify

```bash
# 检查服务健康状态
curl http://localhost:8100/health

# 查看模型信息
curl http://localhost:8100/info

# 测试转录（使用在线音频）
curl -X POST "http://localhost:8100/transcribe_url?audio_url=https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav"
```

### 5. (Optional) 设为系统服务

macOS 上可以使用 launchd 设置开机自启：

```bash
# 创建 plist（自行修改路径）
cat > ~/Library/LaunchAgents/com.qwen.asr.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.qwen.asr</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd /path/to/skills/skills/qwen-asr && bash service/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/qwen-asr.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/qwen-asr.err</string>
</dict>
</plist>
PLIST

launchctl load ~/Library/LaunchAgents/com.qwen.asr.plist
```

### Troubleshooting

| 问题 | 解决方法 |
|------|----------|
| 端口 8100 被占用 | `lsof -i :8100` 找到占用进程，或修改 `start.sh` 中端口号 |
| 模型下载缓慢 | 脚本已自动设置 `HF_ENDPOINT=https://hf-mirror.com` |
| 503 Model not loaded | 模型仍在加载中，首次约需 10-30 秒 |
| `ModuleNotFoundError: mlx` | 确认使用 Apple Silicon Mac |
| 转录结果为空 | 检查音频格式（支持 wav/mp3/ogg/flac），或音频可能太短 |

---

## Service Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/info` | GET | Model information |
| `/transcribe` | POST | Transcribe uploaded audio file |
| `/transcribe_url` | POST | Transcribe audio from URL |

## Usage

### CLI Client

```bash
# Transcribe local file
python3 scripts/asr.py audio.wav

# Transcribe from URL
python3 scripts/asr.py --url "https://example.com/audio.wav"

# Specify language
python3 scripts/asr.py audio.wav --lang zh

# Check service status
python3 scripts/asr.py --check
```

### curl

```bash
# Upload file
curl -X POST "http://localhost:8100/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav"

# From URL with language
curl -X POST "http://localhost:8100/transcribe_url?audio_url=<URL>&language=zh"
```

### Python

```python
import requests

# From URL
response = requests.post(
    "http://localhost:8100/transcribe_url",
    params={"audio_url": "https://example.com/audio.wav", "language": "zh"}
)
text = response.json()["text"]

# From file
with open("audio.wav", "rb") as f:
    response = requests.post("http://localhost:8100/transcribe", files={"file": f})
text = response.json()["text"]
```

## Output Format

```json
{
  "text": "transcribed text here",
  "chunks": [],
  "processing_time": 0.123
}
```

## Service Management

```bash
# Start
bash service/start.sh

# Check status
python3 scripts/asr.py --check

# Stop (find and kill process)
lsof -ti :8100 | xargs kill
```
