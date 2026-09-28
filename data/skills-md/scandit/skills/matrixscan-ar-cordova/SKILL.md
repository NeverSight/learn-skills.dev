---
name: matrixscan-ar-cordova
description: Cordova MatrixScan AR (Barcode AR, BarcodeAr) via the scandit-cordova-datacapture-* plugins — scanning multiple barcodes at once with AR highlights and annotations (info annotations, popovers, status icons) on tracked barcodes. Use for integration, symbology configuration, highlight and annotation providers, BarcodeArView customization, migration from BarcodeBatch/BarcodeTracking, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan AR Cordova Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeAr API is new in Cordova plugin 8.2 — it did not exist in v6 or v7 for Cordova. There is no migration history to reference.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Cordova-specific gotchas worth flagging:

- The Scandit SDK is exposed on the global `window.Scandit` object. The npm package names (`scandit-cordova-datacapture-*`) are plugin manifests — they are **not** runtime ES modules. Do not emit `import { ... } from 'scandit-cordova-datacapture-*'` in user code that will run in the WebView; use `Scandit.X` (with an optional `global.d.ts` for typing) instead. Only Ionic/Angular/Webpack-bundled projects import from the packages directly.
- `document.addEventListener('deviceready', ...)` is the **only** safe gate for Scandit APIs. Do not run any Scandit call at module load time — it will fail because the Cordova bridge is not ready yet.
- `BarcodeArView` in Cordova uses a **DOM-overlay model**: the native AR view is sized and positioned to mirror a plain HTML `<div>` element. You must call `barcodeArView.connectToElement(element)` after construction to link the view to a DOM node, and `barcodeArView.detachFromElement()` when tearing down.
- `new Scandit.BarcodeAr(settings)` — this is the Cordova constructor (not `BarcodeAr.forContext`). Context is wired separately via `context.setFrameSource(camera)`.
- Camera is managed manually in BarcodeAr on Cordova: obtain it with `Scandit.Camera.withSettings(Scandit.BarcodeAr.createRecommendedCameraSettings())`, set it as the frame source, and call `camera.switchToDesiredState(Scandit.FrameSourceState.On/Off)` to start/stop.
- Highlight and annotation providers return `Promise<BarcodeArHighlight | null>` and `Promise<BarcodeArAnnotation | null>` respectively — make the methods `async` or return a Promise explicitly.
- After changing plugin versions, run `cordova prepare` (and reinstall the platform if needed) to propagate the new native artifacts.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan AR from scratch** (e.g. "add MatrixScan AR to my app", "set up AR barcode overlays", "how do I use BarcodeAr in Cordova", "how do I show info annotations", "how do I customize highlights") → read [references/integration.md](references/integration.md) and follow the instructions there.

- **Migrating from BarcodeBatch / BarcodeTracking to BarcodeAr** (e.g. "migrate my MatrixScan code", "update from BarcodeBatch to BarcodeAr", "I'm using BarcodeBatchBasicOverlay / BarcodeBatchAdvancedOverlay", "convert my old MatrixScan integration", "we have BarcodeTracking and need to upgrade") → read [references/migration.md](references/migration.md) and follow the 10-step migration guide there. Key Cordova-specific caveat: `BarcodeArCustomAnnotation` is **NOT available on Cordova** — freeform HTML overlays from `BarcodeBatchAdvancedOverlay` must be replaced with built-in annotation types (`BarcodeArInfoAnnotation`, `BarcodeArPopoverAnnotation`, `BarcodeArStatusIconAnnotation`, or `BarcodeArResponsiveAnnotation`).

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and plugin paths and guessing will lead to 404s.

## Framework variant policy

Cordova is a WebView-based framework. Examples in this skill use **plain JavaScript** (with optional JSDoc type hints as seen in the official MatrixScanARSimpleSample). The same API works in TypeScript — add a `global.d.ts` declaration file (described in [references/integration.md](references/integration.md)) and write TypeScript syntax. This skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Cordova integration | [Get Started](https://docs.scandit.com/sdks/cordova/matrixscan-ar/get-started/) · [Sample](https://github.com/Scandit/datacapture-cordova-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanARSimpleSample) |
| Full API reference | [BarcodeAr API](https://docs.scandit.com/data-capture-sdk/cordova/barcode-capture/api.html) |
