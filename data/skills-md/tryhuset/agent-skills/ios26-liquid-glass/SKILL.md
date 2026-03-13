---
name: ios26-liquid-glass
description: Use when implementing iOS 26 Liquid Glass effects in SwiftUI. Covers glassEffect modifier, GlassEffectContainer, morphing with glassEffectID, and correct parameter usage.
---

You are an expert in iOS 26's Liquid Glass design system. Help developers implement glass effects correctly in SwiftUI using the proper APIs and patterns.

## Availability

Liquid Glass requires iOS 26+. Always gate with availability checks and provide fallbacks:

```swift
if #available(iOS 26, *) {
    content
        .glassEffect()
} else {
    content
        .background(.ultraThinMaterial)
}
```

## Modifier Ordering

Apply `.glassEffect()` after layout and visual modifiers:

```swift
Text("Label")
    .font(.headline)        // 1. Typography
    .foregroundStyle(.white) // 2. Color
    .padding()              // 3. Layout
    .frame(width: 100)      // 4. Size
    .glassEffect()          // 5. Glass effect last
```

## Core API

### glassEffect Modifier

```swift
func glassEffect<S: Shape>(
    _ glass: Glass = .regular,
    in shape: S = .capsule,
    isEnabled: Bool = true
) -> some View
```

Apply to any view to add glass material. Default shape is capsule.

### Glass Struct

```swift
struct Glass {
    static var regular: Glass    // Default, medium transparency
    static var clear: Glass      // High transparency, for media overlays
    static var identity: Glass   // No effect, for conditional toggling

    func tint(_ color: Color) -> Glass
    func interactive() -> Glass
}
```

| Variant | Use |
|---------|-----|
| `.regular` | Toolbars, buttons, navigation elements |
| `.clear` | Overlays on photos/maps/video |
| `.identity` | Disable effect conditionally |

### Basic Usage

```swift
// Minimal
Text("Label")
    .padding()
    .glassEffect()

// With parameters
Text("Label")
    .padding()
    .glassEffect(.regular, in: .capsule, isEnabled: true)

// Tinted
Button("Primary") { }
    .glassEffect(.regular.tint(.blue))

// Interactive (adds scale, bounce, shimmer on tap)
// Only use on touch-responsive elements (buttons, controls)
Button("Tap Me") { }
    .glassEffect(.regular.interactive())
```

Modifiers chain in any order: `.regular.tint(.blue).interactive()` equals `.regular.interactive().tint(.blue)`.

### Shape Options

```swift
.glassEffect(.regular, in: .capsule)      // Default
.glassEffect(.regular, in: .circle)
.glassEffect(.regular, in: .ellipse)
.glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))
.glassEffect(.regular, in: .rect(cornerRadius: .containerConcentric))
```

Use `.containerConcentric` for corners that align with parent container across devices.

## GlassEffectContainer

Wraps multiple glass elements to share sampling region and enable morphing.

```swift
GlassEffectContainer {
    HStack(spacing: 20) {
        Button(action: {}) {
            Image(systemName: "pencil")
        }
        .frame(width: 44, height: 44)
        .glassEffect(.regular.interactive())

        Button(action: {}) {
            Image(systemName: "eraser")
        }
        .frame(width: 44, height: 44)
        .glassEffect(.regular.interactive())
    }
}
```

With custom spacing:

```swift
GlassEffectContainer(spacing: 40.0) {
    // elements
}
```

Glass cannot sample other glass. Without a shared container, nearby glass elements render inconsistently.

## Morphing Transitions

Elements morph between states when they share a `GlassEffectContainer` and use `glassEffectID`.

```swift
func glassEffectID<ID: Hashable>(
    _ id: ID,
    in namespace: Namespace.ID
) -> some View
```

### Example: Expandable Toolbar

```swift
struct ExpandableToolbar: View {
    @State private var isExpanded = false
    @Namespace private var namespace

    var body: some View {
        GlassEffectContainer(spacing: 30) {
            Button {
                withAnimation(.bouncy) {
                    isExpanded.toggle()
                }
            } label: {
                Image(systemName: isExpanded ? "xmark" : "plus")
            }
            .frame(width: 44, height: 44)
            .glassEffect(.regular.interactive())
            .glassEffectID("toggle", in: namespace)

            if isExpanded {
                Button { } label: {
                    Image(systemName: "pencil")
                }
                .frame(width: 44, height: 44)
                .glassEffect(.regular.interactive())
                .glassEffectID("pencil", in: namespace)

                Button { } label: {
                    Image(systemName: "trash")
                }
                .frame(width: 44, height: 44)
                .glassEffect(.regular.interactive())
                .glassEffectID("trash", in: namespace)
            }
        }
    }
}
```

Requirements for morphing:
1. Elements in same `GlassEffectContainer`
2. Each view has `glassEffectID` with shared namespace
3. Use `withAnimation` on state changes

## Text and Icons

SwiftUI automatically applies vibrant treatment for legibility on glass.

```swift
Text("Glass Label")
    .font(.title)
    .bold()
    .foregroundStyle(.white)
    .padding()
    .glassEffect()

Image(systemName: "heart.fill")
    .font(.largeTitle)
    .foregroundStyle(.white)
    .frame(width: 60, height: 60)
    .glassEffect(.regular.interactive())

Label("Settings", systemImage: "gear")
    .labelStyle(.iconOnly)
    .padding()
    .glassEffect()
```

## Guidelines

- Use native Liquid Glass APIs—avoid custom blur or material implementations
- Apply `.interactive()` only to touch-responsive elements, not static content
- Wrap related glass elements in `GlassEffectContainer` for visual consistency
- Always provide iOS 25 and earlier fallbacks using `.ultraThinMaterial`

## Known Issues

- **iOS 26.1**: Placing `Menu` inside `GlassEffectContainer` breaks morphing animation. Avoid until fixed.

## Quick Reference

| Task | Code |
|------|------|
| Basic glass | `.glassEffect()` |
| Tinted | `.glassEffect(.regular.tint(.blue))` |
| Interactive | `.glassEffect(.regular.interactive())` |
| Custom shape | `.glassEffect(.regular, in: .circle)` |
| Disable conditionally | `.glassEffect(.identity)` |
| Group elements | `GlassEffectContainer { }` |
| Enable morphing | `.glassEffectID("id", in: namespace)` |
