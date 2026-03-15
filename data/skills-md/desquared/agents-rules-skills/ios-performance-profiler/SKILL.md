---
name: ios-performance-profiler
description: Identifies potential performance bottlenecks in SwiftUI code including expensive view updates, unnecessary redraws, and memory issues. Use when code involves lists, animations, complex UI, or when the user asks about performance optimization.
---

# Performance Profiler

## Checklist

### View Redraws
- [ ] Views only redraw when dependencies change
- [ ] @State properly scoped
- [ ] Stable view identity (no random IDs)

### Lists
- [ ] Use `List` not `ScrollView + VStack` for large data
- [ ] Stable `Identifiable` IDs
- [ ] Lightweight row views

### Memory
- [ ] No retain cycles (`[weak self]` in closures)
- [ ] @StateObject for owned objects
- [ ] Image caching for remote images

### Body Computation
- [ ] No heavy work in view body
- [ ] Pre-compute expensive operations

## Quick Wins

| Issue | Fix |
|-------|-----|
| Parent redraws | Extract stable child views |
| Expensive body | Pre-compute or cache |
| Unstable IDs | Use UUID in Identifiable |
| Retain cycle | `[weak self]` |
| Broad animation | Scope to specific views |

## Debug

```swift
let _ = Self._printChanges() // In view body
```

## Severity

- 🔴 Critical: Visible lag, leaks
- 🟡 Moderate: Noticeable impact
- 🟢 Minor: Optimization opportunity
