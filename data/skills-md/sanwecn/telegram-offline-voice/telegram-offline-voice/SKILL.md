---
name: telegram-offline-voice
description: 本地生成 Telegram 语音消息，支持自动清洗、分段与临时文件管理。
metadata: {"openclaw":{"emoji":"🎙️","os":["linux"],"requires":{"bins":["ffmpeg","uv"]}}}
---

# telegram-offline-voice 🎙️

**本地生成，一键封装** — 使用 Microsoft Edge-TTS 生成高质量中文语音，完全离线处理。

## 💡 为什么需要这个升级？

原生的 TTS 方案通常只能生成 MP3 附件，且无法处理 Markdown 标记和超长文本。本项目通过工程化封装，将“语音合成”进化为“语音交互”：

- **告别标记音**：自动识别并清洗 `**`, `#`, `[link]` 等 Markdown 符号，避免 AI 读出这些“代码噪音”。
- **智能对话流**：超长文本不再是一读到底，而是按句号、感叹号自动切分为多个语音气泡，听感更像真人在发语音。
- **并发安全**：针对多代理/子代理并行调用的场景，使用 UUID 隔离临时文件，彻底杜绝文件读写冲突。
- **零token消耗**：完全基于 Edge-TTS 本地生成，无需 OpenAI/Azure 的付费 Token。

## ✨ 特性

- 🔒 **隐私保护**：100% 本地音频处理，不经过任何额外云端 TTS 提供商。
- 💰 **零token消耗**：使用免费的 Edge-TTS 引擎，省下昂贵的 API 额度。
- 🎯 **一键生成**：内置 `voice_gen.py` 脚本，自动完成“文本->MP3->OGG”的全过程。
- 🧹 **自动清洗**：自动剔除 Markdown 符号和 URL 链接，让朗读更自然。
- ✂️ **智能分段**：超长文本自动按标点符号切分为多个语音气泡。
- 🛡️ **安全并发**：使用 UUID 命名临时文件，支持多代理同时调用。

## 🛠️ 安装依赖

```bash
# 需要 Python 环境和 FFmpeg
sudo apt update && sudo apt install ffmpeg python3-pip -y

# 推荐安装 uv 以极速运行封装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 🚀 使用方法 (推荐)

直接调用封装脚本，一键生成 Telegram 原生语音气泡路径：

```bash
uv run {baseDir}/scripts/voice_gen.py --text "您的待播报内容"
```

## ⚙️ 技术细节

### 参数说明
- `--text` / `-t`: 待生成的文本（必填）。
- `--voice`: 声线选择，默认 `zh-CN-XiaoxiaoNeural`（晓晓）。
- `--rate`: 语速调节，默认 `+5%`。
- `--outdir`: 临时文件存放目录，默认 `/tmp`。

### 自动化清洗规则
脚本会自动移除以下内容以确保朗读流畅：
- Markdown 符号：`**`, `*`, `_`, `` ` ``, `#`
- 链接逻辑：`[文本](url)` 以及所有 `http/https` 开头的链接
- 分割线：`---`, `***` 等

---

## 👨💻 关于作者

由 **[@sanwe](https://x.com/sanwe)** 调优并维护。
欢迎关注我的推特获取更多 OpenClaw 进阶玩法：[https://x.com/sanwe](https://x.com/sanwe)
