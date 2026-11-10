---
name: docx
description: "Global Microsoft Word (.docx/.dotx) engine for creating, editing, styling, and reviewing documents. Covers: (1) template and brand extraction, (2) neutral layout, typography, accessibility, and visual QA, (3) academic papers with LaTeX math and managed citations, (4) editorial document generation, (5) data tables, (6) legal redlining, (7) native Word fields, and (8) citation identity and claim-to-evidence verification. Use an attached template or the user's named standard as the source of truth; regional and institutional presets are opt-in only."
license: MIT
---

# Unified DOCX Creation, Editing, Brand & Analysis Suite

The definitive Microsoft Word (`.docx` / `.dotx`) engine for AI coding agents. Choose the optimal execution pathway based on user requirements:

| Task / Domain | Engine / Approach | When to Choose |
|---|---|---|
| **On-Brand Corporate** | `scripts/brandkit/` (`scripts/cli.py`) | Preserving company brand profiles, official fonts, colors, and layout shells fail-closed from templates. |
| **Layout & Visual Linter** | `scripts/audit_layout.py` | Auditing the selected template or named standard for margins, fonts, line spacing, image quality, caption positions, tables, and TOC. |
| **Template Contract** | `scripts/template_rules.py` | Reads the complete `.docx`/`.dotx` package and writes an observed formatting contract in Markdown before any edits. |
| **Final Quality Gate** | `scripts/docx_quality.py` | Checks template drift, heading/page flow, broken cross-references, captions/TOC fields, accessibility, notes, headers/footers, table quality, style hygiene, field refresh, and optional rendering. |
| **Academic & Math** | `scripts/pandoc/compile_academic.py` | Papers with LaTeX math formulas (`$$...$$`), footnotes, and linked Zotero/BibTeX bibliographies. |
| **Citation Verification** | `scripts/citations/verify_citations.py` | Auditing documents for fake/hallucinated DOIs, broken URLs, and metadata mismatches against CrossRef/arXiv/PubMed. |
| **Zotero / Mendeley Citations** | `scripts/zotero/`, citation verifier | Inspecting Zotero fields and validating Zotero or legacy Mendeley Desktop `CSL_CITATION` fields without unlinking. |
| **Data Science Tables** | `scripts/data/dataframe_to_word.py` | Injecting CSV, Excel, or JSON data into styled, zebra-striped Word tables with right-aligned numbers. |
| **Editorial Scratch** | `docx-js` (Node.js script) | New documents from scratch requiring bespoke visual layouts, cover pages, and automated TOCs. |
| **Legal Redline** | Raw OpenXML (`<w:ins>`, `<w:del>`) | Contract reviews, tracked revisions, and multi-file comments (`scripts/comment.py`). |

> Detailed decision logic and routing criteria are in [`references/router-matrix.md`](references/router-matrix.md).

## 0. Mandatory Template-First Contract

Before creating or changing a Word document, ask: **"Apakah ada template Word, pedoman format, atau contoh dokumen yang wajib diikuti? Jika ada, kirimkan file `.docx`/`.dotx` atau pedomannya."**

When a template or reference document exists, do this before authoring:

1. Read the complete Word package, including all XML parts, styles, numbering, headers, footers, section breaks, fields, tables, images, and embedded settings. Do not infer rules from a screenshot alone.
2. Generate a reviewable contract: `python scripts/template_rules.py template.docx -o template-rules.md`.
3. Treat `template-rules.md` as the source of truth for allowed and forbidden formatting. Preserve values that are present in the template and ask before introducing a value that is absent or ambiguous.
4. Use the template shell and Word styles. Do not rebuild its appearance with manual font changes, blank paragraphs, typed numbering, or typed captions.
5. After editing, run the schema validator, the template-based layout audit, and a rendered visual inspection. Do not return the document while any format, overflow, field, or corruption check fails.

If the user confirms that no template or guide exists, ask which baseline to use (for example, APA 7, the `general` profile, or an institutional standard) and record that choice before formatting. Do not silently choose a template.

## 0.1 Writing and Human Voice Contract

DOCX formatting does not replace editorial review. Apply the combined humanizer and antislop-copywriting rules to prose, headings, captions, tables, and callouts:

The detailed checklist is in [`references/prose-rules.md`](references/prose-rules.md).

- Preserve every supported fact from the source. Never invent a number, name, date, quote, citation, result, feature, or testimonial. If a detail is missing, ask for it or write the narrower claim.
- Match the reader and the document type. Technical, academic, legal, and factual documents use plain, precise language. When the user supplies a writing sample, match its vocabulary, sentence length, rhythm, and punctuation.
- State the point directly. Remove staged openers, fake objections, empty transitions, aphorisms, generic conclusions, inflated significance, sales language, and filler phrases.
- Prefer concrete subjects and active verbs when the actor is known. Keep passive voice when the actor is unknown, irrelevant, or deliberately withheld.
- Use the number of examples the content requires. Do not force groups of three, repeated sentence openings, false ranges, or synonym cycling.
- Avoid mechanical formatting in prose: no bolding every key term, all-caps emphasis, decorative emojis, excessive quotation marks, or headings that merely repeat the next sentence.
- Use paragraphs for explanation. Use numbered or bulleted lists only for real sequences, sets of requirements, options, or items that are easier to scan point by point.
- Do not rewrite quotations, titles, code, commands, paths, URLs, field codes, or source data as if they were prose.
- Read the document aloud before delivery. Vary sentence length, remove repeated closers, and check that each sentence adds information.

### Prose delivery gate

Before returning a DOCX, perform three passes: draft the content, audit it for AI patterns and unsupported claims, then revise once more. The final pass must confirm that the document has a clear voice, no fabricated specifics, no unexplained claims, no generic AI vocabulary, no unnecessary list structure, and no em or en dashes in authored prose. This gate does not alter source quotations or Word field syntax.

### Word authoring rules

- Prefer continuous paragraphs. Use bullets or numbered lists only when the content is truly a list, a sequence, or a requirement that benefits from point-by-point scanning.
- Use semantic Heading styles for chapters and subchapters, with a Word-generated Table of Contents when the document has navigable sections.
- Use Word's **References → Insert Caption** for every table and figure. Use **Cross-reference** and **Insert Table of Figures** instead of typed numbers or labels.
- Preserve page size, margins, font family, font size, paragraph spacing, line spacing, tabs, indents, headers, footers, page numbers, and multilevel numbering from the template or approved baseline.
- Keep images and tables within the printable area. Check aspect ratio, effective DPI, row splitting, repeated headers, and page breaks.
- Keep equations as native OMML or editable Word equations. Keep citations as Zotero/Mendeley fields when those fields are present.
- Validate that the output opens as a valid Office package and that fields, styles, numbering, captions, tables, images, headers, and footers remain intact.

### Mandatory LaTeX equation contract

- Write every new mathematical expression in LaTeX source. Use inline math such as `$E=mc^2$` and block math such as `$$\sum_{i=1}^{n} x_i$$`.
- Compile the source through `scripts/pandoc/compile_academic.py`, which converts LaTeX into editable Word OMML equations.
- Do not author formulas as screenshots, raster images, Unicode lookalikes, manually spaced text, or a mixture of unrelated equation formats.
- After conversion, verify that the DOCX contains native `<m:oMath>` or `<m:oMathPara>` elements and that no formula was flattened into an image.
- If the user provides a formula in another format, convert it to LaTeX before inserting it and preserve the original meaning.

---

## 1. On-Brand Corporate Governance & Generation (Brand Engine)

Use this pathway when the user provides or references a company template (`.dotx` / `.docx`) or asks to "match our template", "use our brand kit", or generate an on-brand document from variable content.

### The Seven Verbs
The engine implements three deterministic core verbs plus four model-assisted learning verbs:

| Verb | Input | Output | CLI Command |
|---|---|---|---|
| **extract** | A company `.docx` or `.dotx` template | A reusable Brand Profile (`brand-kit/<name>/`) | `python scripts/cli.py extract --name <brand> --template <template.docx>` |
| **comprehend** *(optional)* | Saved profile + model-authored `comprehension.json` | Profile with validated, cached `comprehension` block | `python scripts/cli.py comprehend --name <brand> --input comprehension.json` |
| **verify** | Saved Brand Profile | QA findings + deterministic verdict | `python scripts/cli.py verify --name <brand>` |
| **generate** | Content (`IntermediateDocument`) + profile | New on-brand `.docx` | `python scripts/cli.py generate --name <brand> --input idoc.json -o out.docx` |
| **learn** | Profile's cross-run history | Recurring findings distilled to shell-frozen overrides | `python scripts/cli.py learn --name <brand> --accept` |
| **propose-overrides** | Residual issues + proposal | Shell-backed corrections fail-closed | `python scripts/cli.py propose-overrides --name <brand> --input overrides.json --accept` |
| **refine** | User feedback delta | Comprehension overlaid for future generations | `python scripts/cli.py refine --name <brand> --input refinement.json --accept` |

### Hard Rules for Brand Generation
1. `scripts/cli.py` (or `scripts/brand_cli.py`) is the launcher. It automatically resolves the engine root.
2. Run preflight (`python scripts/cli.py doctor`) before extraction or generation to verify system readiness.
3. **Extract** opens the template read-only and saves `brand-kit/<name>/template/shell.docx` byte-for-byte.
4. **Generate** opens the saved shell and resolves every semantic block through `profile.json`.
5. **Author role-first, not style-first**: Do not put font names, pt sizes, hex colors, or raw style names in an `IntermediateDocument` (`idoc.json`). Consult `brand-kit/<name>/PROFILE.md` for role vocabulary (`heading`, `paragraph`, `list`, `table`, `caption`, `callout`).
6. See [`references/comprehension.md`](references/comprehension.md), [`references/profile-schema.md`](references/profile-schema.md), and [`examples/intermediate-document.example.json`](examples/intermediate-document.example.json) for full schemas.

---

## 2. Comprehensive Layout, Typography & Visual Linter

Audits Word documents against publication guidelines, institutional templates, or thesis guidelines:

```bash
# 1. Audit against a named built-in standard only when the user selects it
python scripts/audit_layout.py manuscript.docx --profile general

# 2. Extract a complete template contract before editing
python scripts/template_rules.py reference-template.docx -o template-rules.md

# 3. Auto-extract layout criteria directly from any reference template (.docx/.dotx)
python scripts/audit_layout.py manuscript.docx --template reference-template.docx

# 5. Explicit CLI overrides for custom guidelines
python scripts/audit_layout.py manuscript.docx \
  --margins 4.0 4.0 3.0 3.0 \
  --font "Times New Roman" \
  --line-spacing 1.5 \
  --columns 1 \
  --table-caption above \
  --figure-caption below \
  --require-toc \
  --min-dpi 300

# 6. Export structured JSON for automated pipelines
python scripts/audit_layout.py manuscript.docx --format json -o layout_audit.json

# 7. Run the final deterministic quality gate, compare against the template,
#    enable Word field refresh, and produce a PDF render for visual inspection
python scripts/docx_quality.py manuscript.docx \
  --template template.docx --fix-fields --render-dir qa-render \
  --format json --output docx-quality.json

# 8. Check dependencies and use Microsoft Word rendering when Word is installed
python scripts/doctor.py
python scripts/word_visual_qa.py manuscript.docx --pdf qa-render/word.pdf
```

**Checked Dimensions & Standards**:
- **Layout & Page Setup**: Margins (Top, Bottom, Left, Right in cm), Paper Size (A4 vs Letter), Orientation, Columns (1 vs 2 columns), Section Breaks, Hyphenation.
- **Typography & Font Integrity**: Font family consistency, size hierarchy, accidental non-black text (#000000 check), lingering highlight markers.
- **Paragraph & Line Spacing**: Alignment (Justify / `both`), line spacing (Single vs 1.5 vs Double), paragraph spacing before/after.
- **Headings & Structure**: Proper `Heading 1/2/3` styles vs raw unstyled bold text ("Fake Headings" that break Navigation Pane and TOC).
- **Captions & TOC**: Table captions ABOVE table (`Tabel X.Y...`), Figure captions BELOW figure (`Gambar X.Y...`), Table of Contents (`TOC`), List of Tables, List of Figures.
- **Math Equations**: Native OMML / LaTeX (`<m:oMath>`) vs formulas pasted as raster pictures or screenshots.
- **Image Quality & Blurriness**: Effective DPI calculation (<150 DPI critical failure), Laplacian blur variance, aspect ratio distortion (squished/stretched images).
- **Table Formatting**: Column overflow beyond printable margin width, academic three-line tables (no vertical borders), header repeat.
- **Header & Footer**: Page numbering configuration.

The final gate is complementary to the layout linter. It catches template
drift, headings that can orphan on a page, broken REF/PAGEREF fields, missing
alt text and table header markers, inconsistent notes, stale headers/footers,
direct-formatting style drift, and unsafe field refresh state. A non-zero exit
code means a blocking accessibility or integrity finding remains. Rendering
uses Microsoft Word COM when available and falls back to LibreOffice when it is not.

---

## 3. Academic & LaTeX Math Pathway (Pandoc)

Converts Markdown with LaTeX math syntax (`$...$` and `$$...$$`) directly to native Word OMML Equations and resolves citations:

```bash
# Basic compile with native Word equations
python scripts/pandoc/compile_academic.py draft.md -o paper.docx

# Academic compile with Zotero/BibTeX citations and journal CSL style
python scripts/pandoc/compile_academic.py draft.md -o paper.docx \
  --bibliography references.bib \
  --csl ieee.csl \
  --reference-doc template.docx
```

---

## 4. Citation & Reference Verification (Anti-Hallucination)

Detects fake, broken, or mismatched citations in Word documents, BibTeX files, and Markdown drafts against CrossRef, arXiv, PubMed, and Open Library:

```bash
# 1. Audit a Word document (checks Zotero CSL XML and body references)
python scripts/citations/verify_citations.py manuscript.docx

# 2b. Prove that cited sentences have source evidence before delivery
python scripts/citations/verify_citations.py manuscript.docx \
  --claim-audit --strict-claims --format markdown -o claim-audit.md

# 2. Generate a clean Markdown audit report for peer review
python scripts/citations/verify_citations.py draft.md --format markdown -o audit_report.md

# 3. Export machine-readable JSON for CI/CD checks
python scripts/citations/verify_citations.py references.bib --format json -o audit.json
```

---

## 5. Dynamic Zotero and Mendeley CSL Field Management

Never flatten managed citations into static text. Keep dynamic OpenXML field codes (`ADDIN ZOTERO_ITEM CSL_CITATION` or legacy Mendeley `ADDIN CSL_CITATION`) intact. The citation verifier extracts both formats for DOI validation:

```bash
# 1. Inspect existing citations in a document
python scripts/zotero/inspect_zotero.py manuscript.docx

# 2. Inject a new Zotero CSL citation with metadata
python scripts/zotero/inject_zotero.py manuscript.docx \
  --after "MobileNetV3" \
  --citation-text "[39]" \
  --title "Searching for MobileNetV3" \
  --authors "Howard, Andrew; Sandler, Mark" \
  --year 2019 \
  --venue "ICCV" \
  --doi "10.1109/ICCV.2019.00140" \
  -o updated_manuscript.docx

# 3. Validate XML integrity
python scripts/zotero/validate_zotero.py updated_manuscript.docx
```

Modern Mendeley Cite stores part of its library metadata in the Word web-extension package. The verifier validates any DOI, PMID, arXiv ID, or URL exposed by the document and does not rewrite the Mendeley fields. When prose makes a cited claim, run `--claim-audit --strict-claims`: every cited sentence must map to a source identifier and retrieved evidence, otherwise delivery stops with `UNMAPPED_CITATION`, `EVIDENCE_UNAVAILABLE`, or `ABSTRACT_NO_SUPPORT`. Abstract overlap is evidence triage, not proof of detailed or causal claims; those require full-text page/section review.

After modifying citations, the human author opens the document in Microsoft Word and refreshes the owning manager: **Zotero → Refresh** or **Mendeley Cite → refresh/update**. Detailed guide in [`references/zotero.md`](references/zotero.md).

---

## 6. Data Science Tabular Pathway (python-docx)

Injects structured data into professionally styled tables with auto-fitted column widths and number alignment:

```bash
# Append a styled table from CSV or Excel into a document
python scripts/data/dataframe_to_word.py results.csv -o report.docx \
  --title "Tabel 1: Ringkasan Hasil Evaluasi" \
  --header-color "1E2761"
```

---

## 7. Editorial Creation with docx-js

For bespoke documents created from scratch, write a Node.js script using `docx`:

- **Page size:** Default is A4. For US Letter: `page: { size: { width: 12240, height: 15840 } }` (DXA).
- **Tables:** Set `columnWidths` on the table AND `width` on every cell in `WidthType.DXA`.
- **Shading:** Use `ShadingType.CLEAR`, never `SOLID`.
- **Lists:** Use a `numbering` configuration with `LevelFormat.BULLET`, never literal bullets.
- **TOC:** Headings must use built-in `HeadingLevel.*` or set `outlineLevel`.
- **Dot-leader tabs:** Use `PositionalTab` with `leader: PositionalTabLeader.DOT`.

---

## 8. Legal Redlining & Document Surgery (Raw OpenXML)

For contract reviews and deep XML modifications:

```bash
unzip -q doc.docx -d unpacked/
python scripts/merge_runs.py unpacked/          # coalesce fragmented text runs
# edit unpacked/word/document.xml in place
(cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
python scripts/office/validate.py out.docx --original doc.docx
```

- **Tracked changes:** Wrap modified text in `<w:ins>` / `<w:del>` with `w:id`, `w:author`, and `w:date`.
- **Comments:** Use `python scripts/comment.py unpacked/ "Komentar hukum..."` to manage the six cross-linked XML comment files cleanly.

---

## 9. Verification Gate

Run the smallest gate that matches the output:
1. Always run schema validation: `python scripts/office/validate.py out.docx`.
2. Run `audit_layout.py` only when the user supplied a layout standard or template.
3. Run citation verification only when the document contains references, DOI/PMID/arXiv IDs, or URLs.
4. Run Zotero validation only when Zotero fields are present.
5. Render with LibreOffice only when visual layout is part of the request.

## Dependencies

`docx` (npm) · `pandoc` · `python-docx` · `openpyxl` · `Pillow` · `numpy` · `pandas` · `markitdown` · LibreOffice (`soffice`) · `pdftoppm` (Poppler)
