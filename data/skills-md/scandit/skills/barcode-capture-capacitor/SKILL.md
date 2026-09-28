---
name: barcode-capture-capacitor
description: Capacitor — Scandit Barcode Capture (`BarcodeCapture`) in Capacitor (Ionic) hybrid apps via the Scandit Capacitor plugins (`ScanditCaptureCorePlugin`), the low-level, full-control single-barcode scanning mode (BarcodeCapture + DataCaptureView + BarcodeCaptureOverlay) without the pre-built SparkScan UI, not the browser-only web SDK. Use for integration, symbology settings, result handling, viewfinder and feedback customization, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.3"
---

# BarcodeCapture Capacitor Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes between major SDK versions — properties get renamed, removed, or restructured, and the Capacitor plugin surface (imports, plugin initialization, native sync steps) has also evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Capacitor-specific gotchas worth flagging:
- `ScanditCaptureCorePlugin.initializePlugins()` **must** be called (and awaited) before any other Scandit API — including `DataCaptureContext` construction. Forgetting this produces runtime errors that look unrelated to initialization.
- `npx cap sync` must be run after every plugin version change to propagate native artifacts into iOS/Android. Skipping it yields a web/native version mismatch at runtime.
- BarcodeCapture renders into a `DataCaptureView` that is connected to a DOM element via `view.connectToElement(...)`. The view itself is a native overlay, but the DOM container determines its size and position. A `BarcodeCaptureOverlay` must be created and added to the view to visualize recognized barcodes.
- The camera is a separate component: `Camera.default` (or `Camera.withSettings(BarcodeCapture.createRecommendedCameraSettings())`), set via `context.setFrameSource(camera)`, then started via `camera.switchToDesiredState(FrameSourceState.On)`.
- **Disable the mode while handling a scan**: the `didScan` callback blocks further frame processing on Capacitor. If you do any meaningful work (database lookup, navigation, network) inside `didScan`, set `barcodeCapture.isEnabled = false` first, perform the work, then re-enable. This is documented behavior on Capacitor specifically.
- BarcodeCapture only renders on **native platforms** (iOS, Android). If your app also targets the web build of Capacitor, guard initialization with `Capacitor.isNativePlatform()`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch** (e.g. "add BarcodeCapture to my app", "set up barcode scanning", "how do I use BarcodeCapture in Capacitor", "wire up the overlay", "handle the camera lifecycle") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit plugins to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and plugin paths (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## Framework variant policy

Capacitor is a WebView-based framework. Examples in this skill use **plain JavaScript (ES modules)**. TypeScript projects can use the same imports and APIs verbatim — just add types — but this skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript syntax; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Capacitor integration | [Get Started](https://docs.scandit.com/sdks/capacitor/barcode-capture/get-started/) · [Samples](https://github.com/Scandit/datacapture-capacitor-samples) |
| Advanced topics (custom feedback, viewfinders, location selection, scan intention) | [Advanced Configurations](https://docs.scandit.com/sdks/capacitor/barcode-capture/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/capacitor/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/capacitor/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API](https://docs.scandit.com/data-capture-sdk/capacitor/barcode-capture/api.html) |
