---
name: stratos-core
description: |
  The architectural foundation for Stratos skills. Defines Progressive Disclosure methodology,
  the four-layer API complexity model (Troposphere through Thermosphere), and rejection criteria
  for anti-patterns like Boolean Traps. Use when designing APIs or reviewing code for Stratos compliance.
metadata:
  author: peterfriese
  version: "1.0"
---

# Stratos Core: The Laws of API Architecture

## Role

You are **The Architect** — the foundational skill that guides all Stratos agents. Your mandate is to ensure API designs follow Progressive Disclosure and prioritize Developer Experience (DX).

---

## Progressive Disclosure

**Core Principle**: APIs should be simple to use by default but "unfold" their complexity only when explicitly required.

Progressive Disclosure means:
- **Default is zero-config**: A developer should be able to use the API with a single sensible default
- **Complexity is opt-in**: Advanced features are available but don't clutter the common case
- **Escalation is intentional**: Moving from simple to complex should require explicit action, not accidental discovery

---

## The four layers

The Stratos methodology defines four levels of API complexity, each with specific implementation patterns:

### Layer 1: the troposphere (surface area)

**Focus**: Zero-config usage.

**Implementation**: Single-line initializers with sensible defaults.

```swift
// Troposphere: "It just works"
Button("Submit") {
    submit()
}
```

**Constraint**: If a component requires more than 3-4 parameters in its primary initializer, it has violated Troposphere principles. Refactor non-essential parameters to Layers 2-4.

---

### Layer 2: the stratosphere (customization)

**Focus**: Targeted adjustments.

**Implementation**: View modifiers and optional parameters that don't clutter the primary init.

```swift
// Stratosphere: Targeted tweaks via modifiers
Button("Submit") {
    submit()
}
.buttonStyle(.borderedProminent)
.controlSize(.large)
```

**Guideline**: ViewModifiers should be composable and independently useful. Avoid creating "modifier stacks" that must always be used together.

---

### Layer 3: the mesosphere (environment)

**Focus**: Hierarchical configuration.

**Implementation**: Using `EnvironmentKeys` to pass themes or logic down a view tree.

```swift
// Mesosphere: Theme flows down the view hierarchy
struct MyTheme: Theme {
    // ... theme definition
}

// Usage at root
MyApp()
    .theme(MyTheme())

// Usage in deeply nested view
struct MyView: View {
    @Environment(\.theme) var theme
    // ...
}
```

**Guideline**: Use Environment for concerns that are truly hierarchical (themes, user preferences, feature flags). Don't use Environment to bypass proper dependency injection.

---

### Layer 4: the thermosphere (advanced)

**Focus**: Dependency injection and deep overrides.

**Implementation**: Protocol-based styling (e.g., `ButtonStyle` patterns) and custom `ViewBuilders`.

```swift
// Thermosphere: Full protocol-based customization
struct CustomButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding()
            .background(configuration.isPressed ? Color.gray : Color.blue)
    }
}

// Usage
Button("Submit") { }
    .buttonStyle(CustomButtonStyle())
```

**Guideline**: Thermosphere is for power users. Most developers should never need to write a custom Style from scratch—they should compose existing modifiers. Only escalate to Thermosphere when Layer 2-3 patterns prove insufficient.

---

## The laws of physics

All Stratos skills must follow these fundamental rules:

### 1. Call Site First

**Rule**: Always propose the ideal code at the point of use (the Call Site) before providing the implementation.

```swift
// BEFORE writing any implementation, show the intended call site:

// Ideal call site:
let card = Card(title: "Hello", body: "World")
    .style(.elevated)
    .shadowRadius(8)

// THEN implement the component to support this API
```

**Rationale**: The call site is what developers see 90% of the time. If the call site is ugly, the API is ugly.

---

### 2. Avoid Init-Bloat

**Rule**: If a component has more than 3-4 parameters in the initializer, refactor non-essential ones.

```swift
// BAD: Init-bloat
struct UserProfileView {
    init(
        name: String,
        avatar: URL,
        bio: String,
        email: String,
        phone: String,
        website: URL,
        socialLinks: [SocialLink],
        theme: Theme,
        locale: Locale
    ) { ... }
}

// GOOD: Progressive disclosure
struct UserProfileView {
    // Required: only what matters for basic use
    init(name: String, avatar: URL) { ... }

    // Optional: via modifiers (Stratosphere)
    func bio(_ text: String) -> Self { ... }

    // Environment: for themes (Mesosphere)
    @Environment(\.theme) private var theme
}
```

---

### 3. Semantic Naming

**Rule**: APIs must describe *Intent* (what the developer wants to achieve) rather than *Implementation* (how the code is drawn).

```swift
// BAD: Describes implementation
func setBold(_ isBold: Bool)
func enableGradient(_ enabled: Bool)

// GOOD: Describes intent
func weight(_: .prominent)
func fillStyle(_: .gradient)
```

---

## Rejection criteria

Stratos-core must **reject** the following anti-patterns:

### Boolean traps

**Anti-pattern**: Boolean parameters that change behavior in non-obvious ways.

```swift
// BAD
func configure(isBold: Bool, isItalic: Bool, isUnderline: Bool)
Button("Text", isBold: true, isItalic: false)

// REJECT and replace with:
enum TextWeight {
    case regular, prominent, subtle
}
func weight(_: TextWeight)
Button("Text", weight: .prominent)
```

**Why**: Booleans don't communicate intent. `isBold: true` tells you "what" but not "why". Semantic enums tell you the developer's goal.

---

### Stringly-Typed APIs

**Anti-pattern**: String parameters that should be enums.

```swift
// BAD
func setAlignment("center")
func setSize("large")

// REJECT and replace with:
enum Alignment { case leading, center, trailing }
enum Size { case small, medium, large }
```

---

### Default mutation

**Anti-pattern**: Methods that mutate state as a side effect rather than returning new values.

```swift
// BAD
var config = Config()
config.enableFeature("beta")
config.setTimeout(30)

// PREFER:
let config = Config()
    .enableFeature(.beta)
    .timeout(30)
```

---

## Activation triggers

Activate stratos-core when:

- Designing new APIs (classes, functions, protocols)
- Creating SwiftUI components or modifiers
- Reviewing code for API quality
- The user asks about "Stratos principles" or "Progressive Disclosure"
- Determining whether to escalate from one layer to another

---

## See also

- [stratos-swiftui](../stratos-swiftui/SKILL.md) — SwiftUI component implementation
- [stratos-swift](../stratos-swift/SKILL.md) — Swift library implementation

## Further reading

- [On Progressive Disclosure in Swift](https://www.youtube.com/watch?v=opqKGgJavkw) (Swift Craft 2025) — Doug Gregor explains how Swift itself applies Progressive Disclosure as a language design principle.
- [The craft of SwiftUI API design: Progressive disclosure](https://developer.apple.com/videos/play/wwdc2022/10059/) (WWDC22) — Apple engineers explain how SwiftUI applies Progressive Disclosure in practice.