---
name: flutter-ai-integration
description: Build or review provider-neutral AI features in Flutter, including streaming responses, conversation state, structured output, tool calls, attachments, cancellation, and safe service boundaries. Use when model behavior is part of the product; do not use for ordinary APIs, product analytics, or generic chat between people.
---

# Flutter AI Integration

Integrate model behavior as an unreliable, asynchronous external capability with an explicit product contract. Preserve the project's provider, backend, networking client, state management, persistence, and UI architecture unless the user requests a migration.

Do not add a provider SDK, account setup, credential, or backend merely because this skill was selected.

## Preflight

Read `pubspec.yaml`, SDK constraints, existing AI or API adapters, backend boundary, authentication, model configuration, state ownership, persistence, privacy requirements, tests, and platform targets. Clarify the intended capability and failure behavior before choosing a model, provider, SDK, or UI toolkit.

Keep model and provider details behind a narrow application-owned interface. Treat output, tool arguments, citations, and structured data as untrusted input. Define cancellation, timeout, retry, partial-result, quota, offline, and unsupported-capability behavior.

## Load references conditionally

- Read [service boundary and secrets](references/service-boundary-and-secrets.md) when selecting client versus backend responsibilities, credentials, provider abstraction, safety, privacy, or model configuration.
- Read [streaming, tools, and state](references/streaming-tools-and-state.md) when implementing streamed output, conversations, attachments, structured responses, or tool/function calls.
- Read [Flutter AI Toolkit and GenUI](references/flutter-ai-toolkit-and-genui.md) only when the project uses or is considering those Flutter packages. Do not introduce them by default.

## Boundaries

- `flutter-networking` owns generic HTTP, WebSocket, SSE, authentication refresh, and transport reliability; this skill owns model-specific semantics on top.
- `dart-concurrency` owns general stream races, cancellation primitives, and isolate behavior.
- `flutter-persistence` owns durable storage and offline synchronization; this skill defines what conversation or model state may be retained.
- `flutter-security` owns a broad threat review; this skill enforces the model boundary, credential placement, untrusted output handling, and least-privilege tools.
- `flutter-ui-patterns` and `flutter-accessibility` own general interface composition and accessibility.

## Verification

Use a deterministic fake model or recorded adapter for ordinary automated tests. Cover partial chunks, cancellation, timeout, malformed structured output, tool denial and failure, repeated or reordered events, quota errors, and provider unavailability. Use a real provider only when credentials, cost, network access, and environment are explicitly in scope; keep such tests separate and non-destructive.

Verify the visible stream and state transitions on affected platforms, including restart or restoration when required. Report which behavior was fake-tested, which was exercised end to end, the exact provider/model configuration when relevant, and any cost, safety, or backend boundary not verified.

## Sources

- [Flutter AI overview](https://docs.flutter.dev/ai)
- [Flutter AI Toolkit](https://docs.flutter.dev/ai/ai-toolkit)
- [Flutter GenUI](https://docs.flutter.dev/ai/genui)
- [Flutter networking](https://docs.flutter.dev/data-and-backend/networking)
