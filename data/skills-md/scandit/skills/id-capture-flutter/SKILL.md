---
name: id-capture-flutter
description: Scandit ID Capture (`IdCapture`) in Flutter projects — scanning passports, driver's licenses, ID cards, residence permits, visas via MRZ, VIZ, barcode, or mobile documents. Use for integration, accepted-document and scanner configuration, captured-field result handling, anonymization, add-on capabilities (voided-ID detection, European driving-license back decoding, AAMVA barcode verification), and SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# ID Capture Flutter Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit ID Capture APIs. The ID Capture API was **restructured at the v7 → v8 boundary** (the `IdCaptureScanner` was reshaped into a wrapper over `physicalDocumentScanner` / `mobileDocumentScanner`, the standalone `AamvaBarcodeVerifier` was removed in favour of settings flags, and several verification APIs were added). The Flutter plugin surface (package names, plugin initialization, widget lifecycle) is also distinct from the iOS, Android, web, React Native, Cordova, and Capacitor SDKs.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Flutter-specific gotchas worth flagging:

- **The ID plugin must be initialized before any Scandit API call.** Call `await ScanditFlutterDataCaptureId.initialize();` in `main()` (after `WidgetsFlutterBinding.ensureInitialized()`, before `runApp`). Initializing the ID plugin initializes the core plugin for you — you do **not** call a separate core `initialize()`. Skipping this causes opaque runtime/MethodChannel crashes.
- **Context is created with `DataCaptureContext.forLicenseKey(licenseKey)`** on Flutter for ID Capture (matches the official `IdCaptureSimpleSample`). Do not use `DataCaptureContext.initialize(...)`.
- **Listener method names are iOS-style on Flutter:** `didCaptureId(IdCapture, CapturedId)` and `didRejectId(IdCapture, CapturedId?, RejectionReason)`. There is no `onIdCaptured` / web-style callback on Flutter.
- **Settings are list-based, not a bitmask.** Configure `settings.acceptedDocuments` (and optionally `settings.rejectedDocuments`) with document objects (`Passport(IdCaptureRegion.any)`, `DriverLicense(...)`, `IdCard(...)`, …) and set `settings.scanner`. The old `supportedDocuments` / `IdDocumentType` bitmask API was removed back at the v6 → v7 boundary — do not use it. Separately, the scanner property was renamed `scannerType` → `scanner` and reshaped into a wrapper at v7 → v8 (see [references/migration.md](references/migration.md)).
- **The three capability add-ons are separate packages but driven by base-module settings flags** (`rejectVoidedIds`, `decodeBackOfEuropeanDrivingLicense`, `rejectForgedAamvaBarcodes`). See [references/supplementary-modules.md](references/supplementary-modules.md). There is **no standalone `AamvaBarcodeVerifier` class on Flutter** in v8.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/Runner/Info.plist`) and Android (declared by the plugin; request at runtime with the `permission_handler` package).

### Forbidden APIs (commonly hallucinated — do NOT emit these)

These compile-fail against the real Flutter packages. Use the right-hand form:

| Do NOT write | Use instead |
|---|---|
| `IdCapture.forContext(context, settings)` | `IdCapture(settings)` then `context.setMode(idCapture)` |
| `IdCaptureOverlay.withIdCapture(...)` / `.withIdCaptureForView(...)` | `IdCaptureOverlay(idCapture)` then `captureView.addOverlay(overlay)` |
| `IdDocumentType` enum / `settings.supportedDocuments` / `settings.scannerType` | `settings.acceptedDocuments` (document classes) + `settings.scanner = IdCaptureScanner(physicalDocumentScanner: ...)` |
| `capturedId.documentType` | `capturedId.document?.documentType` (`IdCaptureDocumentType`) or `capturedId.isPassport()` / `isDriverLicense()` / … |
| `capturedId.isVisa()` | `capturedId.isVisaIcao()` / `capturedId.isVisaLetter()` |
| `capturedId.images.croppedDocument` | `capturedId.images.getCroppedDocument(IdSide.front)` (also `.face`, `.frame`, `getFrame(IdSide.front)`) |
| `image.buffer` / `image.bytes` / `Image.memory(image…)` on an `IdImages` result | the result is already a Flutter `Image` widget — render it directly in the tree |
| `AamvaBarcodeVerifier` (class) | `settings.rejectForgedAamvaBarcodes = true` + `capturedId.verificationResult.aamvaBarcodeVerification` |
| `DrivingLicenseCategory.categoryCode` | `DrivingLicenseCategory.code` (plus `dateOfIssue` / `dateOfExpiry`) |
- The `DataCaptureView` is a Flutter widget; its lifecycle ties to the widget tree. Pause the camera in `didChangeAppLifecycleState` (via `WidgetsBindingObserver`) and clean up listeners / disable the mode when leaving the screen.

## Product Guidance

Apply these rules whenever the user is making a design decision, not just an API question.

- **Accept only the documents you actually need.** A narrow `acceptedDocuments` list (e.g. just `DriverLicense(IdCaptureRegion.us)`) is faster and more accurate than `IdCaptureRegion.any` across all document types. Ask the user which documents and regions they expect before defaulting to "everything".
- **Pick the scanner that matches the data you need.** `FullDocumentScanner()` reads front and back automatically (best for most ID/DL use cases). `SingleSideScanner(barcode, machineReadableZone, visualInspectionZone)` reads a single side from the zone(s) you enable — use it when you only need, say, the PDF417 barcode on the back of a US DL, or only the MRZ of a passport. Use `MobileDocumentScanner` for mobile driver's licenses / mDL.
- **Handle `didRejectId`, not just `didCaptureId`.** Rejections (`RejectionReason.timeout`, `notAcceptedDocumentType`, `documentExpired`, `documentVoided`, `forgedAamvaBarcode`, …) are how the user learns why a scan didn't succeed. A production integration must surface a message for them.
- **Anonymize by default if you don't need every field.** `IdCaptureSettings.anonymizationMode` and per-field anonymization keep regulated data (e.g. document images, sensitive fields) out of the result unless you opt in. Recommend the minimum that satisfies the use case.
- **Hand off to the `data-capture-sdk` skill for non-ID-Capture questions.** If the user asks about another Scandit product (Barcode Capture, SparkScan, MatrixScan, Label Capture, etc.) or about choosing between products, defer to the `data-capture-sdk` skill instead of guessing.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating ID Capture from scratch** (e.g. "add ID scanning to my app", "scan a passport / driver's license", "read the MRZ", "extract the holder's name and date of birth") → read [references/integration.md](references/integration.md) and follow it.
- **One of the three add-on capabilities** ("reject voided / cancelled IDs", "detect punched-hole / voided licenses", "decode the back of a European driving license", "read vehicle categories", "verify the AAMVA barcode / detect forged US licenses") or **data-consistency verification** ("reject documents whose printed data doesn't match the MRZ / barcode", "detect tampered IDs", "cross-check VIZ against barcode") → read [references/supplementary-modules.md](references/supplementary-modules.md).
- **Migrating or upgrading an existing ID Capture integration** ("upgrade ID Capture to the latest SDK", "migrate v7 to v8", "my `supportedDocuments` code stopped compiling", "`AamvaBarcodeVerifier` is gone", "what changed in ID Capture between versions") → read [references/migration.md](references/migration.md).
- **State management or route lifecycle** ("how do I do this with BLoC?", "Riverpod / AsyncNotifier setup", "camera doesn't pause when I push another screen", "`RouteAware` / `RouteObserver`", "GoRouter and ID Capture", "should I keep IdCapture in a Provider / ChangeNotifier?") → read [references/framework-recipes.md](references/framework-recipes.md). The Scandit code itself is unchanged from [references/integration.md](references/integration.md); this file covers the BLoC / Riverpod / route-observer glue.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a Dart compiler / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:

1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

Examples in [references/integration.md](references/integration.md) use **StatefulWidget + WidgetsBindingObserver** because the official `IdCaptureSimpleSample` uses it. If the project uses BLoC (matching the `IdCaptureExtendedSample`), Riverpod, or a route observer / GoRouter, see [references/framework-recipes.md](references/framework-recipes.md) — the Scandit calls are unchanged; only the state-management harness and the route-aware lifecycle differ. Do not introduce a new state-management library just for ID Capture.

Examples are in **Dart** (sound null-safety). Flutter `>=3.22.0` and Dart `>=3.4.0` are required by the ID plugin.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Flutter integration | [Get Started](https://docs.scandit.com/sdks/flutter/id-capture/get-started/) · [Sample (IdCaptureSimpleSample)](https://github.com/Scandit/datacapture-flutter-samples/tree/master/02_ID_Scanning_Samples/IdCaptureSimpleSample) |
| Advanced topics (anonymization, verification, scanners, overlay) | [Advanced Configurations](https://docs.scandit.com/sdks/flutter/id-capture/advanced/) |
| Migration between major SDK versions | [7 → 8](https://docs.scandit.com/sdks/flutter/migrate-7-to-8/) |
| Full API reference | [ID Capture API](https://docs.scandit.com/data-capture-sdk/flutter/id-capture/api.html) |
