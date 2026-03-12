---
name: flutter-isar
description: Isar Database, Caching & Offline-First Patterns
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "data"
---

# Isar Database

-   Use **Isar** as the primary local database for structured data persistence
-   Define collections using `@collection` annotation with `Id` field
-   Place collection definitions in the `data/local/` directory of the relevant feature
-   Run `dart run build_runner build --delete-conflicting-outputs` after modifying collections

## Schema Design

-   Keep collections focused — one collection per domain entity
-   Use `@Index` annotations for fields queried frequently
-   Use `@enumerated` for enum fields
-   Use `Links` and `Backlinks` for relationships between collections
-   NEVER store derived/computed values — compute them in the domain layer

## Migrations

-   Isar handles additive schema changes automatically (new fields, new collections)
-   For breaking changes (renamed fields, removed fields), write migration logic in the repository
-   Version your database schema and check version on app startup

# Repository Pattern for Local Data

-   Local DataSource wraps all Isar `put`, `get`, `delete`, `watch` calls
-   Repositories orchestrate between remote and local DataSources
-   Repositories decide cache-first vs network-first strategy per use case

# Offline-First Patterns

-   **Cache-First**: Read from Isar first, fetch from network in background, update Isar on success
-   **Network-First**: Fetch from network, fall back to Isar on failure
-   **Write-Behind**: Write to Isar immediately, sync to server asynchronously (queue pending changes)
-   Always show cached data immediately while refreshing in background

# Reactive Queries

-   Use Isar's `watchLazy()` or `watch()` to stream changes to the UI via BLoC
-   Wrap Isar watch streams in the repository and expose as `Stream<List<DomainModel>>`
-   Dispose stream subscriptions properly in BLoC `close()` method

# Secure Storage

-   Use `flutter_secure_storage` for sensitive key-value data (tokens, encryption keys)
-   Use `SharedPreferences` ONLY for non-sensitive user preferences (theme, locale, onboarding flags)
-   NEVER store passwords, tokens, or secrets in `SharedPreferences` or plain Isar
