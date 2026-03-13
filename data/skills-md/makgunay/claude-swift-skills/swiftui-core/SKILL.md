---
name: swiftui-core
description: Core SwiftUI patterns for macOS and iOS development including navigation (NavigationSplitView, NavigationStack), state management (@State, @Binding, @Environment, @Bindable with @Observable), the new customizable toolbar system (toolbar IDs, ToolbarSpacer, DefaultToolbarItem, searchToolbarBehavior, matchedTransitionSource, sharedBackgroundVisibility), styled text editing (TextEditor with AttributedString, AttributedTextSelection, transformAttributes, textFormattingDefinition), and layout patterns. Use when building any SwiftUI view, implementing navigation, managing state, creating toolbars, or building rich text editors. Corrects common LLM errors like using deprecated NavigationView, wrong state wrappers, and outdated toolbar APIs.
---

# SwiftUI Core Patterns

Modern SwiftUI patterns for views, navigation, state, toolbars, and text editing.

## Critical Constraints

- ❌ `NavigationView` → ✅ `NavigationSplitView` (sidebar/detail) or `NavigationStack` (push/pop)
- ❌ `@StateObject` → ✅ `@State` with `@Observable` classes (macOS 14+)
- ❌ `@ObservedObject` → ✅ direct property or `@Bindable` for bindings
- ❌ `@EnvironmentObject` → ✅ `@Environment` with custom key
- ❌ `toolbar { }` without IDs for customizable toolbars → ✅ `toolbar(id:)` with `ToolbarItem(id:)`
- ❌ Old `.searchable` without behavior → ✅ Add `.searchToolbarBehavior(.minimize)` for space efficiency
- ❌ Plain `String` in `TextEditor` for rich text → ✅ Use `AttributedString` binding

## Reference Index

| File | When to Use |
|------|-------------|
| `references/toolbars.md` | Customizable toolbars, search integration, spacers, transitions |
| `references/text-editing.md` | TextEditor + AttributedString, selection, formatting toolbar |
| `references/attributed-string.md` | AttributedString API, text alignment, line height, writing direction |

## Navigation Patterns

### Sidebar + Detail (macOS preferred)
```swift
NavigationSplitView {
    List(selection: $selectedItem) {
        ForEach(items) { item in
            NavigationLink(value: item) { Label(item.name, systemImage: item.icon) }
        }
    }
    .navigationTitle("Items")
} detail: {
    if let selectedItem {
        DetailView(item: selectedItem)
    } else {
        ContentUnavailableView("Select an item", systemImage: "sidebar.left")
    }
}
```

### Push Navigation (iOS preferred)
```swift
NavigationStack(path: $path) {
    List(items) { item in
        NavigationLink(value: item) { Text(item.name) }
    }
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

## State Management Quick Reference

| Need | macOS 14+ / iOS 17+ | Older targets |
|------|---------------------|---------------|
| View owns mutable state | `@State` | `@State` (value) / `@StateObject` (object) |
| View receives object | plain property | `@ObservedObject` |
| View needs binding | `@Bindable var model` | `@ObservedObject var model` |
| Shared via environment | `@Environment(\.key)` | `@EnvironmentObject` |
| View-local value | `@State private var` | `@State private var` |

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| `NavigationView { }` | `NavigationSplitView { } detail: { }` or `NavigationStack { }` |
| `.toolbar { ToolbarItem { } }` for customizable | `.toolbar(id: "myToolbar") { ToolbarItem(id: "action") { } }` |
| Using `NavigationLink(destination:)` | Use `NavigationLink(value:)` + `.navigationDestination(for:)` |
| `TextField` for rich text | `TextEditor(text: $attributedString, selection: $selection)` |
| `.sheet(isPresented:)` without transition | Add `.matchedTransitionSource` + `.navigationTransition(.zoom)` |

## References

- [What's new in SwiftUI (WWDC 2025)](https://developer.apple.com/videos/play/wwdc2025/256/)
- [SwiftUI Documentation](https://developer.apple.com/documentation/SwiftUI)
