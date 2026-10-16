---
name: capacitor-app-intents
description: Exposes Capacitor app features to Siri, Shortcuts, Spotlight, the Action button, Apple Intelligence, widgets and controls with native App Intents in ios/App/App, bridged to the web layer. Covers open-app intents routed through Universal Links / `OpenURLIntent` and @capacitor/app `appUrlOpen`, or a local plugin with a pending-route store; headless background intents; App Group / Preferences data sharing; AppShortcutsProvider phrases, AppEntity queries; iOS 26/27 APIs (`supportedModes` replacing `openAppWhenRun`, `continueInForeground`, `LongRunningIntent`, AppIntentsTesting) gated for Capacitor 8 (iOS 15) and 9 (iOS 16). Covers file placement, target membership, and UIScene (Capacitor 8.5+) URL delivery. Use for "add Siri shortcut", "Shortcuts action", "App Shortcuts", "control widget", or an intent that opens the app but the web view never navigates. Do not use for deep link setup (capacitor-deep-linking), push (capacitor-push-notifications), or Android shortcuts.
---

# App Intents for Capacitor Apps

Add native App Intents to the iOS project so system surfaces can run app actions, and connect them to the web layer. App Intents are Swift only. There is no JavaScript API for them, so every intent is native code in the App target or an extension, and the web layer is reached through a URL or a small local plugin.

## When to Use

TRIGGER when:
- The user wants Siri phrases, Shortcuts actions, App Shortcuts, Spotlight actions, Action button or Apple Intelligence integration for a Capacitor app
- The user wants a widget button or a Control Center control to run an app action
- An intent opens the app, but the web view does not navigate, or it navigates only on warm launch
- A background intent crashes, times out, or tries to call JS
- Migrating `openAppWhenRun` to `supportedModes`, or adopting iOS 26/27 App Intents APIs
- A plugin author wants to ship App Intents with a plugin

Do not use:
- Universal Links / custom scheme / `appUrlOpen` setup: `capacitor-deep-linking`
- AppDelegate to SceneDelegate migration: `capacitor-uiscene-migration`
- Push notification actions: `capacitor-push-notifications`
- Live Activities or SVG widgets driven from JS: `capacitor-plugins` (`@capgo/capacitor-widget-kit`)
- Android app shortcuts and intents: not covered here

## Facts that drive the design

- **App Intents need iOS 16.** Capacitor 8 deploys to iOS 15, so every intent type, entity, query and `AppShortcutsProvider` needs `@available(iOS 16.0, *)`, or the user raises the deployment target. Capacitor 9 deploys to iOS 16, so the base API needs no gating. Newer APIs still do (tables in [references/ios-26-27-apis.md](references/ios-26-27-apis.md)).
- **A background intent has no WebView.** iOS can launch the app process headless for `.background` intents. `AppDelegate.application(_:didFinishLaunchingWithOptions:)` runs, but no scene connects and `CAPBridgeViewController` never loads. Background intents must do native work only (network, storage, HealthKit, etc.). They cannot call JS or plugins through the bridge.
- **`perform()` is not on the main actor, and it can run more than once.** Hop explicitly (`await MainActor.run` or `@MainActor func perform()`) before you touch UIKit, the bridge or `@MainActor` state. Do irreversible work last. Details: [references/intent-traps.md](references/intent-traps.md).
- **With UIScene (Capacitor 8.5+) URL delivery moved.** Universal Links and custom-scheme opens reach `SceneDelegate` and are forwarded by `SceneDelegateProxy`, which posts the notifications `@capacitor/app` listens to. If the app still has custom URL code in `AppDelegate`, it no longer runs. Check `capacitor-deep-linking` first if `appUrlOpen` does not fire for a normal link. An intent cannot fix a broken link pipeline.
- **On cold launch the JS listener does not exist yet.** Any route an intent hands to the web layer must survive until JS asks for it: use `App.getLaunchUrl()` for URLs, or a pending-route store plus `notifyListeners(..., retainUntilConsumed: true)` for the local-plugin path.
- **Identifiers are a public contract.** Intent type names, `AppEntity.id` values, `AppEnum` raw values, URL formats and shipped phrases are stored in users' saved shortcuts. Add new ones; do not rename or remove shipped ones without telling the user.

## References

Only load a reference when its topic is in play.

| File | Load when |
|------|-----------|
| [references/project-setup.md](references/project-setup.md) | Creating files, target membership, extensions, App Groups, availability gating, build verification |
| [references/web-bridge.md](references/web-bridge.md) | Connecting an intent to the web layer: URL routing, the local `AppIntentsBridge` plugin, pending routes, shared data |
| [references/intent-traps.md](references/intent-traps.md) | Writing or reviewing any intent, entity, query, phrase, dependency, error or donation |
| [references/ios-26-27-apis.md](references/ios-26-27-apis.md) | `supportedModes`, foreground continuation, long-running/cancellable/undoable intents, execution targets, snippets, Spotlight indexing, schemas, testing |
| [references/widgets-and-controls.md](references/widgets-and-controls.md) | Widget configuration intents, interactive widget buttons, Control Center controls |

## Workflow

### 1. Inspect (read-only)

1. Read `package.json` (`@capacitor/ios` version), `ios/App/App/Info.plist` (scene manifest present?), `ios/App/App/AppDelegate.swift`, `ios/App/App/SceneDelegate.swift`, the App target's deployment target, and any existing `*.entitlements` (Associated Domains, App Groups).
2. Check whether the app already handles deep links in JS (`App.addListener('appUrlOpen', ...)`, `App.getLaunchUrl()`) and which routes exist.
3. Search for existing intents: `grep -rn "AppIntent\|AppShortcutsProvider\|openAppWhenRun" ios/App`.
4. List extension targets (widgets) in `ios/App/App.xcodeproj/project.pbxproj` (`PBXNativeTarget` entries other than `App`).

### 2. Design with the user

For each action the user wants, decide and confirm:

| Question | Options |
|---|---|
| Does it need the UI? | No: background intent, native only. Yes: foreground intent that routes into the web app |
| How does it reach JS? | Universal Link via `OpenURLIntent` (iOS 18+, needs Associated Domains), or a local plugin with a pending-route store (works with custom schemes and iOS 16+) |
| What data does it need? | Fixed set: `AppEnum`. Dynamic, queryable: `AppEntity` + `EntityQuery`. Free text or number: plain `@Parameter` |
| Where must it run? | App target only, or also a widget / control (then the intent file needs both target memberships) |
| Which surfaces? | App Shortcut phrase (at most 10 App Shortcuts per app), Spotlight, widget, control |

Keep one intent per atomic task. Report the plan (files to add, targets, entitlements, JS changes) before editing.

### 3. Implement

1. Create the Swift files in `ios/App/App/Intents/` with the App target membership ([references/project-setup.md](references/project-setup.md)).
2. Write the intents following [references/intent-traps.md](references/intent-traps.md). Gate APIs by version.
3. Add the web bridge ([references/web-bridge.md](references/web-bridge.md)): either reuse the deep-link router, or add the local plugin and register it in a `CAPBridgeViewController` subclass.
4. Add an `AppShortcutsProvider` with `shortTitle`, `systemImageName` and `\(.applicationName)` in every phrase.
5. Add entitlements only when needed (App Groups for shared data, Associated Domains for Universal Links), and on every target that uses them.
6. JS side: handle the route on warm and cold start.

### 4. Verify

```bash
npx cap sync ios
xcodebuild -project ios/App/App.xcodeproj -scheme App \
  -destination 'generic/platform=iOS Simulator' build
# CocoaPods projects: -workspace ios/App/App.xcworkspace
```

- The build log shows the App Intents metadata extraction step with no warnings about phrases. A phrase without `\(.applicationName)` produces a build warning and is dropped at runtime.
- Product > App Shortcuts Preview in Xcode shows the phrases matching.
- Run on a simulator or device: open the Shortcuts app, find the app's actions, run each one.
  - Background intent: completes without the app coming to the foreground. Check the native logs (`ios-android-logs`).
  - Foreground intent, app killed first (cold) and app running (warm): the web view lands on the right route both times.
- Spotlight: search the shortcut title.
- If tests exist, add AppIntentsTesting coverage for iOS 27 test runners ([references/ios-26-27-apis.md](references/ios-26-27-apis.md)).

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| `'AppIntent' is only available in iOS 16.0 or newer` | Capacitor 8 project deploys to iOS 15 | Add `@available(iOS 16.0, *)` to every App Intents type, or raise the deployment target with the user's approval |
| Intent missing from Shortcuts after install | File not in the App target, or metadata extraction failed | Check target membership. Read the build log for the App Intents metadata step. Reinstall the app |
| Phrase never triggers Siri; build warning about the application name | Phrase lacks `\(.applicationName)` | Add the token to every phrase |
| Build error about more than 10 App Shortcuts | Per-app cap | Merge actions or drop low-value ones |
| Crash "...was not initialized prior to access" from `@Dependency` | Dependency registered too late (in a view controller) | Register in `AppDelegate.application(_:didFinishLaunchingWithOptions:)`, which runs on headless launches too |
| Foreground intent opens the app but the web view stays on the home route on cold start | The route was posted before JS added its listener | Use the pending-route store + `retainUntilConsumed`, or `App.getLaunchUrl()` |
| `appUrlOpen` never fires for `OpenURLIntent` | Universal Links not configured, or custom AppDelegate URL code under UIScene | Fix with `capacitor-deep-linking`. `OpenURLIntent` needs a real https Universal Link |
| Swift 6 error: main actor-isolated property cannot satisfy nonisolated requirement | The intent type is marked `@MainActor` | Remove `@MainActor` from the type. Put it on `perform()` or hop inside |
| Background intent killed after about 30 seconds | iOS limit for background intents | Shorten the work, or use `LongRunningIntent` on iOS 27 |
| `'openAppWhenRun' was deprecated in iOS 26.0` | iOS 26 SDK | Add a gated `supportedModes` ([references/ios-26-27-apis.md](references/ios-26-27-apis.md)). Keep `openAppWhenRun` while the deployment target is below 26 |

## Related Skills

- `capacitor-deep-linking`: Universal Links and `appUrlOpen` routing the intents rely on
- `capacitor-uiscene-migration`: required before Xcode 27; moves URL handling to `SceneDelegate`
- `capacitor-plugins`: `@capgo/capacitor-widget-kit` for Live Activities and JS-driven widgets
- `capacitor-testing`: native unit tests and the device verification loop
- `ios-android-logs`: logs from headless intent runs
