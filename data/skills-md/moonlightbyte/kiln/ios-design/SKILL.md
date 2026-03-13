---
name: ios-design
description: |
  This skill should be used when the user asks to "audit iOS code", "review SwiftUI",
  "check HIG compliance", "critique SwiftUI design", "verify Human Interface Guidelines",
  "audit SwiftUI screen", "review iOS UI", "check Apple guidelines", "validate iOS design",
  "fix SwiftUI anti-patterns", "improve SwiftUI performance", "review iOS screen",
  "audit Swift UI", "check safe areas", "verify accessibility iOS",
  or mentions "Human Interface Guidelines", "HIG", "SwiftUI", "iOS UI", "SwiftUI patterns",
  "view identity", "property wrappers", "iOS accessibility", "WCAG iOS", "Dynamic Type".

  This skill should also be used when the user reports symptoms like "Why is my list slow?",
  "Scroll stutters", "Make this feel like a native iOS app", "Safe area problems",
  "Build a settings screen", "SwiftUI performance", "View keeps updating",
  or "Memory leak in my view".

  Provides comprehensive Apple HIG specifications, SwiftUI anti-patterns database,
  typography scale, semantic colors, safe areas, and severity-based audit checklists.
license: MIT
user-invocable: true
references:
  - ./reference/swiftui-antipatterns.md
  - ./reference/wwdc-demystify-swiftui.md
  - ./reference/property-wrapper-rules.md
  - ./reference/icecubes-patterns.md
  - ./reference/ios18-materials-api.md
---

# iOS Design Skill

Expert knowledge of Apple Human Interface Guidelines for SwiftUI applications. This skill enforces design excellence, accessibility compliance, and iOS-native feel.

## Core Principles

### 1. iOS Native Feel
- Use system colors and semantic tokens
- Follow Dynamic Type for text scaling
- Respect Safe Areas and notches
- Support both light and dark mode

### 2. Accessibility First
- Minimum 44x44pt touch targets
- 4.5:1 contrast ratio for normal text
- Proper `accessibilityLabel` on all interactive elements
- Support Dynamic Type up to AX5 (largest accessibility sizes)

### 3. SwiftUI Best Practices
- Use correct property wrappers (@State, @StateObject, @ObservedObject)
- Prefer declarative patterns
- Avoid AnyView type erasure
- Provide stable IDs in ForEach

---

## Typography Scale (11 Styles)

| Style | Size (Default) | Weight | Use Case |
|-------|----------------|--------|----------|
| `.largeTitle` | 34pt | Regular | Hero headlines |
| `.title` | 28pt | Regular | Page titles |
| `.title2` | 22pt | Regular | Section headers |
| `.title3` | 20pt | Regular | Subsection headers |
| `.headline` | 17pt | Semibold | Emphasized body |
| `.body` | 17pt | Regular | Main content |
| `.callout` | 16pt | Regular | Secondary content |
| `.subheadline` | 15pt | Regular | Supporting text |
| `.footnote` | 13pt | Regular | Metadata |
| `.caption` | 12pt | Regular | Captions |
| `.caption2` | 11pt | Regular | Small labels |

### Usage Pattern
```swift
// GOOD - System text styles
Text("Welcome")
    .font(.largeTitle)

// BAD - Hardcoded sizes
Text("Welcome")
    .font(.system(size: 34))
```

### Dynamic Type Support
```swift
// Automatic scaling with system styles
Text("Body text")
    .font(.body)

// Custom sizes that scale
@ScaledMetric(relativeTo: .body) var iconSize: CGFloat = 24

Image(systemName: "star.fill")
    .frame(width: iconSize, height: iconSize)
```

---

## Color System

### Semantic Colors
| Token | Light | Dark | Use Case |
|-------|-------|------|----------|
| `.label` | Black | White | Primary text |
| `.secondaryLabel` | Gray | Light gray | Secondary text |
| `.tertiaryLabel` | Light gray | Darker gray | Tertiary text |
| `.quaternaryLabel` | Lighter gray | Darkest gray | Disabled text |
| `.systemBackground` | White | Black | Primary background |
| `.secondarySystemBackground` | Light gray | Dark gray | Grouped content |
| `.tertiarySystemBackground` | White | Darker gray | Elevated content |
| `.separator` | Light gray | Dark gray | Dividers |
| `.link` | System blue | System blue | Interactive links |

### System Colors
| Color | Use Case |
|-------|----------|
| `.accentColor` | Primary interactive elements |
| `.red` | Destructive actions, errors |
| `.orange` | Warnings |
| `.yellow` | Caution |
| `.green` | Success, positive |
| `.blue` | Default interactive |
| `.purple` | Special features |
| `.pink` | Playful accents |

### Usage Pattern
```swift
// GOOD - Semantic colors
Text("Primary content")
    .foregroundColor(.label)

VStack {
    // content
}
.background(Color(.systemBackground))

// BAD - Hardcoded colors
Text("Primary content")
    .foregroundColor(.black)

VStack {
    // content
}
.background(Color.white)
```

---

## Touch Targets

### Requirements
- **Minimum**: 44x44pt (Apple HIG requirement)
- **Bottom navigation**: 46-50pt recommended
- **Spacing**: 8pt minimum between targets

### Implementation
```swift
// GOOD - System button provides proper touch target
Button(action: { /* action */ }) {
    Image(systemName: "xmark")
}

// GOOD - Custom with proper frame
Image(systemName: "xmark")
    .frame(width: 44, height: 44)
    .contentShape(Rectangle())
    .onTapGesture { /* action */ }

// BAD - Too small
Image(systemName: "xmark")
    .font(.system(size: 16))
    .onTapGesture { /* action */ }
```

---

## Safe Areas

### Respecting Safe Areas
```swift
// GOOD - Content respects safe areas
ScrollView {
    content
}
.safeAreaInset(edge: .bottom) {
    bottomBar
}

// Full-bleed backgrounds that extend into safe areas
ZStack {
    Color.blue.ignoresSafeArea()

    VStack {
        content // Content still respects safe areas
    }
}
```

### Device-Specific Considerations
| Device | Top Safe Area | Bottom Safe Area |
|--------|---------------|------------------|
| iPhone (notch) | 47pt | 34pt |
| iPhone (Dynamic Island) | 59pt | 34pt |
| iPhone SE | 20pt | 0pt |
| iPad | 20pt | 0pt |

---

## Spacing Scale

Base unit: 4pt

| Size | pt | Use Case |
|------|-----|----------|
| xs | 4pt | Inline spacing |
| sm | 8pt | Related elements |
| md | 12pt | Group spacing |
| lg | 16pt | Section spacing |
| xl | 20pt | Major divisions |
| 2xl | 24pt | Page margins (compact) |
| 3xl | 32pt | Large gaps |

### Standard Margins
| Context | Margin |
|---------|--------|
| Compact width | 16pt |
| Regular width | 20pt |
| List insets | 16pt leading, 20pt trailing |

---

## DO / DON'T

### Property Wrappers

**DO**: Use @StateObject for owned objects
```swift
struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()

    var body: some View {
        Text(viewModel.text)
    }
}
```

**DON'T**: Use @ObservedObject for owned objects
```swift
struct ContentView: View {
    @ObservedObject var viewModel = ContentViewModel() // Re-created on every view update!

    var body: some View {
        Text(viewModel.text)
    }
}
```

### List Performance

**DO**: Use LazyVStack/List for long content
```swift
ScrollView {
    LazyVStack {
        ForEach(items, id: \.id) { item in
            ItemRow(item: item)
        }
    }
}
```

**DON'T**: Use VStack for many items
```swift
ScrollView {
    VStack { // All items created at once
        ForEach(items, id: \.id) { item in
            ItemRow(item: item)
        }
    }
}
```

### View Identity

**DO**: Provide stable IDs in ForEach
```swift
ForEach(items, id: \.id) { item in
    ItemRow(item: item)
}
```

**DON'T**: Use indices or miss id parameter
```swift
ForEach(items.indices, id: \.self) { index in // Breaks on reorder
    ItemRow(item: items[index])
}
```

### Type Erasure

**DO**: Use @ViewBuilder or concrete types
```swift
@ViewBuilder
var content: some View {
    if condition {
        Text("A")
    } else {
        Image(systemName: "star")
    }
}
```

**DON'T**: Use AnyView excessively
```swift
var content: AnyView { // Kills performance
    if condition {
        return AnyView(Text("A"))
    } else {
        return AnyView(Image(systemName: "star"))
    }
}
```

### Modifier Order

**DO**: Background before padding, frame before overlay
```swift
Text("Hello")
    .padding()
    .background(Color.blue) // Includes padding in background

Text("World")
    .frame(maxWidth: .infinity)
    .overlay(alignment: .trailing) { // Overlay spans full width
        Button("Edit") { }
    }
```

**DON'T**: Wrong order causes unexpected results
```swift
Text("Hello")
    .background(Color.blue) // Only behind text
    .padding() // Padding outside background

Text("World")
    .overlay(alignment: .trailing) { // Overlay only covers text width
        Button("Edit") { }
    }
    .frame(maxWidth: .infinity)
```

---

## Severity Levels

When auditing, classify issues as:

| Level | Icon | Description | Example |
|-------|------|-------------|---------|
| **Critical** | 🔴 | Blocks accessibility or causes crashes | Missing accessibilityLabel |
| **Important** | 🟠 | Violates HIG or hurts UX | Touch target < 44pt |
| **Warning** | 🟡 | Suboptimal but functional | Hardcoded color |
| **Suggestion** | 🔵 | Polish opportunities | Non-standard spacing |

---

## Expert References

### SwiftUI Architecture & Patterns
- [WWDC 2021: Demystify SwiftUI](./reference/wwdc-demystify-swiftui.md) - View identity, lifetime, dependencies
- [Property Wrapper Decision Tree](./reference/property-wrapper-rules.md) - @State, @StateObject, @Observable, @Binding rules + scanner patterns
- [IceCubesApp Production Patterns](./reference/icecubes-patterns.md) - Real-world patterns from largest open-source SwiftUI app

### Modern iOS 18 Features
- [iOS 18 Materials & Glass Effects](./reference/ios18-materials-api.md) - Material API, glass morphism, liquid glass design

### Anti-Patterns & Scanning
- [Anti-Patterns Database](./reference/swiftui-antipatterns.md) - 23 patterns with regex scanners for automated audits
