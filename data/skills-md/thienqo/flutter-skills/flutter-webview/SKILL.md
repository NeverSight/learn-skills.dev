---
name: flutter-webview
description: Implement, repair, or review embedded web content in Flutter, including navigation policy, JavaScript bridges, cookies, sessions, file flows, permissions, and WebView lifecycle. Use when a Flutter screen hosts web content; route OAuth sign-in to flutter-authentication, app routes to flutter-navigation, and broad threat audits to flutter-security.
---

# Flutter WebView

Treat a WebView as an untrusted web runtime embedded inside a privileged application process. Preserve the project's current WebView package, web contract, router, session owner, and supported platforms unless migration is requested.

Do not add a WebView package, native manifest change, or domain/redirect registration merely because the skill is selected.

## Preflight

Read `pubspec.yaml`, SDK constraints, the selected WebView package and version, platform targets, platform manifests and entitlements, loaded origins and redirects, JavaScript settings and channels, cookies and website data, authentication ownership, file and permission flows, app navigation, lifecycle handling, and tests. Confirm the package's current platform support before promising cross-platform behavior; embedded web content on Flutter web can use different primitives and constraints from system WebViews on Android, iOS, or macOS.

Prefer native Flutter UI for app-owned interaction when it provides the required fidelity and accessibility. Use an embedded browser only for a concrete content or integration requirement. Do not replace the existing package with `webview_flutter` or another dependency by default.

## Load references conditionally

- Read [navigation and content policy](references/navigation-and-content-policy.md) for origin allowlists, schemes, popups, downloads, errors, external links, TLS, and browser history.
- Read [JavaScript bridges and permissions](references/javascript-bridges-and-permissions.md) for message schemas, origin trust, privileged actions, dialogs, media, camera or microphone requests, and minimal JavaScript enablement.
- Read [sessions, files, and lifecycle](references/sessions-files-and-lifecycle.md) for cookies, account switching, logout cleanup, file chooser and download behavior, controller ownership, process recreation, and platform verification.

## Core rules

- Parse every navigation as a URI and decide from explicit scheme, normalized host, port, and path rules. A string prefix is not an origin check.
- Keep JavaScript disabled unless the content contract requires it. Expose the smallest typed message surface and validate every payload again in Dart before changing app state or invoking native capability.
- Never treat a page title, URL fragment, JavaScript message, or matching custom scheme as proof of identity, payment, authorization, or trusted completion. Confirm sensitive outcomes through their owning backend or platform protocol.
- Define which cookies and website data are shared, persisted, isolated, or cleared. Coordinate logout and account switching with the application session owner.
- Handle main-frame load, HTTP, TLS, renderer, permission, popup, file, download, and external-app outcomes explicitly where the selected package exposes them. Do not bypass certificate errors.
- Keep controller and callback ownership lifecycle-safe. Prevent callbacks from a disposed screen, stale navigation, or previous account from mutating current state.

## Boundaries

- `flutter-authentication` owns OAuth or OIDC, PKCE, verified redirects, token lifecycle, logout semantics, and account switching. Native-app authorization uses an external user-agent rather than an embedded WebView.
- `flutter-navigation` owns Flutter routes, deep-link destinations, browser URL synchronization, and back-stack correctness outside the embedded page.
- `flutter-security` owns threat modeling and repository-wide WebView hardening audits; this skill implements the scoped content, bridge, and lifecycle contract.
- `flutter-networking` owns ordinary API transport. Do not tunnel app API behavior through JavaScript just because a WebView exists.
- `flutter-platform-integration` owns custom native WebView capabilities or platform-view bridges when the established plugin cannot satisfy a required API.
- `flutter-device-testing` owns concrete device and emulator execution; this skill defines the WebView behaviors that must be observed.

## Verification

Use deterministic local or staging content controlled for the test, plus real supported platform runtimes for system-WebView behavior. Cover allowed and blocked top-level navigation, redirects, subframes where observable, external schemes, back behavior, JavaScript disabled and enabled states, malformed and replayed messages, account switch and logout, offline and HTTP failure, process recreation, disposal during callbacks, file cancellation and invalid selection, permission denial, and download ownership as applicable.

Record the package and version, platform and OS, WebView engine, tested origins, JavaScript and data-store policy, and which provider or backend boundary was actually observed. Widget tests can verify policy functions and state ownership; they do not prove system WebView rendering, cookie persistence, chooser behavior, permissions, downloads, or navigation callbacks on a device.

## Sources

- [Flutter webview_flutter](https://pub.dev/packages/webview_flutter)
- [Embedding web content into a Flutter web app](https://docs.flutter.dev/platform-integration/web/web-content-in-flutter)
- [Android WebView native bridge risks](https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges)
- [Apple WKWebsiteDataStore](https://developer.apple.com/documentation/webkit/wkwebsitedatastore)
- [OAuth 2.0 for Native Apps](https://www.rfc-editor.org/rfc/rfc8252)
