---
name: id-capture-rn
description: Scandit ID Capture (`IdCapture`) in React Native projects — scanning passports, driver's licenses, ID cards, residence permits, visas via MRZ, VIZ, barcode, or mobile documents. Use for integration, accepted-document and scanner configuration, captured-field result handling, anonymization, add-on capabilities (voided-ID detection, European driving-license back decoding, AAMVA barcode verification), and SDK version migration.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# ID Capture React Native Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit ID Capture APIs. The ID Capture API was **restructured at the v7 → v8 boundary** (the `scannerType` property was renamed to `scanner` and reshaped into a wrapper, the standalone `AamvaBarcodeVerifier` was removed in favour of settings flags, and several verification APIs were added). The React Native plugin surface (package names, enum casing, view component, AppState lifecycle) is also distinct from the iOS, Android, web, Flutter, Cordova, and Capacitor SDKs.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, package names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

React Native–specific gotchas worth flagging:

- **No plugin init call.** Unlike Flutter, you do **not** call `ScanditDataCaptureId.initialize()`. The core auto-initializes at import time. The only "initialize" call is `DataCaptureContext.initialize(licenseKey)` followed by using `DataCaptureContext.sharedInstance` — that is the RN convention.
- **Enums use PascalCase member names with camelCase wire values.** Write `IdCaptureRegion.Us`, `IdImageType.CroppedDocument`, `IdSide.Front`, `RejectionReason.Timeout`, `IdAnonymizationMode.FieldsAndImages`, `IdFieldType.DocumentNumber`, `IdLayoutStyle.Rounded`, `FrameSourceState.On` / `.Off`. **Never** write the lowercase Dart/Flutter form (`IdCaptureRegion.us`) on RN.
- **`CapturedId` MRZ/VIZ getters are `mrzResult` / `vizResult`** (not `mrz` / `viz` — that's Flutter). Other source-specific getters: `barcode`, `mobileDocument`, `mobileDocumentOcr`.
- **Images come back as base64 strings.** `images.face`, `images.frame`, `images.getCroppedDocument(IdSide.Front)`, `images.getFrame(IdSide.Front)` each return a `string | null`. Render with `<Image source={{ uri: 'data:image/png;base64,' + face }} />`. **They are not URIs, files, or Image components.**
- **Listener is a plain object literal.** `IdCaptureListener` is a TypeScript interface with two optional methods — write `const listener = { didCaptureId(_, captured) {...}, didRejectId(_, rejected, reason) {...} }`. Do **not** create a class with `implements IdCaptureListener` — that's the Dart/Flutter style.
- **`addListener`, `removeListener`, `setMode`, `addMode`, `removeMode`, `applySettings`, `setFrameSource`, `switchToDesiredState` all return Promises.** Either `await` them or chain `.then` — forgetting the `await` is a common cause of races at startup.
- **Two view patterns ship.** The official sample wires `<DataCaptureView>` from `scandit-react-native-datacapture-core` + manually adds an `IdCaptureOverlay` through a ref. The id package also ships a higher-level `<IdCaptureView>` component that bundles mode + camera + overlay + callbacks behind props. Both are valid; lead with `<DataCaptureView>` (matches the public sample) and offer `<IdCaptureView>` as a shorthand. See [references/integration.md](references/integration.md).
- **There is no `VisaLetter` document class on React Native.** Only `VisaIcao` ships. (On Flutter both exist; on RN only the ICAO visa is modelled.)
- **Camera lifecycle uses `AppState`, not focus props.** Subscribe with `AppState.addEventListener('change', …)`, stop the camera on `background`/`inactive`, restart on `active`, and gate the resume on `navigation.isFocused()` if the screen is part of a stack navigator.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/<App>/Info.plist`) and Android (use RN's built-in `PermissionsAndroid` API to request `CAMERA` at runtime). The native manifest permission is declared by the plugin.

### Forbidden APIs (commonly hallucinated — do NOT emit these)

These compile-fail against the real RN packages. Use the right-hand form:

| Do NOT write | Use instead |
|---|---|
| `IdCapture.forContext(context, settings)` | `new IdCapture(settings)` then `await context.setMode(idCapture)` |
| `IdCaptureOverlay.withIdCapture(...)` / `.withIdCaptureForView(...)` | `new IdCaptureOverlay(idCapture)` then `view.addOverlay(overlay)` |
| `IdDocumentType` enum / `settings.supportedDocuments` / `settings.scannerType` | `settings.acceptedDocuments` (document classes) + `settings.scanner = new IdCaptureScanner(new FullDocumentScanner())` |
| `capturedId.documentType` | `capturedId.document?.documentType` (`IdCaptureDocumentType`) or `capturedId.isPassport()` / `isDriverLicense()` / … |
| `capturedId.isVisa()` / `capturedId.isVisaLetter()` | `capturedId.isVisaIcao()` (RN ships only the ICAO visa) |
| `capturedId.mrz` / `capturedId.viz` (Flutter names) | `capturedId.mrzResult` / `capturedId.vizResult` |
| `IdCaptureRegion.us` / `IdSide.front` / `AamvaBarcodeVerificationStatus.authentic` (lowercase Dart form) | `IdCaptureRegion.Us` / `IdSide.Front` / `AamvaBarcodeVerificationStatus.Authentic` — **every Scandit enum member on RN is PascalCase**, including `RejectionReason.*`, `IdImageType.*`, `IdAnonymizationMode.*`, `IdFieldType.*`, `FrameSourceState.*`, `IdLayoutStyle.*`, and the verification-status / -reason values |
| `capturedId.images.croppedDocument` | `capturedId.images.getCroppedDocument(IdSide.Front)` (also `.face`, `.frame`, `getFrame(IdSide.Front)`) |
| Treating `images.face` like a URI / file / `Image` component | It's a base64 string — `<Image source={{ uri: 'data:image/png;base64,' + face }} />` |
| `AamvaBarcodeVerifier` (class) | `settings.rejectForgedAamvaBarcodes = true` + `capturedId.verificationResult.aamvaBarcodeVerification` |
| `DrivingLicenseCategory.categoryCode` | `DrivingLicenseCategory.code` (plus `dateOfIssue` / `dateOfExpiry`) |
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

- **Integrating ID Capture from scratch** (e.g. "add ID scanning to my RN app", "scan a passport / driver's license", "read the MRZ", "extract the holder's name and date of birth") → read [references/integration.md](references/integration.md) and follow it.
- **One of the add-on / advanced capabilities** ("reject voided / cancelled IDs", "detect punched-hole / voided licenses", "decode the back of a European driving license", "read vehicle categories", "verify the AAMVA barcode / detect forged US licenses", "reject inconsistent data / data-consistency verification", "scan a mobile driver's license / mDL / ISO 18013-5 mobile document") → read [references/supplementary-modules.md](references/supplementary-modules.md).
- **Migrating or upgrading an existing ID Capture integration** ("upgrade ID Capture to the latest SDK", "migrate v7 to v8", "my `scannerType` code stopped compiling", "`AamvaBarcodeVerifier` is gone", "what changed in ID Capture between versions") → read [references/migration.md](references/migration.md).
- **React Navigation route lifecycle, Expo / dev-client setup, or where to keep the SDK handles** ("camera doesn't stop when I navigate away", "pause the camera on focus/blur", "`useFocusEffect`", "I'm using Expo / Expo Go / Expo Router", "do I need a custom dev client?", "permission with `expo-camera`", "should I put `IdCapture` in Redux / Zustand?") → read [references/framework-recipes.md](references/framework-recipes.md). The Scandit code itself is unchanged from [references/integration.md](references/integration.md); this file covers the React Navigation / Expo / state-management glue.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript compiler / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:

1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

Examples in [references/integration.md](references/integration.md) use **functional components + React hooks** (`useEffect`, `useRef`, `AppState`) because the official `IdCaptureSimpleSample` is written that way. If the project also uses React Navigation, Expo, or wants to share the context across screens, see [references/framework-recipes.md](references/framework-recipes.md) — the Scandit calls are unchanged; only the navigation lifecycle, Expo build flow, and ref-vs-store guidance differ. Do not introduce a new state-management library just for ID Capture.

Examples are in **TypeScript** (the official sample is `.tsx`). React Native `>=0.74` is recommended.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| React Native integration | [Get Started](https://docs.scandit.com/sdks/react-native/id-capture/get-started/) · [Sample (IdCaptureSimpleSample)](https://github.com/Scandit/datacapture-react-native-samples/tree/master/02_ID_Scanning_Samples/IdCaptureSimpleSample) |
| Advanced topics (anonymization, verification, scanners, overlay) | [Advanced Configurations](https://docs.scandit.com/sdks/react-native/id-capture/advanced/) |
| Migration between major SDK versions | [7 → 8](https://docs.scandit.com/sdks/react-native/migrate-7-to-8/) |
| Full API reference | [ID Capture API](https://docs.scandit.com/data-capture-sdk/react-native/id-capture/api.html) |
