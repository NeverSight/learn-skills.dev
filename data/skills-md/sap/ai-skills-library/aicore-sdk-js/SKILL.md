---
name: aicore-sdk-js
metadata:
  version: "2.0"
description: >
  Generate working TypeScript/JavaScript boilerplate for SAP GenAI Hub using @sap-ai-sdk/orchestration,
  @sap-ai-sdk/foundation-models, @sap-ai-sdk/openai (native OpenAI SDK), @sap-ai-sdk/langchain (LangChain),
  @sap-ai-sdk/document-grounding (RAG), @sap-ai-sdk/prompt-registry, @sap-ai-sdk/llm-batch (batch jobs),
  @sap-ai-sdk/rpt (tabular prediction), or @sap-ai-sdk/context-registry (data destinations, tabular artifacts,
  scenario configurations).
  WHEN: user asks for TypeScript, JavaScript, Node.js, or JS/TS code that calls a GenAI Hub
  model, wants a TypeScript starter project, asks how to use @sap-ai-sdk in their app, asks
  how to use LangChain (JS/TS) with SAP AI Core, or wants JS/TS for RAG/document-grounding,
  prompt templates, batch LLM jobs, tabular (RPT) prediction, or managing data destinations /
  tabular artifacts / scenario configurations via the Context Registry.
  DO NOT USE FOR: Java code — use `aicore-sdk-java`. 
compatibility: Requires Node.js 22+ with native ESM support, and npm or bun. Context7 MCP is optional (see Sources & Fallback).
---

## Rules

1. If no deployment URL is known, check the SAP AI Core console or contact your admin to list or create one before generating code.
2. Always include `aicore configure` credential guidance in generated code comments; link to [Connecting to AI Core](https://sap.github.io/ai-sdk/docs/js/connecting-to-ai-core) for setup details.
3. JS/TS lifecycle management (create/list/delete deployments) is not available in this skill — use the SAP AI Core console or contact your admin for deployment management.
4. Target `@sap-ai-sdk` **v2** (orchestration `2.14+`). The preferred invocation pattern is passing `messages` directly to `chatCompletion()` / `stream()`. Only use `promptTemplating.prompt.template` with `{{?placeholder}}` values when the user explicitly wants a server-side reusable template. Never emit the v1 shape `llm: { model_name }` / `templating: { template }` — it does not compile against v2.
5. Never emit Python code snippets — this skill is JS/TS only. If the user asks for Python, inform them that no Python skill is available in this repo and point them to https://sap.github.io/ai-sdk/ for Python SDK guidance.
6. Gather these details before generating code — ask only for what the user hasn't provided:
   - **Framework**: `@sap-ai-sdk/*` (recommended) / `@sap-ai-sdk/langchain` (LangChain) / OpenAI npm package via LiteLLM proxy?
   - **Use case**: chat / streaming / embeddings?
   - **Runtime**: Node.js / Bun / browser?
   - **Model + Deployment ID**: check the SAP AI Core console for existing deployments
   - **Model-switching intent** (ask only when the user specifies an OpenAI model like gpt-4o, gpt-4.1, etc.): do they plan to switch models later (e.g. to Claude or Gemini)? If yes → recommend `@sap-ai-sdk/orchestration` for portability. If they want to stay on OpenAI → use `@sap-ai-sdk/openai` (`SapOpenAi.createClient`) as the simpler native OpenAI SDK alternative; no LiteLLM proxy needed.

---

## Sources & Fallback

Use the best source available, in this order. Never block on a source that isn't present.

1. **Baked-in reference (always available).** `references/SDK_JS.md` and `assets/*.ts` are the
   compile-checked v2 floor. They are correct for the common paths (chat, streaming, LangChain,
   embeddings, proxy) and require no network or MCP. Use them by default.
2. **Context7 MCP (use if available).** _If_ the `context7` `query-docs` tool is registered in
   this session, prefer it for the freshest API, version-specific details, or any feature the
   baked-in reference marks as fast-moving (tool calling, data masking, document grounding,
   prompt registry). Library ID: `/websites/sap_github_io_ai-sdk_js`. If the tool is **not**
   available, silently fall back to the baked-in reference — do not ask the user to install it.
3. **Web docs (last resort).** For anything neither source covers, point to
   [llms.txt](https://sap.github.io/ai-sdk/llms.txt) or fetch the online docs.

Do not fabricate API shapes from memory — this SDK's v1 and v2 APIs differ, and guessing
reproduces stale v1 code. When unsure, use source 2 if present, else source 3.

---

## Asset Map

| Use case                                           | Template                            | Install                                                                              |
| -------------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------ |
| Chat via `@sap-ai-sdk/orchestration` (recommended) | `assets/chat_sap_sdk.ts`            | `npm install @sap-ai-sdk/orchestration`                                              |
| Streaming via `@sap-ai-sdk/orchestration`          | `assets/streaming.ts`               | `npm install @sap-ai-sdk/orchestration`                                              |
| Native OpenAI SDK (chat/stream/embeds/Responses)   | `assets/openai_native.ts`           | `npm install @sap-ai-sdk/openai openai zod`                                          |
| LangChain via `AzureOpenAiChatClient`              | `assets/langchain_openai.ts`        | `npm install @sap-ai-sdk/langchain @langchain/core`                                  |
| LangChain via `OrchestrationClient`                | `assets/langchain_orchestration.ts` | `npm install @sap-ai-sdk/langchain @langchain/core`                                  |
| RAG / document grounding                           | `assets/document_grounding.ts`      | `npm install @sap-ai-sdk/document-grounding`                                         |
| Managed prompt templates                           | `assets/prompt_registry.ts`         | `npm install @sap-ai-sdk/prompt-registry`                                            |
| Batch LLM jobs                                     | `assets/llm_batch.ts`               | `npm install @sap-ai-sdk/llm-batch @sap-ai-sdk/ai-api @sap-ai-sdk/foundation-models` |
| Tabular prediction (SAP-RPT-1, not chat)           | `assets/rpt.ts`                     | `npm install @sap-ai-sdk/rpt`                                                        |
| Context Registry (data destinations, tabular artifacts, scenario configs) | `assets/context_registry.ts` | `npm install @sap-ai-sdk/context-registry` |
| Tabular Orchestration (RPT predict via Scenario Config or inline context) | `assets/tabular_orchestration.ts` | `npm install @sap-ai-sdk/tabular-orchestration` |
| Real-time speech/text via WebSocket (`gpt-realtime`)                      | `assets/realtime.ts`              | `npm install @sap-ai-sdk/openai openai ws`      |
| Chat via OpenAI npm package (LiteLLM proxy)        | `assets/chat_openai_proxy.ts`       | `npm install openai`                                                                 |

---

## Install Options

```bash
# @sap-ai-sdk (recommended — native SAP SDK)
npm install @sap-ai-sdk/orchestration @sap-ai-sdk/foundation-models

# Native OpenAI SDK surface on AI Core (no LiteLLM proxy needed)
npm install @sap-ai-sdk/openai openai zod

# LangChain integration (no LiteLLM proxy needed)
npm install @sap-ai-sdk/langchain @langchain/core

# RAG, prompt templates, batch jobs, tabular prediction
npm install @sap-ai-sdk/document-grounding
npm install @sap-ai-sdk/prompt-registry
npm install @sap-ai-sdk/llm-batch @sap-ai-sdk/ai-api @sap-ai-sdk/foundation-models
npm install @sap-ai-sdk/rpt

# With bun
bun add @sap-ai-sdk/orchestration @sap-ai-sdk/foundation-models

# OpenAI npm package via LiteLLM proxy (only if you need a running proxy; prefer @sap-ai-sdk/openai)
npm install openai
```

---

## Quick Start (@sap-ai-sdk/orchestration)

Pass `messages` directly — this is the default pattern. Only use `promptTemplating.prompt.template` with `{{?placeholder}}` values when the user explicitly wants a reusable server-side template.

```typescript
import { OrchestrationClient } from "@sap-ai-sdk/orchestration";

const client = new OrchestrationClient({
  promptTemplating: {
    model: {
      name: "anthropic--claude-4.5-haiku",
      params: { temperature: 0.7 },
    },
  },
});

const response = await client.chatCompletion({
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Hello!" },
  ],
});
console.log(response.getContent());
```

Run with: `npx tsx index.ts` or `bun run index.ts`

---

## Handoffs

- **Want Java code instead?** → invoke `aicore-sdk-java`

---

## When to Load Reference Files

| Trigger                                                     | Load                                                 |
| ----------------------------------------------------------- | ---------------------------------------------------- |
| `@sap-ai-sdk/*` API, OrchestrationClient, streaming         | `references/SDK_JS.md`                               |
| LangChain, `AzureOpenAiChatClient`, `@sap-ai-sdk/langchain` | `references/SDK_JS.md`                               |
| Native OpenAI SDK, `SapOpenAi`, Responses API               | `references/SDK_JS.md`                               |
| RAG, document grounding, prompt registry, batch, RPT        | `references/SDK_JS.md`                               |
| Tool calling, data masking, grounding config internals      | Context7 (if available), else `references/SDK_JS.md` |
