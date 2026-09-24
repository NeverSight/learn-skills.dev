---
name: book-docx-exporter
description: Use to prepare academic book manuscripts for editable DOCX export for Microsoft Word or Google Docs, including page size, margins, heading styles, header/footer, table of contents, captions, bibliography, and metadata/privacy checks.
metadata:
  short-description: Prepare editable DOCX export for academic books
---

# Book DOCX Exporter

Use this specialist when the user needs a DOCX-ready manuscript specification or wants a manuscript prepared for Word/Google Docs editing.

## Agent Contract

Input:

- final or near-final manuscript,
- layout specification if available,
- page size: UNESCO, A5, A4, or custom,
- publisher/campus template requirements,
- bibliography and unresolved citation notes,
- desired DOCX features: TOC, headers, footers, page numbers, captions, styles.

Output:

- `status`: ready, needs_input, blocked_security, or completed.
- `docx_export_spec`.
- `style_map`: title, subtitle, Heading 1/2/3, body, caption, quote, table, exercises.
- `page_setup`: size, margins, orientation.
- `header_footer_plan`.
- `toc_and_lists_plan`.
- `metadata_privacy_check`.
- `unresolved_items`.
- `security_privacy_notes`.

## Process

1. Run security/privacy and document metadata checks.
2. Confirm page size; default to `UNESCO`.
3. Map manuscript elements to editable Word styles.
4. Define table of contents, figure list, table list, bibliography, and appendices.
5. Preserve editability; do not flatten text into images.
6. Recommend PDF export only after DOCX review/layout is approved.

## Rules

- DOCX is the preferred editable handoff format for authors, editors, and publishers.
- Mark missing dimensions as `[exact size needed for technical export]`.
- Do not silently remove unresolved citation gaps.
- If private data or credentials remain, return `blocked_security`.
