---
name: sparkscan-web
description: SparkScan single-barcode scanning with the pre-built scanning UI (floating trigger button, `<spark-scan-view>`) in web/browser projects (`@scandit/web-datacapture-barcode`), including React/Vite/Next.js apps. Use for integration, scan settings, result handling, trigger-button customization, React-specific issues (StrictMode, React 18 vs 19 binding), camera/HTTPS/COOP-COEP troubleshooting, or SDK version migration — not for SparkScan on native or hybrid platforms.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.2.2"
---

# SparkScan Web Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs. The SparkScan API changes significantly between major SDK versions — properties get renamed, removed, or restructured.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** Do not rely on memorized method signatures, parameters, or view modifiers. If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding. More than one may apply (e.g. a React integration that also hits a camera issue) — read all that are relevant:

- **Integrating SparkScan from scratch** (e.g. "add SparkScan to my app", "set up barcode scanning", "how do I use SparkScan", "how do I handle feedback in SparkScan", "I want to build a scanning app") → read [references/integration.md](references/integration.md) and follow the instructions there. If the user has no existing project, the guide will direct you to offer the pre-built sample first.
- **The project uses React** (a `react` dependency in `package.json`, `.tsx`/`.jsx` files, hooks, JSX) → also read [references/react.md](references/react.md). The correct way to bind the `<spark-scan-view>` custom element differs by React major version, so **check the `react` version in `package.json` first** — the guide explains the React 18 vs 19 difference and the context/lifecycle pitfalls. Always consult it before writing React code; the generic `integration.md` example is vanilla TS.
- **Migrating or upgrading an existing SparkScan integration** (e.g. "upgrade from v6 to v7", "migrate my SparkScan", "what changed between SDK versions") → read [references/migration.md](references/migration.md) and follow the instructions there.
- **Runtime, camera, or deployment trouble** (e.g. "camera won't open on my phone", "works for a second then dies", cross-origin/COOP/COEP/header issues, "blank preview over a LAN IP") → read [references/troubleshooting.md](references/troubleshooting.md). These are environment/hosting issues, not API mistakes, and are easy to misdiagnose as code bugs.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or view modifiers. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:

1. First check whether the page you already fetched (e.g. the Advanced Configurations page) contains a direct hyperlink to it — topic pages link directly to relevant API symbols. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table below), extract the actual link from it, and follow that.

URL structures can vary (e.g. `api/ui/` subdirectory) and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Basic integration | [Get Started](https://docs.scandit.com/sdks/web/sparkscan/get-started/) · [Sample](https://github.com/Scandit/datacapture-web-samples/tree/master/01_Single_Scanning_Samples/01_Barcode_Scanning_with_Pre-built_UI/ListBuildingSample) |
| React integration | [Get Started](https://docs.scandit.com/sdks/web/sparkscan/get-started/) · [Sample](https://github.com/Scandit/datacapture-web-samples/tree/master/05_Framework_Integration_Samples/SparkScanReactSample) |
| Advanced topics (custom feedback, hardware triggers, scanning modes, UI customization) | [Advanced Configurations](https://docs.scandit.com/sdks/web/sparkscan/advanced/) |
| Full API reference | [SparkScan API](https://docs.scandit.com/data-capture-sdk/web/barcode-capture/api.html#:~:text=SymbologySettings-,SparkScan,-SparkScan) |
