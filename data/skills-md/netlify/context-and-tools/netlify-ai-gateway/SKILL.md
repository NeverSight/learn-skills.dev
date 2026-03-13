---
name: netlify-ai-gateway
description: Guide for using Netlify AI Gateway to access AI models. Use when adding AI capabilities (text generation, image generation, embeddings) to a Netlify project. Covers supported providers (OpenAI, Anthropic, Google), SDK configuration via base URL override, environment variables, and usage from Netlify Functions.
---

# Netlify AI Gateway

Netlify AI Gateway provides access to AI models from multiple providers without managing API keys directly. It is available on all Netlify sites.

## How It Works

The AI Gateway acts as a proxy — you use standard provider SDKs (OpenAI, Anthropic, Google) but point them at Netlify's gateway URL instead of the provider's API. Netlify handles authentication, rate limiting, and monitoring.

## Setup

1. Enable AI on your site in the Netlify UI
2. The environment variable `OPENAI_BASE_URL` is set automatically by Netlify
3. Install the provider SDK you want to use

No provider API keys are needed — Netlify's gateway handles authentication.

## Using OpenAI SDK

```bash
npm install openai
```

```typescript
import OpenAI from "openai";

const openai = new OpenAI();
// OPENAI_BASE_URL is auto-configured — no API key or base URL needed

const completion = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: "Hello!" }],
});
```

## Using Anthropic SDK

```bash
npm install @anthropic-ai/sdk
```

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  baseURL: Netlify.env.get("ANTHROPIC_BASE_URL"),
});

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }],
});
```

## Using Google AI SDK

```bash
npm install @google/generative-ai
```

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("placeholder");
// Configure base URL via environment variable

const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
const result = await model.generateContent("Hello!");
```

## In a Netlify Function

```typescript
import type { Config, Context } from "@netlify/functions";
import OpenAI from "openai";

export default async (req: Request, context: Context) => {
  const { prompt } = await req.json();
  const openai = new OpenAI();

  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: prompt }],
  });

  return Response.json({
    response: completion.choices[0].message.content,
  });
};

export const config: Config = {
  path: "/api/ai",
  method: "POST",
};
```

## Environment Variables

| Variable | Provider | Set by |
|---|---|---|
| `OPENAI_BASE_URL` | OpenAI | Netlify (automatic) |
| `ANTHROPIC_BASE_URL` | Anthropic | Netlify (automatic) |

These are configured automatically when AI is enabled on the site. No manual setup required.

## Local Development

With `@netlify/vite-plugin` or `netlify dev`, gateway environment variables are injected automatically. The AI Gateway is accessible during local development after the site has been deployed at least once.

## Available Models

The gateway supports models from OpenAI, Anthropic, and Google. Use standard model identifiers (e.g., `gpt-4o-mini`, `claude-sonnet-4-5-20250929`, `gemini-2.5-flash`). Available models may change — refer to Netlify's AI Gateway documentation for the current list.
