---
name: matrixscan-batch-capacitor
description: Capacitor MatrixScan Batch (scandit-capacitor-datacapture-barcode) — MatrixScan, BarcodeBatch, legacy BarcodeTracking — tracking and scanning multiple barcodes at once with basic/advanced AR overlays in Capacitor iOS/Android apps (not the plain-web sibling). Use for integration, settings and symbologies, per-barcode brushes, TrackedBarcodeView annotations, lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch Capacitor Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch* API surface changes between major SDK versions — constructor signatures, overlay constructors, and listener shapes have all evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names.

Capacitor-specific gotchas worth flagging:

- `ScanditCaptureCorePlugin.initializePlugins()` **must** be called (and awaited) before any other Scandit API — including `DataCaptureContext.initialize`. Forgetting this produces runtime errors that look unrelated to initialization.
- `npx cap sync` must be run after every plugin version change to propagate native artifacts into iOS/Android. Skipping it yields a web/native version mismatch at runtime.
- `context.setMode(barcodeBatch)` is how the mode is registered in the context on Capacitor (confirmed from both samples). This replaces any previously active mode.
- `DataCaptureView.forContext(context)` is the Capacitor factory for the capture view. Then call `view.connectToElement(htmlElement)` to attach it to the DOM.
- **Modern constructors require SDK 7.6+**: `new BarcodeBatch(settings)`, `new BarcodeBatchBasicOverlay(mode, style)`, `new BarcodeBatchAdvancedOverlay(mode)`, and `BarcodeBatch.createRecommendedCameraSettings()` are all available from capacitor=7.6.
- **AdvancedOverlay uses serialized views**: On Capacitor, `setViewForTrackedBarcode` accepts `view: Promise<TrackedBarcodeView?>` — a serialized `TrackedBarcodeView`, NOT a native UI instance. Use `TrackedBarcodeView.withHTMLElement(domElement, options)` from `scandit-capacitor-datacapture-barcode`. Wrap it in a Promise or pass directly — the sample passes the instance directly (the API internally wraps it).
- **MatrixScan AR add-on required**: `BarcodeBatchAdvancedOverlay`, `IBarcodeBatchBasicOverlayListener.brushForTrackedBarcode`, and `setBrushForTrackedBarcode` all require the MatrixScan AR add-on license.
- Camera permission: iOS requires `NSCameraUsageDescription` in `Info.plist`. Android is handled automatically by the plugin.
- **TrackedObject (Capacitor 8.2+)**: In SDK 8.2+, a `TrackedObject` base class was introduced that `TrackedBarcode` extends. No recipe is needed for this — the `TrackedBarcode` API you use day-to-day is unchanged.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch** (e.g. "add MatrixScan to my app", "set up BarcodeBatch", "track multiple barcodes simultaneously", "show AR overlays", "per-barcode brushes", "tap handling", "overlay style (frame/dot)", "feedback / beep / vibration on scan", "lifecycle or cleanup", "camera permissions") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Upgrading the Scandit SDK version** (e.g. "migrate from v6/v7 to v8", "BarcodeTracking is gone", "rename BarcodeTracking to BarcodeBatch", "DataCaptureContext.forLicenseKey not found") **or replacing a third-party scanner** (e.g. "switch from @capacitor-mlkit/barcode-scanning / ML Kit to MatrixScan Batch") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index, extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

Capacitor is a WebView-based framework. Examples in this skill use **plain JavaScript (ES modules)**. TypeScript projects can use the same imports and APIs verbatim — just add types — but this skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript syntax; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Capacitor get started | [Get Started](https://docs.scandit.com/sdks/capacitor/matrixscan/get-started/) |
| Capacitor AR overlays | [Adding AR Overlays](https://docs.scandit.com/sdks/capacitor/matrixscan/advanced/) |
| Bubbles sample | [MatrixScanBubblesSample](https://github.com/Scandit/datacapture-capacitor-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanBubblesSample) |
| Full API reference | [BarcodeBatch API](https://docs.scandit.com/data-capture-sdk/capacitor/barcode-capture/api.html) |
