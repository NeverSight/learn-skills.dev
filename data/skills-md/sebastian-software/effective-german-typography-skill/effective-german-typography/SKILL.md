---
name: effective-german-typography
description: Apply correct German typography rules when writing or reviewing German text. Use when asked to "fix typography", "review typography", write German content, or edit German text in Markdown, HTML, JSX, or plain text. Covers quotation marks, dashes, spaces with units, ellipsis, apostrophes, and regional variants (Germany, Austria, Switzerland).
---

# Effective German Typography

Apply these rules when writing or editing German text. Apply changes silently unless it's a larger transformation task, then provide a short summary.

**Important**: Only apply to visible rendered text. Do not modify code, attribute values, or content intended for copy-paste into source files. Typography rules are suspended inside Markdown code blocks and inline code.

## Quick Reference

| Character | Unicode | Name                   | Usage                  |
| --------- | ------- | ---------------------- | ---------------------- |
| „         | U+201E  | Opening quote (DE/AT)  | „Beispiel"             |
| "         | U+201C  | Closing quote (DE/AT)  | „Beispiel"             |
| ‚         | U+201A  | Opening single quote   | ‚nested'               |
| '         | U+2018  | Closing single quote   | ‚nested'               |
| «         | U+00AB  | Opening guillemet (CH) | «Beispiel»             |
| »         | U+00BB  | Closing guillemet (CH) | «Beispiel»             |
| ‹         | U+2039  | Single guillemet open  | ‹nested›               |
| ›         | U+203A  | Single guillemet close | ‹nested›               |
| –         | U+2013  | En dash                | Ranges, Gedankenstrich |
| −         | U+2212  | Minus sign             | Math only              |
| …         | U+2026  | Ellipsis               | Not three periods      |
| '         | U+2019  | Apostrophe             | Klaus' Haus, O'Brien   |
| ×         | U+00D7  | Multiplication         | 5 × 3                  |
|           | U+00A0  | Non-breaking space     | Before units, %        |
|           | U+2009  | Thin space             | Abbreviations, numbers |
| ẞ         | U+1E9E  | Capital Eszett         | STRAẞE (DE/AT)         |
| ′         | U+2032  | Prime (feet)           | 5′                     |
| ″         | U+2033  | Double prime (inch)    | 10″                    |

## Core Rules

### Quotation Marks

**Germany/Austria**: „Anführungszeichen" with ‚single quotes' for nested.

```
„Er sagte: ‚Komm morgen.'"
```

**Switzerland**: «Guillemets» with ‹single› for nested.

```
«Er sagte: ‹Komm morgen.›»
```

For quotations nested beyond two levels, ask the user for preference.

### Dashes

| Type                  | Character | Usage          | Example                                    |
| --------------------- | --------- | -------------- | ------------------------------------------ |
| Hyphen                | -         | Compound words | Müller-Schmidt                             |
| En dash (no space)    | –         | Ranges         | 2020–2025, 9–17 Uhr, S. 15–20              |
| En dash (with spaces) | –         | Gedankenstrich | Das Wetter – so schön heute – war perfekt. |
| Minus                 | −         | Math formulas  | 5 − 3 = 2                                  |

Avoid em dash (—). Use en dash with spaces for Gedankenstrich.

### Spaces with Numbers and Units

Use non-breaking space (thin space preferred) between number and unit:

```
5 kg, 20 °C, 100 km/h, 50 €, 25 %, 30 ‰
```

**Currency**: Symbol after number with space: `50 €`

**Percent/Permille**: Space before symbol: `25 %`

**Plus/minus**: No space after: `±5 %`

**Section sign**: Non-breaking space: `§ 123`

### Large Numbers

Prefer thin spaces (DIN 5008): `1 000 000`

Periods acceptable based on context: `1.000.000`

If context is unclear, ask user with preference for thin spaces.

**Decimal separator**: Always comma: `3,14`

### Apostrophe

Use typographic apostrophe (U+2019):

```
Klaus' Haus
So'n Quatsch
O'Brien, McDonald's
```

### Ellipsis

Use single ellipsis character (…), not three periods:

```
Er dachte nach …
```

At sentence end, four dots (ellipsis + period):

```
Er sagte noch etwas … .
```

In brackets for omissions: `[…]`

### Abbreviations

Use thin space (or regular space) after periods in abbreviations:

```
z. B., d. h., u. a., usw., etc.
```

At sentence end, only one period:

```
Das gilt für Bücher, Zeitschriften usw.
```

### Ordinal Numbers

Period after number, non-breaking space before following word:

```
1. Platz
der 3. Mai
```

### Time and Date

**Time**: 24-hour format with colon: `14:30 Uhr`

**Time ranges**: En dash without spaces: `9–17 Uhr`, `14:00–15:30`

**Date**: Standard format DD.MM.YYYY: `24.12.2024`

### Footnotes

- Place directly after the word/phrase the footnote refers to
- If referring to whole sentence, place after punctuation

```
Laut Müller¹ ist dies korrekt.
Die Theorie wurde widerlegt.²
```

### Multiplication Sign

Use × (U+00D7) not x:

```
5 × 3 = 15
Bildgröße: 10 × 15 cm
```

### Prime Marks

Keep distinct from quotes for measurements:

```
5′ 10″ (5 feet 10 inches)
```

### Spacing Rules

**Plenken** (wrong): Space before punctuation → Avoid
**Klempen** (wrong): Missing space after punctuation → Avoid

```
Wrong: Das ist falsch , oder ?
Right: Das ist falsch, oder?
```

No space before colon (unlike French):

```
Beispiel: So ist es richtig.
```

### Non-breaking Elements

Use non-breaking space/hyphen to prevent unwanted line breaks:

- Before units: `50 €`
- Before percent: `25 %`
- In phone numbers: `030 123 45 67`
- After section sign: `§ 123`
- After ordinals: `1. Platz`

Use non-breaking hyphen in:

- Phone numbers: `030‑12345`
- ISBN numbers

## Advanced Typography

Apply only where the format supports it (rich text, CSS):

### Small Caps

Use for acronyms and Roman numerals in body text for visual harmony:

```html
<span class="small-caps">NATO</span> <span class="small-caps">XVII</span>.
Jahrhundert
```

### Ligatures

In serif fonts, enable ligatures for: ff, fi, fl, ft

Not applicable to sans-serif fonts.

## Regional Variants

**Default**: Germany German

Only apply Swiss or Austrian rules when there's a clear hint from user or context.

### Swiss German (CH)

- Quotation marks: «Guillemets» and ‹single›
- No Eszett: ß → ss (Straße → Strasse)

### Austrian German (AT)

- Same as Germany German
- Use capital Eszett in all-caps: STRAẞE

### Germany German (DE)

- Quotation marks: „Anführungszeichen" and ‚single'
- Use capital Eszett in all-caps: STRAẞE

## Format-Specific Guidance

### HTML Entities vs Unicode

Check existing context:

- If HTML entities present (`&ndash;`, `&bdquo;`), use entities
- If Unicode characters present, use Unicode
- If unclear, ask user; default to Unicode

Common entities:

| Character | Entity     |
| --------- | ---------- |
| „         | `&bdquo;`  |
| "         | `&ldquo;`  |
| –         | `&ndash;`  |
| …         | `&hellip;` |
| ×         | `&times;`  |
|           | `&nbsp;`   |
|           | `&thinsp;` |

### Markdown/Plain Text

Use Unicode characters directly.

### JSX

Use Unicode in visible text content. Do not modify string literals in code or attributes.

## Related References

- [Print Typography](references/PRINT.md) — Page layout, hyphenation, and PDF generation
