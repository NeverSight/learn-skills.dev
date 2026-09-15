---
name: kisnet-ytm
description: "Retrieve Korean KIS-NET YTM Matrix data through the standalone ytm CLI or @sjunepark/ytm Node SDK. Use when requests ask for KIS-NET bond yields for a date, yield history over dates or the latest N observations, or supported bond kinds. Excludes general yield-to-maturity calculations, investment advice, other data providers, and repository maintenance."
---

# KIS-NET YTM

Use the standalone CLI installed from a GitHub Release. In the repository
checkout, replace `ytm` below with `bun run cli --`; this invokes the Rust/Clap
binary. The Node package is a private development SDK; the release pipeline
publishes only the CLI. For an in-process Node integration, import
`YtmClient` and the operation-specific validation helpers from `@sjunepark/ytm`.

```sh
ytm kinds --format json
ytm history --count 180 --end-date 2026-09-08 --format json
ytm matrix --base-date 2026-06-08 --kind 국채 --format json --pretty
ytm matrix --base-date 2026-06-07 --kind 80 --fallback previous-available --lookback-days 10 --format json
```

- For the latest N observation dates, use `history --count N --end-date YYYY-MM-DD`,
  with optional inclusive `--start-date`. Count is 1–2000; the exact backward
  scan stops within 2000 calendar days. Do not combine count with a date list
  or previous-available fallback. A shortfall raises `insufficient_history`.
- A numeric yield anywhere qualifies a date; missing cells may remain. Report
  `requestedDates.length` as the selected date count and preserve `countSelection`.
  `availableCount` counts date/category pairs, not dates.
- Dates accept `YYYY-MM-DD`, `YYYY.MM.DD`, or `YYYYMMDD`.
- Kind accepts a source code or Korean label. The canonical catalog includes
  `80` 회사채(사모), distinct from `70` 회사채(무보증).
- Exact-date lookup is the default. Use `previous-available` only when the
  caller authorizes walking backward through calendar dates.
- Date fallback runs only after confirmed unavailable data. Eligible transient
  transport failures retry within bounded attempt and retrieval budgets;
  exhausted transport failures, protocol failures, and source-format failures
  abort retrieval rather than selecting an earlier date.
- JSON is the default agent-readable output. Execution and invalid-invocation
  failures are structured JSON; inspect their recovery metadata before
  retrying. `ytm help <unknown>` instead prints a plain-text help error and
  exits with status 2.
- Report requested and resolved dates, kind, tenors, and rows by 적용대상채권.
  Source `-` or empty yields become `null` while raw text remains available.

```js
import { YtmClient, validateMatrixInput } from "@sjunepark/ytm";

const client = new YtmClient();
const validation = validateMatrixInput({
  baseDate: "2026-06-08",
  kind: "회사채(사모)"
});
if (!validation.ok) throw validation.error;
const result = await client.matrix(validation.input);
```
