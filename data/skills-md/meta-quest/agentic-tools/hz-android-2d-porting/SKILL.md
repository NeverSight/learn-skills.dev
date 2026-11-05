---
name: hz-android-2d-porting
license: Apache-2.0
description: "Guides porting existing Android 2D apps to Meta VR and Horizon OS — input adaptation, panel layout, and design requirements. Use when adapting a mobile Android app for Meta VR. For UI design decisions, use hz-panel-designer if available. Build path: Standard Android; use hz-quest-verify-first if the build path is unclear."
allowed-tools: Bash(metavr:*), Bash(hzdb:*)
---

# Android 2D App Porting to Horizon OS

## When to Use

Use this skill when:

- Porting an existing Android 2D app to run on Meta VR headsets
- Adapting a mobile Android app for Horizon OS panels
- Troubleshooting input, layout, or compatibility issues with a 2D app on Meta VR devices
- Preparing an Android app for Horizon Store submission
- Evaluating whether an existing Android app is compatible with Horizon OS

## Overview

Horizon OS is built on Android (AOSP) and can run standard Android applications inside **panels** -- floating 2D windows positioned in 3D space. Most well-built Android apps work on Meta VR devices with minimal changes, but several areas require attention:

1. **Input**: There is no touchscreen. Users interact via controller pointer (ray-casting), hand tracking, or connected peripherals.
2. **Layout**: Apps run in resizable panels, not full-screen on a fixed display.
3. **Compatibility**: Dependencies and permissions must work without Google Play Services or unavailable hardware.
4. **Design and performance**: Apps must meet Horizon Store requirements on mobile hardware.

The goal of porting is to make the app feel native to the Meta VR experience while preserving existing functionality.

## Porting Workflow

### Step 1: Initial Testing

Build and install the existing app with its normal Android workflow. Android Studio, Gradle, and `adb` all work with a connected Meta VR device:

```bash
./gradlew installDebug
adb shell am start -n com.example.yourapp/.MainActivity
```

Prefer `metavr app install <apk>` and `metavr app launch <package>` over raw adb here, then stream `metavr adb logcat --follow` during this first run. Note any immediate crashes, black screens, input problems, or layout breakage.

### Step 2: Compatibility Audit

Check whether the app depends on Google Play Services, unsupported hardware, or prohibited permissions before changing its UI. Make unsupported features optional or replace them with Horizon OS alternatives. See [Compatibility Requirements](references/compatibility-requirements.md).

### Step 3: Input Adaptation

The most common porting issue is input. Touch events are translated from the controller pointer, but:

- **Hover states** are now visible (users point before clicking)
- **Scrolling** uses the thumbstick, not swipe gestures
- **Multi-touch** gestures (pinch-to-zoom) do not translate directly
- **Tap targets** must be large enough for pointer accuracy (48dp minimum)

See [Input Adaptation Reference](references/input-adaptation.md) for detailed guidance.

### Step 4: Layout Adjustment

Panels are resizable and can have various aspect ratios. Your app must handle:

- Dynamic width and height changes
- Landscape and portrait orientations
- Different effective DPI values

Use responsive Android layouts and window-size breakpoints. See [Panel Layout Reference](references/panel-layout.md).

### Step 5: Gradle and Manifest Updates

Update your build configuration to target Horizon OS:

```kotlin
// build.gradle.kts
android {
    defaultConfig {
        minSdk = 29       // Android 10 minimum
        targetSdk = 34    // API 34 or higher required for all new 2D panel apps
    }
}
```

Add required manifest entries for device targeting. See [Gradle Setup Reference](references/gradle-setup.md).

### Step 6: Input Testing

Test with all supported input methods:

- **Controller**: point-and-click, thumbstick scroll, trigger tap
- **Hand tracking**: pinch-to-select, hand scroll
- **Keyboard/mouse**: Bluetooth peripherals, system keyboard for text fields

Use the Meta Spatial Simulator for rapid desktop iteration, then validate on-device with the Meta Horizon OS Android Studio plugin or normal ADB tooling. Keep `metavr adb logcat --follow` running during each input pass — it catches input errors that don't visibly crash.

### Step 7: Store Submission

Before submitting to the Horizon Store:

- Verify all [Compatibility Requirements](references/compatibility-requirements.md)
- Test on at least Quest 3, Quest 3S, and Quest 2 (if targeting them), plus Meta VR Glasses
- Confirm the app works in both passthrough and immersive home environments
- Review Meta's content policies and technical requirements

## Quick Compatibility Check

### Works on Horizon OS

| Feature | Status | Notes |
|---|---|---|
| Standard Android Views | Supported | TextView, RecyclerView, etc. |
| Jetpack Compose | Supported | Full Compose UI toolkit |
| React Native | Supported | Uses the standard Android application path |
| WebView | Supported | Chromium-based |
| Media playback (ExoPlayer) | Supported | Video and audio |
| Networking (HTTP, WebSocket) | Supported | Wi-Fi connectivity |
| Room / SQLite | Supported | Local database |
| WorkManager | Supported | Background tasks |
| Notifications | Supported | Horizon OS notification panel |
| Bluetooth (peripherals) | Supported | Keyboard, mouse, gamepad |
| Android Accessibility APIs | Supported | TalkBack equivalent available |

### Restricted or Unavailable

| Feature | Status | Notes |
|---|---|---|
| Telephony / SMS | Not available | No cellular radio |
| NFC | Not available | No NFC hardware |
| GPS / Fine location | Limited | Wi-Fi-based location only |
| Fingerprint / BiometricPrompt | Not available | Use Meta account auth instead |
| Multiple app-owned panels | Limited | Use the current public multi-panel guidance when available |
| Google Play Services | Not available | Use Meta equivalents or alternatives |
| ARCore | Not available | Use Meta Spatial SDK for spatial features |
| Multi-touch gestures | Limited | Single pointer from controller |

### Common Issues and Fixes

| Issue | Cause | Fix |
|---|---|---|
| App crashes on launch | Missing Google Play Services dependency | Remove or make GMS optional |
| Buttons too small to tap | Touch targets under 48dp | Increase minimum tap target size |
| Keyboard doesn't appear | Custom input field not using `InputConnection` | Use standard `EditText` or `TextField` |
| Layout broken | Fixed-size layout assumptions | Use responsive Views or Compose layouts |
| App requests unavailable permissions | Telephony, NFC, or other absent hardware | Guard with `hasSystemFeature()` checks |
| APK rejected for prohibited permissions | Library or plugin silently added a prohibited permission | Run `aapt dump permissions your-app.apk`, then check [prohibited list](https://developers.meta.com/horizon/resources/permissions-prohibited/) |
| APK rejected for invalid signature | Signed with v1-only scheme | v2 signing is default in AGP 7.0+; for older AGP, add `v2SigningEnabled = true` to your signing config |

## Testing Tools

- **Meta Horizon OS Android Studio plugin**: Device connection, deployment, and Horizon OS development support
- **Meta Spatial Simulator**: Desktop simulation for 2D Android apps on Horizon OS
- **Android Studio, Gradle, and ADB**: Standard Android build, install, launch, and logcat workflows
- **metavr**: Optional command-line convenience for device and app operations

## Performance Considerations

Meta VR devices have mobile-class hardware with strict thermal limits:
- **GPU**: Qualcomm Adreno (varies by model)
- **RAM**: 6-12 GB shared between system and apps
- **Thermal**: Sustained workloads may trigger thermal throttling
- Avoid heavy overdraw and complex shader effects in 2D UI
- Minimize background work to reduce power consumption
- Test with representative data loads (large lists, images, etc.)

## References

- [Compatibility Requirements](references/compatibility-requirements.md) -- store requirements and API compatibility
- [Input Adaptation](references/input-adaptation.md) -- adapting touch to controller and hand input
- [Panel Layout](references/panel-layout.md) -- responsive layout for Horizon OS panels
- [Gradle Setup](references/gradle-setup.md) -- build configuration and manifest entries
