---
name: matrixscan-count-kmp
description: MatrixScan Count (BarcodeCount) in Kotlin Multiplatform (KMP) projects — com.scandit.datacapture.kmp:* Maven artifacts (Scandit/datacapture-kmp-spm on iOS), com.kmp.datacapture.barcode.count imports. Counting and receiving workflows shared across Android/iOS with the Compose composable or base BarcodeCountView. Use for integration, settings configuration, listener wiring, view customization, status mode, or troubleshooting counting workflows.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# MatrixScan Count KMP Skill

## Critical: Do Not Trust Internal Knowledge

Your training data almost certainly has **no coverage of the Scandit Kotlin Multiplatform (KMP) SDK** — it is a new SDK surface (`com.kmp.datacapture.*` packages, first published at version 8.6) sitting on top of the existing Android/iOS native SDKs. Do not pattern-match from the native Android SDK (`com.scandit.datacapture.*`), the Flutter/RN/.NET bindings, or any other Scandit platform skill — package names, constructor shapes, and what is exposed through Compose vs. the base view are all different here.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

KMP-specific gotchas worth flagging:

- The Maven group is `com.scandit.datacapture.kmp`, with artifacts `core`, `barcode`, and `barcode-compose`. On iOS, the app depends on the **`Scandit/datacapture-kmp-spm`** Swift package, which vends **one Kotlin framework** — there is no separate CocoaPods/SPM dependency per Scandit module the way native iOS apps have.
- All Kotlin API packages are `com.kmp.datacapture.*` (e.g. `com.kmp.datacapture.barcode.count.BarcodeCount`), not `com.scandit.datacapture.*` — that package is the wrapped native implementation and is never imported by app code.
- **Two ways to host the view — they expose different surfaces, not just different syntax:**
  - The **Compose Multiplatform wrapper** — `@Composable fun BarcodeCountView(...)` in `com.kmp.datacapture.barcode.compose` — is the fastest path and is what the official `MatrixScanCountSimpleSample` uses on Android. It only exposes: `settings`, `style`, button-visibility booleans (`showUserGuidanceView/showListButton/showExitButton/showShutterButton/showToolbar/showSingleScanButton`), `onScan`, `onExitTap`/`onListTap`/`onSingleScanTap`, an `overlay` slot, and an escape-hatch `barcodeCount` override.
  - It does **not** expose brushes, icons, hint text, toolbar settings, the status provider, hardware trigger, tap-to-uncount, filter highlight settings, accessibility labels, or per-barcode delegate callbacks. For any of those you must drop to the **base (non-Compose) `BarcodeCountView`** class in `com.kmp.datacapture.barcode.count` and host it yourself (`toAndroidView()` on Android, `toUIView()` on iOS) — see `references/integration.md` for both the Compose and base-view interop patterns. Do not tell a user "just set `recognizedBrush` on the `BarcodeCountView` composable" — that parameter does not exist on the composable.
- **The base `BarcodeCountView` constructor differs per platform and cannot be called uniformly from shared `commonMain` code**: Android's is `BarcodeCountView(context: Context, barcodeCount: BarcodeCount, style: BarcodeCountViewStyle = ICON)`; iOS's is `BarcodeCountView(barcodeCount: BarcodeCount, style: BarcodeCountViewStyle = ICON)` (no `Context` — it derives everything from the mode). Base-view construction therefore happens in **platform-specific** code (an Android Activity/Compose `AndroidView`, or Swift via `UIViewRepresentable`), exactly like the sample's iOS `ScannerView.swift` does.
- **`BarcodeCount.forContext(dataCaptureContext, settings)`** is the constructor (not `BarcodeCount(settings)` — that Flutter/JS-only overload does not exist on KMP). Camera settings: `BarcodeCount.createRecommendedCameraSettings()` is a **method** on Android/KMP (unlike iOS/.NET native, where it is a property).
- **No SDK-initialize step is needed** (unlike Flutter's `await ScanditFlutterDataCaptureBarcode.initialize()`). `DataCaptureContext.forLicenseKey(licenseKey)` (or `DataCaptureContext.sharedInstance` after `DataCaptureContext.initialize(licenseKey)`) is usable immediately.
- **`BarcodeCountListener.onScan(barcodeCount, session, frameData)` is synchronous** — `frameData: FrameData` is passed directly, not behind a suspend/async accessor the way Flutter's `Future<FrameData> Function()` works. There is no `didUpdateSession`; the equivalent is `onSessionUpdated(barcodeCount, session, frameData)` (default no-op, override if needed), which fires on every processed frame, not just on shutter press.
- **Symbology enum values are SCREAMING_SNAKE_CASE**: `Symbology.EAN13_UPCA`, `Symbology.CODE128`, `Symbology.CODE39` — not `Symbology.Code128` (C#) or `Symbology.code128` (Dart/Flutter).
- **List scanning was NOT wired up end-to-end as of KMP 8.6** (verify against the API reference if
  the project is on a later version — this is a gap Scandit may have since closed). `BarcodeCountCaptureList`, `TargetBarcode`, `BarcodeCountCaptureListListener`, and `BarcodeCountCaptureListSession` all exist and are constructible, and `BarcodeCountView.barcodeNotInListActionSettings` / `BarcodeCountSettings.disableModeWhenCaptureListCompleted` exist as properties — but there is **no method on `BarcodeCount`** to attach a built `BarcodeCountCaptureList` to the mode (the native SDKs' `SetBarcodeCountCaptureList`/`setCaptureList` has no `kmp` entry in the API docs' `:available:` list, and the KMP `BarcodeCount` expect/actual class has no such member). Do not invent a `setBarcodeCountCaptureList(...)` call — it does not compile. Treat scanning-against-a-list as **not yet available** on KMP and say so if asked; do not silently build the settings/listener plumbing and imply it works end to end.
- **`toAndroidView()` / `toUIView()`** are the typed escape hatches from a KMP view wrapper to the platform-native view: `toAndroidView()` is an extension function (`com.kmp.datacapture.barcode.ui.toAndroidView`) on Android, `toUIView()` is a member function on iOS. Use them, not `toNative()` (internal SDK bridging API — not for app code).
- License placeholder must be exactly: `"-- ENTER YOUR SCANDIT LICENSE KEY HERE --"`.

## Intent Routing

This skill has a single reference file. For any MatrixScan Count / BarcodeCount request on KMP — integrating from scratch, hosting the view (Compose or base-view interop), capture lists, status mode, toolbar/UI customization, lifecycle, or troubleshooting — read `references/integration.md` and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports — and do not assume an API that exists on native Android/iOS or another Scandit platform binding also exists on KMP (KMP is a young surface with real gaps — see the capture-list gotcha above). If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index and extract the actual link from it.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| KMP integration | [Intro](https://docs.scandit.com/sdks/kmp/matrixscan-count/intro/) · [Get Started](https://docs.scandit.com/sdks/kmp/matrixscan-count/get-started/) |
| Advanced (status mode, filtering, styling) | [Advanced Configurations](https://docs.scandit.com/sdks/kmp/matrixscan-count/advanced/) |
| Core concepts (context, camera, views) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
