---
name: matrixscan-count-rn
description: MatrixScan Count (BarcodeCount) in React Native projects — scandit-react-native-datacapture-barcode package. Multi-barcode counting workflows (scan-and-count, counting against an expected capture list, status overlays) with BarcodeCountView. For Capacitor use matrixscan-count-capacitor. Use for integration, settings and symbology configuration, result handling, UI customization, or troubleshooting counting workflows.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan Count React Native Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCount* API surface changes significantly between major SDK versions — constructor signatures change, new properties are added, and the React Native plugin surface (imports, native linking, pod install, package names) has also evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

React Native-specific gotchas worth flagging:

- `DataCaptureContext.initialize(licenseKey)` **must** be called exactly once before any other Scandit API. It sets up `DataCaptureContext.sharedInstance`, which is the singleton everything else reads from. Do not construct multiple contexts.
- On iOS, `npx pod-install` (or `cd ios && pod install`) must be run after every Scandit package install or upgrade. Android auto-links via Gradle — no manual step there.
- Metro's bundler cache frequently masks Scandit package upgrades. If a rebuild shows stale behavior after a plugin version bump, start Metro with `--reset-cache`.
- `BarcodeCountView` is a React component (rendered as JSX). Pass `barcodeCount` and `context` as props. Do NOT manually attach the view to the context — the props handle that. The view does not require an explicit `start()` call (unlike BarcodeArView).
- `listener` and `uiListener` on `BarcodeCountView` are set imperatively via the `ref` callback: `view.listener = ...` and `view.uiListener = ...`.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/<App>/Info.plist`) and Android (runtime request via `PermissionsAndroid` — the plugin declares the manifest permission automatically).
- The `new BarcodeCount(settings)` constructor (without a context argument) is available from react-native=7.6. Older integrations used `BarcodeCount.forDataCaptureContext(context, settings)`. If the target project is on an older plugin, use the factory. Use `dataCaptureContext.addMode(barcodeCount)` to attach the mode when using the ≥7.6 constructor.
- `BarcodeCountStatusProvider`, `setStatusProvider`, `shouldShowStatusModeButton`, `shouldShowStatusIconsOnScan`, `TextForBarcodesNotInListDetectedHint`, `TextForScreenCleanedUpHint`, `TextForClusteringGestureHint`, `StatusModeButtonAccessibilityLabel/Hint`, `StatusModeButtonContentDescription`: all require react-native=8.3+.
- `BarcodeCountNotInListActionSettings` and `barcodeNotInListActionSettings` on `BarcodeCountView`: require react-native=7.1+.
- `tapToUncountEnabled`: requires react-native=7.0+.
- `enableHardwareTrigger(keyCode)` on Android: requires react-native=7.1+, device API level ≥28.
- `hardwareTriggerEnabled` (iOS volume button trigger): requires react-native=7.1+.
- `BarcodeCountStatusProvider.onStatusRequested(barcodes, callback)` is **callback-based** — do NOT await it. Call `callback.onStatusReady(result)` to deliver the result. The callback pattern is async from the platform's perspective.
- `BarcodeCountSettings.clusteringMode` requires react-native=8.3+.
- `BarcodeCountSettings.disableModeWhenCaptureListCompleted` requires react-native=8.3+.
- `BarcodeCountSession.recognizedBarcodes` (array API) requires react-native=7.0+. The `didScan` callback in `BarcodeCountListener` provides the session.
- `BarcodeCount.createRecommendedCameraSettings()` requires react-native=7.6+.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan Count from scratch** (e.g. "add MatrixScan Count to my app", "set up BarcodeCount", "how do I use BarcodeCountView in React Native", "how do I scan and count multiple barcodes", "scan against a list", "customize the count view", "add status overlays", "lifecycle or cleanup") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating from the old `forDataCaptureContext` factory to the new constructor, or adopting Status/MappingFlow/NotInList APIs** (e.g. "migrate from forDataCaptureContext", "upgrade BarcodeCount constructor", "add status mode", "adopt mapping flow", "enable not-in-list action") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths and guessing will lead to 404s.

## Framework variant policy

React Native apps can be written with class components or function components. Examples in this skill use **function components with hooks** because they match the current React Native convention. Even if the target project still contains legacy class components elsewhere, write new MatrixScan Count code as function components — do not rewrite the rest of the app's component style, but keep the BarcodeCount* integration itself on the current idiom (`useRef`, `useEffect`, `useCallback`).

Examples are in **TypeScript** (`.tsx`). If the target project is plain JavaScript (`.js` / `.jsx`), drop the type annotations and keep the same imports and structure.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| React Native integration | [Get Started](https://docs.scandit.com/sdks/react-native/matrixscan-count/get-started/) |
| Full API reference | [BarcodeCount API](https://docs.scandit.com/data-capture-sdk/react-native/barcode-capture/api.html) |
