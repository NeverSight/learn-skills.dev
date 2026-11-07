---
name: flutter-state-management
description: Design or review Flutter state ownership, update flow, and package integration. Use for setState, Listenable, Provider, Riverpod, Bloc, Redux, or custom state problems; preserve the project's established approach unless migration is requested.
---

# Flutter State Management

Start with ownership and lifetime, then choose mechanics.

## Inspect

Identify which state is ephemeral UI state, feature state, shared application state, cached server data, or persisted data. Determine who creates, mutates, observes, and disposes it.

## Rules

- Keep state as local as its consumers allow.
- Maintain a single source of truth and derive secondary values instead of synchronizing copies.
- Make state transitions explicit and keep side effects outside widget `build` methods.
- Preserve an established package and its conventions when they are functioning.
- For a new project, choose based on complexity, team familiarity, testability, code generation tolerance, and lifecycle needs—not popularity alone.
- Expose immutable state or read-only views of mutable collections.
- Model loading, empty, success, and failure states deliberately where the UI distinguishes them.
- Avoid broad subscriptions that rebuild unrelated subtrees.
- Use the package's watch-style accessor (`ref.watch`, `context.watch<T>()`, `BlocBuilder`) only inside `build` or another watch-safe method, and its one-off accessor (`ref.read`, `context.read<T>()`, a Bloc's `add`) inside callbacks and event handlers. Calling the watch-style accessor from a callback throws or misbehaves in most packages.

Do not introduce global service locators or package-level singletons as a shortcut for unclear ownership.

## Verification

Test meaningful transitions, failure recovery, disposal, and repeated events. Inspect rebuild scope for hot paths and run widget tests for state-to-UI behavior.

## Boundaries

Architecture-wide dependency direction belongs to `flutter-architecture`; persistence and remote caching belong to their data specialists.

When disposal behavior or lifecycle leaks are in scope, follow the [lifecycle and disposal reference](references/lifecycle-and-disposal.md). For async state modeling and error recovery, follow the [async state patterns reference](references/async-state-patterns.md).

## Sources

- [Flutter state management fundamentals](https://docs.flutter.dev/get-started/fundamentals/state-management)
