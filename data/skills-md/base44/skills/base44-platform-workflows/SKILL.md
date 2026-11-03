---
name: base44-platform-workflows
description: "Base44 workflows: trigger-driven automated processes defined as CNCF Serverless Workflow files under base44/workflows/ (scheduled, entity, connector, in-app agent, auth, publish and payment triggers; call, wait and switch steps; jq expressions), with the full authoring guide, plus the legacy automations pipeline for apps that predate workflows. Use for any 'when X happens, do Y' or 'every N hours, do Y'."
---
<!-- GENERATED FILE. DO NOT EDIT. Compiled from the Base44 builder's prompt sources; the
     source commit is in /SOURCE_COMMIT at the repository root. Edits here are overwritten by
     the next sync; change the source instead. -->
# Base44 workflows

Workflows is the default pipeline: a `.jsonc` envelope under `base44/workflows/` is live once written. An app whose profile says `automation_pipeline: legacy_automations` uses the automations reference instead.

> **Requires the Builder plan or above.** The workspace's entitlement is reported by the agent-profile endpoint; on a lower plan the platform rejects the deploy.

## Pick the reference for this app

Determine the app profile first. Call `GET /api/apps/{app_id}/agent-profile` (over the Base44 MCP `execute_api`
tool, or with your Base44 CLI token); it returns the framework, app type, runtime,
entitlements and the exact reference files to read. Without it, detect from the project files:
`src/routes/__root.*` and `src/routeTree.gen.ts` mean TanStack Start; `app/_layout.*` means a
native mobile (Expo) app; otherwise it is a Vite SPA.

| Profile | Read |
|---|---|
| Web app, Vite SPA (the default web template) | [Workflows (Vite SPA and mobile: steps call backend functions)](references/backend-functions.md), [Legacy automations (apps that predate workflows)](references/automations-legacy.md) |
| Web app, TanStack Start | [Workflows (TanStack Start: steps call server routes)](references/web-tanstack.md) |
| Native mobile app (Expo, React Native) | [Workflows (Vite SPA and mobile: steps call backend functions)](references/backend-functions.md), [Legacy automations (mobile apps that predate workflows)](references/mobile-automations.md) |
