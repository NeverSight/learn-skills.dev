---
name: building-flutter-apps
description: Flutter clean architecture with Riverpod 3.x codegen, Freezed 3.x sealed classes, GoRouter, and Hive CE persistence. Use when building, reviewing, or refactoring Flutter apps with Riverpod state management. Covers architecture layers, state management, local storage with Hive TypeAdapters, testing, performance, pagination, search, and forms.
license: MIT
metadata:
  author: sgaabdu4
  version: "3.1.0"
  tags: flutter, riverpod, freezed, state-management, clean-architecture, dart, hive, persistence, local-storage
---

# Flutter Best Practices

Flutter clean architecture skill using Riverpod 3.x (codegen), Freezed 3.x (sealed classes), and GoRouter.

## Core Stack

| Package | Version | Purpose |
|---------|---------|---------|
| flutter_riverpod | 3.2.1+ | State management |
| riverpod_annotation | 3.x | Codegen annotations |
| riverpod_generator | 3.x | Provider code generation |
| freezed | 3.2.5+ | Immutable data classes, unions |
| freezed_annotation | 3.x | Freezed annotations |
| go_router | 17.1.0+ | Declarative routing |
| go_router_builder | 4.2.0+ | Type-safe route code generation |
| json_serializable | latest | JSON serialization |
| build_runner | latest | Code generation |

## Architecture

Four layers. Dependencies flow inward: Presentation → Repository → Domain → Data.

```
lib/
├── core/           # Shared: theme, utils, widgets, navigation, services
├── features/       # Feature modules (auth, products, home, ...)
│   └── feature_x/
│       ├── data/           # Models, datasources (API/local)
│       ├── domain/         # Entities (pure Dart, no dependencies)
│       ├── repositories/   # Orchestrate data sources, map models → entities
│       └── presentation/   # Notifiers, screens, widgets
└── main.dart
```

Each layer has one job. Domain holds pure Dart entities. Data holds models and datasources. Repositories bridge them. Presentation manages state and UI.

## Critical Rules

1. **Codegen only** — Use `@riverpod` / `@Riverpod(keepAlive: true)`. Never use `StateProvider`, `StateNotifierProvider`, or `ChangeNotifierProvider`.
2. **Sealed classes** — All Freezed classes use `sealed class`, not `abstract class`.
3. **No prop drilling** — Child widgets watch providers directly. Never pass provider state through constructor parameters.
4. **Guard async** — Check `if (!ref.mounted) return;` after every `await` in notifiers.
5. **Single Ref** — Riverpod 3.0 uses one `Ref` type. No `AutoDisposeRef`, no `FutureProviderRef`, no `ExampleRef`.
6. **Equality filtering** — All providers use `==` to filter notifications. Override `updateShouldNotify` only when needed.
7. **Select in leaves** — Use `ref.watch(provider.select((s) => s.field))` in leaf widgets. Watch full state only when necessary.
8. **One file per class** — Each entity, model, notifier, screen, and widget gets its own file.

## Provider Decision Tree

```
Is it a repository, datasource, or service?
  → @Riverpod(keepAlive: true) — lives forever

Is it a feature notifier (manages mutable state)?
  → @Riverpod(keepAlive: true) class FeatureNotifier extends _$FeatureNotifier

Is it a computed value or one-time fetch?
  → @riverpod (auto-disposes when unused)

Does it need parameters?
  → Add parameters to the generated function (family via codegen)
```

## Freezed Patterns

```dart
// Simple data class
@freezed
sealed class Product with _$Product {
  const factory Product({
    required String id,
    required String name,
    @Default(0) int quantity,
  }) = _Product;

  factory Product.fromJson(Map<String, dynamic> json) => _$ProductFromJson(json);
}

// Union type (exhaustive pattern matching)
@freezed
sealed class AuthState with _$AuthState {
  const factory AuthState.authenticated(User user) = Authenticated;
  const factory AuthState.unauthenticated() = Unauthenticated;
  const factory AuthState.loading() = AuthLoading;
}
```

## Notifier Pattern

```dart
@Riverpod(keepAlive: true)
class ProductNotifier extends _$ProductNotifier {
  @override
  ProductState build() {
    _load();
    return const ProductState();
  }

  Future<void> _load() async {
    state = state.copyWith(isLoading: true);
    try {
      final items = await ref.read(productRepositoryProvider).fetchAll();
      if (!ref.mounted) return;
      state = state.copyWith(items: items, isLoading: false);
    } catch (e) {
      if (!ref.mounted) return;
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }
}
```

## Code Generation

```bash
# Watch mode (recommended during development)
dart run build_runner watch -d

# One-time build
dart run build_runner build -d

# Clean build (resolve conflicts)
dart run build_runner clean && dart run build_runner build -d
```

## Quick Imports

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:go_router/go_router.dart';
import 'package:my_app/core/extensions/extensions.dart'; // All context/string/date extensions

// In route files
part 'routes.g.dart';
```

## Anti-Patterns

| Wrong | Right | Why |
|-------|-------|-----|
| `StateProvider` | `@riverpod` codegen | Legacy, moved to `legacy.dart` |
| `abstract class` with Freezed | `sealed class` | Enables exhaustive matching |
| Parent watches, passes to child | Child watches directly | Prop drilling |
| Missing `ref.mounted` check | `if (!ref.mounted) return;` | Crash on disposed notifier |
| `ref.read` in `initState` | `addPostFrameCallback` then read | Provider not ready |
| `AutoDisposeNotifier` | `Notifier` (unified in 3.0) | Duplicate removed |
| `ExampleRef ref` in codegen | `Ref ref` in codegen | Ref subclasses removed |
| Try-catch at every layer | Catch once in notifier | Useless rethrows |
| `context.go('/path')` string routes | `const MyRoute().go(context)` typed | No compile-time safety |
| `context.go()` between peer routes for URL update | `GoRouter.optionURLReflectsImperativeAPIs = true` + `push`/`pop` | `go` loses directional animation; this flag makes `push`/`pop` update the browser URL |
| Redirect to splash during `loading` for all pages | `return null` during loading for non-setup pages | On web refresh, bouncing `/chat` → `/` → `/home` loses the URL; stay on current page until auth resolves |
| Rely only on GoRouter redirect for post-login nav | Add `ref.listen(authProvider)` in auth pages as fallback | `refreshListenable` timing is unreliable; explicit navigation from login/signup guarantees the transition |
| Setting auth-level `isLoading` during OAuth | Use per-button loading (`isGoogleLoading`) | Auth `isLoading` triggers `SetupStatus.loading` → premature splash redirect before OAuth completes |
| `ref.watch()` inside GoRouter redirect | `ref.listen()` + `refreshListenable` + `ref.read()` in redirect | `ref.watch` recreates router on every state change, resetting route stack |
| Full re-fetch every sync | `mergeAll` + ID-diff `deleteByIds` | O(all) → O(changed) |
| `Theme.of(context).colorScheme` | `context.colors` | Use context extensions |
| `ScaffoldMessenger.of(context)` | `SnackBarUtils.showSuccess()` | Centralized, context-free |

## Reference Files

| Topic | File |
|-------|------|
| Architecture layers, file structure | [architecture.md](references/architecture.md) |
| Atomic design: tokens → pages | [atomic-design.md](references/atomic-design.md) |
| Riverpod 3.x codegen patterns | [riverpod-codegen.md](references/riverpod-codegen.md) |
| Freezed sealed classes, unions | [freezed-sealed.md](references/freezed-sealed.md) |
| State management, async, notifiers | [state-management.md](references/state-management.md) |
| Testing with ProviderContainer.test | [testing.md](references/testing.md) |
| Pagination, search, forms, delta sync | [common-patterns.md](references/common-patterns.md) |
| Performance, rebuilds, optimization | [performance.md](references/performance.md) |
| Keys, slivers, animations, isolates, accessibility, adaptive | [flutter-optimizations.md](references/flutter-optimizations.md) |
| Context extensions, string/date utils, validators, DRY utilities | [extensions-utilities.md](references/extensions-utilities.md) |
| Hive CE persistence, @GenerateAdapters, TypeAdapters | [hive-persistence.md](references/hive-persistence.md) |
