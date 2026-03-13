---
name: swift-macos
description: Comprehensive macOS app development with Swift 6.2, SwiftUI, SwiftData, Swift Concurrency, Foundation Models, Swift Testing, ScreenCaptureKit, and app distribution. Use when building native Mac apps, implementing windows/scenes/navigation/menus/toolbars, persisting data with SwiftData (@Model, @Query, #Predicate, ModelContainer), writing concurrent code (async/await, actors, @concurrent, default MainActor isolation, Sendable), using on-device AI (Foundation Models), testing with Swift Testing, capturing screen/audio with ScreenCaptureKit, recording audio with AVFoundation, building menu bar apps, monitoring processes, registering login items, bridging AppKit, or distributing via App Store/Developer ID/notarization. Triggers on macOS app, Mac app, SwiftUI macOS, Swift macOS, SwiftData, @Model, @Query, Swift concurrency, async await, actor isolation, @MainActor, @concurrent, Sendable, Foundation Models, Swift Testing, notarize, MenuBarExtra, NSViewRepresentable, ScreenCaptureKit, SCStream, SCShareableContent, screen capture, screen recording, audio capture, AVAssetWriter, AVAudioFile, SMAppService, login item, LSUIElement, NSWorkspace, process monitoring.
metadata:
  version: "0.2.0"
---

# macOS App Development - Swift 6.2

Build native macOS apps with Swift 6.2 (latest: 6.2.4, Feb 2026), SwiftUI, SwiftData, and macOS 26 Tahoe. Target macOS 14+ for SwiftData/@Observable, macOS 15+ for latest SwiftUI, macOS 26 for Liquid Glass and Foundation Models.

## Quick Start

```swift
import SwiftUI
import SwiftData

@Model
final class Project {
    var name: String
    var createdAt: Date
    @Relationship(deleteRule: .cascade) var tasks: [Task] = []

    init(name: String) {
        self.name = name
        self.createdAt = .now
    }
}

@Model
final class Task {
    var title: String
    var isComplete: Bool
    var project: Project?

    init(title: String) {
        self.title = title
        self.isComplete = false
    }
}

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup("Projects") {
            ContentView()
        }
        .modelContainer(for: [Project.self, Task.self])
        .defaultSize(width: 900, height: 600)

        #if os(macOS)
        Settings { SettingsView() }

        MenuBarExtra("Status", systemImage: "circle.fill") {
            MenuBarView()
        }
        .menuBarExtraStyle(.window)
        #endif
    }
}

struct ContentView: View {
    @Query(sort: \Project.createdAt, order: .reverse)
    private var projects: [Project]

    @Environment(\.modelContext) private var context
    @State private var selected: Project?

    var body: some View {
        NavigationSplitView {
            List(projects, selection: $selected) { project in
                NavigationLink(value: project) {
                    Text(project.name)
                }
            }
            .navigationSplitViewColumnWidth(min: 200, ideal: 250)
        } detail: {
            if let selected {
                DetailView(project: selected)
            } else {
                ContentUnavailableView("Select a Project",
                    systemImage: "sidebar.left")
            }
        }
    }
}
```

## Scenes & Windows

| Scene | Purpose |
|-------|---------|
| `WindowGroup` | Resizable windows (multiple instances) |
| `Window` | Single-instance utility window |
| `Settings` | Preferences (Cmd+,) |
| `MenuBarExtra` | Menu bar with `.menu` or `.window` style |
| `DocumentGroup` | Document-based apps |

Open windows: `@Environment(\.openWindow) var openWindow; openWindow(id: "about")`

For complete scene lifecycle, see `references/app-lifecycle.md`.

## Menus & Commands

```swift
.commands {
    CommandGroup(replacing: .newItem) {
        Button("New Project") { /* ... */ }
            .keyboardShortcut("n", modifiers: .command)
    }
    CommandMenu("Tools") {
        Button("Run Analysis") { /* ... */ }
            .keyboardShortcut("r", modifiers: [.command, .shift])
    }
}
```

## Table (macOS-native)

```swift
Table(items, selection: $selectedIDs, sortOrder: $sortOrder) {
    TableColumn("Name", value: \.name)
    TableColumn("Date") { Text($0.date, format: .dateTime) }
        .width(min: 100, ideal: 150)
}
.contextMenu(forSelectionType: Item.ID.self) { ids in
    Button("Delete", role: .destructive) { delete(ids) }
}
```

For forms, popovers, sheets, inspector, and macOS modifiers, see `references/swiftui-macos.md`.

## @Observable

```swift
@Observable
final class AppState {
    var projects: [Project] = []
    var isLoading = false

    func load() async throws {
        isLoading = true
        defer { isLoading = false }
        projects = try await ProjectService.fetchAll()
    }
}

// Use: @State var state = AppState()          (owner)
// Pass: .environment(state)                    (inject)
// Read: @Environment(AppState.self) var state  (child)
```

## SwiftData

### @Query & #Predicate

```swift
@Query(filter: #Predicate<Project> { !$0.isArchived }, sort: \Project.name)
private var active: [Project]

// Dynamic predicate
func search(_ term: String) -> Predicate<Project> {
    #Predicate { $0.name.localizedStandardContains(term) }
}

// FetchDescriptor (outside views)
var desc = FetchDescriptor<Project>(predicate: #Predicate { $0.isArchived })
desc.fetchLimit = 50
let results = try context.fetch(desc)
let count = try context.fetchCount(desc)
```

### Relationships

```swift
@Model final class Author {
    var name: String
    @Relationship(deleteRule: .cascade, inverse: \Book.author)
    var books: [Book] = []
}

@Model final class Book {
    var title: String
    var author: Author?
    @Relationship var tags: [Tag] = []  // many-to-many
}
```

Delete rules: `.cascade`, `.nullify` (default), `.deny`, `.noAction`.

### Schema Migration

```swift
enum SchemaV1: VersionedSchema { /* ... */ }
enum SchemaV2: VersionedSchema { /* ... */ }

enum MigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] { [SchemaV1.self, SchemaV2.self] }
    static var stages: [MigrationStage] {
        [.lightweight(fromVersion: SchemaV1.self, toVersion: SchemaV2.self)]
    }
}

// Apply: .modelContainer(for: Model.self, migrationPlan: MigrationPlan.self)
```

### CloudKit Sync

Enable iCloud capability, then `.modelContainer(for: Model.self)` auto-syncs. Constraints: all properties need defaults/optional, no unique constraints, optional relationships.

For model attributes, background contexts, batch ops, undo/redo, and testing, see SwiftData references below.

## Concurrency (Swift 6.2)

### Default MainActor Isolation

Opt entire module into main actor - all code runs on main actor by default:

```swift
// Package.swift
.executableTarget(name: "MyApp", swiftSettings: [
    .defaultIsolation(MainActor.self),
])
```

Or Xcode: Build Settings > Swift Compiler > Default Isolation > MainActor.

### @concurrent

Mark functions for background execution:

```swift
@concurrent
func processFile(_ url: URL) async throws -> Data {
    let data = try Data(contentsOf: url)
    return try compress(data) // runs off main actor
}
// After await, automatically back on main actor
let result = try await processFile(fileURL)
```

Use for CPU-intensive work, I/O, anything not touching UI.

### Actors

```swift
actor DocumentStore {
    private var docs: [UUID: Document] = [:]
    func add(_ doc: Document) { docs[doc.id] = doc }
    func get(_ id: UUID) -> Document? { docs[id] }
    nonisolated let name: String
}
// Requires await: let doc = await store.get(id)
```

### Structured Concurrency

```swift
// Parallel with async let
func loadDashboard() async throws -> Dashboard {
    async let profile = fetchProfile()
    async let stats = fetchStats()
    return try await Dashboard(profile: profile, stats: stats)
}

// Dynamic with TaskGroup
func processImages(_ urls: [URL]) async throws -> [NSImage] {
    try await withThrowingTaskGroup(of: (Int, NSImage).self) { group in
        for (i, url) in urls.enumerated() {
            group.addTask { (i, try await loadImage(url)) }
        }
        var results = [(Int, NSImage)]()
        for try await r in group { results.append(r) }
        return results.sorted { $0.0 < $1.0 }.map(\.1)
    }
}
```

### Sendable

```swift
struct Point: Sendable { var x, y: Double }              // value types: implicit
final class Config: Sendable { let apiURL: URL }          // final + immutable
actor SharedState { var count = 0 }                       // mutable: use actors
// Enable strict mode: .swiftLanguageMode(.v6) in Package.swift
```

### AsyncSequence & Observations

```swift
// Stream @Observable changes (Swift 6.2)
for await state in Observations(of: manager) {
    print(state.progress)
}

// Typed NotificationCenter (Swift 6.2)
struct DocSaved: MainActorMessage { let id: UUID }
NotificationCenter.default.post(DocSaved(id: doc.id))
for await n in NotificationCenter.default.notifications(of: DocSaved.self) {
    refresh(n.id)
}
```

For concurrency deep dives, see concurrency references below.

## Foundation Models (macOS 26+)

On-device ~3B LLM. Free, offline, private:

```swift
import FoundationModels

let session = LanguageModelSession()
let response = try await session.respond(to: "Summarize: \(text)")

// Structured output
@Generable struct Summary { var title: String; var points: [String] }
let result: Summary = try await session.respond(to: prompt, generating: Summary.self)
```

For tool calling, streaming, and sessions, see `references/foundation-models.md`.

## Testing

```swift
import Testing

@Suite("Project Tests")
struct ProjectTests {
    @Test("creates with defaults")
    func create() {
        let p = Project(name: "Test")
        #expect(p.name == "Test")
    }

    @Test("formats sizes", arguments: [(1024, "1 KB"), (0, "0 KB")])
    func format(bytes: Int, expected: String) {
        #expect(formatSize(bytes) == expected)
    }
}

// SwiftData testing
let container = try ModelContainer(
    for: Project.self,
    configurations: ModelConfiguration(isStoredInMemoryOnly: true)
)
let ctx = ModelContext(container)
ctx.insert(Project(name: "Test"))
try ctx.save()
```

For exit tests, attachments, UI testing, see `references/testing.md`.

## Distribution

| Method | Sandbox | Notarization | Review |
|--------|---------|--------------|--------|
| App Store | Required | Automatic | Yes |
| Developer ID | Recommended | Required | No |
| Ad-Hoc | No | No | Local only |

```bash
xcodebuild archive -scheme MyApp -archivePath MyApp.xcarchive
xcodebuild -exportArchive -archivePath MyApp.xcarchive \
  -exportPath ./export -exportOptionsPlist ExportOptions.plist
xcrun notarytool submit ./export/MyApp.dmg \
  --apple-id you@example.com --team-id TEAM_ID \
  --password @keychain:AC_PASSWORD --wait
xcrun stapler staple ./export/MyApp.dmg
```

For complete distribution guide, see `references/distribution.md`.

## SPM

```swift
// swift-tools-version: 6.2
let package = Package(
    name: "MyApp",
    platforms: [.macOS(.v14)],
    targets: [
        .executableTarget(name: "MyApp", swiftSettings: [
            .swiftLanguageMode(.v6),
            .defaultIsolation(MainActor.self),
        ]),
        .testTarget(name: "MyAppTests", dependencies: ["MyApp"]),
    ]
)
```

For build plugins, macros, and Swift Build, see `references/spm-build.md`.

## Liquid Glass (macOS 26)

Apps rebuilt with Xcode 26 SDK get automatic Liquid Glass styling. Use `.glassEffect()` for custom glass surfaces, `GlassEffectContainer` for custom hierarchies. Opt out: `UIDesignRequiresLiquidGlass = NO` in Info.plist.

## ScreenCaptureKit

Capture screen content, app audio, and microphone (macOS 12.3+):

```swift
import ScreenCaptureKit

let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: true)
guard let display = content.displays.first else { return }

// Filter: specific apps only
let filter = SCContentFilter(display: display, including: [targetApp], exceptingWindows: [])

// Configure
let config = SCStreamConfiguration()
config.capturesAudio = true
config.sampleRate = 48000
config.channelCount = 2
config.excludesCurrentProcessAudio = true

// Audio-only: minimize video overhead
config.width = 2; config.height = 2
config.minimumFrameInterval = CMTime(value: 1, timescale: CMTimeScale.max)

let stream = SCStream(filter: filter, configuration: config, delegate: self)
try stream.addStreamOutput(self, type: .screen, sampleHandlerQueue: nil)
try stream.addStreamOutput(self, type: .audio, sampleHandlerQueue: audioQueue)
try await stream.startCapture()
```

macOS 15+: `SCRecordingOutput` for simplified file recording, `config.captureMicrophone` for mic capture. macOS 14+: `SCContentSharingPicker` for system picker UI, `SCScreenshotManager` for single-frame capture.

For complete API reference, audio writing (AVAssetWriter/AVAudioFile), permissions, and examples, see `references/screen-capture-audio.md`.

## AppKit Interop

```swift
struct WebViewWrapper: NSViewRepresentable {
    let url: URL
    func makeNSView(context: Context) -> WKWebView { WKWebView() }
    func updateNSView(_ v: WKWebView, context: Context) {
        v.load(URLRequest(url: url))
    }
}
```

For hosting SwiftUI in AppKit and advanced bridging, see `references/appkit-interop.md`.

## Architecture

| Pattern | Best For | Complexity |
|---------|----------|------------|
| SwiftUI + @Observable | Small-medium, solo | Low |
| MVVM + @Observable | Medium, teams | Medium |
| TCA | Large, strict testing | High |

See `references/architecture.md` for all patterns with examples.

## References

| File | When to read |
|------|-------------|
| **SwiftUI & macOS** | |
| `references/app-lifecycle.md` | Window management, scenes, DocumentGroup, MenuBarExtra |
| `references/swiftui-macos.md` | Sidebar, Inspector, Table, forms, popovers, sheets, search |
| `references/appkit-interop.md` | NSViewRepresentable, hosting controllers, AppKit bridging |
| `references/screen-capture-audio.md` | ScreenCaptureKit, SCStream, audio capture, AVAssetWriter, permissions |
| `references/system-integration.md` | Keyboard shortcuts, drag & drop, file access, App Intents, process monitoring, login items, LSUIElement |
| `references/foundation-models.md` | On-device AI: guided generation, tool calling, streaming |
| `references/architecture.md` | MVVM, TCA, dependency injection, project structure |
| `references/testing.md` | Swift Testing, exit tests, attachments, UI testing, XCTest migration |
| `references/distribution.md` | App Store, Developer ID, notarization, sandboxing, universal binaries |
| `references/spm-build.md` | Package.swift, Swift Build, plugins, macros |
| **Concurrency** | |
| `references/approachable-concurrency.md` | Default MainActor isolation, @concurrent, nonisolated async |
| `references/actors-isolation.md` | Actor model, global actors, custom executors, reentrancy |
| `references/structured-concurrency.md` | Task, TaskGroup, async let, cancellation, priority, named tasks |
| `references/sendable-safety.md` | Sendable protocol, data race safety, @unchecked escape hatches |
| `references/async-patterns.md` | AsyncSequence, AsyncStream, Observations, continuations, Clock |
| `references/migration-guide.md` | GCD to async/await, Combine to AsyncSequence, Swift 6 migration |
| **SwiftData** | |
| `references/models-schema.md` | @Model, @Attribute options, Codable, transformable, external storage |
| `references/relationships-predicates.md` | Advanced relationships, inverse rules, compound predicates |
| `references/container-context.md` | ModelContainer, ModelContext, background contexts, undo/redo, batch ops |
| `references/cloudkit-sync.md` | CloudKit setup, conflict resolution, sharing, debugging sync |
| `references/migrations.md` | VersionedSchema, lightweight/custom migration, Core Data migration |
