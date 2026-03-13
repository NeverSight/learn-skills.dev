---
name: appkit-bridge
description: Bridging AppKit components into SwiftUI macOS apps. Covers NSViewRepresentable and NSViewControllerRepresentable protocols for hosting AppKit views in SwiftUI, NSHostingView/NSHostingController for hosting SwiftUI in AppKit, NSPanel for floating windows, NSWindow configuration (styleMask, level, collectionBehavior), responder chain integration, NSEvent monitoring (global and local), NSAnimationContext for AppKit animations, NSPopover, NSStatusItem for menu bar, and NSGlassEffectView for AppKit Liquid Glass. Use when SwiftUI lacks a native equivalent, building floating panels, custom window chrome, or integrating legacy AppKit components.
---

# AppKit Bridge — SwiftUI ↔ AppKit Integration

## Critical Constraints

- ❌ DO NOT use `NSViewController` as app architecture → ✅ Use SwiftUI `App` + `Scene`, bridge only where needed
- ❌ DO NOT use `NSView` subclass when SwiftUI modifier exists → ✅ Check SwiftUI first, bridge as last resort
- ❌ DO NOT forget `makeCoordinator()` for delegate callbacks → ✅ Use Coordinator pattern for NSViewRepresentable
- ❌ DO NOT call `makeNSView` to update → ✅ Use `updateNSView(_:context:)` for state changes

## NSViewRepresentable (AppKit → SwiftUI)
```swift
import SwiftUI
import AppKit

struct WrappedNSView: NSViewRepresentable {
    var text: String

    func makeNSView(context: Context) -> NSTextField {
        let field = NSTextField()
        field.delegate = context.coordinator
        return field
    }

    func updateNSView(_ nsView: NSTextField, context: Context) {
        nsView.stringValue = text
    }

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    class Coordinator: NSObject, NSTextFieldDelegate {
        var parent: WrappedNSView
        init(_ parent: WrappedNSView) { self.parent = parent }

        func controlTextDidChange(_ obj: Notification) {
            // Handle text changes
        }
    }
}
```

## NSHostingView (SwiftUI → AppKit)
```swift
let swiftUIView = MySwiftUIView()
let hostingView = NSHostingView(rootView: swiftUIView)
hostingView.translatesAutoresizingMaskIntoConstraints = false

// Add to AppKit view hierarchy
parentView.addSubview(hostingView)
NSLayoutConstraint.activate([
    hostingView.leadingAnchor.constraint(equalTo: parentView.leadingAnchor),
    hostingView.trailingAnchor.constraint(equalTo: parentView.trailingAnchor),
    hostingView.topAnchor.constraint(equalTo: parentView.topAnchor),
    hostingView.bottomAnchor.constraint(equalTo: parentView.bottomAnchor),
])
```

## NSPanel — Floating Window
```swift
class FloatingPanel: NSPanel {
    init(contentView: NSView) {
        super.init(
            contentRect: NSRect(x: 0, y: 0, width: 600, height: 400),
            styleMask: [.nonactivatingPanel, .titled, .closable, .fullSizeContentView],
            backing: .buffered, defer: true
        )
        titlebarAppearsTransparent = true
        titleVisibility = .hidden
        isOpaque = false
        backgroundColor = .clear
        level = .floating
        collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .transient]
        isMovableByWindowBackground = true
        hidesOnDeactivate = false
        self.contentView = contentView
        center()
    }
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { false }
}

// Host SwiftUI content
let panel = FloatingPanel(contentView: NSHostingView(rootView: MyView()))
```

## Show/Hide with Animation
```swift
extension FloatingPanel {
    func showCentered() {
        center()
        alphaValue = 0
        makeKeyAndOrderFront(nil)
        NSAnimationContext.runAnimationGroup { ctx in
            ctx.duration = 0.15
            ctx.timingFunction = CAMediaTimingFunction(name: .easeOut)
            animator().alphaValue = 1
        }
    }

    func hideAnimated() {
        NSAnimationContext.runAnimationGroup({ ctx in
            ctx.duration = 0.1
            ctx.timingFunction = CAMediaTimingFunction(name: .easeIn)
            animator().alphaValue = 0
        }, completionHandler: { self.orderOut(nil) })
    }
}
```

## NSPopover
```swift
let popover = NSPopover()
popover.contentViewController = NSHostingController(rootView: PopoverContent())
popover.behavior = .transient
popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
popover.contentViewController?.view.window?.makeKey()
```

## Window Positioning
```swift
extension NSPanel {
    func centerOnActiveScreen() {
        guard let screen = NSScreen.main ?? NSScreen.screens.first else { return }
        let frame = screen.visibleFrame
        setFrameOrigin(NSPoint(x: frame.midX - self.frame.width / 2,
                                y: frame.midY - self.frame.height / 2))
    }
}
```

## Decision Tree
```
Need a floating overlay? → NSPanel + NSHostingView
Need a menu bar popover? → NSPopover + NSHostingController
Need custom window chrome? → NSWindow subclass + titlebarAppearsTransparent
Need AppKit control in SwiftUI? → NSViewRepresentable
Need SwiftUI view in AppKit? → NSHostingView or NSHostingController
Need glass effect in AppKit? → NSGlassEffectView (see liquid-glass skill)
```

## References

- [NSViewRepresentable](https://developer.apple.com/documentation/SwiftUI/NSViewRepresentable)
- [NSHostingView](https://developer.apple.com/documentation/SwiftUI/NSHostingView)
- [NSPanel](https://developer.apple.com/documentation/appkit/nspanel)
