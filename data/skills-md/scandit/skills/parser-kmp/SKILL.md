---
name: parser-kmp
description: Scandit Parser in Kotlin Multiplatform (KMP) projects — com.scandit.datacapture.kmp:parser artifact, com.kmp.datacapture.parser imports. Parses barcode/RFID data strings (GS1 AI, GS1 Digital Link, HIBC, Swiss QR, VIN, IATA boarding pass, EPC) into ParsedField values in commonMain. AAMVA driver's licenses belong to ID Capture (id-capture-* skills). Use for Parser setup, data-format configuration, parsed-result handling, or troubleshooting parsing.
license: MIT
metadata:
  author: scandit
  version: "1.0.1"
---

# Parser KMP Skill

## Critical: Do Not Trust Internal Knowledge

Scandit's Kotlin Multiplatform (KMP) SDK is new, shipping in 8.6. Your training data almost
certainly predates it and contains **zero** reliable knowledge of its API — do not pattern-match
it against the Android or iOS native SDKs you may know. The KMP API packages are
`com.kmp.datacapture.*` (NOT `com.scandit.datacapture.*`), and shapes diverge from both native
SDKs in specific ways (see below).

**Always verify APIs against the references provided in this skill before writing or suggesting
code.** Do not rely on memorized method signatures, parameters, or property names from any other
Scandit platform. If you cannot find an API in the provided references, fetch the relevant
documentation page before responding.

KMP-specific gotchas worth flagging:

- Import root is `com.kmp.datacapture.parser.*` — e.g. `com.kmp.datacapture.parser.Parser`,
  `com.kmp.datacapture.parser.ParserDataFormat`. Never write `com.scandit.datacapture.parser.*`
  in KMP code.
- Creation is the companion factory `Parser.forFormat(dataCaptureContext, format)` — takes the
  shared `DataCaptureContext` and a `ParserDataFormat` value. There is no bare constructor, no
  `Parser.create(format)`, and no `Parser.fromJson(...)` on KMP.
- `ParserDataFormat` has exactly seven values: `GS1_AI`, `HIBC`, `SWISS_QR`, `VIN`, `IATA_BCBP`,
  `GS1_DIGITAL_LINK`, `EPC`. There is **no `AAMVA` value** — do not invent one. AAMVA driver's
  license data is handled by ID Capture, not this Parser.
- `parser.parseString(data: String)` and `parser.parseRawData(data: ByteArray)` both return a
  `ParsedData` and are declared `@Throws(Exception::class)`. On failure they throw
  `ParserException` (a plain `RuntimeException` subclass common to both platforms — iOS has no
  native parser-exception type, so its `NSError` is mapped into this same common `ParserException`
  under the hood). Catch `ParserException` first (for `code`, `message`, `additionalInfo`) and fall
  back to `Exception` only for anything unexpected.
- `ParsedData` exposes `fields: List<ParsedField>`, `fieldsByName: Map<String, ParsedField>`,
  `fieldsWithIssues: List<ParsedField>` (fields that have warnings), and `jsonString: String`.
  There is no top-level "issues" list on `ParsedData` itself — per-field warnings live on
  `ParsedField.warnings`.
- `ParsedField` exposes `name: String`, `parsed: Any?`, `rawString: String`, and
  `warnings: List<ParserIssue>`. `parsed`'s actual runtime type (string, number, map, etc.) is
  field-specific — consult the format's field documentation before casting it.
- `ParserIssue` exposes only `code: ParserIssueCode` and `message: String` — there is no severity
  or field-name property on the issue itself (the field it belongs to is implied by which
  `ParsedField.warnings` list it came from). `ParserIssueCode` and `ParserIssueAdditionalInfoKey`
  are plain Kotlin enums shared across platforms.
- `parser.setOptions(options: Map<String, Any>)` takes a plain Kotlin `Map`, not a per-platform
  options builder. Available keys are format-specific and only meaningful for the formats that
  support them (e.g. GS1 AI: `allowHumanReadableCodes`, `strictMode`; Swiss QR: `strictMode`,
  `minimalVersion`; VIN: `strictMode`, `falsePositiveCompensation`; GS1 Digital Link: `strictMode`,
  `outputHumanReadableString`). HIBC, IATA BCBP, and EPC currently take no options.
- Parsing itself needs **no camera and no camera permission** — a `Parser` only needs a
  `DataCaptureContext` constructed with a license key that has the parser feature enabled. Camera
  setup, `AndroidManifest.xml`/`Info.plist` permission entries, and a scanning mode are only
  needed if you're also capturing barcodes to feed the parser — for that, route the user to
  `barcode-capture-kmp` or `sparkscan-kmp`.
- The license key placeholder is exactly `-- ENTER YOUR SCANDIT LICENSE KEY HERE --`.

## Intent Routing

Based on the user's request, load the appropriate reference file before responding:

- **Creating a Parser, parsing a data string/raw data, reading parsed fields, handling parser
  issues/exceptions, or combining Parser with a barcode scan result** (e.g. "add the Parser to my
  KMP app", "parse this GS1 barcode", "how do I read a HIBC field", "why did parseString throw",
  "parse the barcode I just scanned") → read `references/integration.md` and follow the
  instructions there.
- **Setting up the camera, BarcodeCapture, or SparkScan itself** (not the parser) → this skill
  only covers the Parser half; hand the scanning setup off to `barcode-capture-kmp` or
  `sparkscan-kmp`.
- **AAMVA / driver's license barcode field extraction** → this is not handled by Parser; route to
  an `id-capture-*` skill instead.

## API Usage Policy

Only use APIs that are explicitly documented in the Scandit references below. Do not invent or
guess method signatures, parameters, or property names — and never carry over a signature from the
Android-native or iOS-native SDKs without verifying it also holds for KMP. If unsure whether an API
exists or how it is called — or if a compile error occurs — fetch the relevant reference page
before responding. Do not tell the user to check the docs themselves. After answering, always
include the relevant link so the user can explore further.

**Never construct or guess documentation URLs.** When you need a specific class or property's API
page:
1. First check whether the page you already fetched contains a direct hyperlink to it — topic
   pages link directly to relevant API symbols. Always request links alongside content in your
   fetch prompt.
2. If no direct link was found, fetch the API index (see **Full API reference** in the table
   below), extract the actual link from it, and follow that.

URL structures can vary and guessing will lead to 404s.

## References

Direct users to the right resource based on their question:

| Topic | Resource |
|---|---|
| Get Started | [Get Started](https://docs.scandit.com/sdks/kmp/parser/get-started/) |
| Supported data formats | [Supported Data Formats](https://docs.scandit.com/parser/formats.html) |
| Core concepts (context, integration) | [Core Concepts](https://docs.scandit.com/sdks/kmp/core-concepts/) |
| Combining with scanning | [BarcodeCapture KMP](https://docs.scandit.com/sdks/kmp/barcode-capture/get-started/) · [SparkScan KMP](https://docs.scandit.com/sdks/kmp/sparkscan/get-started/) |
