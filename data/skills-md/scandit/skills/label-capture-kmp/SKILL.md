---
name: label-capture-kmp
description: Smart Label Capture (Scandit `LabelCapture`) in Kotlin Multiplatform (KMP) / Compose Multiplatform projects (`com.kmp.datacapture.label.*`, shared commonMain consumed by Android and iOS) — extracting multiple fields (price, expiry date, serial or lot number, weight) from a label in one scan, using barcode fields, regex text fields, or the Kotlin DSL. Use for integration, label-definition configuration, captured-session handling, shared-view hosting, overlay customization, and the Validation Flow — in place of the single-platform Android or iOS skills.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# Label Capture KMP Skill

## Critical: Do Not Trust Internal Knowledge

Scandit's Kotlin Multiplatform (KMP) SDK is new: Label Capture first shipped on KMP at **SDK 8.6**. Your training data almost certainly has no KMP-specific knowledge of this API, and may confuse it with the single-platform Android or iOS Label Capture APIs, which use different types and package names. Do not port Android or iOS snippets by guessing at renamed symbols.

- The Kotlin package is **`com.kmp.datacapture.label.*`** (`com.kmp.datacapture.label.capture`, `.definition`, `.ui.overlay`, `.adaptive`) — not `com.scandit.datacapture.label.*` (that is the single-platform Android package).
- The Maven group is **`com.scandit.datacapture.kmp`** (artifacts `core`, `barcode`, `label`, `label-compose`, plus the model container add-ons `label-text` and `price-label`) — not `com.scandit.datacapture` (single-platform Android) and not a CocoaPod/SPM-only distribution (single-platform iOS).
- The mode is constructed with **`LabelCapture.forContext(dataCaptureContext, settings)`**, not `LabelCapture.forDataCaptureContext(...)` (Android) or a Swift initializer.
- Field definitions are built with the shared `LabelDefinitionBuilder` (via `LabelCaptureSettingsBuilder().label(name) { ... }` or the top-level `labelCaptureSettings { ... }` DSL) — regex setters are **`setValueRegex(es)` / `setAnchorRegex(es)`** from day one. There was never a legacy `setPattern`/`setDataTypePattern` era on KMP (that rename happened on Android at the 7.x→8.0 boundary, before KMP existed) — do not invent or "migrate" a KMP regex-rename story.
- The license key placeholder is **exactly** `-- ENTER YOUR SCANDIT LICENSE KEY HERE --`.
- iOS embedding uses `DataCaptureView(dataCaptureContext:)` + `.toUIView()`; Android embedding uses `DataCaptureView(context, dataCaptureContext)` + `.toAndroidView()`. Neither is a raw Android `View` or `UIView` constructor from the single-platform SDKs.

**Always verify APIs against `references/integration.md` before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or builder shapes from the single-platform Android/iOS Label Capture skills. If you cannot find an API in the provided reference, fetch the relevant documentation page before responding.

## Intent Routing

Based on the user's request, read `references/integration.md` and jump to the relevant section before responding:

- **Integrating Label Capture from scratch in a KMP shared module** (e.g. "add Label Capture to my Kotlin Multiplatform app", "scan a price tag with barcode and expiry date from commonMain", "wire up Label Capture for Android and iOS from one shared module") → read **Prerequisites** and **Minimal Integration**. Interactive: don't write code before you know the label's fields — ask what's on the label first (see the field catalogue in **Label definitions & fields**).
- **Defining label structure** (fields, regex, presets, pre-built whole-label factories) → read **Label definitions & fields**. Prefer a pre-built field/factory over a hand-written regex whenever one matches — the same rule as the single-platform skills.
- **Reading captured results** (`CapturedLabel`, `LabelField`, `onSessionUpdated`, `asDate()`) → read **Handling results**.
- **Customizing overlays** (field/label brushes on the Basic Overlay, floating AR views via the Advanced Overlay, the Validation Flow, or the beta Adaptive Recognition / Receipt Scanning overlay) → read **Overlays**.
- **Building the UI with Compose Multiplatform** (`LabelCaptureView` composable, `rememberLabelCapture`, `LabelOverlayStyle`) instead of the platform-specific `DataCaptureView` hosts → read **Compose Multiplatform**.
- **Lifecycle, teardown, or "camera keeps running in the background"** → read **Lifecycle & Teardown**.
- **Troubleshooting** (crash on launch, black preview, nothing captured, Compose recomposition churn) → read **Pitfalls**.

## API Usage Policy

Only use APIs that are explicitly documented in `references/integration.md` or the linked Scandit KMP references below. Do not invent or guess method signatures, parameters, or builder shapes — and do not assume a single-platform Android/iOS Label Capture API exists unchanged on KMP; the KMP surface is a distinct `expect`/`actual` layer with its own shape (e.g. no `ApplySettingsAsync`, no `RecommendedCameraSettings` property — only `createRecommendedCameraSettings()`). If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:

1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the **Full API reference** index below, extract the actual link from it, and follow that.

URL structures can vary and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Basic integration | [Intro](https://docs.scandit.com/sdks/kmp/label-capture/intro/) · [Get Started](https://docs.scandit.com/sdks/kmp/label-capture/get-started/) |
| Label Definitions (fields, regex, presets) | [Label Definitions](https://docs.scandit.com/sdks/kmp/label-capture/label-definitions/) |
| Overlays (Basic / Advanced / Validation Flow / Adaptive Recognition) | `references/integration.md` · [Advanced Configurations](https://docs.scandit.com/sdks/kmp/label-capture/advanced/) |
| Compose Multiplatform | `references/integration.md` · [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
| Core concepts (context, camera, views) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
