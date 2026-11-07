---
name: base44-platform-backend-functions
description: "Base44 server-side code: backend functions (HTTP handlers in base44/functions/<name>/entry.ts on Cloudflare Workers) for Vite SPA apps, or TanStack Start server functions and server routes. Secrets, the Base44 SDK on the server, auth and service role, webhooks, admin-only handlers, frontend invocation, testing, and the InvokeLLM model table. Use when the app needs external APIs, privileged logic or scheduled work."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 backend functions

A Vite SPA app runs server code as backend functions; a TanStack Start app runs it as server functions and server routes inside its own project. Writing the file deploys it.

> **Requires the Builder plan or above.** The workspace's entitlement is reported by the agent-profile endpoint; on a lower plan the platform rejects the deploy.

## Pick the reference for this app

Determine the app profile first. Call `GET /api/apps/{app_id}/agent-profile` (over the Base44 MCP `execute_api`
tool, or with your Base44 CLI token); it returns the framework, app type, runtime,
entitlements and the exact reference files to read. Without it, detect from the project files:
`src/routes/__root.*` and `src/routeTree.gen.ts` mean TanStack Start; `app/_layout.*` means a
native mobile (Expo) app; otherwise it is a Vite SPA.

| Profile | Read |
|---|---|
| Web app, Vite SPA (the default web template) | [Backend functions (Vite SPA)](references/web-spa.md) |
| Web app, TanStack Start | [Server functions and server routes (TanStack Start)](references/web-tanstack.md) |
| Native mobile app (Expo, React Native) | [Backend functions (mobile apps)](references/mobile.md) |
