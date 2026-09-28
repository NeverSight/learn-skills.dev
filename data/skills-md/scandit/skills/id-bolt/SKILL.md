---
name: id-bolt
description: Scandit ID Bolt in web projects (`@scandit/web-id-bolt`) — the hosted, drop-in identity-document scanning pop-up (passports, driver's licenses, ID cards) with built-in handover to the user's phone, for adding ID scanning to a website with minimal code and no camera UI to build. Use for integration (IdBoltSession), document selection, validators, returned-data and anonymization options, theming and workflow customization, or troubleshooting. A different product from ID Capture — for in-page fully-customizable scanning embedded in your own UI use id-capture-web.
license: Apache-2.0
metadata:
  author: scandit
  version: "1.0.1"
---

# ID Bolt (Web) Skill

## What ID Bolt is — and what it is NOT

ID Bolt is a **hosted, drop-in** identity-scanning product. You call `IdBoltSession.create(...)` and `start()`, and Scandit opens its **own scanning UI in a pop-up** (`https://app.id-scanning.com`). Scandit hosts the camera, the viewfinder, the scanning logic, the result screen, and the engine files. Your code only **configures** the session and **receives the result** in a callback — you don't build a UI/camera workflow at all.

It also supports **device handover**: when the current device has no camera or a poor one (e.g. a desktop), ID Bolt can show a QR code so the user finishes the scan on another device such as their phone, and the result still flows back to your `onCompletion` callback on the original page. This is built into the hosted flow, not something you wire up.

This makes ID Bolt the fastest way to add ID scanning to a website, but it also means almost everything you might know about the **ID Capture** Web SDK does **not apply**. ID Bolt is a thin wrapper _around_ ID Capture; it is not ID Capture.

|                                  | **ID Bolt** (`@scandit/web-id-bolt`)                                         | **ID Capture** (`@scandit/web-datacapture-id`)                                    |
| -------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| UI                               | Scandit-hosted pop-up                                                        | You build it, embedded in your page                                               |
| Camera / view / overlay          | Managed by Scandit                                                           | You manage `Camera`, `DataCaptureView`, `IdCaptureOverlay`                        |
| Entry point                      | `IdBoltSession.create(url, opts)` + `await session.start()`                  | `await DataCaptureContext.forLicenseKey(...)` + `await IdCapture.forContext(...)` |
| Results                          | `onCompletion(result => result.capturedId)` callback in options              | `idCapture.addListener({ didCaptureId, didRejectId })`                            |
| Documents                        | `DocumentSelection.create({ accepted, rejected })`                           | `settings.acceptedDocuments = [...]`                                              |
| Scanner                          | `new SingleSideScanner(...)` / `new FullDocumentScanner()` (passed directly) | `settings.scanner = new IdCaptureScanner({ physicalDocument: ... })` (wrapper)    |
| Engine files / `libraryLocation` | N/A (hosted)                                                                 | You self-host the engine WASM files                                               |

**If the task needs an embedded, in-page, fully-custom camera experience, this is the wrong skill — use `id-capture-web`.** If the task is "add ID scanning to my site quickly without building UI," ID Bolt is right.

## Critical: Do Not Trust Internal Knowledge

Your training data is unlikely to contain ID Bolt's API at all, and is very likely to contain the **ID Capture** Web/native APIs, which look superficially similar and will produce non-working code if pattern-matched. Verify every API against the references below before writing code. The dominant failure modes:

1. **Wrong package.** ID Bolt is `@scandit/web-id-bolt`. There is no `@scandit/web-datacapture-core` or `@scandit/web-datacapture-id` dependency for an ID Bolt integration.
2. **Inventing a context/camera/view.** ID Bolt has **none** of `DataCaptureContext`, `Camera`, `DataCaptureView`, `FrameSource`, `IdCaptureOverlay`, or engine `libraryLocation`. Do not emit setup code for them.
3. **Wrong result mechanism.** Results arrive through the `onCompletion` callback you pass into `create(...)` — there is **no `addListener`**, no `didCaptureId`/`didRejectId`.
4. **Wrong document/scanner shape.** Documents go in `DocumentSelection.create({ accepted, rejected })` (not `acceptedDocuments`). Scanners are passed directly as `scanner: new FullDocumentScanner()` — there is **no `IdCaptureScanner` wrapper** and **no `IdCaptureSettings`**.

### Forbidden APIs (commonly hallucinated — do NOT emit these)

| Do NOT write                                                                                       | Use instead                                                                                                                    |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `import { ... } from "@scandit/web-datacapture-id"`                                                | `import { ... } from "@scandit/web-id-bolt"`                                                                                   |
| `await DataCaptureContext.forLicenseKey(...)` / `new DataCaptureView()` / `Camera.pickBestGuess()` | nothing — ID Bolt has no context/camera/view; just `IdBoltSession.create(url, opts)`                                           |
| `idCaptureLoader({ enableVIZDocuments: true })` / `libraryLocation`                                | nothing — the engine is hosted by Scandit                                                                                      |
| `new IdCaptureSettings()` + `settings.acceptedDocuments = [...]`                                   | `DocumentSelection.create({ accepted: [...], rejected: [...] })`                                                               |
| `settings.scanner = new IdCaptureScanner({ physicalDocument: new FullDocumentScanner() })`         | `scanner: new FullDocumentScanner()` (passed directly in options)                                                              |
| `await IdCapture.forContext(context, settings)`                                                    | `IdBoltSession.create(serviceUrl, options)` (synchronous) then `await session.start()`                                         |
| `idCapture.addListener({ didCaptureId, didRejectId })`                                             | `onCompletion: (result) => { result.capturedId }` and `onCancellation: (reason) => {}` in the options object                   |
| `settings.rejectExpiredIds = true` / `rejectInconsistentData`                                      | `validation: [Validators.notExpired()]`                                                                                        |
| `RejectionReason.DocumentExpired` etc.                                                             | validations are surfaced in-flow; cancellation uses `CancellationReason.UserClosed` / `CancellationReason.ServiceStartFailure` |
| `await idCapture.setEnabled(true)` / `idCapture.reset()`                                           | nothing — the hosted pop-up manages its own state                                                                              |

## Intent Routing

- **In-page / embedded / fully-custom ID scanning** (own camera UI, `DataCaptureView`, overlays, runtime mode switching) → this is **ID Capture**, not ID Bolt. Hand off to the `id-capture-web` skill.
- **Other Scandit products** (Barcode Capture, SparkScan, MatrixScan, Label Capture, or product selection) → hand off to the `data-capture-sdk` skill.
- **Add hosted ID scanning to a website quickly, configure documents/scanner/validation, read results, theme/localize the pop-up** → use the Product Guidance and Minimal integration shape below, verifying every API against the References.

## Product Guidance

- **Accept only the documents you need.** Ask which document types and regions the user expects, then list them in `DocumentSelection.create({ accepted: [...] })`. Use `rejected: [...]` to carve out exceptions (e.g. accept any passport but reject a specific region).
- **Pick the scanner to match the data.** `SingleSideScanner(barcode, mrz, viz, options?)` (the default) reads one side; pass booleans to enable each zone. `FullDocumentScanner()` forces front **and** back and enables all modalities — use it when you need maximum data (e.g. a US driver's license barcode plus the VIZ).
- **Choose the right `returnDataMode` (required).** `ReturnDataMode.Full` returns extracted data without images; `ReturnDataMode.FullWithImages` includes document/face images. Don't request images unless the use case needs them.
- **Anonymize sensitive data when you don't need it.** `anonymizationMode` (`None`/`FieldsOnly`/`ImagesOnly`/`FieldsAndImages`) plus `anonymizedFields` (with `IdFieldType` entries) let you drop fields/images before they ever reach your callback. `result.capturedId.anonymizedFields` reports what was anonymized.
- **Use `validation` for accept/reject rules.** `Validators.notExpired()`, `Validators.notExpiredIn({ days, months })`, and `Validators.US.isRealID()` are built in. For business rules (blacklists, country/nationality matching), pass a **custom validator function** returning an `ExternalValidatorResult` (`{ type: "external", name, valid, details? }`); it may be async. Failed validations are surfaced to the user inside the hosted flow.
- **Always handle both callbacks.** `onCompletion(result)` fires only after a successful scan that passed all validations (`result.capturedId` may still be `null` — guard it). `onCancellation(reason)` fires when the user closes the pop-up or the service fails to start; switch on `CancellationReason`.
- **Manage the session lifecycle.** For several scans in a row, set `keepAliveForNextSession: true` to keep resources warm, and call `IdBoltSession.terminate()` when fully done to release them.
- **Customize the hosted UI through options, not CSS on your page.** Use `workflow` (welcome/result screens, image upload), `locale` (e.g. `"en-US"`, `"de"`, `"fr"`), `theme` (colors/dimensions/images/fonts), and `textOverrides`. You cannot style the pop-up internals from your own stylesheet — it runs on Scandit's origin.
- **`theme.styleOverrides` needs a COMPLETE CSS ruleset per element, not just the declarations you want to change.** Each override (`button`/`link`/`title`/`banner`, targeting `.bolt-button`/`.bolt-link`/`.bolt-title`/`.bolt-banner`) renders that element in its **own shadow DOM with all default styles dropped**, so you must supply the full rule — selector included, plus every property the element needs to look right (background, colour, padding, border-radius, layout) and any `:hover`/`:focus` states — restated in full. A value like `` `text-transform:uppercase;` `` (bare declarations, or only the delta) applies nothing or yields an unstyled element. Prefer `theme.colors` + `theme.dimensions` for plain recolouring/rounding (those keep ID Bolt's layout); reach for `styleOverrides` only for personality the slots can't express, and then restate the whole element. **Note:** the desktop interstitial "continue"/"learn-more" links are **not** `.bolt-link` and are driven by neither `colors.primary` nor `styleOverrides.link` — their colour isn't themeable through the public API. See the [Style Overrides docs](https://docs.scandit.com/hosted/id-bolt/theming/#style-overrides) for the canonical full-ruleset example.
- **Defer non-ID-Bolt questions.** ID Capture → `id-capture-web`; other products/selection → `data-capture-sdk`.

## Minimal integration shape

Prerequisites: `npm install @scandit/web-id-bolt`. A license key entitled for ID Bolt comes from the Scandit dashboard (free test account at <https://ssl.scandit.com/dashboard/sign-up?p=id-bolt>). The service URL is `https://app.id-scanning.com` (a Scandit-hosted alias). There are **no** engine/WASM files to host.

```ts
import {
  DocumentSelection,
  IdBoltSession,
  Region,
  Passport,
  IdCard,
  DriverLicense,
  ReturnDataMode,
  Validators,
  CancellationReason,
} from "@scandit/web-id-bolt";

const ID_BOLT_URL = "https://app.id-scanning.com";
const LICENSE_KEY = "-- YOUR LICENSE KEY HERE --";

async function startIdBolt() {
  const documentSelection = DocumentSelection.create({
    accepted: [new Passport(Region.Any), new IdCard(Region.Any), new DriverLicense(Region.Any)],
  });

  const idBoltSession = IdBoltSession.create(ID_BOLT_URL, {
    licenseKey: LICENSE_KEY,
    documentSelection,
    returnDataMode: ReturnDataMode.Full,
    validation: [Validators.notExpired()],
    locale: "en-US",
    onCompletion: (result) => {
      if (result.capturedId) {
        console.log("Document type:", result.capturedId.documentType);
        console.log("Full name:", result.capturedId.fullName);
        console.log("Document number:", result.capturedId.documentNumber);
        console.log("Date of birth:", result.capturedId.dateOfBirth);
        console.log("Date of expiry:", result.capturedId.dateOfExpiry);
      }
    },
    onCancellation: (reason) => {
      switch (reason) {
        case CancellationReason.UserClosed:
          console.log("User closed the scanning window");
          break;
        case CancellationReason.ServiceStartFailure:
          console.log("ID Bolt service failed to start");
          break;
      }
    },
  });

  // Opens the hosted pop-up; resolves when the flow ends.
  await idBoltSession.start();
}

// ID Bolt must be started from a user gesture (the pop-up requires it).
document.getElementById("scan-id")!.addEventListener("click", startIdBolt);
```

```html
<button id="scan-id">Scan your ID</button>
```

Notes:

- `IdBoltSession.create(...)` is **synchronous**; only `session.start()` is awaited.
- Start from a **user gesture** (click) — browsers block programmatic pop-ups/camera otherwise.
- To read images, switch to `returnDataMode: ReturnDataMode.FullWithImages` and read the image fields off `result.capturedId`.

## API Usage Policy

Only use APIs that exist in `@scandit/web-id-bolt` and the referenced documentation. Do not invent or guess method signatures, parameters, or property names — and especially do not borrow them from the ID Capture SDK, which is a different package. When unsure whether an API exists or how to call it, fetch the documentation before responding. Do not tell the user to check the docs themselves. After answering, include the relevant link so they can explore further. **Never construct or guess documentation URLs** — fetch the API overview and follow links from there.

## References

| Topic                                            | Resource                                                                                                                                |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| API overview                                     | [ID Bolt API Overview](https://docs.scandit.com/hosted/id-bolt/api-overview/)                                                           |
| Getting started                                  | [Getting Started](https://docs.scandit.com/hosted/id-bolt/getting-started/)                                                             |
| Document selection                               | [Document Selection](https://docs.scandit.com/hosted/id-bolt/document-selection/)                                                       |
| Validators                                       | [Validators](https://docs.scandit.com/hosted/id-bolt/validators/)                                                                       |
| Data handling & anonymization                    | [Data Handling](https://docs.scandit.com/hosted/id-bolt/data-handling/)                                                                 |
| Callbacks (`onCompletion`/`onCancellation`)      | [Callbacks](https://docs.scandit.com/hosted/id-bolt/callbacks/)                                                                         |
| Workflow & scanner options                       | [Workflow Options](https://docs.scandit.com/hosted/id-bolt/workflow/)                                                                   |
| Theming & text overrides                         | [Theming](https://docs.scandit.com/hosted/id-bolt/theming/) · [Text Overrides](https://docs.scandit.com/hosted/id-bolt/text-overrides/) |
| Advanced (lifecycle, keep-alive, transaction id) | [Advanced Options](https://docs.scandit.com/hosted/id-bolt/advanced/)                                                                   |
| Release notes                                    | [Release Notes](https://docs.scandit.com/hosted/id-bolt/release-notes/)                                                                 |
| Source of truth                                  | `@scandit/web-id-bolt` package                                                                                                          |
