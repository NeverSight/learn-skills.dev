---
name: label-capture-cordova
description: Smart Label Capture (Scandit `LabelCapture`) in Cordova / PhoneGap projects — extracting multiple fields (price, expiry date, serial or lot number, weight) from a label in one scan, using barcode fields plus text fields with regex patterns. Use for integration, label-definition configuration, captured-label handling, the Validation Flow, and SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# Label Capture Cordova Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit Label Capture APIs. The Cordova plugin surface (global `Scandit.*` namespace, `deviceready` gating, plugin install, platform prepare) is distinct from the web, React Native, Flutter, and Capacitor SDKs.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Cordova-specific gotchas worth flagging:
- **All Scandit code must run after `deviceready`.** The `Scandit.*` global namespace is not populated until then. Wrap your initialization in `document.addEventListener('deviceready', () => {...}, false);`.
- **Listener method names are iOS-style on Cordova.** The Validation Flow listener uses `didCaptureLabelWithFields(fields)` and `didSubmitManualInputForField(field, oldValue, newValue)` — NOT the web equivalents `onValidationFlowLabelCaptured` / `onManualInput`.
- **Class-based field API**, same shape as RN/Capacitor (and opposite to Flutter). Use `Scandit.CustomBarcode.initWithNameAndSymbologies(name, [...])`, `new Scandit.ExpiryDateText(name)`, `field.optional = false`, `Scandit.LabelCaptureSettings.settingsFromLabelDefinitions([...], {})`. There is no `LabelCaptureSettingsBuilder` / `LabelDefinitionBuilder` and no v8.5 factory-function sugar — those are web-only.
- After `cordova plugin add` / version bump, run `cordova prepare ios` (and `cordova prepare android`) to sync native dependencies. iOS additionally requires a fresh `pod install` inside `platforms/ios/`.
- Camera permission: iOS requires `NSCameraUsageDescription` in the app's `Info.plist` (or via `<config-file>` in `config.xml`); Android's `CAMERA` permission is declared by the plugin automatically and must be requested at runtime if your minSdkVersion targets API 23+.
- `Scandit.DataCaptureContext.initialize(licenseKey)` returns the singleton context; do not construct multiple contexts.

## Product Guidance

Apply these rules whenever the user is making a design decision, not just an API question. They reflect how Scandit recommends Label Capture be integrated.

- **Default to the Validation Flow.** New integrations should use `LabelCaptureValidationFlowOverlay`, not `LabelCaptureBasicOverlay`. Recommend the basic/advanced overlay path only when the customer explicitly needs a live AR overlay or a UI that the Validation Flow's fixed layout cannot produce. See [references/validation-flow.md](references/validation-flow.md).
- **Validation Flow must be rendered full-screen.** Do not place it inside a card, half-sheet, modal slice, or partial-height widget — the layout assumes full-screen height for the field checklist, manual-entry sheet, and keyboard.
- **Prefer pre-made labels first, then pre-made fields, then custom.** Try in this order: (1) does a **pre-made label definition** cover the use case? — `Scandit.LabelDefinition.createVinLabelDefinition(name)`, `Scandit.LabelDefinition.createPriceCaptureDefinition(name)`, `Scandit.LabelDefinition.createSevenSegmentDisplayLabelDefinition(name)`. (2) Can the label be built from **pre-made fields**? — `ExpiryDateText`, `PackingDateText`, `DateText`, `WeightText`, `UnitPriceText`, `TotalPriceText`, `SerialNumberBarcode`, `PartNumberBarcode`, `ImeiOneBarcode`, `ImeiTwoBarcode`. (3) Only as a last resort, fall back to `CustomText` / `CustomBarcode`.
- **Start from the sample app on greenfield integrations.** If the user is starting from scratch, recommend cloning `LabelCaptureSimpleSample` (link in the References table) and adapting it.
- **Hand off to the `data-capture-sdk` skill for non-Label-Capture questions.** If the user asks about another Scandit product (Barcode Capture, SparkScan, MatrixScan, ID Capture, etc.) or about choosing between products, defer to the `data-capture-sdk` skill instead of guessing.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating Label Capture from scratch** (e.g. "add Label Capture to my app", "scan a price tag with barcode and expiry date", "how do I use Smart Label Capture") → read [references/integration.md](references/integration.md). By default, integrate the Validation Flow (the integration guide leads with it).
- **Validation Flow questions** ("how do I customize it", "what can we change", "why is it implemented this way", "how do I react to manual edits", "can I change the colors") → read [references/validation-flow.md](references/validation-flow.md).
- **Visual customization beyond the Validation Flow** ("live AR overlay", "draw a tag next to each captured field", "get the camera frame during scanning") → read [references/customization.md](references/customization.md).
- **Adaptive Recognition Engine / cloud fallback / receipt scanning** ("how do I enable ARE", "use cloud recognition", "scan a receipt", "AdaptiveRecognitionMode", "is ARE available in production") → read [references/adaptive-recognition.md](references/adaptive-recognition.md).
- **Migrating or upgrading an existing Label Capture integration** → read [references/migration.md](references/migration.md).

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

Examples in this skill are written in **plain JavaScript (ES6+)** because that is the default for Cordova templates and the official `LabelCaptureSimpleSample`. If the target project uses TypeScript (some Cordova projects do), keep the same imports/structure and add type annotations as needed — do not change the global `Scandit.*` access pattern, do not switch to ES module imports, and do not assume bundler features.

## References

| Topic | Resource |
|---|---|
| Cordova integration | [Get Started](https://docs.scandit.com/sdks/cordova/label-capture/get-started/) · [Sample (LabelCaptureSimpleSample)](https://github.com/Scandit/datacapture-cordova-samples/tree/master/03_Advanced_Batch_Scanning_Samples/05_Smart_Label_Capture/LabelCaptureSimpleSample) |
| Label Definitions (fields, regex, presets) | [Label Definitions](https://docs.scandit.com/sdks/cordova/label-capture/label-definitions/) |
| Advanced topics (Validation Flow customization, adaptive recognition, custom overlays) | [Advanced Configurations](https://docs.scandit.com/sdks/cordova/label-capture/advanced/) |
| Full API reference | [Label Capture API](https://docs.scandit.com/data-capture-sdk/cordova/label-capture/api.html) |
