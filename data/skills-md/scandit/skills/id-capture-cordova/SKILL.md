---
name: id-capture-cordova
description: Scandit ID Capture (`IdCapture`) in Cordova / PhoneGap projects (`scandit-cordova-datacapture-id`) — scanning passports, driver's licenses, ID cards, residence permits, visas via MRZ, VIZ, barcode, or mobile documents. Use for integration, accepted-document and scanner configuration, captured-field result handling, anonymization, add-on capabilities (voided-ID detection, European driving-license back decoding, AAMVA barcode verification), and SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# ID Capture Cordova Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit ID Capture APIs. The ID Capture API was **restructured at the v7 → v8 boundary** (the standalone `AamvaBarcodeVerifier` was removed in favour of settings flags, and several verification APIs were added). The Cordova plugin surface (global `Scandit.*` namespace after `deviceready`, the imperative `DataCaptureView` + `connectToElement` pattern, `pause` / `resume` document events) is also distinct from the iOS, Android, web, Flutter, React Native, and Capacitor SDKs.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Cordova-specific gotchas worth flagging:

- **Wait for `deviceready` before touching any Scandit API.** The Cordova plugin system populates `window.Scandit.*` and registers native bridges in response to the `deviceready` event — calling `Scandit.DataCaptureContext.initialize(...)` (or anything else) at module load runs into `undefined` symbols. Always wrap the bootstrap in `document.addEventListener('deviceready', () => { … }, false);`.
- **The consumer pattern is the `Scandit.*` global, not an `import`.** Cordova's plugin loader merges every Scandit class onto `window.Scandit`. Write `new Scandit.IdCapture(settings)`, `Scandit.IdCaptureRegion.Us`, `Scandit.RejectionReason.Timeout`. You **do not** `import { IdCapture } from 'scandit-cordova-datacapture-id'` in your application code (that path resolves only inside the plugin's own TypeScript build).
- **The view is an imperative class connected to a `<div>`, not a custom element.** There is no `<data-capture-view>` HTML tag. Create the view with `Scandit.DataCaptureView.forContext(context)` and attach it to a plain `<div id="…">` via `view.connectToElement(divElement)`. Detach with `view.detachFromElement()` when navigating away.
- **`Scandit.DataCaptureContext.initialize(licenseKey)` returns the context.** Capture the return value: `const context = Scandit.DataCaptureContext.initialize('<key>');`. There is no `sharedInstance` pattern in the Cordova sample.
- **Camera is constructed with `Scandit.Camera.withSettings(...)`, returning `Camera | null`.** Use `Scandit.Camera.withSettings(Scandit.IdCapture.createRecommendedCameraSettings())` and **guard the result for null** before dereferencing it.
- **Enums use PascalCase member names with camelCase wire values** (same TypeScript convention as RN / Capacitor). Write `Scandit.IdCaptureRegion.Us`, `Scandit.IdImageType.CroppedDocument`, `Scandit.IdSide.Front`, `Scandit.RejectionReason.Timeout`, `Scandit.IdAnonymizationMode.FieldsAndImages`, `Scandit.IdFieldType.DocumentNumber`, `Scandit.IdLayoutStyle.Rounded`, `Scandit.FrameSourceState.On` / `.Off`, `Scandit.AamvaBarcodeVerificationStatus.Authentic`. **Never** use the lowercase Dart/Flutter form.
- **`CapturedId` MRZ/VIZ getters are `mrzResult` / `vizResult`** (not `mrz` / `viz` — that's Flutter). Other source-specific getters: `barcode`, `mobileDocument`, `mobileDocumentOcr`.
- **Images come back as base64 strings.** `images.face`, `images.frame`, `images.getCroppedDocument(Scandit.IdSide.Front)`, `images.getFrame(Scandit.IdSide.Front)` each return a `string | null`. Render with `<img src="data:image/png;base64,${face}">`. **They are not URIs, files, or HTMLImageElements.**
- **Listener is a plain object literal.** `Scandit.IdCaptureListener` is a TypeScript interface with two optional methods — write `const listener = { didCaptureId(_, captured) { … }, didRejectId(_, rejected, reason) { … } }`. Do **not** create a class with `implements IdCaptureListener` — that's the Dart/Flutter style.
- **There is no `VisaLetter` document class on Cordova.** Only `VisaIcao` ships. (On Flutter both exist; on Cordova / RN / Capacitor only the ICAO visa is modelled.)
- **Lifecycle uses Cordova's `pause` / `resume` document events.** Subscribe with `document.addEventListener('pause' / 'resume', …)` to stop / restart the camera and toggle `idCapture.isEnabled`. There is no React `AppState` (that's RN) and no `@capacitor/app` plugin (that's Capacitor).
- Camera permission is **declared by the plugin and resolved by the native side**. The Cordova ID plugin doesn't ship a JS-side permission request — install `cordova-plugin-android-permissions` (or call the camera-permission API of whatever permissions plugin the project already uses) and request `CAMERA` before mounting the scan view if you want to control the prompt timing; otherwise the OS will prompt on first camera use.

### Forbidden APIs (commonly hallucinated — do NOT emit these)

These either don't exist or were removed. Use the right-hand form:

| Do NOT write | Use instead |
|---|---|
| `import { IdCapture } from 'scandit-cordova-datacapture-id'` in application code | `new Scandit.IdCapture(settings)` after `deviceready` (Cordova merges symbols onto `window.Scandit`) |
| `Scandit.IdCapture.forContext(context, settings)` | `new Scandit.IdCapture(settings)` then `context.setMode(idCapture)` |
| `Scandit.IdCaptureOverlay.withIdCapture(...)` / `.withIdCaptureForView(...)` | `new Scandit.IdCaptureOverlay(idCapture)` then `view.addOverlay(overlay)` |
| `IdDocumentType` enum / `settings.supportedDocuments` | `settings.acceptedDocuments` (document classes) + `settings.scanner = new Scandit.IdCaptureScanner(new Scandit.FullDocumentScanner())` |
| `capturedId.documentType` | `capturedId.document?.documentType` (`IdCaptureDocumentType`) or `capturedId.isPassport()` / `isDriverLicense()` / … |
| `capturedId.isVisa()` / `capturedId.isVisaLetter()` | `capturedId.isVisaIcao()` (Cordova ships only the ICAO visa) |
| `capturedId.mrz` / `capturedId.viz` (Flutter names) | `capturedId.mrzResult` / `capturedId.vizResult` |
| `Scandit.IdCaptureRegion.us` / `Scandit.IdSide.front` / `Scandit.AamvaBarcodeVerificationStatus.authentic` (lowercase Dart form) | `Scandit.IdCaptureRegion.Us` / `Scandit.IdSide.Front` / `Scandit.AamvaBarcodeVerificationStatus.Authentic` — **every Scandit enum member on Cordova is PascalCase**, including `RejectionReason.*`, `IdImageType.*`, `IdAnonymizationMode.*`, `IdFieldType.*`, `FrameSourceState.*`, `IdLayoutStyle.*`, and the verification status / reasons |
| `capturedId.images.croppedDocument` | `capturedId.images.getCroppedDocument(Scandit.IdSide.Front)` (also `.face`, `.frame`, `getFrame(Scandit.IdSide.Front)`) |
| Treating `images.face` like a URI / file / `HTMLImageElement` | It's a base64 string — `<img src="data:image/png;base64,${face}">` or `imgEl.src = '...'` |
| `Scandit.AamvaBarcodeVerifier` (class) | `settings.rejectForgedAamvaBarcodes = true` + `capturedId.verificationResult.aamvaBarcodeVerification` |
| `DrivingLicenseCategory.categoryCode` | `DrivingLicenseCategory.code` (plus `dateOfIssue` / `dateOfExpiry`) |
| `<data-capture-view>` custom element or any framework-component wrapper | `Scandit.DataCaptureView.forContext(context)` + `view.connectToElement(document.getElementById('...'))` |
| `Camera.default` (RN / Flutter idiom) | `Scandit.Camera.withSettings(Scandit.IdCapture.createRecommendedCameraSettings())` — and guard the `Camera \| null` return |
| Touching `Scandit.*` before `deviceready` fires | wrap your bootstrap in `document.addEventListener('deviceready', () => { … }, false);` |

## Product Guidance

Apply these rules whenever the user is making a design decision, not just an API question.

- **Accept only the documents you actually need.** A narrow `acceptedDocuments` list (e.g. just `new Scandit.DriverLicense(Scandit.IdCaptureRegion.Us)`) is faster and more accurate than `IdCaptureRegion.Any` across all document types. Ask the user which documents and regions they expect before defaulting to "everything".
- **Pick the scanner that matches the data you need.** `new Scandit.FullDocumentScanner()` reads front and back automatically (best for most ID/DL use cases). `new Scandit.SingleSideScanner(barcode, machineReadableZone, visualInspectionZone)` reads a single side from the zone(s) you enable. Use `Scandit.MobileDocumentScanner` for mobile driver's licenses / mDL.
- **Handle `didRejectId`, not just `didCaptureId`.** Rejections (`Scandit.RejectionReason.Timeout`, `NotAcceptedDocumentType`, `DocumentExpired`, `DocumentVoided`, `ForgedAamvaBarcode`, …) are how the user learns why a scan didn't succeed. A production integration must surface a message for them.
- **Anonymize by default if you don't need every field.** `IdCaptureSettings.anonymizationMode` and per-field `addAnonymizedField` keep regulated data (e.g. document images, sensitive fields) out of the result unless you opt in.
- **Hand off to the `data-capture-sdk` skill for non-ID-Capture questions.** If the user asks about another Scandit product (Barcode Capture, SparkScan, MatrixScan, Label Capture, etc.) or about choosing between products, defer to the `data-capture-sdk` skill instead of guessing.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating ID Capture from scratch** ("add ID scanning to my Cordova app", "scan a passport / driver's license", "read the MRZ", "extract the holder's name and date of birth") → read [references/integration.md](references/integration.md) and follow it.
- **One of the three add-on capabilities** ("reject voided / cancelled IDs", "detect punched-hole / voided licenses", "decode the back of a European driving license", "read vehicle categories", "verify the AAMVA barcode / detect forged US licenses") → read [references/supplementary-modules.md](references/supplementary-modules.md).
- **Migrating or upgrading an existing ID Capture integration** ("upgrade ID Capture to the latest SDK", "migrate v7 to v8", "`AamvaBarcodeVerifier` is gone", "what changed in ID Capture between versions") → read [references/migration.md](references/migration.md).

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or globals. If unsure whether an API exists or how it is called — or if a TypeScript compiler / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:

1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

Examples in this skill are in **plain JavaScript / TypeScript** (no UI-framework bindings) because the official `IdCaptureSimpleSample` is plain `www/js/*.js` running after `deviceready`. If the project uses a UI framework on top of Cordova (jQuery Mobile, Onsen UI, an older Ionic v1 / Ionic v3 setup, Framework7), keep the same bootstrap and Scandit calls and wire `view.connectToElement(...)` into a host `<div>` in the framework's view template. Do not introduce a new framework just for ID Capture.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Cordova integration | [Get Started](https://docs.scandit.com/sdks/cordova/id-capture/get-started/) · [Sample (IdCaptureSimpleSample)](https://github.com/Scandit/datacapture-cordova-samples/tree/master/02_ID_Scanning_Samples/IdCaptureSimpleSample) |
| Advanced topics (anonymization, verification, scanners, overlay) | [Advanced Configurations](https://docs.scandit.com/sdks/cordova/id-capture/advanced/) |
| Migration between major SDK versions | [7 → 8](https://docs.scandit.com/sdks/cordova/migrate-7-to-8/) |
| Full API reference | [ID Capture API](https://docs.scandit.com/data-capture-sdk/cordova/id-capture/api.html) |
