---
name: swiftui-macos-performance
description: "SwiftUI performance on macOS — avoiding redundant redraws, EquatableView optimization, TimelineView, lazy containers with large datasets (Table 10k+ rows), Instruments for SwiftUI (Hangs, Time Profiler), MainActor hop cost, off-main rendering. Use when profiling or optimizing SwiftUI performance on macOS."
sources: https://developer.apple.com/documentation/swiftui/view-equatableview, https://developer.apple.com/documentation/xcode/identifying-responsiveness-issues-in-your-app, https://developer.apple.com/videos/play/wwdc2025/306/, https://developer.apple.com/videos/play/wwdc2025/266/, https://developer.apple.com/videos/play/wwdc2023/10248/, https://developer.apple.com/documentation/Xcode/understanding-and-improving-swiftui-performance, https://sosumi.ai/documentation/xcode/understanding-hangs-in-your-app, https://digitalblake.com/2026/04/28/swiftui-vs-appkit-macos-ui-performance/, https://useyourloaf.com/blog/swiftui-tasks-blocking-the-mainactor/, https://dkvekariya.medium.com/swiftui-performance-tuning-guide-2026-part-2-fd1ef785fbf7
researched: 2026-06-06
platform: macOS 26+
---

# SwiftUI Performance on macOS

SwiftUI performance tuning for macOS 26+ with Swift 6.3. Covers redundant redraw prevention, EquatableView optimization, lazy containers for large datasets, TimelineView scheduling, Instruments profiling (Hangs, Time Profiler, SwiftUI template), MainActor hop cost, off-main rendering, and view identity. For AppKit-level rendering control, see `swiftui-appkit-interop`. For Metal GPU profiling, see `macos-metal-gpu`.

See [references/performance-patterns.md](references/performance-patterns.md) for deep-dive patterns: EquatableView for expensive view subtrees, Table with 10k+ rows, reading Instruments Hangs traces, MainActor hop batching, and async image loading with cache.

## Contents

- [Redundant Redraw Prevention](#redundant-redraw-prevention)
- [EquatableView](#equatableview)
- [Lazy Containers](#lazy-containers)
- [TimelineView](#timelineview)
- [Instruments for SwiftUI](#instruments-for-swiftui)
- [MainActor Hop Cost](#mainactor-hop-cost)
- [Off-Main Rendering](#off-main-rendering)
- [View Identity](#view-identity)
- [Constraints & Gotchas](#constraints--gotchas)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Redundant Redraw Prevention

SwiftUI re-evaluates a view's body whenever the framework detects that the view's state has changed. The most common performance problem is triggering re-evaluations that don't produce visual changes.

**Triggers that cause body re-evaluation:**

| Trigger | Example | Cost |
|---------|---------|------|
| `@State` mutation | `counter += 1` inside a view | Re-evaluates the view and all non-equatable children |
| `@ObservedObject` / `@StateObject` change | An `@Published` property fires | Re-evaluates every subscriber |
| `@Observable` (macro) property read | Accessing a tracked property in body | Body re-runs when any accessed property changes |
| Environment value change | `.preferredColorScheme(.dark)` propagates | Re-evaluates the subtree |
| Parent body re-evaluation | Parent's state changes | All children re-evaluate unless identity or EquatableView blocks it |

**Key principle:** The cost isn't the SwiftUI body call itself — it's the diffing pass against the existing view tree and any resulting layout/rendering work. A body that returns the exact same view tree is cheap. A body that constructs new reference types, performs allocations, or triggers layout is expensive.

**Practical techniques:**

1. **Hoist state granularly.** Place `@State` as deep in the tree as possible. A `@State` at the root of a window causes the entire window content to re-evaluate.

2. **Use `@Observable` selectively.** The `@Observable` macro tracks individual property reads in `body`. A view that only reads `model.name` will not re-evaluate when `model.timestamp` changes. This is the single biggest improvement over `ObservableObject` for view-level granularity.

3. **Avoid constructing objects in `body`.** `MyView(data: DataObject())` creates a new `DataObject` every evaluation. Move construction to `init`, a static property, or a `@State` holder.

4. **Scope `.onChange(of:)` precisely.** Reacting to a high-frequency publisher at a wide scope propagates changes unnecessarily.

```swift
// BAD: Counter bump re-evaluates the entire ContentView body,
// including ExpensiveSidebar.
struct ContentView: View {
    @State private var counter = 0

    var body: some View {
        HStack {
            ExpensiveSidebar()           // re-evaluates every tap
            Button("Tap") { counter += 1 }
        }
    }
}

// GOOD: Isolate the mutable state.
struct ContentView: View {
    var body: some View {
        HStack {
            ExpensiveSidebar()
            TapButton()
        }
    }
}

struct TapButton: View {
    @State private var counter = 0
    var body: some View {
        Button("Tap") { counter += 1 }
    }
}
```

## EquatableView

`EquatableView` short-circuits body re-evaluation when the view's value hasn't changed. SwiftUI compares the new value to the old one using `==`; if equal, neither `body` evaluation nor the diffing pass occurs.

**Applying `.equatable()`:**

```swift
struct RowView: View, Equatable {
    let id: UUID
    let title: String
    let subtitle: String

    // SwiftUI calls this before evaluating body.
    // Return false to skip re-evaluation entirely.
    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.id == rhs.id &&
        lhs.title == rhs.title &&
        lhs.subtitle == rhs.subtitle
    }

    var body: some View {
        VStack(alignment: .leading) {
            Text(title).font(.headline)
            Text(subtitle).font(.caption)
        }
    }
}

// In a parent:
List(items) { item in
    RowView(id: item.id, title: item.title, subtitle: item.subtitle)
        .equatable()  // enables the == check
}
```

**When `.equatable()` helps:**

- **Expensive body:** The view's body performs significant computation or creates complex sub-trees.
- **Stable inputs:** The view's inputs don't change most of the time (e.g., a row in a list where only one row updates at a time).
- **Many siblings:** A `List` or `LazyVStack` with hundreds of items where only a few change per frame.

**When it doesn't help:**

- Simple views (a `Text` with a string) — the equality check costs more than re-evaluating.
- Views whose inputs change every frame (e.g., a progress indicator).
- Views with `inout` or `@Binding` parameters — `Equatable` can't see through reference types.

**For view structs (not the view itself):**

```swift
// Wrap a sub-tree to make it equatable:
struct ExpensiveChart: View {
    let dataPoints: [CGPoint]

    var body: some View {
        ChartSubtree(points: dataPoints)
            .guard { dataPoints.count > 0 }  // not equatable
    }
}

// Make the comparison data conform to Equatable and use EquatableView directly:
struct ExpensiveChart: View {
    let dataPoints: [CGPoint]

    var body: some View {
        EquatableView(ChartContent(dataPoints: dataPoints))
    }
}

struct ChartContent: View, Equatable {
    let dataPoints: [CGPoint]

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.dataPoints.count == rhs.dataPoints.count
        // Deep compare only when count changes, or use a hash.
    }

    var body: some View { /* expensive rendering */ }
}
```

**`EquatableView` vs `.equatable()`:** They are the same mechanism. `.equatable()` is syntactic sugar that wraps the view in `EquatableView`. Use `.equatable()` when the view itself conforms to `Equatable`. Use `EquatableView(_:)` directly when you want to wrap a different view type with a custom comparison.

## Lazy Containers

SwiftUI's non-lazy containers (`VStack`, `HStack`, `Grid`, `List`) materialize every child view immediately. With hundreds or thousands of items, this causes unacceptable launch-time and memory overhead.

**LazyVStack / LazyHStack:**

```swift
ScrollView {
    LazyVStack(spacing: 4) {
        ForEach(items) { item in
            RowView(item: item)
        }
    }
}
```

`LazyVStack` only materializes views that are visible on screen (plus a small buffer). As the user scrolls, views are created and destroyed. The memory footprint is proportional to the visible area, not the data set size.

**Critical:** `LazyVStack` calls `body` for each item as it scrolls into visibility, but it does **not** maintain item identity across scrolls unless you provide stable IDs in `ForEach`. Without stable IDs, scrolling an item out of view and back in can create a new view instance, losing state.

**Table with 10k+ rows:**
**Table with 50k+ rows (2026 research):** For extreme-scale tables, use a reference-type (class) data model instead of structs to avoid costly diffs. Pre-compute display values off-main, then assign sorted results in a single batch. Prefer direct key-path bindings (`TableColumn("Time", value: \.displayTime)`) over closure-based columns to reduce per-cell overhead. Specify fixed or bounded column widths to help layout. This pattern achieves ~60 FPS with 50k+ rows.
**LazyVGrid recycling (2026):** SwiftUI's `LazyVGrid`/`LazyHGrid` improve over `Grid`/`Stack` by lazily creating views, but do NOT aggressively reuse cells like AppKit's `NSCollectionView`. For 100k+ item collections, AppKit-backed `NSCollectionView` with diffable data sources remains superior for memory stability and smooth scrolling. Use SwiftUI lazy grids for moderate datasets (hundreds to low thousands).
**Nested ScrollView fix (2025):** Nested horizontal inside vertical `ScrollView` can trap scroll events on macOS. Fix: set `scrollView.usesPredominantAxisOnly = false` on the inner `NSScrollView` via `NSViewRepresentable`, or forward vertical delta events from the horizontal scroller to the vertical parent.

```swift
struct LargeTableView: View {
    @State private var items: [RowModel] = loadTenThousandRows()
    @State private var selection: Set<RowModel.ID> = []
    @State private var sortOrder = [KeyPathComparator(\RowModel.name)]

    var body: some View {
        Table(of: RowModel.self,
              selection: $selection,
              sortOrder: $sortOrder
        ) {
            TableColumn("Name", value: \.name) { item in
                Text(item.name)
                    .equatable()  // each column cell can be equatable
            }
            TableColumn("Size", value: \.size) { item in
                Text(ByteCountFormatter.string(fromByteCount: item.size, countStyle: .file))
                    .foregroundStyle(.secondary)
            }
            TableColumn("Modified", value: \.modified) { item in
                Text(item.modified, style: .date)
            }
        } rows: {
            ForEach(items) { item in
                TableRow(item)
                    .equatable()
            }
        }
        .tableStyle(.inset)
        .onChange(of: sortOrder) { _, newOrder in
            items.sort(using: newOrder)
        }
    }
}
```

Table uses lazy row materialization internally — only visible rows exist in memory. For 10k+ rows:

- **Row identity:** Each `RowModel` must have a stable, unique `ID` (use `Identifiable`). Table uses identity for selection state, diffing, and animation. Rowing with array indices as IDs causes selection to shift when rows are inserted/removed above.
- **Cell reuse:** Table internally reuses row views across scroll. Ensure your row content doesn't assume persistent view state outside of what's driven by the model.
- **Background loading:** Load data in a background task, then assign the array on the `@MainActor`:

```swift
func loadData() async {
    let rows = await Task.detached(priority: .userInitiated) {
        // parse files, read database, etc.
        return (0..<10_000).map { RowModel(index: $0) }
    }.value

    self.items = rows  // single assignment, single diff
}
```

- **Avoid incremental inserts.** Appending rows one at a time causes a diff-and-animate pass per insertion. Batch all rows into a single array assignment.
**Large table selection hang (2025):** Selecting a row in a `Table` with 1000+ rows can cause multi-second hangs. Instruments traces show time in `CFRunLoop` observers and SwiftUI view updates, not user code. Root cause: per-row `@Observable` property changes trigger cascading invalidations. Fix: reduce per-item state, batch updates, and avoid iterating all rows on every interaction. Even with minimal code, SwiftUI + CFRunLoop overhead contributes significantly.

**LazyVGrid:**

```swift
let columns = [GridItem(.adaptive(minimum: 150, maximum: 200), spacing: 8)]

ScrollView {
    LazyVGrid(columns: columns, spacing: 8) {
        ForEach(photoItems) { item in
            PhotoThumbnail(item: item)
        }
    }
    .padding()
}
```

## TimelineView

`TimelineView` schedules view updates on a timer, decoupling rendering from user interaction or data changes. It's the correct tool for clocks, progress indicators, and real-time data displays.

**`.animation` timeline:**

```swift
// Fires every frame (matching display refresh rate). Use for
// continuously animating content.
TimelineView(.animation) { context in
    let elapsed = context.date.timeIntervalSinceReferenceDate
    Canvas { gc, size in
        // Draw using elapsed time.
        let angle = elapsed.truncatingRemainder(dividingBy: 4) * .pi / 2
        gc.draw(gearShape, at: CGPoint(x: size.width/2, y: size.height/2))
    }
}
```

**`.periodic` timeline:**

```swift
// Fires at a fixed interval — every 3 seconds here.
TimelineView(.periodic(from: .now, by: 3)) { context in
    StatusIndicator(status: fetchStatus())
        .id(context.date)  // force refresh by identity
}
```

**`.explicit` timeline:**

```swift
// You control the schedule. Useful for choreographed animations
// or sparse updates.
let schedule = TimelineSchedule.explicit([
    Date().addingTimeInterval(1),
    Date().addingTimeInterval(3),
    Date().addingTimeInterval(7),
])

TimelineView(schedule) { context in
    StepIndicator(step: step(for: context.date))
}
```

**Pausing:**

Timelines automatically pause when the view is not visible. For macOS-specific pausing (app in background), use `.disabled(true)` or switch to a paused schedule:

```swift
@State private var isPaused = false

var body: some View {
    let schedule = isPaused
        ? TimelineSchedule.explicit([])
        : TimelineSchedule.animation

    TimelineView(schedule) { context in
        ClockFace(time: context.date)
    }
    .onReceive(NotificationCenter.default.publisher(for: NSApplication.didResignActiveNotification)) { _ in
        isPaused = true
    }
    .onReceive(NotificationCenter.default.publisher(for: NSApplication.didBecomeActiveNotification)) { _ in
        isPaused = false
    }
}
```

**Cost awareness:** `.animation` timeline fires at display refresh rate (60–120 Hz). Each firing re-evaluates the body. Keep the body lightweight — move complex computation outside the timeline closure or cache using `@State`.

## Instruments for SwiftUI

Xcode Instruments provides several templates for diagnosing SwiftUI performance:

| Instrument | What it shows | When to use |
|------------|---------------|-------------|
| **Hangs** | Main thread stalls and responsiveness issues | App feels janky or freezes intermittently |
| **Time Profiler** | CPU call stacks sampled over time | High CPU usage, slow operations |
| **Allocations** | Memory allocations and growth | Memory spikes, excessive allocation |
| **Leaks** | Memory leaks in Swift/ObjC | Growing memory over time |
| **SwiftUI** | View body evaluations, body duration, layout passes | Too many body evaluations, slow body, layout thrash |
| **Metal System Trace** | GPU timeline, draw calls, shader cost | GPU-bound rendering |
| **Energy Log** | CPU/GPU/network energy impact | Battery drain |

**Hangs instrument:**

The Hangs instrument on macOS shows main-thread stalls exceeding a threshold (default: renderLoop threshold). It captures the call stack at the moment a hang is detected. Key workflows:

1. Record a session while reproducing the sluggish behavior.
2. Switch to the "Hangs" track — each hang appears as a bar.
3. Select a hang to see the call stack. Look for SwiftUI body evaluation, layout, or your own long-running work on the main thread.
4. Filter by "Responsiveness" to differentiate input hogs from render stalls.

**SwiftUI instrument template:**

The SwiftUI template tracks:
- **View body number of updates:** How many times each view's body is evaluated. Views with disproportionately high counts are optimization targets.
- **View body duration:** Time spent in body evaluation. High duration = compute-heavy body.
- **Layout duration:** Time spent in SwiftUI layout.

Each row is a view type (by name). Sort by "Event Count" or "Average Duration" to find the hot spots.

**Allocations + SwiftUI together:**

Record with both the Allocations and SwiftUI templates. Correlate allocation spikes with view body evaluations to find views that allocate excessively (e.g., creating new `URL` or `DateFormatter` in every body pass).
**Instruments 26+ SwiftUI Instrument (WWDC25):** Xcode 26 introduces a dedicated SwiftUI instrument with four diagnostic lanes:
- **Update Groups** — Shows SwiftUI work being performed.
- **Long View Body Updates** — Flags views whose body takes too long.
- **Long Representable Updates** — Flags slow representable updates.
- **Other Long Updates** — Captures remaining long SwiftUI tasks.
Red/orange marks indicate hangs. Pair with Time Profiler and Hangs & Hitches for complete diagnosis. Profile with Release config — debug builds mask real performance.

## MainActor Hop Cost

SwiftUI runs on the main actor. Every `@Published` mutation, every `await MainActor.run {}`, and every `@State` write is a "hop" to the main actor. These hops are cheap individually (microseconds) but expensive in aggregate.

**Measuring hop cost:**

Use `OS_SIGNPOST` or `CFAbsoluteTimeGetCurrent()` around critical sections:

```swift
func processBatch(_ items: [Item]) {
    let start = CFAbsoluteTimeGetCurrent()

    for item in items {
        Task { @MainActor in
            self.items.append(item)  // one hop per item
        }
    }

    let elapsed = CFAbsoluteTimeGetCurrent() - start
    print("Hop cost: \(elapsed * 1000)ms for \(items.count) items")
}
```

**Batching main actor work:**

```swift
// BAD: N hops to the main actor for N items.
func addItems(_ newItems: [RowModel]) async {
    for item in newItems {
        await MainActor.run {
            self.items.append(item)  // each triggers diff + layout
        }
    }
}

// GOOD: One hop, one diff pass.
func addItems(_ newItems: [RowModel]) async {
    await MainActor.run {
        self.items.append(contentsOf: newItems)  // single diff
    }
}
```

**Nonisolated computation:**

Compute derived data off the main actor, then publish the final result:

```swift
@Observable
class DocumentViewModel {
    private(set) var items: [RowModel] = []
    private(set) var filteredItems: [RowModel] = []

    func updateFilter(_ query: String) async {
        let allItems = items  // capture on main actor
        let results = await Task.detached(priority: .userInitiated) {
            allItems.filter { $0.name.localizedCaseInsensitiveContains(query) }
        }.value

        self.filteredItems = results  // single main actor hop
    }
}
**@MainActor isolation in SwiftUI 2026:** The `View` protocol is now annotated `@MainActor` by default (Swift 6.2+). All synchronous work in `body` blocks the main thread if it exceeds ~16ms. Mark slow work as `nonisolated` or use `Task.detached(priority:)` for background execution. Blocking the MainActor (>100ms) leads to non-responsive UI — Instruments Hangs, not data races. Swift 6.2 can infer default actor isolation, simplifying cross-actor calls.
**Swift concurrency pattern for view models (2025):** If `ObservableObject` is `@MainActor`-isolated, all methods (including `async`) run on the main thread. Fix: refactored long-running work into `nonisolated` functions:
```swift
@MainActor
class Store: ObservableObject {
    @Published var results: [Item] = []
    func search(query: String) async {
        // Runs on MainActor — DON'T do heavy work here
        let items = await Task.detached(priority: .userInitiated) {
            return self.allItems.filter { $0.matches(query) }
        }.value
        self.results = results  // Back on MainActor for the state write
    }
}
```
```

## Off-Main Rendering

Some rendering work can move off the main thread to keep the main actor free for user interaction.

**Image rendering off main thread:**

```swift
func renderThumbnail(from image: NSImage, size: CGSize) async -> NSImage? {
    await Task.detached(priority: .userInitiated) {
        let rep = NSBitmapImageRep(
            bitmapDataPlanes: nil,
            pixelsWide: Int(size.width),
            pixelsHigh: Int(size.height),
            bitsPerSample: 8,
            samplesPerPixel: 4,
            hasAlpha: true,
            isPlanar: false,
            colorSpaceName: .deviceRGB,
            bytesPerRow: 0,
            bitsPerPixel: 0
        )!

        NSGraphicsContext.current?.imageInterpolation = .high
        NSGraphicsContext.saveGraphicsState()
        defer { NSGraphicsContext.restoreGraphicsState() }

        guard let ctx = NSGraphicsContext(bitmapImageRep: rep) else { return nil }
        NSGraphicsContext.current = ctx

        image.draw(in: NSRect(origin: .zero, size: size),
                   from: NSRect(origin: .zero, size: image.size),
                   operation: .copy,
                   fraction: 1.0)

        let thumbnail = NSImage(size: size)
        thumbnail.addRepresentation(rep)
        return thumbnail
    }.value
}
```

**Drawing to CGImage:**

```swift
func renderToCGImage(drawing: @escaping (CGContext, CGSize) -> Void, size: CGSize) -> CGImage? {
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    guard let context = CGContext(
        data: nil,
        width: Int(size.width),
        height: Int(size.height),
        bitsPerComponent: 8,
        bytesPerRow: 0,
        space: colorSpace,
        bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
    ) else { return nil }

    drawing(context, size)
    return context.makeImage()
}
```

**Async image loading:**

```swift
AsyncImage(url: url) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image.resizable()
    case .failure:
        Image(systemName: "exclamationmark.triangle")
    @unknown default:
        EmptyView()
    }
}
```

For custom caching, load the image in a `@Task` and store in an `@Observable` cache (see `references/performance-patterns.md`).

## View Identity

SwiftUI uses view identity to determine whether a view is the "same" view across updates. Correct identity enables animation, state preservation, and efficient diffing.

**Identity types:**

| Type | Mechanism | Use case |
|------|-----------|----------|
| **Structural identity** | Position in the view tree | Default — works for static layouts |
| **Explicit identity** | `.id(value)` modifier | When views can be reordered or their position shifts |
| **Stable model identity** | `Identifiable` + `ForEach` | Lists, tables, grids driven by data |

**`.id()` pitfalls:**

```swift
// BAD: New random identity every evaluation — view state resets every frame.
MyView().id(UUID())

// GOOD: Identity derived from stable model data.
MyView().id(item.id)

// BAD: Using array index as identity in a mutable collection.
ForEach(items.indices) { index in
    RowView(item: items[index])  // row at index 0 gets identity 0, but if row 0
                                 // is deleted, the content that WAS at index 1
                                 // (identity 1) gets reused for the new index 0.
}

// GOOD: Model-identity.
ForEach(items) { item in
    RowView(item: item)  // identity follows the model, survives reordering
}
```

**Structural identity vs explicit identity:** SwiftUI defaults to structural identity — the first child of a `VStack` always has identity "first child." This means:

- If you conditionally swap two views with the same type, SwiftUI reuses the view state (because the position hasn't changed). Use `.id()` to force a state reset.
- If you conditionally change the type of view at a position, SwiftUI destroys and recreates the view (different type = different identity at that position).
- `ForEach` with stable IDs gives you data-driven identity, which is almost always what you want.

## Constraints & Gotchas

- **SwiftUI Instruments template:** Available in Xcode's Instruments (not in Xcode's gauge overlays). The template requires macOS 14+ / iOS 16+. On earlier OS versions, use the blank instrument and add the `swiftui` signpost interval manually.
- **Hangs vs Time Profiler:** Hangs captures the *symptom* (main thread blocked) with high-fidelity call stacks at the exact stall point. Time Profiler samples CPU usage and is better for finding sustained CPU spikes. Use both together — Hangs tells you *where* the main thread is stuck, Time Profiler tells you *what* is consuming CPU.
- **EquatableView and `@Binding`:** `@Binding` is a reference type. Two `@Binding` wrappers wrapping the same property are *not* equal because the reference type's identity differs. If your view has `@Binding` inputs, `Equatable` will always return `false`, defeating the purpose. Split the view: hold the binding in a parent, pass only the current value to the equatable child.
- **Lazy container identity:** Lazy containers can recycle views. If your view has local `@State`, a recycled view may show stale state. Always drive visible state from the model.
- **TimelineView `.animation` cost:** Fires at display refresh rate in the background. Always paused in macOS apps when the window is occluded, but still fires when the window is visible. Don't use it for timers that should respect backgrounding — use `Timer.publish(every:)` with lifecycle notifications instead.
- **Table row height caching:** Table caches row heights. If row content changes height (e.g., dynamic text), call `tableColumnHeaders.forEach { $0.sizeToFit() }` or toggle `rowSizeCategory` to invalidate the cache.

## Common Mistakes

1. **Measuring performance in debug builds.** SwiftUI body evaluation is significantly slower in debug (no optimizations, no inlining). Always profile with Release configuration (`Product > Scheme > Edit Scheme > Run > Build Configuration: Release`).

2. **Excessive `.id()` usage.** `.id(UUID())` on every view in a list defeats SwiftUI's diffing and causes full recreation. Use stable, meaningful IDs.

3. **Creating objects in view body.** `Text(DateFormatter.mapStyle.string(from: date))` creates a `DateFormatter` every evaluation. Cache it: `private static let formatter: DateFormatter = { ... }()`.

4. **Ignoring `@Observable` migration.** Views that observe `ObservableObject` with `@Published` properties re-evaluate when *any* `@Published` property changes. `@Observable` tracks individual property reads — migrating gives free granularity.

5. **Using `List` for large macOS tables.** On macOS, `Table` is purpose-built for tabular data with column sorting, reordering, and `NSTableColumn` integration. `List` with `ForEach` wrapping `HStack`-based rows has higher overhead for multi-column data.

6. **GCD instead of structured concurrency for background work.** DispatchQueue-scheduled work that updates `@State` requires `DispatchQueue.main.async { ... }`, which is harder to batch and reason about than `nonisolated` functions with a single `MainActor.run { ... }` at the end.

7. **Not testing with real dataset sizes.** Performance issues with 1k rows may be invisible with 100. Always test with production-scale data or larger.

## Review Checklist

Before shipping performance-critical SwiftUI code:

- [ ] No object allocations in `body` (DateFormatter, URL, Data created inline)
- [ ] `@State` placed at the deepest possible scope
- [ ] `ForEach` uses model identity, not array indices
- [ ] Large lists/tables use lazy containers or `Table`
- [ ] Expensive view subtrees use `.equatable()`
- [ ] Background computation uses `Task.detached` or `nonisolated`, not DispatchQueue
- [ ] Main actor hops batched (single assignment, not per-item)
- [ ] Instruments Hangs trace shows no stalls > 16ms on main thread
- [ ] SwiftUI instrument shows body evaluation counts proportional to actual changes
- [ ] Profile done in Release configuration

## References
- [Identifying Responsiveness Issues in Your App](https://developer.apple.com/documentation/xcode/identifying-responsiveness-issues-in-your-app) — Apple Docs
- [View.equatable()](https://developer.apple.com/documentation/swiftui/view-equatableview) — Apple Docs
- [TimelineView](https://developer.apple.com/documentation/swiftui/timelineview) — Apple Docs
- [LazyVStack](https://developer.apple.com/documentation/swiftui/lazyvstack) — Apple Docs
- [LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid) — Apple Docs
- [Instruments User Guide](https://help.apple.com/instruments/mac/current/) — Apple Docs
- [Understanding and improving SwiftUI performance](https://developer.apple.com/documentation/Xcode/understanding-and-improving-swiftui-performance) — Apple Docs
- [Optimize SwiftUI performance with Instruments - WWDC25](https://developer.apple.com/videos/play/wwdc2025/306/) — Apple WWDC
- [Explore concurrency in SwiftUI - WWDC25](https://developer.apple.com/videos/play/wwdc2025/266/) — Apple WWDC
- [Analyze hangs with Instruments - WWDC23](https://developer.apple.com/videos/play/wwdc2023/10248/) — Apple WWDC
- [SwiftUI Tasks Blocking MainActor](https://useyourloaf.com/blog/swiftui-tasks-blocking-the-mainactor/) — Use Your Loaf
- [Using Instruments to Profile SwiftUI](https://www.hackingwithswift.com/quick-start/swiftui/how-to-use-instruments-to-profile-your-swiftui-code-and-identify-slow-layouts) — Hacking with Swift
- [Performance Tuning Guide 2026 (Part 2)](https://dkvekariya.medium.com/swiftui-performance-tuning-guide-2026-part-2-fd1ef785fbf7) — Medium
- For deep-dive patterns, see [references/performance-patterns.md](references/performance-patterns.md)
