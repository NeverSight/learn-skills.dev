---
name: barcode-capture-ios
description: Scandit Barcode Capture (`BarcodeCapture`) in native iOS (Swift) projects — the low-level, full-control single-barcode scanning mode (BarcodeCapture + DataCaptureView + overlay), without the pre-built SparkScan UI. Use for integration, scan settings, result handling, overlay customization, SDK version migration (v6→v7→v8), replacing a third-party barcode scanner, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# BarcodeCapture iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes between major SDK versions — properties get renamed, removed, or restructured.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch, configuring settings, customizing feedback, adding a viewfinder, handling scans, or doing async work after a scan** (e.g. "add BarcodeCapture to my app", "set up barcode scanning", "how do I use BarcodeCapture in iOS", "filter duplicate scans", "suppress the beep", "add a viewfinder", "disable scanning while I look up the barcode") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit SDK to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Replacing a third-party barcode scanner with BarcodeCapture** (e.g. "replace my [scanner] with BarcodeCapture", "migrate from [framework] to BarcodeCapture", "switch from [library] barcode scanning to BarcodeCapture") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

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
| UIKit integration | [Get Started (UIKit)](https://docs.scandit.com/sdks/ios/barcode-capture/get-started/) · [Sample](https://github.com/Scandit/datacapture-ios-samples/tree/master/01_Single_Scanning_Samples/02_Barcode_Scanning_with_Low_Level_API/BarcodeCaptureSimpleSampleSwift) |
| SwiftUI integration | [Get Started (SwiftUI)](https://docs.scandit.com/sdks/ios/barcode-capture/get-started-with-swift-ui/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/ios/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/ios/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API](https://docs.scandit.com/data-capture-sdk/ios/barcode-capture/api.html) |
