---
name: swiftdata-expert
description: Expert guidance for SwiftData on iOS 17+ and macOS 14+. Use when the user asks about SwiftData models, relationships, queries, predicates, ModelContext, ModelContainer, CloudKit sync, schema migrations, SwiftUI integration with @Query or @Bindable, performance optimization, testing with in-memory containers, or debugging silent save failures and crashes related to SwiftData.
---

# SwiftData Expert Skill

**Version:** 1.0.0  
**Target:** iOS 17+, macOS 14+, SwiftUI + SwiftData projects

## Agent Behavior Contract

1. **Triage first**: Use 60-second assessment before diving into code
2. **Route correctly**: Match problem to appropriate section
3. **Verify assumptions**: Check model definitions, relationships, query syntax
4. **Test incrementally**: Validate each change with diagnostics
5. **Document decisions**: Explain why specific patterns were chosen
6. **Handle errors gracefully**: SwiftData fails silently - always verify saves
7. **Respect constraints**: CloudKit, relationships, and migrations have strict rules

## First 60 Seconds Triage

When user reports SwiftData issue:

```
1. IDENTIFY SYMPTOM
   - Data not saving? → Check autosave, context, container setup
   - Crash on launch? → Model definition, relationship, migration issue
   - Query returns empty? → Predicate syntax, model registration
   - UI not updating? → @Query usage, observation, context
   - CloudKit sync failing? → Optional properties, unique constraints

2. LOCATE PROBLEM AREA
   - Models (01) → @Model, properties, initializers
   - Relationships (02) → @Relationship, delete rules, inverse
   - Queries (03) → @Query, #Predicate, FetchDescriptor
   - Context/Container (04) → ModelContext, ModelContainer, saves
   - SwiftUI Integration (05) → @Query, @Bindable, environment
   - Performance (06) → Batch operations, faulting, indexes
   - CloudKit (07) → Configuration, optional properties, sync

3. VERIFY BASICS
   - Is @Model applied to class?
   - Is modelContainer() in App struct?
   - Are relationships properly defined?
   - Is context being used correctly?
   - Are saves happening (autosave vs manual)?
```

## Routing Map

| User Says | Go To | Common Fixes |
|-----------|-------|--------------|
| "Data not persisting" | 04-context-saves.md | Enable autosave, call save() manually |
| "Crash with relationships" | 02-relationships.md | Add @Relationship, fix delete rules |
| "Query returns nothing" | 03-queries-predicates.md | Fix predicate syntax, check model registration |
| "UI not updating" | 05-swiftui-integration.md | Use @Query, check @Bindable |
| "CloudKit not syncing" | 07-cloudkit-sync.md | Make properties optional, remove @Attribute(.unique) |
| "Migration failed" | 08-migrations.md | Define migration plan, handle schema changes |
| "Performance issues" | 06-performance.md | Add batch operations, optimize queries |
| "Network data not saving" | 10-network-integration.md | Use MainActor for inserts, handle Codable |

## Common Errors → Next Best Move

```swift
// ERROR: "Circular reference resolving attached macro 'Relationship'"
// FIX: Only define @Relationship on ONE side of relationship

// ERROR: "illegal attempt to establish a relationship"
// FIX: Insert objects BEFORE manipulating relationship arrays

// ERROR: "Too many items in %{PROPERTY}@"
// FIX: Check maximumModelCount constraint, reduce array size

// ERROR: "validation recovery attempt FAILED"
// FIX: Non-optional property set to nil via relationship - make optional

// ERROR: Silent save failure
// FIX: Check CloudKit requirements (optional properties, no unique)

// ERROR: Network data not inserting
// FIX: Use MainActor.run for modelContext.insert after URLSession
```

## Quick Reference

### Model Definition
```swift
import SwiftData

@Model
class User {
    var name: String
    var age: Int
    var email: String?
    
    init(name: String, age: Int, email: String? = nil) {
        self.name = name
        self.age = age
        self.email = email
    }
}
```

### App Setup
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: User.self)
    }
}
```

### Query in SwiftUI
```swift
struct ContentView: View {
    @Query(sort: \User.name) var users: [User]
    @Environment(\.modelContext) var modelContext
    
    var body: some View {
        List(users) { user in
            Text(user.name)
        }
    }
}
```

### CRUD Operations
```swift
// Create
let user = User(name: "Alice", age: 30)
modelContext.insert(user)

// Update
user.name = "Alice Smith"

// Delete
modelContext.delete(user)

// Save (if autosave disabled)
try modelContext.save()
```

## Detailed Guides

- **[01-models-attributes.md](01-models-attributes.md)** - Model definitions, attributes, transformers
- **[02-relationships.md](02-relationships.md)** - One-to-one, one-to-many, many-to-many, delete rules
- **[03-queries-predicates.md](03-queries-predicates.md)** - @Query, #Predicate, FetchDescriptor, sorting, filtering
- **[04-context-saves.md](04-context-saves.md)** - ModelContext, ModelContainer, autosave, manual saves, undo/redo
- **[05-swiftui-integration.md](05-swiftui-integration.md)** - @Query, @Bindable, Observable objects, dynamic sorting/filtering
- **[06-performance.md](06-performance.md)** - Batch operations, concurrency, faulting, prefetching, indexes
- **[07-cloudkit-sync.md](07-cloudkit-sync.md)** - iCloud setup, requirements, troubleshooting
- **[08-migrations.md](08-migrations.md)** - Schema changes, migration plans, versioning
- **[09-testing-previews.md](09-testing-previews.md)** - In-memory containers, preview data, testing strategies
- **[10-network-integration.md](10-network-integration.md)** - URLSession, Codable, fetch/save, image handling, sync patterns

## Critical Rules

1. **Models must be classes** - Structs not supported
2. **@Model required** - Apply to all persistent classes
3. **Relationships need care** - Use @Relationship for explicit control
4. **CloudKit has strict rules** - Optional properties, no unique constraints
5. **Silent failures common** - Always verify saves, check constraints
6. **One container per app** - Usually sufficient, shared via environment
7. **Context = main actor** - Default context is @MainActor safe
8. **Migrations automatic** - For simple changes, complex needs MigrationPlan

## When to Use Each Pattern

| Pattern | Use When | Avoid When |
|---------|----------|------------|
| Inferred relationships | Simple optional relationships | Need explicit delete rules |
| @Relationship | Need delete rules, inverse control | Simple optional relationships |
| @Query | SwiftUI views, automatic updates | UIKit, manual control needed |
| FetchDescriptor | Complex queries, batch operations | Simple SwiftUI queries |
| Autosave | Most apps, simple workflows | Batch operations, transactions |
| Manual save | Batch operations, explicit control | Simple CRUD operations |
| In-memory | Testing, previews, temporary data | Production data persistence |
| CloudKit sync | Multi-device, backup | Local-only, complex sharing |

## Verification Checklist

Before marking task complete:

- [ ] Models have @Model macro
- [ ] App has modelContainer() modifier
- [ ] Relationships have proper delete rules
- [ ] Queries use correct predicate syntax
- [ ] Context is accessed via @Environment
- [ ] CloudKit requirements met (if syncing)
- [ ] Migrations defined (if schema changed)
- [ ] Previews use in-memory containers
- [ ] No silent save failures
- [ ] UI updates when data changes

## Resources

- Apple SwiftData Documentation
- WWDC23 Session 10187: Meet SwiftData
- WWDC23 Session 10195: Build an app with SwiftData
- SwiftData by Example (Paul Hudson)
- Community articles (see individual section files)
