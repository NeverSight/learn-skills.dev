---
name: creating-backstage-catalog-provider
description: Use when building a catalog backend module that ingests entities from an external source (e.g. Azure DevOps, internal API, JSON file). Covers both the normal EntityProvider and the IncrementalEntityProvider for large-volume sources, plus module wiring via catalogProcessingExtensionPoint or incrementalIngestionProvidersExtensionPoint. Triggers on phrases like "catalog provider", "ingest entities from X", "import entities from <source>", or "incremental ingestion".
---

# Creating a Backstage Catalog Provider

## When to use this skill

- Building a module that ingests catalog entities from an external source (Azure DevOps, GitHub topic search, internal asset registry, JSON file, etc.)
- Editing an existing `catalog-backend-module-*` plugin
- The ingestion runs periodically (provider model) — for one-shot processing of an entity definition file, write a `CatalogProcessor` instead

## What you build

A catalog provider is a backend module (`createBackendModule({ pluginId: 'catalog', ... })`) that registers a provider against an extension point. There are two provider models — pick based on data volume.

### Choose the model first: normal vs incremental

| Use **normal** `EntityProvider` when...                               | Use **`IncrementalEntityProvider`** when...                            |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Total entity count is small (~hundreds at most)                       | Total entity count is large (thousands+)                               |
| The full set fits in memory comfortably                               | Holding the full set in memory is impractical                          |
| The source returns the full snapshot in one round-trip (or a handful) | The source supports pagination — cursor / page-token / offset / etc.   |
| You're prototyping or building a POC                                  | You're shipping for production-scale catalogs                          |
| Refresh frequency is low                                              | High write rate or scale; incremental handles batching, backoff, retry |

The two models register against different extension points and have different runtime semantics:

- **Normal** registers against `catalogProcessingExtensionPoint` from `@backstage/plugin-catalog-node`. Adopters need no extra install.
- **Incremental** registers against `incrementalIngestionProvidersExtensionPoint` from `@backstage/plugin-catalog-backend-module-incremental-ingestion`. Adopters must also install `catalogModuleIncrementalIngestionEntityProvider` (the framework module that orchestrates batches and persists cursors via the catalog database).

If you don't know upfront, default to normal. Migrating to incremental later is mechanical — same domain fetch logic, different framework wiring.

If the data volume is genuinely unknown, ask the user. Rough thresholds: <500 entities → normal is fine; >10,000 → incremental is required; in between → ask about source pagination support and growth trajectory.

## Choose the right pattern

| Building...                                                       | Reference                                           |
| ----------------------------------------------------------------- | --------------------------------------------------- |
| A normal `EntityProvider` class (default for small/medium volume) | references/entity-provider.md (Normal section)      |
| An `IncrementalEntityProvider` class (large volume)               | references/entity-provider.md (Incremental section) |
| The module that wires either kind in                              | references/module-registration.md                   |

## Two invocation modes

- **Standalone**: editing an existing catalog-backend-module-\* plugin.
- **Post-scaffold** (called by `creating-backstage-plugin` for `catalog-provider-module`): scaffold both files together — provider class + module registration.

## Common gotchas

- The provider's `getProviderName()` must be unique across the catalog (same rule for both normal and incremental). Use a stable name — emitted entities are linked to the provider by it; renaming orphans them.
- **Normal provider:** `applyMutation({ type: 'full', entities })` replaces the whole set the provider owns. `applyMutation({ type: 'delta', added, removed })` adds/removes individual entries — useful when you only learn about changes incrementally. Note this is a _delta mutation_, not the same thing as the `IncrementalEntityProvider` model.
- **Normal provider:** the connection isn't available until `connect()` runs — guard `this.connection` against `undefined` in any method that might run before connect.
- **Normal provider:** don't fetch from an external system in `connect()` directly — receive a `SchedulerServiceTaskRunner` and call `this.schedule.run({ id, fn })` inside `connect()` so the work runs periodically and survives restarts.
- **Incremental provider:** the framework owns the iteration loop. Your `next(context, cursor?)` returns one page; the framework calls it repeatedly with the cursor you returned previously, and persists state in the catalog database. Don't try to schedule your own refresh.
- **Incremental provider:** adopters MUST install `catalogModuleIncrementalIngestionEntityProvider` (from `@backstage/plugin-catalog-backend-module-incremental-ingestion`) in addition to your module. Document this prerequisite in your module's README.
- `catalogProcessingExtensionPoint` comes from `@backstage/plugin-catalog-node` (the library package). `incrementalIngestionProvidersExtensionPoint` comes from `@backstage/plugin-catalog-backend-module-incremental-ingestion`. Don't depend on `@backstage/plugin-catalog-backend` from a module — that's the host plugin.
