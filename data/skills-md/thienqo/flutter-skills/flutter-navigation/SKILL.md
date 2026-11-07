---
name: flutter-navigation
description: Implement, review, or verify Flutter routing, deep-link destinations, back-stack behavior, nested navigation, restoration, redirects, and URL synchronization. Use for route correctness; pair with flutter-device-testing on a concrete runtime, and do not introduce a routing package by default.
---

# Flutter Navigation

Model navigation as application state when URLs, deep links, restoration, or multiple navigators require it; use simpler imperative navigation for genuinely local flows.

## Inspect first

Identify the current router, route ownership, authentication flow, tab/shell structure, supported platforms, URL requirements, and state restoration expectations. Preserve the existing routing package unless migration is requested.

## Rules

- Keep route names, path parameters, and argument decoding typed or centrally validated.
- Make redirect logic deterministic and free of redirect loops.
- Preserve intended back behavior across Android system back, browser history, iOS gestures, nested navigators, and modals.
- Use nested navigation only for independent histories such as tab shells.
- Parse deep links into domain-safe state and define behavior for unknown or unauthorized destinations.
- Keep navigation side effects outside widget `build`.
- Do not place large domain objects directly in URLs or restoration state.

## Verification

Test cold deep links, warm links, back/forward behavior, authentication redirects, invalid parameters, restoration where required, and each supported shell/tab history.

## References

When tab shell patterns or independent back histories are in scope, follow the [nested shell navigation reference](references/nested-shell-navigation.md).
When handling deep links or state restoration, follow the [deep link and restoration reference](references/deep-link-and-restoration.md).

## Sources

- [Flutter navigation and routing](https://docs.flutter.dev/ui/navigation)
- [Deep linking](https://docs.flutter.dev/ui/navigation/deep-linking)
