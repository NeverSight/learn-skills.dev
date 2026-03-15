---
name: walkie-talkie
description: WhatsApp 语音/文字双模对话：收到语音消息先本地转写（whisper CLI），再正常推理，并同时返回文字+语音。
when: |
  When user asks to enable voice chat / 语音对话 / walkie-talkie / 对讲机模式,
  OR when the incoming message contains an audio/voice-note attachment.
examples:
  - "开启语音对话模式"
  - "进入 walkie-talkie"
  - "我发语音你用语音回"
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      anyBins: ["whisper", "ffmpeg"]
---

# Walkie‑Talkie（语音对讲）模式

目标：用户在 WhatsApp 里**发文字或语音都可以**。
- **文字**：正常回复文字。
- **语音**：先本地转写成文字 → 正常生成回复 → **同时回文字 + 回语音**。

## 触发
- 用户明确说：开启/进入语音对话、walkie-talkie、对讲机模式。
- 或系统/网关把消息标记为 voice note / audio，并提供本地文件路径（常见为 .ogg/.opus/.m4a 等）。

## 执行步骤（语音消息）

### 1) 找到音频文件路径
优先从消息里拿到本地路径（OpenClaw 通常会把媒体下载到本地，并在消息里给出 path/filePath/url）。
- 如果你没拿到路径：请直接问用户“我这条语音没拿到文件路径/附件，麻烦重发一次或发文字”。

### 2) 转成 wav（16k 单声道）
使用 exec：
```bash
ffmpeg -y -i "$IN" -ac 1 -ar 16000 /tmp/oc_voice.wav
```

### 3) 本地转写（whisper CLI）
使用 exec：
```bash
whisper /tmp/oc_voice.wav --model small --language Chinese --task transcribe --output_format txt --output_dir /tmp
cat /tmp/oc_voice.txt
```
- 如果识别语言不确定：先不指定 --language，让 whisper 自动。

### 4) 用转写文本作为用户输入
把转写文本当作用户刚刚发来的内容继续对话。

### 5) 回复：文字 + 语音
- 文字：照常在当前会话回复。
- 语音：调用 `tts` 工具把最终回复转成音频，然后用 `message` 工具发送为语音消息（asVoice=true）。

注意：如果用 message 工具发送语音给用户（用户可见），请遵守主代理规则：工具发送后，本回合最终回复用 NO_REPLY 避免重复。

## 失败策略
- ffmpeg/whisper 报错：回复用户“我这次语音转写失败，请重发或改发文字”，并把关键报错摘要给出（不要贴过长日志）。
- 音频太长：提示用户分段发送。

## 性能建议
- 默认用 whisper small（速度/准确平衡）。
- 追求速度可用 base；追求准确可用 medium（更慢）。
