---
name: "flutter-riverpod-arch"
description: "Implement Feature-First architecture with Riverpod state management and Flutter Hooks in Flutter applications"
license: "MIT"
metadata:
  author: "shohei"
  version: "1.0.0"
---

# Flutter Riverpod Architecture

## Goal

Implements scalable Flutter applications using the Feature-First directory structure, Riverpod (with code generation) for state management, and `flutter_hooks` / `HookConsumerWidget` for UI composition. This architecture is a lightweight approach inspired by Domain-Driven Design and Clean Architecture. The design philosophy is three layers — Presentation, Domain, and Infrastructure — and the code-level notation in this skill is UI, UseCase, and Repository. Data source access is encapsulated inside repositories. Applies `@Riverpod(keepAlive: true)` for repository providers and `@riverpod` for screen-scoped state.

### Layer Mapping (Source of Truth)

| Design philosophy | Code-level notation |
| --- | --- |
| Presentation | UI |
| Domain | UseCase |
| Infrastructure | Repository |

## Decision Logic

Decide whether the task belongs in UI, UseCase, or Repository, whether it is feature-specific or shared, and which Riverpod scope is appropriate.

See **[architecture.md](references/architecture.md)** for structure and naming, **[providers.md](references/providers.md)** for Repository/UseCase placement, and **[riverpod.md](references/riverpod.md)** for provider scope rules.

## Instructions

### 1. Plan the Feature Structure

Identify the feature, confirm whether the implementation is shared or feature-local, and place files in the correct layer before coding.

See **[architecture.md](references/architecture.md)** for directory structure and naming.

### 2. Implement the Repository Layer

Implement Repository code in the Repository layer and follow the Riverpod/provider rules for Repository providers.

See **[providers.md](references/providers.md)** for Repository implementation details and **[riverpod.md](references/riverpod.md)** for provider scope rules.

### 3. Implement the UseCase Layer

Implement UseCase code in the UseCase layer for validation, orchestration, and UI-facing state changes.

See **[providers.md](references/providers.md)** for UseCase patterns and **[riverpod.md](references/riverpod.md)** for provider scope rules.

### 4. Build the UI with HookConsumerWidget

Build UI in the Presentation layer using the patterns required by this skill.

See **[presentation.md](references/presentation.md)** for page and widget structure, **[riverpod.md](references/riverpod.md)** for `ref.watch` / `ref.read`, and **[button.md](references/ui/button.md)** for button and cursor rules.

### 5. Implement Responsive Layout

Apply the responsive layout rules defined for this skill.

See **[responsive.md](references/ui/responsive.md)** for breakpoint policy and responsive layout patterns.

### 6. Write Tests

Test Repository, UseCase, controller, and widget behavior with the testing patterns used by this skill.

See **[testing.md](references/testing.md)** for test structure, overrides, and fake/mock patterns.

## Constraints

- **Prefer `HookConsumerWidget`:** This skill uses `HookConsumerWidget` (with `flutter_hooks`) for all stateful pages and complex widgets. `StatefulWidget` may be used for isolated, purely local UI state with no Riverpod interaction.
- **No `ref.read()` in `build`:** `ref.read()` must only appear inside event handlers or callbacks, never at the top of a `build` method to derive reactive UI state.
- **No `ref.watch()` in event handlers:** `ref.watch()` must only appear inside `build()` or a provider's `build()` method.
- **No business logic in Views:** Widget classes must contain only layout, conditional rendering, and navigation. All data transformation and validation must reside in Use Cases or Repositories.
- **List patterns:** Follow the list and sliver rules defined in **[list.md](references/ui/list.md)**.
- **Avoid button wrapper widgets for style only:** Do not create a custom wrapper widget whose sole purpose is applying a fixed button style. If you need to encapsulate behavior such as loading state or submission flow, a wrapper is acceptable.
- **Use targeted `MediaQuery` static methods:** Prefer `MediaQuery.sizeOf`, `MediaQuery.paddingOf`, `MediaQuery.orientationOf` etc. over `MediaQuery.of(context)` to avoid unnecessary rebuilds.
- **No `LayoutBuilder` for page-level breakpoints:** Use `ResponsiveLayout` (which uses `MediaQuery.sizeOf`) so the layout decision is based on actual screen width, not parent constraints.
- **Mouse cursors required on macOS/Web:** Every `Button` variant must include `enabledMouseCursor: SystemMouseCursors.click`. Every `InkWell` must include `mouseCursor: SystemMouseCursors.click`.
- **Code generation required:** After adding or modifying a `@riverpod` annotation, always run `dart run build_runner build`.
- **Naming conventions:** Files and directories use `snake_case`; classes use `UpperCamelCase`; page classes end in `Page`; repository classes end in `Repository`; use case classes use verb-noun format (e.g., `FetchPosts`, `CreatePost`).

## Reference Files

- **[architecture.md](references/architecture.md)** — Project structure, directory layout, naming conventions
- **[providers.md](references/providers.md)** — Repository and use case implementation patterns
- **[riverpod.md](references/riverpod.md)** — Provider types, `ref.watch` vs `ref.read`, caching, code generation
- **[presentation.md](references/presentation.md)** — Page structure, navigation, hooks usage, error handling
- **[testing.md](references/testing.md)** — Test patterns, mocking strategy, `ProviderContainer` usage
- **[button.md](references/ui/button.md)** — Button patterns, `styleFrom`, hover cursor for macOS/Web
- **[list.md](references/ui/list.md)** — `ListView.builder`, Pull-to-Refresh, pagination with Slivers
- **[responsive.md](references/ui/responsive.md)** — Breakpoints, `ResponsiveLayout`, platform-specific layouts
