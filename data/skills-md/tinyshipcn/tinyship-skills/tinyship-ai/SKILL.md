---
name: tinyship-ai
description: >-
  Configure AI features in TinyShip: chat (OpenAI, DeepSeek, Qwen), image
  generation (fal.ai, Gemini, Qwen), and video generation. Includes credit
  cost setup. Use when the user asks to "configure AI", "add AI chat",
  "set up image generation", "video generation", "AI provider",
  "add AI feature", or "configure AI credits".
---

# TinyShip AI Integration

Guide for configuring AI capabilities in TinyShip. Built on Vercel AI SDK.

## Available Capabilities

| Capability | Providers | Config File |
|-----------|-----------|-------------|
| **AI Chat** | Qwen, DeepSeek, OpenAI | `config/ai.ts` |
| **Image Generation** | fal.ai, Gemini, Qwen | `config/aiImage.ts` |
| **Video Generation** | Qwen (DashScope), Volcengine | `config/aiVideo.ts` |

Ask the user which capabilities they want to enable.

## AI Chat Setup

### Step 1: Choose Provider

| Provider | Strengths | Cost | API Key Source |
|----------|-----------|------|----------------|
| **Qwen** (recommended) | Chinese/English, cost-effective | Low | [Aliyun DashScope](https://dashscope.aliyun.com/) |
| **DeepSeek** | Strong coding, very cheap | Very Low | [DeepSeek Platform](https://platform.deepseek.com/) |
| **OpenAI** | Best overall performance | High | [OpenAI Platform](https://platform.openai.com/) |

### Step 2: Configure Environment

Add the chosen provider's API key to `.env`:

```bash
# Default provider selection
AI_PROVIDER="qwen"  # or "deepseek" or "openai"

# Qwen
QWEN_API_KEY="sk-xxxxx"
QWEN_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

# DeepSeek
DEEPSEEK_API_KEY="sk-xxxxx"

# OpenAI
OPENAI_API_KEY="sk-xxxxx"
OPENAI_BASE_URL=""  # optional: custom gateway URL
```

### Step 3: Verify

1. Start the dev server
2. Navigate to `/ai`
3. Send a test message
4. Verify streaming response works

## Image Generation Setup

Add the chosen provider's API key to `.env`:

```bash
# fal.ai (recommended, supports many models)
FAL_API_KEY="xxxxx"

# Google Gemini
GOOGLE_GENERATIVE_AI_API_KEY="xxxxx"
GOOGLE_GENERATIVE_AI_BASE_URL=""  # optional: custom gateway

# Qwen (reuses QWEN_API_KEY from chat setup)
```

Configure available models in `config/aiImage.ts`. The config file defines which
models are available and their default parameters.

Verify at `/image-generate`.

## Video Generation Setup

Add the chosen provider's API key to `.env`:

```bash
# Qwen/DashScope (reuses QWEN_API_KEY)
# No additional config needed if Qwen chat is already set up

# Volcengine
VOLCENGINE_ACCESS_KEY_ID="xxxxx"
# VOLCENGINE_BASE_URL="https://ark.cn-beijing.volces.com"  # optional
```

Configure available models in `config/aiVideo.ts`.

Verify at `/video-generate`.

## Credit Costs (Optional)

If you want AI features to consume credits, configure `config/credits.ts`:

```typescript
credits: {
  consumptionMode: 'dynamic',
  dynamicChatCostPerKiloToken: 1,
  modelMultipliers: {
    'qwen-turbo': 1.0,
    'qwen-max': 2.0,
    'deepseek-chat': 0.5,
    'gpt-4': 3.0,
    'default': 1.0
  },
  imageGenerationCost: 5,   // credits per image
  videoGenerationCost: 20,  // credits per video
}
```

Make sure credit purchase plans are set up (use `tinyship-payment` skill).

## Adding a New AI Provider

Read `libs/ai/AGENTS.md` for the full pattern. Summary:

1. Install the SDK: `pnpm add @ai-sdk/new-provider`
2. Update types in `libs/ai/types.ts`
3. Add env key mapping in `libs/ai/config.ts`
4. Implement provider in `libs/ai/providers.ts`
5. Add env vars to `env.example`

## Reference Files in TinyShip Repo

- `config/ai.ts` — chat provider configuration
- `config/aiImage.ts` — image generation configuration
- `config/aiVideo.ts` — video generation configuration
- `config/credits.ts` — credit costs for AI features
- `libs/ai/AGENTS.md` — AI library architecture and provider patterns
- `libs/credits/AGENTS.md` — credit system architecture
- `docs/user-guide/ai/chat.md` — AI chat documentation
- `docs/user-guide/ai/image.md` — image generation documentation
- `docs/user-guide/ai/video.md` — video generation documentation
