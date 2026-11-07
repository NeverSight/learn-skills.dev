---
name: i18n-and-localization
description: >-
  A framework-neutral review lens for internationalizing a web UI: ICU
  MessageFormat messages keyed by meaning, CLDR plural and gender selection,
  locale-aware date, number, currency, and list formatting with `Intl`,
  right-to-left and bidirectional text, locale in the URL with negotiation and
  `hreflang`, and the message-catalog lifecycle (fallback, lazy loading,
  pseudo-localization). Composes with `react`, `angular`, and `vue` for the i18n
  library API. Use it when the user mentions i18n, l10n, internationalization,
  localization, translation, ICU MessageFormat, plurals, `Intl`, RTL, bidi,
  locale routing, `hreflang`, `Accept-Language`, or a message catalog.
license: CC-BY-4.0
metadata:
  author: danielteles
  version: "1.0"
---

# Internationalization and Localization — Review Skill

The i18n review lens for web UI: how user-facing text is authored so it can be translated, how
values are formatted per locale, how right-to-left and bidirectional text are handled, and how the
locale is chosen and the catalog delivered. Framework-neutral — the rules hold for any i18n library;
examples use ICU MessageFormat and the `Intl` API.

> **Builds on.** `react` / `angular` / `vue` for the i18n library that implements these rules
> (FormatJS, @angular/localize, vue-i18n), `accessibility` for the lang and dir semantics and
> screen-reader language switching, and `styling-and-design-tokens` for the logical CSS properties
> that make a layout work in RTL. On a conflict, this skill sets the i18n requirement, the
> framework skill picks the API, `accessibility` owns the lang semantics, and
> `styling-and-design-tokens` owns the CSS mechanism. Load a sibling only when the task turns on
> its layer; if it is not loaded, apply that layer from general knowledge and do not block.

This SKILL.md is self-sufficient: the **Ruleset** below is the complete, enforceable list. Each
`references/<topic>.md` holds that group's reasoning and `❌ / ✅` code, and
`references/worked-example.md` a full review pass; open them for depth when your runtime allows.

---

## How to Use This Skill

Pick the mode that matches the task. Do the steps in order.

| Mode | Steps |
|---|---|
| **Generate** — add user-facing text or formatting for a feature | 1. Every string is an ICU message with a meaning-based key and a translator description; no concatenation (`messages`). 2. Count-dependent text uses `plural` / `selectordinal`; person-dependent text uses `select` (`plurals-gender`). 3. Dates, numbers, currency, relative time, and lists go through `Intl` with the active locale (`formatting`). 4. The layout uses logical properties and isolates interpolated values for bidi (`rtl-bidi`). 5. Run the Ruleset as a checklist. Fix each fail before you hand off. |
| **Review** — check a pull request or a diff | 1. Run the Ruleset against the diff. 2. Write one finding per fail, in the Output Format below. 3. Order the findings: `must-fix` first, then `consider`. 4. If nothing fails, say so in one line. Do not invent findings. |
| **Audit** — assess an existing surface for i18n readiness | 1. Grep for hardcoded user-facing strings, string concatenation building sentences, and `count === 1` ternaries. 2. Find manual date/number formatting and `toLocaleString()` calls with no locale. 3. Check `<html lang>` / `dir`, run the UI in a pseudo-locale and an RTL locale. 4. Check locale negotiation, the URL scheme, and `hreflang`. 5. List findings by Ruleset topic. |

### Output Format

Write one finding per line:

```
<severity> · <topic> · <file>:<line> — <what is wrong>. <the fix as an action>.
```

- `<severity>` is `must-fix` (a string that cannot be translated correctly, or a locale that renders wrong) or `consider` (works, but a rule prefers another
  form).
- `<topic>` is a Ruleset topic slug (`messages`, `plurals-gender`, `formatting`, `rtl-bidi`, `locale-routing`, `catalog`).

### Rules for Every Mode

- Name the Ruleset topic when you enforce a rule.
- Assume the translation is longer, has different word order, pluralizes differently, and may read right-to-left. A string that only works in English is a bug.
- Never build a sentence by concatenating translated fragments — grammar, order, and agreement do not survive it.

---

## Ruleset

### messages → `references/messages.md`

- [ ] Every user-facing string is an externalized message, not a literal in the component or a hardcoded attribute.
- [ ] A message is one complete sentence or phrase with named ICU placeholders (`{name}`, `{count}`) — never assembled from concatenated or interpolated
      sub-strings.
- [ ] Messages are keyed by meaning or location (`checkout.payButton`), not by their English text.
- [ ] Each message ships a description / context note for translators, and a screenshot or usage where the tool supports it.
- [ ] Inline formatting (bold, a link) inside a message uses ICU rich-text tags or the library's component interpolation, not HTML strings spliced together.
- [ ] Strings are extracted by a tool from the source of truth; there is no separate hand-maintained list that drifts.

### plurals-gender → `references/plurals-gender.md`

- [ ] Any count-dependent text uses ICU `plural` with CLDR categories (`one`, `other`, and `zero` / `two` / `few` / `many` where a locale needs them) — never
      `count === 1 ? 'item' : 'items'`.
- [ ] Ordinals ("1st", "2nd") use `selectordinal`, not a suffix table.
- [ ] Text that varies by gender or another enum uses ICU `select` with an `other` branch, not string branching in code.
- [ ] The number that drives the plural is passed as a message argument and rendered with `#` inside the message.
- [ ] An `=0` / `=1` exact match is used only for a genuinely special sentence, with the category branches still present.

### formatting → `references/formatting.md`

- [ ] Dates and times are formatted with `Intl.DateTimeFormat` (or the library wrapper) with the active locale and an explicit time zone — never manual
      `getMonth()` string-building or a fixed pattern.
- [ ] Numbers, percentages, and units use `Intl.NumberFormat`; currency uses it with a `currency` code and the locale, and the amount is stored in minor units,
      not a float.
- [ ] Relative time ("in 3 days") uses `Intl.RelativeTimeFormat`; lists ("A, B, and C") use `Intl.ListFormat` — not a hand-joined string with a hardcoded
      conjunction.
- [ ] `toLocaleString()` / `toLocaleDateString()` are never called without an explicit locale argument.
- [ ] Server-rendered formatted values are produced with the request's locale and time zone, not the server's, and match what the client would render (no
      hydration mismatch).
- [ ] Collation-sensitive sorting of user-visible lists uses `Intl.Collator`, not the default code-unit sort.
- [ ] String length, truncation, and character counts use `Intl.Segmenter` (grapheme clusters), never `.length` / `slice`.
- [ ] Language, region, and currency names shown to the user (a locale switcher) come from `Intl.DisplayNames`, not a hand-written map.

### rtl-bidi → `references/rtl-bidi.md`

- [ ] `dir` is set (on `<html>`, from the locale) and flips to `rtl` for RTL locales; the app is verified in at least one RTL locale.
- [ ] Layout uses flow-relative logical properties and values (`margin-inline`, `inset-inline-start`, `text-align: start`) — no physical `left` / `right` in
      directional layout (mechanism: `styling-and-design-tokens`).
- [ ] A value interpolated into a sentence (a name, an ID, a file path) is bidi-isolated — `<bdi>`, the library's isolate, or Unicode isolate characters.
- [ ] User-generated content of unknown direction is rendered with `dir="auto"`.
- [ ] Directional icons (back / forward arrows, send, undo) are mirrored in RTL; a logo or a play button is not.
- [ ] No layout math assumes LTR (e.g. computing an offset from the left edge, or `text-align: left` for "start").

### locale-routing → `references/locale-routing.md`

- [ ] The active locale is in the URL — a path segment (`/de/…`) or a subdomain; a cookie alone is not enough.
- [ ] First-visit locale is negotiated from `Accept-Language` against the supported set, with a defined default fallback; the user's explicit choice is then
      persisted and wins.
- [ ] Each localized page has `hreflang` alternates (including `x-default`) and a self-referential canonical.
- [ ] `<html lang>` matches the rendered locale exactly (region included where it matters), and it updates on a client-side locale switch.
- [ ] SSR renders the requested locale's messages and formats on the first response — no default-locale flash corrected after hydration.

### catalog → `references/catalog.md`

- [ ] A missing translation falls back to the default locale (or a defined chain), never renders the raw key or an empty string, and is reported.
- [ ] Locale message bundles are loaded on demand for the active locale, not all locales bundled into the main chunk.
- [ ] CLDR / plural data is loaded per locale alongside its messages, not assumed present.
- [ ] A pseudo-localization pass runs in development or CI (accented, padded, bracketed text) to surface hardcoded strings, truncation, and concatenation before
      translators do.
- [ ] The build fails or warns on an untranslated key in a shipping locale and on an unused key in the catalog.
- [ ] Message keys are stable across releases; a removed key is deprecated, not silently dropped mid-cycle.

---

## Limits

This skill is the internationalization of a web UI. It does not cover:

- Translation itself — vendor choice, TMS workflow, MT post-editing, glossary and style-guide authoring, linguistic QA.
- Content strategy and localization of imagery, video, legal copy, and pricing.
- Backend and data-layer i18n — locale-aware collation in the database, multi-currency accounting, per-region data residency.
- The framework's i18n library API in depth — `react-intl` components, `@angular/localize` build pipeline, `vue-i18n` config. Those are `react` / `angular` /
  `vue`.
- The CSS mechanism for RTL (logical properties, `:dir()`), which is `styling-and-design-tokens`; this skill states that the layout must be direction-agnostic.
- Accessibility beyond `lang` / `dir` and language-of-parts — the full lens is `accessibility`.
- Right-to-left typography and complex-script shaping (Arabic joining, Indic clusters) beyond "use the platform text stack and test it".

This skill states what makes a UI translatable and locale-correct. It is not a substitute for running the product in a real translation and a real RTL locale.

---

## References

This skill composes with:

- **`react`** / **`angular`** / **`vue`** — the i18n library and its API (FormatJS / `react-intl`, `@angular/localize` and `$localize`, `vue-i18n`), message
  extraction, and the framework's SSR locale wiring.
- **`accessibility`** — `lang` on the document and on foreign-language spans, `dir`, and announcing a language change; the full lens lives there.
- **`styling-and-design-tokens`** — logical properties and `:dir()` are how a layout survives an RTL locale; this skill requires direction-agnostic layout, that
  skill supplies the CSS.
- **`architecture-and-design`** — where the message catalog and locale state sit in the app structure.
