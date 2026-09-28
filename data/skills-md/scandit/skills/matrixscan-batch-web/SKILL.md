---
name: matrixscan-batch-web
description: MatrixScan Batch (MatrixScan, BarcodeBatch, legacy BarcodeTracking) in web/browser (TypeScript/JavaScript) projects (@scandit/web-datacapture-barcode) — tracking and scanning multiple barcodes at once. Use for integration, settings and symbologies, per-barcode brushes, HTML-element AR overlays, manual feedback, lifecycle, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch Web Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch Web API changes between major SDK versions — constructor signatures, overlay factory names, async patterns, and initialization have all evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or import paths. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Web-specific gotchas worth flagging:

- `BarcodeBatch.forContext(context, settings)` is **async** — always `await` it. Do not use `new BarcodeBatch(settings)` (that is the React Native ≥7.6 form).
- `barcodeBatch.setEnabled(true/false)` is **async** — always `await` it.
- `BarcodeBatchBasicOverlay.withBarcodeBatchForView(barcodeBatch, view)` and `BarcodeBatchBasicOverlay.withBarcodeBatchForViewWithStyle(barcodeBatch, view, style)` are **async** factory methods — always `await` them. There is no implicit overlay.
- `BarcodeBatchAdvancedOverlay.withBarcodeBatchForView(barcodeBatch, view)` is **async** — always `await` it.
- `setAnchorForTrackedBarcode` and `setOffsetForTrackedBarcode` on `BarcodeBatchAdvancedOverlay` are **synchronous** (return `void`) — do not `await` them.
- `clearTrackedBarcodeViews()` on `BarcodeBatchAdvancedOverlay` is also **synchronous** (returns `void`).
- `BarcodeBatch.recommendedCameraSettings` is a **static property**, not a method call.
- The module loader is `barcodeCaptureLoader()` (from `@scandit/web-datacapture-barcode`) — there is no separate `barcodeBatchLoader`. Both BarcodeCapture and BarcodeBatch use the same loader.
- **Multithreading is mandatory for BarcodeBatch.** Without `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` (self-hosted) or `credentialless` (CDN), the SDK falls back to single-threaded mode and batch tracking will be too slow to use.
- **AR views on web use plain HTML elements** — `TrackedBarcodeView.withHTMLElement(element, options)` returns a `Promise<TrackedBarcodeView>`. Pass that Promise directly to `setViewForTrackedBarcode` or return it from `viewForTrackedBarcode` — both accept a Promise. This is NOT a subclass pattern.
- `session.removedTrackedBarcodes` returns `string[]` (identifiers serialized as strings) — use `Number.parseInt(id, 10)` when comparing against `TrackedBarcode.identifier` (which is a `number`).
- The `DataCaptureView` can be created before context init: `new DataCaptureView()` → `connectToElement(element)` → `await view.setContext(context)`. This allows a progress bar to be shown during SDK loading. The alternative `await DataCaptureView.forContext(context)` is equally valid.
- The DOM element passed to `view.connectToElement()` must have defined dimensions and a set `position` (e.g. `fixed` or `absolute`) — zero-sized or unpositioned containers will not render the camera preview.
- Camera is managed manually: call `await context.frameSource?.switchToDesiredState(FrameSourceState.On)` to start and `FrameSourceState.Off` to stop. The camera does not stop automatically when the page loses focus.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch** (e.g. "add MatrixScan to my web app", "set up BarcodeBatch", "track multiple barcodes simultaneously", "show AR overlays on barcodes", "per-barcode brush colors", "lifecycle or cleanup") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing MatrixScan Batch integration** (e.g. "upgrade from v6 to v7", "migrate BarcodeTracking to BarcodeBatch", "bump the Scandit SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party multi-barcode scanner with MatrixScan Batch** (e.g. "replace my ZXing-js / @zxing/library continuous scanner with MatrixScan Batch", "migrate from BrowserMultiFormatReader multi-scan to BarcodeBatch", "switch from [web barcode library] continuous multi-result scanning to BarcodeBatch") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| Get Started | [Get Started](https://docs.scandit.com/sdks/web/matrixscan/get-started/) · [Simple Sample](https://github.com/Scandit/datacapture-web-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanSimpleSample) · [AR Bubbles Sample](https://github.com/Scandit/datacapture-web-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanBubblesSample) |
| Advanced topics (AR overlays, brush customization) | [Adding AR Overlays](https://docs.scandit.com/sdks/web/matrixscan/advanced/) |
| Multithreading / COOP+COEP headers | [Improve Runtime Performance](https://docs.scandit.com/sdks/web/matrixscan/get-started/#improve-runtime-performance-by-enabling-browser-multithreading) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/web/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/web/migrate-7-to-8/) |
| Full API reference | [BarcodeBatch API](https://docs.scandit.com/data-capture-sdk/web/barcode-capture/api.html) |
