---
name: audiobits
description: Build procedural browser audio with AudioBits, from a simple confirmation sound to original recipes, sustained live controls, and complete interactive experiences. Use for integrating AudioBits into an application, designing sounds, or adapting copy-owned catalog source.
---

# AudioBits

Choose the simplest solution that satisfies the request. Inspect the consumer's
framework, entrypoints, installed dependencies, audio ownership and existing
controls before editing. Use its installed `audiobits` public exports, types,
`audiobits/schema.json` and `audiobits/capabilities.json` as the authority. Do not
assume the website or this Skill matches that runtime version.

## Choose the depth

- **Simple integration:** Read [integration](references/integration.md). Create
  or integrate a minimal valid recipe and wire activation, errors, Stop and
  disposal into the existing application. Avoid a catalog install or controller
  when a short local sound is sufficient.
- **Original sound:** Also read [recipe design](references/recipe-design.md).
  Inspect supported features, design JSON-only data, validate it, and connect
  only the controls the request needs.
- **Sustained controls or a complete experience:** Read
  [interactions](references/interactions.md) and check
  [catalog](references/catalog.md) for a useful starting point. Install only
  relevant owned source and adapt its controller to application state and UI.
  Keep the application's entrypoint and lifecycle; do not transplant a demo.
- **Validation or optional tools:** Read [tooling](references/tooling.md) when
  choosing checks, resolving contracts, or considering the bundled local MCP.
  Every workflow works without MCP.

## Optional MCP policy

Understand the request first. For simple sounds and integrations, use public
APIs and ordinary coding tools directly; do not suggest MCP installation.
For complex catalog discovery, capability comparisons or repeated validation,
check whether AudioBits MCP is already available and use its actual tools where
helpful. If absent but useful, explain the concrete benefit and request any
required permission for host configuration. When authorized and supported,
follow [tooling](references/tooling.md) to configure the installed local script.
If configuration is unsupported, denied or fails, continue the normal workflow
with installed exports and the catalog reference. Never block audio development
on MCP setup. Installing this Skill does not register or start the server.

## Core workflow

1. Establish the installed runtime's supported contract and the host's resource
   ownership. Install `audiobits` with the project's package manager only if
   needed; do not upgrade an existing consumer incidentally.
2. Keep recipes serializable and application state in host/controller code.
   Use `defineSound` for typed local definitions and `validateRecipe` for
   generated or external data. Fix reported issues before integrating playback.
3. Call `audio.start()` synchronously in a direct user gesture, await activation,
   then play. Surface failures and allow a new gesture to retry. Invalidate
   pending starts on Stop, hide and teardown so cancelled audio never plays later.
4. Own resources at the existing host boundary. Stop voices, suspend on hide,
   require a new gesture on return, and dispose on navigation/unmount. Clean up
   listeners, frames, subscriptions and caller-owned native connections.
5. Typecheck through public exports, validate recipes, and check relevant control
   extrema and browser lifecycle behavior. Report the checks run and their results.

Do not invent runtime APIs, unsupported primitives, or executable recipe strings.
Compose supported features first. Add no recording, worklets, framework adapters,
runtime changes or unrelated application complexity unless the user requests them.
