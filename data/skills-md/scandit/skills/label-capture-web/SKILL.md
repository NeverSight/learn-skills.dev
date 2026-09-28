---
name: label-capture-web
description: Smart Label Capture (Scandit `LabelCapture`) in web/browser (TypeScript/JavaScript) projects — extracting multiple fields (price, expiry date, serial or lot number, weight) from a label in one scan, using barcode fields plus text fields with regex patterns. Use for integration, label-definition configuration, captured-session handling, overlay UI, the Validation Flow, and SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# Label Capture Web Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit Label Capture APIs. Label Capture has evolved across recent SDK releases:

- At the v7→v8 major bump (v7.6 → v8.0), `LabelFieldDefinition` regex properties were renamed (`pattern`→`valueRegex`, `patterns`→`valueRegexes`, `dataTypePattern`→`anchorRegex`, `dataTypePatterns`→`anchorRegexes`).
- In v8.2, the Validation Flow UI was redesigned and three customisation properties were deprecated.
- In v8.5, additive ergonomic shorthands were introduced for the builders.

**ARE (Adaptive Recognition Engine)** is Scandit's cloud-based OCR fallback — enabled via `AdaptiveRecognitionMode.Auto` on label definitions. It is currently in Beta, works **only with the Validation Flow overlay**, and requires a license key with the ARE feature flag enabled. Trial keys can be issued for evaluation; production keys require contacting support@scandit.com. Do not enable it by default.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or builder shapes. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Questions about other Scandit products or scanning modes** (e.g. SparkScan, Barcode Capture, MatrixScan, ID Capture, or general SDK setup questions not specific to Label Capture) → hand off to the `data-capture-sdk` skill. Do not attempt to answer questions about other capture modes from memory — the dedicated skill has the correct and up-to-date references.

- **Integrating Label Capture from scratch** (e.g. "add Label Capture to my app", "scan a price tag with barcode and expiry date", "how do I use Smart Label Capture", "how do I enable the Validation Flow", "I want to build a label scanning app", "which overlay should I use", "what is ARE", "how do I improve OCR accuracy") → read [references/integration.md](references/integration.md) and follow the instructions there. If the user has no existing project, the guide will direct you to offer the pre-built sample first.
- **Migrating or upgrading an existing Label Capture integration** (e.g. "upgrade my Label Capture to the latest SDK", "migrate from v8.1 to v8.2", "what changed between SDK versions for Label Capture") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or view modifiers. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:

1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Basic integration | [Get Started](https://docs.scandit.com/sdks/web/label-capture/get-started/) · [Sample (LabelCaptureSimpleSample)](https://github.com/Scandit/datacapture-web-samples/tree/master/03_Advanced_Batch_Scanning_Samples/05_Smart_Label_Capture/LabelCaptureSimpleSample) |
| Label Definitions (fields, regex, presets) | [Label Definitions](https://docs.scandit.com/sdks/web/label-capture/label-definitions/) |
| Advanced topics (Validation Flow customization, adaptive recognition, custom overlays) | [Advanced Configurations](https://docs.scandit.com/sdks/web/label-capture/advanced/) |
| Full API reference | [Label Capture API](https://docs.scandit.com/data-capture-sdk/web/label-capture/api.html) |
