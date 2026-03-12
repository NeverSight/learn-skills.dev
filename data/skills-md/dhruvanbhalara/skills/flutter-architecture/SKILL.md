---
name: flutter-architecture
description: Clean Architecture, Data Models, Tech Stack, Error Handling & Platform Channels
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "architecture"
---

# Technology Stack

- Flutter for cross-platform development
- Dart as the primary programming language
- bloc for state management
- injectable for dependency injection
- Dart Mappable for immutable data models
- Dio for HTTP networking
- isar for local database
- Firebase for backend services

# Clean Architecture

-   **Domain Purity**: The `domain` layer must be pure Dart. NO `package:flutter` imports.
-   **Layer Dependency**: `Presentation -> Domain <- Data`. Data layer implements Domain interfaces.
-   **Feature-First 2.0**: Enforce strict separation of `DataSources` (External/Raw) vs `Repositories` (Domain abstraction).

## Directory Structure

- Organize code according to feature-based Clean Architecture pattern (`featureA/bloc`, `featureA/models`, `featureA/views`)
- Place cross-feature components in the `core` directory
- Group shared widgets in `core/views/widgets` by type

## Three-Layer Data Model Pattern

1. **API Layer (ItemApiModel)**
   - Represents the raw data structure as received from the server
   - Contains all fields provided by the API
   - Should match the API contract exactly

2. **Domain Layer (Item)**
   - Represents the internal data model
   - Contains only the fields necessary for business logic
   - Strips out unnecessary API fields

3. **UI Layer (ItemUiState)**
   - Represents the data model optimized for UI rendering
   - Contains parsed and formatted data ready for display
   - Handles all UI-specific transformations

## Data Model Rules

- Use Dart Mappable for defining immutable UI states
- Each layer should have its own type definition
- The UI layer should use the UI state data models, never directly the domain model or the API model
- The UI state model should be derived from the domain model, not the API model
- The domain model should be derived from the API model, not the UI state model

## Repository & DataSource Pattern

- Repositories orchestrate between data sources (return Domain Model)
- Data sources access raw data (return API Model)
- The repository should be the source of truth, and it returns the domain model
- DataSources MUST only contain raw SDK/API calls. No mapping or business logic.
- No direct backend SDK/API calls outside DataSources

## Data Flow

```
UI Event → BLoC (emit Loading) → Repository → DataSource (API/SDK)
    ↓
Response → Repository (map to Domain Entity) → BLoC (emit Success/Error) → UI
```

# Dart 3 Language Features

-   **Sealed Classes**: Use `sealed class` for domain failures to enable exhaustive pattern matching across layers.
-   **Records**: Use records for lightweight multi-value returns where defining a full class is overkill (e.g., `(String name, int age)`).
-   **If-Case Pattern**: Prefer `if (value case final v?)` over `if (value != null)` for null checking with binding.
-   **Class Modifiers**: Use `final`, `interface`, `base`, and `sealed` class modifiers to express API intent.

# Error Handling

-   **Functional Error Handling**: Use `Either<Failure, T>` or `Result<T>` sealed classes. NEVER throw exceptions across layer boundaries.
-   **Pattern Matching**: Exhaustively handle all sealed class states using Dart 3.x `switch` expressions in UI and BLoCs.
-   Throw errors when needed, and catch them at appropriate boundaries
-   Log errors with context
-   Present user-friendly error messages in the UI
-   Avoid silent failures; always handle or propagate errors

# Platform Channels & Native Integration

-   Use `MethodChannel` for one-off calls to native code (e.g., reading device info, triggering native APIs)
-   Use `EventChannel` for continuous streams from native to Flutter (e.g., sensor data, connectivity changes)
-   Place all channel code in a dedicated `platform/` directory within the relevant feature
-   Define channel names as constants: `static const channel = MethodChannel('com.app.feature/method')`
-   Wrap all channel calls in a DataSource — never call `MethodChannel` directly from BLoC or UI
-   Handle `MissingPluginException` gracefully for platforms that don't implement the channel
-   Use `defaultTargetPlatform` checks to guard platform-specific behavior

## FFI (Foreign Function Interface)

-   Use `dart:ffi` for performance-critical native C/C++ code
-   Define bindings in a separate class with clear documentation
-   Prefer Federated Plugins when sharing native code across multiple packages

## Platform-Specific Code

-   Use `Platform.isAndroid` / `Platform.isIOS` for runtime checks (import `dart:io`)
-   For web, use `kIsWeb` from `package:flutter/foundation.dart`
-   Prefer adaptive widgets (`Switch.adaptive`, `Slider.adaptive`) over manual platform checks where possible

# Coding Guidelines & Maintenance

-   **Conciseness**: Keep files < 300 lines and functions < 50 lines. Keep classes to < 10 public methods.
-   **Strong Typing**: STRICTLY prohibit `dynamic`. Use `Object?` or explicit types.
-   **Guard Clauses**: Use early returns (e.g., `if (user == null) return;`) to reduce nesting and improve readability.
-   **Disposable Lifecycle**: `TextEditingController`, `ScrollController`, `FocusNode`, `StreamSubscription`, `AnimationController`, etc., MUST be `late` initialized in `initState()` and disposed in `dispose()`.
-   **No Print Statements**: STRICTLY prohibit `print()`. Use `AppLogger` for all logging.
-   **Reuse**: Extract widgets or code blocks used multiple times into `core/views/widgets` or utilities.

# Documentation

-   **Why, not What**: Comments MUST explain the rationale (intent), not what the code does.
-   **Public API**: Document public classes and methods with triple-slash (`///`) comments.
-   **History**: Do NOT include version history or "fixed by" comments. Git is the source of truth.
