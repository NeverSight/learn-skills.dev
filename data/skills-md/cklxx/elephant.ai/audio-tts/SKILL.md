---
name: audio-tts
description: 本地 TTS 语音生成（macOS say + afconvert），输出 m4a 文件。
triggers:
  intent_patterns:
    - "语音|读出来|朗读|TTS|配音|发个语音"
  context_signals:
    keywords: ["语音", "朗读", "tts", "配音", "音频"]
  confidence_threshold: 0.6
priority: 6
requires_tools: [bash, write]
max_tokens: 200
cooldown: 30
output:
  format: markdown
  artifacts: true
  artifact_type: audio
---

# audio-tts

使用 macOS 自带 `say` 生成语音，并转成 m4a。

## Requirements
- macOS（内置 `say`）
- `afconvert`（macOS 自带）

## Usage

```bash
python3 skills/audio-tts/run.py speak --text '你好，这是语音测试'
```

## Parameters

### speak
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 朗读文本 |
| voice | string | 否 | voice 名称（如 Ting-Ting / Samantha），默认空（系统默认） |
| rate | int | 否 | 语速 WPM（say 的 -r 参数） |
| output | string | 否 | 输出路径（默认 /tmp/tts_<ts>.m4a） |
```
