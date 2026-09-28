---
name: scandit-xamarin-to-net-migration
description: Migrate the Scandit Data Capture SDK integration after a Xamarin app is already on the .NET stack (.NET for Android, .NET for iOS, or .NET MAUI) — e.g. after Microsoft's .NET app-modernization tooling. Use when the project builds as .NET/MAUI but Scandit code still references `Scandit.DataCapture.*.Xamarin(.Forms)` packages, `.Unified` namespaces, or legacy `Scandit.BarcodePicker.Xamarin`. Swaps packages, fixes SDK-8 init, namespaces and views, verifies scanning, and hands off to the matching `*-net-android`/`-net-ios`/`-net-maui` skill. Migrates only the Scandit SDK, not the general app.
license: MIT
metadata:
  author: scandit
  version: "1.0.0"
---

# Scandit Xamarin → .NET Migration Skill

Migrates the **Scandit Data Capture SDK integration** after a customer's Xamarin app has already been moved onto the supported .NET stack — .NET for Android, .NET for iOS, or .NET MAUI. Microsoft ended Xamarin support on **May 1, 2024**, and Scandit stopped shipping Xamarin SDK updates from v8.0, so the modern binding is the only path to newer Scandit releases.

## Scope — read this first, then say it to the user

**This skill migrates the Scandit SDK and nothing else.** It is a *post-migration* tool: it assumes the application shell has already been ported to .NET/MAUI, and it fixes up the Scandit slice that the general migration left behind.

| This skill **owns** | This skill does **NOT** touch (owned by Microsoft's .NET app-modernization tooling + the customer's team) |
|---|---|
| Swapping `Scandit.DataCapture.*.Xamarin(.Forms)` packages for the .NET / `*.Maui` equivalents | Converting the project to SDK-style, collapsing Forms heads into a MAUI head project |
| The Scandit `.Unified` → plain namespace rename and the `<scandit:…>` XAML `xmlns` | The general `Xamarin.Forms` → `Microsoft.Maui` namespace/API sweep, `MessagingCenter`/`DisplayAlert`/`MainPage` deprecations |
| SDK-8 `Initialize()` (Android/iOS) or the `.UseScandit*()` builder chain (MAUI) | Custom renderers → handlers, platform effects, `DependencyService` → DI |
| Relocating Scandit views/overlays where the .NET/MAUI binding requires it | Third-party NuGet packages with no .NET equivalent |
| The Scandit runtime prerequisites (camera permission, Scandit's OS-version minimums) | Everything else in the app |

If the project is **not yet on .NET/MAUI** (still `MonoAndroid`/`Xamarin.iOS`/`Xamarin.Forms`, `packages.config`, legacy `.csproj`), this skill does **not** convert it. Stop and tell the user to run **Microsoft's .NET app-modernization tooling** first, then return here for the Scandit part. Do not hand-roll the project conversion — that is out of scope by design (see `references/detection.md`, Precondition).

> **Which Microsoft tool?** Microsoft's recommended path is now the **[GitHub Copilot app‑modernization / upgrade agent](https://learn.microsoft.com/en-us/dotnet/core/porting/github-copilot-upgrade/overview)** built into Visual Studio 2026 and VS 2022 (17.14.16+). It **supersedes the now‑deprecated [.NET Upgrade Assistant](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview)**, which still exists (and many existing projects were migrated with it) but is no longer the recommended tool. Either one produces the .NET/MAUI shell this skill runs *after*; point users at the Copilot agent first, and treat "the Upgrade Assistant" in a user's message as the same out‑of‑scope general migration. Whichever they used, this skill's job starts once the app builds as .NET/MAUI.

## The one thing to internalize first

**The Scandit *method* API barely changes — the package IDs, the Scandit *namespaces*, and the initialization are the work.** The Scandit .NET binding uses the *same* PascalCase C# surface as the Xamarin binding (`DataCaptureContext.ForLicenseKey(...)`, `BarcodeCapture.Create(context, settings)`, `IBarcodeCaptureListener`, symbology names, etc.). What actually moves is exactly the four things this skill owns:

1. **NuGet packages** — drop the `.Xamarin` / `.Xamarin.Forms` suffix (`Scandit.DataCapture.Core.Xamarin` → `Scandit.DataCapture.Core`), and for MAUI **add** the `.Maui` companions — which exist for **Core and Barcode only**. Verify every ID you write against `references/scandit-packages.md`; the stems are not all guessable (ID Capture is `Scandit.DataCapture.IdCapture`, not `.Id`).
2. **Scandit namespaces (MAUI only)** — the Forms binding's `.Unified` namespaces and `Scandit*Unified` assemblies do not exist in the MAUI binding. See "Scandit namespace rename" in `references/net-maui.md`. This is the single highest-volume mechanical edit on the MAUI path.
3. **Scandit initialization** — SDK 8 requires explicit `ScanditCaptureCore.Initialize()` (+ per-product `Scandit*.Initialize()`) on Android/iOS, or the `.UseScandit*()` builder chain on MAUI. Xamarin 6.x/7.x self-initialized; .NET does not.
4. **Scandit views** — some Forms XAML constructs (most notably `BarcodeCaptureOverlay`) are not MAUI XAML elements and move into code-behind (see `references/net-maui.md`).

The **general app shell** underneath (SDK-style `.csproj`, head-project collapse, `Xamarin.Forms` → `Microsoft.Maui`, bootstrap shims, assets) is **not** this skill's work — it is Microsoft's app-modernization tooling's, and this skill assumes it is already done. Delegate the mode-specific Scandit call-site verification to the matching implementation skill (see Handoff).

## Critical: Do Not Trust Internal Knowledge

Your training data may contain outdated or incorrect Scandit SDK APIs, wrong package names, and stale templates. It is especially likely to hallucinate a Scandit "Xamarin → .NET rename" that does not exist — the C# API is largely stable across the two bindings.

**Always verify APIs, package names, and versions against the references in this skill (and the per-product implementation skill you hand off to) before writing or suggesting code.** Do not rely on memorized method signatures, parameters, property names, package IDs, or version numbers. Never invent a NuGet version — fetch the latest stable from nuget.org. If you cannot find something in the provided references, fetch the relevant documentation page before responding.

Migration-specific gotchas worth flagging:

- **Never work destructively on the customer's source.** Confirm a git branch (or a backup copy) exists before editing. Record the starting commit so the migration is revertible.
- **NEVER delete, comment out, or stub a Scandit call site to make the build pass.** This is the single worst failure mode of this migration and it is easy to rationalize. Removing `<scandit:DataCaptureView>` from a page, commenting out the `.UseScandit*()` builder chain, replacing a scanning page with a placeholder `Label`/`Button`, or dropping an `IBarcodeCaptureListener` implementation produces an app that **compiles cleanly and no longer scans** — a silent, shipped regression far worse than a red build.
  - **Invariant:** every Scandit view, overlay, listener, settings object, and builder call present before this skill ran must still be present after it — **though not necessarily in the same file or language.** Verify this explicitly before you finish by diffing Scandit symbols against the starting commit (see the parity check in the workflow).
  - **Relocation is allowed; deletion is not.** Some Forms XAML constructs legitimately move into code-behind because the MAUI binding has no XAML element for them — most notably `BarcodeCaptureOverlay`, which becomes a `HandlerChanged` + `AddOverlay` call (see `references/net-maui.md`). Moving a construct from markup to C# satisfies the invariant. Removing it without recreating it does not.
  - If a Scandit construct will not compile, the cause is almost always a **wrong namespace/assembly name in your code, or a type that is not a XAML element at all** — not a missing API. Read the implementation skill's documented namespace, and check whether the type is a control or a runtime object, before concluding the API does not exist.
  - A build that only goes green because integration code was removed is a **FAILED migration**. Report it as blocked, with the compile error, and leave the original code in place — do not report success.
- **Do not conclude a Scandit API "does not exist" from a compile error.** Before making that claim, verify against the implementation skill's references, and if still unsure inspect the shipped assembly directly, e.g.
  `strings ~/.nuget/packages/scandit.datacapture.core.maui/<version>/lib/<tfm>/ScanditCaptureCoreMaui.dll | grep UseScandit`.
  `UseScanditCore`, `AddDataCaptureView` (in `ScanditCaptureCoreMaui`) and `UseScanditBarcode` (in `ScanditBarcodeCaptureMaui`) are all real and shipped — if they appear to be missing, your `using`/`xmlns` is wrong. They are **extension methods**, so `CS1061: 'MauiAppBuilder' has no method 'UseScanditCore'` means a missing `using`, not a missing API. The three required directives are:
  ```csharp
  using Scandit.DataCapture.Core;          // UseScanditCore
  using Scandit.DataCapture.Core.UI.Maui;  // AddDataCaptureView
  using Scandit.DataCapture.Barcode;       // UseScanditBarcode
  ```
  Commenting out the `.UseScandit*()` chain to get a green build is the **canonical instance** of the forbidden gutting above: the app then builds, launches, and fails at the first Scandit call because the SDK was never initialized.
- **The migration is resumable and idempotent.** Re-running on a partially migrated project must *continue*, not redo — always re-run detection first (see `references/detection.md`) and skip steps whose target state is already present (packages already suffix-less, init already added, etc.).
- **Xamarin package IDs carry a `.Xamarin` *or* `.Xamarin.Forms` suffix; .NET ones do not.** `Scandit.DataCapture.Core.Xamarin` → `Scandit.DataCapture.Core`, and `Scandit.DataCapture.Core.Xamarin.Forms` → `Scandit.DataCapture.Core` **+** `Scandit.DataCapture.Core.Maui`. Strip the whole suffix — naively "dropping `.Xamarin`" from `Core.Xamarin.Forms` yields `Scandit.DataCapture.Core.Forms`, which **does not exist** and fails restore with `NU1101`. The legacy v5 `Scandit.BarcodePicker.Xamarin` (Barcode Picker API) has **no** modern equivalent — it maps to a Barcode Capture / SparkScan reintegration, not a package swap. Flag it and route to the matching implementation skill.
- **Do not guess the target TFM version — resolve it from the installed toolchain.** Run `dotnet workload list` and `dotnet --version` and match the TFM the project is already built against; a `net8.0-*` build command on a machine with only the .NET 10 SDK fails to restore. Whatever the project uses, use the *same* TFM in the build-verification commands you run and report.
- **`net10.0-android` needs an explicit kotlinx-serialization-json override.** Scandit's Android AAR chain pulls a transitive `Org.Jetbrains.Kotlinx.KotlinxSerializationJson` that only targets `net8.0-android`/`net9.0-android`. On `net10.0-android` the project builds **clean** and then crashes at the first scan with `Java.Lang.NoClassDefFoundError: Lkotlinx/serialization/json/JsonKt;`. If the project targets `net10.0-android`, add the override from `references/net-maui.md` ("Android kotlinx-serialization override") — and note that a green build does **not** rule this out.
- **SDK 8.0+ requires explicit initialization** that Xamarin 6.x/7.x did not. Omitting `ScanditCaptureCore.Initialize()` compiles fine but crashes at the first Scandit call. The exact placement is per-platform — the implementation skill you hand off to has the template.

## Precondition check (do this before anything else)

Confirm the app has already been migrated to .NET/MAUI. Follow `references/detection.md` → **Precondition**. In short:

- **On .NET/MAUI already** (`<Project Sdk="Microsoft.NET.Sdk">`, TFM `net*-android` / `net*-ios`, or `<UseMaui>true</UseMaui>`) → proceed with this skill.
- **Still on Xamarin** (`MonoAndroid` / `Xamarin.iOS` TFM, `Xamarin.Forms` reference, `packages.config`, legacy `.csproj`) → **stop.** Tell the user the general app migration is out of scope for this skill and must be done first with Microsoft's .NET app-modernization tooling (the GitHub Copilot app‑modernization agent; see Scope for the link and the deprecated Upgrade Assistant it replaces); offer to do the Scandit part as soon as the app is on .NET/MAUI. Do not attempt the project conversion yourself.

## Intent Routing

Based on the detected setup and the user's request, load the appropriate reference file before responding:

- **First contact / unknown setup** ("my .NET app's Scandit code won't build after the upgrade", "finish moving Scandit to MAUI") → always start with `references/detection.md` to run the precondition check and classify the target platform, then follow the matching reference.
- **.NET for Android target** → read `references/net-android.md`.
- **.NET for iOS target** → read `references/net-ios.md`.
- **.NET MAUI target** → read `references/net-maui.md`.
- **Which Scandit packages/APIs change, and which implementation skill to hand off to** → read `references/scandit-packages.md`.
- **Producing the final migration report** → read `references/report-template.md`.

## Migration workflow

Copy this checklist into the working session and track progress. It is the same regardless of target platform.

```
Scandit migration progress:
- [ ] 1. Precondition — confirm the app is already on .NET/MAUI (else → Microsoft's app-modernization tooling, stop)
- [ ] 2. Detect      — target platform, Scandit packages + version, Scandit surface baseline
- [ ] 3. Packages    — swap .Xamarin(.Forms) → .NET (+ .Maui for MAUI), one version from nuget.org
- [ ] 4. Wire        — SDK-8 Initialize() / .UseScandit*() chain, namespaces, views, camera prereqs
- [ ] 5. Verify      — parity check, build per target, smoke-scan, write the report
```

**Phase 1 — Precondition.** Run the precondition check above. If the app is still on Xamarin, stop and route to Microsoft's app-modernization tooling.

**Phase 2 — Detect.** Follow `references/detection.md`. Output: the target platform (net-android / net-ios / MAUI), the Scandit packages + version referenced, the detected Scandit product, and a **baseline of the Scandit symbol surface** for the Phase 5 parity check. This phase is also the resume check — skip any Scandit step already done.

**Phase 3 — Swap the Scandit packages.** Follow `references/scandit-packages.md`: strip the `.Xamarin` / `.Xamarin.Forms` suffix (add `*.Maui` companions on MAUI), pinned to a single latest-stable version fetched from nuget.org. `dotnet restore`.

**Phase 4 — Wire the Scandit integration.** Apply the matching `references/net-*.md`: SDK-8 `Initialize()` (Android/iOS) or the `.UseScandit*()` builder chain (MAUI), the Scandit `.Unified` → plain namespace rename and `xmlns` (MAUI), any view relocation, and the Scandit runtime prerequisites (camera permission; Scandit's Android API-24 / iOS-15 minimums). Then **hand off to the matching implementation skill** (see below) to verify/rewrite the mode-specific call sites — do not re-derive the Scandit API here.

**Phase 5 — Verify and report.** In this order:

1. **Integration-parity check (do this *before* the build).** Confirm no Scandit integration was lost. Diff the Scandit symbol surface against the starting commit, e.g.

   ```bash
   git grep -IohE 'scandit[A-Za-z]*:[A-Za-z]+|UseScandit[A-Za-z]*|BarcodeCaptureOverlay|DataCaptureView|IBarcodeCaptureListener' <start-sha> -- . ':(exclude)**/obj/**' ':(exclude)**/bin/**' | sort -u > /tmp/before.txt
   git grep -IohE 'scandit[A-Za-z]*:[A-Za-z]+|UseScandit[A-Za-z]*|BarcodeCaptureOverlay|DataCaptureView|IBarcodeCaptureListener'              -- . ':(exclude)**/obj/**' ':(exclude)**/bin/**' | sort -u > /tmp/after.txt
   diff /tmp/before.txt /tmp/after.txt
   ```

   Anything present before and absent after must be either (a) a documented rename/relocation you applied deliberately, or (b) a **defect you fix now**. Also grep the diff for commented-out `UseScandit`/`scandit:` lines — a commented builder call is a lost integration, not a migration.
2. **Build** for the target platform, using the TFM the project already targets.
3. **Smoke check** on a device/emulator where available: the SDK initializes, the camera preview renders (a black/blank preview usually means `DataCaptureContext` is not bound on the view), and a scan reports a result. On `net10.0-android` a clean build does not imply a working scan — see the kotlinx gotcha.
4. **Report** using `references/report-template.md`: the Scandit changes applied, anything still owed on the Scandit side, and how to validate. If step 1 or 2 failed, the status is *Blocked* or *Partial* — never *Complete*.

## Handoff to the implementation skills

The mode-specific Scandit call sites are verified by the per-product .NET skill for the customer's product + target platform. Pick the skill that matches both:

| Target platform | Skill name pattern | Examples |
|---|---|---|
| .NET for Android (`net*-android`, non-MAUI) | `<product>-net-android` | `barcode-capture-net-android`, `id-capture-net-android` |
| .NET for iOS (`net*-ios`, non-MAUI) | `<product>-net-ios` | `barcode-capture-net-ios`, `id-capture-net-ios` |
| .NET MAUI | `<product>-net-maui` | `barcode-capture-net-maui`, `sparkscan-net-maui`, `id-capture-net-maui`, `label-capture-net-maui` |

All seven .NET products have the full `net-android` / `net-ios` / `net-maui` trio: Barcode Capture, SparkScan, Smart Label Capture, ID Capture, MatrixScan AR, MatrixScan Batch, and MatrixScan Count (21 skills total). **Load the handoff skill before you write any target-platform Scandit code**, not after: it holds the exact XAML `xmlns`, assembly names, and builder-chain signature you need, and guessing them is the main cause of the "the API doesn't exist" false conclusion. If the skill you named fails to load, re-derive its slug from `references/scandit-packages.md` rather than proceeding without it.

If you are unsure which Scandit **product** the customer uses (Barcode Capture, SparkScan, MatrixScan AR/Batch/Count, Smart Label Capture, ID Capture), hand off to the **`data-capture-sdk`** router skill — it identifies the product and names the correct implementation skill. Naming the specific skill is always better than telling the user "an implementation skill exists."

## API Usage Policy

Only use APIs, package IDs, and namespaces that are explicitly documented in this skill's references or in the implementation skill you hand off to. Do not invent or guess method signatures, parameters, property names, package names, or version numbers. If unsure whether an API exists or how it is called — or if a compile error occurs — fetch the relevant reference page before responding. Do not tell the user to check the docs themselves. After answering, always include the relevant link so the user can explore further.

**Never construct or guess documentation or NuGet URLs.** When you need a specific page:
1. First check whether a page you already fetched links to it — topic pages link directly to relevant API symbols and sibling docs. Always request links alongside content in your fetch prompt.
2. If no direct link was found, fetch the API/docs index (see **References** below), extract the actual link from it, and follow that.

URL structures vary between the Xamarin (versioned, e.g. `docs.scandit.com/7.6.x/sdks/xamarin/...`) and .NET (`docs.scandit.com/sdks/net/...`) doc trees, and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Microsoft's .NET app-modernization tooling (general app migration — out of scope here; **recommended**) | [GitHub Copilot app-modernization / upgrade agent](https://learn.microsoft.com/en-us/dotnet/core/porting/github-copilot-upgrade/overview) |
| .NET Upgrade Assistant (its **deprecated** predecessor — still works; many apps were migrated with it) | [Upgrade Assistant overview](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview) |
| Microsoft's Xamarin → .NET upgrade guidance | [Upgrade from Xamarin to .NET](https://learn.microsoft.com/en-us/dotnet/maui/migration/) |
| Scandit .NET SDK docs | [Scandit for .NET](https://docs.scandit.com/sdks/net/android/add-sdk/) |
| Scandit MAUI SDK docs | [Scandit for .NET MAUI](https://docs.scandit.com/sdks/net/maui/add-sdk/) |
| Legacy Scandit Xamarin docs (source side) | [Scandit for Xamarin (7.6.x)](https://docs.scandit.com/7.6.14/sdks/xamarin/ios/add-sdk/) |
| Scandit .NET NuGet packages | [nuget.org/profiles/Scandit](https://www.nuget.org/profiles/Scandit) |
