---
name: matrixscan-count-capacitor
description: Capacitor MatrixScan Count (BarcodeCount) — plugin scandit-capacitor-datacapture-barcode. Multi-barcode counting and receiving workflows (scan-and-count, inventory count, capture list, status mode) with BarcodeCountView on a DOM element in Capacitor apps, iOS/Android native only. For React Native use matrixscan-count-rn. Use for integration, symbology configuration, result handling, view customization, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Count Capacitor Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCount API has evolved significantly across versions — constructor signatures, view factory methods, and feature availability vary by SDK version. Properties, method names, and plugin patterns may differ from other platforms or from general knowledge.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Capacitor-specific gotchas worth flagging:

- `ScanditCaptureCorePlugin.initializePlugins()` **must** be called (and awaited) before any other Scandit API — including `DataCaptureContext` construction. Forgetting this produces runtime errors that look unrelated to initialization.
- `npx cap sync` must be run after every plugin version change to propagate native artifacts into iOS/Android. Skipping it yields a web/native version mismatch at runtime.
- **BarcodeCountView requires a DOM element.** `BarcodeCountView.connectToElement(htmlElement)` mirrors its size and position from a DOM element. Call `detachFromElement()` on cleanup.
- **BarcodeCount runs on iOS and Android only.** It does not run in the browser. Guard with `Capacitor.isNativePlatform()` if your app also targets web.
- **Minimum SDK versions:**
  - BarcodeCount on Capacitor: **6.18**
  - `new BarcodeCount(settings)` constructor (no context): **7.6**. Before 7.6, use `BarcodeCount.forDataCaptureContext(context, settings)`.
  - `BarcodeCountView` constructed with object literal `new BarcodeCountView({context, barcodeCount, style})`: verified in samples. The static factories `BarcodeCountView.forContextWithMode(context, barcodeCount)` and `BarcodeCountView.forContextWithModeAndStyle(context, barcodeCount, style)` are also documented.
  - Not-in-list action settings (`BarcodeNotInListActionSettings`): **7.1**
  - Status mode (`setStatusProvider`, `shouldShowStatusModeButton`, `shouldShowStatusIconsOnScan`): **8.3**
  - Mapping flow (`BarcodeCountMappingFlowSettings`, `BarcodeCountView.forMapping`): **8.3**
- Plugin packages: `@scandit/datacapture-barcode` and `@scandit/datacapture-core` (npm registry) **or** `scandit-capacitor-datacapture-barcode` and `scandit-capacitor-datacapture-core` depending on the package registry used. Check the user's existing `package.json` imports and match.
- Camera permission: iOS `NSCameraUsageDescription` in `Info.plist`. Android handled automatically by the plugin.
- `BarcodeCount.recommendedCameraSettings` (static getter) returns recommended camera settings. On Capacitor 7.6+, `BarcodeCount.createRecommendedCameraSettings()` (static method) is also available — the sample uses the getter form.
- `barcodeCount.isEnabled = true` must be set to start scanning after creating `BarcodeCountView`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Count from scratch** (e.g. "add MatrixScan Count to my app", "set up BarcodeCount", "how do I use BarcodeCountView in Capacitor", "how do I count barcodes", "scan against a list", "packing slip verification", "receiving workflow") → read [references/integration.md](references/integration.md) and follow the instructions there.

- **Migrating from an older BarcodeCount API or adding newer features** (e.g. "upgrade BarcodeCount constructor", "migrate from forDataCaptureContext", "add status mode", "add mapping flow", "add not-in-list actions") → read [references/migration.md](references/migration.md) and follow the migration steps there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Get Started page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

## Framework variant policy

Capacitor is a WebView-based framework. Examples in this skill use **plain JavaScript (ES modules)**. TypeScript projects can use the same imports and APIs verbatim — just add types — but this skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript syntax; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Capacitor integration | [Get Started](https://docs.scandit.com/sdks/capacitor/matrixscan-count/get-started/) · [Sample](https://github.com/Scandit/datacapture-capacitor-samples/tree/master/03_Advanced_Batch_Scanning_Samples/02_Counting_and_Receiving/MatrixScanCountSimpleSample) |
| Full API reference | [BarcodeCount API](https://docs.scandit.com/data-capture-sdk/capacitor/barcode-capture/api.html) |
