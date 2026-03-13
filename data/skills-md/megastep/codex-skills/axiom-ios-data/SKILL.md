---
name: axiom-ios-data
description: Use when working with ANY data persistence, database, axiom-storage, CloudKit, migration, or serialization. Covers SwiftData, Core Data, GRDB, SQLite, CloudKit sync, file storage, Codable, migrations.
license: MIT
---

# iOS Data & Persistence Router

**You MUST use this skill for ANY data persistence, database, axiom-storage, CloudKit, or serialization work.**

## When to Use

Use this router when working with:
- Databases (SwiftData, Core Data, GRDB, SQLiteData)
- Schema migrations
- CloudKit sync
- File storage (iCloud Drive, local storage)
- Data serialization (Codable, JSON)
- Storage strategy decisions

## Routing Logic

### SwiftData

**Working with SwiftData** → `$axiom-swiftdata`
**Schema migration** → `$axiom-swiftdata-migration`
**Migration issues** → `$axiom-swiftdata-migration-diag`
**Migrating from Realm** → `$axiom-realm-migration-ref`
**SwiftData vs SQLiteData** → `$axiom-sqlitedata-migration`

### Other Databases

**GRDB queries** → `$axiom-grdb`
**SQLiteData** → `$axiom-sqlitedata`
**Advanced SQLiteData** → `$axiom-sqlitedata-ref`
**Core Data patterns** → `$axiom-core-data`
**Core Data issues** → `$axiom-core-data-diag`

### Migrations

**Database migration safety** → `$axiom-database-migration` (critical - prevents data loss)

### Serialization

**Codable issues** → `$axiom-codable`

### Cloud Storage

**Cloud sync patterns** → `$axiom-cloud-sync`
**CloudKit** → `$axiom-cloudkit-ref`
**iCloud Drive** → `$axiom-icloud-drive-ref`
**Cloud sync errors** → `$axiom-cloud-sync-diag`

### File Storage

**Storage strategy** → `$axiom-storage`
**Storage issues** → `$axiom-storage-diag`
**Storage management** → `$axiom-storage-management-ref`
**File protection** → `$axiom-file-protection-ref`

### tvOS Storage

**tvOS data persistence** → `$axiom-tvos` (CRITICAL: no persistent local storage on tvOS)
**tvOS + CloudKit** → `$axiom-sqlitedata` (recommended: SyncEngine as persistent store)

### Automated Scanning

**Core Data audit** → Launch `core-data-auditor` agent or `/axiom:audit core-data` (migration risks, thread-confinement, N+1 queries, production data loss)
**Codable audit** → Launch `codable-auditor` agent or `/axiom:audit codable` (try? swallowing errors, JSONSerialization, date handling)
**iCloud audit** → Launch `icloud-auditor` agent or `/axiom:audit icloud` (entitlement checks, file coordination, CloudKit anti-patterns)
**Storage audit** → Launch `storage-auditor` agent or `/axiom:audit storage` (wrong file locations, missing backup exclusions, data loss risks)

## Decision Tree

1. SwiftData? → swiftdata, swiftdata-migration
2. Core Data? → core-data, core-data-diag
3. GRDB? → grdb
4. SQLiteData? → sqlitedata, sqlitedata-ref
5. ANY schema migration? → database-migration (ALWAYS — prevents data loss)
6. Realm migration? → realm-migration-ref
7. SwiftData vs SQLiteData? → sqlitedata-migration
8. Cloud sync architecture? → cloud-sync
9. CloudKit? → cloudkit-ref
10. iCloud Drive? → icloud-drive-ref
11. Cloud sync errors? → cloud-sync-diag
12. Codable/JSON serialization? → codable
13. File storage strategy? → storage, storage-diag, storage-management-ref
14. File protection? → file-protection-ref
15. Want Core Data safety scan? → core-data-auditor (Agent)
16. Want Codable anti-pattern scan? → codable-auditor (Agent)
17. Want iCloud sync audit? → icloud-auditor (Agent)
18. Want storage location audit? → storage-auditor (Agent)
19. tvOS data persistence? → axiom-tvos (CRITICAL: no persistent local storage) + axiom-sqlitedata (CloudKit SyncEngine)

## Anti-Rationalization

| Thought | Reality |
|---------|---------|
| "Just adding a column, no migration needed" | Schema changes without migration crash users. database-migration prevents data loss. |
| "I'll handle the migration manually" | Manual migrations miss edge cases. database-migration covers rollback and testing. |
| "Simple query, I don't need the skill" | Query patterns prevent N+1 and thread-safety issues. The skill has copy-paste solutions. |
| "CloudKit sync is straightforward" | CloudKit has 15+ failure modes. cloud-sync-diag diagnoses them systematically. |
| "I know Codable well enough" | Codable has silent data loss traps (try? swallows errors). codable skill prevents production bugs. |
| "I'll use local storage on tvOS" | tvOS has NO persistent local storage. System deletes Caches at any time. axiom-tvos explains the iCloud-first pattern. |

## Critical Pattern: Migrations

**ALWAYS invoke `$axiom-database-migration` when adding/modifying database columns.**

This prevents:
- "FOREIGN KEY constraint failed" errors
- "no such column" crashes
- Data loss from unsafe migrations

## Example Invocations

User: "I need to add a column to my SwiftData model"
→ Invoke: `$axiom-database-migration` (critical - prevents data loss)

User: "How do I query SwiftData with complex filters?"
→ Invoke: `$axiom-swiftdata`

User: "CloudKit sync isn't working"
→ Invoke: `$axiom-cloud-sync-diag`

User: "Should I use SwiftData or SQLiteData?"
→ Invoke: `$axiom-sqlitedata-migration`

User: "Check my Core Data code for safety issues"
→ Invoke: `core-data-auditor` agent

User: "Scan for Codable anti-patterns before release"
→ Invoke: `codable-auditor` agent

User: "Audit my iCloud sync implementation"
→ Invoke: `icloud-auditor` agent

User: "Check if my files are stored in the right locations"
→ Invoke: `storage-auditor` agent

User: "How do I persist data on tvOS?"
→ Invoke: `$axiom-tvos` + `$axiom-sqlitedata`

User: "My tvOS app loses data between launches"
→ Invoke: `$axiom-tvos`
