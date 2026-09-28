---
name: matrixscan-find-kmp
description: MatrixScan Find (BarcodeFind) in Kotlin Multiplatform (KMP) projects — com.scandit.datacapture.kmp Maven artifacts, com.kmp.datacapture.barcode.find imports. Search-and-find workflows shared across Android/iOS — build an item list, find specific barcodes among many, BarcodeFindView UI (Compose or base view). Use for integration, item-list setup, result handling, UI customization, lifecycle wiring, or troubleshooting search-and-find workflows.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# MatrixScan Find KMP Skill

## Critical: Do Not Trust Internal Knowledge

Your training data may not contain the Scandit Kotlin Multiplatform (KMP) SDK at all — it is a new SDK (first released at version 8.6) with its own package names (`com.kmp.datacapture.*`), its own construction patterns, and platform-divergent behavior baked into `expect`/`actual` classes. Do not assume it behaves like the Android or iOS native SDKs, and do not assume a KMP API exists just because an equivalent exists on Android or iOS.

**Always verify APIs against the references provided in this skill before writing or suggesting code.** If you cannot find an API in the provided references, fetch the relevant documentation page before responding.

KMP-specific gotchas worth flagging:

- `BarcodeFind` is constructed via the companion factory `BarcodeFind.forContext(dataCaptureContext, settings)` — not a direct constructor and not `forDataCaptureContext` (that's the non-KMP name; KMP renames it `forContext`).
- `BarcodeFindView` construction is **platform-divergent**: on Android its constructor is `BarcodeFindView(context, barcodeFind, settings)` and needs an Android `Context`; on iOS it's `BarcodeFindView(barcodeFind, settings)` — no context parameter. Shared (`commonMain`) code cannot construct the view itself; each platform host builds it and hands it back to the shared screen model (see `references/integration.md`).
- `BarcodeFindView.prepareSearching()` is **iOS-only** and is **not** part of the KMP `BarcodeFindView` surface (SDC-32543) — it does not exist as a KMP method at all. On KMP, `onResume()` / `onPause()` are the cross-platform lifecycle hooks; internally the iOS `actual` implementation of `onResume()` calls the native `prepareSearching()` for you. Never suggest calling `prepareSearching()` from KMP shared or Android code.
- `BarcodeFindView.cameraStateOnStop` and `BarcodeFindView.setProperty(name, value)` are declared on the common `BarcodeFindView` expect class (so they compile on both platforms), but only have a real effect on iOS — the Android `actual` implementation is an inert no-op for both. Don't rely on them to change Android behavior.
- Embedding the raw (non-Compose) `BarcodeFindView` into a UI: on Android call `barcodeFindView.toAndroidView()` (extension function, returns the underlying `android.view.View`); on iOS call `barcodeFindView.toUIView()` (a member function on `BarcodeFindView` itself). These are two different call shapes — don't mix them up.
- `BarcodeFind.setItemList(items: Set<BarcodeFindItem>)` and the whole item-search flow only ever deal in `BarcodeFindItem` / `BarcodeFindItemSearchOptions` / `BarcodeFindItemContent` — never invent a "BarcodeFindItemList" collection type.
- `BarcodeFindListener` has a default (empty) implementation for `onSessionUpdated(session)`, but `onSearchPaused`, `onSearchStarted`, and `onSearchStopped` have no default and must be implemented.
- MatrixScan Find is commonly paired with SparkScan (scan a list first with SparkScan, then locate those items with BarcodeFind) — see the "SparkScan hand-off" note in `references/integration.md`. If the user's question is purely about SparkScan (scanning, not finding), route them to the `sparkscan-kmp` skill instead.

## Intent Routing

Based on the user's request, read `references/integration.md` and follow the instructions there for:

- **Integrating MatrixScan Find from scratch** (e.g. "add MatrixScan Find to my KMP app", "set up BarcodeFind", "how do I search for items with BarcodeFind")
- **Building the item list to search for** (e.g. "how do I set the list of barcodes to find", "add info/image to a found item", "highlight items with a custom color")
- **Handling found items** (e.g. "how do I know when an item is found", "what happens when the user taps finish")
- **Transforming scanned barcode data** (e.g. "normalize scanned barcode data before matching", "ignore certain barcodes during search")
- **Customizing feedback** (e.g. "change the sound when an item is found", "disable vibration")
- **Customizing the BarcodeFindView UI** (e.g. "hide the carousel", "change the hint text", "hide the finish button")
- **Using Compose Multiplatform** (e.g. "use BarcodeFind in `@Composable` code", "the barcode-compose BarcodeFindView composable")
- **Lifecycle wiring across Android/iOS** (e.g. "why does my BarcodeFindView freeze", "onResume/onPause for BarcodeFindView")

This skill only covers integration (there is no migration guide — MatrixScan Find on KMP has no prior KMP version to migrate from).

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or guess method signatures, parameters, or property names. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API page:
1. First check whether the page you already fetched contains a direct hyperlink to it.
2. If no direct link was found, fetch the Get Started / Advanced page (see the table below), extract the actual link from it, and follow that.

URL structures can vary and guessing will lead to 404s. The KMP SDK is new; some topic-specific get-started pages referenced below may not exist yet for the `kmp` platform — if a link 404s, fall back to the general docs index at https://docs.scandit.com/ and tell the user the page may not be published yet.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Intro](https://docs.scandit.com/sdks/kmp/matrixscan-find/intro/) · [Get Started](https://docs.scandit.com/sdks/kmp/matrixscan-find/get-started/) |
| Advanced (customization, transformer, filtering) | [Advanced Configurations](https://docs.scandit.com/sdks/kmp/matrixscan-find/advanced/) |
| Sample app (SparkScan search + BarcodeFind find) | In-monorepo: `frameworks/kmp/samples/03_Advanced_Batch_Scanning_Samples/03_Search_and_Find/SearchAndFindSample` |
| Core concepts (context, camera, views) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
| SparkScan (the "search" half of search-and-find) | Route to the `sparkscan-kmp` skill |
