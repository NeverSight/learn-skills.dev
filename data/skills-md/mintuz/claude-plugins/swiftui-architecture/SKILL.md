---
name: swiftui-architecture
description: WHEN building SwiftUI views, managing state, setting up shared services, or making architectural decisions; NOT for UIKit or legacy patterns; provides pure SwiftUI data flow without ViewModels using @State, @Binding, @Observable, and @Environment.
---

# Modern SwiftUI Architecture

Concise entry point for pure SwiftUI architecture without ViewModels. Use the references for patterns, examples, and edge cases.

## Start Here

- State management: `references/state-management.md`
- Observable services: `references/observable-patterns.md`
- Async work: `references/async-patterns.md`
- Navigation: `references/navigation-patterns.md`
- UI components: `references/lists.md`, `references/scrollview.md`, `references/forms.md`, `references/grids.md`, `references/sheets.md`, `references/tabs.md`
- Anti-patterns: `references/anti-patterns.md`

## Typical Flow

1. Choose state ownership and data flow (`references/state-management.md`).
2. Model shared logic as @Observable services (`references/observable-patterns.md`).
3. Wire navigation with AppRouter (`references/navigation-patterns.md`).
4. Build UI using component guides.
5. Audit against anti-patterns (`references/anti-patterns.md`).
