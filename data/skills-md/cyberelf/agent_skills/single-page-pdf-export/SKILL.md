---
name: single-page-pdf-export
description: "Use when the user asks to export a local HTML file, web page, or invitation page to a single-page PDF, a no-pagination PDF, a long PDF with auto-calculated height, or a PDF without headers and footers. Trigger on phrases like 单页 PDF, 不分页, 自动计算长度, 长图 PDF, 去掉页眉页脚, export HTML to single-page PDF, or print page to one PDF page."
---

# Single-Page PDF Export Skill

Export an HTML file or loaded page to a single-page PDF whose height is calculated from the rendered content, with no browser header or footer.

## Use This Skill For

- Local `.html` files that should become a single long PDF
- Pages that should not be split across multiple PDF pages
- Requests to remove browser print headers and footers
- Pages using viewport-height layouts like `min-h-screen` that break normal printing

## Inputs To Resolve

Before exporting, determine:

1. The source page:
   - Local file path like `/user/test/page.html`
   - Or a `file:///`, `http://`, or `https://` URL
2. The output PDF path:
   - If the user does not specify one, default to the source filename plus `-single-page.pdf`

## Workflow

1. Confirm the source exists if it is a local file.
2. Ensure a Chromium-based browser is installed:
   - Prefer Chrome, then Edge
   - The asset script checks common Windows install paths and `CHROME_PATH`
3. Ensure Node dependencies are available in the current workspace:
   - Install `puppeteer-core` with `npm install --no-save puppeteer-core`
   - If you want to verify the resulting page count, also install `pdf-lib`
4. Run the bundled exporter:

```bash
node ./assets/export-single-page-pdf.mjs "<input>" "<output>"
```

5. Validate the result:
   - Confirm the PDF file exists
   - If `pdf-lib` is available, verify page count is `1`

## Validation Command

Use this only when you need to confirm that the PDF is truly single-page:

```bash
node --input-type=module -e "import { readFileSync } from 'node:fs'; import { PDFDocument } from 'pdf-lib'; const bytes = readFileSync(process.argv[1]); const pdf = await PDFDocument.load(bytes); console.log('pages=' + pdf.getPageCount());" "<output.pdf>"
```

## Notes

- The exporter freezes `h-screen` and `min-h-screen` utilities to pixel values before printing. This avoids the common feedback loop where print page height changes the layout height and forces pagination.
- The exporter disables animations and transitions before measuring the page.
- The exporter sets a custom print page size and zero margins, and disables browser headers and footers.

## Troubleshooting

- If `puppeteer-core` is missing, install it in the workspace with `npm install --no-save puppeteer-core`.
- If Chrome or Edge is installed in a non-standard location, set `CHROME_PATH` before running the exporter.
- If the output still splits across pages, rerun the exporter with the bundled script instead of the browser's normal print dialog.
- If the source is a local file with relative assets, prefer passing the local file path instead of pasting raw HTML into a temporary file.

## Expected Outcome

The result should be a single PDF page whose height matches the rendered document, with backgrounds preserved and no header or footer added by the browser.