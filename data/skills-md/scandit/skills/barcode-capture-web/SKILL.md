---
name: barcode-capture-web
description: Scandit Barcode Capture (`BarcodeCapture`) in web/browser (TypeScript/JavaScript) projects — the low-level, full-control single-barcode scanning mode (BarcodeCapture + DataCaptureView + overlay), without the pre-built SparkScan UI; not the Cordova or Capacitor hybrid plugins. Use for integration, scan settings, result handling, overlay and viewfinder customization, Scandit Web SDK version migration (v6→v7→v8), or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# BarcodeCapture Web Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture Web API changes significantly between major SDK versions — methods get renamed, async patterns change, and the context initialization was redesigned in v8.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, async patterns, or import paths. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Web-specific gotchas worth flagging:
- `DataCaptureContext.forLicenseKey()` must be `await`ed — it is async and sets `DataCaptureContext.sharedInstance`. Do not capture its return value; use `DataCaptureContext.sharedInstance` throughout.
- `BarcodeCapture.forContext(context, settings)` is async — always `await` it.
- `DataCaptureView.forContext(context)` is async — always `await` it.
- `BarcodeCaptureOverlay.withBarcodeCaptureForView(barcodeCapture, view)` is async — always `await` it.
- `barcodeCapture.setEnabled(false/true)` is async — `await` it before doing work in `didScan` to prevent duplicate scans.
- The listener callback is `didScan` — **not** `onBarcodeScanned` (that is the Android name).
- `codeDuplicateFilter` is a **number in milliseconds** on web (e.g. `500`) — not a `TimeInterval` object like Android.
- `BarcodeCapture.recommendedCameraSettings` is a **static property**, not a method call.
- The DOM element passed to `view.connectToElement()` must have defined dimensions and positioning — a zero-sized or unpositioned element will not render the camera preview.
- Camera is managed manually: call `context.frameSource.switchToDesiredState(FrameSourceState.On)` to start and `FrameSourceState.Off` to stop. The camera does not stop automatically.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch, configuring settings, customizing feedback or overlay, adding a viewfinder, handling scans, or doing async work after a scan** (e.g. "add BarcodeCapture to my app", "set up barcode scanning", "how do I use BarcodeCapture in web", "filter duplicate scans", "suppress the beep", "add a viewfinder", "disable scanning while I look up the barcode") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Get Started](https://docs.scandit.com/sdks/web/barcode-capture/get-started/) · [Sample](https://github.com/Scandit/datacapture-web-samples/tree/master/01_Single_Scanning_Samples/02_Barcode_Scanning_with_Low_Level_API/BarcodeCaptureSimpleSample) |
| Advanced topics (viewfinders, location selection, feedback, duplicate filtering, composite codes) | [Advanced Configurations](https://docs.scandit.com/sdks/web/barcode-capture/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/web/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/web/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API](https://docs.scandit.com/data-capture-sdk/web/barcode-capture/api.html) |
