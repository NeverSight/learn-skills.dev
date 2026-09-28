---
name: matrixscan-ar-ios
description: MatrixScan AR scanning pipeline in iOS projects (Swift, UIKit/SwiftUI) — BarcodeAr mode and settings, BarcodeArView, listener, feedback, camera and controls, plus migration from MatrixScan Batch (BarcodeBatch/BarcodeTracking). Use for integration, configuration, or troubleshooting — highlight and annotation work routes to the sibling skills matrixscan-ar-highlight-ios and matrixscan-ar-annotation-ios.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan AR iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The MatrixScan AR API changes between SDK versions — classes get renamed, restructured, or replaced (e.g. `BarcodeTracking` → `BarcodeBatch` → `BarcodeAr`).

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or view modifiers. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

## Scope

This skill is scoped to the **MatrixScan AR scanning pipeline**: `DataCaptureContext`, `BarcodeAr` mode, `BarcodeArSettings`, `BarcodeArView`, `BarcodeArViewSettings`, `BarcodeArListener`, `BarcodeArFeedback`, camera and control visibility.

Out of scope:
- **Highlights** (customizing the shapes drawn over detected barcodes — `BarcodeArHighlightProvider`, `BarcodeArRectangleHighlight`, `BarcodeArCircleHighlight`, etc.) — handled by the `matrixscan-ar-highlight-ios` skill.
- **Annotations** (info cards, status icons, popovers, responsive annotations — `BarcodeArAnnotationProvider`, `BarcodeArInfoAnnotation`, `BarcodeArPopoverAnnotation`, etc.) — handled by the `matrixscan-ar-annotation-ios` skill.

If a user question spans integration **and** highlight/annotation customization, cover the integration part here and tell the user which sibling skill handles the rest.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Setting up or adjusting the MatrixScan AR scanning pipeline** (e.g. "add MatrixScan AR to my app", "set up the AR scanner", "enable these symbologies", "configure feedback / torch / camera / controls", "change the camera settings", "show the zoom control") → read [references/integration.md](references/integration.md) and follow the instructions there. If the project already has MatrixScan AR wired up, do not re-create the context, mode, view, or lifecycle — locate the existing ones (grep for `BarcodeArView`, then `BarcodeAr`) and change only what the user asked for. Before writing code, determine whether the project uses UIKit or SwiftUI (check for `import SwiftUI`, an `@main` `App` struct, `SceneDelegate`/`AppDelegate`, `.storyboard`/`.xib` files, etc.) and use the matching Get Started page from the References table below.
- **Migrating from MatrixScan Batch to MatrixScan AR** (e.g. "migrate from BarcodeBatch / BarcodeTracking to MatrixScan AR", "replace MatrixScan Batch with MatrixScan AR", "switch from overlay-based scanning to AR") → read [references/migration.md](references/migration.md) and follow the instructions there.

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
| UIKit integration | [Get Started (UIKit)](https://docs.scandit.com/sdks/ios/matrixscan-ar/get-started/) · [Sample](https://github.com/Scandit/datacapture-ios-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanARSimpleSample) |
| SwiftUI integration | [Get Started (SwiftUI)](https://docs.scandit.com/sdks/ios/matrixscan-ar/get-started-with-swift-ui/) |
| Full API reference | [MatrixScan AR API](https://docs.scandit.com/data-capture-sdk/ios/barcode-capture/api.html) |
