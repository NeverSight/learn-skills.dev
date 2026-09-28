---
name: matrixscan-batch-cordova
description: Cordova MatrixScan Batch (scandit-cordova-datacapture-* plugins) — MatrixScan, BarcodeBatch, legacy BarcodeTracking — tracking and scanning multiple barcodes at once with basic/advanced AR overlays. Use for integration, settings and symbologies, per-barcode brushes, TrackedBarcodeView annotations, lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch Cordova Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch* API surface changes between major SDK versions — constructor signatures, overlay constructors, and listener shapes have all evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names.

Cordova-specific gotchas worth flagging:

- **Global namespace**: The Scandit SDK is exposed on `window.Scandit`. Use `Scandit.BarcodeBatch`, `Scandit.DataCaptureView`, etc. at runtime. The npm packages (`scandit-cordova-datacapture-*`) are plugin manifests, not ES modules. Do not emit `import { ... } from 'scandit-cordova-datacapture-*'` in user code running in the WebView. Only TypeScript projects using a bundler can import types at compile time.
- **`deviceready` gate**: All Scandit APIs must be called after `document.addEventListener('deviceready', ...)`. Never call at module load time.
- **`context.setMode(barcodeBatch)`**: This is the Cordova method to register the mode with the context. It replaces any previously active mode. Confirmed from both Cordova samples.
- **Modern constructors require SDK 7.6+**: `new Scandit.BarcodeBatch(settings)`, `new Scandit.BarcodeBatchBasicOverlay(mode, style)`, `new Scandit.BarcodeBatchAdvancedOverlay(mode)`, and `Scandit.BarcodeBatch.createRecommendedCameraSettings()` are all available from cordova=7.6.
- **AdvancedOverlay uses serialized views**: On Cordova, `setViewForTrackedBarcode` accepts `view: Promise<TrackedBarcodeView?>` — a serialized `TrackedBarcodeView`, NOT a native UI instance. Use `Scandit.TrackedBarcodeView.withHTMLElement(domElement, options)` to construct one. This is the same shape as Capacitor. See the Bubbles sample for the exact pattern.
- **MatrixScan AR add-on required**: `BarcodeBatchAdvancedOverlay`, `IBarcodeBatchBasicOverlayListener.brushForTrackedBarcode`, and `setBrushForTrackedBarcode` all require the MatrixScan AR add-on to be licensed.
- **Camera permissions** are configured automatically by the plugins on both iOS and Android.
- **`DataCaptureView.forContext(context)`** is the Cordova factory. Then call `view.connectToElement(htmlElement)` to attach it to the DOM.
- **TrackedObject (Cordova 8.2+)**: In SDK 8.2+, a `TrackedObject` base class was introduced that `TrackedBarcode` extends. No recipe is needed — the `TrackedBarcode` API you use day-to-day is unchanged.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch** (e.g. "add MatrixScan to my app", "set up BarcodeBatch", "track multiple barcodes simultaneously", "show AR overlays", "per-barcode brushes", "tap handling", "removed barcodes", "feedback / beep / vibration", "lifecycle or cleanup", "camera permissions") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan integration** (e.g. "upgrade from v6 to v7/v8", "migrate BarcodeTracking to BarcodeBatch", "is BarcodeTracking the same as BarcodeBatch?", "bump the Scandit plugins", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party multi-barcode scanner** (e.g. "replace phonegap-plugin-barcodescanner with MatrixScan Batch", "migrate from the Cordova ML Kit barcode plugin", "we loop a scanner to read all barcodes, switch us to Scandit") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index, extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

Cordova is a WebView-based framework. Examples in this skill use **plain JavaScript** (with optional JSDoc type hints). The same API works in TypeScript — add a `global.d.ts` declaration file and write TypeScript syntax. This skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Cordova get started | [Get Started](https://docs.scandit.com/sdks/cordova/matrixscan/get-started/) |
| Cordova AR overlays | [Adding AR Overlays](https://docs.scandit.com/sdks/cordova/matrixscan/advanced/) |
| Bubbles sample | [MatrixScanBubblesSample](https://github.com/Scandit/datacapture-cordova-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanBubblesSample) |
| Full API reference | [BarcodeBatch API](https://docs.scandit.com/data-capture-sdk/cordova/barcode-capture/api.html) |
