---
name: base44-platform-platform
description: "Base44 platform concepts for a web app: entities, backend functions or server code, workflows, pages and layouts, the project file structure, authentication (platform login vs the custom-auth boilerplate), user invites and the GitHub features. Read first when starting work on a Base44 web app."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 platform

A Base44 web app is a Vite + React SPA or a TanStack Start project backed by Base44's entities, functions and auth. This reference is the platform orientation the builder itself works from: concepts, file layout, authentication wiring and user invites.

## Pick the reference for this app

Determine the app profile first. Call `GET /api/apps/{app_id}/agent-profile` (over the Base44 MCP `execute_api`
tool, or with your Base44 CLI token); it returns the framework, app type, runtime,
entitlements and the exact reference files to read. Without it, detect from the project files:
`src/routes/__root.*` and `src/routeTree.gen.ts` mean TanStack Start; `app/_layout.*` means a
native mobile (Expo) app; otherwise it is a Vite SPA.

| Profile | Read |
|---|---|
| Web app, Vite SPA (the default web template) | [Web app, Vite SPA](references/web-spa.md) |
| Web app, TanStack Start | [Web app, TanStack Start](references/web-tanstack.md) |
| Native mobile app (Expo, React Native) | [Native mobile app (Expo)](references/mobile.md) |
