---
name: matrixscan-ar-web
description: MatrixScan AR (Barcode AR, BarcodeAr) in web/browser (TypeScript/JavaScript) projects (@scandit/web-datacapture-barcode) — scanning multiple barcodes at once with AR overlays, highlights, and annotations on tracked barcodes. Use for integration, symbology configuration, highlight and annotation providers, session handling, migration from BarcodeBatch, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan AR Web Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeAr* Web API is substantially different from the React Native API — the initialization pattern, view creation, and provider callback signature all differ.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or import paths. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Web-specific gotchas worth flagging:

- `DataCaptureContext.forLicenseKey()` sets `DataCaptureContext.sharedInstance` as a side effect — no need to save the return value. Access the context via `DataCaptureContext.sharedInstance` throughout the app.
- `BarcodeAr.forContext(DataCaptureContext.sharedInstance, settings)` is **async** — always `await` it. Do not use `new BarcodeAr(settings)` (that is the React Native ≥7.6 form).
- `BarcodeArView.create(element, context, barcodeAr)` is **async** — always `await` it. The `element` argument is the DOM container into which the view is inserted.
- `BarcodeArView` **is an HTML element** (extends `ScanditHTMLElement`) — it attaches itself to the provided container. Clean it up by calling `barcodeArView.remove()`, which removes it from the DOM.
- **Providers use a callback pattern on web**, not a return value. The signatures are `highlightForBarcode(barcode, callback)` and `annotationForBarcode(barcode, callback)`. Deliver the result via `callback(highlight)` / `callback(annotation)` — do NOT return it. This is different from React Native where providers are async functions returning a Promise.
- Must call `await barcodeArView.start()` **explicitly** — the view does not start automatically after `create()`.
- `ScanditIconBuilder.build()` returns `Promise<ScanditIcon>` — icon construction is **async** on web. Use `new ScanditIconBuilder().withIcon(ScanditIconType.Checkmark).build()` — there is no static `forType()` method, and `ScanditIconType.Info` does not exist. The full enum (31 values) is in [references/integration.md](references/integration.md).
- `BarcodeArResponsiveAnnotation.threshold` is a **static property** — set it BEFORE calling `BarcodeArResponsiveAnnotation.create(barcode, closeUp, far)`.
- **BarcodeArView manages the camera internally.** Do NOT manually set up `Camera`, `context.setFrameSource`, or `switchToDesiredState` — that pattern belongs to BarcodeBatch, not BarcodeAr.
- **No `DataCaptureView` is needed.** `BarcodeArView.create()` replaces `DataCaptureView` entirely for MatrixScan AR.
- The module loader is `barcodeCaptureLoader()` (from `@scandit/web-datacapture-barcode`) — there is no separate loader for BarcodeAr.
- **Custom highlight/annotation elements** must implement `BarcodeArHighlight` / `BarcodeArAnnotation` as Web Components extending `HTMLElement`. They must have `position: absolute`, `will-change: transform`, and implement `updatePosition(point, transformOrigin, rotationAngle)` which the SDK calls every frame. Add `[hidden] { display: none }` for SDK visibility management. Register once with `customElements.define` guarded by `if (!customElements.get(tag))`.
- `session.addedTrackedBarcodes` returns `Record<string, TrackedBarcode>` (a dictionary), **not** an array — use `Object.values(session.addedTrackedBarcodes)` to iterate. Same for `session.allTrackedBarcodes`.
- **Multithreading is mandatory.** Set `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` (self-hosted) or `credentialless` (CDN). Without these headers the SDK falls back to single-threaded mode, which is too slow for AR tracking.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan AR from scratch** (e.g. "add MatrixScan AR to my web app", "set up BarcodeAr", "show AR highlights on barcodes", "show info annotations", "how to use BarcodeArView on web", "lifecycle or cleanup") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating from BarcodeBatch / BarcodeTracking to BarcodeAr** (e.g. "migrate from BarcodeBatch to BarcodeAr", "convert MatrixScan Batch to MatrixScan AR", "replace BarcodeTracking with BarcodeAr") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Get Started](https://docs.scandit.com/sdks/web/matrixscan-ar/get-started/) · [Simple Sample](https://github.com/Scandit/datacapture-web-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanARSimpleSample) |
| Multithreading / COOP+COEP headers | [Improve Runtime Performance](https://docs.scandit.com/sdks/web/matrixscan-ar/get-started/#improve-runtime-performance-by-enabling-browser-multithreading) |
| Full API reference | [BarcodeAr API](https://docs.scandit.com/data-capture-sdk/web/barcode-capture/api.html) |
