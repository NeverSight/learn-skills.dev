---
name: liquid-glass
description: Comprehensive guide to Apple's Liquid Glass design system introduced in macOS 26, iOS 26, and across all Apple platforms. Covers SwiftUI (.glassEffect(), GlassEffectContainer, .interactive(), .tint(), glassEffectID morphing, .buttonStyle(.glass), .buttonStyle(.glassProminent), glassEffectUnion), AppKit (NSGlassEffectView, NSGlassEffectContainerView), UIKit (UIGlassEffect, UIGlassContainerEffect, UIScrollEdgeEffect), and WidgetKit (accented rendering mode, widgetAccentable). Use whenever building UI with the new Apple design language, adopting glass effects, styling buttons or toolbars, or creating modern macOS/iOS interfaces. Always consult this skill when asked about new Apple design.
---

# Liquid Glass Design System

Apple's new material design combining glass optics with fluid interaction. Available across all platforms.

## Quick Reference — SwiftUI

```swift
// Basic glass effect (capsule shape by default)
view.glassEffect()

// Custom shape
view.glassEffect(in: .rect(cornerRadius: 16))
view.glassEffect(in: .circle)

// Tinted glass (suggests prominence)
view.glassEffect(.regular.tint(.blue))

// Interactive (responds to touch/pointer)
view.glassEffect(.regular.interactive())

// Button styles
Button("Primary") { }.buttonStyle(.glassProminent)
Button("Secondary") { }.buttonStyle(.glass)

// Container for multiple glass views (required for merging/performance)
GlassEffectContainer(spacing: 40) {
    HStack(spacing: 40) {
        ItemView().glassEffect()
        ItemView().glassEffect()
    }
}

// Morphing transitions between glass views
@Namespace var ns
view.glassEffect().glassEffectID("myID", in: ns)

// Unite multiple views into single glass shape
view.glassEffect().glassEffectUnion(id: "group1", namespace: ns)
```

## Critical Constraints

- ❌ DO NOT apply multiple glass effects without `GlassEffectContainer` → ✅ Wrap in `GlassEffectContainer` for performance and merging
- ❌ DO NOT forget `.interactive()` on buttons/controls → ✅ Add `.interactive()` for touch/pointer response
- ❌ DO NOT use heavy tint alpha values → ✅ Use subtle tints (0.2–0.3 alpha) for glass aesthetic
- ❌ DO NOT apply `.glassEffect()` before layout modifiers → ✅ Apply after `.frame()`, `.padding()`, etc.
- ❌ DO NOT use old `NSVisualEffectView` with `.material` for new designs → ✅ Use `NSGlassEffectView` (AppKit) or `.glassEffect()` (SwiftUI)

## Reference Index

| File | When to Use |
|------|-------------|
| `references/swiftui-glass.md` | SwiftUI glass effects, containers, morphing, button styles |
| `references/appkit-glass.md` | AppKit NSGlassEffectView, NSGlassEffectContainerView, hover effects |
| `references/uikit-glass.md` | UIKit UIGlassEffect, scroll edge effects, container effects |
| `references/widgetkit-glass.md` | Widget accented rendering mode, widgetAccentable modifier |

## Decision Tree

```
Building SwiftUI interface?
├── Single glass element → .glassEffect() on the view
├── Multiple glass elements → Wrap in GlassEffectContainer
├── Need morphing transitions → Use @Namespace + .glassEffectID()
├── Grouping elements into one shape → Use .glassEffectUnion()
└── Buttons → .buttonStyle(.glass) or .buttonStyle(.glassProminent)

Building AppKit interface?
├── Single glass element → NSGlassEffectView with contentView
├── Multiple glass elements → NSGlassEffectContainerView
└── Hover/interaction → NSTrackingArea + animator().tintColor

Building Widgets?
├── Support tinted/clear appearance → Check widgetRenderingMode
├── Mark accent content → .widgetAccentable()
└── Custom glass in widget → .glassEffect() (same as SwiftUI)
```

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Glass views don't merge when close | Wrap in `GlassEffectContainer` with appropriate `spacing` |
| No animation when glass appears/disappears | Use `withAnimation { }` + `glassEffectID` |
| Glass button doesn't respond to hover | Add `.interactive()` to the glass effect |
| Too many glass effects = performance drop | Limit glass effects; use `GlassEffectContainer` |
| Widget looks wrong in tinted mode | Check `widgetRenderingMode` environment, use `widgetAccentable()` |

## References

- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [Landmarks: Building an app with Liquid Glass](https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass)
- [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass)
- [WWDC 2025: Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/)
