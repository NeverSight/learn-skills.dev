---
name: flutter-apps-skill
description: Flutter feature-first MVVM architecture with Riverpod 3.x code generation, Freezed 3.x sealed classes, GoRouter, Drift, Hive CE persistence, and ShowcaseView guided tours. Use this skill when building, reviewing, or refactoring Flutter apps that use Riverpod for state management. Covers feature-first structure, MVVM presentation patterns, state management, local storage, onboarding tours, performance, pagination, search, and forms.
license: MIT
metadata:
  author: akhlashashmi
  version: "3.3.0"
  tags: flutter, riverpod, freezed, state-management, mvvm, dart, drift, hive, persistence, local-storage, showcaseview, guided-tours, onboarding
---

# Flutter Best Practices

Use this skill for Flutter apps built with a feature-first MVVM architecture, Riverpod 3.x code generation, Freezed 3.x sealed classes, and GoRouter.

## Core Stack

| Package | Version | Purpose |
|---------|---------|---------|
| flutter_riverpod | 3.2.1+ | State management |
| riverpod_annotation | 3.x | Code generation annotations |
| riverpod_generator | 3.x | Provider code generation |
| freezed | 3.2.5+ | Immutable data classes and unions |
| freezed_annotation | 3.x | Freezed annotations |
| go_router | 17.1.0+ | Declarative routing |
| go_router_builder | 4.2.0+ | Type-safe route code generation |
| drift | 2.32.0+ | SQLite ORM and reactive queries |
| drift_dev | 2.32.0+ | Drift code generation and migrations |
| drift_flutter | 0.3.0+ | Flutter helpers for Drift connections |
| sqlite3_flutter_libs | latest | Native SQLite binaries |
| showcaseview | 5.0.1+ | First-run guided tours |
| json_serializable | latest | JSON serialization |
| build_runner | latest | Code generation runner |

## Architecture

Use a feature-first MVVM structure. Organize code by feature first, then split each feature into `data`, `domain`, `repositories`, and `presentation`.

Treat `presentation/` as the MVVM layer:
- Screens and widgets are the View.
- Riverpod notifiers are the ViewModel.
- `domain/` holds pure business entities.
- `data/` holds models and data sources.
- `repositories/` orchestrate reads, writes, mapping, and caching for the feature.

```text
lib/
|-- core/           # Shared code: theme, utils, widgets, navigation, services
|-- features/       # Feature modules (auth, products, home, ...)
|   `-- feature_x/
|       |-- data/           # Models and data sources (API/local)
|       |-- domain/         # Pure Dart entities with no framework dependencies
|       |-- repositories/   # Coordinate data sources and map models to entities
|       `-- presentation/   # Notifiers, screens, and widgets
`-- main.dart
```

Keep each layer focused on one responsibility. Domain defines entities. Data handles models and data sources. Repositories coordinate feature data flow. Presentation manages UI state and user interaction through MVVM-style notifiers.

## Critical Rules

1. **Use code generation only**. Prefer `@riverpod` or `@Riverpod(keepAlive: true)`. Do not use `StateProvider`, `StateNotifierProvider`, or `ChangeNotifierProvider`.
2. **Use sealed classes with Freezed**. Declare Freezed types as `sealed class`, not `abstract class`.
3. **Avoid prop drilling**. Let child widgets watch providers directly instead of receiving provider state through constructors.
4. **Guard async work**. After every `await` in a notifier, check `if (!ref.mounted) return;`.
5. **Use a single `Ref` type**. Riverpod 3.x uses `Ref`. Do not use `AutoDisposeRef`, `FutureProviderRef`, or generated ref subtypes.
6. **Rely on equality filtering**. Providers already use `==` to filter updates. Override `updateShouldNotify` only when necessary.
7. **Use `select` in leaf widgets**. Prefer `ref.watch(provider.select((s) => s.field))` when a widget needs only one field.
8. **Keep one class per file**. Each entity, model, notifier, screen, and widget should live in its own file.
9. **Stay feature-first**. Do not move feature-specific code into app-wide type folders.
10. **Keep MVVM boundaries clear**. Put UI logic in widgets and Riverpod notifiers, not in repositories or datasources.

## Provider Decision Tree

```text
Is it a repository, datasource, or service?
  -> Use @Riverpod(keepAlive: true) so it stays alive

Is it a feature notifier that manages mutable state?
  -> Use @Riverpod(keepAlive: true) class FeatureNotifier extends _$FeatureNotifier

Is it a computed value or one-time fetch?
  -> Use @riverpod so it auto-disposes when unused

Does it need parameters?
  -> Add parameters to the generated function and let codegen create the family
```

## Freezed Patterns

```dart
// Simple data class
@freezed
sealed class Product with _$Product {
  const Product._(); // Required when adding methods or getters

  const factory Product({
    required String id,
    required String name,
    @Default(0) int quantity,
  }) = _Product;

  factory Product.fromJson(Map<String, dynamic> json) => _$ProductFromJson(json);

  // Keep domain behavior on the model itself.
  bool get inStock => quantity > 0;
}

// Union type with exhaustive pattern matching
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

# Clean build to resolve conflicts
dart run build_runner clean && dart run build_runner build -d
```

## Quick Imports

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:go_router/go_router.dart';
import 'package:my_app/core/extensions/extensions.dart'; // Context, string, and date extensions

// In route files
part 'routes.g.dart';
```

## Anti-Patterns

| Avoid | Prefer | Why |
|-------|--------|-----|
| `StateProvider` | `@riverpod` code generation | `StateProvider` is legacy and moved to `legacy.dart` |
| `abstract class` with Freezed | `sealed class` | Enables exhaustive pattern matching |
| Parent watches and passes state to child | Child watches directly | Avoids prop drilling |
| Missing `ref.mounted` check | `if (!ref.mounted) return;` | Prevents updates after disposal |
| `ref.read` in `initState` | `addPostFrameCallback` and then read | Ensures the provider is ready |
| `AutoDisposeNotifier` | `Notifier` in Riverpod 3.x | Old duplication was removed |
| `ExampleRef ref` in generated code | `Ref ref` | Ref subclasses were removed |
| `try-catch` in every layer | Catch once in the notifier | Avoids repetitive rethrows |
| `context.go('/path')` string routes | `const MyRoute().go(context)` | Gives compile-time safety |
| `context.go()` between peer routes just to update the URL | `GoRouter.optionURLReflectsImperativeAPIs = true` with `push`/`pop` | Preserves directional animation while still updating the browser URL |
| Redirect every `loading` state to splash | Return `null` during loading for non-setup pages | Prevents losing the current web URL during refresh |
| Depend only on GoRouter redirect after login | Add `ref.listen(authProvider)` in auth pages as a fallback | Redirect timing can be unreliable |
| Use auth-level `isLoading` during OAuth | Use per-button loading such as `isGoogleLoading` | Prevents premature splash redirects |
| `ref.watch()` inside GoRouter redirect | `ref.listen()` plus `refreshListenable`, then `ref.read()` in redirect | Prevents router recreation and stack resets |
| Full re-fetch on every sync | `mergeAll` plus ID diff with `deleteByIds` | Reduces work from all records to changed records only |
| `Theme.of(context).colorScheme` | `context.colors` | Keeps color access consistent through extensions |
| `ScaffoldMessenger.of(context)` | `SnackBarUtils.showSuccess()` | Centralizes feedback and avoids context plumbing |
| Anemic model with mapping logic elsewhere | Rich model with methods on the model | Keeps behavior close to data |
| Missing `@JsonSerializable(explicitToJson: true)` on nested Freezed models | Add it on the factory constructor | Prevents release crashes such as `_XYZ is not a subtype of Map` |

## Reference Files

Read only the reference file that matches the task.

| Topic | File |
|-------|------|
| Architecture layers and file structure | [architecture.md](references/architecture.md) |
| Atomic design from tokens to pages | [atomic-design.md](references/atomic-design.md) |
| Riverpod 3.x code generation patterns | [riverpod-codegen.md](references/riverpod-codegen.md) |
| Freezed sealed classes, unions, and rich models | [freezed-sealed.md](references/freezed-sealed.md) |
| State management, async flows, and notifiers | [state-management.md](references/state-management.md) |
| Pagination, search, forms, and delta sync | [common-patterns.md](references/common-patterns.md) |
| Performance, rebuilds, and optimization | [performance.md](references/performance.md) |
| Keys, slivers, animations, isolates, accessibility, and adaptive UI | [flutter-optimizations.md](references/flutter-optimizations.md) |
| Context extensions, string and date utilities, validators, and DRY helpers | [extensions-utilities.md](references/extensions-utilities.md) |
| Hive CE persistence, `@GenerateAdapters`, and TypeAdapters | [hive-persistence.md](references/hive-persistence.md) |
| Drift persistence, scalable structure, and migrations | [drift-persistence.md](references/drift-persistence.md) |
| Showcase guided tours, mixins, and the v5 API | [showcase-tours.md](references/showcase-tours.md) |
