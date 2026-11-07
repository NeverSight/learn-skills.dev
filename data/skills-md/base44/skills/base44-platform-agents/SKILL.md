---
name: base44-platform-agents
description: "Base44 in-app AI agents: JSON agent configs under base44/agents/ with entity, backend-function or server-route tools, WhatsApp and Telegram channels, the agents SDK for conversation UIs, and code agents (an agent loop the app runs on the AI gateway). Use when the app needs a conversational assistant or programmable AI."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 agents

An agent is a `.jsonc` file under `base44/agents/`; writing it defines the agent. Build the conversation UI with the agents SDK, or run a code agent on the AI gateway.

## Pick the reference for this app

Determine the app profile first. Call `GET /api/apps/{app_id}/agent-profile` (over the Base44 MCP `execute_api`
tool, or with your Base44 CLI token); it returns the framework, app type, runtime,
entitlements and the exact reference files to read. Without it, detect from the project files:
`src/routes/__root.*` and `src/routeTree.gen.ts` mean TanStack Start; `app/_layout.*` means a
native mobile (Expo) app; otherwise it is a Vite SPA.

| Profile | Read |
|---|---|
| Web app, Vite SPA (the default web template) | [Agents (Vite SPA: tools are backend functions)](references/web-spa.md) |
| Web app, TanStack Start | [Agents (TanStack Start: tools are server routes)](references/web-tanstack.md) |
