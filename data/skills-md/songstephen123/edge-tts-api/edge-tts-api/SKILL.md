---
name: edge-tts-api
description: "Use this skill whenever you want to deploy a self-hosted TTS API service using Microsoft Edge TTS (completely free, no API key required). Triggers include: 'deploy tts service', 'tts api server', 'self-hosted tts', 'edge tts service', or requests to set up a text-to-speech API for Feishu, DingTalk, or other applications."
---

# edge-tts-api

一个基于微软 Edge TTS 的自托管 API 服务，**完全免费，无需 API Key**，可被飞书、钉钉等应用调用。

## Highlights

- 💰 **完全免费** - 使用 Edge TTS，无需 Azure 账户或 API Key
- 🎙️ **神经网络音质** - 与 Azure TTS 相同的高质量语音
- 🌏 **多语言支持** - 中文、英文、日文等 40+ 语言
- ⚡ **快速响应** - RESTful API 设计
- 🔌 **通用接口** - 可接入任何应用（飞书、钉钉、微信...）
- 🐳 **一键部署** - Docker 支持

## Triggers

- 部署 tts 服务 / tts api / 语音服务
- 飞书机器人 tts / 钉钉语音播报
- edge tts / 免费 tts / 无需 api key
- 自托管 tts / self-hosted tts
- install tts service

## Quick Start

### 安装并启动

```bash
# 通过 npx skills add 安装
npx skills add your-username/edge-tts-api

# 进入目录
cd ~/skills/edge-tts-api

# 一键部署到云服务器
bash scripts/deploy-cloud.sh

# 或本地启动
bash scripts/start.sh
```

### 快速测试

```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，世界"}' \
  --output hello.mp3
```

## Capabilities

### 文本转语音
- 支持多种神经网络音色（中文、英文等多语言）
- 语速、音调、音量可调
- 返回 MP3 格式音频

### 音色选择

**中文音色：**
- `xiaoxiao` - 晓晓（女声，温柔）
- `xiaoyi` - 晓伊（女声，亲和）
- `yunyang` - 云扬（男声，成熟）
- `xiaomeng` - 晓梦（童声）

**英文音色：**
- `aria` - Aria（女声）
- `guy` - Guy（男声）

### 飞书集成

本技能提供完整的飞书集成示例，支持：
- 群聊消息转语音
- @机器人触发
- 自定义音色和语速

## Workflow

1. **安装技能** - `npx skills add your-username/edge-tts-api`
2. **配置环境** - 复制 `.env.example` 到 `.env`（可选）
3. **启动服务** - `bash scripts/start.sh` 或部署到云服务器
4. **调用 API** - 通过 HTTP POST 请求生成语音
5. **集成应用** - 接入飞书、钉钉等应用

## API Endpoints

| 端点 | 方法 | 说明 |
|------|------|------|
| `/tts` | POST | 文本转语音 |
| `/voices` | GET | 获取音色列表 |
| `/voices/popular` | GET | 获取常用音色 |
| `/health` | GET | 健康检查 |

## Requirements

- Python 3.10+
- 服务器：512MB+ 内存
- 已开放端口：8000（或自定义）

## Limitations

- Edge TTS 通过逆向工程实现，未来可能有变化
- 不支持语音克隆（如需克隆可使用 Noiz TTS）
- 建议用于个人和非商业项目

## Cloud Deployment

支持一键部署到：
- 腾讯云
- 火山引擎
- 阿里云
- AWS

详见 `docs/CLOUD_DEPLOYMENT.md` 或 `docs/VOLCENGINE_DEPLOYMENT.md`

## Integration Examples

### 飞书机器人

```python
import requests

TTS_API = "http://YOUR_SERVER_IP:8000/tts"

def send_voice_message(text):
    response = requests.post(TTS_API, json={"text": text})
    audio = response.content
    # 发送到飞书...
```

### cURL

```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"你好","voice":"xiaoxiao"}' \
  --output speech.mp3
```

完整示例见 `examples/` 目录。

## License

MIT License
