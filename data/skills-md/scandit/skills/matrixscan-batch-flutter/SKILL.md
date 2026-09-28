---
name: matrixscan-batch-flutter
description: MatrixScan Batch (MatrixScan, BarcodeBatch, legacy BarcodeTracking) in Flutter projects (scandit_flutter_datacapture_barcode_batch) — tracking and scanning multiple barcodes at once. Use for integration, settings and symbologies, tracked-barcode handling, per-barcode brushes, advanced-overlay AR widgets, lifecycle, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch Flutter Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch* API surface changes between major SDK versions — constructor signatures, overlay constructors, listener shapes, and Flutter-specific class names have all evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names.

Flutter-specific gotchas worth flagging:

- `await ScanditFlutterDataCaptureBarcode.initialize()` **must** be called (and awaited) in `main()` after `WidgetsFlutterBinding.ensureInitialized()` and before `runApp(...)`. The Bubbles sample also calls `await DataCaptureContext.initialize(licenseKey)` in `main()` and then uses `DataCaptureContext.sharedInstance`; the Simple sample passes the context to the screen. Both patterns are valid — pick the one that matches the project structure.
- `BarcodeBatch(settings)` is the context-free constructor (Flutter ≥7.6). After constructing, call `dataCaptureContext.setMode(barcodeBatch)` explicitly. On older SDKs use the factory constructor that accepts the context.
- `BarcodeBatch.createRecommendedCameraSettings()` is available from Flutter ≥7.6.
- **Advanced overlay method names on Flutter differ from other platforms**:
  - Set a widget: `setWidgetForTrackedBarcode(BarcodeBatchAdvancedOverlayWidget? widget, TrackedBarcode trackedBarcode)` (NOT `setViewForTrackedBarcode`)
  - Clear all widgets: `clearTrackedBarcodeWidgets()` (NOT `clearTrackedBarcodeViews`)
- **Custom AR annotation = subclass of `BarcodeBatchAdvancedOverlayWidget`** (Flutter-only base class). The widget state must extend `BarcodeBatchAdvancedOverlayWidgetState<T>` and override `build()` returning a `BarcodeBatchAdvancedOverlayContainer`.
- **Using `BarcodeBatchAdvancedOverlay` requires the MatrixScan AR add-on.** Using `brushForTrackedBarcode` and `setBrushForTrackedBarcode` on `BarcodeBatchBasicOverlay` also requires the MatrixScan AR add-on.
- `BarcodeBatchAdvancedOverlay` exposes a `view` getter on Flutter (Flutter-only; not available on other platforms).
- `offsetForTrackedBarcode` is a member of `BarcodeBatchAdvancedOverlayListener` on Flutter (per the RST, `@dart@` annotation). It is present on Flutter; no extra interface needed.
- **`TrackedObject` (Flutter ≥7.3+)**: A `TrackedObject` base class was introduced in SDK 7.3 that `TrackedBarcode` extends. No recipe is required for this — the day-to-day `TrackedBarcode` API is unchanged.
- The import barrel for BarcodeBatch classes is `scandit_flutter_datacapture_barcode_batch` — a separate barrel from `scandit_flutter_datacapture_barcode`. Always import both.
- `Symbology` enum values use **lowerCamelCase** in Dart: `Symbology.code128`, `Symbology.ean13Upca`, `Symbology.code39`. Do not write `Symbology.Code128` or `Symbology.EAN13UPCA`.
- `session.trackedBarcodes` is a `Map<int, TrackedBarcode>` in Dart (keyed by integer identifier, not string).
- `session.removedTrackedBarcodes` is a `List<int>` in Dart (integer identifiers).
- Lifecycle cleanup: call `_barcodeBatch.removeListener(this)`, set `_barcodeBatch.isEnabled = false`, switch camera off, and call `dataCaptureContext.removeAllModes()` (or `removeCurrentMode()` if using the singleton pattern).
- License placeholder must be exactly: `'-- ENTER YOUR SCANDIT LICENSE KEY HERE --'`

## Intent Routing

Based on the user's request, load the reference file before responding:

- **Integrating MatrixScan Batch from scratch** (e.g. "add MatrixScan to my Flutter app", "set up BarcodeBatch", "track multiple barcodes simultaneously", "show AR overlays", "per-barcode brushes", "scan feedback / beep / vibrate", "lifecycle or cleanup", "camera permissions") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Upgrading an existing MatrixScan integration across SDK versions** (e.g. "migrate from v6 to v7", "upgrade to SDK 8", "my code uses BarcodeTracking", "rename BarcodeTracking to BarcodeBatch") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party scanner with MatrixScan Batch** (e.g. "migrate from mobile_scanner", "we use ML Kit / google_mlkit_barcode_scanning and want to track multiple barcodes", "replace our existing barcode plugin with Scandit MatrixScan") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if an analyzer or runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index and extract the actual link from it.

## Framework variant policy

Flutter apps use many state-management patterns (StatefulWidget, BLoC, Provider, Riverpod). Examples in this skill use **StatefulWidget with `WidgetsBindingObserver`** because it matches both official samples (`MatrixScanSimpleSample`, `MatrixScanBubblesSample`) and keeps the scan pipeline straightforward. If the target project uses a different pattern, keep the BarcodeBatch wiring conceptually the same — one owner holds `DataCaptureContext`, `BarcodeBatch`, the camera, and the overlays — and port the snippets into the project's existing convention.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Flutter get started | [Get Started](https://docs.scandit.com/sdks/flutter/matrixscan/get-started/) |
| Flutter AR overlays | [Adding AR Overlays](https://docs.scandit.com/sdks/flutter/matrixscan/advanced/) |
| Full API reference | [BarcodeBatch API](https://docs.scandit.com/data-capture-sdk/flutter/barcode-capture/api.html) |
