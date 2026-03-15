---
name: swiftdata
description: SwiftData persistence framework patterns for macOS and iOS apps. Covers @Model definitions, @Query, relationships (with delete rules), ModelContainer/ModelContext configuration, class inheritance with @Model subclasses, type-based predicates (#Predicate with is/as? casting), polymorphic relationships, @Attribute options (.preserveValueOnDeletion), schema migrations, and import/export. Use when implementing data persistence, defining models, querying data, or working with SwiftData. Prevents common LLM errors like generating Core Data syntax, inventing nonexistent SwiftData APIs, or misusing @Query.
---

# SwiftData Persistence Patterns

## Critical Constraints

- ❌ DO NOT use Core Data syntax (`NSManagedObject`, `NSFetchRequest`, `NSPredicate`) → ✅ Use `@Model`, `@Query`, `#Predicate`
- ❌ DO NOT use `@FetchRequest` → ✅ Use `@Query`
- ❌ DO NOT use string-based predicates → ✅ Use `#Predicate<ModelType>` macro with Swift expressions
- ❌ DO NOT create `NSPersistentContainer` → ✅ Use `ModelContainer` and `ModelContext`
- ❌ DO NOT forget `@Model` on subclasses → ✅ Both base class AND subclasses need `@Model`
- ❌ DO NOT use `@Model` on structs → ✅ `@Model` is for classes only

## Basic Model Definition
```swift
import SwiftData

@Model
class Trip {
    @Attribute(.preserveValueOnDeletion)
    var name: String
    var destination: String
    var startDate: Date
    var endDate: Date

    @Relationship(deleteRule: .cascade, inverse: \Accommodation.trip)
    var accommodation: Accommodation?

    init(name: String, destination: String, startDate: Date, endDate: Date) {
        self.name = name
        self.destination = destination
        self.startDate = startDate
        self.endDate = endDate
    }
}
```

## Class Inheritance

Both base and subclass need `@Model`. Subclass adds specialized properties.

```swift
@Model
class BusinessTrip: Trip {
    var purpose: String
    var expenseCode: String
    var perDiemRate: Double

    @Relationship(deleteRule: .cascade, inverse: \BusinessMeal.trip)
    var businessMeals: [BusinessMeal] = []

    init(name: String, destination: String, startDate: Date, endDate: Date,
         purpose: String, expenseCode: String, perDiemRate: Double) {
        self.purpose = purpose
        self.expenseCode = expenseCode
        self.perDiemRate = perDiemRate
        super.init(name: name, destination: destination, startDate: startDate, endDate: endDate)
    }
}

@Model
class PersonalTrip: Trip {
    enum Reason: String, CaseIterable, Codable, Identifiable {
        case family, vacation, wellness, other
        var id: Self { self }
    }
    var reason: Reason
    var notes: String?

    init(name: String, destination: String, startDate: Date, endDate: Date,
         reason: Reason, notes: String? = nil) {
        self.reason = reason
        self.notes = notes
        super.init(name: name, destination: destination, startDate: startDate, endDate: endDate)
    }
}
```

## Querying with Inheritance

```swift
// All trips (base + all subclasses)
@Query(sort: \Trip.startDate) var allTrips: [Trip]

// Filter by subclass type
let businessOnly = #Predicate<Trip> { $0 is BusinessTrip }
@Query(filter: businessOnly) var businessTrips: [Trip]

// Filter by subclass property
let vacations = #Predicate<Trip> {
    if let personal = $0 as? PersonalTrip {
        return personal.reason == .vacation
    }
    return false
}
```

## ModelContainer Setup
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: [Trip.self, BusinessTrip.self, PersonalTrip.self])
    }
}

// Custom configuration
let config = ModelConfiguration("MyStore", isStoredInMemoryOnly: false)
let container = try ModelContainer(for: Trip.self, configurations: config)
```

## CRUD Operations
```swift
// Create
let trip = Trip(name: "Paris", destination: "France", startDate: .now, endDate: .now)
modelContext.insert(trip)

// Read
let descriptor = FetchDescriptor<Trip>(sortBy: [SortDescriptor(\.startDate)])
let trips = try modelContext.fetch(descriptor)

// Update — just modify properties, SwiftData auto-saves
trip.name = "Paris 2025"

// Delete
modelContext.delete(trip)

// Save explicitly
try modelContext.save()
```

## Decision Tree: Inheritance vs Enum

```
Use inheritance when:
├── Clear IS-A relationship (BusinessTrip IS-A Trip)
├── Subclasses have significantly different properties
├── Need both deep queries (all trips) and shallow queries (business only)
└── Polymorphic relationships needed

Use enum/flag instead when:
├── Only a few shared properties
├── Distinction is simple (just a type tag)
├── Boolean flag suffices
└── Query strategy only focuses on specialized properties
```

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| `@Model struct MyData` | `@Model class MyData` — must be class |
| `NSPredicate(format:)` | `#Predicate<MyModel> { $0.name == "test" }` |
| Missing `@Model` on subclass | Add `@Model` to both base and subclass |
| `@FetchRequest` in SwiftUI | `@Query var items: [Item]` |
| Forgetting inverse on relationship | Add `inverse: \OtherModel.property` |
| Not registering subclasses in container | Include all model types in `.modelContainer(for:)` |

## References

- [SwiftData Documentation](https://developer.apple.com/documentation/SwiftData)
- [Adopting inheritance in SwiftData](https://developer.apple.com/documentation/SwiftData/Adopting-inheritance-in-SwiftData)
- [WWDC 2025: What's new in SwiftData](https://developer.apple.com/videos/play/wwdc2025/)
