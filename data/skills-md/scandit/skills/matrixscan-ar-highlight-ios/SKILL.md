---
name: matrixscan-ar-highlight-ios
description: MatrixScan AR highlights in iOS projects (Swift, UIKit/SwiftUI) — the shapes drawn over tracked barcodes. Use for adding highlights, customizing or modifying existing ones, or handling highlight tap interaction — pipeline setup belongs to matrixscan-ar-ios.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.1"
---

# MatrixScan AR highlight iOS Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The MatrixScan AR API changes significantly between major SDK versions — properties get renamed, removed, or restructured.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or view modifiers. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding. A single question may span multiple intents (e.g. "add tappable highlights to my app" is both integration and user-interaction) — in that case load every matching reference.

- **Integrating MatrixScan AR highlights** (e.g. "add MatrixScan AR highlights to my app", "set up MatrixScan AR highlights", "Which MatrixScan AR highlight types are available?", "how do I use MatrixScan AR highlights") → read [references/integration.md](references/integration.md) and follow the instructions there. Before writing any integration code, determine whether the project uses UIKit or SwiftUI (check for `import SwiftUI`, an `@main` `App` struct, `SceneDelegate`/`AppDelegate`, `.storyboard`/`.xib` files, etc.) and load the matching Get Started page from the References table below.
- **Handling user interaction with MatrixScan AR highlights** (e.g. "how do I handle user interaction in MatrixScan AR highlights?", "when the user presses a MatrixScan AR highlight do ...") → read [references/user-interaction.md](references/user-interaction.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or view modifiers. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Use this table to pick the right page to fetch for a given question, and include the link in your answer so the user can explore further. Do not tell the user to go read the docs themselves.

| Topic | Resource |
|---|---|
| UIKit integration | [Get Started (UIKit)](https://docs.scandit.com/sdks/ios/matrixscan-ar/get-started/) · [Sample](https://github.com/Scandit/datacapture-ios-samples/tree/master/03_Advanced_Batch_Scanning_Samples/01_Batch_Scanning_and_AR_Info_Lookup/MatrixScanARSimpleSample) |
| SwiftUI integration | [Get Started (SwiftUI)](https://docs.scandit.com/sdks/ios/matrixscan-ar/get-started-with-swift-ui/) |
| Full API reference | [MatrixScan AR API](https://docs.scandit.com/data-capture-sdk/ios/barcode-capture/api.html) |
