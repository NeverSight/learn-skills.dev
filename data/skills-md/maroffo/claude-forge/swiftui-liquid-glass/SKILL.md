---
name: swiftui-liquid-glass
description: "iOS 26+ Liquid Glass API for glassmorphism effects. Use when user wants glass effects, frosted backgrounds, translucent UI, or .glassEffect() modifier guidance."
compatibility: "Requires Xcode with iOS 26+ SDK."
---

# ABOUTME: iOS 26+ Liquid Glass API for glassmorphism effects and interactive UI
# ABOUTME: .glassEffect() modifier, intensity, tint, style, interactive glass, fallbacks

# SwiftUI Liquid Glass

## When to Invoke
- iOS 26+ glassmorphism effects
- Frosted glass backgrounds
- Translucent interactive UI
- Material design alternatives
- Modern iOS 26 aesthetic

## Capabilities
- Apply glass effects to views
- Interactive glass for tappable elements
- Fallback to materials on older iOS
- Customize glass intensity/blur
- Layer glass containers

## Basic API

```swift
import SwiftUI

@available(iOS 26, *)
struct GlassCard: View {
    var body: some View {
        VStack {
            Text("Liquid Glass")
            Text("iOS 26+")
        }
        .padding()
        .glassEffect()  // Basic glass effect
    }
}
```

## With Fallbacks

```swift
struct AdaptiveGlassView: View {
    var body: some View {
        if #available(iOS 26, *) {
            content
                .glassEffect(intensity: 0.7)
        } else {
            content
                .background(.ultraThinMaterial)
        }
    }

    var content: some View {
        Text("Works on all iOS versions")
            .padding()
    }
}
```

## Glass Effect Parameters

| Parameter | Type | Purpose |
|-----------|------|---------|
| `intensity` | `Double` | Glass blur strength (0.0-1.0) |
| `tint` | `Color` | Glass tint color |
| `style` | `GlassEffectStyle` | `.light`, `.dark`, `.adaptive` |

## Interactive Glass

```swift
@available(iOS 26, *)
struct InteractiveGlassButton: View {
    var body: some View {
        Button("Tap Me") {
            print("Tapped")
        }
        .padding()
        .glassEffect(intensity: 0.8, interactive: true)  // Responds to touch
    }
}
```

## GlassEffectContainer

Wrap content in `GlassEffectContainer { ZStack { background; foreground.glassEffect() } }` for layered glass over images/content.

## Common Patterns

```swift
// Card: .glassEffect(intensity: 0.75, tint: .blue.opacity(0.1)).cornerRadius(16)
// Toolbar: .glassEffect(style: .adaptive)
// Migration: see "With Fallbacks" above (.ultraThinMaterial → .glassEffect())
```
