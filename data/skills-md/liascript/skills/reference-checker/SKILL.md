---
name: reference-checker
description: >
  Verifies scientific literature references for accuracy and produces a structured report.
  Always use when the user wants to check, verify, or validate bibliographic entries, citations,
  or references — including individual ones. Always outputs a complete reference verification report
  with per-entry ratings (three-tier: ✅ correct / ⚠️ warning / 🚨 critical error) and a summary table.
  Also use for: 'check my references', 'verify citations', 'are my sources correct?',
  'Stimmen die Angaben?', 'Sind die Quellen korrekt?', 'Bitte Referenzen checken',
  or similar verification requests. Output language always matches the user's input language.
license: CC0-1.0
---

# Reference Checker

This skill systematically verifies scientific literature references using web search and always outputs results in a consistent, three-tier format.

---

## Workflow

### 1. Extract References
Extract and number all references to be checked from the user's input.

### 2. Web Search per Reference
Perform **separate web searches** for each reference. Search strategy:
- Primary: Title + journal + year
- Secondary: Authors + title (if no results)
- Tertiary: Search DOI directly (if provided)
- Quaternary: Patent databases / institutional repositories (for patents, reports, theses)

Verify the following:
- **Authors:** Full names, order, correct spelling; for "et al." check at least the first author
- **Title:** Exact wording
- **Journal / Source:** Correct name
- **Year:** Publication year (note online-first vs. print publication date)
- **Volume:** Number
- **Page or article number:** First page or article number (e.g., 123603)
- **Document type:** Article, patent, dissertation, report, conference paper, etc.
- **DOI:** Retrieve and validate
- **URL:** Retrieve direct URL to the publication

### 3. Output Language
Always respond **in the same language as the user's request** (English, German, or other).

---

## Three-Tier Rating System

### ✅ — CORRECT
The reference is complete and all verified details match. Minor formatting differences (e.g., spacing, abbreviations) do not count as errors.

### ⚠️ — WARNING
The reference exists and is findable, but has issues that should be fixed before submission. Typical ⚠️ cases:
- **Year error:** Online-first year ≠ print year (e.g., online 2014, printed 2015)
- **Incomplete details:** Missing authors, missing volume/page numbers, missing patent numbers
- **Non-standard format:** Only a URL provided (e.g., institutional repository), no complete citation style
- **Minor errors:** Slight typos in author names, wrong initials, slightly different title
- **Missing document type:** Dissertation/patent/report not identified as such

### 🚨 — CRITICAL ERROR
Severe errors that compromise the integrity of the reference. Typical 🚨 cases:
- **Not verifiable / possibly hallucinated:** No match despite extensive search; plausible-sounding details with no real counterpart — often a sign of AI-generated false citations
- **Wrong journal:** Article exists but was published in a different journal
- **Wrong authors:** Completely different author group
- **Wrong page numbers/article numbers:** Significant deviation from actual details
- **Wrong first author**

---

## Output Format (ALWAYS follow)

### Report Title
```
## Reference Verification Report
```
(English) or
```
## Referenzprüfungsbericht
```
(German)

---

### Per Reference: Individual Rating

```
### [N] ✅ — CORRECT
[Brief confirmation]. DOI: ... URL: ...

### [N] ⚠️ — [ERROR DESCRIPTION IN UPPERCASE]
[Explanation of the problem and correct details].
DOI: ... URL: ...

### [N] 🚨 — [ERROR DESCRIPTION IN UPPERCASE]
[Explanation; explicitly flag hallucination suspicion if applicable].
Correct details (if a similar paper was found):
DOI: ... URL: ...
```

**Note on hallucination suspicion (🚨):** If a reference cannot be found despite multiple searches and the title, journal, volume, and pages are plausible but unverifiable, always include the warning: *"This appears to be a hallucinated/AI-generated reference. Do not use without verification."* (or in German: *"Diese Referenz scheint halluziniert/KI-generiert zu sein. Nicht ohne Überprüfung verwenden."*)

---

### Summary Table

**Always** append a table at the end of the report. Columns: Number | Status emoji | Main issue.

**English:**
```markdown
## Summary Table

| # | Status | Issue |
|---|--------|-------|
| [1] | ✅ | Correct |
| [2] | ⚠️ | [Brief description] |
| [3] | 🚨 | [Brief description] |
```

**German:**
```markdown
## Zusammenfassende Tabelle

| Nr. | Status | Problem |
|-----|--------|---------|
| [1] | ✅ | Korrekt |
| [2] | ⚠️ | [Kurzbeschreibung] |
| [3] | 🚨 | [Kurzbeschreibung] |
```

If multiple references have 🚨 status, append a **notice block** at the end of the table:

```
> **Key concern:** References [X], [Y], [Z] bear the hallmarks of AI-generated (hallucinated)
> citations. These should be replaced with verified sources or removed before submission.
```
(or German equivalent)

---

## Complete Error Category Reference

| Category | Symbol | Typical Cases |
|----------|--------|---------------|
| Correct | ✅ | All details verified |
| Year error | ⚠️ | Online-first vs. print year |
| Incomplete | ⚠️ | Missing authors, volume, pages |
| Non-standard | ⚠️ | URL only, no complete citation style |
| Typo | ⚠️ | Minor deviations in names/title |
| Wrong document type | ⚠️ | Patent/dissertation not identified |
| Wrong journal | 🚨 | Paper exists but published elsewhere |
| Wrong authors | 🚨 | Completely different author group |
| Wrong pages/article no. | 🚨 | Significant deviation |
| Not verifiable | 🚨 | No match; hallucination suspected |
| Wrong first author | 🚨 | First author does not match |

---

## Rules

1. **Always search** — never assess a reference from memory, even for well-known classics.
2. **Always include DOI and URL** — even for ✅ references.
3. **Never skip a reference** — every entry appears in the report.
4. **Summary table is mandatory** — it closes every report.
5. **Keep language consistent** — English or German depending on the request, maintained throughout.
6. **For ambiguous matches** try at least 3 different search strategies before assigning 🚨.
7. **Distinguish page numbers vs. article numbers** correctly.
8. **Check online-first vs. print carefully** — the correct citation year is the print publication year unless explicitly stated otherwise.
9. **Patents and reports** follow their own citation standards: inventor, applicant, patent number, country, date.
10. **Recognize hallucination patterns:** Plausible title + real journal + unverifiable pages/numbers = strong indicator of AI-generated false citation → always warn explicitly.
