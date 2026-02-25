---
name: global-hotkeys
description: System-wide keyboard shortcut registration on macOS using NSEvent monitoring (simple, app-level) and Carbon EventHotKey API (reliable, system-wide). Covers NSEvent.addGlobalMonitorForEvents and addLocalMonitorForEvents, CGEvent tap for keystroke simulation, Carbon RegisterEventHotKey for system-wide hotkeys, modifier flag handling (.deviceIndependentFlagsMask), common key code mappings, debouncing, Accessibility permission requirements (AXIsProcessTrusted), and SwiftUI .onKeyPress for in-app shortcuts. Use when implementing global keyboard shortcuts, hotkey-triggered panels, or system-wide key event monitoring.
---

# Global Hotkeys — System-Wide Keyboard Shortcuts

## Critical Constraints

- ❌ DO NOT use only `addGlobalMonitorForEvents` → ✅ Also add `addLocalMonitorForEvents` (global doesn't fire when YOUR app is focused)
- ❌ DO NOT forget Accessibility permission → ✅ Global event monitoring requires `AXIsProcessTrusted()`
- ❌ DO NOT compare raw `modifierFlags` → ✅ Mask with `.deviceIndependentFlagsMask` first
- ❌ DO NOT use NSEvent for system-wide hotkeys in sandboxed apps → ✅ Use Carbon `RegisterEventHotKey` for reliability

## Decision Tree
```
In-app shortcut only?
└── SwiftUI .onKeyPress or .keyboardShortcut

System-wide, non-sandboxed?
├── Simple → NSEvent global + local monitors
└── Reliable → Carbon RegisterEventHotKey

System-wide, sandboxed (App Store)?
└── Carbon RegisterEventHotKey + Accessibility entitlement
```

## Method 1: NSEvent Monitors (Simple)
```swift
import AppKit

class HotkeyManager {
    private var globalMonitor: Any?
    private var localMonitor: Any?
    var onHotkey: (() -> Void)?
    var modifiers: NSEvent.ModifierFlags = [.command, .shift]
    var keyCode: UInt16 = 49  // Space

    func start() {
        globalMonitor = NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { [weak self] event in
            self?.handleEvent(event)
        }
        localMonitor = NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            self?.handleEvent(event)
            return event
        }
    }

    func stop() {
        if let m = globalMonitor { NSEvent.removeMonitor(m) }
        if let m = localMonitor { NSEvent.removeMonitor(m) }
    }

    private func handleEvent(_ event: NSEvent) {
        let flags = event.modifierFlags.intersection(.deviceIndependentFlagsMask)
        if flags == modifiers && event.keyCode == keyCode {
            DispatchQueue.main.async { self.onHotkey?() }
        }
    }
}
```

## Method 2: Carbon API (Reliable, System-Wide)
```swift
import Carbon

class CarbonHotkeyManager {
    private var hotkeyRef: EventHotKeyRef?
    private var eventHandler: EventHandlerRef?
    var onHotkey: (() -> Void)?

    func register(keyCode: UInt32, modifiers: UInt32) {
        unregister()
        var hotkeyID = EventHotKeyID()
        hotkeyID.signature = OSType("HTKY".fourCharCodeValue)
        hotkeyID.id = 1

        var eventType = EventTypeSpec(
            eventClass: OSType(kEventClassKeyboard),
            eventKind: UInt32(kEventHotKeyPressed)
        )

        let handler: EventHandlerUPP = { _, event, userData in
            let mgr = Unmanaged<CarbonHotkeyManager>.fromOpaque(userData!).takeUnretainedValue()
            mgr.onHotkey?()
            return noErr
        }

        InstallEventHandler(GetApplicationEventTarget(), handler, 1, &eventType,
                           Unmanaged.passUnretained(self).toOpaque(), &eventHandler)
        RegisterEventHotKey(keyCode, modifiers, hotkeyID,
                           GetApplicationEventTarget(), 0, &hotkeyRef)
    }

    func unregister() {
        if let ref = hotkeyRef { UnregisterEventHotKey(ref) }
        if let h = eventHandler { RemoveEventHandler(h) }
    }
}

extension String {
    var fourCharCodeValue: FourCharCode {
        utf8.reduce(0) { ($0 << 8) + FourCharCode($1) }
    }
}
```

## Carbon Modifier Constants
```swift
// Carbon modifier flags for RegisterEventHotKey
let cmdKey: UInt32    = UInt32(cmdKey)      // 256
let shiftKey: UInt32  = UInt32(shiftKey)    // 512
let optionKey: UInt32 = UInt32(optionKey)   // 2048
let controlKey: UInt32 = UInt32(controlKey) // 4096

// Example: Cmd+Shift+Space
register(keyCode: 49, modifiers: UInt32(cmdKey) | UInt32(shiftKey))
```

## Common Key Codes
| Key | Code | Key | Code | Key | Code |
|-----|------|-----|------|-----|------|
| Space | 49 | Return | 36 | Escape | 53 |
| Tab | 48 | Delete | 51 | A | 0 |
| S | 1 | D | 2 | F | 3 |
| J | 38 | K | 40 | L | 37 |

## SwiftUI In-App Shortcuts
```swift
// Keyboard shortcut on button
Button("Save") { save() }
    .keyboardShortcut("s", modifiers: .command)

// Raw key press handler
.onKeyPress(.escape) { dismiss(); return .handled }
.onKeyPress(.upArrow) { moveUp(); return .handled }
.onKeyPress(.downArrow) { moveDown(); return .handled }
```

## Accessibility Permission Check
```swift
func checkAccessibilityPermissions() -> Bool {
    let options = [kAXTrustedCheckOptionPrompt.takeRetainedValue() as String: true]
    return AXIsProcessTrustedWithOptions(options as CFDictionary)
}

// Non-prompting check
func isAccessibilityGranted() -> Bool {
    AXIsProcessTrusted()
}
```

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Hotkey works everywhere except own app | Add local monitor alongside global monitor |
| Modifier comparison fails | Mask with `.deviceIndependentFlagsMask` |
| Hotkey fires twice | Debounce with timestamp check (0.3s threshold) |
| Doesn't work on first launch | Check/request Accessibility permission |

## References

- [NSEvent](https://developer.apple.com/documentation/appkit/nsevent)
- [Carbon Events](https://developer.apple.com/documentation/coreservices/carbon_events)
