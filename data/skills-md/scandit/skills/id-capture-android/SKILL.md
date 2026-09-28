---
name: id-capture-android
description: Scandit ID Capture (`IdCapture`) in native Android (Kotlin or Java) projects — scanning passports, driver's licenses, ID cards, residence permits, health-insurance cards, visas via MRZ, VIZ, PDF417 barcode, or mobile documents. Use for integration, accepted-document and scanner configuration, CapturedId result handling, rejection rules, AAMVA verification, anonymization, overlay UI, camera lifecycle, and Scandit Android SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# ID Capture Android (Kotlin/Java) Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit ID Capture APIs. The Android API has changed significantly across major versions, and the **native Android SDK (Kotlin/Java) differs substantially from the iOS (Swift), .NET, Flutter, and React Native SDKs**. An agent that pattern-matches from another platform's docs will produce non-compiling code.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** The most common sources of wrong code:

- **The v6 API** — `supportedDocuments` (a bitmask of `IdDocumentType` like `ID_CARD_VIZ`/`DL_VIZ`), `supportedSides`, and session-based callbacks (`onIdCaptured(idCapture, session, frameData)`) were all replaced in v7. Do not emit any of these.
- **The v7.x API** — `settings.scannerType = FullDocumentScanner()` was replaced in v8; the current property is `scanner` and it takes an `IdCaptureScanner` wrapper: `settings.scanner = IdCaptureScanner(FullDocumentScanner())`.
- **Cross-platform drift** — iOS uses `IdCapture(context:settings:)`, .NET uses `IdCapture.Create(...)`, Flutter uses a different builder. The Android API is the static factory `IdCapture.forDataCaptureContext(context, settings)`.
- **Zone result property names** — on Android the zone results are `capturedId.mrz`, `capturedId.viz`, `capturedId.barcode` (and `capturedId.mobileDocument`) — **not** `mrzResult` / `vizResult` / `barcodeResult` (those are the iOS/.NET-style names).
- **Enum casing** — Android enums are `UPPER_SNAKE_CASE`: `IdCaptureRegion.ANY`, `IdCaptureRegion.EU_AND_SCHENGEN`, `RejectionReason.DOCUMENT_EXPIRED`, `IdAnonymizationMode.FIELDS_AND_IMAGES` — not the Swift `.any` / `.documentExpired` camelCase.
- **Standalone verifier classes** — `AamvaBarcodeVerifier` / `DataConsistencyVerifier` are not used here. Verification is settings-driven: set `rejectForgedAamvaBarcodes = true` / `rejectInconsistentData = true` and read `capturedId.verificationResult`.
- **Image opt-in** — Android uses `settings.setShouldPassImageTypeToResult(IdImageType.FACE, true)` — not the iOS `setIncludeImage(_:for:)`.
- **NFC** — NFC chip reading exists on native Android but is **not covered by this skill**. If the user asks about NFC, refer them to the official documentation.

### Forbidden APIs (commonly hallucinated — do NOT emit these)

| Do NOT write | Use instead                                                                                                  |
|---|--------------------------------------------------------------------------------------------------------------|
| `IdCapture(context, settings)` (iOS) / `IdCapture.Create(...)` (.NET) / `new IdCapture(...)` | `IdCapture.forDataCaptureContext(context, settings)`                                                         |
| `settings.supportedDocuments = [...]` / `IdDocumentType` bitmask | `settings.acceptedDocuments = listOf(IdCard(IdCaptureRegion.ANY), ...)`                                      |
| `settings.supportedSides = ...` | `settings.scanner = IdCaptureScanner(SingleSideScanner(...))`                                                |
| `settings.scannerType = FullDocumentScanner()` (v7 API) | `settings.scanner = IdCaptureScanner(FullDocumentScanner())`                                                 |
| `settings.setIncludeImage(true, ...)` (iOS) | `settings.setShouldPassImageTypeToResult(IdImageType.CROPPED_DOCUMENT, true)`                                |
| `IdCaptureRegion.Any` / `.us` / `RejectionReason.documentExpired` (camelCase/PascalCase) | `IdCaptureRegion.ANY` / `IdCaptureRegion.US` / `RejectionReason.DOCUMENT_EXPIRED` (UPPER_SNAKE)              |
| `AamvaBarcodeVerifier(...)` / `AamvaBarcodeVerifier.create(...)` | `settings.rejectForgedAamvaBarcodes = true` + read `capturedId.verificationResult?.aamvaBarcodeVerification` |
| `DataConsistencyVerifier(...)` | `settings.rejectInconsistentData = true` + read `capturedId.verificationResult?.dataConsistency`             |
| `capturedId.mrzResult` / `capturedId.vizResult` / `capturedId.barcodeResult` | `capturedId.mrz` / `capturedId.viz` / `capturedId.barcode`                                                   |
| `DataCaptureContext.initialize(licenseKey:)` (iOS) / `.ForLicenseKey(...)` (.NET) | `DataCaptureContext.forLicenseKey("...")`                                                                    |
| `IdCaptureOverlay(idCapture, view)` (iOS-style constructor) | `IdCaptureOverlay.newInstance(idCapture, dataCaptureView)`                                                   |

## Product Guidance

- **Accept only the documents you actually need.** Ask the user which document types and regions they expect. Documents not in `acceptedDocuments` will be rejected with `RejectionReason.NOT_ACCEPTED_DOCUMENT_TYPE`. A narrow list (e.g. just `DriverLicense(IdCaptureRegion.US)`) is faster and more accurate than `IdCaptureRegion.ANY` across every document type.
- **Pick the scanner that matches the data you need.** Ask the user whether they need data from both sides, a specific zone only, or a mobile-presented ID — then choose `FullDocumentScanner`, `SingleSideScanner`, or `MobileDocumentScanner` accordingly. See [references/advanced.md](references/advanced.md) for details.
- **Handle `onIdRejected`, not just `onIdCaptured`.** Rejections (`RejectionReason.TIMEOUT`, `.NOT_ACCEPTED_DOCUMENT_TYPE`, `.DOCUMENT_EXPIRED`, `.HOLDER_UNDERAGE`, `.FORGED_AAMVA_BARCODE`, `.INCONSISTENT_DATA`, …) are how the user learns why a scan didn't succeed.
- **Callbacks run on a background thread.** Both `onIdCaptured` and `onIdRejected` are invoked off the main thread — dispatch all UI work with `runOnUiThread {}` (Activity) or post to the main `Handler`. Set `idCapture.isEnabled = false` at the top of the callback while you handle the result, and re-enable it when the user is ready to scan again.
- **Mode co-existence with BarcodeCapture.** `IdCapture` and `BarcodeCapture` can run together on one `DataCaptureContext` (e.g. an airport screen reading a boarding-pass barcode and a passport). Create each mode with its `forDataCaptureContext` factory, give each its own listener, and toggle each with `isEnabled` — no need to remove one to add the other. See [references/advanced.md](references/advanced.md).
- **Be aware of the default anonymization list.** The SDK anonymizes certain fields by default to meet regional legal requirements (e.g. document number on German ID cards). If a field is unexpectedly `null`, check `capturedId.anonymizedFields`. See [references/advanced.md](references/advanced.md).
- **Hand off to the `data-capture-sdk` skill for non-ID-Capture questions.** If the user asks about Barcode Capture, SparkScan, MatrixScan, Label Capture, or choosing between products, defer to the `data-capture-sdk` skill.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating ID Capture from scratch, or any question about document selection, scanner choice, rejection rules, image capture, or reading results (top-level fields or zone-specific `mrz`/`viz`/`barcode`)** → read [references/integration.md](references/integration.md) and follow it.
- **USDL verification (forged barcodes, data inconsistency, frontReviewImage), anonymization, voided detection, EU driving-license back decoding, BarcodeCapture co-existence, mobile documents (mDL), overlay customization, or custom feedback** → read [references/advanced.md](references/advanced.md) and follow it.
- **Upgrading the Scandit Android SDK version on an existing ID Capture integration** (e.g. "migrate from 6.x to 7", "update Scandit to the latest version", "we're on 7.x and the build breaks after bumping dependencies", code that still uses `supportedDocuments` / `IdDocumentType` / `onIdCaptured(idCapture, session, frameData)`) → read [references/migration.md](references/migration.md) and follow it.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how to call it — or if a compile error occurs — fetch the relevant documentation page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. an `api/ui/` subdirectory) and guessing will lead to 404s.

## References

| Topic | Resource |
|---|---|
| Get Started (Android) | [Get Started (Android)](https://docs.scandit.com/sdks/android/id-capture/get-started/) |
| Advanced topics | [Advanced Configurations (Android)](https://docs.scandit.com/sdks/android/id-capture/advanced/) |
| SDK version migration | [references/migration.md](references/migration.md) · [Migrate 6→7](https://docs.scandit.com/sdks/android/migrate-6-to-7/) · [Migrate 7→8](https://docs.scandit.com/sdks/android/migrate-7-to-8/) |
| Full API reference | [ID Capture API (Android)](https://docs.scandit.com/data-capture-sdk/android/id-capture/api.html) |

## API surface this skill covers

All classes available on the native Android SDK. The modern document/scanner API (`acceptedDocuments`, `IdCaptureScanner`, `FullDocumentScanner`) landed at **7.0**; the rejection flags and verification result model at **7.6/8.0**. This skill targets the current **8.x** stable release.

- **`IdCapture`** — static `IdCapture.forDataCaptureContext(context: DataCaptureContext, settings: IdCaptureSettings)`; `isEnabled` (get/set); `addListener(IdCaptureListener)` / `removeListener(...)`; static `createRecommendedCameraSettings()`; `feedback` (`IdCaptureFeedback`); `reset()`; `applySettings(settings)`.
- **`IdCaptureSettings`** — `IdCaptureSettings()`; properties: `scanner` (`IdCaptureScanner`), `acceptedDocuments` / `rejectedDocuments` (`List<IdCaptureDocument>`), `rejectVoidedIds`, `rejectExpiredIds`, `rejectIdsExpiringIn` (`Duration?`), `rejectNotRealIdCompliant`, `rejectForgedAamvaBarcodes`, `rejectInconsistentData`, `rejectHolderBelowAge` (`Int?`), `decodeBackOfEuropeanDrivingLicense`, `anonymizationMode` (`IdAnonymizationMode`), `anonymizeDefaultFields`; methods `setShouldPassImageTypeToResult(IdImageType, Boolean)`, `addAnonymizedField(document, IdFieldType)`.
- **`IdCaptureScanner`** — `IdCaptureScanner(physicalDocument: PhysicalDocumentScanner?)` and `IdCaptureScanner(physicalDocument:, mobileDocument:)`.
- **Physical scanners**: `FullDocumentScanner()` — both sides, all zones; `SingleSideScanner(barcode: Boolean, machineReadableZone: Boolean, visualInspectionZone: Boolean)` — single side, selected zones.
- **`MobileDocumentScanner`** — `MobileDocumentScanner(iso180135: Boolean, ocr: Boolean)` (also `MobileDocumentScanner()` and an `elementsToRetain` overload). `iso180135` uses ISO 18013-5 QR + Bluetooth handover; `ocr` reads a mobile document displayed on another device's screen.
- **Document types** (`IdCaptureDocument`, props `region` + `documentType`): `IdCard(IdCaptureRegion)`, `DriverLicense(IdCaptureRegion)`, `Passport(IdCaptureRegion)`, `VisaIcao(IdCaptureRegion)`, `ResidencePermit(IdCaptureRegion)`, `HealthInsuranceCard(IdCaptureRegion)`, `RegionSpecific(RegionSpecificSubtype)`.
- **`IdCaptureRegion`** enum — `ANY`, `EU_AND_SCHENGEN`, and ~250 region values (`US`, `UK`, `UAE`, `GERMANY`, …), all `UPPER_SNAKE_CASE`.
- **`IdCaptureListener`** — `onIdCaptured(mode: IdCapture, id: CapturedId)`, `onIdRejected(mode: IdCapture, id: CapturedId?, reason: RejectionReason)`. (These are the SDK's interface parameter names, also used by the official samples; Kotlin allows renaming them in your override.)
- **`CapturedId`** — `fullName` / `firstName` / `lastName` (`String?`), `sex` / `sexType`, `dateOfBirth` / `dateOfExpiry` / `dateOfIssue` (`DateResult?`), `nationality`, `address`, `age` (`Int?`), `isExpired`, `document` (`IdCaptureDocument?`), `issuingCountry` (`IdCaptureRegion`), `documentNumber` / `documentAdditionalNumber`, `viz` / `mrz` / `barcode` / `mobileDocument` (`VizResult?`/`MrzResult?`/`BarcodeResult?`/`MobileDocumentResult?`), `images` (`IdImages`), `verificationResult` (`VerificationResult?` — nullable), `anonymizedFields`.
- **`DateResult`** — `day` / `month` (`Int?`), `year` (`Int`), `localDate` / `utcDate` (`java.util.Date`).
- **`IdImages`** — `face` (`Bitmap?`), `frame` (`Bitmap?`), `getCroppedDocument(side: IdSide)` (`Bitmap?`).
- **`VerificationResult`** — `dataConsistency` (`DataConsistencyResult?`), `aamvaBarcodeVerification` (`AamvaBarcodeVerificationResult?`).
- **`DataConsistencyResult`** — `allChecksPassed`, `frontReviewImage` (`Bitmap?`).
- **`AamvaBarcodeVerificationResult`** — `status` (`AamvaBarcodeVerificationStatus`: `AUTHENTIC` / `LIKELY_FORGED` / `FORGED`).
- **`IdCaptureOverlay`** — `IdCaptureOverlay.newInstance(idCapture, dataCaptureView)`; `idLayoutStyle` (`IdLayoutStyle`: `ROUNDED` / `SQUARE`), `idLayoutLineStyle` (`IdLayoutLineStyle`: `BOLD` / `LIGHT`), `showTextHints`, `setFrontSideTextHint(...)` / `setBackSideTextHint(...)`, `capturedBrush` / `localizedBrush` / `rejectedBrush`.
- **`IdCaptureFeedback`** — `IdCaptureFeedback()`; `idCaptured` / `idRejected` (`Feedback`); static `defaultFeedback()`.
- **`DataCaptureContext`** — `DataCaptureContext.forLicenseKey("...")`; `setFrameSource(camera)`; `removeCurrentMode()` / `removeAllModes()`.
- **`Camera`** — `Camera.getDefaultCamera(IdCapture.createRecommendedCameraSettings())`; `switchToDesiredState(FrameSourceState.ON / OFF)`.
- **`DataCaptureView`** — `DataCaptureView.newInstance(context, dataCaptureContext)`.
- **`RejectionReason`** enum — `NOT_ACCEPTED_DOCUMENT_TYPE`, `INVALID_FORMAT`, `DOCUMENT_VOIDED`, `TIMEOUT`, `SINGLE_IMAGE_NOT_RECOGNIZED`, `DOCUMENT_EXPIRED`, `DOCUMENT_EXPIRES_SOON`, `NOT_REAL_ID_COMPLIANT`, `HOLDER_UNDERAGE`, `FORGED_AAMVA_BARCODE`, `INCONSISTENT_DATA`.
- **`IdAnonymizationMode`** enum — `NONE`, `FIELDS_ONLY`, `IMAGES_ONLY`, `FIELDS_AND_IMAGES`.
- **`IdImageType`** enum — `FACE`, `CROPPED_DOCUMENT`, `FRAME`.
- **`IdSide`** enum — `FRONT`, `BACK`.

### Available on native Android but NOT covered by this skill

- **NFC** chip reading — native Android only; refer to the official documentation.
- **Deserializer** (`IdCaptureDeserializer`) — available on Android native but not in scope here.
