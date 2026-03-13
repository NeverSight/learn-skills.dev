---
name: cross-platform
description: "Patterns for sharing code between macOS and iOS in SwiftUI apps. Covers project structure (70% shared / 15% macOS / 15% iOS), platform abstraction via protocols and #if os() conditional compilation, adaptive navigation (NavigationSplitView on Mac/iPad → NavigationStack on iPhone), shared components with platform styling, iOS-specific extensions (custom keyboard extension, interactive widgets, share extension, action extension, Control Center widget, lock screen widget), App Groups for data sharing with extensions, CloudKit sync monitoring, JSON export/import, schema versioning and migration, URL scheme deep linking, and the full macOS→iOS migration checklist. Use when building apps that target both macOS and iOS, when adding iOS support to a macOS app, when building widgets or keyboard extensions, or when setting up iCloud sync with SwiftData."
---

# Cross-Platform: macOS ↔ iOS

Patterns for sharing code between macOS and iOS, building iOS-specific extensions, and syncing data across platforms.

## Critical Constraints

- ❌ Never import `AppKit` or `UIKit` in shared code — use SwiftUI types and `#if os()` for platform-specific imports
- ❌ Never use `NSColor`/`UIColor` directly in shared views — use SwiftUI `Color`
- ❌ Never use `NSFont`/`UIFont` directly — use SwiftUI `.font()`
- ✅ Abstract platform services behind protocols
- ✅ Use `#if os(macOS)` / `#if os(iOS)` for platform-specific implementations
- ✅ Use `@Environment(\.horizontalSizeClass)` for adaptive layouts within a platform

## Project Structure

```
MyApp/
├── Shared/                        # 70-80% of code
│   ├── Models/                    # SwiftData models
│   ├── ViewModels/                # @Observable view models
│   ├── Services/
│   │   ├── StorageService.swift
│   │   ├── SyncService.swift
│   │   └── ClipboardService.swift # Protocol — platform-abstracted
│   ├── Views/
│   │   ├── Components/            # Shared UI: cards, rows, badges
│   │   └── Screens/               # Platform-adapted via #if os()
│   └── Extensions/
├── macOS/                         # 15-20% — Mac-specific
│   ├── App/
│   │   ├── MacApp.swift
│   │   └── AppDelegate.swift
│   ├── Services/
│   │   ├── HotkeyManager.swift
│   │   ├── MenuBarController.swift
│   │   └── MacClipboardService.swift
│   └── Views/
│       ├── FloatingPanel.swift
│       └── QuickAccessView.swift
├── iOS/                           # 15-20% — iOS-specific
│   ├── App/
│   │   └── iOSApp.swift
│   ├── Services/
│   │   ├── KeyboardExtension/
│   │   └── iOSClipboardService.swift
│   └── Views/
│       ├── MainTabView.swift
│       └── WidgetView.swift
├── Widgets/                       # Shared widget target
└── MyApp.xcodeproj
```

## Platform Abstraction

### Protocol-Based Services
```swift
// Shared/Services/ClipboardServiceProtocol.swift
protocol ClipboardServiceProtocol {
    func copy(_ text: String)
    func read() -> String?
}

// macOS/Services/MacClipboardService.swift
#if os(macOS)
import AppKit
class MacClipboardService: ClipboardServiceProtocol {
    func copy(_ text: String) {
        NSPasteboard.general.clearContents()
        NSPasteboard.general.setString(text, forType: .string)
    }
    func read() -> String? { NSPasteboard.general.string(forType: .string) }
}
#endif

// iOS/Services/iOSClipboardService.swift
#if os(iOS)
import UIKit
class iOSClipboardService: ClipboardServiceProtocol {
    func copy(_ text: String) { UIPasteboard.general.string = text }
    func read() -> String? { UIPasteboard.general.string }
}
#endif

// Shared/Services/ClipboardService.swift
class ClipboardService {
    static var shared: ClipboardServiceProtocol = {
        #if os(macOS)
        return MacClipboardService()
        #else
        return iOSClipboardService()
        #endif
    }()
}
```

### Conditional Compilation in Views
```swift
struct PromptListView: View {
    var body: some View {
        #if os(macOS)
        NavigationSplitView {
            sidebar
        } detail: {
            detail
        }
        #else
        NavigationStack {
            list
        }
        #endif
    }
}
```

### Environment-Based Adaptation (iPad vs iPhone)
```swift
struct AdaptiveView: View {
    @Environment(\.horizontalSizeClass) var sizeClass

    var body: some View {
        if sizeClass == .compact {
            VStack { content }   // iPhone
        } else {
            HStack { content }   // iPad / Mac
        }
    }
}
```

### Shared Components with Platform Styling
```swift
struct GlassCard<Content: View>: View {
    let content: Content
    init(@ViewBuilder content: () -> Content) { self.content = content() }

    var body: some View {
        content
            .padding()
            .glassEffect(.regular, in: .rect(cornerRadius: 16))
    }
}

struct PrimaryButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(title, action: action)
            .buttonStyle(.glassProminent)
            #if os(macOS)
            .controlSize(.large)
            #endif
    }
}
```

## iOS Extensions

### Custom Keyboard Extension
Replaces global hotkey on iOS — users type prompts via custom keyboard.

```swift
// iOS/KeyboardExtension/KeyboardViewController.swift
import UIKit
import SwiftUI

class KeyboardViewController: UIInputViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        let hostingController = UIHostingController(rootView: KeyboardView(
            onSelect: { [weak self] prompt in
                self?.textDocumentProxy.insertText(prompt.content)
            }
        ))
        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.view.frame = view.bounds
        hostingController.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
    }
}
```

### Interactive Widgets (Home Screen + Lock Screen)
```swift
import WidgetKit
import SwiftUI
import AppIntents

struct PromptWidget: Widget {
    let kind = "PromptWidget"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(
            kind: kind,
            intent: SelectPromptsIntent.self,
            provider: PromptTimelineProvider()
        ) { entry in
            PromptWidgetView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .configurationDisplayName("Quick Prompts")
        .description("Tap to copy your favorite prompts")
        .supportedFamilies([.systemSmall, .systemMedium, .accessoryRectangular])
    }
}

// Widget buttons trigger App Intents directly
struct PromptWidgetView: View {
    let entry: PromptEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            ForEach(entry.prompts) { prompt in
                Button(intent: CopyPromptIntent(prompt: prompt.entity)) {
                    HStack {
                        Image(systemName: prompt.icon).foregroundStyle(.secondary)
                        Text(prompt.title).lineLimit(1)
                        Spacer()
                        Image(systemName: "doc.on.clipboard").font(.caption).foregroundStyle(.tertiary)
                    }
                    .padding(.vertical, 4)
                }
                .buttonStyle(.plain)
            }
        }
        .padding()
    }
}
```

### Share Extension (Save text from other apps)
```swift
import UIKit
import SwiftUI
import UniformTypeIdentifiers

class ShareViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        guard let item = extensionContext?.inputItems.first as? NSExtensionItem,
              let provider = item.attachments?.first(where: {
                  $0.hasItemConformingToTypeIdentifier(UTType.plainText.identifier)
              }) else { close(); return }

        provider.loadItem(forTypeIdentifier: UTType.plainText.identifier) { [weak self] text, _ in
            DispatchQueue.main.async {
                if let text = text as? String { self?.showSaveUI(text: text) }
                else { self?.close() }
            }
        }
    }

    func showSaveUI(text: String) {
        let saveView = SavePromptView(initialContent: text,
            onSave: { [weak self] title, content, category in
                SharedPromptStore.shared.add(SharedPrompt(title: title, content: content, category: category))
                self?.close()
            },
            onCancel: { [weak self] in self?.close() }
        )
        let hc = UIHostingController(rootView: saveView)
        addChild(hc)
        view.addSubview(hc.view)
        hc.view.frame = view.bounds
        hc.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
    }

    func close() { extensionContext?.completeRequest(returningItems: nil) }
}
```

### Control Center Widget (iOS 18+)
```swift
import WidgetKit

struct PromptControlWidget: ControlWidget {
    var body: some ControlWidgetConfiguration {
        AppIntentControlConfiguration(kind: "PromptControl", intent: CopyFavoritePromptIntent.self) { config in
            ControlWidgetButton(action: config) {
                Label(config.prompt?.title ?? "Prompt", systemImage: "doc.on.clipboard")
            }
        }
        .displayName("Quick Prompt")
    }
}
```

### URL Scheme Deep Links
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onOpenURL { url in
                    // myapp://copy/{id}, myapp://edit/{id}, myapp://new?content={encoded}
                    guard url.scheme == "myapp" else { return }
                    switch url.host {
                    case "copy":
                        if let id = UUID(uuidString: url.lastPathComponent) {
                            PromptService.shared.copyToClipboard(id: id)
                        }
                    case "edit":
                        if let id = UUID(uuidString: url.lastPathComponent) {
                            NavigationState.shared.editPrompt(id: id)
                        }
                    default: break
                    }
                }
        }
    }
}
```

## Data Sync & App Groups

### App Groups for Extensions/Widgets
Extensions (widgets, keyboard, share) run in separate processes. Share data via App Groups.

```swift
// 1. Add App Groups capability to main app AND all extensions
// 2. Use same group identifier: "group.com.yourapp.shared"

// Shared container for SwiftData
extension ModelContainer {
    static var shared: ModelContainer = {
        let schema = Schema([Prompt.self, Category.self])
        let storeURL = FileManager.default
            .containerURL(forSecurityApplicationGroupIdentifier: "group.com.yourapp.shared")!
            .appendingPathComponent("prompts.sqlite")
        let config = ModelConfiguration(url: storeURL)
        return try! ModelContainer(for: schema, configurations: [config])
    }()
}

// Lightweight sharing via UserDefaults
let sharedDefaults = UserDefaults(suiteName: "group.com.yourapp.shared")
sharedDefaults?.set(encodedData, forKey: "prompts")
```

### CloudKit Sync with SwiftData
```swift
let config = ModelConfiguration(
    schema: schema,
    isStoredInMemoryOnly: false,
    cloudKitDatabase: .automatic  // Enable iCloud sync
)
```

### Sync Status Monitoring
```swift
class SyncMonitor: ObservableObject {
    @Published var syncStatus: SyncStatus = .unknown
    enum SyncStatus { case unknown, syncing, synced, error(String), noAccount }

    init() {
        CKContainer.default().accountStatus { [weak self] status, _ in
            DispatchQueue.main.async {
                switch status {
                case .available: self?.syncStatus = .synced
                case .noAccount: self?.syncStatus = .noAccount
                default: self?.syncStatus = .error("iCloud unavailable")
                }
            }
        }
        // Observe sync events
        NotificationCenter.default.addObserver(
            forName: NSPersistentCloudKitContainer.eventChangedNotification,
            object: nil, queue: .main
        ) { [weak self] notification in
            guard let event = notification.userInfo?[NSPersistentCloudKitContainer.eventNotificationUserInfoKey]
                    as? NSPersistentCloudKitContainer.Event else { return }
            self?.syncStatus = event.endDate != nil ? .synced : .syncing
        }
    }
}
```

### JSON Export/Import
```swift
struct PromptExport: Codable {
    let version: Int
    let exportedAt: Date
    let prompts: [PromptData]
    struct PromptData: Codable {
        let id: UUID, title: String, content: String
        let categoryName: String?, isFavorite: Bool
    }
}

extension PromptService {
    func exportToJSON() throws -> Data {
        let prompts = try context.fetch(FetchDescriptor<Prompt>())
        let export = PromptExport(version: 1, exportedAt: Date(), prompts: prompts.map {
            .init(id: $0.id, title: $0.title, content: $0.content,
                  categoryName: $0.category?.name, isFavorite: $0.isFavorite)
        })
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        return try encoder.encode(export)
    }

    func importFromJSON(_ data: Data) throws -> Int {
        let export = try JSONDecoder().decode(PromptExport.self, from: data)
        var imported = 0
        for p in export.prompts {
            let existing = try? context.fetch(
                FetchDescriptor<Prompt>(predicate: #Predicate { $0.id == p.id })
            ).first
            if existing == nil {
                let prompt = Prompt(title: p.title, content: p.content)
                prompt.id = p.id; prompt.isFavorite = p.isFavorite
                context.insert(prompt); imported += 1
            }
        }
        try context.save()
        return imported
    }
}
```

### Schema Versioning
```swift
enum SchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)
    static var models: [any PersistentModel.Type] { [Prompt.self, Category.self] }
}

enum SchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)
    static var models: [any PersistentModel.Type] { [Prompt.self, Category.self, PromptVariable.self] }
}

enum MigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] { [SchemaV1.self, SchemaV2.self] }
    static var stages: [MigrationStage] {
        [MigrationStage.lightweight(fromVersion: SchemaV1.self, toVersion: SchemaV2.self)]
    }
}
```

## Widget Refresh
```swift
// After any prompt change — notify widgets
WidgetCenter.shared.reloadAllTimelines()
// Or specific widget
WidgetCenter.shared.reloadTimelines(ofKind: "PromptWidget")
```

## macOS → iOS Migration Checklist

### Core Functionality
- [ ] All models work on both platforms (no AppKit/UIKit imports)
- [ ] ViewModels have no platform-specific imports
- [ ] Services use protocol abstraction

### UI Adaptation
- [ ] Navigation adapted (SplitView → Stack on iPhone)
- [ ] Touch targets ≥ 44pt minimum
- [ ] No hover-only interactions (add tap alternatives)
- [ ] Keyboard shortcuts have touch equivalents

### Platform Features
- [ ] Hotkey → Keyboard extension or widget on iOS
- [ ] Menu bar → App icon or widget on iOS
- [ ] Floating panel → Sheet or full-screen modal on iOS
- [ ] Right-click → Long press context menu

### Data
- [ ] CloudKit sync enabled
- [ ] App Groups configured for extensions
- [ ] Shared UserDefaults for lightweight data
- [ ] SwiftData shared container for extensions

### Testing
- [ ] Shared tests pass on both platforms
- [ ] UI tests for each platform
- [ ] Widget previews work
- [ ] Test on real device (not just simulator)

## Common Pitfalls

1. **Documents directory differs** — abstract file paths, don't hardcode
2. **Keyboard presence on iOS** — handle `keyboardLayoutGuide` or `.ignoresSafeArea(.keyboard)`
3. **Right-click menus** — provide `.contextMenu` (works as right-click on Mac, long-press on iOS)
4. **Window management** — macOS has multiple windows; iOS is single-window (use `openWindow` conditionally)
5. **Status bar** — macOS `MenuBarExtra`; no equivalent on iOS (use widget instead)
