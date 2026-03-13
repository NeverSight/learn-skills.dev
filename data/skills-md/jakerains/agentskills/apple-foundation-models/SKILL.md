---
name: apple-foundation-models
description: Build Apple Intelligence features with Foundation Models and Image Playground on iOS, iPadOS, macOS, and visionOS. Use when implementing or debugging SystemLanguageModel, LanguageModelSession, guided generation with @Generable, tool calling, custom adapters, model availability checks, context-window limits, local on-device inference, routing to larger-model paths (App Intents Use Model or custom backend fallback), and ImagePlayground or ImageCreator APIs.
---

# Apple Foundation Models and Image Playground

Implement reliable Apple Intelligence features with Apple's on-device text and image generation APIs.

## Workflow

1. Classify the request before writing code. Use Foundation Models for on-device text generation in app code, use ImagePlayground for image generation in app code, and use App Intents and Shortcuts guidance when the request is specifically about the "Use Model" action and automation workflows.
2. Check platform support and runtime readiness first (`isAvailable` and `availability` states), then design fallback UI for unavailable states.
3. Implement a local-first path with clear prompt and instruction design before considering adapters.
4. Add tools, guided generation, and performance tuning only as needed for the task.
5. Decide whether to route to a larger model path. For Apple-managed routing in automation flows, use App Intents and Shortcuts "Use Model" guidance. For in-app cloud escalation, use an explicit backend model path and keep local execution as the default when possible.
6. Validate behavior on physical devices and include robust error handling for language, context size, and tool failures.

## References

- Foundation model implementation details: `references/foundation-models-framework.md`
- Local versus larger-model routing strategy: `references/routing-local-vs-bigger-model.md`
- Image Playground implementation details: `references/image-playground.md`

## Execution Rules

- Prefer official Apple docs and WWDC sources for API behavior.
- Treat Foundation Models app APIs as on-device unless Apple docs explicitly document a server-routing API for app code.
- Re-verify docs for "latest" requests because Apple Intelligence behavior can change across OS releases.
- Keep prompts concise and structured to reduce token use and latency.
