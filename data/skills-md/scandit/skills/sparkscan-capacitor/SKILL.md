---
name: sparkscan-capacitor
description: Capacitor — SparkScan single-barcode scanning with the pre-built scanning UI in Capacitor (Ionic) hybrid mobile apps via the Scandit Capacitor plugins (`ScanditCaptureCorePlugin`), not the browser-only web SDK. Use for integration, scan settings, result handling, UI customization, SDK version migration, or troubleshooting.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.2"
---

# SparkScan Capacitor Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The SparkScan API changes significantly between major SDK versions — properties get renamed, removed, or restructured, and the Capacitor plugin surface (imports, plugin initialization, native sync steps) has also evolved.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, plugin names, or property names. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

Capacitor-specific gotchas worth flagging:
- `ScanditCaptureCorePlugin.initializePlugins()` **must** be called (and awaited) before any other Scandit API — including `DataCaptureContext` construction. Forgetting this produces runtime errors that look unrelated to initialization.
- `npx cap sync` must be run after every plugin version change to propagate native artifacts into iOS/Android. Skipping it yields a web/native version mismatch at runtime.
- SparkScan renders as a native overlay above the webview — there is no DOM mount point for the scanner. Do not instruct users to add a `<div id="scanner">` container.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Integrating SparkScan from scratch** (e.g. "add SparkScan to my app", "set up barcode scanning", "how do I use SparkScan in Capacitor", "how do I handle feedback in SparkScan") → read [references/integration.md](references/integration.md) and follow the instructions there.
- **Migrating or upgrading an existing SparkScan integration** (e.g. "upgrade from v6 to v7", "migrate my SparkScan", "bump the Scandit plugins to v8", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, property names, or imports. If unsure whether an API exists or how it is called — or if a TypeScript / runtime error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures vary across SDK versions and plugin paths (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## Framework variant policy

Capacitor is a WebView-based framework. Examples in this skill use **plain JavaScript (ES modules)**. TypeScript projects can use the same imports and APIs verbatim — just add types — but this skill does not assume a TypeScript project by default. If the target project is clearly TypeScript (`.ts` files, `tsconfig.json`), adapt the final output to TypeScript syntax; otherwise stay in plain JS.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Capacitor integration | [Get Started](https://docs.scandit.com/sdks/capacitor/sparkscan/get-started/) · [Sample](https://github.com/Scandit/datacapture-capacitor-samples/tree/master/01_Single_Scanning_Samples/01_Barcode_Scanning_with_Pre_Built_UI/ListBuildingSample) |
| Advanced topics (custom feedback, hardware triggers, scanning modes, UI customization) | [Advanced Configurations](https://docs.scandit.com/sdks/capacitor/sparkscan/advanced/) |
| Migration between major SDK versions | [6 → 7](https://docs.scandit.com/sdks/capacitor/migrate-6-to-7/) · [7 → 8](https://docs.scandit.com/sdks/capacitor/migrate-7-to-8/) |
| Full API reference | [SparkScan API](https://docs.scandit.com/data-capture-sdk/capacitor/barcode-capture/api.html) |
