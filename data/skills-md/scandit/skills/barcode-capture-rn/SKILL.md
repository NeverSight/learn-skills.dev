---
name: barcode-capture-rn
description: Scandit Barcode Capture (`BarcodeCapture`) in React Native projects — the low-level, full-control single-barcode scanning mode (BarcodeCapture + DataCaptureView + BarcodeCaptureOverlay), without the pre-built SparkScan UI. Use for integration, symbology configuration, result handling, viewfinder and feedback customization, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.3"
---

# BarcodeCapture React Native Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeCapture API changes between major SDK versions — properties get renamed, removed, or restructured, and the React Native plugin surface (imports, native linking, pod install, package names) has also evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

React Native-specific gotchas worth flagging:
- `DataCaptureContext.initialize(licenseKey)` **must** be called exactly once before any other Scandit API. It sets up `DataCaptureContext.sharedInstance`, which is the singleton everything else reads from. Do not construct multiple contexts.
- **Never call `dataCaptureContext.dispose()`.** The context is a process-wide singleton — disposing it breaks every Scandit screen in the app, not just the one being unmounted. On screen unmount call `dataCaptureContext.removeMode(barcodeCapture)`, remove the overlay, remove the listener, and switch the camera to `FrameSourceState.Off`. That is the complete cleanup; do not add `dispose()`.
- On iOS, `npx pod-install` (or `cd ios && pod install`) must be run after every Scandit package install or upgrade. Android auto-links via Gradle — no manual step there.
- Metro's bundler cache frequently masks Scandit package upgrades. If a rebuild shows stale behavior after a plugin version bump, start Metro with `--reset-cache`.
- BarcodeCapture is **not** a self-contained view component. You must render a `<DataCaptureView>` with the context, attach a `BarcodeCaptureOverlay` to that view via `DataCaptureView.addOverlay(...)`, and drive the camera yourself with `Camera.default` + `dataCaptureContext.setFrameSource(camera)` + `camera.switchToDesiredState(FrameSourceState.On)`. Tearing all of that down on unmount is the integrator's responsibility.
- Inside `didScan`, set `barcodeCapture.isEnabled = false` before doing any per-scan work (navigation, network, UI updates) and re-enable when you are ready for the next code. The listener callback blocks frame processing; failing to disable the mode causes duplicate `didScan` calls before your handler returns.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/<App>/Info.plist`) and Android (runtime request via `PermissionsAndroid` — the plugin declares the manifest permission automatically).

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating BarcodeCapture from scratch** (e.g. "add BarcodeCapture to my app", "set up barcode scanning", "how do I use BarcodeCapture in React Native", "how do I add a viewfinder") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing BarcodeCapture integration** (e.g. "upgrade from v6 to v7", "migrate my BarcodeCapture", "bump the Scandit packages to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## Framework variant policy

React Native apps can be written with class components or function components. Examples in this skill use **function components with hooks** because they match the official React Native samples and the current React Native convention. Even if the target project still contains legacy class components elsewhere, write new BarcodeCapture code as function components — do not rewrite the rest of the app's component style, but keep the BarcodeCapture integration itself on the current idiom (`useRef`, `useEffect`, `useFocusEffect`, `useMemo`).

Examples are in **TypeScript** (`.tsx`). If the target project is plain JavaScript (`.js` / `.jsx`), drop the type annotations and keep the same imports and structure.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| React Native integration | [Get Started](https://docs.scandit.com/sdks/react-native/barcode-capture/get-started/) · [Samples](https://github.com/Scandit/datacapture-react-native-samples) |
| Advanced topics (custom viewfinder, location selection, scan intention, composite codes, feedback) | [Advanced Configurations](https://docs.scandit.com/sdks/react-native/barcode-capture/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/react-native/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/react-native/migrate-7-to-8/) |
| Full API reference | [BarcodeCapture API](https://docs.scandit.com/data-capture-sdk/react-native/barcode-capture/api.html) |
