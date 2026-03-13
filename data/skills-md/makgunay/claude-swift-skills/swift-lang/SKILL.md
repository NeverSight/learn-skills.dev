---
name: swift-lang
description: Swift 6.2 language patterns and critical corrections for LLM code generation. Covers the concurrency paradigm shift (default MainActor isolation, @concurrent for background work, isolated conformances, nonisolated opt-out), @Observable vs ObservableObject, structured concurrency, modern error handling, property wrappers, InlineArray, Span, and value generics. Use whenever generating Swift code, especially async/concurrent code, class/struct design, or performance-critical paths. This skill prevents the most common LLM mistakes in Swift code generation.
---

# Swift 6.2 Language Patterns

Corrective guide for Swift code generation. Swift 6.2 fundamentally changed the concurrency model — most LLM training data reflects the old model.

## Critical Constraints

- ❌ DO NOT use `ObservableObject` + `@Published` for macOS 14+ / iOS 17+ → ✅ Use `@Observable` macro (import Observation)
- ❌ DO NOT use `@StateObject` → ✅ Use `@State` with `@Observable` classes
- ❌ DO NOT use `@ObservedObject` → ✅ Use `@Bindable` for bindings, or just pass the object
- ❌ DO NOT use `@EnvironmentObject` → ✅ Use `@Environment` with custom key
- ❌ DO NOT assume async functions always hop off the actor → ✅ In Swift 6.2, async functions run on the caller's actor by default
- ❌ DO NOT use `Task.detached` to get background execution → ✅ Use `@concurrent` attribute on the function
- ❌ DO NOT add `@Sendable` to everything to silence warnings → ✅ Use default MainActor isolation mode, opt out with `nonisolated`
- ❌ DO NOT use `DispatchQueue.main.async` for main thread work → ✅ Use `@MainActor` or `MainActor.run {}`
- ❌ DO NOT use `DispatchQueue.global().async` for background work → ✅ Use `@concurrent` functions with `await`
- ❌ DO NOT create `NavigationView` → ✅ Use `NavigationSplitView` or `NavigationStack`

## Decision Tree: Concurrency Model

```
Starting a new project or file?
├── Is this an app/script/executable target?
│   └── YES → Enable default MainActor isolation (recommended)
│         └── All code is @MainActor by default
│         └── No data-race errors for single-threaded code
│         └── Use nonisolated + @concurrent for background work
├── Is this a library/framework?
│   └── YES → Use explicit annotations (@MainActor, nonisolated, Sendable)
│
Need background execution?
├── Use @concurrent on the function
├── Mark the containing type as nonisolated
├── Add async to the function signature
└── Callers must await the result
```

## Decision Tree: Observable Pattern

```
Need observable state in a view?
├── macOS 14+ / iOS 17+ target?
│   ├── YES → Use @Observable macro
│   │   ├── View owns it? → @State private var model = MyModel()
│   │   ├── View receives it? → just use the parameter (no wrapper needed)
│   │   ├── Need binding? → @Bindable var model
│   │   └── Environment? → @Environment(MyModel.self) var model
│   └── NO (older targets) → Use ObservableObject + @Published
│       ├── View owns it? → @StateObject
│       ├── View receives it? → @ObservedObject
│       └── Environment? → @EnvironmentObject
```

## Verified Patterns

See `references/concurrency.md` for comprehensive Swift 6.2 concurrency patterns.
See `references/performance.md` for InlineArray, Span, and memory optimization.

### Pattern: @Observable Class (Modern)
<!-- Verified: macOS 14+, Swift 5.9+, Xcode 15+ -->
```swift
import SwiftUI
import Observation

@Observable
class StickerModel {
    var stickers: [Sticker] = []
    var isLoading = false

    func loadStickers() async {
        isLoading = true
        stickers = await StickerService.fetch()
        isLoading = false
    }
}

struct StickerListView: View {
    @State private var model = StickerModel()  // NOT @StateObject

    var body: some View {
        List(model.stickers) { sticker in
            StickerRow(sticker: sticker)
        }
        .task { await model.loadStickers() }
    }
}

// Passing to child — no wrapper needed
struct StickerRow: View {
    var sticker: Sticker  // plain property, NOT @ObservedObject
    var body: some View {
        Text(sticker.name)
    }
}

// When child needs to mutate
struct StickerEditor: View {
    @Bindable var model: StickerModel  // NOT @ObservedObject
    var body: some View {
        TextField("Name", text: $model.stickers[0].name)
    }
}
```

### Pattern: Environment with @Observable
<!-- Verified: macOS 14+, Swift 5.9+ -->
```swift
import SwiftUI

// Define environment key
struct AppModelKey: EnvironmentKey {
    static let defaultValue = AppModel()
}

extension EnvironmentValues {
    var appModel: AppModel {
        get { self[AppModelKey.self] }
        set { self[AppModelKey.self] = newValue }
    }
}

// Inject
@main
struct MyApp: App {
    @State private var appModel = AppModel()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.appModel, appModel)
        }
    }
}

// Consume
struct ContentView: View {
    @Environment(\.appModel) private var appModel
    var body: some View { /* use appModel */ }
}
```

### Pattern: Default MainActor Isolation (Swift 6.2)
<!-- Verified: Swift 6.2, Xcode 26 -->
```swift
// With default MainActor isolation enabled in build settings,
// everything is @MainActor by default. No annotations needed.

final class StickerLibrary {
    static let shared = StickerLibrary()  // Safe — implicitly @MainActor
    var stickers: [Sticker] = []           // Safe — on main actor
}

final class StickerModel {
    let photoProcessor = PhotoProcessor()

    func extractSticker(_ item: PhotosPickerItem) async throws -> Sticker? {
        guard let data = try await item.loadTransferable(type: Data.self) else {
            return nil
        }
        // No data-race error in Swift 6.2 — runs on caller's actor
        return await photoProcessor.extractSticker(data: data, with: item.itemIdentifier)
    }
}
```

### Pattern: @concurrent for Background Work
<!-- Verified: Swift 6.2, Xcode 26 -->
```swift
// To explicitly run work OFF the main actor, use @concurrent
nonisolated struct PhotoProcessor {
    @concurrent
    func process(data: Data) async -> ProcessedPhoto? {
        // This runs on the concurrent thread pool, NOT the main actor
        // Heavy image processing here
        return ProcessedPhoto(data: data)
    }
}

// Caller — must await
let processor = PhotoProcessor()
let result = await processor.process(data: imageData)
```

### Pattern: Isolated Conformances
<!-- Verified: Swift 6.2, Xcode 26 -->
```swift
protocol Exportable {
    func export()
}

// Mark the conformance as @MainActor — safe because compiler
// ensures it's only used on the main actor
extension StickerModel: @MainActor Exportable {
    func export() {
        photoProcessor.exportAsPNG()  // Can access MainActor state
    }
}

// This works — ImageExporter is also on MainActor
@MainActor
struct ImageExporter {
    var items: [any Exportable]
    mutating func add(_ item: StickerModel) {
        items.append(item)  // OK — same actor isolation
    }
}
```

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| `class MyModel: ObservableObject` with `@Published` | `@Observable class MyModel` — remove `@Published`, remove protocol |
| `@StateObject var model = MyModel()` | `@State private var model = MyModel()` |
| `@ObservedObject var model: MyModel` | `var model: MyModel` (or `@Bindable` for bindings) |
| `@EnvironmentObject var model: MyModel` | `@Environment(MyModel.self) var model` or custom key |
| `Task.detached { await heavy() }` | Mark `heavy()` as `@concurrent nonisolated` |
| `DispatchQueue.global().async { }` | `@concurrent func doWork() async { }` |
| `static let shared` causes Sendable warning | Enable default MainActor isolation, or add `@MainActor` |
| Adding `@Sendable` everywhere | Use actor isolation instead — `@MainActor` or explicit actors |
| `await MainActor.run { }` inside already-MainActor code | Just call directly — already on MainActor |

## Build Settings for Swift 6.2

Enable approachable concurrency in Xcode Build Settings → Swift Compiler - Concurrency:
- **Default Actor Isolation**: `MainActor` (infer @MainActor by default)
- **Strict Concurrency Checking**: `complete`

Or in Package.swift:
```swift
.target(
    name: "MyTarget",
    swiftSettings: [
        .defaultIsolation(MainActor.self)
    ]
)
```

## References

- [WWDC 2025: What's new in Swift](https://developer.apple.com/videos/play/wwdc2025/245/)
- [WWDC 2025: Improve memory usage and performance with Swift](https://developer.apple.com/videos/play/wwdc2025/312/)
- [Swift Migration Guide](https://swift.org/migration)
- [Observation framework](https://developer.apple.com/documentation/Observation)
