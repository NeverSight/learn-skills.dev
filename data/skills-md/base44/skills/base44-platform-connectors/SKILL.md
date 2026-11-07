---
name: base44-platform-connectors
description: "Base44 app connectors: OAuth integrations with external services (Google, Slack, GitHub and more) in shared, app-user and BYO-shared modes, how to connect one from an external agent, and how server code reads the token with getConnection. Use when the app must act on a user's or the builder's account at a third-party service."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 connectors

Connectors are configured against the app, not authored as files: list the catalog, connect with the complete scope set, then read tokens in server code.

> **Requires the Builder plan or above.** The workspace's entitlement is reported by the agent-profile endpoint; on a lower plan the platform rejects the deploy.

## Pick the reference for this app

Determine the app profile first. Call `GET /api/apps/{app_id}/agent-profile` (over the Base44 MCP `execute_api`
tool, or with your Base44 CLI token); it returns the framework, app type, runtime,
entitlements and the exact reference files to read. Without it, detect from the project files:
`src/routes/__root.*` and `src/routeTree.gen.ts` mean TanStack Start; `app/_layout.*` means a
native mobile (Expo) app; otherwise it is a Vite SPA.

| Profile | Read |
|---|---|
| Web app, Vite SPA (the default web template) | [App connectors (Vite SPA)](references/web-spa.md) |
| Web app, TanStack Start | [App connectors (TanStack Start)](references/web-tanstack.md) |
| Native mobile app (Expo, React Native) | [App connectors (mobile apps)](references/mobile.md) |
