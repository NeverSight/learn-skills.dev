---
name: barcode-capture-cordova
description: Cordova — Scandit Barcode Capture (`BarcodeCapture`) in Apache Cordova hybrid apps via the `scandit-cordova-datacapture-*` plugins (global `window.Scandit`), the low-level, full-control single-barcode scanning mode (BarcodeCapture + DataCaptureView + BarcodeCaptureOverlay) without the pre-built SparkScan UI, not the browser-only web SDK. Use for integration, scan settings, result handling, overlay wiring, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.3"
---

# BarcodeCapture Cordova Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes significantly between major SDK versions — capture-mode factories get replaced with constructors, listener signatures shift, and the Cordova plugin surface (global `Scandit` namespace, plugin install commands, `deviceready` timing) has also evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Cordova-specific gotchas worth flagging:
- The Scandit SDK is exposed on the global `window.Scandit` object. The npm package names (`scandit-cordova-datacapture-*`) are plugin manifests — they are **not** runtime ES modules. Do not emit `import { ... } from 'scandit-cordova-datacapture-*'` in user code that will run in the WebView; use `Scandit.X` (with an optional `global.d.ts` for typing) instead. Only Ionic/Angular/Webpack-bundled projects import from the packages directly.
- `document.addEventListener('deviceready', ...)` is the **only** safe gate for Scandit APIs. Do not run any Scandit call at module load time — it will fail because the Cordova bridge is not ready yet.
- After changing plugin versions, run `cordova prepare` (and reinstall the platform if needed) to propagate the new native artifacts. Skipping this yields a runtime version mismatch.
- `BarcodeCapture` requires a visible **DataCaptureView** to render the camera preview. Unlike SparkScan, there is no native overlay — the `DataCaptureView` is mounted into an HTML element via `view.connectToElement(...)`, and the `BarcodeCaptureOverlay` is added on top of that view to draw recognized barcodes. Forgetting either step is the most common reason "scanning works but I see nothing".
- Inside the `didScan` callback, disable the mode (`barcodeCapture.isEnabled = false`) before doing any UI work that takes more than a frame — the listener blocks frame processing while it runs, so long-running work there freezes the camera and may cause duplicate scans.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch** (e.g. "add BarcodeCapture to my app", "set up barcode scanning", "how do I use BarcodeCapture in Cordova", "how do I render the camera preview") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit plugins to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and plugin paths and guessing will lead to 404s.

## Framework variant policy

Cordova is a WebView-based framework. Examples in this skill use **plain JavaScript** (with optional JSDoc type hints as seen in the official BarcodeCaptureSimpleSample). The same API works in TypeScript — add a `global.d.ts` declaration file (described in [references/integration.md](references/integration.md)) and write TypeScript syntax. This skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Cordova integration | [Get Started](https://docs.scandit.com/sdks/cordova/barcode-capture/get-started/) · [Sample](https://github.com/Scandit/datacapture-cordova-samples) |
| Advanced topics (custom feedback, viewfinders, scan area, location selection, composite codes) | [Advanced Configurations](https://docs.scandit.com/sdks/cordova/barcode-capture/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/cordova/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/cordova/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API](https://docs.scandit.com/data-capture-sdk/cordova/barcode-capture/api.html) |
