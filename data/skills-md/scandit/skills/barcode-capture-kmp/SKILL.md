---
name: barcode-capture-kmp
description: Scandit Barcode Capture (`BarcodeCapture`) in Kotlin Multiplatform (KMP) and Compose Multiplatform projects using Scandit's KMP SDK (`com.kmp.datacapture.*` imports) — the low-level, full-control single-barcode scanning mode without the pre-built SparkScan UI. Use for integration, scan settings, shared-code result handling, overlay and viewfinder customization, or troubleshooting.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# Barcode Capture KMP Skill

## Critical: Do Not Trust Internal Knowledge

Scandit's Kotlin Multiplatform (KMP) SDK is new, shipping in 8.6. Your training data almost certainly predates it and contains **zero** reliable knowledge of its API — do not pattern-match it against the Android or iOS native SDKs you may know. The KMP API packages are `com.kmp.datacapture.*` (NOT `com.scandit.datacapture.*`), and shapes diverge from both native SDKs in specific ways (see below).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names from any other Scandit platform. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

KMP-specific gotchas worth flagging:
- Import root is `com.kmp.datacapture.*` — e.g. `com.kmp.datacapture.barcode.capture.BarcodeCapture`, `com.kmp.datacapture.core.capture.DataCaptureContext`. Never write `com.scandit.datacapture.*` in KMP code.
- `BarcodeCaptureSettings` has no public constructor — use the factory `BarcodeCaptureSettings.barcodeCaptureSettings()` (or the capture-presets overload). Writing `BarcodeCaptureSettings()` is a compile error.
- `codeDuplicateFilter` is a plain `Long` on KMP — **not** `TimeInterval` (iOS/Android-native) and **not** a `.NET TimeSpan`. Do not wrap it in a duration type.
- The listener interface is `BarcodeCaptureListener` with `onBarcodeScanned(barcodeCapture, session, data)` and `onSessionUpdated(barcodeCapture, session, data)` as the two methods you must implement; `onObservationStarted`/`onObservationStopped` have empty default bodies and are optional overrides. The `FrameData` parameter is named `data`.
- `BarcodeCapture.forContext(dataCaptureContext, settings)` is the factory — not `forDataCaptureContext` (Android-native) and not a raw constructor.
- `Camera.getDefaultCamera(BarcodeCapture.createRecommendedCameraSettings())` passes the recommended camera settings directly — there is no separate `applySettings` call needed for initial setup.
- Building the camera preview view (`DataCaptureView`) is **platform-divergent by construction signature**: Android's constructor takes `(context: android.content.Context, dataCaptureContext: DataCaptureContext?)`; iOS's takes only `(dataCaptureContext: DataCaptureContext?)`. Shared `commonMain` code cannot construct a `DataCaptureView` directly — each platform host constructs it and hands it to a shared `setup` function.
- To embed the native view: Android uses the `view.toAndroidView(): View` extension inside a Compose `AndroidView` factory (or a plain `ViewGroup`); iOS uses `view.toUIView(): UIView` inside a `UIViewRepresentable`. These are the *only* supported bridges — never call `toNative()` from application code (it's public only because Kotlin's `internal` cannot span the multi-module KMP SDK).
- `BarcodeCaptureOverlay.withBarcodeCaptureForView(barcodeCapture, view)` attaches the overlay to a specific `DataCaptureView` and adds it in one step conceptually, but you must still call `view.addOverlay(overlay)` yourself — the factory only constructs the overlay. There's also `BarcodeCaptureOverlay.withBarcodeCapture(barcodeCapture)` (no view binding), used by the Compose composable which takes overlays as a declarative list instead.
- Teardown order matters and there is no `onDestroy`: `barcodeCapture.isEnabled = false` → `barcodeCapture.removeListener(this)` → `dataCaptureContext.removeMode(barcodeCapture)` → `camera?.switchToDesiredState(FrameSourceState.OFF)`. Skipping `removeMode` leaves the mode attached to the shared context across screen visits, degrading performance.
- `LaserlineViewfinder` is **NOT available on KMP** — only `RectangularViewfinder` and `AimerViewfinder` ship in the KMP viewfinder package. Do not suggest a laser-line viewfinder for a KMP app.
- The license key placeholder is exactly `-- ENTER YOUR SCANDIT LICENSE KEY HERE --` (matches the canonical sample). Use this exact string, not a different placeholder.
- On Compose Multiplatform, `BarcodeCapture` has **no dedicated `-compose` composable** (unlike SparkScan, BarcodeCount, BarcodeFind, BarcodeAr, BarcodePick). Use the base `core-compose` `DataCaptureView` composable with `overlays = listOf(overlay)` — do not look for a `BarcodeCaptureView` composable, it does not exist.
- Compose overlay instances must be `remember`-ed. The `core-compose` `DataCaptureView` composable diffs `overlays` by content/reference equality every recomposition; a fresh `BarcodeCaptureOverlay` built inline on every recomposition causes constant remove/re-add churn (visible flicker).
- Request the `CAMERA` permission at runtime on Android before starting the camera (the manifest declaration alone is not sufficient) — see the canonical sample's `HomeScreen.kt` permission-launcher pattern. On iOS, `NSCameraUsageDescription` in `Info.plist` triggers the OS permission prompt automatically on first camera use.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch, configuring settings, customizing feedback, adding a viewfinder, handling scans, wiring the Compose Multiplatform view, or doing async work after a scan** (e.g. "add BarcodeCapture to my KMP app", "set up barcode scanning in my shared module", "how do I use BarcodeCapture with Compose Multiplatform", "filter duplicate scans", "suppress the beep", "add a viewfinder", "disable scanning while I look up the barcode") → read `references/integration.md` and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names — and never carry over a signature from the Android-native or iOS-native SDKs without verifying it also holds for KMP. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Get Started](https://docs.scandit.com/sdks/kmp/barcode-capture/get-started/) |
| Configure symbologies | [Configure Barcode Symbologies](https://docs.scandit.com/sdks/kmp/barcode-capture/configure-barcode-symbologies/) |
| Compose Multiplatform | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
| Core concepts (context, camera, views) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
