---
name: accessible-pdf
user_invocable: true
description: Make a LaTeX document produce accessible tagged PDFs (PDF/UA-1, PDF/A-2b). Creates a non-destructive copy and Makefile target. Use when the user needs accessible or tagged PDFs.
---

# accessible-pdf — Accessible PDF from LaTeX

Transform a LaTeX document to produce tagged, screen-reader-friendly PDFs compliant with PDF/UA-1 and PDF/A-2b. Applies preamble changes and switches the build to LuaLaTeX. The user chooses whether to edit the original file in place or create a `-accessible` copy with a separate Makefile target.

Reference: <https://yyahn.com/wiki/Accessible-PDF-from-LaTeX/>

## When to Use

- "make my PDF accessible", "tagged PDF", "PDF/UA", "screen reader"
- ADA/accessibility compliance for any LaTeX document (CV, syllabus, report, paper)

## Prerequisites

- **TeX Live 2025+** (the `\DocumentMetadata` tagging framework is recent)
- **LuaLaTeX** and **latexmk** (both ship with TeX Live)
- **pdfinfo** from poppler (for verification): `brew install poppler` on macOS
- **make** (optional) — used for the Makefile target; `latexmk` can be run directly instead

**Windows users**: `make` is not standard on Windows — run `latexmk -lualatex <basename>` directly instead of using the Makefile. Install poppler via `choco install poppler` or `scoop install poppler`.

Check early: run `lualatex --version` and `pdfinfo -v`. If either is missing, tell the user what to install and stop.

## Workflow

### Phase 1: Find, analyze, and plan

#### 1. Find the document

Use the user-provided path. If none given, glob for `**/*.tex` files containing `\begin{document}`. If multiple matches, ask the user to pick. No assumptions about directory structure — this could be a CV, syllabus, report, or paper.

#### 2. Read the preamble

Read everything before `\begin{document}`. Identify:

- `\documentclass` line and options
- All `\usepackage` lines
- Whether `\DocumentMetadata` already exists
- Whether `hyperref` / `\hypersetup` already exists
- Font-related packages: `inputenc`, `fontenc`, `fontspec`, `mathpazo`, `mathptmx`, `newtxtext`, `newtxmath`, `helvet`, `courier`, `libertine`, `libertinus`, `lmodern`, `inconsolata`, etc.
- Symbol packages: `marvosym`, `pifont`, `wasysym`, etc.
- `\title{...}` and `\author{...}` content (needed for hypersetup metadata)
- Language settings from `babel` or `polyglossia`

If the document already has `\DocumentMetadata` and uses `fontspec`, it may already be configured for accessibility. Note this in the questions below.

#### 3. Ask the user

Present all decisions as a single numbered list so the user can answer in one message:

1. **Edit in place or create a copy?** Edit the original `.tex` file, or create `<basename>-accessible.tex` alongside it? (Multi-file projects: only the main file changes either way.)
2. **Makefile?** Add a Makefile target, or just run `latexmk` directly? (If a Makefile already exists, note this.)
3. **Platform?** macOS, Linux, or Windows? (Affects install instructions for poppler and whether `make` is available.)
4. **Build and verify now?** Build the PDF and check tagging after applying changes, or stop after editing?

Use the answers to tailor Phases 2–4 below.

### Phase 2: Apply transformations

#### 4. Apply transformations

Apply these 5 ordered changes to the target file (either the original or the `-accessible` copy):

**a) Add `\DocumentMetadata` block**

Insert before the `\documentclass` line:

```latex
\DocumentMetadata{
  lang = en,
  pdfstandard = a-2b,
  pdfstandard = ua-1,
  pdfversion = 2.0,
  testphase = {phase-II},
}
```

If the document uses `babel` or `polyglossia` with a non-English language, use the appropriate language code instead of `en`.

**b) Replace Type1 font packages with OpenType equivalents**

Add `\usepackage{fontspec}` after `\documentclass` (if not already present). Then apply these replacements:

| Remove | Replace with |
|--------|-------------|
| `\usepackage[utf8]{inputenc}` (any options) | Remove entirely — LuaLaTeX handles UTF-8 natively |
| `\usepackage[T1]{fontenc}` (any options) | Remove entirely — fontspec handles encoding |
| `\usepackage{mathpazo}` or `\usepackage[sc]{mathpazo}` | `\setmainfont{TeX Gyre Pagella}` |
| `\usepackage{mathptmx}` | `\setmainfont{TeX Gyre Termes}` |
| `\usepackage{newtxtext}` | `\setmainfont{TeX Gyre Termes}` |
| `\usepackage{helvet}` (any options) | `\setsansfont{TeX Gyre Heros}` |
| `\usepackage{courier}` | `\setmonofont{TeX Gyre Cursor}` |
| `\usepackage{lmodern}` | Remove entirely — Latin Modern is the LuaLaTeX default |
| `\usepackage{inconsolata}` | `\setmonofont{Inconsolatazi4-Regular.otf}[BoldFont=Inconsolatazi4-Bold.otf]` |
| `\usepackage{libertine}` or `\usepackage{libertinus}` | `\setmainfont{Libertinus Serif}` |

**Math font packages** (`newtxmath`, `eulervm`, `mathpazo` with math features): flag these for the user to review rather than silently replacing. Math font compatibility with LuaLaTeX can be tricky. Add a `% TODO: review math font compatibility` comment.

For any font package not in the table above, add a `% TODO: find OpenType equivalent for <package>` comment and warn the user.

**c) Add/update hyperref accessibility metadata**

If `hyperref` is not loaded, add `\usepackage{hyperref}`.

Add or merge into the existing `\hypersetup`:

```latex
\hypersetup{
  pdftitle={<from \title{}>},
  pdfauthor={<from \author{}>},
  pdflang={en},
  pdfdisplaydoctitle=true,
}
```

Preserve any existing `\hypersetup` keys (like `colorlinks`, `linkcolor`, etc.) — only add the accessibility-specific keys that are missing. `pdfdisplaydoctitle=true` is required for PDF/UA.

**d) Replace symbol font packages**

| Remove | Add | Command mappings |
|--------|-----|-----------------|
| `\usepackage{marvosym}` | `\usepackage{fontawesome5}` | `\Letter` -> `\faEnvelope`, `\Mundus` -> `\faGlobe`, `\Telefon` -> `\faPhone` |

Search the document body (not just the preamble) for uses of replaced commands and apply the mappings. For commands with no known mapping, leave the original with a `% TODO: replace with accessible equivalent` comment.

`pifont` and `wasysym`: keep them but flag for review if heavily used — some of their symbols may lack Unicode mappings.

#### 5. Show the user a summary

List all changes made, organized by category (metadata, fonts, hyperref, symbols). Highlight any `% TODO:` items that need manual attention.

### Phase 3: Makefile target (if requested)

Skip this phase if the user declined a Makefile.

#### 6. Add build target

**Copy mode** — append or create a target:

```makefile
# Accessible PDF (PDF/UA-1, PDF/A-2b) — built with LuaLaTeX
<basename>-accessible.pdf: <basename>-accessible.tex
	latexmk -lualatex <basename>-accessible
```

**In-place mode** — if a Makefile exists with a `pdflatex` target, update it to use `latexmk -lualatex`. Otherwise, append or create:

```makefile
# Build with LuaLaTeX for accessible tagged PDF
<basename>.pdf: <basename>.tex
	latexmk -lualatex <basename>
```

### Phase 4: Build and verify (if requested)

Skip this phase if the user declined building now.

#### 7. Build

Run the appropriate command:
- **Makefile**: `make <basename>-accessible.pdf` (copy) or `make <basename>.pdf` (in-place)
- **No Makefile**: `latexmk -lualatex <basename>-accessible` (copy) or `latexmk -lualatex <basename>` (in-place)

If the build fails, diagnose:

- **Missing fonts**: suggest `tlmgr install <font-package>`
- **Package conflicts with testphase**: suggest downgrading to `phase-I`
- **unicode-math conflicts**: common with certain math packages — flag for user

#### 8. Quick sanity check (pdfinfo)

Run `pdfinfo <output>.pdf` and check:

- **Tagged**: should be `yes`. If `no`, the `\DocumentMetadata` setup needs debugging.
- **Title**: should match the document title. If missing, `\hypersetup` wasn't applied correctly.
- **Author**: should be present.

This is a basic sanity check only — it confirms the PDF has tags and metadata but says nothing about whether the tags are correct or the reading order makes sense.

#### 9. Present summary

Report:
- File locations and build command
- `pdfinfo` results (tagged, title, author)
- Any `% TODO:` items remaining
- **Tell the user they must validate manually.** This skill applies the right LaTeX changes, but real accessibility verification requires external tools:
  - **PDFix Validate** (<https://pdfix.net/products/pdfix-validate/>) — web-based PDF/UA validator; upload the PDF and review the report. This is the recommended first check.
  - **PAC (PDF Accessibility Checker)** — desktop tool, considered the gold standard for PDF/UA validation (Windows only).
  - **macOS VoiceOver** (Cmd+F5 in Preview) — test actual screen reader navigation.
  - **axesCheck** — another web-based checker, though it may flag issues that PDFix does not and vice versa.

## Rules

- Flag uncertain font mappings with `% TODO:` rather than guessing
- Use `testphase = {phase-II}` as default — `phase-III` is more complete but conflicts with more packages
- If the document already appears configured for accessibility, confirm with the user before proceeding
