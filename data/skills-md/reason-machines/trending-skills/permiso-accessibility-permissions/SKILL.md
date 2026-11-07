---
name: permiso-accessibility-permissions
description: Permission dialog UI for macOS accessibility and privacy settings, replicating the Codex Computer Use guided permissions flow
triggers:
  - show accessibility permission dialog
  - guide user through privacy settings
  - permiso permission panel
  - accessibility permission helper macOS
  - show permission dialog like Codex
  - request accessibility access macOS
  - PermisoAssistant present panel
  - guided settings permission flow Swift
---

# Permiso — macOS Permission Dialog Helper

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Permiso provides a polished permission dialog UI for macOS apps that guides users through enabling accessibility and privacy settings — replicating the guided flow seen in OpenAI's Codex Computer Use product.

## What It Does

- Presents an animated, guided overlay panel directing users to open System Settings and enable specific permissions (e.g. Accessibility)
- Mirrors the UX pattern from Codex Computer Use: an on-screen assistant that walks users through enabling access
- Handles the common friction point of macOS permission flows with a clear, app-integrated UI

## Installation

### Swift Package Manager

Add to your `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/zats/permiso", branch: "main")
]
```

Or in Xcode: **File → Add Package Dependencies** → enter `https://github.com/zats/permiso`

Then add `Permiso` to your target's dependencies:

```swift
.target(
    name: "YourApp",
    dependencies: ["Permiso"]
)
```

## Core API

### Basic Usage

```swift
import Permiso

@MainActor
func showAccessibilityHelper() {
    PermisoAssistant.shared.present(panel: .accessibility)
}
```

### Triggering on App Launch

```swift
import SwiftUI
import Permiso

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    checkAndRequestAccessibility()
                }
        }
    }

    @MainActor
    func checkAndRequestAccessibility() {
        let trusted = AXIsProcessTrusted()
        if !trusted {
            PermisoAssistant.shared.present(panel: .accessibility)
        }
    }
}
```

### AppDelegate Pattern

```swift
import AppKit
import Permiso

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        requestAccessibilityIfNeeded()
    }

    @MainActor
    func requestAccessibilityIfNeeded() {
        guard !AXIsProcessTrusted() else { return }
        PermisoAssistant.shared.present(panel: .accessibility)
    }
}
```

## Common Patterns

### Check Permission Before Sensitive Actions

```swift
import Permiso
import ApplicationServices

@MainActor
func performAccessibilityAction() {
    guard AXIsProcessTrusted() else {
        PermisoAssistant.shared.present(panel: .accessibility)
        return
    }
    // Proceed with accessibility-dependent work
    doAccessibilityWork()
}
```

### Polling for Permission Grant

```swift
import Permiso
import ApplicationServices
import Combine

class PermissionMonitor: ObservableObject {
    @Published var isAccessibilityGranted = false
    private var timer: AnyCancellable?

    @MainActor
    func startMonitoring() {
        if AXIsProcessTrusted() {
            isAccessibilityGranted = true
            return
        }

        PermisoAssistant.shared.present(panel: .accessibility)

        timer = Timer.publish(every: 1.0, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                if AXIsProcessTrusted() {
                    self?.isAccessibilityGranted = true
                    self?.timer?.cancel()
                }
            }
    }
}
```

### SwiftUI View Integration

```swift
import SwiftUI
import Permiso

struct SettingsView: View {
    @State private var accessibilityGranted = AXIsProcessTrusted()

    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Image(systemName: accessibilityGranted ? "checkmark.circle.fill" : "xmark.circle.fill")
                    .foregroundColor(accessibilityGranted ? .green : .red)
                Text("Accessibility Access")
            }

            if !accessibilityGranted {
                Button("Enable Accessibility Access") {
                    requestAccess()
                }
                .buttonStyle(.borderedProminent)
            }
        }
        .padding()
        .onReceive(Timer.publish(every: 2, on: .main, in: .common).autoconnect()) { _ in
            accessibilityGranted = AXIsProcessTrusted()
        }
    }

    @MainActor
    func requestAccess() {
        PermisoAssistant.shared.present(panel: .accessibility)
    }
}
```

## Requirements

- **macOS**: The library targets macOS (version as specified by the package; check for macOS 13+ for best compatibility)
- **Swift**: Swift 5.9+
- **Main Actor**: `PermisoAssistant.shared.present(panel:)` must be called from the main thread / `@MainActor` context

## Entitlements / Info.plist

For accessibility usage, ensure your app's `Info.plist` includes a usage description (though macOS doesn't require this like iOS, it's good practice), and that your app is **not sandboxed** or has the correct entitlements if it needs to use accessibility APIs:

```xml
<!-- In your .entitlements file if needed -->
<key>com.apple.security.temporary-exception.apple-events</key>
<true/>
```

For apps that actually use accessibility features after permission is granted:

```swift
// Request trust prompt (system dialog) alongside Permiso's guided UI
let options = [kAXTrustedCheckOptionPrompt.takeRetainedValue(): true] as CFDictionary
AXIsProcessTrustedWithOptions(options)
```

## Troubleshooting

**Panel doesn't appear**
- Ensure you're calling from `@MainActor` / main thread
- Check that your app has a visible window; the panel attaches to the app's UI context

**`AXIsProcessTrusted()` returns false even after granting**
- macOS caches trust state; the app may need to be relaunched or the check polled with a timer (see polling pattern above)
- Some sandboxed apps require a full app restart after granting accessibility

**Build errors: `cannot find 'PermisoAssistant' in scope`**
- Confirm `import Permiso` is at the top of the file
- Confirm the package is added to the correct target in Xcode, not just the project

**Panel appears but dismisses immediately**
- Make sure you're not overriding the window or calling dismiss logic right after present
- Avoid calling present inside a `Task { }` that gets cancelled immediately

## Key Types Reference

| Type | Description |
|------|-------------|
| `PermisoAssistant` | Singleton entry point — use `.shared` |
| `PermisoAssistant.shared.present(panel:)` | Shows the guided permission dialog |
| `.accessibility` | Panel type for Accessibility settings |
