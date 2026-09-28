---
name: matrixscan-count-cordova
description: Cordova MatrixScan Count (BarcodeCount) — plugin scandit-cordova-datacapture-barcode. Counting and receiving workflows (scan-and-count, inventory count, scan against a capture list, status mode, tap-to-uncount) with BarcodeCountView in Cordova apps. For Capacitor use matrixscan-count-capacitor. Use for integration, symbology configuration, view customization, result handling, SDK version migration, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Count Cordova Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCount Cordova API has evolved significantly across SDK versions. Key milestones:

- **Cordova 6.24**: BarcodeCount first available on Cordova.
- **Cordova 7.6**: Context-free constructor `new Scandit.BarcodeCount(settings)` introduced; `context.addMode(barcodeCount)` is now the wiring call.
- **Cordova 7.1**: `BarcodeCountNotInListActionSettings` available.
- **Cordova 8.3**: `BarcodeCountStatusProvider`, `shouldShowStatusModeButton`, `textForBarcodesNotInListDetectedHint`, `textForClusteringGestureHint`, `textForScreenCleanedUpHint`, `disableModeWhenCaptureListCompleted`, `ClusteringMode` available.
- **Filtering / unique / additional barcodes / reset**: `BarcodeCountSettings.filterSettings` (`BarcodeFilterSettings` — `excludedSymbologies`, `excludedCodesRegex`), `expectsOnlyUniqueBarcodes`, `setAdditionalBarcodes` / `clearAdditionalBarcodes`, and `reset()` are available on Cordova.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

> **Source note**: There is no public Cordova MatrixScan Count sample. The integration reference is anchored to the internal DebugApp (`frameworks/cordova/debugapp/src/pages/BarcodeCount.tsx` and `frameworks/cordova/debugapp/src/hooks/modes/useBarcodeCount.ts`) and the Cordova plugin source (`frameworks/cordova/scandit-cordova-datacapture-barcode/www/ts/src/BarcodeCountView.ts`).

## Cordova-Specific Gotchas

- **Global namespace**: The Scandit SDK is exposed on `window.Scandit`. Use `Scandit.BarcodeCount`, `Scandit.BarcodeCountView`, etc. at runtime. The npm packages (`scandit-cordova-datacapture-*`) are plugin manifests, not ES modules. Do not emit `import { ... } from 'scandit-cordova-datacapture-*'` in user code running in the WebView. Only TypeScript projects using Webpack/bundler can import types at compile time.
- **`deviceready` gate**: All Scandit APIs must be called after `document.addEventListener('deviceready', ...)`. Never call at module load time.
- **Plugin install**: Both plugins are required:
  ```bash
  cordova plugin add scandit-cordova-datacapture-core
  cordova plugin add scandit-cordova-datacapture-barcode
  ```
  After any plugin change, run `cordova prepare`.
- **Web platform NOT supported**: BarcodeCount on Cordova requires iOS or Android. The web platform is not supported.
- **`BarcodeCountView` uses a DOM-overlay model**: The native view is sized and positioned to mirror an HTML element. The attach API (verified against plugin source) is:
  - `barcodeCountView.connectToElement(htmlElement)` — synchronous, no `await` needed (internally async, but the public signature is `void`).
  - `barcodeCountView.detachFromElement()` — synchronous `void`. Call during teardown.
  - `barcodeCountView.setFrame(rect, isUnderContent)` — manually position using a `Rect`. Returns `Promise<void>`. Use only when NOT using `connectToElement`.
  - `barcodeCountView.show()` / `barcodeCountView.hide()` — returns `Promise<void>`. Only use with `setFrame`; throws if called with an element attached.
- **Constructor pattern (≥7.6)**: `new Scandit.BarcodeCount(settings)` followed by `context.addMode(barcodeCount)`. The older `BarcodeCount.forDataCaptureContext(context, settings)` wired context automatically; the new constructor does not.
- **Camera**: Use `Scandit.BarcodeCount.createRecommendedCameraSettings()` (≥7.6 Cordova). Obtain the camera with `Scandit.Camera.withSettings(cameraSettings)`, set it via `context.setFrameSource(camera)`, and toggle with `camera.switchToDesiredState(Scandit.FrameSourceState.On/Off)`.
- **License placeholder**: Always use the exact string `'-- ENTER YOUR SCANDIT LICENSE KEY HERE --'`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Count from scratch** (e.g. "add MatrixScan Count to my app", "set up BarcodeCount in Cordova", "how do I scan a list of items", "how do I show the count view", "how do I customize the toolbar or hints", "how do I use tap-to-uncount", "how do I enable status mode") → read [references/integration.md](references/integration.md) and follow the instructions there.

- **Migrating from an older BarcodeCount constructor pattern** (e.g. "migrate from BarcodeCount.forDataCaptureContext", "update to the new constructor", "adopt status mode", "add not-in-list action settings to existing code") → read [references/migration.md](references/migration.md) and follow the migration guide there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index, extract the actual link from it, and follow that.

## Framework Variant Policy

Cordova is a WebView-based framework. Examples in this skill use **plain JavaScript** (with optional JSDoc type hints). The same API works in TypeScript — add a `global.d.ts` declaration file and write TypeScript syntax. This skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Cordova integration | [Get Started](https://docs.scandit.com/sdks/cordova/matrixscan-count/get-started/) |
| Full API reference | [BarcodeCount API](https://docs.scandit.com/data-capture-sdk/cordova/barcode-capture/api.html) |
