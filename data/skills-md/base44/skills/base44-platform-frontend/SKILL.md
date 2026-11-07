---
name: base44-platform-frontend
description: "Frontend coding standards for Base44 web apps: code conventions, the installed packages, routing (React Router in the Vite SPA, file routes in TanStack Start), Tailwind and design tokens, styling and componentization rules, npm installs, and how files are edited in the sandbox. Use when writing or changing pages, components or routes."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 frontend

The builder's own frontend rules for Base44 web apps. Pick the reference for the app's framework; the TanStack reference ends with a worked example.

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
| Native mobile app (Expo, React Native) | [Native mobile app (Expo, React Native, NativeWind)](references/mobile.md) |
