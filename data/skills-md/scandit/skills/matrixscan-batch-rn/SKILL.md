---
name: matrixscan-batch-rn
description: MatrixScan Batch (MatrixScan, BarcodeBatch, legacy BarcodeTracking) in React Native projects — tracking and scanning multiple barcodes at once. Use for integration, settings and symbologies, tracked-barcode handling, per-barcode brushes, advanced-overlay AR annotations, tap handling, manual feedback, lifecycle, third-party scanner replacement, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Batch React Native Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeBatch* API surface changes between major SDK versions — constructor signatures, overlay constructors, and listener shapes have all evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names.

React Native-specific gotchas worth flagging:

- `DataCaptureContext.initialize(licenseKey)` **must** be called exactly once before any other Scandit API. It sets up `DataCaptureContext.sharedInstance`. Do not construct multiple contexts.
- `dataCaptureContext.setMode(barcodeBatch)` is how the mode is registered in the context (confirmed from all RN samples). This replaces any previously active mode.
- `dataCaptureContext.removeMode(barcodeBatch)` is the cleanup call — use it in the `useEffect` cleanup function.
- `new BarcodeBatch(settings)` and `new BarcodeBatchBasicOverlay(mode, style)` and `new BarcodeBatchAdvancedOverlay(mode)` constructors (without a context argument) are available from react-native=7.6.
- `BarcodeBatch.createRecommendedCameraSettings()` is available from react-native=7.6.
- Overlays must be added to a `DataCaptureView` via `view.addOverlay(overlay)` inside the `DataCaptureView` `ref` callback.
- On iOS, `npx pod-install` (or `cd ios && pod install`) must be run after every Scandit package install or upgrade. Android auto-links via Gradle.
- Metro's bundler cache frequently masks Scandit package upgrades. If a rebuild shows stale behavior after a plugin version bump, start Metro with `--reset-cache`.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/<App>/Info.plist`) and Android (runtime request via `PermissionsAndroid`).
- **New Architecture caveat (react-native ≥ 0.79, iOS)**: When using the new React Native architecture (Fabric / TurboModules), iOS apps must have the `AppDelegate` implement the `ScanditReactNativeFactoryContainer` protocol (available in the core module) when using `BarcodeBatchAdvancedOverlay`. See integration.md for details.
- **MatrixScan AR add-on required**: `BarcodeBatchAdvancedOverlay`, `BarcodeBatchBasicOverlayListener.brushForTrackedBarcode`, and `BarcodeBatchBasicOverlay.setBrushForTrackedBarcode` all require the MatrixScan AR add-on to be licensed.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Batch from scratch** (e.g. "add MatrixScan to my app", "set up BarcodeBatch", "track multiple barcodes simultaneously", "read the tracked barcode data / identifier / location", "handle taps on highlights or AR views", "emit feedback / beep on a new barcode", "show AR overlays", "per-barcode brushes", "lifecycle or cleanup", "camera permissions") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Replacing a third-party multi-barcode scanner with MatrixScan Batch** (e.g. "replace my react-native-vision-camera useCodeScanner with MatrixScan Batch", "migrate from VisionCamera multi-barcode scanning to Scandit", "switch from RNCamera / ML Kit batch scanning to BarcodeBatch") → read [references/third-party-migration.md](references/third-party-migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called, fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the API index, extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

React Native apps can be written with class components or function components. Examples in this skill use **function components with hooks** because they match the current React Native convention. Write new BarcodeBatch integration code as function components — use `useRef`, `useEffect`, `useCallback`.

Examples are in **TypeScript** (`.tsx`). If the target project is plain JavaScript (`.js` / `.jsx`), drop the type annotations and keep the same imports and structure.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| React Native get started | [Get Started](https://docs.scandit.com/sdks/react-native/matrixscan/get-started/) |
| React Native AR overlays | [Adding AR Overlays](https://docs.scandit.com/sdks/react-native/matrixscan/advanced/) |
| Full API reference | [BarcodeBatch API](https://docs.scandit.com/data-capture-sdk/react-native/barcode-capture/api.html) |
