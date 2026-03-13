---
name: PDF Generator
slug: pdf-generator
description: Create and manipulate professional PDF documents with formatting, images, and metadata
category: document-creation
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create pdf"
  - "generate pdf document"
  - "convert to pdf"
  - "pdf from markdown"
  - "make a pdf"
tags:
  - pdf
  - documents
  - conversion
  - formatting
---

# PDF Generator

The PDF Generator skill enables creation of professional PDF documents from various sources including Markdown, HTML, plain text, and structured data. It handles formatting, images, metadata, watermarks, and multi-page layouts. This skill leverages Node.js libraries like `puppeteer`, `pdfkit`, or `jsPDF` for comprehensive PDF generation capabilities.

Whether you need to convert documentation to PDF, generate reports with charts, create printable forms, or produce client deliverables, this skill provides the tools and workflows to create publication-quality PDFs programmatically.

## Core Workflows

### Workflow 1: Convert Markdown to PDF
**Purpose:** Transform Markdown files into formatted PDF documents with styling

**Steps:**
1. Read the source Markdown file
2. Parse Markdown to HTML using a library like `marked`
3. Apply CSS styling for professional appearance
4. Use Puppeteer to render HTML as PDF with proper page breaks
5. Add metadata (title, author, creation date)
6. Save to specified output path

**Implementation:**
```javascript
const puppeteer = require('puppeteer');
const marked = require('marked');
const fs = require('fs');

async function markdownToPdf(mdPath, outputPath, options = {}) {
  const markdown = fs.readFileSync(mdPath, 'utf8');
  const html = marked.parse(markdown);

  const styledHtml = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body { font-family: 'Helvetica', sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        blockquote { border-left: 4px solid #3498db; padding-left: 20px; color: #7f8c8d; }
      </style>
    </head>
    <body>${html}</body>
    </html>
  `;

  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(styledHtml);
  await page.pdf({
    path: outputPath,
    format: 'A4',
    margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' },
    printBackground: true,
    ...options
  });
  await browser.close();
}
```

### Workflow 2: Generate Multi-Page PDF Report
**Purpose:** Create structured reports with headers, footers, page numbers, and sections

**Steps:**
1. Define report structure (cover page, TOC, sections, appendix)
2. Create PDFKit document instance
3. Add cover page with title, logo, date
4. Generate table of contents with page references
5. Add sections with consistent formatting
6. Include headers and footers on each page
7. Add page numbers and finalize

**Implementation:**
```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

function generateReport(data, outputPath) {
  const doc = new PDFDocument({
    size: 'A4',
    margins: { top: 50, bottom: 50, left: 50, right: 50 }
  });

  const stream = fs.createWriteStream(outputPath);
  doc.pipe(stream);

  // Cover page
  doc.fontSize(28)
     .text(data.title, { align: 'center' })
     .moveDown(2)
     .fontSize(14)
     .text(`Generated: ${new Date().toLocaleDateString()}`, { align: 'center' });

  doc.addPage();

  // Table of contents
  doc.fontSize(20).text('Table of Contents', { underline: true });
  doc.moveDown();
  data.sections.forEach((section, idx) => {
    doc.fontSize(12)
       .fillColor('blue')
       .text(`${idx + 1}. ${section.title}`, { link: `#section${idx}` })
       .fillColor('black');
  });

  // Sections
  data.sections.forEach((section, idx) => {
    doc.addPage();
    doc.fontSize(18)
       .fillColor('black')
       .text(section.title, { destination: `section${idx}` });
    doc.moveDown();
    doc.fontSize(11).text(section.content, { align: 'justify' });
  });

  // Add page numbers
  const pages = doc.bufferedPageRange();
  for (let i = 0; i < pages.count; i++) {
    doc.switchToPage(i);
    doc.fontSize(10)
       .text(`Page ${i + 1} of ${pages.count}`,
             50, doc.page.height - 50,
             { align: 'center' });
  }

  doc.end();
}
```

### Workflow 3: Batch Convert HTML to PDF
**Purpose:** Convert multiple HTML files to PDFs in a single operation

**Steps:**
1. Scan directory for HTML files or accept file list
2. Set up Puppeteer browser instance (reuse for efficiency)
3. For each HTML file:
   - Load HTML content
   - Apply standard styling
   - Render to PDF with consistent settings
   - Save with corresponding filename
4. Close browser and report results

### Workflow 4: Add Watermark to Existing PDF
**Purpose:** Apply text or image watermarks to PDF documents

**Steps:**
1. Load existing PDF using pdf-lib
2. Get all pages
3. For each page:
   - Draw watermark text (diagonal, semi-transparent)
   - OR overlay watermark image
4. Save modified PDF
5. Preserve original metadata

**Implementation:**
```javascript
const { PDFDocument, rgb, degrees } = require('pdf-lib');
const fs = require('fs');

async function addWatermark(inputPath, outputPath, watermarkText) {
  const existingPdfBytes = fs.readFileSync(inputPath);
  const pdfDoc = await PDFDocument.load(existingPdfBytes);
  const pages = pdfDoc.getPages();

  pages.forEach(page => {
    const { width, height } = page.getSize();
    page.drawText(watermarkText, {
      x: width / 2 - 100,
      y: height / 2,
      size: 48,
      color: rgb(0.75, 0.75, 0.75),
      opacity: 0.3,
      rotate: degrees(-45)
    });
  });

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(outputPath, pdfBytes);
}
```

### Workflow 5: Merge Multiple PDFs
**Purpose:** Combine multiple PDF documents into a single file

**Steps:**
1. Create new PDF document
2. Load each source PDF
3. Copy all pages from each source
4. Append to new document
5. Save merged PDF with combined metadata

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Convert Markdown to PDF | "convert [file.md] to pdf" |
| Generate report from data | "create pdf report from [data]" |
| Batch convert HTML | "convert all html files to pdf" |
| Add watermark | "add watermark [text] to [file.pdf]" |
| Merge PDFs | "merge [file1.pdf] and [file2.pdf]" |
| Extract pages | "extract pages 1-5 from [file.pdf]" |
| Compress PDF | "compress [file.pdf]" |
| Add metadata | "set pdf metadata for [file.pdf]" |

## Best Practices

- **Page Sizing:** Always specify format ('A4', 'Letter') and orientation for consistency
- **Margins:** Use minimum 15mm margins for printability
- **Fonts:** Embed fonts or use standard PDF fonts (Helvetica, Times, Courier) for compatibility
- **Images:** Compress images before embedding to reduce file size
- **File Size:** Monitor PDF size; use compression for files over 5MB
- **Accessibility:** Include document structure tags for screen readers when possible
- **Metadata:** Always set title, author, and creation date metadata
- **Page Breaks:** Use CSS `page-break-before` or `page-break-after` for controlled pagination
- **Testing:** Test PDFs in multiple viewers (Adobe, Preview, browsers)
- **Security:** Offer password protection and permission settings for sensitive documents
- **Validation:** Verify PDF/A compliance if archival quality is required
- **Batch Operations:** Reuse browser instances when converting multiple files

## Common Patterns

**Documentation Export:**
```javascript
// Convert project README to PDF with styling
await markdownToPdf('./README.md', './docs/README.pdf', {
  headerTemplate: '<div style="font-size:10px; text-align:center;">Project Documentation</div>',
  footerTemplate: '<div style="font-size:10px; text-align:center;">Page <span class="pageNumber"></span></div>',
  displayHeaderFooter: true
});
```

**Invoice Generation:**
```javascript
// Create PDF invoice from template
const doc = new PDFDocument();
doc.pipe(fs.createWriteStream('invoice.pdf'));
doc.fontSize(20).text('INVOICE', { align: 'center' });
doc.fontSize(12).text(`Invoice #: ${invoiceNumber}`);
doc.text(`Date: ${date}`);
// ... add line items, totals, etc.
doc.end();
```

## Dependencies

Install required packages:
```bash
npm install puppeteer pdfkit pdf-lib marked
```

## Error Handling

- **File Not Found:** Verify source file paths before processing
- **Memory Issues:** For large PDFs, use streaming and chunk processing
- **Font Errors:** Fallback to standard fonts if custom fonts fail to load
- **Rendering Timeout:** Increase Puppeteer timeout for complex pages
- **Permissions:** Handle read/write permission errors gracefully

## Performance Tips

- Reuse Puppeteer browser instances for batch operations
- Use PDF compression for files with many images
- Cache rendered HTML for repeated conversions
- Process large PDFs page-by-page rather than loading entirely into memory
- Use worker threads for parallel PDF generation