---
name: ios-architecture-expert
description: >
  Guides building modular, testable iOS/Swift applications following the
  Essential Developer methodology -- clean architecture with protocol-oriented
  design, composition root, generic presenters, and modern Swift concurrency.
  Use when designing features, structuring modules, composing dependencies,
  or reviewing iOS architecture.
---

# iOS Architecture Expert — Essential Developer Methodology

## Agent Behavior Contract

When this skill is active, follow these rules **strictly**:

1. **Feature modules have zero UIKit/SwiftUI imports** — only Foundation. Domain models, use cases, presenters, and API/cache logic never depend on a UI framework.
2. **Define protocol boundaries at every layer transition** — `FeedStore`, `HTTPClient`, `ResourceView`, `FeedCache`, etc. Concrete types live behind protocols.
3. **Domain models are value types** — `struct`, `Hashable`, `Sendable`. No classes for models.
4. **Presentation logic is framework-agnostic** — presenters output view models (structs). No `UIImage`, `UIColor`, or SwiftUI types in the presentation layer.
5. **All dependency wiring happens in the Composition Root** — the app target (or a dedicated `CompositionRoot` module). Feature modules never create their own dependencies.
6. **Tests drive the design** — one test class per use case, named by behavior (`CacheFeedUseCaseTests`, not `LocalFeedLoaderTests`). Use `makeSUT()` factory in every test class.
7. **Use SPM multi-target packages** for module separation — `EssentialFeed` (Foundation), `EssentialFeediOS` (UIKit), `EssentialApp` (composition).
8. **Prefer async/await over closures/Combine** for async operations. Use `Task.immediate` for synchronous-first execution in adapters.
9. **Use Swift Testing** (`@Test`, `#expect`) for new tests. Follow patterns in the `swift-testing-expert` skill when available.
10. **Mark shared mutable state with `@MainActor`** — presenters, adapters, view controllers, and composition code run on the main actor.

---

## Architecture Layers

| Layer | Responsibility |
|-------|---------------|
| **Feature** | Domain models (`struct`, `Sendable`) and abstract use-case protocols. Zero framework imports beyond Foundation. |
| **API** | Endpoint enums, static mappers with private `Decodable` types, `HTTPClient` protocol. |
| **Cache** | Store protocols, local models (decoupled from domain), use-case orchestrators, cache policy objects. |
| **Presentation** | Generic `LoadResourcePresenter<Resource, View>`, view model structs, localized error strings. |
| **UI (UIKit)** | View controllers, cells, `DiffableDataSource`, `CellController` type-erasure. Conforms to presenter view protocols. |
| **UI (SwiftUI)** | `@Observable` view models, `View` composition, environment-based DI. Same presenter patterns, different binding. |
| **Composition** | `Composer` static factories, `PresentationAdapter`, `WeakRefVirtualProxy`, `FeedViewAdapter`. App-target only. |

> Full code examples: [architecture-layers.md](references/architecture-layers.md)

---

## Key Patterns Quick Reference

| Pattern | Purpose |
|---------|---------|
| `LoadResourcePresenter<Resource, View>` | Reusable loading/error/success state machine with generic mapper |
| `WeakRefVirtualProxy<T>` | Break retain cycles in presenter→view binding via conditional conformance |
| Specification Pattern | Protocol-driven shared test specs across store implementations |
| Composition Root / Service | Central dependency creation and wiring (`FeedService`) |
| UI Composer (static factory) | Wire presenter→adapter→view chain per feature (`FeedUIComposer.feedComposedWith`) |
| `LoadResourcePresentationAdapter` | Generic async loader bridging use cases to presenters with cancellation |
| `FeedViewAdapter` | Maps domain models to `CellController` array, composes recursive `loadMore` |
| `Paginated<Item>` | Recursive pagination with optional `loadMore` closure (`Sendable`) |
| Static Mapper | Pure function for data transformation — `FeedItemsMapper.map(_:from:)` |
| Cache Policy | Business rule encapsulation for cache validation — `FeedCachePolicy.validate(_:against:)` |
| Local Model | Cache-layer representation decoupled from domain — `LocalFeedImage` |
| `Scheduler` protocol | Abstract store execution context for CoreData/InMemory polymorphism |
| `CellController` | Type-erased cell composition — wraps `UITableViewDataSource` + `Delegate` + `Prefetching` |

---

## Feature Decision Tree

Starting a new feature? Follow this path:

1. **Define the domain model** → `struct` in Feature layer, `Hashable`, `Sendable`
2. **Need remote data?** → Endpoint enum + static mapper in API layer
3. **Need persistence?** → Store protocol + local model + cache policy in Cache layer
4. **Need to display it?** → `LoadResourcePresenter` + view model struct in Presentation layer
5. **UIKit or SwiftUI?** → Build view layer, conform to `ResourceView` protocols
6. **Wire it up** → Composer + adapter + proxy in Composition Root

> Step-by-step guide: [feature-implementation-workflow.md](references/feature-implementation-workflow.md)

---

## Modernization Notes

**SPM over xcframework**: Structure as a multi-target Swift package. Feature and API/Cache targets depend only on Foundation. UI targets import UIKit/SwiftUI. Composition target imports everything. See [spm-project-structure.md](references/spm-project-structure.md).

**Swift Testing over XCTest**: New test suites use `@Test` and `#expect`. Shared specs become protocol extensions with `@Test` methods. The `makeSUT()` pattern and `trackForMemoryLeaks` adapt to Swift Testing's lifecycle. Defer to the `swift-testing-expert` skill for detailed patterns.

**async/await**: `HTTPClient` returns `async throws`. `LoadResourcePresentationAdapter` uses `Task.immediate` for synchronous-first execution. `Paginated<Item>.loadMore` is `@Sendable () async throws -> Self`. `Scheduler` protocol abstracts CoreData context dispatch.

**SwiftUI composition**: Replace `WeakRefVirtualProxy` with `@Observable` view models (SwiftUI manages lifecycle). Replace `CellController` type-erasure with `ForEach` + `@ViewBuilder`. Composition Root injects `@Observable` objects via `.environment()`. See SwiftUI sections in [composition-and-adapters.md](references/composition-and-adapters.md).

---

## References

- [architecture-layers.md](references/architecture-layers.md) — Layer-by-layer patterns with code examples from each architectural boundary
- [composition-and-adapters.md](references/composition-and-adapters.md) — Composition Root, UI composers, adapters, proxies, and pagination (UIKit + SwiftUI)
- [testing-strategy.md](references/testing-strategy.md) — Five-layer test strategy: unit, specification, integration, snapshot, acceptance
- [feature-implementation-workflow.md](references/feature-implementation-workflow.md) — Step-by-step checklist for building a feature end-to-end
- [spm-project-structure.md](references/spm-project-structure.md) — SPM multi-target layout, Package.swift example, and CI configuration
