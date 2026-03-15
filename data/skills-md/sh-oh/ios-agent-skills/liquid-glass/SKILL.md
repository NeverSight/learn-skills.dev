---
name: liquid-glass
description: iOS 26 Liquid Glass design system guide for SwiftUI, UIKit, AppKit, and WidgetKit. Covers glass effects, morphing transitions, and interactive states.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# Liquid Glass Design System (iOS 26+)

A new design system introduced in iOS 26. It expresses depth and hierarchy through translucent glass effects.

## Basic Glass Effect

```swift
// Basic capsule-shaped Glass Effect
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect()

// Custom shape
Text("Rounded Glass")
    .padding()
    .glassEffect(in: .rect(cornerRadius: 16.0))

// Circle
Image(systemName: "star.fill")
    .frame(width: 60, height: 60)
    .glassEffect(in: .circle)
```

## Interactive Glass

```swift
// Glass with touch interaction
Button("Tap Me") {
    // action
}
.glassEffect(.regular.interactive())

// Color tint + interactive
Button("Orange Glass") {
    // action
}
.glassEffect(.regular.tint(.orange).interactive())
```

## Button Styles

```swift
// Glass button style
Button("Glass Button") { }
    .buttonStyle(.glass)

// Prominent Glass button
Button("Prominent") { }
    .buttonStyle(.glassProminent)
```

## GlassEffectContainer (Multiple Effects)

Groups multiple glass effects together for consistent visual treatment.

```swift
GlassEffectContainer(spacing: 40.0) {
    HStack(spacing: 40.0) {
        Image(systemName: "scribble.variable")
            .frame(width: 80.0, height: 80.0)
            .glassEffect()

        Image(systemName: "eraser.fill")
            .frame(width: 80.0, height: 80.0)
            .glassEffect()

        Image(systemName: "lasso")
            .frame(width: 80.0, height: 80.0)
            .glassEffect()
    }
}
```

## Morphing Transitions

Assign IDs to glass effects to apply morphing animations during view transitions.

```swift
struct MorphingExample: View {
    @State private var selectedTool = "pencil"
    @Namespace private var namespace

    var body: some View {
        HStack(spacing: 20) {
            ForEach(["pencil", "eraser", "lasso"], id: \.self) { tool in
                Image(systemName: tool)
                    .frame(width: 60, height: 60)
                    .glassEffect()
                    .glassEffectID(tool, in: namespace)
                    .onTapGesture {
                        withAnimation(.spring(response: 0.4)) {
                            selectedTool = tool
                        }
                    }
            }
        }
    }
}
```

## UIKit Integration

```swift
// Using Liquid Glass in UIKit
class GlassViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let label = UILabel()
        label.text = "Glass Label"

        // Use UIGlassEffect in UIKit
        if #available(iOS 26.0, *) {
            let glassEffect = UIGlassEffect()
            label.addGlassEffect(glassEffect)
        }
    }
}
```

## WidgetKit Integration

```swift
// Liquid Glass in widgets
struct MyWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "MyWidget", provider: Provider()) { entry in
            VStack {
                Text(entry.title)
                    .glassEffect()
            }
        }
    }
}
```

## Design Guidelines

### DO:
- Use glass effects over background content to express depth
- Group related elements with `GlassEffectContainer`
- Use morphing transitions for smooth view transitions
- Provide touch feedback with interactive glass

### DON'T:
- Overuse glass effects on every element
- Nest glass on top of glass (reduces readability)
- Use glass on text-heavy areas
- Use glass where there is no background content (minimal visual effect)

## Availability Check

```swift
if #available(iOS 26.0, *) {
    content
        .glassEffect()
} else {
    content
        .background(.ultraThinMaterial)
        .cornerRadius(12)
}
```

---

> Liquid Glass is a core design change in iOS 26.
> Always check the latest APIs in the Apple Developer Documentation before use.
