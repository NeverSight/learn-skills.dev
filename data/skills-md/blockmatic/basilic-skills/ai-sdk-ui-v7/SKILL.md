---
name: ai-sdk-ui-v7
description: Build React chat UIs with Vercel AI SDK v7 — useChat, DefaultChatTransport, status, sendMessage. Use when implementing AI SDK v7 chat UIs or troubleshooting useChat stream parse / no response / stale values. Never write useChat from memory.
---

# Skill: ai-sdk-ui

## Scope

- Applies to: `@ai-sdk/react` `useChat` and `DefaultChatTransport` from `ai`
- Does NOT cover: Backend generation (see [ai-sdk-core](../ai-sdk-core-v7/SKILL.md))

## Assumptions

- SDK major is `ai` ^7; `@ai-sdk/react` is a separate package major. Folder follows `ai`
- **Never write `useChat` from memory.** Grep `node_modules/@ai-sdk/react/docs/` and `node_modules/ai/docs/`, else https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
- Chat HTTP may be Fastify; pass `transport` when the URL is not `/api/chat`

## Principles

- `useChat` from `@ai-sdk/react`; `DefaultChatTransport` from `ai`
- Local input state; `sendMessage({ text })`; `status` not `isLoading`; render `message.parts`
- Server: see [ai-sdk-core](../ai-sdk-core-v7/SKILL.md). Handlers use `createUIMessageStreamResponse` + `toUIMessageStream({ stream: result.stream })`. Leave deprecated `toUIMessageStreamResponse()` only when the task is unrelated to streaming or the SDK

## Constraints

### MUST

- `DefaultChatTransport({ api })` when the endpoint is not `/api/chat`
- Disable send while `status !== 'ready'`

### AVOID

- `import { useChat } from 'ai/react'`
- `toDataStreamResponse` / `pipeDataStreamToResponse`
- Pre-v5 `handleInputChange` / `handleSubmit` / `useAssistant`

## Interactions

- Uses [ai-sdk-core](../ai-sdk-core-v7/SKILL.md)
- Complements [fastify](../fastify-v5/SKILL.md), [next](../next-v16/SKILL.md)

## Templates

- [use-chat-basic.tsx](templates/use-chat-basic.tsx)
- [nextjs-api-route.ts](templates/nextjs-api-route.ts)
- [nextjs-chat-app-router.tsx](templates/nextjs-chat-app-router.tsx)
