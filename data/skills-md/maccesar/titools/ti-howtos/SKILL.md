---
name: ti-howtos
description: "Titanium SDK native feature integration guide. Use when implementing, reviewing, analyzing, or examining Titanium location services, maps (Google Maps v2, Map Kit), push notifications (APNs, FCM), camera/gallery, media APIs, SQLite databases, HTTPClient networking, WKWebView, Android Intents, background services, iOS Keychain/iCloud, WatchKit/Siri integration, or CI/CD with Fastlane and Appium."
argument-hint: "[feature]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Bash(node *)
---

# Titanium SDK how-tos

Hands-on guide to Titanium SDK native integrations. Focuses on practical steps, platform differences, and the details that usually bite.

## Project detection

::::info Auto-detects Titanium projects
This skill detects Titanium projects automatically.

Indicators:
- `tiapp.xml` exists (definitive)
- Alloy project: `app/` folder
- Classic project: `Resources/` folder

Behavior:
- Titanium detected: provide native integration guidance, permissions, modules, and platform notes
- Not detected: say this skill is for Titanium projects only
::::

## Integration workflow

1. Requirement check: permissions, `tiapp.xml`, and module dependencies.
2. Service setup: listeners and services (Location, Push, Core Motion, and so on).
3. Lifecycle sync: tie listeners to Android and iOS lifecycle events.
4. Error handling: use robust callbacks for async native calls.
5. Platform optimization: apply platform-specific logic (Intent filters, Spotlight, Core Motion).

## Native integration rules

### iOS permissions
- Location: `NSLocationWhenInUseUsageDescription` or `NSLocationAlwaysAndWhenInUseUsageDescription` in `tiapp.xml`.
- Motion activity: required for Core Motion Activity API.
- Camera and photo: `NSCameraUsageDescription` and `NSPhotoLibraryUsageDescription`.
- Background modes: required for background audio, location, or VOIP.
- iOS 17+: add `PrivacyInfo.xcprivacy` for UserDefaults and File Timestamps.

### Android resource management
- Services: stop background services when they are no longer needed.
- Location: use `distanceFilter` and FusedLocationProvider (requires `ti.playservices`).
- Intents: set action, data type, and category. Copy the root activity to `tiapp.xml` for intent filters.

### Data and networking
- HTTPClient: handle both `onload` and `onerror`.
- SQLite: close both `db` and `resultSet` to avoid locks.
- Filesystem: check `isExternalStoragePresent()` before using SD card storage.
- Binary data: use `Ti.Buffer` and `Ti.Codec` for byte-level work.
- Streams: use `BufferStream`, `FileStream`, or `BlobStream` for chunked I/O.

### Media and memory
- Camera and gallery: use `imageAsResized` to reduce memory pressure.
- Audio: handle `pause` and `resume` for streaming interruptions.
- WebView: avoid TableView embedding; set `touchEnabled=false` if needed.
- Video: Android requires fullscreen; iOS supports embedded players.

### Platform-specific properties

::::danger Platform-specific properties need modifiers
Using `Ti.UI.iOS.*` or `Ti.UI.Android.*` without platform modifiers can break cross-platform builds.

Bad example:
```javascript
// Wrong: adds Ti.UI.iOS to Android build
const win = Ti.UI.createWindow({
  statusBarStyle: Ti.UI.iOS.StatusBar.LIGHT_CONTENT
});
```

Good options:

TSS modifier (Alloy):
```tss
"#mainWindow[platform=ios]": {
  statusBarStyle: Ti.UI.iOS.StatusBar.LIGHT_CONTENT
}
```

Conditional code:
```javascript
if (OS_IOS) {
  $.mainWindow.statusBarStyle = Ti.UI.iOS.StatusBar.LIGHT_CONTENT;
}
```

Always require modifiers:
- iOS: `statusBarStyle`, `modalStyle`, `modalTransitionStyle`, any `Ti.UI.iOS.*`.
- Android: `actionBar` config, any `Ti.UI.Android.*` constant.

For TSS platform modifiers, see the code conventions in `skills/ti-expert/references/code-conventions.md#platform--device-modifiers` or the platform UI guides in `references/ios-platform-deep-dives.md`.
::::

## Reference guides

### Core features
- [Location and maps](references/location-and-maps.md): GPS tracking and battery-efficient location rules.
- [Google Maps v2 (Android)](references/google-maps-v2.md): API keys, Google Play Services, and v2 features.
- [iOS Map Kit](references/ios-map-kit.md): 3D camera, system buttons, and iOS callouts.
- [Notification services](references/notification-services.md): push notifications (APNs/FCM), local alerts, interactive notifications.

### Data handling
- [Remote data sources](references/remote-data-sources.md): HTTPClient lifecycle, JSON/XML parsing, uploads, downloads, sockets, SOAP, SSL.
- [Local data sources](references/local-data-sources.md): filesystem operations, SQLite, Properties API, persistence strategy.
- [Buffer, Codec, and Streams](references/buffer-codec-streams.md): binary data manipulation and serial data flows.

### Media and content
- [Media APIs](references/media-apis.md): audio playback and recording, video streaming, camera and gallery, ImageViews, density assets.

### Web integration
- [Web content integration](references/web-content-integration.md): WebView (WKWebView), local and remote content, bidirectional communication.
- [Webpack build pipeline](references/webpack-build-pipeline.md): Ti 9.1.0+ build pipeline, npm integration, and the `@` alias.

### Platform-specific (Android)
- [Android platform deep dives](references/android-platform-deep-dives.md): intents, intent filters, broadcast permissions, background services.

### Platform-specific (iOS)
- [iOS platform deep dives](references/ios-platform-deep-dives.md): iOS 17 privacy, silent push, Spotlight, Handoff, iCloud, Core Motion, WatchKit and Siri.

### Advanced and DevOps
- [Extending Titanium](references/extending-titanium.md): Hyperloop, native modules (Proxy and View), Xcode debugging, AndroidX migration for SDK 9.0.
- [Debugging and profiling](references/debugging-profiling.md): memory management, leak detection, native tools.
- [Automation (Fastlane and Appium)](references/automation-fastlane-appium.md): CI/CD, UI testing, store deployment.

## Related skills

For tasks beyond native feature integration, use:

| Task                                           | Use this skill |
| ---------------------------------------------- | -------------- |
| Project architecture, services, memory cleanup | `ti-expert`    |
| UI layouts, ListViews, gestures, animations    | `ti-ui`        |
| Hyperloop, app distribution, tiapp.xml config  | `ti-guides`    |
| Alloy MVC, models, data binding                | `alloy-guides` |

## Response format

1. Prerequisites: required permissions, `tiapp.xml` config, or modules.
2. Step-by-step implementation: task-focused code guide with error handling.
3. Platform caveats: iOS and Android differences.
4. Best practices: memory, lifecycle, and performance tips.
