---
name: openrouter
description: >
  Complete OpenRouter API documentation reference. Use when working with OpenRouter — an AI model
  routing platform that provides a unified API for accessing 300+ LLMs (OpenAI, Anthropic, Google,
  Meta, Mistral, etc.). Triggers: OpenRouter API integration, model routing, provider selection,
  multi-model fallbacks, OpenRouter SDK (TypeScript/Python), OpenRouter chat completions,
  OpenRouter embeddings, OpenRouter structured outputs, OpenRouter tool calling, OpenRouter
  streaming, BYOK (Bring Your Own Key), OpenRouter OAuth, OpenRouter guardrails, prompt caching
  via OpenRouter, OpenRouter billing/credits, model variants (:free, :extended, :nitro, :thinking,
  :online), Broadcast observability integrations, Zero Data Retention, or any task involving
  openrouter.ai API endpoints.
---

# OpenRouter Documentation

Complete reference for the OpenRouter API platform. All documentation is stored in `references/`.

## Quick Navigation

Consult `references/INDEX.md` for the full table of contents with descriptions of every page.

## When to Read Which Files

- **Getting started**: Read `references/quickstart.md`
- **API basics (endpoints, auth, params, errors)**: Read files in `references/api/reference/`
- **Chat completions**: Read `references/api/api-reference/chat/send-chat-completion-request.md`
- **Streaming**: Read `references/api/reference/streaming.md`
- **Model selection & routing**: Read files in `references/guides/routing/`
- **Model variants (:free, :nitro, etc.)**: Read files in `references/guides/routing/model-variants/`
- **Tool calling / function calling**: Read `references/guides/features/tool-calling.md`
- **Structured outputs (JSON schema)**: Read `references/guides/features/structured-outputs.md`
- **Embeddings**: Read `references/api/reference/embeddings.md`
- **Authentication & OAuth**: Read files in `references/guides/overview/auth/`
- **SDK usage (TypeScript)**: Read files in `references/sdks/typescript/`
- **SDK usage (Python)**: Read files in `references/sdks/python/`
- **Framework integrations (Vercel AI, LangChain, etc.)**: Read files in `references/guides/community/`
- **Observability (Langfuse, Datadog, etc.)**: Read files in `references/guides/features/broadcast/`
- **Multimodal (images, audio, video, PDF)**: Read files in `references/guides/overview/multimodal/`
- **Guardrails & spending controls**: Read `references/guides/features/guardrails.md`
- **Pricing & credits**: Read `references/api/api-reference/credits/`
- **Error handling**: Read `references/api/reference/errors-and-debugging.md`
- **Rate limits**: Read `references/api/reference/limits.md`
- **Best practices (latency, caching, uptime)**: Read files in `references/guides/best-practices/`
- **Enterprise setup**: Read `references/enterprise-quickstart.md`
- **Responses API (beta)**: Read files in `references/api/reference/responses/`

## Key Concepts

- **Base URL**: `https://openrouter.ai/api/v1` (OpenAI-compatible)
- **Auth header**: `Authorization: Bearer <OPENROUTER_API_KEY>`
- **Model format**: `provider/model-name` (e.g. `openai/gpt-4o`, `anthropic/claude-sonnet-4-5`)
- **Variants**: Append `:free`, `:extended`, `:nitro`, `:thinking`, `:online` to model IDs
- **Fallbacks**: Pass array of models to `models` field for automatic fallback
- **Provider routing**: Use `provider.order`, `provider.only`, `provider.ignore` for control
