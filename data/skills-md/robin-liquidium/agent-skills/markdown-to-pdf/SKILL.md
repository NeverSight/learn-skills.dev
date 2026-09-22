---
name: markdown-to-pdf
description: Markdown→PDF via bundled renderer; memos, investor docs, briefs.
---

# Markdown To PDF

Use this skill to render Markdown files into clean local PDFs with the bundled renderer in `scripts/markdown_to_pdf.py`.

## Default behavior
- Prefer a pageless-style PDF: one tall page sized to the content height.
- Use A4 width unless the user asks for something else.
- Keep the output visually minimal and text-first.

## Workflow
1. Confirm the input Markdown path and desired output PDF path.
2. Run the bundled renderer.
3. Use the default fit-to-content mode unless the user explicitly wants standard pages.
4. Verify the PDF was created and report the output path.

## Commands
- Pageless-style default:
```bash
python3 <skill-path>/scripts/markdown_to_pdf.py INPUT.md OUTPUT.pdf
```

- Standard A4 pages:
```bash
python3 <skill-path>/scripts/markdown_to_pdf.py INPUT.md OUTPUT.pdf --page-mode a4
```

- Custom page size:
```bash
python3 <skill-path>/scripts/markdown_to_pdf.py INPUT.md OUTPUT.pdf --page-mode custom --page-width-mm 210 --page-height-mm 297
```

## Notes
- The renderer intentionally supports a narrow Markdown subset: headings, paragraphs, bullets, numbered lists, and simple pipe tables.
- The bundled CSS in `assets/default.css` mirrors the visual direction for browser-based workflows, but the primary path is the local Python renderer.
- If the user asks for a different layout, page size, or denser typography, override the defaults explicitly.
