---
name: id-capture-ios
description: Scandit ID Capture (`IdCapture`) in native iOS Swift projects (UIKit or SwiftUI) — scanning passports, driver's licenses, ID cards, residence permits, health-insurance cards, visas via MRZ, VIZ, PDF417 barcode, or mobile documents on iOS. Use for integration, accepted-document and scanner configuration, CapturedId result handling, rejection rules, AAMVA verification, anonymization, overlay UI, camera lifecycle, and Scandit iOS SDK version migration in Swift, UIKit, or SwiftUI iOS apps.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# ID Capture iOS (Swift/UIKit) Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit ID Capture APIs. The iOS Swift API has changed significantly across major versions, and the **native iOS SDK differs substantially from the Android (Kotlin/Java), .NET, Flutter, and React Native SDKs**. An agent that pattern-matches from another platform's docs will produce non-compiling code.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** The most common sources of wrong code:

- **The v6 API** — `supportedDocuments` (a bitmask enum like `.idCardVIZ`/`.dlVIZ`), `supportedSides`, and session-based callbacks (`didCaptureIn session:frameData:`) were all replaced in v7. Do not emit any of these.
- **The v7.x API** — `settings.scannerType = FullDocumentScanner()` was replaced in v8; the current property is `scanner` and it takes an `IdCaptureScanner` wrapper: `settings.scanner = IdCaptureScanner(physicalDocument: FullDocumentScanner())`.
- **ObjC prefixes** — the Objective-C SDK uses an `SDC` prefix on all types (`SDCIdCapture`, `SDCCapturedId`, etc.). These prefixes do **not** appear in Swift. Never emit `SDCIdCapture`, `SDCIdCaptureSettings`, etc. in Swift code.
- **Cross-platform drift** — Android uses `IdCapture.forDataCaptureContext(...)`, .NET uses `IdCapture.Create(...)`, Flutter uses a different builder. The Swift API is `IdCapture(context:settings:)`.
- **Standalone verifier classes** — `AamvaBarcodeVerifier` and `DataConsistencyVerifier` do not exist in the native iOS SDK. Verification is settings-driven: set `rejectForgedAamvaBarcodes = true` / `rejectInconsistentData = true` and read `capturedId.verificationResult`.
- **NFC** — `NfcScanner` exists on native iOS but is **not covered by this skill**. If the user asks about NFC, refer them to the official documentation.

### Forbidden APIs (commonly hallucinated — do NOT emit these)

| Do NOT write | Use instead |
|---|---|
| `IdCapture.Create(context, settings)` / `IdCapture.forDataCaptureContext(...)` | `IdCapture(context: context, settings: settings)` |
| `settings.supportedDocuments = [.idCardVIZ, .dlVIZ, ...]` | `settings.acceptedDocuments = [IdCard(region: .any), ...]` |
| `settings.supportedSides = .frontOnly` | `settings.scanner = IdCaptureScanner(physicalDocument: SingleSideScanner(...))` |
| `settings.scannerType = FullDocumentScanner()` (v7 API) | `settings.scanner = IdCaptureScanner(physicalDocument: FullDocumentScanner())` |
| `new AamvaBarcodeVerifier(...)` / `AamvaBarcodeVerifier.Create(...)` | `settings.rejectForgedAamvaBarcodes = true` + read `capturedId.verificationResult.aamvaBarcodeVerification` |
| `new DataConsistencyVerifier(...)` | `settings.rejectInconsistentData = true` + read `capturedId.verificationResult.dataConsistency` |
| `capturedId.barcodeResult` | `capturedId.barcode` |
| `capturedId.Images` / `capturedId.VerificationResult` (PascalCase, .NET style) | `capturedId.images` / `capturedId.verificationResult` (camelCase) |
| `SDCIdCapture` / `SDCCapturedId` / any `SDC`-prefixed type in Swift | `IdCapture` / `CapturedId` (no prefix in Swift) |
| `DataCaptureContext.ForLicenseKey(...)` (.NET) or `DataCaptureContext.forLicenseKey(...)` (Android) | `DataCaptureContext.initialize(licenseKey: "...")` then `DataCaptureContext.shared` |

## Product Guidance

- **Accept only the documents you actually need.** Ask the user which document types and regions they expect. Documents not in `acceptedDocuments` will be rejected with `RejectionReason.notAcceptedDocumentType`.
- **Pick the scanner that matches the data you need.** Ask the user whether they need data from both sides, a specific zone only, or a mobile-presented ID — then choose `FullDocumentScanner`, `SingleSideScanner`, or `MobileDocumentScanner` accordingly. See [references/advanced.md](references/advanced.md) for details.
- **Handle `didReject` not just `didCapture`.** Rejections (`RejectionReason.timeout`, `.notAcceptedDocumentType`, `.documentExpired`, `.holderUnderage`, `.forgedAamvaBarcode`, `.inconsistentData`, …) are how the user learns why a scan didn't succeed.
- **Mode co-existence with BarcodeCapture.** `IdCapture` and `BarcodeCapture` can run together on one `DataCaptureContext` (e.g. an airport screen reading a boarding-pass barcode and a passport). Attach each mode to the context (its iOS constructor `IdCapture(context:settings:)` / `BarcodeCapture(context:settings:)`), give each its own listener, and toggle each with `isEnabled` — no need to remove one to add the other. See [references/advanced.md](references/advanced.md).
- **Be aware of the default anonymization list.** The SDK anonymizes certain fields by default to meet regional legal requirements (e.g. document number on German ID cards). If a field is unexpectedly `nil`, check `capturedId.anonymizedFields`. See [references/advanced.md](references/advanced.md).
- **Hand off to the `data-capture-sdk` skill for non-ID-Capture questions.** If the user asks about Barcode Capture, SparkScan, MatrixScan, Label Capture, or choosing between products, defer to the `data-capture-sdk` skill.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating ID Capture from scratch, or any question about document selection, scanner choice, rejection rules, image capture, or reading results (top-level fields or zone-specific mrzResult/vizResult/barcode)** → read [references/integration.md](references/integration.md) and follow it.
- **USDL verification (forged barcodes, data inconsistency, frontReviewImage), anonymization, BarcodeCapture co-existence, overlay customization, or custom feedback** → read [references/advanced.md](references/advanced.md) and follow it.
- **Upgrading the Scandit iOS SDK version on an existing ID Capture integration** (e.g. "migrate from 6.x to 7", "update Scandit to the latest version", "we're on 7.x and the build breaks after bumping packages", code that still uses `supportedDocuments` / `IdDocumentType` / `didCaptureIn session:`) → read [references/migration.md](references/migration.md) and follow it.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how to call it — or if a compile error occurs — fetch the relevant documentation page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** Fetch the index page and follow links from there.

## References

| Topic | Resource |
|---|---|
| Get Started (iOS) | [Get Started (iOS Swift)](https://docs.scandit.com/sdks/ios/id-capture/get-started/) |
| Advanced topics | [Advanced Configurations (iOS)](https://docs.scandit.com/sdks/ios/id-capture/advanced/) |
| SDK version migration | [references/migration.md](references/migration.md) · [Migrate 6→7](https://docs.scandit.com/sdks/ios/migrate-6-to-7/) · [Migrate 7→8](https://docs.scandit.com/sdks/ios/migrate-7-to-8/) |
| Full API reference | [ID Capture API (iOS)](https://docs.scandit.com/data-capture-sdk/ios/id-capture/api.html) |

## API surface this skill covers

All classes available on the native iOS SDK. The modern document/scanner API (`acceptedDocuments`, `IdCaptureScanner`, `FullDocumentScanner`) landed at **7.0**; the rejection flags and verification result model at **7.6/8.0**. This skill targets the current **8.x** stable release.

- **`IdCapture`** — `IdCapture(context: DataCaptureContext, settings: IdCaptureSettings)`; `isEnabled` (get/set); `addListener(_:)` / `removeListener(_:)` (`IdCaptureListener`); `static recommendedCameraSettings`; `feedback` (`IdCaptureFeedback`); `reset()`; `applySettings(_:)`.
- **`IdCaptureSettings`** — `IdCaptureSettings()`; properties: `scanner` (`IdCaptureScanner`), `acceptedDocuments` / `rejectedDocuments` (`[any IdCaptureDocument]`), `rejectVoidedIds`, `rejectExpiredIds`, `rejectIdsExpiringIn` (`Duration?`), `rejectNotRealIdCompliant`, `rejectForgedAamvaBarcodes`, `rejectInconsistentData`, `rejectHolderBelowAge` (`Int?`), `anonymizationMode` (`IdAnonymizationMode`); methods `setIncludeImage(_:for:)` / `includeImage(for:)`, `addAnonymizedField(_:forDocument:)`, `removeAnonymizedField(_:forDocument:)`.
- **`IdCaptureScanner`** — `IdCaptureScanner(physicalDocument: (any PhysicalDocumentScanner)?)` and `IdCaptureScanner(physicalDocument:mobileDocument:)`; `physicalDocument` / `mobileDocument` properties.
- **Physical scanners**: `FullDocumentScanner()` — both sides, all zones; `SingleSideScanner(enablingBarcode:machineReadableZone:visualInspectionZone:)` — single side, selected zones; props `barcode` / `machineReadableZone` / `visualInspectionZone`.
- **`MobileDocumentScanner`** — `MobileDocumentScanner(enablingIso180135:ocr:)`; `iso180135` / `ocr` props. `iso180135` uses ISO 18013-5 QR + Bluetooth handover; `ocr` reads a mobile document displayed on another device's screen.
- **Document types** (`IdCaptureDocument` protocol, props `region: IdCaptureRegion` + `documentType: IdCaptureDocumentType`): `IdCard(region:)`, `DriverLicense(region:)`, `Passport(region:)`, `VisaIcao(region:)`, `ResidencePermit(region:)`, `HealthInsuranceCard(region:)`, `RegionSpecific(subtype: RegionSpecificSubtype)`.
- **`IdCaptureRegion`** enum — `.any`, `.euAndSchengen`, and ~250 region values (`.us`, `.uk`, `.uae`, `.germany`, …).
- **`IdCaptureListener`** protocol — `idCapture(_:didCapture:)` (required), `idCapture(_:didReject:reason:)` (required).
- **`CapturedId`** — `fullName` / `firstName` / `lastName` (`String?`), `sex` / `sexType`, `dateOfBirth` / `dateOfExpiry` / `dateOfIssue` (`DateResult?`), `nationality` / `nationalityISO`, `address`, `age` (`Int?`), `isExpired`, `document` (`(any IdCaptureDocument)?`), `issuingCountry` (`IdCaptureRegion`), `documentNumber` / `documentAdditionalNumber`, `vizResult` / `mrzResult` / `barcode` / `mobileDocumentResult` / `mobileDocumentOcrResult`, `images` (`IdImages`), `verificationResult` (`VerificationResult`), `usRealIdStatus`.
- **`DateResult`** — `day` / `month` / `year` (`Int`).
- **`IdImages`** — `face` (`UIImage?`), `frame` (`UIImage?`), `croppedDocument(side:)` (`UIImage?`).
- **`VerificationResult`** — `dataConsistency` (`DataConsistencyResult?`), `aamvaBarcodeVerification` (`AamvaBarcodeVerificationResult?`).
- **`DataConsistencyResult`** — `allChecksPassed`, `frontReviewImage` (`UIImage?`).
- **`AamvaBarcodeVerificationResult`** — `status` (`AamvaBarcodeVerificationStatus`: `.authentic` / `.likelyForged` / `.forged`).
- **`IdCaptureOverlay`** — `IdCaptureOverlay(idCapture:view:)`; `idLayoutStyle` (`IdLayoutStyle`: `.rounded` / `.square`), `idLayoutLineStyle` (`IdLayoutLineStyle`: `.bold` / `.light`), `showTextHints`, `textHintPosition`, `setFrontSideTextHint(_:)` / `setBackSideTextHint(_:)`, `capturedBrush` / `localizedBrush` / `rejectedBrush`.
- **`IdCaptureFeedback`** — `IdCaptureFeedback()`; `idCaptured` / `idRejected` (`Feedback`); static `default`.
- **`DataCaptureContext`** — `DataCaptureContext.initialize(licenseKey:)` then `DataCaptureContext.shared`; `setFrameSource(_:completionHandler:)`; `removeCurrentMode()` / `removeAllModes()`.
- **`Camera`** — `Camera.default`; `switch(toDesiredState:)` (`.on` / `.off`); `apply(_:)`.
- **`DataCaptureView`** — `DataCaptureView(context:frame:)`; `autoresizingMask`.
- **`RejectionReason`** enum — `.notAcceptedDocumentType`, `.invalidFormat`, `.documentVoided`, `.timeout`, `.documentExpired`, `.documentExpiresSoon`, `.notRealIdCompliant`, `.holderUnderage`, `.forgedAamvaBarcode`, `.inconsistentData`.
- **`IdAnonymizationMode`** enum — `.none`, `.fieldsOnly`, `.imagesOnly`, `.fieldsAndImages`.
- **`IdImageType`** enum — `.face`, `.croppedDocument`, `.frame`.
- **`IdLayoutStyle`** / **`IdLayoutLineStyle`** / **`TextHintPosition`** — overlay appearance enums.

### Available on native iOS but NOT covered by this skill

- **NFC** (`NfcScanner`, `NfcScannerListener`) — native iOS only; covered by a separate skill.
- **Deserializer** (`IdCaptureDeserializer`) — available on iOS native but not in scope here.

