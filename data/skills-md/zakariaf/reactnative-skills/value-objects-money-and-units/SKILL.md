---
name: value-objects-money-and-units
description: Stores money as ISO 4217 minor units, quantities in canonical units, instants as epoch ms. Use when adding a price, currency, tax, split, unit or timestamp, or a total is a cent off. Not for calendar days (dates-streaks-and-statistics).
---

# Value objects: money, units and instants

Every amount, quantity and moment in an Expo app is stored once, in one canonical integer form
(minor units plus an ISO 4217 code, a canonical unit, epoch milliseconds), changed only by pure
tested functions that never lose or invent a minor unit, and turned into text only at the edge, so a
language, digits or unit-system change on iOS or Android never corrupts a stored value. Two
zero-dependency checkers prove it on the app's own code.

## Rules that must hold

1. **Money is `Money`: an integer count of minor units plus an ISO 4217 code** (`money(minor, currency)`
   from `src/core/money/money.ts`), in types, state, rows and APIs; a plain number field is named
   `<what>Minor`. Never a float, a major-unit number or a formatted string. Why: binary floats cannot
   hold 0.01, and a total drifts in a way nobody can re-derive. (`float-money`, `money-integer`)
2. **Scale only by the ISO 4217 exponent, from the generated table; an unknown code is a typed
   failure.** JPY 0, USD 2, KWD 3, CLF 4 decimals; `parseCurrencyCode` returns `unknown-currency`.
   Never `* 100`, `/ 100`, `toFixed(2)` or `?? 2`, and never the exponent from Intl/CLDR, whose display
   digits differ for 16 codes (IQD 3 vs 0). Why: a hard-coded 100 is a 100× error in yen and 10× in
   dinars, and Intl formats an unknown code like `ZZZ` with two decimals instead of refusing it.
   (`hard-coded-scale`, `exponent-default`, `exponent-table`, `unknown-currency`)
3. **One currency per aggregate; arithmetic only through the Money functions.** `addMoney`,
   `subtractMoney`, `sumMoney`, `compareMoney` throw on mixed currencies and unsafe integers; changing
   currency is `convertMoney` with an explicit rate, rounded once. No arithmetic on `.minor` outside
   `src/core/money/`. Why: EUR plus USD is a bug, not data, and only the functions check it.
   (`raw-minor-arithmetic`, `cross-currency`, `convert-money`)
4. **Every division of money goes through `allocate()`** (largest remainder, ties to the lower index):
   bill splits, prorated tax or discounts, instalments, `splitEvenly`. Never divide and round each
   part. Why: the parts then sum to the whole to the exact minor unit, for any input, every time.
   (`money-division`, `allocate-vectors`, `allocate-conservation`, `allocate-refuses`)
5. **Rates are exact ratios applied once, at the total, with a named rounding mode.**
   `parsePercent('8.25')`, `basisPoints(825)`, `applyRate(amount, rate, 'half-even')`, `includedTax`
   for tax-inclusive prices; then `allocate()` the result. Never `amount * 0.0825`, never round an
   intermediate sum. Why: the percent-to-minor-units step is the second rounding site that allocate
   tests never see. (`money-float-rate`, `apply-rate`)
6. **Text and vendor values enter exactly, at the boundary.** Input is normalized at the edge
   (`normalizeDecimalInput` with the app's locale tag), then `parseMoney` reads it in the currency's
   exponent and refuses extra decimals (`too-many-decimals`), never rounding silently, and a group
   separator only where it can stand (`ambiguous-separator`: English `1,000` is asked about once,
   the price of never reading a 1000× amount); store prices enter through
   `moneyFromStoreDouble` (expo-iap's `price` double, both platforms) or `moneyFromMicros` (Android
   subscription micros), and the price shown to pay is the store's own `displayPrice`. Why: `parseFloat('19.99')` is already
   wrong, and Arabic-Indic digits throw in a naive parser. (`parse-money`, `store-price`)
7. **Format only at the edge, in `src/i18n/`:** `formatMoney(amount, localeTag)` or
   `useFormatMoney()`, with fraction digits set to the ISO exponent and the value passed as exact
   decimal text. No `style: 'currency'` elsewhere, no currency symbol glued to a number, no formatting
   in `src/core/`. Why: the forced FormatJS polyfill then prints the same text in Jest, on iOS and on
   Android, in the person's digits, and a float input is a cent off past 2^53 / 100.
   (`currency-format-edge`, `currency-fraction-digits`, `currency-symbol-literal`, `core-formats`)
8. **Derive totals; store inputs.** An order total, a balance or a share is computed on read from
   its lines and rates; a stored figure is a fact of record (the amount actually charged) and is named
   so (`chargedMinor`). Entities link by stable id, never by embedded copies. Why: a stored total is
   stale the moment a line changes, and two sources drift.
9. **A physical quantity is an integer in its dimension's canonical unit, named with the unit**
   (`durationMs`, `distanceMm`, `weightG`, `volumeMl`, `sizeBytes`). Conversion uses exact factors
   (a mile is 1,609,344 mm) and rounds once, half-even, into the canonical unit; the unit system
   (expo-localization `measurementSystem`, or a setting) only changes the display.
   Why: miles typed and kilometres typed must be the same row. (`unit-suffix`, `units-exact`)
10. **An instant is UTC epoch milliseconds, `<what>AtMs` in code and `<what>_at_ms INTEGER` in
    SQLite.** ISO 8601 text exists only at the wire, always with `Z` or an offset, parsed once by
    `parseIsoInstant` (offset-less text is refused) and written by `toIsoInstant`; never a `Date`
    object or a string in state or storage; seconds from an API convert once. A calendar day is a
    local DateKey (dates-streaks-and-statistics). Why: local text means a different moment on every
    phone, and seconds read as milliseconds land in 1970. (`instant-type`, `instant-column`,
    `instant-parse`)
11. **Persist and send the canonical form.** SQL money is `<name>_minor INTEGER NOT NULL` in a STRICT
    table with the currency as `TEXT` on the aggregate; JSON money is decimal text with its code or an
    integer of minor units, never a JSON float; a schema field is `v.pipe(v.number(),
    v.safeInteger())`. Why: STRICT refuses a REAL in an INTEGER column, and `AVG()` returns REAL.
    (`money-column`, `instant-column`, `float-money`)
12. **The value-object core is pure and proven.** `src/core/{decimal,money,units,time}/` import only
    `src/core` (BigInt arithmetic, no React Native, Expo or Intl) and every module ships its test
    with the pinned vectors and properties. Why: one tested core makes every rule above a
    millisecond test, and the checker can run the app's own modules. (`money-core`, `core-tests`,
    `module-load`, `missing-module`)

## Workflow

1. **Read the reference for the task:**

   | Task | Read |
   |---|---|
   | Money type, currencies, exponents, conversion, store prices, iOS/Android behaviour | [references/money-model.md](references/money-model.md) |
   | Splitting, tax, tip, discounts, rounding modes, the two rounding sites | [references/allocation-and-rates.md](references/allocation-and-rates.md) |
   | Showing money or quantities, an amount input field, digits, RTL | [references/edge-formatting-and-input.md](references/edge-formatting-and-input.md) |
   | Distances, weights, durations, timestamps, API dates | [references/units-and-instants.md](references/units-and-instants.md) |
   | SQLite columns, JSON and API shapes, store state, test recipes | [references/storage-and-tests.md](references/storage-and-tests.md) |
   | A checker failure, the allow marker, options, NOT APPLICABLE | [references/checkers.md](references/checkers.md) |

2. **Check the prerequisites.** `src/core/result.ts` (error-handling-typed-results; a synced copy is
   in `templates/src/core/`), the i18n layer with the forced FormatJS polyfills and `localeTagFor`
   (i18n-strings-and-catalogs), and the render helpers (unit-and-component-tests) for the hook tests.
3. **Copy the templates** to the paths their first lines name: always `templates/src/core/decimal/`
   and `templates/src/core/money/`; `templates/src/core/units/` for physical quantities;
   `templates/src/core/time/` for instants; `templates/src/i18n/` (`format-money`, `use-format-money`,
   `use-locale-tag`, `normalize-decimal-input`, `format-quantity`). Each ships with its test. Trim the
   exponent table only by deleting rows; never edit an exponent.
4. **Model the domain** with `Money` fields, the currency on the aggregate, rates as `Rate`, quantities
   and instants as unit-named integers, and derived results in their own types
   ([examples/order-split.ts](examples/order-split.ts)).
5. **Convert at every boundary, once:** repository rows ([examples/order-row.ts](examples/order-row.ts)),
   migrations ([examples/v0002-create-orders.ts](examples/v0002-create-orders.ts); the migration
   itself follows persistence-and-migrations), API responses
   ([examples/order-response.ts](examples/order-response.ts)), store products
   ([examples/product-price.ts](examples/product-price.ts)), input fields
   ([examples/use-amount-field.ts](examples/use-amount-field.ts)).
6. **Split and rate** with `applyRate` once at the total, then `allocate()` by the subtotals; test the
   sum property ([examples/order-split.test.ts](examples/order-split.test.ts)).
7. **Show values** from model hooks with `useFormatMoney()`, `useLocaleTag()` and `formatQuantity`;
   components receive finished strings.
8. **Test first for any rule change**, then
   `npx jest src/core/decimal src/core/money src/core/units src/core/time src/i18n --ci --selectProjects unit`
   and `npm run typecheck`.
9. **Run the checks** from the repo root: `node ${CLAUDE_SKILL_DIR}/scripts/check-value-core.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-value-code.mjs .`; fix every `FAIL` line (file, rule and fix
   are printed) and rerun until both print `RESULT: PASS`.

## Definition of done

- [ ] No money field, column or schema holds a float or a major-unit number; every amount is `Money`
      or `<what>Minor`, and every `value-objects-allow` marker carries its reason.
- [ ] Scaling, splitting and rates go through the core (`parseMoney`, `toDecimalString`, `allocate`,
      `applyRate`, `convertMoney`); no `* 100`, `/ n`, `* 0.08` or `.minor` arithmetic outside it.
- [ ] Money is formatted only by `formatMoney` / `useFormatMoney()` in `src/i18n/`, with ISO digits.
- [ ] Totals are derived; stored figures are facts of record and named so.
- [ ] Quantities and instants are unit-named integers; ISO text is parsed once with an offset.
- [ ] The core modules and their tests are the templates or pass the same tests; `npm run typecheck`
      and the Jest run in workflow step 8 pass.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-value-core.mjs .` prints `RESULT: PASS` (an app with no
      money, units or instant module prints `NOT APPLICABLE: no value-object core: ...`).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-value-code.mjs .` prints `RESULT: PASS`.

## Anti-patterns

- **`price: number` holding 19.99.** Store `Money` (or `priceMinor: number` holding 1999).
- **`(priceMinor / 100).toFixed(2)` for display.** Wrong for JPY and KWD, Latin digits only, no
  symbol placement. `formatMoney(price, localeTag)`.
- **`EXPONENTS[code] ?? 2`, or digits from `resolvedOptions().maximumFractionDigits`.** An unknown
  code is a failure; CLDR says IQD has 0 decimals where ISO 4217 says 3.
- **`Math.round(total / people)` for each person.** Three people and 10.00 give 3.33 × 3 = 9.99.
  `splitEvenly(total, 3)` gives 3.34, 3.33, 3.33.
- **`subtotal * 0.0825`, or recomputing a printed tax from its rate.** Keep the rate exact and apply
  it once; a tax the receipt states is the ground truth.
- **Summing separately rounded parts to get a total.** Round the total once, then allocate it.
- **`a.minor + b.minor` in a feature.** It skips the currency and overflow checks; `addMoney(a, b)`.
- **`` `$${amount}` `` or `'€' + text`.** The symbol position, spacing and digits are the locale's.
- **`parseFloat(text)` on a price field, or `Number('١٢٫٥')`.** Normalize, then `parseMoney`.
- **Storing `total` next to the lines it sums.** Derive it; it is stale after the next edit.
- **`createdAt: Date` in a store, `created_at TEXT` in SQLite, `new Date('2026-10-10T08:30')`.** Epoch
  ms in `createdAtMs`; offset-less text is local time on an unknown phone.
- **`distance: number` with no unit, or storing miles because the person chose miles.** Canonical
  integer, unit in the name, convert for display.
- **Showing `formatMoney(productPrice)` as the price to pay.** Show the store's `displayPrice`; keep
  the Money for arithmetic.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/money-model.md](references/money-model.md) | Decisions and reasons, the Money API, the ISO 4217 table and its refresh, CLDR differences, safe ranges, BigInt on Hermes, conversion, store prices (expo-iap 5.8.0), iOS/Android table, pitfalls | Workflow step 1; any money type or currency change |
| [references/allocation-and-rates.md](references/allocation-and-rates.md) | Largest remainder with verified vectors, the split pipeline, the two rounding sites, rounding modes, tax-inclusive prices, discounts and refunds, edge policies | Workflow steps 1 and 6 |
| [references/edge-formatting-and-input.md](references/edge-formatting-and-input.md) | `formatMoney` facts verified under the polyfill, digits and RTL marks, display options, caching, amount inputs and keyboards, store display prices, unit formatting | Workflow steps 1, 5 and 7 |
| [references/units-and-instants.md](references/units-and-instants.md) | Canonical units and exact factors, choosing granularity, temperature, durations versus days, instants, ISO 8601 at the wire, seconds versus milliseconds, Date pitfalls | Workflow steps 1 and 4 |
| [references/storage-and-tests.md](references/storage-and-tests.md) | SQLite types and aggregates (verified), STRICT tables, JSON and API shapes, valibot, Zustand state, test recipes and property tests | Workflow steps 5 and 8 |
| [references/checkers.md](references/checkers.md) | Both checkers' rules, scopes and name lists, the allow marker, options, expected output, troubleshooting, multi-package | Workflow step 9, and when a check fails |
| `templates/src/core/decimal/` | `decimal.ts` (exact decimal text), `rounding.ts` (`divideRounded`, rounding modes) and tests | Workflow step 3, always |
| `templates/src/core/money/` | `currency-exponents.ts` (generated ISO table), `currency.ts`, `money.ts`, `allocate.ts`, `rate.ts`, `money-text.ts`, `store-price.ts` and tests | Workflow step 3, always |
| `templates/src/core/units/` | `units.ts` (dimensions, exact factors, parse and display) and its test | Workflow step 3, for quantities |
| `templates/src/core/time/` | `instant.ts` (`parseIsoInstant`, `toIsoInstant`, epoch seconds) and its test | Workflow step 3, for instants |
| `templates/src/core/result.ts` | The Result type (synced from error-handling-typed-results; do not edit here) | Workflow step 2, only when the app lacks it |
| `templates/src/core/result.test.ts` | Its test (synced; do not edit here) | With `result.ts` |
| `templates/src/i18n/` | `format-money.ts`, `use-format-money.ts`, `use-locale-tag.ts`, `normalize-decimal-input.ts`, `format-quantity.ts` and tests | Workflow step 3, with the i18n layer |
| [examples/order-split.ts](examples/order-split.ts) | An Order shared between Accounts: subtotals, tax and tip, all closed by `allocate()`, derived | Workflow steps 4 and 6 |
| [examples/order-split.test.ts](examples/order-split.test.ts) | Its worked example and the sum property | Workflow step 6 |
| [examples/order-row.ts](examples/order-row.ts) | Repository rows to Money and back, with typed failures | Workflow step 5 |
| [examples/v0002-create-orders.ts](examples/v0002-create-orders.ts) | A migration with `_minor`, `_at_ms`, `_on` and `_bps` columns, no stored total | Workflow step 5 |
| [examples/order-response.ts](examples/order-response.ts) | An API response schema and its one conversion | Workflow step 5 |
| [examples/product-price.ts](examples/product-price.ts) | A store product's price to Money (Android subscription micros, else the double), with the allow marker | Workflow step 5 |
| [examples/use-amount-field.ts](examples/use-amount-field.ts) | A money input's model hook: normalize, parse, message by failure kind | Workflow step 5 |
| `scripts/check-value-code.mjs` | Scans `src/` for float money, hard-coded scales, raw arithmetic, formatting outside the edge, unit-less names, wrong SQL columns, a missing or untested core | Workflow step 9 |
| `scripts/check-value-core.mjs` | Runs the app's money, units and instant modules against the rules (vectors, 400 seeded splits, ISO table) | Workflow step 9 |
| `scripts/lib/value-names.mjs` | The money, physical and instant name lists both checkers use | When a name is misjudged |
| `scripts/lib/sql-columns.mjs` | Reads column names and types from SQL in string literals | Never by hand |
| `scripts/lib/value-core-checks.mjs` | The currency, Money and allocation checks | When a core rule changes |
| `scripts/lib/value-edge-checks.mjs` | The rate, conversion, text, store-price, unit and instant checks | When an edge rule changes |
| `scripts/lib/app-modules.mjs` | Imports the app's pure TypeScript (synced from the library; do not edit here) | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source lexer and helpers (synced from the library; do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared checker library (synced from the library; do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and examples and catch every planted bug | After changing a checker, a rule, a template or an example |
| `assets/iso-4217.json` | ISO 4217 exponents (list one, published 2026-09-17) and the 16 CLDR differences | When refreshing the currency table |
| `assets/shared.json` | The synced-file manifest | Never by hand |
| `tests/` | `bases/app/` and `fixtures/` (overlay cases for both checkers) | When a self-test case changes |

## Related skills

- `error-handling-typed-results` - the Result type and failure kinds the parsers return.
- `i18n-strings-and-catalogs` - locale tags, digits, the forced polyfills and catalog messages.
- `dates-streaks-and-statistics` - local calendar days, the clock and day arithmetic.
- `persistence-and-migrations` - tables, STRICT migrations and repositories.
- `networking-and-server-state` - the ApiClient and response validation at the wire.
- `in-app-purchases` - the purchase flow and the store's product prices.
- `forms-and-input` - text fields, keyboards and form validation around an amount field.
- `state-management-zustand` - stores that hold Money and derive totals in selectors.
- `unit-and-component-tests` - Jest setup, render helpers and property tests.
