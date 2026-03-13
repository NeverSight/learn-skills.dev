---
name: ai-api-integrations
description: "Connect applications, scripts, and backend services to AI model APIs (OpenAI, Anthropic Claude, Google Gemini/Vertex AI, xAI Grok), Supabase (PostgreSQL database with vector search), and Clerk (authentication). Use when building AI-powered features that require (1) AI model integration for text generation, translation, embeddings, or image generation, (2) Supabase database operations with pgvector semantic search, (3) Clerk user authentication and session management, (4) Combining AI outputs with database storage, (5) Cost-optimized model selection and prompt engineering, (6) Best practices for production deployments avoiding common anti-patterns."
---

# AI API Integrations

> **Last Updated**: January 2026

Build production-ready AI applications with OpenAI, Anthropic, Google, xAI, Supabase, and Clerk.

## Model Selection Policy

### ALWAYS Default to Newest Models

**When implementing AI features, ALWAYS use the latest generation models by default:**

| Provider | Default Model | DO NOT Default To |
|----------|---------------|-------------------|
| **Anthropic** | Claude Sonnet 4.5 or Opus 4.5 | ~~Haiku 3~~, ~~Sonnet 3.5~~ |
| **OpenAI** | GPT-5.2 or GPT-5.2 Instant | ~~GPT-4o-mini~~, ~~GPT-4o~~ |
| **Google** | Gemini 3 Flash or Gemini 3 Pro | ~~Gemini 2.0 Flash-Lite~~, ~~Gemini 1.5~~ |
| **xAI** | Grok 4.1 | ~~Grok 3~~, ~~Grok 2~~ |

### Required: Explain Model Choice to User

**Every time you select a model, you MUST explain your choice to the user:**

```
Model Selection: Using GPT-5.2 ($1.75/$14.00 per 1M tokens)
Reason: Latest OpenAI flagship with 400K context window, ideal for [task description].
Alternative: If cost is a concern, we could use Grok 4.1 ($0.20/$0.50) which is #1 on LMArena.
```

### Legacy Models: User Must Explicitly Request

Older/budget models should ONLY be used when:
1. **User explicitly requests** a specific older model
2. **User specifies budget constraints** and approves the downgrade
3. **High-volume batch processing** where user has approved cost optimization

**Legacy models (do not use by default):**
- Haiku 3 ($0.25/$1.25) - Use Haiku 4.5 instead
- GPT-4o-mini ($0.15/$0.60) - Use GPT-5.2 Instant instead
- Gemini 2.0 Flash-Lite ($0.075/$0.30) - Use Gemini 3 Flash instead
- Any model from 2024 or earlier

### Model Selection Template

When implementing, always communicate:
```markdown
**Model Choice:** [Model Name]
**Cost:** $X.XX input / $X.XX output per 1M tokens
**Why this model:** [Specific reason for this task]
**Alternatives:** [Lower cost option] if budget is a priority, [higher capability option] for more complex needs
```

## Pricing Matrix (January 2026)

### Quick Reference: Cost per 1M Tokens

| Provider | Model | Input | Output | Best For |
|----------|-------|-------|--------|----------|
| **xAI** | Grok 4.1 | **$0.20** | **$0.50** | Best value, #1 LMArena |
| **xAI** | Grok 4.1 Fast | $0.20 | $0.50 | Fast, no thinking |
| **Google** | Gemini 2.0 Flash-Lite | $0.075 | $0.30 | Absolute lowest cost |
| **Google** | Gemini 3 Flash | $0.50 | $3.00 | Fast frontier-class |
| **OpenAI** | GPT-4o-mini | $0.15 | $0.60 | Reliable workhorse |
| **OpenAI** | GPT-5.2 | $1.75 | $14.00 | 400K context, flagship |
| **Anthropic** | Haiku 3 | $0.25 | $1.25 | Budget Claude |
| **Anthropic** | Sonnet 4.5 | $3.00 | $15.00 | Balanced quality/cost |
| **Anthropic** | Opus 4.5 | $5.00 | $25.00 | Highest intelligence |
| **Google** | Gemini 3 Pro | $2.00 | $12.00 | State-of-the-art |

### Cost Optimization Discounts

| Feature | Savings | Available On |
|---------|---------|--------------|
| Prompt Caching | **90%** | Anthropic, OpenAI, Google, xAI |
| Batch Processing | **50%** | Anthropic, OpenAI, Google |
| Free Tier | 100% | Google (1K req/day), OpenAI (limited) |

### Pricing Resources (Bookmark These)

| Provider | Official Pricing Page |
|----------|----------------------|
| Anthropic | [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| OpenAI | [platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing) |
| Google | [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| xAI | [docs.x.ai/docs/models](https://docs.x.ai/docs/models) |

## Quick Start

### 1. Environment Setup

Create `.env.local`:

```bash
# AI Providers (choose one or more)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
GOOGLE_AI_API_KEY=...  # For Google AI SDK
GOOGLE_CLOUD_PROJECT=...  # For Vertex AI
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Supabase
SUPABASE_PROJECT_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...  # Backend only

# Clerk
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
```

### 2. Install Dependencies

```bash
# AI providers
npm install openai @anthropic-ai/sdk @google/generative-ai @google-cloud/vertexai

# Claude Agent SDK (for building agents)
npm install @anthropic-ai/claude-agent-sdk

# Supabase
npm install @supabase/supabase-js

# Clerk
npm install @clerk/backend @clerk/nextjs

# Utilities
npm install zod dotenv
```

### 3. Basic Example: AI with Database Storage

```typescript
import OpenAI from "openai";
import { createClient } from "@supabase/supabase-js";
import { verifyToken } from "@clerk/backend";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const supabase = createClient(
  process.env.SUPABASE_PROJECT_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(req: Request) {
  // 1. Authenticate with Clerk
  const token = req.headers.get("Authorization")?.replace("Bearer ", "");
  const { userId } = await verifyToken(token!, {
    secretKey: process.env.CLERK_SECRET_KEY,
  });

  // 2. Parse request
  const { text, targetLanguage } = await req.json();

  // 3. Call AI
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",  // $0.15/$0.60 per 1M tokens
    messages: [
      { role: "system", content: "You are a professional translator." },
      { role: "user", content: `Translate to ${targetLanguage}: ${text}` },
    ],
    temperature: 0.3,
    max_tokens: 1000,
  });

  // 4. Store in Supabase
  const { data } = await supabase.from("translations").insert({
    user_id: userId,
    source_text: text,
    translated_text: completion.choices[0].message.content,
    tokens_used: completion.usage.total_tokens,
  }).select().single();

  return Response.json({ translation: data.translated_text, id: data.id });
}
```

## Reference Documentation

### AI Provider APIs

| Provider | Reference | Key Features |
|----------|-----------|--------------|
| **[Anthropic Claude](references/anthropic-api.md)** | Claude Opus/Sonnet/Haiku | Prompt caching (90% savings), batch processing (50% savings), 1M context beta |
| **[Claude Agent SDK](references/claude-agent-sdk.md)** | Build AI agents | Multi-turn sessions, tools, hooks, subagents, MCP integration |
| **[OpenAI](references/openai-api.md)** | GPT-5.2, GPT-4o | 400K context, structured outputs, vision, embeddings, Whisper |
| **[Google AI](references/google-ai.md)** | Gemini 3 Flash/Pro | 2M context, free tier, video understanding, Imagen images |
| **[xAI Grok](references/xai-grok.md)** | Grok 4.1 | Best value ($0.20/$0.50), 2M context, web/X search, voice API |

### Platform Services

| Service | Reference | Key Features |
|---------|-----------|--------------|
| **[Supabase](references/supabase.md)** | Database, auth, storage | pgvector search, RLS, realtime subscriptions |
| **[Clerk](references/clerk.md)** | Authentication | User management, organizations, JWT tokens |

### Guides

| Guide | Description |
|-------|-------------|
| **[Best Practices](references/best-practices.md)** | Prompt engineering, cost optimization, database patterns |
| **[Anti-Patterns](references/antipatterns.md)** | Common mistakes to avoid |

## Claude Agent SDK

Build production AI agents with the same tools that power Claude Code.

### Quick Example

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Simple query
for await (const message of query({
  prompt: "Find all TODO comments in the codebase and create a summary",
  options: {
    allowedTools: ["Read", "Glob", "Grep"],
    model: "sonnet"  // claude-sonnet-4-5
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

### Multi-Turn Sessions (V2 API)

```typescript
import { unstable_v2_createSession } from "@anthropic-ai/claude-agent-sdk";

await using session = unstable_v2_createSession({
  model: "claude-sonnet-4-5-20250929"
});

// Turn 1
await session.send("Read the authentication module");
for await (const msg of session.stream()) {
  if (msg.type === "assistant") console.log(msg.message.content);
}

// Turn 2 - maintains context
await session.send("Now find security issues");
for await (const msg of session.stream()) {
  if ("result" in msg) console.log(msg.result);
}
```

### Built-in Tools

| Tool | Description |
|------|-------------|
| Read, Write, Edit | File operations |
| Glob, Grep | Search files and content |
| Bash | Run commands |
| WebSearch, WebFetch | Web access |
| AskUserQuestion | User interaction |
| Task | Spawn subagents |

**See [Claude Agent SDK Reference](references/claude-agent-sdk.md)** for complete documentation.

## Model Selection Guide

### Default Models by Use Case (Use These First)

| Use Case | Default Model | Cost | Why |
|----------|---------------|------|-----|
| General tasks | **Grok 4.1** | $0.20/$0.50 | Best value, #1 LMArena, newest |
| Complex reasoning | **Claude Opus 4.5** | $5/$25 | Highest intelligence |
| Code generation | **GPT-5.2-Codex** | varies | Purpose-built for code |
| Long documents | **Gemini 3 Flash** | $0.50/$3 | 2M context, newest Google |
| Real-time info | **Grok 4.1 + tools** | $0.20/$0.50 + tools | Built-in web/X search |
| Image generation | **Imagen 3 Fast** | $0.02/image | High quality, fast |
| Embeddings | **text-embedding-3-large** | $0.13/1M | Best quality embeddings |
| Fast responses | **GPT-5.2 Instant** | ~$0.60/$2.40 | Fast, newest OpenAI |

### Legacy Models (Only If User Requests)

| Use Case | Legacy Option | Cost | When to Use |
|----------|---------------|------|-------------|
| Budget/high-volume | Gemini 2.0 Flash-Lite | $0.075/$0.30 | User explicitly approves |
| Budget Claude | Haiku 3 | $0.25/$1.25 | User explicitly requests |
| Budget OpenAI | GPT-4o-mini | $0.15/$0.60 | User explicitly requests |

### Provider Comparison (Newest Models)

```
                    COST                 CAPABILITY
Lowest ←────────────────────────────────────────→ Highest

   Grok 4.1    │ Gemini 3 Flash │  GPT-5.2  │ Gemini 3 Pro │ Opus 4.5
  $0.20/$0.50  │   $0.50/$3.00  │ $1.75/$14 │  $2.00/$12   │  $5/$25
```

## Cost Optimization Strategies

### 1. Prompt Caching (90% Savings)

```typescript
// Anthropic
const message = await anthropic.messages.create({
  model: "claude-sonnet-4-5-20241022",
  system: [{
    type: "text",
    text: largeContext,
    cache_control: { type: "ephemeral" }  // Cache for 5 min
  }],
  messages: [{ role: "user", content: question }],
});
// First request: normal price
// Subsequent requests: 90% off cached portion
```

### 2. Batch Processing (50% Savings)

```typescript
// Non-urgent tasks processed within 24 hours
const batch = await anthropic.batches.create({
  requests: items.map(item => ({
    custom_id: item.id,
    params: { model: "claude-sonnet-4-5-20241022", messages: [...] }
  }))
});
// 50% discount on all tokens
```

### 3. Model Tiering

```typescript
async function processWithTier(text: string, tier: "budget" | "standard" | "premium") {
  const models = {
    budget: { provider: "xai", model: "grok-4.1" },           // $0.20/$0.50
    standard: { provider: "openai", model: "gpt-4o-mini" },   // $0.15/$0.60
    premium: { provider: "anthropic", model: "claude-opus-4-5" }  // $5/$25
  };
  return await callModel(text, models[tier]);
}
```

## Core Patterns

### Centralized Configuration

```typescript
// config/ai-models.ts
export const AI_MODELS = {
  translation: "gpt-4o-mini",
  embedding: "text-embedding-3-small",
  complex: "claude-opus-4-5",
} as const;

export const PRICING = {
  "gpt-4o-mini": { input: 0.15, output: 0.60 },
  "grok-4.1": { input: 0.20, output: 0.50 },
  "claude-sonnet-4-5": { input: 3.00, output: 15.00 },
} as const;

export function calculateCost(model: string, inputTokens: number, outputTokens: number): number {
  const prices = PRICING[model] || PRICING["gpt-4o-mini"];
  return ((inputTokens * prices.input) + (outputTokens * prices.output)) / 1_000_000;
}
```

### Structured Outputs (Zod)

```typescript
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod";

const AnalysisSchema = z.object({
  summary: z.string(),
  issues: z.array(z.object({
    severity: z.enum(["high", "medium", "low"]),
    description: z.string(),
  })),
  recommendations: z.array(z.string()),
});

const completion = await openai.beta.chat.completions.parse({
  model: "gpt-5.2",
  messages: [...],
  response_format: zodResponseFormat(AnalysisSchema, "analysis"),
});

const result = completion.choices[0].message.parsed;
// TypeScript knows: result.summary, result.issues, result.recommendations
```

### Vector Search Pattern

```typescript
// 1. Generate embedding
const embedding = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: searchQuery,
});

// 2. Search with Supabase pgvector
const { data } = await supabase.rpc("match_documents", {
  query_embedding: embedding.data[0].embedding,
  match_threshold: 0.5,
  match_count: 10,
});

// 3. Use results in AI prompt
const context = data.map(d => d.content).join("\n");
const completion = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [
    { role: "system", content: `Context:\n${context}` },
    { role: "user", content: userQuestion },
  ],
});
```

## Security Best Practices

1. **Never expose API keys to frontend** - Use backend API routes
2. **Enable Row Level Security (RLS)** in Supabase
3. **Validate all inputs** with Zod schemas
4. **Use private metadata** in Clerk for sensitive data
5. **Implement rate limiting** on public endpoints
6. **Set max_tokens** on all AI calls to prevent runaway costs

## Common Anti-Patterns

See [Anti-Patterns Reference](references/antipatterns.md) for details.

| Anti-Pattern | Fix |
|--------------|-----|
| **Defaulting to legacy models** | Use newest models (GPT-5.2, Grok 4.1, Gemini 3, Sonnet 4.5) |
| **Not explaining model choice** | Always tell user which model, cost, and why |
| **Using old models without asking** | Only use Haiku 3, GPT-4o-mini, Gemini 2.0 if user explicitly requests |
| Hardcoding model names | Centralize in config file |
| No cost tracking | Log all API calls with token counts |
| Missing max_tokens | Always set limits |
| No retry logic | Implement exponential backoff |
| Not using structured outputs | Use Zod + response_format |
| Exposing API keys | Backend-only API calls |

## When to Use This Skill

- Integrate AI model APIs (text, translation, embeddings, images)
- Build semantic search with pgvector
- Implement authentication with Clerk
- Combine AI outputs with database storage
- Optimize costs across multiple AI providers
- Build production-ready AI agents

## Updating This Skill

### To Update Pricing

1. Check official pricing pages (linked above)
2. Update `references/*.md` files with new model names and prices
3. Update the Pricing Matrix table in this file
4. Update `PRICING` constant in config examples

### Last Verified

- Anthropic: January 2026
- OpenAI: January 2026 (GPT-5.2 released Dec 2025)
- Google: January 2026 (Gemini 3 Flash released Dec 2025)
- xAI: January 2026 (Grok 4.1 released Nov 2025)
