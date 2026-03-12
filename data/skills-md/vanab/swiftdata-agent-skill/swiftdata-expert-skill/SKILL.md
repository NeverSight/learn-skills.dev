---
name: swiftdata-expert-skill
description: Expert guidance for designing, implementing, migrating, and debugging SwiftData persistence in Swift and SwiftUI apps. Use when working with @Model schemas, @Relationship/@Attribute rules, Query or FetchDescriptor data access, ModelContainer/ModelContext configuration, CloudKit sync, SchemaMigrationPlan/history APIs, ModelActor concurrency isolation, or Core Data to SwiftData adoption/coexistence.
---

# SwiftData Expert Skill

## Overview

Use this skill to build, review, and harden SwiftData persistence architecture with Apple-documented patterns from iOS 17 through current updates. Prioritize data integrity, migration safety, sync correctness, and predictable concurrency behavior.

## Agent Behavior Contract (Follow These Rules)

1. Identify the minimum deployment target before recommending APIs (notably `#Index`, `#Unique`, `HistoryDescriptor`, `DataStore`, inheritance examples).
2. Confirm the app has real `ModelContainer` wiring before debugging data issues; without it, inserts fail and fetches are empty.
3. Distinguish main-actor UI operations from background persistence operations; never assume one context fits both.
4. Treat schema changes as migration changes: evaluate lightweight migration first, then `SchemaMigrationPlan` when needed.
5. For CloudKit-enabled apps, verify schema compatibility constraints before proposing model changes.
6. Prefer deterministic query definitions (shared predicates, explicit sort order, bounded fetches) over ad hoc filtering in views.
7. Use persistent history tokens when reading cross-process changes; delete stale history to avoid storage growth.
8. In code reviews, prioritize data loss risk, accidental mass deletion, sync divergence, and context-isolation bugs over style changes.

## Analysis Commands (Use Early)

- Search container setup:
  - `rg "modelContainer\\(|ModelContainer\\(" -n`
- Search model definitions:
  - `rg "^@Model|#Unique|#Index|@Relationship|@Attribute|@Transient" -n`
- Search context usage:
  - `rg "modelContext|mainContext|ModelContext\\(" -n`
- Search migrations and history:
  - `rg "SchemaMigrationPlan|VersionedSchema|MigrationStage|fetchHistory|deleteHistory|historyToken" -n`
- Search CloudKit and app groups:
  - `rg "cloudKitDatabase|iCloud|CloudKit|groupContainer|AppGroup|NSPersistentCloudKitContainer" -n`

## Project Intake (Before Advising)

- Determine deployment targets: iOS, iPadOS, macOS, watchOS, and visionOS.
- Locate container setup: `.modelContainer(...)` modifier or manual `ModelContainer(...)`.
- Verify whether autosave is expected and whether explicit `save()` is required.
- Check if undo is enabled (`isUndoEnabled`) and whether operations occur on `mainContext` or custom contexts.
- Check CloudKit capabilities and chosen container strategy (`automatic`, `.private(...)`, `.none`).
- Check if app group storage is required.
- Check if Core Data coexistence is in scope.
- Check if schema changes must be backward-compatible with existing user data.

## Workflow Decision Tree

1. Need a new model or schema shape:
   - Read `references/modeling-and-schema.md`.
2. Need create, update, delete behavior or context correctness:
   - Read `references/model-context-and-lifecycle.md`.
3. Need filtering, sorting, or dynamic list behavior:
   - Read `references/querying-and-fetching.md`.
4. Need relationship modeling or inheritance:
   - Read `references/relationships-and-inheritance.md`.
5. Need migration planning, release upgrades, or change tracking:
   - Read `references/migrations-and-history.md`.
6. Need iCloud sync or CloudKit compatibility:
   - Read `references/cloudkit-sync.md`.
7. Need incremental migration from Core Data:
   - Read `references/core-data-adoption.md`.
8. Need background isolation or actor-based persistence:
   - Read `references/concurrency-and-actors.md`.
9. Need quick diagnostics or API availability checks:
   - Read `references/troubleshooting-and-updates.md`.
10. Need end-to-end execution playbook for a concrete task:
   - Read `references/implementation-playbooks.md`.

## Triage-First Playbook (Common Problems -> Next Move)

- Insert fails or fetch is always empty:
  - Confirm `.modelContainer(...)` is attached at app or window root and the model type is included.
- Duplicate rows appear after network refresh:
  - Add `@Attribute(.unique)` or `#Unique` constraints and rely on insert-upsert behavior.
- Unexpected data loss during delete:
  - Audit delete rules (`.cascade` vs `.nullify`) and check for unbounded `delete(model:where:)`.
- Undo or redo does nothing:
  - Ensure `isUndoEnabled: true` and that changes are saved via `mainContext` (not only background context).
- CloudKit sync not behaving:
  - Check capabilities, remote notifications, and CloudKit schema compatibility; explicitly set `cloudKitDatabase` if multiple containers exist.
- Widget or App Intent changes are not reflected:
  - Use persistent history (`fetchHistory`) with token + author filtering.
- `historyTokenExpired` appears:
  - Reset local token strategy and rebootstrap change consumption from a safe point.
- Query results are expensive or unstable:
  - Use shared predicate builders, explicit sorting, and bounded `FetchDescriptor` settings.

## Anti-Patterns (Reject by Default)

- Building persistence logic before validating container wiring.
- Performing broad deletes without predicate review and confirmation.
- Mixing UI-driven editing and background write pipelines without isolation boundaries.
- Relying on ad hoc in-memory filtering instead of store-backed predicates.
- Enabling CloudKit sync without capability setup and schema compatibility checks.
- Shipping schema changes without migration rehearsal on existing user data.
- Consuming history without token persistence and cleanup policy.

## Core Patterns

### App-level container wiring (SwiftUI)

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            RootView()
        }
        .modelContainer(for: [Trip.self, Accommodation.self])
    }
}
```

### Manual container configuration

```swift
let config = ModelConfiguration(isStoredInMemoryOnly: false)
let container = try ModelContainer(
    for: Trip.self,
    Accommodation.self,
    configurations: config
)
```

### Dynamic query setup in a view initializer

```swift
struct TripListView: View {
    @Query private var trips: [Trip]

    init(searchText: String) {
        let predicate = #Predicate<Trip> {
            searchText.isEmpty || $0.name.localizedStandardContains(searchText)
        }
        _trips = Query(filter: predicate, sort: \.startDate, order: .forward)
    }

    var body: some View { List(trips) { Text($0.name) } }
}
```

### Safe batch delete pattern

```swift
do {
    try modelContext.delete(
        model: Trip.self,
        where: #Predicate { $0.endDate < .now },
        includeSubclasses: true
    )
    try modelContext.save()
} catch {
    // Handle delete and save failures.
}
```

## Reference Files

- `references/modeling-and-schema.md`
- `references/model-context-and-lifecycle.md`
- `references/querying-and-fetching.md`
- `references/relationships-and-inheritance.md`
- `references/migrations-and-history.md`
- `references/cloudkit-sync.md`
- `references/core-data-adoption.md`
- `references/concurrency-and-actors.md`
- `references/troubleshooting-and-updates.md`
- `references/implementation-playbooks.md`

## Best Practices Summary

1. Keep model code as the source of truth; avoid hidden schema assumptions.
2. Apply explicit uniqueness and indexing strategy for large or frequently queried datasets.
3. Insert root models and let SwiftData traverse relationship graphs automatically.
4. Keep query behavior deterministic with explicit predicates and sort descriptors.
5. Bound fetches (`fetchLimit`, offsets, identifier-only fetches) for scalability.
6. Treat delete rules as business rules; review them during schema changes.
7. Use `ModelConfiguration` for environment-specific behavior (in-memory tests, CloudKit, app groups, read-only stores).
8. Handle history as an operational system: token persistence, filtering, and cleanup.
9. Use model actors or isolated contexts for non-UI persistence work.
10. Gate recommendations by API availability and deployment target.

## Verification Checklist (After Changes)

- Build succeeds for target platforms and minimum deployment versions.
- CRUD tests pass with real store and in-memory store.
- Relationship deletes behave as intended (`cascade`, `nullify`, and others).
- Query behavior is stable with realistic datasets and sort or filter combinations.
- Migration path is validated on pre-existing data (not only clean installs).
- CloudKit behavior is validated in a development container before release.
- Cross-process changes (widgets, intents, extensions) are observed correctly.
- Error paths and rollback behavior are covered for destructive operations.

## Response Contract

- For review tasks, report findings first by severity and include exact file paths and lines.
- For implementation tasks, describe:
  - container or context changes,
  - schema or migration changes,
  - query or performance changes,
  - verification steps run and any gaps.
- If deployment target blocks a recommended API, provide the best fallback compatible with the current target.
