---
name: swiftui-expert
version: 1.0.0
description: Write, review, or improve SwiftUI code following best practices
  for state management, view composition, performance, and modern APIs.
  Use when building SwiftUI features, refactoring views, reviewing code quality,
  or adopting modern SwiftUI patterns.
author: SwiftyJourney
tags:
  - swiftui
  - ios
  - apple
  - state-management
  - view-composition
  - performance
  - animations
  - swift
---

# SwiftUI Expert Skill

## Overview

Use this skill to build, review, or improve SwiftUI features with correct state management, modern API usage, Swift concurrency best practices, optimal view composition, and iOS 26+ Liquid Glass styling. Prioritize native APIs, Apple design guidance, and performance-conscious patterns. This skill focuses on facts and best practices without enforcing specific architectural patterns.

For architectural decisions (MVVM, MVC, VIPER, Clean Architecture, Coordinator, two-layer view patterns), defer to the `architecture-design-skill`.

---

## Workflow Decision Tree

### 1) Review existing SwiftUI code
- Check property wrapper usage against the selection guide (see `references/state-management.md`)
- Verify modern API usage (see `references/modern-apis.md`)
- Verify view composition follows extraction rules (see `references/view-composition.md`)
- Check performance patterns are applied (see `references/performance-patterns.md`)
- Verify list patterns use stable identity (see `references/list-patterns.md`)
- Check animation patterns for correctness (see `references/animation-basics.md`, `references/animation-transitions.md`)
- Inspect Liquid Glass usage for correctness (see `references/liquid-glass.md`)

### 2) Improve existing SwiftUI code
- Audit state management for correct wrapper selection (prefer `@Observable` over `ObservableObject`)
- Replace deprecated APIs with modern equivalents (see `references/modern-apis.md`)
- Extract complex views into separate subviews (see `references/view-composition.md`)
- Refactor hot paths to minimize redundant state updates (see `references/performance-patterns.md`)
- Ensure ForEach uses stable identity (see `references/list-patterns.md`)
- Improve animation patterns (see `references/animation-basics.md`, `references/animation-transitions.md`)
- Suggest image downsampling when `UIImage(data:)` is used (optional, see `references/image-optimization.md`)
- Adopt Liquid Glass only when explicitly requested by the user

### 3) Implement new SwiftUI feature
- Design data flow first: identify owned vs injected state (see `references/state-management.md`)
- Use modern APIs (no deprecated modifiers or patterns, see `references/modern-apis.md`)
- Use `@Observable` for shared state (with `@MainActor` if not using default actor isolation)
- Structure views for optimal diffing: extract subviews early, keep views small (see `references/view-composition.md`)
- Separate business logic into testable models when needed (see `references/state-management.md#when-to-use-a-viewmodel`)
- Use correct animation patterns (see `references/animation-basics.md`, `references/animation-transitions.md`, `references/animation-advanced.md`)
- Apply glass effects after layout/appearance modifiers (see `references/liquid-glass.md`)
- Gate iOS 26+ features with `#available` and provide fallbacks

---

## Core Guidelines

### State Management
- **Always prefer `@Observable` over `ObservableObject`** for new code
- **Mark `@Observable` classes with `@MainActor`** unless using default actor isolation
- **Always mark `@State` and `@StateObject` as `private`** (makes dependencies clear)
- **Never declare passed values as `@State` or `@StateObject`** (they only accept initial values)
- Use `@State` with `@Observable` classes (not `@StateObject`)
- `@Binding` only when child needs to **modify** parent state
- `@Bindable` for injected `@Observable` objects needing bindings
- Use `let` for read-only values; `var` + `.onChange()` for reactive reads
- Legacy: `@StateObject` for owned `ObservableObject`; `@ObservedObject` for injected
- Nested `ObservableObject` doesn't work (pass nested objects directly); `@Observable` handles nesting fine

### When to Use a ViewModel
Use a separate model class (often called a ViewModel) when:
- **Testability**: you need to unit-test state transitions or business logic
- **Complex state**: multiple interdependent state properties that evolve together
- **Async coordination**: orchestrating multiple async operations with loading/error state
- **Reuse across views**: the same logic is needed in more than one view

For simple views with straightforward display logic, keeping `@State` directly in the view is fine and often cleaner.

This is a practical guide, not an MVVM mandate — see `architecture-design-skill` if you need to decide on an app-wide architectural pattern.

### View Composition
- **Prefer modifiers over conditional views** for state changes (maintains view identity)
- Extract complex views into separate `struct` subviews for performance (not `@ViewBuilder` functions)
- Keep views small; each view should have one clear responsibility
- Keep view `body` simple and pure (no side effects or complex logic)
- Use `@ViewBuilder` functions only for small, simple sections
- Prefer `@ViewBuilder let content: Content` over closure-based content properties in containers
- Use specialized built-in components when they fit: `Label`, `GroupBox`, `Form`, `Section`
- Build custom view styles (`ButtonStyle`, `LabelStyle`) to reuse styling across instances
- Action handlers should reference methods, not contain inline logic
- Use relative layout over hard-coded constants
- Views should work in any context (don't assume screen size or presentation style)

### Reusability Recommendation
Prefer passing primitive/value types to presentational (content) views rather than full model objects. This makes views more reusable, simplifies previews, and reduces dependencies.

```swift
// Preferred for pure display views
struct UserRow: View {
    let name: String
    let avatarURL: URL?
    let isOnline: Bool
}

// Acceptable when the view needs the full model or has bindings to it
struct UserEditor: View {
    @Bindable var user: UserModel
}
```

This is a recommendation for reusability, not a strict rule. Views that edit or coordinate model state often need the model directly.

### Modern APIs
- Use `foregroundStyle()` instead of `foregroundColor()`
- Use `clipShape(.rect(cornerRadius:))` instead of `cornerRadius()`
- Use `Tab` API instead of `tabItem()` (iOS 18+)
- Use `Button` instead of `onTapGesture()` (unless need location/count)
- Use `NavigationStack` instead of `NavigationView`
- Use `navigationDestination(for:)` for type-safe navigation
- Use two-parameter or no-parameter `onChange()` variant
- Use `ImageRenderer` for rendering SwiftUI views
- Use `.sheet(item:)` instead of `.sheet(isPresented:)` for model-based content
- Sheets should own their actions and call `dismiss()` internally
- Use `ScrollViewReader` for programmatic scrolling with stable IDs
- Avoid `UIScreen.main.bounds` for sizing
- Avoid `GeometryReader` when alternatives exist (e.g., `containerRelativeFrame()`)

### Swift Best Practices
- Use modern Text formatting (`.format` parameters, not `String(format:)`)
- Use `localizedStandardContains()` for user-input filtering (not `contains()`)
- Prefer static member lookup (`.blue` vs `Color.blue`)
- Use `.task` modifier for automatic cancellation of async work
- Use `.task(id:)` for value-dependent tasks

### Performance
- Pass only needed values to views (avoid large "config" or "context" objects)
- Eliminate unnecessary dependencies to reduce update fan-out
- Check for value changes before assigning state in hot paths
- Avoid redundant state updates in `onReceive`, `onChange`, scroll handlers
- Minimize work in frequently executed code paths
- Use `LazyVStack`/`LazyHStack` for large lists
- Use stable identity for `ForEach` (never `.indices` for dynamic content)
- Ensure constant number of views per `ForEach` element
- Avoid inline filtering in `ForEach` (prefilter and cache)
- Avoid `AnyView` in list rows
- Consider POD views for fast diffing (or wrap expensive views in POD parents)
- Suggest image downsampling when `UIImage(data:)` is encountered (optional optimization)
- Avoid layout thrash (deep hierarchies, excessive `GeometryReader`)
- Gate frequent geometry updates by thresholds
- Use `Self._printChanges()` to debug unexpected view updates

### Animations
- Use `.animation(_:value:)` with value parameter (deprecated version without value is too broad)
- Use `withAnimation` for event-driven animations (button taps, gestures)
- Prefer transforms (`offset`, `scale`, `rotation`) over layout changes (`frame`) for performance
- Transitions require animations outside the conditional structure
- Custom `Animatable` implementations must have explicit `animatableData`
- Use `.phaseAnimator` for multi-step sequences (iOS 17+)
- Use `.keyframeAnimator` for precise timing control (iOS 17+)
- Animation completion handlers need `.transaction(value:)` for reexecution
- Implicit animations override explicit animations (later in view tree wins)

### Liquid Glass (iOS 26+)
**Only adopt when explicitly requested by the user.**
- Use native `glassEffect`, `GlassEffectContainer`, and glass button styles
- Wrap multiple glass elements in `GlassEffectContainer`
- Apply `.glassEffect()` after layout and visual modifiers
- Use `.interactive()` only for tappable/focusable elements
- Use `glassEffectID` with `@Namespace` for morphing transitions

---

## Quick Reference

### Property Wrapper Selection (Modern)
| Wrapper | Use When |
|---------|----------|
| `@State` | Internal view state (must be `private`), or owned `@Observable` class |
| `@Binding` | Child modifies parent's state |
| `@Bindable` | Injected `@Observable` needing bindings |
| `let` | Read-only value from parent |
| `var` | Read-only value watched via `.onChange()` |

**Legacy (Pre-iOS 17):**
| Wrapper | Use When |
|---------|----------|
| `@StateObject` | View owns an `ObservableObject` (use `@State` with `@Observable` instead) |
| `@ObservedObject` | View receives an `ObservableObject` |

### Modern API Replacements
| Deprecated | Modern Alternative |
|------------|-------------------|
| `foregroundColor()` | `foregroundStyle()` |
| `cornerRadius()` | `clipShape(.rect(cornerRadius:))` |
| `tabItem()` | `Tab` API (iOS 18+) |
| `onTapGesture()` | `Button` (unless need location/count) |
| `NavigationView` | `NavigationStack` |
| `onChange(of:) { value in }` | `onChange(of:) { old, new in }` or `onChange(of:) { }` |
| `fontWeight(.bold)` | `bold()` |
| `GeometryReader` | `containerRelativeFrame()` or `visualEffect()` |
| `showsIndicators: false` | `.scrollIndicators(.hidden)` |
| `String(format: "%.2f", value)` | `Text(value, format: .number.precision(.fractionLength(2)))` |
| `string.contains(search)` | `string.localizedStandardContains(search)` (for user input) |

### Liquid Glass Patterns
```swift
// Basic glass effect with fallback
if #available(iOS 26, *) {
    content
        .padding()
        .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))
} else {
    content
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}

// Grouped glass elements
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        GlassButton1()
        GlassButton2()
    }
}

// Glass buttons
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```

---

## Review Checklist

### State Management
- [ ] Using `@Observable` instead of `ObservableObject` for new code
- [ ] `@Observable` classes marked with `@MainActor` (if needed)
- [ ] Using `@State` with `@Observable` classes (not `@StateObject`)
- [ ] `@State` and `@StateObject` properties are `private`
- [ ] Passed values NOT declared as `@State` or `@StateObject`
- [ ] `@Binding` only where child modifies parent state
- [ ] `@Bindable` for injected `@Observable` needing bindings
- [ ] Nested `ObservableObject` avoided (or passed directly to child views)
- [ ] ViewModel used only when testability or complex state warrants it

### Modern APIs (see `references/modern-apis.md`)
- [ ] Using `foregroundStyle()` instead of `foregroundColor()`
- [ ] Using `clipShape(.rect(cornerRadius:))` instead of `cornerRadius()`
- [ ] Using `Tab` API instead of `tabItem()` (iOS 18+)
- [ ] Using `Button` instead of `onTapGesture()` (unless need location/count)
- [ ] Using `NavigationStack` instead of `NavigationView`
- [ ] Avoiding `UIScreen.main.bounds`
- [ ] Using alternatives to `GeometryReader` when possible
- [ ] Button images include text labels for accessibility

### Sheets & Navigation (see `references/navigation-patterns.md`)
- [ ] Using `.sheet(item:)` for model-based sheets
- [ ] Sheets own their actions and dismiss internally
- [ ] Using `navigationDestination(for:)` for type-safe navigation

### ScrollView (see `references/scroll-patterns.md`)
- [ ] Using `ScrollViewReader` with stable IDs for programmatic scrolling
- [ ] Using `.scrollIndicators(.hidden)` instead of initializer parameter

### Text & Formatting (see `references/text-formatting.md`)
- [ ] Using modern Text formatting (not `String(format:)`)
- [ ] Using `localizedStandardContains()` for search filtering

### View Composition (see `references/view-composition.md`)
- [ ] Using modifiers instead of conditionals for state changes
- [ ] Complex views extracted to separate subviews (not `@ViewBuilder` functions)
- [ ] Views kept small with one responsibility
- [ ] Container views use `@ViewBuilder let content: Content`
- [ ] Specialized built-ins used where appropriate (Label, GroupBox, Form)
- [ ] Custom styles used to share visual patterns across instances
- [ ] Presentational views prefer primitive parameters (reusability recommendation)

### Performance (see `references/performance-patterns.md`)
- [ ] View `body` kept simple and pure (no side effects)
- [ ] Passing only needed values (not large config objects)
- [ ] Eliminating unnecessary dependencies
- [ ] State updates check for value changes before assigning
- [ ] Hot paths minimize state updates
- [ ] No object creation in `body`
- [ ] Heavy computation moved out of `body`

### List Patterns (see `references/list-patterns.md`)
- [ ] ForEach uses stable identity (not `.indices`)
- [ ] Constant number of views per ForEach element
- [ ] No inline filtering in ForEach
- [ ] No `AnyView` in list rows

### Layout (see `references/view-composition.md`)
- [ ] Avoiding layout thrash (deep hierarchies, excessive GeometryReader)
- [ ] Gating frequent geometry updates by thresholds
- [ ] Business logic separated into testable models (when warranted)
- [ ] Action handlers reference methods (not inline logic)
- [ ] Using relative layout (not hard-coded constants)
- [ ] Views work in any context (context-agnostic)

### Animations (see `references/animation-basics.md`, `references/animation-transitions.md`, `references/animation-advanced.md`)
- [ ] Using `.animation(_:value:)` with value parameter
- [ ] Using `withAnimation` for event-driven animations
- [ ] Transitions paired with animations outside conditional structure
- [ ] Custom `Animatable` has explicit `animatableData` implementation
- [ ] Preferring transforms over layout changes for animation performance
- [ ] Phase animations for multi-step sequences (iOS 17+)
- [ ] Keyframe animations for precise timing (iOS 17+)
- [ ] Completion handlers use `.transaction(value:)` for reexecution

### Liquid Glass (iOS 26+)
- [ ] `#available(iOS 26, *)` with fallback for Liquid Glass
- [ ] Multiple glass views wrapped in `GlassEffectContainer`
- [ ] `.glassEffect()` applied after layout/appearance modifiers
- [ ] `.interactive()` only on user-interactable elements
- [ ] Shapes and tints consistent across related elements

---

## References
- `references/state-management.md` — Property wrappers, data flow, when to use a ViewModel
- `references/view-composition.md` — View extraction, styles, specialized views, reusability
- `references/performance-patterns.md` — Performance optimization techniques and anti-patterns
- `references/list-patterns.md` — ForEach identity, stability, and list best practices
- `references/modern-apis.md` — Modern API usage and deprecated replacements
- `references/animation-basics.md` — Core animation concepts, implicit/explicit animations
- `references/animation-transitions.md` — Transitions, custom transitions, Animatable protocol
- `references/animation-advanced.md` — Transactions, phase/keyframe animations, completion handlers
- `references/navigation-patterns.md` — Sheet presentation and navigation patterns
- `references/scroll-patterns.md` — ScrollView patterns and programmatic scrolling
- `references/text-formatting.md` — Modern text formatting and string operations
- `references/image-optimization.md` — AsyncImage, image downsampling, and optimization
- `references/liquid-glass.md` — iOS 26+ Liquid Glass API (adopt only when explicitly requested)

---

## Philosophy

This skill focuses on **facts and best practices**, not architectural opinions:
- We don't enforce specific architectures (e.g., MVVM, VIPER) — see `architecture-design-skill`
- We do encourage separating business logic for testability when warranted
- We prioritize modern APIs over deprecated ones
- We emphasize thread safety with `@MainActor` and `@Observable`
- We optimize for performance and maintainability
- We follow Apple's Human Interface Guidelines and API design patterns
- We use "prefer"/"avoid" for recommendations; "always"/"never" only for correctness of API
