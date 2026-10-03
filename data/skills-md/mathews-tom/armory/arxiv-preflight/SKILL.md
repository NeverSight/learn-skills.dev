---
name: arxiv-preflight
description: 'Pre-submission validation audit for arXiv papers across TeX source, PDF, figures, metadata, bibliography, file organization, and common-error scans. Produces pass/fail report with specific fixes per arXiv requirement. Triggers on: "check my arXiv submission", "validate for arXiv", "arXiv preflight", "ready for arXiv", "arxiv check", "arxiv submission readiness". Companion to manuscript-review (prose), manuscript-provenance (code), arxiv-figures, arxiv-package.'
metadata:
  version: 1.0.0
  complements:
    [manuscript-review, manuscript-provenance, arxiv-figures, arxiv-package]
  category: review
  tags: [arxiv, preflight, latex, validation, submission]
  difficulty: advanced
  phase: review
---

# arXiv Preflight Check

**Pipeline position:** Phase 3a (submission readiness). Runs after Phase 2
fixes and PDF recompilation. Gate for arxiv-figures and arxiv-package.
See `/manuscript-pipeline` for full execution order.

## Purpose

Systematically validate a TeX/LaTeX project (or PDF submission) against all
arXiv submission requirements, producing a structured pass/fail report with
specific fixes for every violation found.

Companion skills:
- `manuscript-review` — audits prose quality, structure, and claims
- `manuscript-provenance` — audits computational reproducibility
- `arxiv-figures` — optimizes figures for arXiv
- `arxiv-package` — packages the submission tarball

This skill focuses exclusively on arXiv technical compliance — not prose
quality or scientific content.

## Workflow

### 1. Ingest

Identify the submission directory. Locate:
- Main `.tex` file(s)
- All included files (figures, `.bbl`, `.bst`, style files, subdirectories)
- Any `00README.XXX` file
- Any `anc/` directory
- Compiled PDF (if available)

```
Read references/guidelines.md
```

### 2. Validation Passes

Execute all passes. For each check:
- **PASS** — requirement met
- **FAIL** — violation found (document exact file, line, specific fix)
- **WARN** — advisory (not a blocker but may cause issues)
- **N/A** — not applicable

---

**Pass 1 — File Organization**

1. No absolute file paths in any `.tex` file (`\input`, `\includegraphics`, `\include`, `\bibliography`)
2. No spaces or special characters (`&`, `\`, `:`) in filenames
3. No auxiliary files that should be excluded: `.aux`, `.log`, `.toc`, `.lot`, `.lof`, `.dvi`, `.ps`, `.pdf` (except figure PDFs)
4. Required files present: `.bbl` if using BibTeX/BibLaTeX, `.ind` if using makeindex, `.gls`/`.nls` if using glossary/nomenclature
5. No hidden files (starting with `.`) except `.tex`-related configs
6. No journal templates or referee letters included
7. Subdirectory structure: no `\include{}` calls into subdirectories (use `\input{}` instead)
8. If multiple `.tex` files with `\documentclass`: verify `00README.XXX` declares `toplevelfile`

**Pass 2 — TeX/LaTeX Compliance**

1. Processor compatibility: figure formats match processor
   - DVI mode: only `.ps`/`.eps` figures
   - PDFLaTeX: only `.pdf`/`.png`/`.jpg` figures
   - No mixed formats without conditional compilation
2. No `psfig` package usage (use `graphicx`)
3. No `\today` macro in date fields
4. No embedded JavaScript
5. `\pdfoutput` testing uses `ifpdf` package, not `\ifx\pdfoutput\undefined`
6. No shell-escape dependent packages without workarounds (`minted` → `frozencache=true`)
7. No `xr` package for external document references
8. No double-spaced "referee" mode formatting
9. Caption `\cite` calls use `\protect\cite`
10. `\include` not used for subdirectory files
11. BibLaTeX `.bbl` format version compatible with target TeX Live (3.3 for TL2025)
12. All custom/non-standard style files included in submission
13. No packages outside TeX Live distribution (check against common non-TL packages)

**Pass 3 — Figure Validation**

1. All referenced figures exist at specified paths
2. Figure formats match processor requirements
3. No figures reference absolute paths
4. No embedded animations, JavaScript, or interactive elements
5. PNG files: check for oversized images (>34 Megapixel warning)
6. Reasonable file sizes (flag individual figures >5MB, total figures >25MB)
7. Alt text present in `\includegraphics` calls (advisory — accessibility best practice)
8. `\includegraphics` uses `graphicx` package, not deprecated alternatives

**Pass 4 — Bibliography Validation**

1. `.bbl` filename matches corresponding `.tex` filename
2. If `.bib` included: `.bbl` also included (arXiv can process `.bib` but `.bbl` is safer)
3. arXiv identifiers in references use correct format (`YYMM.NNNNN`)
4. No extraneous formatting within e-print identifiers
5. BibLaTeX `.bbl` format version check (examine `\RequirePackage` version in `.bbl`)

**Pass 5 — Metadata Compliance** (check `.tex` front matter)

1. Title: no all-uppercase, no raw Unicode, cryptic macros expanded
2. Authors: proper name format, no honorifics, no `et al.` truncation
3. Abstract: no leading "Abstract" text, within 1920 character limit, no leading whitespace on lines
4. Abstract: opaque TeX macros expanded, no formatting commands (`\em`, `\it`)
5. If comments metadata present: page count and figure count included (advisory)

**Pass 6 — PDF Validation** (if compiled PDF available)

1. All fonts embedded (check with `pdffonts` or equivalent)
2. No Type 3 (bitmap) fonts
3. Machine readable (not scanned/bitmapped)
4. No embedded JavaScript
5. No security restrictions preventing text extraction
6. Reasonable file size

**Pass 7 — 00README.XXX Validation** (if present)

1. Valid directive syntax (each line: `filename directive` or standalone directive)
2. Referenced files exist
3. DVI-related directives use correct filename (no `.tex` extension)
4. No conflicting directives

**Pass 8 — Ancillary Files** (if `anc/` directory present)

1. No `.tex` files in `anc/` directory
2. No PDFs with embedded JavaScript
3. No internal references to `anc/` directory from `.tex` source
4. Reasonable total size

**Pass 9 — Common Error Scan**

1. `%%BoundingBox` at top of PS/EPS files (not at end)
2. No `\Bbbk` conflicts between `newtxmath` and `amssymb`
3. No ambiguous double subscript/superscript (`a_x_y` → `a_{x}_y`)
4. No concatenated source files
5. No Scientific Workplace `.rap` files
6. No modified versions of standard style files (`epsf.sty`, `epsfig.sty`)
7. `hyperref` with complex section names: `bookmarks=false` or proper PDF string handling

---

### 3. Generate Report

Produce a structured report:

```markdown
# arXiv Preflight Report

**Project:** [directory name]
**Date:** [date]
**Processor:** [detected processor]
**Verdict:** [READY / NEEDS FIXES / BLOCKED]

## Summary

| Category | Pass | Fail | Warn | N/A |
|----------|------|------|------|-----|
| File Organization | | | | |
| TeX Compliance | | | | |
| Figures | | | | |
| Bibliography | | | | |
| Metadata | | | | |
| PDF | | | | |
| 00README | | | | |
| Ancillary Files | | | | |
| Common Errors | | | | |

## Blocking Issues (FAIL)

[Each with file, line number, specific violation, exact fix]

## Warnings (WARN)

[Advisory items that may cause processing issues]

## All Checks

[Full pass/fail/warn/N/A status for every checkpoint]
```

### 4. Output

Save report as `arxiv-preflight-report.md` in the project directory.

Present verdict and blocking issue count. If READY, confirm submission can proceed.
If NEEDS FIXES, list the specific fixes in priority order.

## Core Principles

- **Binary compliance.** arXiv requirements are not suggestions — FAIL means the submission
  will be rejected or processing will break. WARN means it may cause issues.
- **Exact fixes.** Every FAIL includes the specific command, line, or file change needed.
- **No false positives.** Only flag violations against documented arXiv requirements.
  Do not impose style preferences or best practices as failures.
- **Processor-aware.** All checks account for the detected TeX processor.
  PDFLaTeX rules do not apply to DVI-mode submissions and vice versa.
