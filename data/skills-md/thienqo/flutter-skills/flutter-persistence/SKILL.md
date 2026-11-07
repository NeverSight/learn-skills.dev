---
name: flutter-persistence
description: Design or review Flutter on-device persistence, caching, schema migrations, and offline synchronization. Use for preferences, files, local databases, cache lifecycle, or durable queues while preserving the existing package; route remote transport to flutter-networking and broad threat audits to flutter-security.
---

# Flutter Persistence

Choose storage from data shape, query needs, durability, sensitivity, synchronization, and migration requirements.

Before choosing APIs, inspect `pubspec.yaml`, SDK constraints, the resolved persistence package and version, generated-schema policy, existing storage owners, supported platforms, and tests. Preserve the established package unless a demonstrated requirement exceeds its supported contract.

## Select proportionately

- Use preferences only for small settings, not relational or critical domain data.
- Use files for document/blob ownership with explicit atomicity and cleanup.
- Use a database when queries, relationships, transactions, indexing, or migration justify it.
- Use platform secure storage for small secrets; do not treat ordinary app databases as secret vaults.
- Preserve an established package unless it cannot satisfy a concrete requirement.

## Model ownership

Define the source of truth, cache freshness, write ordering, conflict behavior, offline mutations, deletion semantics, and recovery from corrupt or incompatible data. Keep storage models behind repositories so schema details do not leak into widgets.

## Load references conditionally

- Read [caching policy](references/caching-policy.md) when choosing cache keys, freshness, invalidation, eviction, stale disclosure, or user isolation.
- Read [offline synchronization](references/offline-sync.md) when local and remote data can diverge, mutations queue offline, background work runs, or conflicts and deletions must reconcile.
- Read [schema migrations and recovery](references/schema-migrations-and-recovery.md) before changing a database schema, serialized durable format, migration callback, or incompatible-data recovery policy.

Route HTTP validators and transport caching to `flutter-networking`, and image, widget, scroll, or memory-cache performance to `flutter-performance`.

## Migration and safety

Classify stored state as durable user data, a durable operation, a disposable cache, or reproducible derived data before defining migration and recovery behavior. Version schemas and test every supported upgrade path from real prior-version artifacts. Never destroy durable user data as an automatic response to migration failure; rebuilding a disposable cache is valid only when its ownership and rebuild source are explicit. Avoid storing access tokens, passwords, or sensitive personal data in logs or plain preferences.

## Verification

Test first run, reopen, upgrade, failed write, concurrent access, corrupted data, deletion, and offline/online transitions relevant to the feature. Use temporary databases or directories for deterministic tests.

## Sources

- [Flutter persistence cookbook](https://docs.flutter.dev/cookbook/persistence)
- [Flutter offline-first support](https://docs.flutter.dev/app-architecture/design-patterns/offline-first)
