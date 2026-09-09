---
name: front-a11y
description: "Audit or fix accessibility issues (WCAG 2.1 AA) in HTML, Vue, Svelte, or Astro files. Checks images, ARIA, keyboard navigation, forms, and semantic HTML. Usage: /front-a11y [fix]"
argument-hint: "[fix]"
allowed-tools: Read, Edit, Write, Glob
---

Audit or fix accessibility issues in the file that is currently open or explicitly mentioned by the user.

- Default (no arguments): **Audit mode** : analyse the file and produce a structured report of all accessibility issues found.
- If `$ARGUMENTS` contains `fix`: **Fix mode** : apply all automatically-fixable issues directly to the file, then report what was fixed and what requires manual attention.

---

## Step 1 : Detect the file language

Look at the extension of the target file:

- If `.html` → the language file is `front-a11y-html.md`
- If `.jsx` or `.tsx` → the language file is `front-a11y-jsx.md`
- If `.vue` → the language file is `front-a11y-vue.md`
- If `.svelte` → the language file is `front-a11y-svelte.md`
- If `.astro` → the language file is `front-a11y-astro.md`
- Otherwise → inform the user that this file type is not supported. Supported types: `.html`, `.jsx`, `.tsx`, `.vue`, `.svelte`, `.astro`.

The path of this skill file is always available from context. Resolve all sub-file paths relative to it.

---

## Step 2 : Load the shared rules

Read `front-a11y-rules.md` (located in the same directory as this skill file).
It contains all accessibility rules, their severity levels, detection criteria, and fix instructions.

---

## Step 3 : Load the language-specific notes

Read the language file identified in Step 1 (located in the same directory as this skill file).
It contains syntax notes for that language, detection nuances that override or extend the shared rules, and framework-specific additional rules.

---

## Step 4 : Apply both

Apply all rules from `front-a11y-rules.md`, adjusted by the syntax notes and detection nuances from the language file.
Then apply the framework-specific rules from the language file.

---

## Output rules

### Audit mode

- Do **not** modify the file.
- Output a structured accessibility report using this format:

```
## Accessibility Audit : filename.ext

### 🔴 Critical
**[line N] Short issue title**
Element: `<img src="hero.jpg">`
Problem: The `alt` attribute is missing.
Fix: Add `alt="[description]"` for meaningful images, or `alt=""` for decorative ones.

---

### 🟠 Major
...

### 🟡 Minor
...

---

### Summary
| Severity | Count |
|---|---|
| 🔴 Critical | N |
| 🟠 Major | N |
| 🟡 Minor | N |
| **Total** | **N** |
```

- Group issues by severity: Critical → Major → Minor.
- If a severity has no issues, omit that section.

### Fix mode

- Apply all automatically-fixable issues directly to the file.
- Output the **complete corrected file** : do not truncate.
- Preserve all original formatting and indentation.
- After the file, output a **Fix Report**:

```
## Fix Report : filename.ext

### ✅ Fixed
- [line N] Short description of applied fix
- ...

### ⚠️ Requires manual attention
- [line N] Short description + suggested action
- ...
```
