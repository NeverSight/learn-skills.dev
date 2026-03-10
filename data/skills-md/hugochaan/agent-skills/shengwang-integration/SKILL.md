---
name: shengwang-integration
description: |
  Integrate Shengwang (Agora) products: ConvoAI voice agents, RTC audio/video,
  RTM messaging, Cloud Recording, and token generation. Use when the user
  mentions Shengwang, Agora, 声网, ConvoAI, RTC, RTM, voice agent, AI agent,
  video call, live streaming, recording, token, or any Agora product task.
license: MIT
metadata:
  author: shengwang
  version: "1.0.0"
---

# Shengwang Integration

## Routing Rules

### Step 1: Check if intake can be skipped

Skip [intake](intake/README.md) and route directly ONLY when ALL of these are true:
- User names a specific operation (e.g. "stop agent xxx", "generate a token", "download SDK")
- User provides enough technical details to act immediately (channel name, agent ID, language, etc.)
- The request maps unambiguously to exactly one module in the table below

Examples that SKIP intake:
- "帮我停掉 agent_abc123" → [conversational-ai](references/conversational-ai/README.md)
- "生成一个 RTC token，Go 语言" → [token-server](references/token-server/README.md)
- "error 403 是什么意思" → [conversational-ai/troubleshooting](references/conversational-ai/common-errors.md)
- "下载 ConvoAI Go SDK" → route to the relevant product module (each has Demo Projects / download links)

Examples that MUST go through intake:
- "我想做一个 AI 客服" → needs analysis, go to intake
- "帮我接入 ConvoAI" → product identified but details missing, go to intake
- "我想做视频通话 + AI 助手" → multi-product, go to intake
- "voice bot" / "AI agent" → vague, go to intake

### Step 2: Route

| User intent | Route to |
|-------------|----------|
| New request, vague, or missing details | [intake](intake/README.md) |
| Credentials, AppID, REST auth | [general](references/general/credentials-and-auth.md) |
| Download SDK, sample project, Token Builder, GitHub repo | Route to the relevant product module |
| Generate Token, token server, AccessToken2, RTC/RTM auth | [token-server](references/token-server/README.md) |
| ConvoAI operation (with details already known) | [conversational-ai](references/conversational-ai/README.md) |
| RTC SDK integration | [rtc](references/rtc/README.md) |
| RTM messaging / signaling | [rtm](references/rtm/README.md) |
| Cloud Recording | [cloud-recording](references/cloud-recording/README.md) |

## Download Rules

- Use `git clone --depth 1 <url>` — GitHub URLs must be repo root only (no branch/subdirectory paths)
- On any download failure: report the error, provide the URL for manual download, never silently skip

## Links

- Console: https://console.shengwang.cn/
- Docs (CN): https://doc.shengwang.cn/
- GitHub: https://github.com/AgoraIO-Community
