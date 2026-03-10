---
name: uikit-expert
description: Write, review, or improve UIKit code following best practices for view controller lifecycle, Auto Layout, collection views, navigation, animation, memory management, and modern iOS 18–26 APIs. Use when building new UIKit features, refactoring existing views or view controllers, reviewing code quality, adopting modern UIKit patterns (diffable data sources, compositional layout, cell configuration), or bridging UIKit with SwiftUI. Does not cover SwiftUI-only code.
---

# UIKit Expert Skill

## Overview
Use this skill to build, review, or improve UIKit features with correct lifecycle management, performant Auto Layout, modern collection view APIs, and safe navigation patterns. Prioritize native APIs, Apple's documented best practices, and performance-conscious patterns. This skill focuses on facts and best practices without enforcing specific architectural patterns (no MVVM/VIPER/Coordinator mandates).

## Workflow Decision Tree

### 1) Review existing UIKit code
- Check view controller lifecycle usage — `viewIsAppearing` for geometry, `viewDidLoad` for setup only (see `references/view-controller-lifecycle.md`)
- Verify Auto Layout correctness — batch activation, no constraint churn, `translatesAutoresizingMaskIntoConstraints` (see `references/auto-layout.md`)
- Check collection/table view APIs — diffable data sources, stable identity, CellRegistration (see `references/modern-collection-views.md`)
- Verify cell configuration uses `UIContentConfiguration`, not deprecated `textLabel` (see `references/cell-configuration.md`)
- Check list scroll performance — prefetching, cell reuse cleanup, reconfigureItems (see `references/list-performance.md`)
- Verify navigation patterns — bar appearance all 4 slots, no concurrent transition crashes (see `references/navigation-patterns.md`)
- Check animation correctness — API selection, PropertyAnimator state machine, constraint animation (see `references/animation-patterns.md`)
- Audit memory management — `[weak self]`, delegate ownership, Timer/CADisplayLink traps (see `references/memory-management.md`)
- Check concurrency safety — Task lifecycle, cancellation in viewDidDisappear (see `references/concurrency-main-thread.md`)
- If SwiftUI interop present — verify UIHostingController containment, sizingOptions (see `references/uikit-swiftui-interop.md`)
- Check image loading — downsampling, cell reuse race condition (cancel/clear/verify) (see `references/image-loading.md`)
- Verify keyboard handling — UIKeyboardLayoutGuide over manual notifications (see `references/keyboard-scroll.md`)
- Check trait handling and accessibility — registerForTraitChanges, Dynamic Type, VoiceOver (see `references/adaptive-appearance.md`)
- Validate modern API adoption and iOS 26+ availability handling (see `references/modern-uikit-apis.md`)

### 2) Improve existing UIKit code
- Replace geometry work in `viewDidLoad` with `viewIsAppearing` (see `references/view-controller-lifecycle.md`)
- Eliminate constraint churn — create once, toggle `isActive` or modify `.constant` (see `references/auto-layout.md`)
- Migrate from legacy `UITableViewDataSource` to diffable data sources (see `references/modern-collection-views.md`)
- Replace deprecated `textLabel`/`detailTextLabel`/`imageView` with `UIContentConfiguration` (see `references/cell-configuration.md`)
- Replace `reloadItems` with `reconfigureItems` for in-place cell updates (see `references/list-performance.md`)
- Fix navigation bar appearance — set all 4 appearance slots, use `navigationItem` not `navigationBar` (see `references/navigation-patterns.md`)
- Improve animations — use PropertyAnimator for gestures, correct constraint animation pattern (see `references/animation-patterns.md`)
- Fix retain cycles — add `[weak self]`, cancel Tasks in `viewDidDisappear`, use block-based Timer (see `references/memory-management.md`)
- Migrate GCD to Swift concurrency — replace `DispatchQueue.main.async` with `Task` (see `references/concurrency-main-thread.md`)
- Suggest image downsampling when `UIImage(data:)` or full-resolution loading detected (as optional optimization, see `references/image-loading.md`)
- Replace keyboard notification handling with `UIKeyboardLayoutGuide` (see `references/keyboard-scroll.md`)
- Replace `traitCollectionDidChange` with `registerForTraitChanges` (see `references/adaptive-appearance.md`)
- Adopt iOS 26 APIs where appropriate — Observation, updateProperties(), .flushUpdates (see `references/modern-uikit-apis.md`)

### 3) Implement new UIKit feature
- Design data flow first: identify owned state, injected dependencies, and model layer
- Set up view controller lifecycle correctly — one-time setup in `viewDidLoad`, geometry in `viewIsAppearing` (see `references/view-controller-lifecycle.md`)
- Build Auto Layout with batch activation and zero churn (see `references/auto-layout.md`)
- Use modern collection view stack: DiffableDataSource + CompositionalLayout + CellRegistration (see `references/modern-collection-views.md`)
- Configure cells with `UIContentConfiguration` and `configurationUpdateHandler` (see `references/cell-configuration.md`)
- Implement prefetching and proper cell reuse cleanup for lists (see `references/list-performance.md`)
- Set up navigation with all 4 appearance slots and concurrent-transition guards (see `references/navigation-patterns.md`)
- Choose correct animation API for the use case (see `references/animation-patterns.md`)
- Use `[weak self]` in escaping closures, cancel Tasks in lifecycle methods (see `references/memory-management.md`)
- Use `@MainActor` correctly, store Task references (see `references/concurrency-main-thread.md`)
- If embedding SwiftUI — use full child VC containment for UIHostingController (see `references/uikit-swiftui-interop.md`)
- Downsample images for display, handle cell reuse race condition (see `references/image-loading.md`)
- Use `UIKeyboardLayoutGuide` for keyboard handling (see `references/keyboard-scroll.md`)
- Support Dynamic Type, VoiceOver, dark mode from the start (see `references/adaptive-appearance.md`)
- Gate iOS 26+ features with `#available` and provide sensible fallbacks (see `references/modern-uikit-apis.md`)

## Core Guidelines

### View Controller Lifecycle
- Use `viewDidLoad` for one-time setup: subviews, constraints, delegates — NOT geometry
- Use `viewIsAppearing` (back-deployed iOS 13+) for geometry-dependent work, trait-based layout, scroll-to-item
- `viewDidLayoutSubviews` fires multiple times — use only for lightweight layer frame adjustments
- `viewWillAppear` is limited to transition coordinator animations and balanced notification registration
- Always call `super` in every lifecycle override
- Child VC containment: `addChild` → `addSubview` → `didMove(toParent:)` — in that exact order
- Verify deallocation with `deinit` logging during development

### Auto Layout
- Always set `translatesAutoresizingMaskIntoConstraints = false` on programmatic views
- Use `NSLayoutConstraint.activate([])` — never individual `.isActive = true`
- Create constraints once, toggle `isActive` or modify `.constant` — never remove and recreate
- Never change priority from/to `.required` (1000) at runtime — use 999
- Animate constraints: update constant → call `layoutIfNeeded()` inside animation block on superview
- iOS 26+: use `.flushUpdates` option to simplify constraint animation
- Avoid deeply nested UIStackViews in reusable cells

### Collection Views & Data Sources
- Use `UICollectionViewDiffableDataSource` with stable identifiers (UUID/database ID, not full model structs)
- Use `reconfigureItems` for content updates, `reloadItems` only when cell type changes
- Use `applySnapshotUsingReloadData` for initial population (bypasses diffing)
- Use `UICollectionViewCompositionalLayout` for any non-trivial layout
- Use `UICollectionView.CellRegistration` — no string identifiers, no manual casting
- Use `UIContentConfiguration` for cell content and `UIBackgroundConfiguration` for cell backgrounds
- Use `configurationUpdateHandler` for state-driven styling (selection, highlight)

### Navigation
- Configure all 4 `UINavigationBarAppearance` slots (standard, scrollEdge, compact, compactScrollEdge)
- Set appearance on `navigationItem` (per-VC) in `viewDidLoad`, not on `navigationBar` in `viewWillAppear`
- Use `setViewControllers(_:animated:)` for deep links — not sequential push calls
- Guard against concurrent transitions — check `transitionCoordinator` before push/pop
- Set `prefersLargeTitles` once on the bar; use `largeTitleDisplayMode` per VC

### Animation
- `UIView.animate` — simple one-shot animations; check `finished` in completion
- `UIViewPropertyAnimator` — gesture-driven, interruptible; respect state machine (inactive → active → stopped)
- `CABasicAnimation` — layer-only properties (cornerRadius, shadow, 3D transforms); set model value first
- iOS 17+ spring API: `UIView.animate(springDuration:bounce:)` aligns with SwiftUI
- Constraint animation: flush layout → update constant → animate `layoutIfNeeded()` on superview

### Memory Management
- Default to `[weak self]` in all escaping closures
- Timer: use block-based API with `[weak self]`, invalidate in `viewWillDisappear`
- CADisplayLink: use weak proxy pattern (no block-based API available)
- NotificationCenter: `[weak self]` in closure, remove observer in `deinit`
- Nested closures: re-capture `[weak self]` in stored inner closures
- Delegates: always `weak var delegate: SomeDelegate?` with `AnyObject` constraint
- Verify deallocation with `deinit` — if never called, a retain cycle exists

### Concurrency
- `UIViewController` is `@MainActor` — all subclass methods are implicitly main-actor
- Store `Task` references, cancel in `viewDidDisappear` — not `deinit`
- Check `Task.isCancelled` before UI updates after `await`
- `Task.detached` does NOT inherit actor isolation — explicit `MainActor.run` needed for UI
- Never call `DispatchQueue.main.sync` from background — use `await MainActor.run`

### UIKit–SwiftUI Interop
- UIHostingController: full child VC containment (`addChild` → `addSubview` → `didMove`), retain as stored property
- `sizingOptions = .intrinsicContentSize` (iOS 16+) for Auto Layout containers
- UIViewRepresentable: set mutable state in `updateUIView`, not `makeUIView`; guard against update loops
- UIHostingConfiguration (iOS 16+) for SwiftUI content in collection view cells

### Image Loading
- Decoded bitmap size = width × height × 4 bytes (a 12MP photo = ~48MB RAM)
- Downsample with ImageIO at display size — never load full bitmap and resize
- iOS 15+: use `byPreparingThumbnail(of:)` or `prepareForDisplay()` for async decoding
- Cell reuse: cancel Task in `prepareForReuse`, clear image, verify identity on completion

### Keyboard & Scroll
- Use `UIKeyboardLayoutGuide` (iOS 15+) — pin content bottom to `view.keyboardLayoutGuide.topAnchor`
- iPad: set `followsUndockedKeyboard = true` for floating keyboards
- Replace all manual keyboard notification handling with the layout guide

### Adaptive Layout & Accessibility
- Use `registerForTraitChanges` (iOS 17+) instead of deprecated `traitCollectionDidChange`
- Dynamic Type: `UIFont.preferredFont(forTextStyle:)` + `adjustsFontForContentSizeCategory = true`
- Dark mode: use semantic colors (`.label`, `.systemBackground`); re-resolve CGColor on trait changes
- VoiceOver: set `accessibilityLabel`, `accessibilityTraits`, `accessibilityHint` on custom views
- Use `UIAccessibilityCustomAction` for complex list item actions

## Quick Reference

### View Controller Lifecycle Method Selection
| Method | Use For |
|--------|---------|
| `viewDidLoad` | One-time setup: subviews, constraints, delegates |
| `viewIsAppearing` | Geometry-dependent work, trait-based layout, scroll-to-item |
| `viewWillAppear` | Transition coordinator animations only |
| `viewDidLayoutSubviews` | Lightweight layer frame adjustments (fires multiple times) |
| `viewDidAppear` | Start animations, analytics, post-appearance work |
| `viewWillDisappear` | Cancel tasks, invalidate timers, save state |
| `viewDidDisappear` | Final cleanup, cancel background work |

### Animation API Selection
| API | Best For | Interactive | Off Main Thread |
|-----|----------|-------------|-----------------|
| `UIView.animate` | Simple one-shot changes | No | No |
| `UIViewPropertyAnimator` | Gesture-driven, interruptible | Yes | No |
| `CABasicAnimation` | Layer properties, 3D transforms | Limited | Yes (Render Server) |

### Deprecated → Modern API Replacements
| Deprecated / Legacy | Modern Replacement | Since |
|---------------------|-------------------|-------|
| `traitCollectionDidChange` | `registerForTraitChanges(_:handler:)` | iOS 17 |
| Keyboard notifications | `UIKeyboardLayoutGuide` | iOS 15 |
| `cell.textLabel` / `detailTextLabel` | `UIListContentConfiguration` | iOS 14 |
| `register` + string dequeue | `UICollectionView.CellRegistration` | iOS 14 |
| `reloadItems` on snapshot | `reconfigureItems` | iOS 15 |
| `barTintColor` / `isTranslucent` | `UINavigationBarAppearance` (4 slots) | iOS 13 |
| `UICollectionViewFlowLayout` (complex) | `UICollectionViewCompositionalLayout` | iOS 13 |
| Manual `layoutIfNeeded()` in animations | `.flushUpdates` option | iOS 26 |
| Legacy app lifecycle | `UIScene` + `SceneDelegate` | Mandatory iOS 26 |
| `ObservableObject` + manual invalidation | `@Observable` + `UIObservationTrackingEnabled` | iOS 18 |

## Review Checklist

### View Controller Lifecycle
- [ ] `viewDidLoad` contains NO geometry-dependent work
- [ ] Geometry/trait work is in `viewIsAppearing`, not `viewWillAppear`
- [ ] Every lifecycle override calls `super`
- [ ] Child VC uses correct containment sequence
- [ ] `deinit` is implemented for leak verification during development

### Auto Layout
- [ ] `translatesAutoresizingMaskIntoConstraints = false` on all programmatic views
- [ ] Constraints activated via `NSLayoutConstraint.activate([])`
- [ ] No constraint removal/recreation — using `isActive` toggle or `.constant` modification
- [ ] No priority changes from/to `.required` (1000) at runtime
- [ ] No `setNeedsLayout()` inside `layoutSubviews` or `viewDidLayoutSubviews` (infinite loop)
- [ ] Constraint identifiers set for debugging

### Collection Views
- [ ] Using diffable data source with stable identifiers (not full model structs)
- [ ] `reconfigureItems` for content updates, not `reloadItems`
- [ ] `CellRegistration` instead of string-based register/dequeue
- [ ] `UIContentConfiguration` instead of deprecated cell properties
- [ ] No duplicate identifiers in snapshot (`BUG_IN_CLIENT` crash)
- [ ] Self-sizing cells have unambiguous top-to-bottom constraint chain

### Navigation
- [ ] All 4 `UINavigationBarAppearance` slots configured
- [ ] Appearance set on `navigationItem` in `viewDidLoad`, not `navigationBar` in `viewWillAppear`
- [ ] Concurrent transition guard in place
- [ ] `prefersLargeTitles` set once; `largeTitleDisplayMode` per VC

### Animation
- [ ] Correct API chosen for use case (animate vs PropertyAnimator vs CA)
- [ ] `UIViewPropertyAnimator` state machine respected
- [ ] Constraint animation uses correct pattern (flush → update → animate)
- [ ] `CAAnimation` sets model value before adding animation
- [ ] Completion handlers check `finished` parameter

### Memory Management
- [ ] `[weak self]` in all escaping closures
- [ ] Timers use block-based API with `[weak self]`; invalidated in `viewWillDisappear`
- [ ] Task references stored and cancelled in `viewDidDisappear`
- [ ] CADisplayLink uses weak proxy pattern
- [ ] Delegates declared as `weak var` on `AnyObject`-constrained protocol
- [ ] No strong self re-capture in nested stored closures

### Concurrency
- [ ] `Task.isCancelled` checked after `await` before UI updates
- [ ] No `Task.detached` for UI work without explicit `MainActor.run`
- [ ] No redundant `@MainActor` on `UIViewController` subclasses (already inherited)
- [ ] No `DispatchQueue.main.sync` from background

### Image Loading
- [ ] Images downsampled to display size (not loaded at full resolution)
- [ ] Cell image loading: cancel in `prepareForReuse`, clear image, verify identity
- [ ] `NSCache` sized by decoded bitmap bytes, not file size

### UIKit–SwiftUI Interop
- [ ] `UIHostingController` retained as stored property (not local variable)
- [ ] `UIHostingController` uses full child VC containment (`addChild` → `addSubview` → `didMove`)
- [ ] `updateUIView` guards against infinite update loops with equality checks

### Keyboard
- [ ] Using `UIKeyboardLayoutGuide` (iOS 15+) instead of keyboard notifications
- [ ] iPad: `followsUndockedKeyboard = true` on the layout guide

### Adaptive & Accessibility
- [ ] `registerForTraitChanges` (iOS 17+) instead of `traitCollectionDidChange`
- [ ] Dynamic Type: `preferredFont` + `adjustsFontForContentSizeCategory = true`
- [ ] CGColor properties re-resolved on trait changes (layer.borderColor, shadowColor)
- [ ] Custom views have `accessibilityLabel` and `accessibilityTraits`
- [ ] `UIAccessibilityCustomAction` for complex list item actions

### Modern APIs (iOS 26+)
- [ ] `#available` guards with sensible fallbacks for iOS 26+ features
- [ ] `UIScene` lifecycle adopted (mandatory for iOS 26 SDK)
- [ ] `UIObservationTrackingEnabled` considered for iOS 18+ targets

## References
- `references/view-controller-lifecycle.md` — Lifecycle ordering, viewIsAppearing, child VC containment
- `references/auto-layout.md` — Batch activation, constraint churn, priority, animation, debugging
- `references/modern-collection-views.md` — Diffable data sources, compositional layout, CellRegistration
- `references/cell-configuration.md` — UIContentConfiguration, UIBackgroundConfiguration, configurationUpdateHandler
- `references/list-performance.md` — Prefetching, cell reuse, reconfigureItems, scroll performance
- `references/navigation-patterns.md` — Bar appearance, concurrent transitions, large titles, deep links
- `references/animation-patterns.md` — UIView.animate, UIViewPropertyAnimator, CAAnimation, springs
- `references/memory-management.md` — Retain cycles, [weak self], Timer/CADisplayLink/nested closure traps
- `references/concurrency-main-thread.md` — @MainActor, Task lifecycle, Swift 6, GCD migration
- `references/uikit-swiftui-interop.md` — UIHostingController, UIViewRepresentable, sizing, state bridging
- `references/image-loading.md` — Downsampling, decoded bitmap math, cell reuse race condition
- `references/keyboard-scroll.md` — UIKeyboardLayoutGuide, scroll view insets, iPad floating keyboard
- `references/adaptive-appearance.md` — Trait changes, Dynamic Type, dark mode, VoiceOver, accessibility
- `references/modern-uikit-apis.md` — Observation framework, updateProperties(), .flushUpdates, UIScene, Liquid Glass

## Philosophy

This skill focuses on **facts and best practices**, not architectural opinions:
- We don't enforce specific architectures (e.g., MVVM, VIPER, Coordinator)
- We do encourage separating business logic for testability
- We optimize for correctness first, then performance
- We follow Apple's documented APIs and Human Interface Guidelines
- We use "suggest" or "consider" for optional optimizations
- We use "always" or "never" only for correctness issues
