---
name: id-capture-capacitor
description: Scandit ID Capture (`IdCapture`) in Capacitor projects — scanning passports, driver's licenses, ID cards, residence permits, visas via MRZ, VIZ, barcode, or mobile documents. Use for integration, accepted-document and scanner configuration, captured-field result handling, anonymization, add-on capabilities (voided-ID detection, European driving-license back decoding, AAMVA barcode verification), and SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# ID Capture Capacitor Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit ID Capture APIs. The ID Capture API was **restructured at the v7 → v8 boundary** (the `scannerType` property was renamed to `scanner` and reshaped into a wrapper, the standalone `AamvaBarcodeVerifier` was removed in favour of settings flags, and several verification APIs were added). The Capacitor plugin surface (package names, the imperative `DataCaptureView` + `connectToElement` pattern, explicit `initializePlugins()` startup) is also distinct from the iOS, Android, web, Flutter, React Native, and Cordova SDKs.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, package names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Capacitor-specific gotchas worth flagging:

- **Explicit plugin initialization is required.** Capacitor does not auto-init — call `await ScanditCaptureCorePlugin.initializePlugins()` once at app startup, **before** creating the `DataCaptureContext` or anything else. Skipping it leaves the native bridge un-wired and produces opaque "plugin not implemented" errors.
- **The view is an imperative class connected to a `<div>`, not a custom element.** There is no `<data-capture-view>` HTML tag and no React/Vue/Angular component shipped by Scandit. Create the view with `DataCaptureView.forContext(context)` and attach it to a plain `<div id="...">` via `view.connectToElement(divElement)`. Detach with `view.detachFromElement()` when navigating away.
- **`DataCaptureContext.initialize(licenseKey)` returns the context.** Capture the return value: `const context = DataCaptureContext.initialize('<key>');`. There's no `sharedInstance` pattern in the sample — keep a reference to the returned context.
- **Camera is constructed with `Camera.withSettings(...)`, not `Camera.default + applySettings`.** Use `Camera.withSettings(IdCapture.createRecommendedCameraSettings())` to construct a camera pre-configured for ID Capture. The Flutter/RN-style `Camera.default` does not match the Capacitor sample's idiom.
- **Enums use PascalCase member names with camelCase wire values** (same TypeScript convention as RN). Write `IdCaptureRegion.Us`, `IdImageType.CroppedDocument`, `IdSide.Front`, `RejectionReason.Timeout`, `IdAnonymizationMode.FieldsAndImages`, `IdFieldType.DocumentNumber`, `IdLayoutStyle.Rounded`, `FrameSourceState.On` / `.Off`, `AamvaBarcodeVerificationStatus.Authentic`. **Never** use the lowercase Dart/Flutter form.
- **`CapturedId` MRZ/VIZ getters are `mrzResult` / `vizResult`** (not `mrz` / `viz` — that's Flutter). Other source-specific getters: `barcode`, `mobileDocument`, `mobileDocumentOcr`.
- **Images come back as base64 strings.** `images.face`, `images.frame`, `images.getCroppedDocument(IdSide.Front)`, `images.getFrame(IdSide.Front)` each return a `string | null`. Render with `<img src="data:image/png;base64,${face}">` (or set `.src` on an existing `<img>`). **They are not URIs, files, or HTMLImageElements.**
- **Listener is a plain object literal.** `IdCaptureListener` is a TypeScript interface with two optional methods — write `const listener = { didCaptureId(_, captured) { … }, didRejectId(_, rejected, reason) { … } }`. Do **not** create a class with `implements IdCaptureListener` — that's the Dart/Flutter style.
- **`addListener`, `removeListener`, `setMode`, `addMode`, `removeMode`, `applySettings`, `setFrameSource`, `switchToDesiredState` all return Promises.** Either `await` them or chain `.then`.
- **There is no `VisaLetter` document class on Capacitor.** Only `VisaIcao` ships. (On Flutter both exist; on Capacitor/RN only the ICAO visa is modelled.)
- **Lifecycle uses the Capacitor `App` plugin (`@capacitor/app`), not `AppState` (that's RN) or `WidgetsBindingObserver` (that's Flutter).** Subscribe with `App.addListener('appStateChange', …)` to pause/resume the camera and disable the mode.
- Camera permission is handled by the `@capacitor/camera` plugin: install it, add `NSCameraUsageDescription` to iOS `Info.plist`, and call `Camera.requestPermissions()` from `@capacitor/camera` (separate from the Scandit `Camera` class) before mounting the scan view.

### Forbidden APIs (commonly hallucinated — do NOT emit these)

These compile-fail against the real Capacitor packages. Use the right-hand form:

| Do NOT write | Use instead |
|---|---|
| `IdCapture.forContext(context, settings)` | `new IdCapture(settings)` then `await context.setMode(idCapture)` |
| `IdCaptureOverlay.withIdCapture(...)` / `.withIdCaptureForView(...)` | `new IdCaptureOverlay(idCapture)` then `view.addOverlay(overlay)` |
| `IdDocumentType` enum / `settings.supportedDocuments` / `settings.scannerType` | `settings.acceptedDocuments` (document classes) + `settings.scanner = new IdCaptureScanner(new FullDocumentScanner())` |
| `capturedId.documentType` | `capturedId.document?.documentType` (`IdCaptureDocumentType`) or `capturedId.isPassport()` / `isDriverLicense()` / … |
| `capturedId.isVisa()` / `capturedId.isVisaLetter()` | `capturedId.isVisaIcao()` (Capacitor ships only the ICAO visa) |
| `capturedId.mrz` / `capturedId.viz` (Flutter names) | `capturedId.mrzResult` / `capturedId.vizResult` |
| `IdCaptureRegion.us` / `IdSide.front` / `AamvaBarcodeVerificationStatus.authentic` (lowercase Dart form) | `IdCaptureRegion.Us` / `IdSide.Front` / `AamvaBarcodeVerificationStatus.Authentic` — **every Scandit enum member on Capacitor is PascalCase**, including `RejectionReason.*`, `IdImageType.*`, `IdAnonymizationMode.*`, `IdFieldType.*`, `FrameSourceState.*`, `IdLayoutStyle.*`, and the verification status / reasons |
| `capturedId.images.croppedDocument` | `capturedId.images.getCroppedDocument(IdSide.Front)` (also `.face`, `.frame`, `getFrame(IdSide.Front)`) |
| Treating `images.face` like a URI / file / `HTMLImageElement` | It's a base64 string — `<img src="data:image/png;base64,${face}">` or `imgEl.src = '...'` |
| `AamvaBarcodeVerifier` (class) | `settings.rejectForgedAamvaBarcodes = true` + `capturedId.verificationResult.aamvaBarcodeVerification` |
| `DrivingLicenseCategory.categoryCode` | `DrivingLicenseCategory.code` (plus `dateOfIssue` / `dateOfExpiry`) |
| `<data-capture-view>` custom element or `<IdCaptureView>` React-style component | `DataCaptureView.forContext(context)` + `view.connectToElement(document.getElementById('...'))` |
| `Camera.default` (RN/Flutter idiom) | `Camera.withSettings(IdCapture.createRecommendedCameraSettings())` |
| Skipping `ScanditCaptureCorePlugin.initializePlugins()` at startup | always `await ScanditCaptureCorePlugin.initializePlugins();` before any other Scandit API call |
| `idCapture.addListener(...)` without `await` (race at startup) | `await idCapture.addListener(listener)` — same for `removeListener`, `setMode`, `applySettings`, `setFrameSource`, `switchToDesiredState` |

## Product Guidance

Apply these rules whenever the user is making a design decision, not just an API question.

- **Accept only the documents you actually need.** A narrow `acceptedDocuments` list (e.g. just `new DriverLicense(IdCaptureRegion.Us)`) is faster and more accurate than `IdCaptureRegion.Any` across all document types. Ask the user which documents and regions they expect before defaulting to "everything".
- **Pick the scanner that matches the data you need.** `new FullDocumentScanner()` reads front and back automatically (best for most ID/DL use cases). `new SingleSideScanner(barcode, machineReadableZone, visualInspectionZone)` reads a single side from the zone(s) you enable — use it when you only need, say, the PDF417 barcode on the back of a US DL, or only the MRZ of a passport. Use `MobileDocumentScanner` for mobile driver's licenses / mDL.
- **Handle `didRejectId`, not just `didCaptureId`.** Rejections (`RejectionReason.Timeout`, `NotAcceptedDocumentType`, `DocumentExpired`, `DocumentVoided`, `ForgedAamvaBarcode`, …) are how the user learns why a scan didn't succeed. A production integration must surface a message for them.
- **Anonymize by default if you don't need every field.** `IdCaptureSettings.anonymizationMode` and per-field `addAnonymizedField` keep regulated data (e.g. document images, sensitive fields) out of the result unless you opt in. Recommend the minimum that satisfies the use case.
- **Hand off to the `data-capture-sdk` skill for non-ID-Capture questions.** If the user asks about another Scandit product (Barcode Capture, SparkScan, MatrixScan, Label Capture, etc.) or about choosing between products, defer to the `data-capture-sdk` skill instead of guessing.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating ID Capture from scratch** (e.g. "add ID scanning to my Capacitor app", "scan a passport / driver's license", "read the MRZ", "extract the holder's name and date of birth") → read [references/integration.md](references/integration.md) and follow it.
- **One of the three add-on capabilities** ("reject voided / cancelled IDs", "detect punched-hole / voided licenses", "decode the back of a European driving license", "read vehicle categories", "verify the AAMVA barcode / detect forged US licenses") → read [references/supplementary-modules.md](references/supplementary-modules.md).
- **Migrating or upgrading an existing ID Capture integration** ("upgrade ID Capture to the latest SDK", "migrate v7 to v8", "my `scannerType` code stopped compiling", "`AamvaBarcodeVerifier` is gone", "what changed in ID Capture between versions") → read [references/migration.md](references/migration.md).
- **Wiring ID Capture into a host UI framework on top of Capacitor** ("how do I do this in Ionic Angular?", "show me the Ionic React lifecycle", "I'm using Vue 3 / Composition API", "where does the camera start/stop go in `ngAfterViewInit` / `useEffect` / `onMounted`?", "page lifecycle on route transition", "`@ViewChild` for the data-capture-view div") → read [references/framework-recipes.md](references/framework-recipes.md). The Scandit code itself is unchanged from [references/integration.md](references/integration.md); this file shows only the lifecycle glue per framework.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript compiler / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:

1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

Examples in [references/integration.md](references/integration.md) are in **TypeScript / plain JS** (no framework-specific bindings). The official `IdCaptureSimpleSample` is written in JS that runs after `DOMContentLoaded`. If the target project uses a framework on top of Capacitor (Ionic Angular, Ionic React, or Vue 3), see [references/framework-recipes.md](references/framework-recipes.md) for the lifecycle skeleton — the Scandit calls are unchanged; only *where* they hook in differs. Do not introduce a new framework just for ID Capture.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Capacitor integration | [Get Started](https://docs.scandit.com/sdks/capacitor/id-capture/get-started/) · [Sample (IdCaptureSimpleSample)](https://github.com/Scandit/datacapture-capacitor-samples/tree/master/02_ID_Scanning_Samples/IdCaptureSimpleSample) |
| Advanced topics (anonymization, verification, scanners, overlay) | [Advanced Configurations](https://docs.scandit.com/sdks/capacitor/id-capture/advanced/) |
| Migration between major SDK versions | [7 → 8](https://docs.scandit.com/sdks/capacitor/migrate-7-to-8/) |
| Full API reference | [ID Capture API](https://docs.scandit.com/data-capture-sdk/capacitor/id-capture/api.html) |
