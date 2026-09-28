---
name: matrixscan-pick-ios
description: MatrixScan Pick (BarcodePick) in native iOS projects (Swift, ScanditBarcodeCapture) — pick/put verification workflows where the app confirms each item picked, with BarcodePickView, product provider, highlight styles, and auto-pick or tap-to-pick behavior. Use for integration, settings configuration, highlight styling, feedback, finish-button handling, or troubleshooting pick workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "0.1.1"
---

# MatrixScan Pick iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The MatrixScan Pick API has evolved across SDK versions — classes, properties, and view modifiers may have been renamed or restructured.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or view modifiers. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

## Scope

This skill is scoped to the **MatrixScan Pick picking workflow**: `DataCaptureContext`, `BarcodePick` mode, `BarcodePickSettings`, `BarcodePickView`, `BarcodePickViewSettings`, the product provider (`BarcodePickAsyncMapperProductProvider`), state-aware highlights (CustomView and built-in styles), the finish button, sound/haptic feedback, camera and control visibility.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Setting up or adjusting the MatrixScan Pick picking flow** (e.g. "add MatrixScan Pick to my app", "set up the product list", "show / hide the finish button", "mute the beep", "track what's been picked") → read [references/integration.md](references/integration.md) and follow the instructions there. If the project already has MatrixScan Pick wired up, do not re-create the context, mode, view, or lifecycle — locate the existing ones (grep for `BarcodePickView`, then `BarcodePick`) and change only what the user asked for. Before writing code, determine whether the project uses UIKit or SwiftUI (check for `import SwiftUI`, an `@main` `App` struct, `SceneDelegate`/`AppDelegate`, `.storyboard`/`.xib` files, etc.) and use the matching Get Started page from the References table below.
- **Customizing the highlights drawn over barcodes** (e.g. "change the highlight color per state", "use a rectangle instead of a dot", "show an icon / status badge on picked items", "draw a custom view over each barcode", "style the to-pick vs picked highlight") → read [references/highlights.md](references/highlights.md). This assumes the basic integration is already in place; it covers the five highlight styles and the per-state brush / icon / status-icon / custom-view APIs.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or view modifiers. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Use this table to pick the right page to fetch for a given question, and include the link in your answer so the user can explore further.

| Topic | Resource |
|---|---|
| UIKit integration | [Get Started (UIKit)](https://docs.scandit.com/sdks/ios/matrixscan-pick/get-started/) · [Sample](https://github.com/Scandit/datacapture-ios-samples/tree/master/03_Advanced_Batch_Scanning_Samples/04_Picking/RestockingSample) |
| SwiftUI integration | [Get Started (SwiftUI)](https://docs.scandit.com/sdks/ios/matrixscan-pick/get-started-with-swift-ui/) |
| Full API reference | [MatrixScan Pick API](https://docs.scandit.com/data-capture-sdk/ios/barcode-capture/api.html) |
