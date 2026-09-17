---
name: ai-sdk-core-v7
description: Build backend AI with Vercel AI SDK v7 — generateText, streamText, ToolLoopAgent, tools. Use when implementing AI SDK v7 or troubleshooting AI errors. Never write AI SDK from memory.
---

# Skill: ai-sdk-core

## Scope

- Applies to: Backend AI with Vercel AI SDK v7 (`ai` package)
- Does NOT cover: React chat UIs (see [ai-sdk-ui](../ai-sdk-ui-v7/SKILL.md))

## Assumptions

- Folder major tracks the installed `ai` package in `package.json`, not a skill-file revision
- Node.js 22+, ESM; Zod 4 for `inputSchema`
- **Never write AI SDK from memory.** Grep `node_modules/ai/docs/` and `node_modules/ai/src/` for the installed version. Else https://ai-sdk.dev/docs (append `.md`) or https://ai-sdk.dev/api/search-docs?q=
- v6 leftovers: https://ai-sdk.dev/docs/migration-guides/migration-guide-7-0

## Principles

- `generateText` / `streamText` for request handlers and one-shot API routes; `instructions` for system-style prompt
- Request-handler tool loops: `stopWhen: isStepCount(n)` on `generateText` / `streamText` — not `maxSteps`, not `stepCountIs`
- `ToolLoopAgent` + `generate()` / `stream()` for durable agents — not hand-rolled loops, not `new Agent()`
- UI streams: `createUIMessageStreamResponse` + `toUIMessageStream({ stream: result.stream })` from `'ai'`. Use these for new handlers and for dedicated stream/SDK updates
- `result.toUIMessageStreamResponse()` still works in v7 (deprecated). Leave it only when the task is unrelated to streaming or the SDK
- Tool results must be JSON-serializable (no `Date`)
- System prompt lives in `instructions`. Client `messages` must not include `{ role: 'system' }` unless the server fully trusts the payload

## Constraints

### MUST

- Read bundled docs before writing calls
- `convertToModelMessages` when the client sends UI messages
- Reject untrusted `{ role: 'system' }` in `messages`. Do not set `allowSystemInMessages: true` for client-supplied chat

### AVOID

- `toDataStreamResponse` / `pipeDataStreamToResponse`
- `stepCountIs` / `maxSteps` / `result.fullStream` / top-level `system:` (use `isStepCount`, `result.stream`, `instructions`)
- Guessing model IDs

## Interactions

- Complements [ai-sdk-ui](../ai-sdk-ui-v7/SKILL.md), [fastify](../fastify-v5/SKILL.md), [next](../next-v16/SKILL.md)
- Upstream: [vercel/ai use-ai-sdk](https://github.com/vercel/ai/blob/main/skills/use-ai-sdk/SKILL.md)

## Templates

- [generate-text-basic.ts](templates/generate-text-basic.ts)
- [stream-text-chat.ts](templates/stream-text-chat.ts)
- [agent-with-tools.ts](templates/agent-with-tools.ts)

## References

- [Request handlers](references/request-handlers.md) — tools + `isStepCount`, Fastify SSE, system-message reject
