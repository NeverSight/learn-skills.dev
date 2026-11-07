---
name: base44-platform-integrations-sdk
description: "Base44 built-in integrations on the SDK client: InvokeLLM, SendEmail, file uploads (public and private), signed URLs, data extraction and image generation, with every Core endpoint's input schema, plus analytics event tracking. Use when a feature needs AI, email, files or analytics without a third-party service."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 integrations sdk

File uploads and signed URLs are called from the browser SDK; every other Core integration runs in server code on an app with core-integration control, the default for new apps (profile `core_integrations: backend_functions_only`). The endpoint schemas below are the ones the platform serves today.

## Pick the reference for this app

Determine the app profile first. Call `GET /api/apps/{app_id}/agent-profile` (over the Base44 MCP `execute_api`
tool, or with your Base44 CLI token); it returns the framework, app type, runtime,
entitlements and the exact reference files to read. Without it, detect from the project files:
`src/routes/__root.*` and `src/routeTree.gen.ts` mean TanStack Start; `app/_layout.*` means a
native mobile (Expo) app; otherwise it is a Vite SPA.

| Profile | Read |
|---|---|
| Web app, Vite SPA (the default web template) | [Integrations and analytics SDK (Vite SPA)](references/web-spa.md) |
| Web app, TanStack Start | [Integrations and analytics SDK (TanStack Start)](references/web-tanstack.md) |
| Native mobile app (Expo, React Native) | [Integrations SDK (mobile apps)](references/mobile.md) |
