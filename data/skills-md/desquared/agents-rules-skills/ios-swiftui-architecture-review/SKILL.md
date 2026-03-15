---
name: ios-swiftui-architecture-review
description: Analyze SwiftUI view hierarchies and suggest MVVM or other architectural improvements. Use when **reviewing existing SwiftUI code**, creating new SwiftUI components, analyzing view structure, or when the user asks about SwiftUI architecture patterns. Best for code review and refactoring guidance.
---

# SwiftUI Architecture Review

> **When to Use This Skill:**
> - Reviewing EXISTING SwiftUI views/ViewModels
> - Code review for architectural violations
> - Refactoring guidance for specific files
> - Validating state management patterns
>
> **When to Use `project-architecture-analyst` Agent Instead:**
> - Planning NEW features (uncertain file placement)
> - Understanding project-wide architecture
> - Major changes affecting multiple modules
> - Need to discover existing patterns before implementing

## Review Checklist

### Separation of Concerns
- [ ] Views: presentation only (no business logic, network, DB)
- [ ] ViewModels: state + business logic (@Observable or ObservableObject)
- [ ] Data access separated from views

### State Management
- `@State` - view-local state only
- `@StateObject` - view-owned ViewModels (avoid in List rows)
- `@ObservedObject` - passed-in ViewModels
- `@Bindable` - two-way binding to Observable objects (iOS 17+)
- `@Environment` - shared state (read-only preferred)
- `@EnvironmentObject` - injected dependencies (check for missing inject)

#### State Lifecycle Issues
- [ ] No retained cycles in ViewModels (@Published closures)
- [ ] Proper cleanup in deinit or .onDisappear
- [ ] @StateObject not recreated on parent refresh
- [ ] Environment values exist before access

### Dependency Injection
- [ ] Dependencies injected (check project: Swinject, Resolver, Factory, manual)
- [ ] No hardcoded singletons in views
- [ ] ViewModels receive dependencies

### View Composition
- [ ] Views are small (single responsibility)
- [ ] Complex views broken into components
- [ ] Reusable components extracted

## Common Issues

| Issue | Fix |
|-------|-----|
| Business logic in view | Extract to ViewModel |
| Network call in view | Move to ViewModel with `task` |
| Singleton in view | Inject via DI or @Environment |
| 200+ line view | Break into components |

## Severity

- 🔴 Critical: Architecture violation
- 🟡 Improvement: Better pattern available
- 🟢 Enhancement: Optional optimization
