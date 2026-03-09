---
name: pdf-best-practices
description: Comprehensive guidelines for creating HTML that renders perfectly as PDF documents. Use when generating HTML for PDF conversion, handling page breaks, formatting tables for PDF, optimizing images for print, controlling content density, setting up colors and backgrounds for print, adding headers/footers/page numbers, or creating specific document types like invoices, reports, certificates, and letters. Also use when the user mentions 'HTML to PDF,' 'PDF generation,' 'print CSS,' 'page breaks,' 'PDF layout,' 'PDF tables,' 'PDF images,' 'content density,' 'print styles,' or 'pdfnoodle.'
---

# PDF Best Practices Skill

> Comprehensive guidelines for creating HTML that renders perfectly as PDF documents.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HTML to PDF Pipeline                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐  │
│   │  HTML    │───▶│  PDF Engine  │───▶│  Pagination │───▶│  Final PDF   │  │
│   │ Content  │    │  (Puppeteer) │    │  & Layout   │    │  Document    │  │
│   └──────────┘    └──────────────┘    └─────────────┘    └──────────────┘  │
│        │                                     │                              │
│        ▼                                     ▼                              │
│   ┌──────────┐                        ┌─────────────┐                       │
│   │  CSS     │                        │ Page Breaks │                       │
│   │  Styles  │                        │  & Margins  │                       │
│   └──────────┘                        └─────────────┘                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Reference

| I want to...                              | Read this                                           |
| ----------------------------------------- | --------------------------------------------------- |
| Set up document structure correctly       | [Document Setup](resources/document-setup.md)       |
| Control page breaks                       | [Page Breaks](resources/page-breaks.md)             |
| Format tables for PDF                     | [Tables](resources/tables.md)                       |
| Handle images properly                    | [Images](resources/images.md)                       |
| Optimize content density                  | [Content Density](resources/content-density.md)     |
| Set up colors and backgrounds             | [Colors & Backgrounds](resources/colors.md)         |
| Add headers, footers, page numbers        | [Headers & Footers](resources/headers-footers.md)   |
| Create specific document types            | [Document Types](resources/document-types.md)       |

## Start Here

### Building a new PDF document?
1. Start with [Document Setup](resources/document-setup.md) for the HTML structure
2. Review [Page Breaks](resources/page-breaks.md) to prevent awkward splits
3. Check [Content Density](resources/content-density.md) to avoid sparse pages

### Working with data tables?
1. Read [Tables](resources/tables.md) for formatting and header repetition
2. Apply [Page Breaks](resources/page-breaks.md) to prevent row splitting

### Document has images?
1. Follow [Images](resources/images.md) for sizing and positioning
2. Use [Page Breaks](resources/page-breaks.md) to keep images with captions

### Creating a specific document type?
1. Check [Document Types](resources/document-types.md) for type-specific guidelines
2. Available types: Invoice, Report, Certificate, Letter, Table-heavy, Image-heavy

## Default Configuration

When generating PDFs, use these recommended parameters:

```json
{
  "format": "A4",
  "margin": {
    "top": "40px",
    "right": "40px",
    "bottom": "40px",
    "left": "40px"
  },
  "printBackground": true
}
```

## Quick Checklist

Before generating any PDF:

- [ ] Complete HTML structure with DOCTYPE, html, head, body
- [ ] CSS includes `@page` rule with A4 size
- [ ] Body has `-webkit-print-color-adjust: exact`
- [ ] All images have explicit width/height
- [ ] Tables use thead/tbody structure
- [ ] `page-break-inside: avoid` on logical content blocks
- [ ] Headings have `page-break-after: avoid`
- [ ] No excessive whitespace or sparse pages
- [ ] Font sizes are 9pt or larger
- [ ] Colors have sufficient contrast
- [ ] pdfParams includes format, margins, and `printBackground: true`
