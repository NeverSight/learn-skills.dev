---
name: book-pdf-exporter
description: Use to prepare final PDF export specifications for academic books after layout and DOCX review, with flexible page sizes including default UNESCO, A5, A4, and custom dimensions.
metadata:
  short-description: Prepare final PDF export specifications
---

# Book PDF Exporter

Use this specialist when the manuscript is ready for PDF preview, print proof, or final digital distribution.

## Agent Contract

Input:

- final manuscript or DOCX-ready package,
- layout specification,
- page size: UNESCO, A5, A4, or custom,
- cover specification if included,
- print/digital distribution target,
- publisher/printer requirements.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `pdf_export_spec`.
- `page_size_spec`.
- `print_settings`: margins, bleed, safe area, color mode if relevant.
- `digital_settings`: bookmarks, accessibility, compression if relevant.
- `preflight_checklist`.
- `unresolved_items`.
- `security_privacy_notes`.

## Process

1. Run final security/privacy and metadata check.
2. Confirm final publisher preset and page size; default to `PT. Asadel Liamsindo Teknologi` (UNESCO 15.5x23 cm) for ID or `Asadel Publisher` (Royal 15.6x23.4 cm) for INTL. Supports popular presets (University Press, IKAPI, Springer, Elsevier).
3. Validate that DOCX field codes for Table of Contents (`TOC \o "1-3" \h \z \u`) are updated and resolved prior to PDF export.
4. Verify that Chapter Openers begin on Recto (Odd) pages with 120pt Space Before and hidden running headers.
5. Separate print PDF needs (PDF/X-1a, 300 DPI, mirror margins, bleed) from digital PDF needs (interactive bookmarks, hyperlinked TOC, web reader).
6. Check whether cover PDF and interior PDF need separate export specs.
7. Produce a final preflight checklist.

## Rules

- **Default Text Alignment**: ALL body text paragraphs in generated PDF files, LaTeX settings, and export specifications MUST use **Justified (Rata Kanan-Kiri)** alignment (`\justifying` / `align: justify`) by default.
- **TOC Preflight**: Ensure Microsoft Word TOC field codes or LaTeX `\tableofcontents` are compiled twice to ensure 100% accurate page numbers.
- **Recto Page Alignment**: Enforce odd-page chapter starts (`\cleardoublepage` in LaTeX / Section Break Odd Page in DOCX).
- PDF is the final distribution/proof format, not the preferred editing format.
- Use DOCX for editable review before PDF whenever possible.
- Ask for exact dimensions when `UNESCO` or custom size must become a technical export.
- If credentials, private data, or hidden metadata remain, return `blocked_security`.
