---
name: macos-app-structure
description: macOS application architecture patterns covering App protocol (@main), Scene types (WindowGroup, Window, Settings, MenuBarExtra), multi-window management, NSApplicationDelegateAdaptor for AppKit lifecycle hooks, Info.plist configuration (LSUIElement for menu bar apps, NSAccessibilityUsageDescription), entitlements for sandbox/hardened runtime, and project structure conventions. Use when scaffolding a new macOS app, configuring scenes and windows, setting up menu bar apps, or resolving macOS-specific lifecycle issues. Corrects the common LLM mistake of generating iOS-only app structures.
---

# macOS App Structure

## Critical Constraints

- ❌ DO NOT use iOS-only scenes (`TabView` as root scene) → ✅ Use `WindowGroup`, `Window`, or `NavigationSplitView`
- ❌ DO NOT use `UIApplicationDelegate` → ✅ Use `NSApplicationDelegateAdaptor` for AppKit hooks
- ❌ DO NOT forget `Settings` scene for Preferences → ✅ macOS apps should have a Settings scene
- ❌ DO NOT assume single-window → ✅ macOS apps can have multiple windows; design for it
- ❌ DO NOT use iOS navigation patterns → ✅ Use `NavigationSplitView` (sidebar + detail) for macOS

## Standard macOS App
```swift
import SwiftUI

@main
struct MyApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .defaultSize(width: 900, height: 600)

        Settings {
            SettingsView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // AppKit lifecycle hooks
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true  // Quit when last window closes
    }
}
```

## Menu Bar App
```swift
@main
struct MenuBarApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "command") {
            MenuBarView()
        }
        .menuBarExtraStyle(.window)  // Full window popover (not just menu items)

        Settings {
            SettingsView()
        }
    }
}
```

To hide dock icon, add to Info.plist:
```xml
<key>LSUIElement</key>
<true/>
```

## Multiple Named Windows
```swift
@main
struct MultiWindowApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        Window("Inspector", id: "inspector") {
            InspectorView()
        }
        .defaultSize(width: 300, height: 400)
        .defaultPosition(.trailing)

        Settings {
            SettingsView()
        }
    }
}

// Open a named window from code
@Environment(\.openWindow) private var openWindow
Button("Open Inspector") { openWindow(id: "inspector") }
```

## Content View with Sidebar
```swift
struct ContentView: View {
    @State private var selection: SidebarItem? = .library

    var body: some View {
        NavigationSplitView {
            List(selection: $selection) {
                Section("Library") {
                    Label("All Items", systemImage: "square.grid.2x2")
                        .tag(SidebarItem.library)
                    Label("Favorites", systemImage: "heart")
                        .tag(SidebarItem.favorites)
                }
            }
            .navigationSplitViewColumnWidth(min: 180, ideal: 220)
        } detail: {
            switch selection {
            case .library: LibraryView()
            case .favorites: FavoritesView()
            case nil: ContentUnavailableView("Select an item", systemImage: "sidebar.left")
            }
        }
        .navigationTitle("My App")
    }
}
```

## Project Structure Convention
```
MyApp/
├── MyApp.swift              # @main App struct
├── AppDelegate.swift        # NSApplicationDelegateAdaptor (if needed)
├── Models/                  # SwiftData @Model classes
├── Views/
│   ├── ContentView.swift    # Main navigation structure
│   ├── Components/          # Reusable view components
│   └── Settings/            # Settings/Preferences views
├── ViewModels/              # @Observable view models
├── Services/                # Business logic, networking, persistence
├── Utilities/               # Extensions, helpers
├── Resources/
│   ├── Assets.xcassets
│   └── Localizable.xcstrings
├── Info.plist
└── MyApp.entitlements
```

## Key Info.plist Entries (macOS)
```xml
<key>LSUIElement</key>           <!-- true = menu bar only, no dock icon -->
<key>NSAccessibilityUsageDescription</key>  <!-- Required for Accessibility API -->
<key>NSAppleEventsUsageDescription</key>    <!-- Required for AppleScript -->
```

## Key Entitlements
```xml
<!-- App Sandbox (required for App Store) -->
<key>com.apple.security.app-sandbox</key><true/>

<!-- Network access -->
<key>com.apple.security.network.client</key><true/>

<!-- File access -->
<key>com.apple.security.files.user-selected.read-write</key><true/>

<!-- iCloud -->
<key>com.apple.developer.icloud-container-identifiers</key>
```

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| No `Settings` scene | Add `Settings { SettingsView() }` — expected on macOS |
| App doesn't quit when last window closes | Implement `applicationShouldTerminateAfterLastWindowClosed` |
| Dock icon showing for menu bar app | Add `LSUIElement = true` to Info.plist |
| Window too small on macOS | Add `.defaultSize(width:height:)` to WindowGroup |
| Using `TabView` as main navigation | Use `NavigationSplitView` with sidebar on macOS |

## References

- [SwiftUI App Structure](https://developer.apple.com/documentation/SwiftUI/App)
- [MenuBarExtra](https://developer.apple.com/documentation/SwiftUI/MenuBarExtra)
- [App Sandbox Design Guide](https://developer.apple.com/documentation/security/app_sandbox)
