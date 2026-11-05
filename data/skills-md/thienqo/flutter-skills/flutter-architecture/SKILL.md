---
name: flutter-architecture
description: Select, review, or evolve Flutter application boundaries, dependency direction, and feature organization. Use for new project structure, scaling problems, or architecture migrations; do not impose a new pattern during a focused feature fix.
---

# Flutter Architecture

Choose the least complex architecture that keeps responsibilities clear, state testable, and dependencies replaceable.

## Preserve before migrating

Inspect the existing feature structure, state mechanism, dependency injection, data sources, tests, and team conventions. Extend a coherent architecture even when it differs from a preferred example. Propose migration only for a concrete problem and make it incremental.

## Baseline boundaries

- Views render state and forward user intent; keep data access and business rules outside widgets.
- Presentation logic owns UI state and commands.
- Repositories are the source of truth for domain data and coordinate services or caches.
- Services wrap external systems such as HTTP, storage, and platform plugins.
- Add use cases/domain services only when logic is reused, complex, or otherwise clutters presentation state.
- Point dependencies inward through explicit interfaces where replacement or testing justifies them.

The Flutter team's MVVM guidance is a useful default for a new scalable application, not a mandate to replace Riverpod, Bloc, Redux, or an established feature-first design.

## Organization

Prefer user-facing feature boundaries. Place genuinely shared infrastructure in a small core area. Avoid global folders that accumulate unrelated models, widgets, and helpers.

Load [greenfield and evolution](references/greenfield-and-evolution.md) for new-project choices or incremental migrations. Load [feature boundaries and dependency rules](references/feature-boundaries-and-dependency-rules.md) when modules leak across features or ownership is unclear.

## Verification

Demonstrate the dependency path for one feature, test presentation logic without rendering widgets where practical, and confirm no circular or UI-to-infrastructure shortcuts were introduced.

## Sources

- [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide)
- [Common architecture concepts](https://docs.flutter.dev/app-architecture/concepts)
