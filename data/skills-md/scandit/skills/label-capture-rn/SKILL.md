---
name: label-capture-rn
description: Smart Label Capture (Scandit `LabelCapture`) in React Native projects — extracting multiple fields (price, expiry date, serial or lot number, weight) from a label in one scan, using barcode fields plus text fields with regex patterns. Use for integration, label-definition configuration, captured-label handling, the Validation Flow, and SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# Label Capture React Native Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit Label Capture APIs. Label Capture has evolved across recent SDK releases, and the React Native plugin surface (imports, native linking, pod install, package names) has its own conventions distinct from the web SDK.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

React Native-specific gotchas worth flagging:
- **Listener method names are iOS-style on React Native.** The Validation Flow listener uses `didCaptureLabelWithFields(fields)` and `didSubmitManualInputForField(field, oldValue, newValue)` — NOT the web equivalents `onValidationFlowLabelCaptured` / `onManualInput`. If you see web-style listener names suggested, they are wrong on React Native.
- `DataCaptureContext.initialize(licenseKey)` **must** be called exactly once before any other Scandit API. It sets up `DataCaptureContext.sharedInstance`, which is the singleton everything else reads from. Do not construct multiple contexts. (The official `LabelCaptureSimpleSample` uses the legacy `DataCaptureContext.forLicenseKey(...)` form — both work, but new integrations should use `initialize` for consistency with the rest of the v8 RN docs.)
- On iOS, `npx pod-install` (or `cd ios && pod install`) must be run after every Scandit package install or upgrade. Android auto-links via Gradle.
- Metro's bundler cache frequently masks Scandit package upgrades. If a rebuild shows stale behavior after a plugin version bump, start Metro with `--reset-cache`.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/<App>/Info.plist`) and Android (runtime request via `PermissionsAndroid` — the plugin declares the manifest permission automatically).
- Field definitions on RN are **class-based**, not builder-based: `CustomBarcode.initWithNameAndSymbologies(name, [...])`, `new ExpiryDateText(name)`, `field.optional = true`, `LabelCaptureSettings.settingsFromLabelDefinitions([...], {})`. There is no `LabelCaptureSettingsBuilder` / `LabelDefinitionBuilder` and no v8.5 factory-function sugar — those are web-only.

## Product Guidance

Apply these rules whenever the user is making a design decision, not just an API question. They reflect how Scandit recommends Label Capture be integrated.

- **Default to the Validation Flow.** New integrations should use `LabelCaptureValidationFlowOverlay`, not `LabelCaptureBasicOverlay`. Recommend the basic/advanced overlay path only when the customer explicitly needs a live AR overlay or a UI that the Validation Flow's fixed layout cannot produce. See [references/validation-flow.md](references/validation-flow.md).
- **Validation Flow must be rendered full-screen.** Do not place it inside a card, half-sheet, modal slice, or partial-height widget — the layout assumes full-screen height for the field checklist, manual-entry sheet, and keyboard.
- **Prefer pre-made labels first, then pre-made fields, then custom.** Try in this order: (1) does a **pre-made label definition** cover the use case? — `LabelDefinition.createVinLabelDefinition(name)`, `LabelDefinition.createPriceCaptureDefinition(name)`, `LabelDefinition.createSevenSegmentDisplayLabelDefinition(name)`. (2) Can the label be built from **pre-made fields**? — `ExpiryDateText`, `PackingDateText`, `DateText`, `WeightText`, `UnitPriceText`, `TotalPriceText`, `SerialNumberBarcode`, `PartNumberBarcode`, `ImeiOneBarcode`, `ImeiTwoBarcode`. (3) Only as a last resort, fall back to `CustomText` / `CustomBarcode`.
- **Start from the sample app on greenfield integrations.** If the user is starting from scratch, recommend cloning `LabelCaptureSimpleSample` (link in the References table below) and adapting it, rather than wiring everything from zero.
- **Hand off to the `data-capture-sdk` skill for non-Label-Capture questions.** If the user asks about another Scandit product (Barcode Capture, SparkScan, MatrixScan, ID Capture, etc.) or about choosing between products, defer to the `data-capture-sdk` skill instead of guessing.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating Label Capture from scratch** (e.g. "add Label Capture to my app", "scan a price tag with barcode and expiry date", "how do I use Smart Label Capture") → read [references/integration.md](references/integration.md) and follow the instructions there. By default, integrate the Validation Flow (the integration guide leads with it).
- **Validation Flow questions** (e.g. "how do I customize the Validation Flow", "what can we change in the VF?", "why is it implemented this way", "how do I react to manual edits", "can I change the colors") → read [references/validation-flow.md](references/validation-flow.md).
- **Visual customization beyond the Validation Flow** (e.g. "I want a live AR overlay", "I want to draw a tag next to each captured field", "how do I get the camera frame during scanning") → read [references/customization.md](references/customization.md).
- **Adaptive Recognition Engine / cloud fallback / receipt scanning** ("how do I enable ARE", "use cloud recognition", "scan a receipt", "AdaptiveRecognitionMode", "is ARE available in production") → read [references/adaptive-recognition.md](references/adaptive-recognition.md).
- **Migrating or upgrading an existing Label Capture integration** (e.g. "upgrade my Label Capture to the latest SDK", "what changed between SDK versions for Label Capture") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## Framework variant policy

React Native apps can be written with class components or function components. Examples in this skill use **function components with hooks** because they match the official `LabelCaptureSimpleSample` and the current React Native convention. Even if the target project still contains legacy class components elsewhere, write new Label Capture code as function components — do not rewrite the rest of the app's component style, but keep the Label Capture integration itself on the current idiom (`useRef`, `useEffect`, `useMemo`, imperative `ref` callback for view-level properties).

Examples are in **TypeScript** (`.tsx`). If the target project is plain JavaScript (`.js` / `.jsx`), drop the type annotations and keep the same imports and structure.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| React Native integration | [Get Started](https://docs.scandit.com/sdks/react-native/label-capture/get-started/) · [Sample (LabelCaptureSimpleSample)](https://github.com/Scandit/datacapture-react-native-samples/tree/master/03_Advanced_Batch_Scanning_Samples/05_Smart_Label_Capture/LabelCaptureSimpleSample) |
| Label Definitions (fields, regex, presets) | [Label Definitions](https://docs.scandit.com/sdks/react-native/label-capture/label-definitions/) |
| Advanced topics (Validation Flow customization, adaptive recognition, custom overlays) | [Advanced Configurations](https://docs.scandit.com/sdks/react-native/label-capture/advanced/) |
| Full API reference | [Label Capture API](https://docs.scandit.com/data-capture-sdk/react-native/label-capture/api.html) |
