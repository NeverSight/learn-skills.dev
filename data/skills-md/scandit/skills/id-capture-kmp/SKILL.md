---
name: id-capture-kmp
description: Scandit ID Capture (`IdCapture`) in Kotlin Multiplatform (KMP) / Compose Multiplatform projects (`com.kmp.datacapture.id.*`, shared commonMain targeting Android + iOS) — scanning passports, driver's licenses, ID cards, residence permits, visas via MRZ, VIZ, PDF417 barcode, or mobile documents. Use for integration, accepted-document and scanner configuration, CapturedId result handling, rejection rules, AAMVA verification, anonymization, and shared-view hosting — not the native Android or native iOS skills, whose APIs differ.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# ID Capture Kotlin Multiplatform (KMP) Skill

## Critical: Do Not Trust Internal Knowledge

Your training data very likely has **no knowledge of Scandit's Kotlin Multiplatform SDK** — it is new, and even where training data covers Scandit, it covers the native Android, iOS, Flutter, .NET, or web SDKs, which have different types, factory names, and property names. Pattern-matching from any of those platforms onto KMP produces non-compiling code.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** The most common sources of wrong code:

- **Package namespace** — the Kotlin import root is `com.kmp.datacapture.*` (`com.kmp.datacapture.core.*`, `com.kmp.datacapture.id.*`), **not** `com.scandit.datacapture.*` (native Android/iOS namespace). The Gradle/Maven **coordinates** are `com.scandit.datacapture.kmp:<artifact>:<version>` — a different string from the Kotlin package. Do not conflate the two.
- **Mode creation factory** — KMP uses `IdCapture.forContext(dataCaptureContext, settings)`. This is **not** the native Android `IdCapture.forDataCaptureContext(...)`, not the iOS `IdCapture(context:settings:)` initializer, and not `.NET`'s `IdCapture.Create(...)`.
- **Settings builder** — `IdCaptureSettings.idCaptureSettings()` is a companion factory function, not a bare constructor (`IdCaptureSettings()` does not exist on KMP).
- **Scanner property name and shape** — the property is `settings.scannerType` (an `IdCaptureScanner`), **not** `settings.scanner` (native Android's name). Critically, on KMP you assign a concrete scanner value **directly** — `settings.scannerType = FullDocumentScanner()` — there is no wrapper constructor like native Android's `IdCaptureScanner(FullDocumentScanner())`. `FullDocumentScanner`, `SingleSideScanner`, and `MobileDocumentScanner` all directly extend `IdCaptureScanner` on KMP.
- **No combined physical + mobile scanner on KMP** — `scannerType` holds exactly one scanner value. Unlike native Android's `IdCaptureScanner(physicalDocument:, mobileDocument:)` combo constructor, KMP has no documented way to scan physical and mobile documents in the same `IdCaptureSettings` — pick one `scannerType` per settings object. If a user asks for both simultaneously, say this is not available on KMP rather than inventing a combined constructor.
- **`SingleSideScanner` has a 4th parameter on KMP** — `SingleSideScanner(barcode: Boolean, machineReadableZone: Boolean, visualInspectionZone: Boolean, freeFormText: Boolean = false)`. The `freeFormText` parameter is KMP-specific.
- **Result property naming drift from native Android** — `capturedId.sexType` (a `Sex` enum: `FEMALE` / `MALE` / `UNSPECIFIED`), not `capturedId.sex`. Zone results are `capturedId.mrz` / `.viz` / `.barcode` / `.mobileDocument` / `.mobileDocumentOcr` — never `mrzResult`/`vizResult`/`barcodeResult`.
- **Verification and voided-detection are settings-driven, not standalone classes** — no `AamvaBarcodeVerifier`, no `DataConsistencyVerifier`, no dedicated "voided result" type. Set `settings.rejectForgedAamvaBarcodes` / `rejectInconsistentData` / `rejectVoidedIds` and read `capturedId.verificationResult` (for AAMVA/consistency) or the `RejectionReason.DOCUMENT_VOIDED` case (for voided detection).
- **Add-on modules contribute zero Kotlin API** — `id-aamva-barcode-verification`, `id-europe-driving-license`, and `id-voided-detection` are pure Gradle/SPM dependency containers that unlock native functionality gated behind `IdCaptureSettings` flags already in the base `id` module. Do not invent imports like `com.kmp.datacapture.idAamvaBarcodeVerification.SomeClass` — there is nothing to import from them.
- **Overlay factories** — `IdCaptureOverlay.withIdCapture(idCapture)` / `IdCaptureOverlay.withIdCaptureForView(idCapture, view)`. Not `.newInstance(...)` (native Android) and not a constructor.
- **Enum casing** — `UPPER_SNAKE_CASE` throughout: `IdCaptureRegion.ANY`, `RejectionReason.DOCUMENT_EXPIRED`, `IdAnonymizationMode.FIELDS_AND_IMAGES`, `IdLayoutStyle.ROUNDED` — never Swift-style `.any` / `.documentExpired`.
- **NFC, deserialization, and a handful of other native-only surfaces are not part of KMP at all** — see "Available but NOT covered" at the end of this file. Don't suggest them; they don't exist on this SDK.

### Forbidden APIs (commonly hallucinated — do NOT emit these)

| Do NOT write | Use instead |
|---|---|
| `IdCapture.forDataCaptureContext(context, settings)` (native Android) / `IdCapture(context:settings:)` (iOS) / `IdCapture.Create(...)` (.NET) | `IdCapture.forContext(dataCaptureContext, settings)` |
| `IdCaptureSettings()` (bare constructor) | `IdCaptureSettings.idCaptureSettings()` |
| `settings.scanner = IdCaptureScanner(FullDocumentScanner())` (native Android wrapper style) | `settings.scannerType = FullDocumentScanner()` |
| `settings.scanner = IdCaptureScanner(physicalDocument = ..., mobileDocument = ...)` (combined scanner) | Not available on KMP — pick one `scannerType` value |
| `IdCaptureOverlay.newInstance(idCapture, dataCaptureView)` (native Android) | `IdCaptureOverlay.withIdCaptureForView(idCapture, dataCaptureView)` or `IdCaptureOverlay.withIdCapture(idCapture)` |
| `capturedId.sex` | `capturedId.sexType` (a `Sex` enum) |
| `capturedId.mrzResult` / `.vizResult` / `.barcodeResult` | `capturedId.mrz` / `.viz` / `.barcode` |
| `AamvaBarcodeVerifier(...)` / `DataConsistencyVerifier(...)` | `settings.rejectForgedAamvaBarcodes` / `settings.rejectInconsistentData`, then read `capturedId.verificationResult` |
| `import com.kmp.datacapture.idAamvaBarcodeVerification.*` or similarly named add-on imports | Nothing to import — add the Gradle/SPM dependency only, then use the base-module `IdCaptureSettings` flags |
| `IdCaptureRegion.Any` / `.us` / `RejectionReason.documentExpired` (camelCase) | `IdCaptureRegion.ANY` / `IdCaptureRegion.US` / `RejectionReason.DOCUMENT_EXPIRED` |
| `DataCaptureContext.forLicenseKey(key)` as the primary pattern | `DataCaptureContext.initialize("...")` (the pattern used by the official KMP samples; `forLicenseKey` also exists but is not the canonical sample form) |
| `com.scandit.datacapture.id.*` imports | `com.kmp.datacapture.id.*` (Kotlin package differs from the Maven group) |

## Product Guidance

- **This is a shared-code SDK — most logic belongs in `commonMain`.** `DataCaptureContext`, `IdCaptureSettings`, `IdCapture`, `IdCaptureListener`, and the `DataCaptureView` setup all live in a shared `ScreenModel`/view-model class in `commonMain`. Only the thin hosting code (embedding the native view, driving lifecycle events) differs between `androidApp` and `iosApp`.
- **Accept only the documents you actually need.** Ask which document types and regions. Documents not in `acceptedDocuments` are rejected with `RejectionReason.NOT_ACCEPTED_DOCUMENT_TYPE`.
- **Pick the scanner that matches the data you need.** `FullDocumentScanner()` for both sides/all zones, `SingleSideScanner(...)` for a specific zone, `MobileDocumentScanner(...)` for mDL/ISO 18013-5. See `references/integration.md`.
- **Handle `onIdRejected`, not just `onIdCaptured`.** Give the user a distinct message per `RejectionReason`.
- **Both listener callbacks may run off the main thread on the native side** — dispatch UI-affecting state changes through the shared `StateFlow`/`ScreenModel` pattern shown in `references/integration.md`, the same way the official samples do, rather than mutating UI state directly from the callback.
- **AAMVA verification, EU driving-license back-decoding, and voided-document detection each require an extra Gradle/SPM dependency** in addition to the base `id` artifact — the add-on module exists purely to link the native detection library; the Kotlin API is entirely on the base `IdCaptureSettings`/`CapturedId`. Forgetting the add-on dependency means the settings flag has no effect at runtime.
- **iOS ships as a single umbrella SPM package** (`Scandit/datacapture-kmp-spm`) — pick one variant that includes `id` (and any add-ons you use); an app can only link one Scandit KMP Kotlin framework.
- **Hand off to a different skill for non-ID-Capture questions.** If the user asks about Barcode Capture, SparkScan, MatrixScan, or Label Capture on KMP, or about native Android/iOS ID Capture, defer to the appropriate skill.

## Intent Routing

Based on the user's request, load `references/integration.md` and follow it. It covers:

- Prerequisites (Gradle/SPM dependencies, license key, camera permissions)
- Minimal integration (shared `DataCaptureContext` → `IdCaptureSettings` → `IdCapture` → `DataCaptureView`/`IdCaptureOverlay` → Android/iOS hosting)
- Scanner types and accepted/rejected documents
- Handling results (`CapturedId`) and rejection (`RejectionReason`)
- Feedback and overlay customization
- AAMVA/USDL verification and data-consistency checks (the `id-aamva-barcode-verification` add-on)
- EU driving-license back decoding (the `id-europe-driving-license` add-on)
- Voided-document detection (the `id-voided-detection` add-on)
- The Compose Multiplatform `IdCaptureView` composable (the `id-compose` module)
- Lifecycle and teardown
- Pitfalls specific to this platform

This is an integration-only skill — there is no separate migration guide because the KMP SDK has no prior major version to migrate from.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below or verified in `references/integration.md`. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how to call it — or if a compile error occurs — fetch the relevant documentation page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the Get Started / Advanced page (see the References table below), extract the actual link, and follow that.

URL structures vary and guessing will lead to 404s.

## References

| Topic | Resource |
|---|---|
| ID Capture overview (KMP) | [Intro](https://docs.scandit.com/sdks/kmp/id-capture/intro/) |
| Get Started (KMP) | [Get Started](https://docs.scandit.com/sdks/kmp/id-capture/get-started/) |
| Full integration guide | `references/integration.md` |
| Advanced (scanner modes, verification, Compose) | [Advanced Configurations](https://docs.scandit.com/sdks/kmp/id-capture/advanced/) |
| Supported documents | [Supported Documents](https://docs.scandit.com/sdks/kmp/id-capture/supported-documents/) |
| Core concepts (context, camera, views, Compose) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |

## API surface this skill covers

Covers the KMP ID Capture surface as of **8.6**, the release it shipped in (all classes below are
annotated `kmp=8.6` in the SDK docs). Later versions add to this surface rather than replacing it —
check the linked reference pages for anything not listed here.

- **`IdCapture`** — `IdCapture.forContext(dataCaptureContext: DataCaptureContext?, settings: IdCaptureSettings): IdCapture`; `isEnabled: Boolean`; `dataCaptureContext: DataCaptureContext?` (read-only); `feedback: IdCaptureFeedback`; `externalTransactionId: String?`; `addListener(listener)` / `removeListener(listener)`; `applySettings(settings)`; `reset()`; static `createRecommendedCameraSettings(): CameraSettings`.
- **`IdCaptureSettings`** — factory `IdCaptureSettings.idCaptureSettings()`; properties `scannerType: IdCaptureScanner`, `acceptedDocuments` / `rejectedDocuments: List<IdCaptureDocument>`, `rejectExpiredIds`, `rejectIdsExpiringIn: Duration?`, `rejectVoidedIds`, `rejectHolderBelowAge: Int?`, `rejectionTimeoutSeconds: Int`, `rejectNotRealIdCompliant`, `rejectForgedAamvaBarcodes`, `rejectInconsistentData`, `decodeBackOfEuropeanDrivingLicense`, `anonymizationMode: IdAnonymizationMode`, `anonymizeDefaultFields`; methods `setShouldPassImageTypeToResult(type, value)` / `getShouldPassImageTypeToResult(type)`, `addAnonymizedField(document, fieldType)` / `removeAnonymizedField(...)` / `clearAnonymizedFields()`.
- **`IdCaptureScanner`** — base type of the three scanner classes. `FullDocumentScanner()` — no parameters, both sides/all zones. `SingleSideScanner(barcode: Boolean = true, machineReadableZone: Boolean = true, visualInspectionZone: Boolean = true, freeFormText: Boolean = false)`. `MobileDocumentScanner(iso180135: Boolean = false, ocr: Boolean = false, elementsToRetain: Set<MobileDocumentDataElement> = emptySet())` (or `MobileDocumentScanner.mobileDocumentScanner()`).
- **Document types** (`IdCaptureDocument`, each takes a single `region: IdCaptureRegion`): `IdCard`, `DriverLicense`, `Passport`, `VisaIcao`, `VisaLetter`, `ResidencePermit`, `HealthInsuranceCard`; `RegionSpecific(subtype: RegionSpecificSubtype)`.
- **`IdCaptureRegion`** enum — `ANY`, `EU_AND_SCHENGEN`, and ~250 region values (`US`, `UK`, `UAE`, …), all `UPPER_SNAKE_CASE`.
- **`IdCaptureListener`** — `onIdCaptured(mode: IdCapture, id: CapturedId)`, `onIdRejected(mode: IdCapture, id: CapturedId?, reason: RejectionReason)`.
- **`CapturedId`** — `fullName` / `firstName` / `lastName` (`String?`), `sexType` (`Sex`), `dateOfBirth` / `dateOfExpiry` / `dateOfIssue` (`DateResult?`), `nationality`, `address`, `age` (`Int?`), `isExpired: Boolean?`, `document` (`IdCaptureDocument?`), `issuingCountry` (`IdCaptureRegion`), `documentNumber` / `documentAdditionalNumber`, `usRealIdStatus`, `isCitizenPassport`, `viz` / `mrz` / `barcode` / `mobileDocument` / `mobileDocumentOcr`, `images` (`IdImages`), `verificationResult` (`VerificationResult?`), `anonymizedFields` (`Set<IdFieldType>`) / `isAnonymized(field)`, plus `isIdCard()` / `isDriverLicense()` / `isPassport()` / `isVisaIcao()` / `isVisaLetter()` / `isResidencePermit()` / `isHealthInsuranceCard()` / `isRegionSpecific(subtype)`.
- **`DateResult`** — `day: Int?`, `month: Int?`, `year: Int`.
- **`IdImages`** — `face: CapturedImage?` (property), `frame: CapturedImage?` (property, side-agnostic) and `frame(side: IdSide): CapturedImage?` (function, per-side), `croppedDocument(side: IdSide): CapturedImage?`.
- **`VerificationResult`** — `dataConsistency: DataConsistencyResult?`, `aamvaBarcodeVerification: AamvaBarcodeVerificationResult?`.
- **`DataConsistencyResult`** — `allChecksPassed: Boolean`, `passedChecks` / `skippedChecks` / `failedChecks: Set<DataConsistencyCheck>`, `frontReviewImage: CapturedImage?`.
- **`AamvaBarcodeVerificationResult`** — `allChecksPassed: Boolean`, `status: AamvaBarcodeVerificationStatus` (`AUTHENTIC` / `LIKELY_FORGED` / `FORGED`).
- **`IdCaptureOverlay`** — `IdCaptureOverlay.withIdCapture(idCapture)` / `.withIdCaptureForView(idCapture, view)`; `idLayoutStyle` (`IdLayoutStyle`: `ROUNDED` default / `SQUARE`), `idLayoutLineStyle` (`IdLayoutLineStyle`: `LIGHT` default / `BOLD`), `textHintPosition` (`TextHintPosition`: `ABOVE_VIEWFINDER` / `BELOW_VIEWFINDER`), `showTextHints`, `setFrontSideTextHint(text)` / `setBackSideTextHint(text)`, `capturedBrush` / `localizedBrush` / `rejectedBrush` (`Brush`).
- **`IdCaptureFeedback`** — `IdCaptureFeedback()`; `idCaptured` / `idRejected` (`Feedback`); static `defaultFeedback()`.
- **`DataCaptureContext`** — `DataCaptureContext.initialize(licenseKey, ...)` (also `forLicenseKey(...)` and related overloads); `setFrameSource(frameSource)`; `addMode(mode)` / `removeMode(mode)` / `removeCurrentMode()` / `removeAllModes()`; static `sharedInstance`.
- **`Camera`** — `Camera.getDefaultCamera(settings: CameraSettings): Camera?` (nullable — no camera on some devices); `switchToDesiredState(FrameSourceState.ON / OFF, callback)`.
- **`DataCaptureView`** — hosted per-platform; expose it to the UI layer via the `toAndroidView()` / `toUIView()` extension functions shown in `references/integration.md`; `addOverlay(overlay)`; `logoStyle` (`LogoStyle`).
- **`RejectionReason`** enum — `NOT_ACCEPTED_DOCUMENT_TYPE`, `INVALID_FORMAT`, `DOCUMENT_VOIDED`, `TIMEOUT`, `SINGLE_IMAGE_NOT_RECOGNIZED`, `DOCUMENT_EXPIRED`, `DOCUMENT_EXPIRES_SOON`, `NOT_REAL_ID_COMPLIANT`, `HOLDER_UNDERAGE`, `FORGED_AAMVA_BARCODE`, `INCONSISTENT_DATA`, `BLUETOOTH_COMMUNICATION_ERROR`, `BLUETOOTH_UNAVAILABLE`, `CLOUD_REQUEST_FAILED`.
- **`IdAnonymizationMode`** enum — `NONE`, `FIELDS_ONLY` (default), `IMAGES_ONLY`, `FIELDS_AND_IMAGES`.
- **`IdImageType`** enum — `FACE`, `CROPPED_DOCUMENT`, `FRAME`. **`IdSide`** enum — `FRONT`, `BACK`. **`Sex`** enum — `FEMALE`, `MALE`, `UNSPECIFIED`.
- **Compose Multiplatform** (`id-compose` module) — `@Composable IdCaptureView(settings, modifier, overlayStyle, onCapture, onReject, ...)`. See `references/integration.md` for details.

### Available on the KMP SDK but NOT covered by this skill

- **NFC** chip reading — not part of the KMP SDK (`nfc/nfc-scanner.rst` and `nfc/nfc-result.rst` do not include `kmp` in their platform list).
- **`IdCaptureException`**, **`LocalizedOnlyId`**, **`PhysicalDocumentScanner`** (the standalone base-class page, distinct from the concrete scanners covered above), and the **deserialization API** (`IdCaptureDeserializer` / `IdCaptureDeserializerListener`) — none apply to KMP per the SDK documentation's platform filters.
