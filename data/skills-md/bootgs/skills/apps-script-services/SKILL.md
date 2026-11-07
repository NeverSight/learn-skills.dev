---
name: apps-script-services
description: Idiomatic, quota-safe patterns for Google Apps Script's built-in services and runtime — batched SpreadsheetApp reads/writes, PropertiesService/CacheService for state, LockService for concurrency safety, UrlFetchApp with retry/backoff, V8 runtime API gaps, and custom spreadsheet function constraints. Use when Apps Script code is slow, hits quota or rate-limit errors, has race conditions from concurrent trigger executions, or needs a browser/Node API that doesn't exist in Apps Script. Framework-agnostic — applies with or without bootgs. Not for menus, sidebars or dialogs (`apps-script-ui`), nor for trigger registration and simple-vs-installable questions (`apps-script-triggers`).
license: Apache-2.0
compatibility: scripts/check-quotas.sh requires curl and python3.
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
---

# Apps Script Services

## Available scripts

- **`scripts/fetch_policy.py`** — the shared fetching contract the script below fetches through: it names the script and the repository in the User-Agent, reads `robots.txt` before the target, paces requests, and stops rather than retries on 403/429/503. Vendored from `template/scripts/fetch_policy.py`; don't edit it here.
- **`scripts/check-quotas.sh`** — fetches current Apps Script quotas/limitations from the official docs (see Checking current quotas below). Run with `--help` for options.

## SpreadsheetApp: batch, don't loop

Every `getValue()`/`setValue()`/`getRange(row, col)` call is a remote call to the Sheets backend — a loop over N cells makes N round trips. Read and write in one call:

```ts
// Slow: N round trips
for (let row = 1; row <= sheet.getLastRow(); row += 1) {
  sheet.getRange(row, 1).setValue(computeValue(row));
}

// Fast: 2 round trips total (one read, one write)
const range = sheet.getRange(1, 1, sheet.getLastRow(), 1);
const values = range.getValues();
const updated = values.map(([value]) => [computeValue(value)]);
range.setValues(updated);
```

`appendRow` inside a loop has the same problem — collect rows and call `getRange(...).setValues(rows)` once, or `sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows)`.

## PropertiesService: size limits

`ScriptProperties`/`UserProperties`/`DocumentProperties` each cap a single value at **9 KB** and the total store at **500 KB**. Storing structured state means `JSON.stringify` on write, `JSON.parse` on read — and checking the serialized size before writing, since GAS throws a generic error on overflow rather than telling you which key exceeded the limit:

```ts
function setJsonProperty(store: GoogleAppsScript.Properties.Properties, key: string, value: unknown): void {
  const serialized = JSON.stringify(value);
  if (serialized.length > 9 * 1024) throw new Error(`Property "${key}" exceeds the 9KB per-value limit`);
  store.setProperty(key, serialized);
}
```

## CacheService: TTL and size limits

Max TTL is 6 hours (`21600` seconds) regardless of what you pass to `put` — a longer value is silently capped, not rejected. Max value size is 100 KB. Use it for expensive-to-recompute, safe-to-lose data (API responses, computed aggregates) — never as a substitute for `PropertiesService` when the value must survive a cache eviction.

## LockService: preventing concurrent-trigger races

Two `onEdit`/`onFormSubmit` executions can genuinely overlap (a user editing while a form submits, or two near-simultaneous edits). Any code that reads-then-writes shared state (a counter, an index, a "next available row") needs a lock around that section:

```ts
function withScriptLock<T>(fn: () => T, timeoutMs = 10_000): T {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(timeoutMs)) {
    throw new Error("Could not acquire script lock — another execution is holding it");
  }
  try {
    return fn();
  } finally {
    lock.releaseLock();
  }
}
```

Use `getScriptLock()` for state shared across all users, `getUserLock()` for per-user state, `getDocumentLock()` for state scoped to one bound document. Always `tryLock` with an explicit timeout and handle the failure — `getLock().lock()` variants that block indefinitely can hang a trigger until it's killed by the execution time limit.

## UrlFetchApp: don't let it throw on non-2xx, and back off on rate limits

By default, a non-2xx response throws, discarding the response body you'd need to debug it. Set `muteHttpExceptions: true` and check the status yourself:

```ts
function fetchWithBackoff(url: string, options: GoogleAppsScript.URL_Fetch.URLFetchRequestOptions, maxRetries = 3): GoogleAppsScript.URL_Fetch.HTTPResponse {
  for (let attempt = 0; attempt <= maxRetries; attempt += 1) {
    const response = UrlFetchApp.fetch(url, { ...options, muteHttpExceptions: true });
    const status = response.getResponseCode();
    if (status < 500 && status !== 429) return response;
    if (attempt === maxRetries) return response;
    Utilities.sleep(2 ** attempt * 1000); // 1s, 2s, 4s, ...
  }
  throw new Error("unreachable");
}
```

## V8 runtime: what's missing, and the service that replaces it

V8 is the only runtime (Rhino was removed) and supports modern syntax — `const`/`let`, arrow functions, destructuring, classes, `async`/`await`. It does **not** include several APIs a browser or Node environment would have; reaching for them produces a `ReferenceError`, not a polyfilled fallback:

| Missing API | Apps Script replacement |
|---|---|
| `setTimeout` / `setInterval` | `Utilities.sleep(ms)` — blocking, not scheduled |
| `fetch` | `UrlFetchApp.fetch()` (see above) |
| `FormData` | Build the payload manually (a query string or JSON body) |
| `URL` | String manipulation, or `net/path`-style helpers from `apps-script-utils` |
| `crypto` | `Utilities.computeDigest()` for hashing, `Utilities.getUuid()` for IDs |

## Custom spreadsheet functions: a restricted execution context

A function used as `=MY_FUNC(...)` in a cell runs in a more restricted context than a menu action or trigger, with limits that don't show up until runtime:

```ts
/**
 * @param {string} input
 * @return {string}
 * @customfunction
 */
function MY_FUNC(input: string): string {
  return input.toUpperCase();
}
```

- The `@customfunction` JSDoc tag is required — without it, the function isn't exposed as a formula even if public.
- Execution limit is **30 seconds**, against the usual 6 minutes for everything else. Both are Google's to change without notice — `scripts/check-quotas.sh "Custom function"` and `scripts/check-quotas.sh "runtime"` return the current numbers.
- Cannot call services that require authorization or UI: `MailApp`, `UrlFetchApp`, `SpreadsheetApp.getUi()`, and triggers are all unavailable. `Utilities` and `CacheService` are fine.

## Checking current quotas

Every numeric limit above (9 KB, 500 KB, 6 hours, quota caps) is Google's to change without notice — a skill that hardcodes them goes stale silently. `scripts/check-quotas.sh` fetches the current numbers straight from the official docs instead of relying on a snapshot baked into this file:

```bash
scripts/check-quotas.sh                # full quotas + limitations table
scripts/check-quotas.sh "Properties"   # just the PropertiesService rows
scripts/check-quotas.sh "runtime"      # execution time limits
```

Exits `3` with nothing on stdout if the keyword matches no rows, `2` if the docs page couldn't be fetched or parsed — see `--help` for the full reference.

It covers everything on the docs page's quotas/limitations tables (execution time, triggers, `PropertiesService`, `UrlFetchApp`, email). It does not cover `CacheService`'s TTL/size caps, which live on a separate reference page — those are long-stable (6 hour max TTL, 100 KB max value) but verify against [the CacheService reference](https://developers.google.com/apps-script/reference/cache/cache) if precision matters.

## Verification

- [ ] No `getValue`/`setValue`/`appendRow` call sits inside a loop over rows — replaced with one batched `getValues`/`setValues` call.
- [ ] Any `PropertiesService` write of structured data checks serialized size against the 9 KB per-value limit before writing.
- [ ] Any handler that reads-then-writes shared state across concurrent trigger executions is wrapped in a `LockService` lock with an explicit timeout.
- [ ] `UrlFetchApp.fetch` calls set `muteHttpExceptions: true` and check `getResponseCode()` explicitly, with backoff on 429/5xx.
- [ ] No code assumes `setTimeout`, `fetch`, `FormData`, `URL`, or `crypto` exist — each has an Apps Script replacement in use instead.
- [ ] Every `@customfunction` avoids `MailApp`, `UrlFetchApp`, and `SpreadsheetApp.getUi()`, and completes well under the custom-function runtime limit (30 seconds at the time of writing — `scripts/check-quotas.sh "Custom function"` confirms it).
