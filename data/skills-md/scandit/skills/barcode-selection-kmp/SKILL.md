---
name: barcode-selection-kmp
description: Barcode Selection (BarcodeSelection) in Kotlin Multiplatform (KMP) projects — com.scandit.datacapture.kmp Maven artifacts, com.kmp.datacapture.barcode.selection imports. Tap-to-select or aim-to-select one barcode among many visible at once in dense scenes, shared across Android/iOS with the Compose Multiplatform DataCaptureView. Use for integration, selection-strategy configuration, result handling, overlay brushes, or troubleshooting selection.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# Barcode Selection KMP Skill

## Critical: Do Not Trust Internal Knowledge

Scandit's Kotlin Multiplatform (KMP) SDK is new, shipping in 8.6. Your training data almost certainly predates it and contains **zero** reliable knowledge of its API — do not pattern-match it against the Android or iOS native SDKs you may know, and do not pattern-match it against the `barcode-capture-kmp` skill either: `BarcodeSelection` diverges from `BarcodeCapture` in several specific ways even within the same KMP SDK. The API packages are `com.kmp.datacapture.*` (NOT `com.scandit.datacapture.*`).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names from any other Scandit platform or mode. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

KMP-specific gotchas worth flagging:
- Import root is `com.kmp.datacapture.barcode.selection.*` for the mode/settings/session/listener/overlay, `com.kmp.datacapture.barcode.data.*` for `Symbology`/`Barcode`/`CapturePreset`. Never write `com.scandit.datacapture.*` in KMP code.
- `BarcodeSelectionSettings` has no public constructor — use the factory `BarcodeSelectionSettings.barcodeSelectionSettings()`, or `BarcodeSelectionSettings.barcodeSelectionSettings(capturePresets: Set<CapturePreset>)` to pre-tune for a vertical (`CapturePreset.RETAIL`, `.LOGISTICS`, `.TRANSPORT`, `.HEALTHCARE`, `.MANUFACTURING`). Writing `BarcodeSelectionSettings()` is a compile error.
- The mode factory is `BarcodeSelection.forContext(dataCaptureContext, settings)` — not `forDataCaptureContext` (Android-native) and not a raw constructor.
- `settings.selectionType` takes a `BarcodeSelectionType` built from a factory, not a constructor: `BarcodeSelectionTapSelection.tapSelection()` or `BarcodeSelectionAimerSelection.aimerSelection()`. Defaults to tap selection.
- Switching between Tap-to-Select and Aim-to-Select at runtime does **not** require recreating `BarcodeSelection`: mutate `settings.selectionType` and call `barcodeSelection.applySettings(settings)` (synchronous on KMP — there is no async/`Task`-returning overload here, unlike some other platforms).
- Aimer selection has its own `selectionStrategy` (`BarcodeSelectionAutoSelectionStrategy()` — auto-selects once the algorithm understands intent — or `BarcodeSelectionManualSelectionStrategy()` — requires aiming + a tap/`selectAimedBarcode()` call — defaults to manual) and its own `aimerBehavior` (`BarcodeSelectionAimerBehavior.TOGGLE_SELECTION` / `.REPEAT_SELECTION`, defaults to `REPEAT_SELECTION`). Tap selection instead has `freezeBehavior` (`BarcodeSelectionFreezeBehavior.MANUAL` / `.MANUAL_AND_AUTOMATIC`) and `tapBehavior` (`BarcodeSelectionTapBehavior.TOGGLE_SELECTION` / `.REPEAT_SELECTION`).
- The listener interface is `BarcodeSelectionListener` with `onSelectionUpdated(barcodeSelection, session, frameData)` and `onSessionUpdated(barcodeSelection, session, frameData)` as the two methods you must implement (`onObservationStarted`/`onObservationStopped` have empty default bodies and are optional). Note the parameter is `frameData: FrameData?` — **nullable** (it is `null` when the camera is frozen and the selection changes) — unlike `BarcodeCaptureListener`'s non-null `data: FrameData`.
- Read newly selected/unselected barcodes from `session.newlySelectedBarcodes` / `session.newlyUnselectedBarcodes` (both `List<Barcode>`, not a single nullable barcode like `BarcodeCapture`'s `newlyRecognizedBarcode`). Use `session.getCount(barcode)` to read how many times a barcode has been selected (relevant with `BarcodeSelectionTapBehavior.REPEAT_SELECTION` / `BarcodeSelectionAimerBehavior.REPEAT_SELECTION`, where re-selecting bumps a counter instead of toggling off).
- `BarcodeSelection.createRecommendedCameraSettings()` is a companion function on `BarcodeSelection` itself (same shape as `BarcodeCapture`).
- `barcodeSelection.freezeCamera()` / `barcodeSelection.unfreezeCamera()` freeze/resume the live preview so users can carefully tap multiple codes without them moving; `barcodeSelection.selectUnselectedBarcodes()` selects everything currently tracked; `barcodeSelection.selectAimedBarcode()` is for **manual** aimer selection only; `barcodeSelection.reset()` clears the selection history (counts) without touching enabled/camera state.
- `BarcodeSelectionBasicOverlay` has two factories: `withBarcodeSelectionForView(barcodeSelection, view)` — binds to a specific `DataCaptureView`, adds itself automatically — and `withBarcodeSelection(barcodeSelection)` (no view binding, used by the Compose composable's declarative `overlays` list).
- The overlay exposes **four** brush properties, not one: `trackedBrush` (barcode recognized but not yet selected/aimed), `aimedBrush` (currently aimed at, aimer mode only), `selectingBrush` (transient, during the moment of selection), and `selectedBrush` (currently selected). Get style defaults via `BarcodeSelectionBasicOverlay.defaultTrackedBrushForStyle(style)` / `defaultAimedBrushForStyle(style)` / `defaultSelectedBrushForStyle(style)` / `defaultSelectingBrushForStyle(style)`, where `style` is `BarcodeSelectionBasicOverlayStyle.FRAME` (default) or `.DOT`.
- The overlay's `viewfinder` property is **read-only** (`val`, not `var`) — unlike `BarcodeCaptureOverlay.viewfinder`, you cannot assign a different `Viewfinder` instance. It is only visible when `selectionType` is `BarcodeSelectionAimerSelection`. Style it through the overlay's own hint/brush setters instead of swapping the viewfinder.
- `barcodeSelection.setFeedback(soundEnabled: Boolean, vibrationEnabled: Boolean)` is a KMP convenience method for the common case; for finer control assign a `BarcodeSelectionFeedback` instance to `barcodeSelection.feedback` (its `selection: Feedback` property holds the actual sound/vibration).
- Building the camera preview view (`DataCaptureView`) is **platform-divergent by construction signature**, same as every other KMP mode: Android's constructor takes `(context: android.content.Context, dataCaptureContext: DataCaptureContext?)`; iOS's takes only `(dataCaptureContext: DataCaptureContext?)`. Shared `commonMain` code cannot construct a `DataCaptureView` directly — each platform host constructs it and hands it to a shared `setup` function.
- To embed the native view: Android uses `view.toAndroidView(): View` inside a Compose `AndroidView` factory; iOS uses `view.toUIView(): UIView` inside a `UIViewRepresentable`. These are the *only* supported bridges — never call `toNative()` from application code (it is `public` only because Kotlin's `internal` cannot span the multi-module KMP SDK).
- Teardown order matters and there is no `onDestroy`: `barcodeSelection.isEnabled = false` → `barcodeSelection.removeListener(this)` → `dataCaptureContext.removeMode(barcodeSelection)` → `camera?.switchToDesiredState(FrameSourceState.OFF)`. Skipping `removeMode` leaves the mode attached to the shared context across screen visits.
- `BarcodeSelection` requires the MatrixScan add-on entitlement on the license (per the platform-agnostic API doc). If a user's license lacks it, `BarcodeSelection` will not function — this is a licensing question, not a code bug.
- The license key placeholder is exactly `-- ENTER YOUR SCANDIT LICENSE KEY HERE --` (matches the canonical sample). Use this exact string, not a different placeholder.
- On Compose Multiplatform, `BarcodeSelection` has **no dedicated `-compose` composable**. Use the base `core-compose` `DataCaptureView` composable with `overlays = listOf(overlay)` — do not look for a `BarcodeSelectionView` composable, it does not exist.
- Compose overlay instances must be `remember`-ed. The `core-compose` `DataCaptureView` composable diffs `overlays` by content/reference equality every recomposition; a fresh `BarcodeSelectionBasicOverlay` built inline on every recomposition causes constant remove/re-add churn (visible flicker).
- Request the `CAMERA` permission at runtime on Android before starting the camera (the manifest declaration alone is not sufficient). On iOS, `NSCameraUsageDescription` in `Info.plist` triggers the OS permission prompt automatically on first camera use.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeSelection from scratch, choosing tap vs aimer selection, configuring selection strategies, handling selections and per-barcode counts, freezing/unfreezing the camera, customizing overlay brushes, wiring the Compose Multiplatform view, or troubleshooting selection behavior** (e.g. "add BarcodeSelection to my KMP app", "let users tap to select barcodes", "switch to aim-to-select", "how many times was this barcode selected", "freeze the camera while selecting", "use BarcodeSelection with Compose Multiplatform") → read `references/integration.md` and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names — and never carry over a signature from `BarcodeCapture`, or from the Android-native/iOS-native SDKs, without verifying it also holds for KMP `BarcodeSelection`. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Intro](https://docs.scandit.com/sdks/kmp/barcode-selection/intro/) · [Get Started](https://docs.scandit.com/sdks/kmp/barcode-selection/get-started/) · `references/integration.md` |
| Compose Multiplatform | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
| Core concepts (context, camera, views) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
