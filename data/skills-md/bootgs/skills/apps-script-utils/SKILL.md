---
name: apps-script-utils
description: Documents apps-script-utils, a standalone guard/utility library for Google Apps Script (isX/nonX/requireX convention, A1-notation and sheet helpers, string/number/array helpers, typed exceptions, HTML/JSON/path helpers). Use when writing Apps Script code that needs input guards, spreadsheet range parsing, or common data utilities. Independent of any framework — also used internally by bootgs, so the two pair naturally if the project already uses bootgs. Not for platform quotas and limits (`apps-script-services`), nor for trigger or UI behaviour (`apps-script-triggers`, `apps-script-ui`).
license: Apache-2.0
compatibility: scripts/check-latest-version.sh requires curl and python3.
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
  package: apps-script-utils
---

# Apps Script Utils

## Available files

- **`references/api-reference.md`** — full function catalog by category with signatures. Load on demand (see Categories below).
- **`scripts/fetch_policy.py`** — the shared fetching contract the version check fetches through: it names the script and the repository in the User-Agent, reads `robots.txt` before the target, paces requests, and stops rather than retries on 403/429/503. Vendored from `template/scripts/fetch_policy.py`; don't edit it here.
- **`scripts/check-latest-version.sh`** — checks the current published version against what's installed. Run with `--help` for options.

`apps-script-utils` is a standalone package — no framework required. Install it directly in any Apps Script or plain TypeScript project:

```bash
npm install apps-script-utils
```

It also happens to be a direct runtime dependency of `bootgs` (bootgs's own core imports guards like `isString`/`isObject` from it), so in a bootgs project it's already in `node_modules` and importable with no separate install — see the `bootgs-quickstart` skill. That relationship is one-directional: this package has no dependency on bootgs and works identically with or without it.

Check what's actually published before trusting a function list against a specific version:

```bash
scripts/check-latest-version.sh
```

## The naming convention

Every category in the library follows the same three-function shape — learn it once, and every function name in `references/api-reference.md` is predictable without looking it up:

| Pattern | Signature | Behavior |
|---|---|---|
| `isX(value)` | `value is X` (type guard) | Never throws. Use in conditionals. |
| `nonX(value)` | `boolean` | Negation of `isX`. |
| `requireX(value, message?)` | `X` (narrowed) or throws | Throws a **typed** exception from `exception/` (e.g. `EmptyStringException`, `NullPointerException`) when the guard fails — not a generic `Error`. Returns the narrowed value on success, so it doubles as an assertion. |

Prefer `requireX` at the boundary of a function (repository/service entry points) over manual `if (!x) throw ...` — the thrown exception type is consistent across the whole codebase and callers can `catch` a specific exception class instead of pattern-matching a message string.

This is the target shape the library is rolling out toward, not a guarantee for every existing guard yet — some `isX` functions, particularly in `lang/base`, don't have a `nonX` or `requireX` counterpart published yet. `references/api-reference.md` lists exactly which variants exist per category; don't assume a `nonX`/`requireX` exists for a given `isX` without checking it there first.

## Worked examples

```ts
import { parseA1Notation, requireNonEmptyString, isEmail } from "apps-script-utils";

const range = parseA1Notation("Sheet1!A1:B2"); // -> structured GridRange
const range2 = parseA1Notation("'My Sheet'!5:15"); // quoted sheet names and row-only ranges both parse

const name = requireNonEmptyString(rawInput); // throws EmptyStringException if rawInput is "", null, or undefined

if (isEmail(value)) {
  // value is narrowed to `string` here, and matches a real email format (incl. plus-aliases), not a naive regex
}
```

## Categories

| Category | Contains |
|---|---|
| `appsscript/sheet` | A1-notation parsing/formatting, row helpers, `GridRange` containment checks, sheet lookup/guards — the largest category (~35 functions) |
| `appsscript/{slide,admin,ui,net}` | Service-specific helpers (`isAdmin`, `isUi`, `checkMultipleAccount`, `requireValidToken`) |
| `appsscript/{drive,doc,form}` | Reserved namespaces — currently empty, don't assume functions exist here without checking `node_modules/apps-script-utils/dist` first |
| `lang/base` | Generic guards: `isArray`, `isBoolean`, `isEmpty`, `isNil`, `isObject`, `isString`, ... — `nonX`/`requireX` pairs exist for some but not all of these yet, check `references/api-reference.md` |
| `lang/string` | `toCamelCase`, `toKebabCase`, `toSnakeCase`, `isEmail`, `isValidSlug`, `isValidVersion` + `versionCompare`, `escapeRegExp` |
| `lang/number` | `isInteger`, `toInteger`, `nonNegative` |
| `lang/array` | `chunk`, `is2DArray`, `transpose` |
| `exception/` | `Exception` base class + `NullPointerException`, `IllegalArgumentException`, `EmptyStringException`, `InvalidStringException`, `InvalidEmailFormatException`, `RuntimeException`, `RepositoryIsNotDefinedException`, `ServiceIsNotDefinedException` |
| `net/path` | `join`, `normalize`, `parse`, `isAbsolute`, `isRelative`, `isValidDomain` |
| `net/url` | `isUrl` |
| `html/` | `encodeHtml`, `decodeHtml`, `escapeHtml`, `escapeXml` |
| `json/` | `parseJson`, `stringifyJson` — safe wrappers over `JSON.parse`/`JSON.stringify` |
| `time/` | `now` |

Load `references/api-reference.md` when you need the exact signature of a specific function rather than just knowing it exists.

## Gotchas

- `appsscript/drive`, `appsscript/doc`, `appsscript/form` are placeholder namespaces with no exports yet — don't guess a function name into existence for these services.
- `requireX` exceptions extend the package's own `Exception` base, not `Error` directly in every case. If used inside a bootgs `@ExceptionHandler` (see the `bootgs-validation` skill), catch `Error` (their common ancestor) or the specific exception classes — not bootgs's `AppException`/`HttpException`, which these are unrelated to.

## Verification

- [ ] Ran `scripts/check-latest-version.sh` before relying on a specific function's presence or signature, not just this document.
- [ ] For `appsscript/{drive,doc,form}`, confirmed the function actually exists in `node_modules/apps-script-utils/dist` rather than assuming the namespace is populated.
- [ ] Used the matching `isX`/`nonX`/`requireX` variant instead of hand-rolling an equivalent guard or a generic `if (!x) throw`.
