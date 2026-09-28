---
name: matrixscan-batch-kmp
description: MatrixScan Batch (MatrixScan, BarcodeBatch, Scandit KMP) in Kotlin Multiplatform (KMP) projects (`com.scandit.datacapture.kmp` packages, `com.kmp.datacapture.*` imports) — tracking and scanning multiple barcodes at once in shared commonMain code with Android/iOS hosts and the Compose Multiplatform DataCaptureView. Use for integration, settings and symbologies, tracked-barcode handling, overlay customization, lifecycle, or troubleshooting.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# MatrixScan Batch KMP Skill

## Critical: Do Not Trust Internal Knowledge

Scandit's Kotlin Multiplatform (KMP) SDK is new, shipping in 8.6. Your training data almost
certainly predates it and contains **zero** reliable knowledge of its API — do not pattern-match
it against the Android or iOS native SDKs you may know. The KMP API packages are
`com.kmp.datacapture.*` (NOT `com.scandit.datacapture.*`), and shapes diverge from both native
SDKs in specific ways (see below).

**Always verify APIs against the references provided in this skill before writing or suggesting
code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot
find an API in the provided references, fetch the relevant documentation page before responding.

KMP-specific gotchas worth flagging:

- **Factory, not constructor.** `BarcodeBatch.forContext(dataCaptureContext, settings)` is a
  `companion object` factory function — not a public constructor, and not native Android's
  `BarcodeBatch.forDataCaptureContext(context, settings)` name.
- **Settings are built via a factory, not `X()`.** `BarcodeBatchSettings.barcodeBatchSettings()`
  is a companion factory function. `BarcodeBatchSettings` has no public no-arg constructor in KMP.
- **Overlays always need an explicit `view.addOverlay(overlay)` call.** Unlike native Android's
  `BarcodeBatchBasicOverlay.newInstance(mode, view)`, which auto-adds itself to the view, KMP's
  factories do not attach the overlay for you — the reference sample always follows overlay
  creation with `view.addOverlay(overlay)`, regardless of which factory was used:
  - `BarcodeBatchBasicOverlay.withBarcodeBatch(barcodeBatch)` — no view; must call `addOverlay`.
  - `BarcodeBatchBasicOverlay.withBarcodeBatchForView(barcodeBatch, view)` — takes a view, but
    still requires the explicit `addOverlay` call.
  - `BarcodeBatchAdvancedOverlay.withBarcodeBatch(barcodeBatch)` — the **only** advanced-overlay
    factory (there is no `ForView` variant); `addOverlay` is mandatory.
- **`BarcodeBatchBasicOverlayListener` is wired with a function, not a property.** Call
  `overlay.setListener(this)` — there is no settable `overlay.listener` property on
  `BarcodeBatchBasicOverlay` in KMP (unlike native Android's `overlay.listener = this`).
  `BarcodeBatchAdvancedOverlay` is the opposite: it exposes a real settable property,
  `advancedOverlay.listener = this`. Do not mix these two patterns up.
- **No factory sets the overlay style at creation time.** Native Android/iOS have a 3-argument
  `newInstance(mode, view, style)` overload to pick `BarcodeBatchBasicOverlayStyle.DOT` at
  construction. KMP's `withBarcodeBatch` / `withBarcodeBatchForView` factories take **no style
  parameter**, and `overlay.style` is a read-only property. As of the current KMP API surface,
  there is no documented way to construct a DOT-style overlay — every overlay is created with the
  default FRAME style. Tell the user this is a known KMP gap rather than inventing a style
  parameter or a `setProperty("style", …)` workaround.
- **`createRecommendedCameraSettings()` exists on KMP's `BarcodeBatch`**, mirroring native
  Android/Flutter — it is a real, documented `companion object` method
  (`BarcodeBatch.createRecommendedCameraSettings(): CameraSettings`). Don't assume it is missing;
  build custom `CameraSettings()` only when the app has a specific reason to override the default
  (e.g. a higher `preferredResolution` for small/distant barcodes).
- **`Camera.getDefaultCamera(...)` returns `Camera?`** — always null-check before use.
- **Teardown uses `dataCaptureContext.removeMode(barcodeBatch)`**, not `removeCurrentMode()`.
- **`viewForTrackedBarcode` returns `NativeView?`**, a KMP `expect`/`actual` typealias that
  resolves directly to `android.view.View` on Android and `UIView` on iOS — no wrapper type, no
  cast needed. Build the platform view in platform code (or a lambda the platform host supplies)
  since `commonMain` cannot construct an `android.view.View` or `UIView` directly.
- **`Feedback` has no public constructor on KMP.** Build it via `Feedback.defaultFeedback()`, then
  optionally override its `sound` / `vibration` properties — there is no
  `Feedback(vibration, sound)` two-argument constructor like native Android's.
  `BarcodeBatch` still emits no feedback automatically; call `feedback.emit()` yourself from
  `onSessionUpdated`.
- **Per-barcode brush customization and `BarcodeBatchAdvancedOverlay` both require the MatrixScan
  AR add-on license** — same requirement as native Android/iOS.
- **`didTapViewForTrackedBarcode` (the advanced-overlay tap callback) is not part of the KMP
  `BarcodeBatchAdvancedOverlayListener`.** It only exists on web/cordova/react-native/flutter/
  capacitor. Don't offer it on KMP.
- Symbology names use underscores, same as native Android: `Symbology.EAN13_UPCA`,
  `Symbology.CODE128`, `Symbology.QR` — not camelCase.
- All symbologies are disabled by default in `BarcodeBatchSettings`. Enable only what the app
  needs to keep tracking performance high.
- The license key placeholder is exactly `-- ENTER YOUR SCANDIT LICENSE KEY HERE --`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeBatch from scratch, or extending an existing integration** (e.g. "add
  MatrixScan Batch to my KMP app", "track multiple barcodes in Kotlin Multiplatform", "how do I
  highlight tracked barcodes", "how do I show an AR bubble/info view over each tracked barcode",
  "how do I use BarcodeBatch with Compose Multiplatform", "react to barcodes leaving the frame",
  "beep when a new barcode is tracked") → read `references/integration.md` and follow the
  instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or
guess method signatures, parameters, or property names. If unsure whether an API exists or how it
is called — or if a compile error occurs — fetch the relevant reference page before responding.
Do not tell the user to check the docs themselves. After answering, always include the relevant
link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API
page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic
   pages link directly to relevant API symbols. Always request links alongside content in your
   fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table
   below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Intro](https://docs.scandit.com/sdks/kmp/matrixscan/intro/) · [Get Started](https://docs.scandit.com/sdks/kmp/matrixscan/get-started/) |
| AR overlays (BasicOverlay brushes, AdvancedOverlay views) | [Advanced Configurations](https://docs.scandit.com/sdks/kmp/matrixscan/advanced/) |
| Core concepts (context, camera, views) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
