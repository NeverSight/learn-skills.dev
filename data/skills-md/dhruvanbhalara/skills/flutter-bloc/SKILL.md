---
name: flutter-bloc
description: State Management, Dependency Injection & Navigation
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "architecture"
---

# BLoC Pattern

-   **Sealed States & Events**: Always use `sealed class` for both States and Events to ensure exhaustive UI handling and compile-time safety.
-   **Immutability**: All States, Events, and Domain Entities MUST be immutable (using `final` and `Equatable` or `freezed`).
-   **Official BLoC Part-Part Of Pattern**: Every `_bloc.dart` file MUST include its corresponding `_event.dart` and `_state.dart` files using `part` directives. Each event/state file MUST have a `part of` directive pointing back to the bloc file. This ensures a single library scope and shared private members.
    ```dart
    // auth_bloc.dart
    part 'auth_event.dart';
    part 'auth_state.dart';

    class AuthBloc extends Bloc<AuthEvent, AuthState> { ... }

    // auth_event.dart
    part of 'auth_bloc.dart';

    // auth_state.dart
    part of 'auth_bloc.dart';
    ```
-   **Mandatory Directory Structure**: Every BLoC feature set MUST reside in its own sub-directory within the `bloc/` folder. Flat `bloc/` directories are STRICTLY prohibited.
    ```text
    presentation/bloc/
    └── <bloc_name>/
        ├── <bloc_name>_bloc.dart
        ├── <bloc_name>_event.dart
        └── <bloc_name>_state.dart
    ```
-   **Loading State Mandate**: ALWAYS emit `Loading` before async work, then `Success` or `Error`. Never skip the loading state.
-   **Concurrency**: Use `transformers` (e.g., `restartable()`, `droppable()`) for events requiring debouncing (search) or throttling (buttons).
-   **Zero-Logic UI**: Widgets MUST NOT contain business logic, orchestration logic, or direct calls to external services. They should ONLY dispatch events and build UI based on BLoC states.

## BLoC Widget Usage

-   `BlocBuilder` for local UI rebuilds based on state
-   `BlocListener` for side effects (navigation, snackbars, dialogs)
-   `BlocConsumer` when both rebuild and side effects are needed
-   `context.read<Bloc>().add(Event())` for dispatching events
-   `context.watch<Bloc>().state` for reactive rebuilds (inside `build()` only)

## BLoC Submission Checklist

- [ ] Events and States use `Equatable` with correct `props`
- [ ] All async operations follow `Loading → Success/Error` pattern
- [ ] No business logic in UI widgets
- [ ] No SDK/API calls outside DataSources
- [ ] Zero hardcoded colors, spacing, or typography \u2014 use design tokens (`AppColors`, `AppSpacing`)
- [ ] Code formatted with `dart format`

# Dependency Injection

-   Use `injectable` for dependency injection and service location
-   **Standardized Injection**:
    -   Use `@injectable` for screen-specific BLoCs to ensure a fresh instance per screen access.
    -   Use `@lazySingleton` for global or shared BLoCs (e.g., `AuthBloc`, `ThemeBloc`, `SettingsBloc`, `PasswordBloc`).
-   Organize blocs logically by feature and ensure strict separation of concerns

# Navigation & Routing

-   **Dynamic Routes**: STRICTLY prohibit hardcoded route strings in `GoRouter` configuration. Use static constants in `AppRoutes`.
-   **Centralized BLoCs**: BLoC providers MUST be injected via `ShellRoute` or `BlocProvider` in `app_router.dart` when shared across multiple screens or within a feature branch.
-   **No Local Providers**: Avoid `BlocProvider` in individual screen `build()` methods if the BLoC is needed by a feature set.
-   **Primitive Route Arguments**: STRICTLY prohibit passing complex objects (BLoCs, ChangeNotifiers, Entity instances) as route arguments. Pass only primitive IDs/Keys and fetch data in the destination screen using `Repository` or `Bloc` injection.
