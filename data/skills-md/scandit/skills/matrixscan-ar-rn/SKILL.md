---
name: matrixscan-ar-rn
description: MatrixScan AR (Barcode AR, BarcodeAr) in React Native projects — scanning multiple barcodes at once with AR overlays, highlights, and annotations on tracked barcodes. Use for integration, symbology configuration, highlight and annotation providers, session handling, feedback, migration from BarcodeBatch, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# MatrixScan AR React Native Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The BarcodeAr* API surface changes significantly between major SDK versions — classes get renamed, constructor signatures change, properties are restructured, and the React Native plugin surface (imports, native linking, pod install, package names) has also evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

React Native-specific gotchas worth flagging:

- `DataCaptureContext.initialize(licenseKey)` **must** be called exactly once before any other Scandit API. It sets up `DataCaptureContext.sharedInstance`, which is the singleton everything else reads from. Do not construct multiple contexts.
- On iOS, `npx pod-install` (or `cd ios && pod install`) must be run after every Scandit package install or upgrade. Android auto-links via Gradle — no manual step there.
- Metro's bundler cache frequently masks Scandit package upgrades. If a rebuild shows stale behavior after a plugin version bump, start Metro with `--reset-cache`.
- `BarcodeArView` is a React component that **wraps** its children — the native AR overlay renders on top of your JSX tree. Children render under the native AR layer. Do not render `BarcodeArView` as a sibling to the content that should appear under the overlay.
- Highlight providers (`BarcodeArHighlightProvider.highlightForBarcode`) and annotation providers (`BarcodeArAnnotationProvider.annotationForBarcode`) fire **asynchronously, once per barcode**. They are `async` functions that return a Promise resolving to the highlight or annotation object. Do not assume synchronous return.
- `BarcodeArView` must be started explicitly via `view.start()` in the `ref` callback. Unlike SparkScan, the view does not start automatically on mount.
- Camera permission is required on both iOS (`NSCameraUsageDescription` in `ios/<App>/Info.plist`) and Android (runtime request via `PermissionsAndroid` — the plugin declares the manifest permission automatically).
- `BarcodeAr` requires SDK 7.1+. The `new BarcodeAr(settings)` constructor (without a context argument) is available from react-native=7.6. Use `dataCaptureContext.addMode(barcodeAr)` to attach the mode to the context.
- `BarcodeArCustomHighlight` requires SDK 8.0+. `BarcodeArCustomAnnotation` requires SDK 8.1+. `BarcodeArResponsiveAnnotation` requires SDK 8.2+.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating MatrixScan AR from scratch** (e.g. "add MatrixScan AR to my app", "set up Barcode AR", "how do I use BarcodeArView in React Native", "how do I show AR overlays on barcodes", "adding or changing highlights or annotations", "lifecycle, cleanup, or session handling") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating from BarcodeBatch to BarcodeAr** (e.g. "migrate from BarcodeBatch", "convert BarcodeBatch to BarcodeAr", "move from MatrixScan to MatrixScan AR", "replace BarcodeTracking with BarcodeAr", "upgrade my old MatrixScan code to AR") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and package paths (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## Framework variant policy

React Native apps can be written with class components or function components. Examples in this skill use **function components with hooks** because they match the current React Native convention. Even if the target project still contains legacy class components elsewhere, write new MatrixScan AR code as function components — do not rewrite the rest of the app's component style, but keep the BarcodeAr* integration itself on the current idiom (`useRef`, `useEffect`, `useMemo`).

Examples are in **TypeScript** (`.tsx`). If the target project is plain JavaScript (`.js` / `.jsx`), drop the type annotations and keep the same imports and structure.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| React Native integration | [Get Started](https://docs.scandit.com/sdks/react-native/matrixscan-ar/get-started/) |
| Full API reference | [BarcodeAr API](https://docs.scandit.com/data-capture-sdk/react-native/barcode-capture/api.html) |
