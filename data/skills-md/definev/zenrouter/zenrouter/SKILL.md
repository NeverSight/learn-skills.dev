---
name: zenrouter
description: >
  Implement and extend routing using the zenrouter Coordinator pattern.
  Use this skill when the user asks to add a route, feature module, layout,
  redirect rule, redirect guard, nested coordinator, or navigate programmatically.
  Triggers on: route, router, routing, coordinator, CoordinatorModular, RouteModule,
  NavigationPath, IndexedStackPath, RouteLayout, RouteRedirectRule, RedirectRule,
  RedirectResult, parseRouteFromUri, push, pop, replace, navigate, deep link,
  toUri, parentLayoutKey, layoutKey, bindLayout, RouteUnique, RouteGuard,
  RouteRedirect, notFoundRoute, zenrouter.
---

# ZenRouter Skill

This project uses [zenrouter](https://pub.dev/packages/zenrouter) — a Flutter
router that supports **imperative**, **declarative**, and **coordinator-based**
navigation. This skill covers the **Coordinator + RouteModule** pattern, which
is the right choice when you need deep linking, URL sync, layouts, and modular
feature organisation.

> **Deep-dive references** — read these only when you need the specific topic:
>
> | File | When to read |
> |:-----|:-------------|
> | [ADVANCED.md](./ADVANCED.md) | Coordinator-as-Module, tab navigation, composable redirect rules, parameter route examples |
> | [MIXIN.md](./MIXIN.md) | Full reference for `RouteGuard`, `RouteRedirect`, `RouteDeepLink`, `RouteTransition`, `RouteQueryParameters`, `RouteRestorable` |
> | [NAVIGATION.md](./NAVIGATION.md) | When to use `push` vs `navigate` vs `replace` and other navigation methods |

---

## Key Types

| Type | Package | Purpose |
|:-----|:--------|:--------|
| `RouteTarget` | `zenrouter_core` | Base class for all routes; identity via `props` |
| `RouteUnique` | `zenrouter_core` | Mixin — adds URI identity; **required** for coordinator routes |
| `Coordinator<T>` | `zenrouter` | Central hub: owns `NavigationPath`s, parses URIs, drives Flutter Router |
| `CoordinatorModular<T>` | `zenrouter_core` | Mixin on `Coordinator` — splits route parsing across `RouteModule`s |
| `RouteModule<T>` | `zenrouter_core` | Handles one feature's URI patterns and navigation paths |
| `NavigationPath<T>` | `zenrouter` | Mutable stack of routes; one per layout group |
| `IndexedStackPath<T>` | `zenrouter` | Fixed set of routes for tab-bar style navigation |
| `RouteLayout<T>` | `zenrouter` | Mixin — layout route that wraps nested routes (shell, tab bar, drawer, etc.) |
| `RouteRedirectRule<T>` | `zenrouter_core` | Mixin — delegates redirect logic to a list of `RedirectRule`s |
| `RedirectRule<T>` | `zenrouter_core` | Single composable guard; returns `continueRedirect`, `redirectTo`, or `stop` |

---

## 1. Route Base Type

All routes in a coordinator must extend `RouteTarget with RouteUnique`:

```dart
abstract class AppRoute extends RouteTarget with RouteUnique {
  @override
  Widget build(covariant Coordinator coordinator, BuildContext context);
}
```

---

## 2. Coordinator

### Simple (no modules)

```dart
class AppCoordinator extends Coordinator<AppRoute> {
  late final homeStack = NavigationPath<AppRoute>.createWith(
    label: 'home',
    coordinator: this,
  )..bindLayout(HomeLayout.new);

  @override
  List<StackPath> get paths => [...super.paths, homeStack];

  @override
  AppRoute parseRouteFromUri(Uri uri) => switch (uri.pathSegments) {
    [] || ['home'] => HomeRoute(),
    ['product', final id] => ProductRoute(id: id),
    _ => NotFoundRoute(uri: uri),
  };
}

// Wire up:
MaterialApp.router(routerConfig: AppCoordinator())
```

### Modular (with feature modules)

Add `CoordinatorModular<T>` to delegate URI parsing across feature modules:

```dart
class AppCoordinator extends Coordinator<AppRoute>
    with CoordinatorModular<AppRoute> {
  @override
  Set<RouteModule<AppRoute>> defineModules() => {
    AuthModule(this),
    ShopModule(this),
    ProfileModule(this),
  };

  @override
  AppRoute notFoundRoute(Uri uri) => NotFoundRoute(uri: uri);
}
```

**Rules:**
- Module order in `defineModules()` determines parsing priority — first non-null result wins.
- `CoordinatorModular` overrides `parseRouteFromUri` automatically; do **not** override it.
- `notFoundRoute` is called when all modules return `null`.

> For nested feature groups with sub-modules, see [Coordinator as Module](./ADVANCED.md#coordinator-as-module) in ADVANCED.md.

---

## 3. Route Module

```dart
class ShopModule extends RouteModule<AppRoute> {
  ShopModule(super.coordinator);

  late final shopStack = NavigationPath<AppRoute>.createWith(
    coordinator: coordinator,   // ← always the inherited `coordinator` field (= root)
    label: 'shop',
  )..bindLayout(ShopLayout.new);

  @override
  List<StackPath> get paths => [shopStack];

  @override
  FutureOr<AppRoute?> parseRouteFromUri(Uri uri) => switch (uri.pathSegments) {
    ['shop'] => ShopHomeRoute(),
    ['shop', 'products', final id] => ProductDetailRoute(id: id),
    _ => null,   // ← MUST return null for unrecognised URIs
  };
}
```

**Rules:**
- Always return `null` for unrecognised URIs so other modules can claim them.
- Use `coordinator` (inherited field) for `NavigationPath.createWith` — it always
  refers to the root coordinator that owns the navigation state.
- `bindLayout(LayoutClass.new)` takes the constructor, not an instance.

---

## 4. Route Definition

```dart
// Standard route
class ShopHomeRoute extends AppRoute {
  @override
  Object? get parentLayoutKey => ShopLayout;   // matches RouteLayout.layoutKey (default: runtimeType)

  @override
  Uri toUri() => Uri.parse('/shop');

  @override
  Widget build(covariant AppCoordinator coordinator, BuildContext context) {
    return ShopHomePage(
      onProductTap: (id) => coordinator.push(ProductDetailRoute(id: id)),
    );
  }
}

// Route with parameters — must override props
class ProductDetailRoute extends AppRoute {
  ProductDetailRoute({required this.id});
  final String id;

  @override
  List<Object?> get props => [id];

  @override
  Object? get parentLayoutKey => ShopLayout;

  @override
  Uri toUri() => Uri.parse('/shop/products/$id');

  @override
  Widget build(covariant AppCoordinator coordinator, BuildContext context) =>
      ProductDetailPage(id: id);
}
```

**Rules:**
- `parentLayoutKey` must exactly match `layoutKey` of the target `RouteLayout`.
  Default `layoutKey` is `runtimeType`, so using the layout class `Type` is simplest.
- Override `props` for routes with parameters.
- `toUri()` is used for deep linking and URL sync.

> For redirect-only routes, see [RedirectRule](./ADVANCED.md#redirectrule) in ADVANCED.md.

---

## 5. Layout

```dart
class ShopLayout extends AppRoute with RouteLayout<AppRoute> {
  @override
  StackPath<AppRoute> resolvePath(covariant AppCoordinator coordinator) =>
      coordinator.getModule<ShopCoordinator>().shopStack;

  // layoutKey defaults to runtimeType — override only if you need a custom value
  // @override Object get layoutKey => 'ShopLayout';

  @override
  Widget build(covariant AppCoordinator coordinator, BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Shop')),
      body: buildPath(coordinator),   // renders the active child route
    );
  }
}
```

**Rules:**
- Use `buildPath(coordinator)` to render child routes — do **not** call `super.build()`.
- `resolvePath` must return the exact `NavigationPath` that was `bindLayout`-ed in the module.
- For tab navigation, see [IndexedStackPath](./ADVANCED.md#indexedstackpath-tab-navigation) in ADVANCED.md.

---

## 6. Navigation

```dart
coordinator.push(ProductDetailRoute(id: '42'));    // add to stack
coordinator.navigate(ShopHomeRoute());             // pop-to-existing or push new
coordinator.replace(SettingsRoute());              // full state reset
coordinator.pop();                                 // pop top route

// Navigate from a URI string (e.g. deep link):
final route = await coordinator.parseRouteFromUri(Uri.parse('/shop/products/42'));
coordinator.push(route!);
```

Redirect rules run automatically on every navigation call.

> For full details on `pushReplacement`, `pushOrMoveToTop`, `tryPop`, `recover`, and decision flowcharts, see [NAVIGATION.md](./NAVIGATION.md).

---

## 7. File Structure Convention

```
lib/src/router/
├── coordinator.dart          ← Root Coordinator or Coordinator-as-Module
├── route.dart                ← Base route type (e.g. AppRoute)
├── _public.dart              ← Barrel: export module + public routes + public rules
├── rules/
│   ├── auth_required.dart
│   └── force_redirect.dart
└── routes/
    ├── (auth)/               ← Route group (shares a layout)
    │   ├── _layout.dart      ← Layout for this group
    │   ├── sign_in.dart      ← /sign-in
    │   └── forgot_password.dart
    ├── (dashboard)/
    │   ├── _layout.dart
    │   ├── _index.dart       ← Index / redirect-only route
    │   └── transactions/     ← URI segment directory
    │       ├── _index.dart   ← /transactions
    │       └── [id].dart     ← /transactions/:id  (named parameter route)
    │   └── blog/
    │       ├── _layout.dart   ← blog layout
    │       └── [...slug].dart ← /blog/*             (catch-all parameter route)
    └── not_found.dart
```

**Conventions:**
- `(group)/` — parenthesised directories are **layout groups** (organisational only). They do **not** appear in the URI. Routes inside share a layout.
- `group/` — bare directories (no parentheses) **do** appear in the URI. `transactions/` → the URI includes `/transactions/...`.
- `_layout.dart` — the `RouteLayout` for its group; prefixed with `_` because it's structural, not a user-facing route.
- `_index.dart` — the index route for a directory (often a redirect-only route).
- `[param].dart` — a **named parameter route** file. The brackets mirror dynamic URI segments (e.g. `[id].dart` → `/transactions/:id`).
- `[...param].dart` — a **catch-all parameter route** file. Captures all remaining URI segments as a single list (e.g. `[...slug].dart` → `/blog/*`).
- `_public.dart` — barrel file that exports only public symbols.
- `rules/` — reusable `RedirectRule` implementations.

> For detailed examples of parameter route classes, see [Named Parameter Routes](./ADVANCED.md#named-parameter-routes) and [Catch-All Parameter Routes](./ADVANCED.md#catch-all-parameter-routes) in ADVANCED.md.

---

## 8. Naming Conventions

### Route Classes

| Pattern | Example | When |
|:--------|:--------|:-----|
| `<Feature>Route` | `SignInRoute`, `TransactionRoute` | Standard page route |
| `<Feature>DetailRoute` | `TransactionDetailRoute` | Detail page with `[id]` |
| `<Feature>IndexRoute` | `DashboardIndexRoute` | Index / redirect-only route |
| `<Feature>Tab` | `HomeTab`, `ShopTab` | Tab in an `IndexedStackPath` |
| `NotFoundRoute` | `NotFoundRoute` | 404 catch-all |

### Layout, Module, and Rule Classes

| Pattern | Example | When |
|:--------|:--------|:-----|
| `<Feature>Layout` | `AuthLayout`, `DashboardLayout` | Layout shell |
| `<Feature>Module` | `AuthModule`, `ShopModule` | Simple `RouteModule` |
| `<Feature>Coordinator` | `ShopCoordinator` | Coordinator-as-Module (has sub-modules) |
| `<Condition>Rule` | `AuthRequiredRule`, `AlreadyAuthRule` | Redirect rule |

### URI Patterns

| Pattern | Example | Route |
|:--------|:--------|:------|
| `/feature` | `/sign-in` | `SignInRoute` |
| `/feature/:id` | `/transaction/abc123` | `TransactionDetailRoute(id: 'abc123')` |
| `/group/feature` | `/shop/products` | `ProductListRoute` |
| `/group/feature/:id` | `/shop/products/42` | `ProductDetailRoute(id: '42')` |

Use kebab-case for URI segments. Use singular nouns for resource detail paths (`/transaction/:id` not `/transactions/:id`).

NavigationPath labels use kebab-case: `'auth'`, `'dashboard'`, `'shop-products'`.

---

## 9. Adding a New Feature: Checklist

1. **Create route** — extend base route type; set `parentLayoutKey`, `toUri()`, `build()`, `props`.
2. **Register** in `parseRouteFromUri` of the owning module.
3. **Export** from `_public.dart` barrel if navigated to from outside.
4. **New layout group?** — create `(group)/_layout.dart` with `RouteLayout`, new `NavigationPath` with `bindLayout`, add to `paths`.
5. **New module?** — create `module.dart` extending `RouteModule<T>`, register in parent's `defineModules()`.
6. **New feature group with sub-modules?** — use [Coordinator-as-Module](./ADVANCED.md#coordinator-as-module) pattern.

---

## Common Mistakes

| Mistake | Fix |
|:--------|:----|
| `parseRouteFromUri` in a module not returning `null` for non-owned URIs | Must return `null` so other modules can claim the URI |
| `parentLayoutKey` doesn't match `layoutKey` | Default `layoutKey` is usually `runtimeType` — use the layout class `Type` as `parentLayoutKey` |
| Forgetting `...super.paths` when overriding `paths` | Always spread `super.paths` to include root and inherited module paths |
| Overriding `parseRouteFromUri` on a `CoordinatorModular` coordinator | Don't — `CoordinatorModular` handles it; override `notFoundRoute` instead |
| Standalone `Coordinator` returning `null` from `parseRouteFromUri` | Standalone coordinators must never return `null`; add a catch-all case |
