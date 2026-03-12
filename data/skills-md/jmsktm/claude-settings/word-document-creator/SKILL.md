---
name: Word Document Creator
slug: word-document-creator
description: Generate Microsoft Word .docx files with formatting, tables, images, and styles
category: document-creation
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create word document"
  - "generate docx"
  - "make word file"
  - "create .docx"
  - "word document from template"
tags:
  - word
  - docx
  - microsoft-office
  - documents
  - templates
---

# Word Document Creator

The Word Document Creator skill provides comprehensive capabilities for generating Microsoft Word (.docx) documents programmatically. It handles formatting, styles, tables, images, headers, footers, and complex layouts using the `docx` library for Node.js. This skill is essential for automated document generation, report creation, and template-based workflows.

Create everything from simple letters to complex reports with tables, charts, images, and custom styling. The skill supports both creation from scratch and template-based generation with variable replacement.

## Core Workflows

### Workflow 1: Create Formatted Document from Scratch
**Purpose:** Build a Word document with headings, paragraphs, lists, and formatting

**Steps:**
1. Import `docx` library and create Document instance
2. Define styles for headings, body text, lists
3. Add sections with headers and footers
4. Create paragraphs with formatting (bold, italic, color, alignment)
5. Add numbered and bulleted lists
6. Insert tables with formatting
7. Export to .docx file

**Implementation:**
```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');
const fs = require('fs');

async function createDocument(outputPath) {
  const doc = new Document({
    sections: [{
      properties: {},
      headers: {
        default: new Header({
          children: [new Paragraph({ text: "Company Name", alignment: AlignmentType.RIGHT })]
        })
      },
      children: [
        new Paragraph({
          text: "Business Proposal",
          heading: HeadingLevel.HEADING_1,
          alignment: AlignmentType.CENTER
        }),
        new Paragraph({
          children: [
            new TextRun({ text: "Prepared for: ", bold: true }),
            new TextRun("Client Name")
          ]
        }),
        new Paragraph({
          text: "Executive Summary",
          heading: HeadingLevel.HEADING_2
        }),
        new Paragraph({
          text: "This proposal outlines the scope, timeline, and budget for the project...",
          alignment: AlignmentType.JUSTIFIED
        })
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
}
```

### Workflow 2: Generate Document from Template
**Purpose:** Use a template Word file and replace placeholders with actual data

**Steps:**
1. Load template .docx file using `pizzip` and `docxtemplater`
2. Define data object with replacement values
3. Set data to template
4. Render template with substitutions
5. Handle loops for repeated sections (tables, lists)
6. Handle images and conditional sections
7. Export final document

**Implementation:**
```javascript
const Docxtemplater = require('docxtemplater');
const PizZip = require('pizzip');
const fs = require('fs');

function generateFromTemplate(templatePath, data, outputPath) {
  const content = fs.readFileSync(templatePath, 'binary');
  const zip = new PizZip(content);

  const doc = new Docxtemplater(zip, {
    paragraphLoop: true,
    linebreaks: true
  });

  // Data object with placeholder values
  doc.setData({
    clientName: data.clientName,
    projectName: data.projectName,
    date: new Date().toLocaleDateString(),
    items: data.items, // Array for looping
    total: data.total
  });

  doc.render();

  const buf = doc.getZip().generate({
    type: 'nodebuffer',
    compression: 'DEFLATE'
  });

  fs.writeFileSync(outputPath, buf);
}

// Template placeholders: {clientName}, {projectName}, etc.
// Loop syntax: {#items}{name} - {price}{/items}
```

### Workflow 3: Create Document with Tables and Images
**Purpose:** Build complex documents containing data tables and embedded images

**Steps:**
1. Create Document instance
2. Define table with rows and columns
3. Set cell formatting (borders, shading, alignment)
4. Add table headers with bold styling
5. Populate data rows
6. Insert images with sizing and positioning
7. Add captions to images
8. Export document

**Implementation:**
```javascript
const { Document, Packer, Paragraph, Table, TableRow, TableCell, Media } = require('docx');
const fs = require('fs');

async function createTableDocument(data, imagePath, outputPath) {
  const image = Media.addImage(doc, fs.readFileSync(imagePath), 300, 200);

  const doc = new Document({
    sections: [{
      children: [
        new Paragraph({ text: "Sales Report Q4 2025", heading: HeadingLevel.HEADING_1 }),
        new Table({
          rows: [
            // Header row
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph({ text: "Month", bold: true })] }),
                new TableCell({ children: [new Paragraph({ text: "Revenue", bold: true })] }),
                new TableCell({ children: [new Paragraph({ text: "Growth", bold: true })] })
              ]
            }),
            // Data rows
            ...data.map(row => new TableRow({
              children: [
                new TableCell({ children: [new Paragraph(row.month)] }),
                new TableCell({ children: [new Paragraph(row.revenue)] }),
                new TableCell({ children: [new Paragraph(row.growth)] })
              ]
            }))
          ]
        }),
        new Paragraph({ text: "" }), // Spacing
        new Paragraph({ text: "Revenue Trend Chart", heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ children: [image] }),
        new Paragraph({ text: "Figure 1: Quarterly Revenue Trend", italics: true })
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
}
```

### Workflow 4: Batch Generate Documents
**Purpose:** Create multiple personalized documents from a data source

**Steps:**
1. Load data source (JSON, CSV, database)
2. Load document template
3. For each record:
   - Create new document instance
   - Populate with record data
   - Apply formatting
   - Save with unique filename
4. Track success/failure for each document
5. Generate summary report

### Workflow 5: Add Advanced Formatting
**Purpose:** Apply styles, fonts, colors, spacing, and page layout

**Steps:**
1. Define custom styles in document
2. Create style hierarchy (heading levels, body, captions)
3. Set font families, sizes, colors
4. Configure paragraph spacing and indentation
5. Set page margins and orientation
6. Add page numbers and section breaks
7. Apply themes and color schemes

**Implementation:**
```javascript
const doc = new Document({
  styles: {
    paragraphStyles: [
      {
        id: "CustomHeading",
        name: "Custom Heading",
        basedOn: "Heading1",
        next: "Normal",
        run: {
          size: 32,
          bold: true,
          color: "2E74B5",
          font: "Calibri"
        },
        paragraph: {
          spacing: { before: 240, after: 120 }
        }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1440 = 1 inch
      }
    },
    children: [
      new Paragraph({ text: "Styled Heading", style: "CustomHeading" })
    ]
  }]
});
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create new document | "create word document [name]" |
| From template | "generate docx from template [file]" |
| Add table | "add table with [rows] rows to [doc]" |
| Insert image | "insert [image] into word doc" |
| Batch generate | "create word docs for each [data]" |
| Apply style | "format word doc with [style]" |
| Add header/footer | "add header [text] to document" |
| Create TOC | "generate table of contents" |

## Best Practices

- **Styles Over Direct Formatting:** Define and use styles for consistency and easy updates
- **Templates:** Use templates for repeated document types (contracts, reports, letters)
- **Page Layout:** Set margins, orientation, and page size early in document creation
- **Tables:** Use table styles for professional appearance and easy maintenance
- **Images:** Compress images before embedding; use appropriate resolution (150-300 DPI)
- **Headers/Footers:** Keep them simple and consistent across sections
- **File Size:** Monitor document size; avoid embedding high-resolution images unnecessarily
- **Compatibility:** Test documents in different Word versions if targeting broad audience
- **Data Validation:** Validate input data before template substitution to avoid errors
- **Error Handling:** Gracefully handle missing template placeholders
- **Version Control:** Use template versioning for document types that evolve
- **Accessibility:** Use proper heading hierarchy and alt text for images

## Common Patterns

**Meeting Minutes:**
```javascript
const doc = new Document({
  sections: [{
    children: [
      new Paragraph({ text: "Meeting Minutes", heading: HeadingLevel.HEADING_1 }),
      new Paragraph({ text: `Date: ${date}` }),
      new Paragraph({ text: `Attendees: ${attendees.join(', ')}` }),
      new Paragraph({ text: "Agenda", heading: HeadingLevel.HEADING_2 }),
      // ... agenda items
      new Paragraph({ text: "Action Items", heading: HeadingLevel.HEADING_2 }),
      // ... action items table
    ]
  }]
});
```

**Mail Merge:**
```javascript
// Template: Dear {firstName} {lastName}, ...
contacts.forEach(contact => {
  generateFromTemplate('letter-template.docx', contact, `letter-${contact.id}.docx`);
});
```

## Dependencies

Install required packages:
```bash
npm install docx docxtemplater pizzip
```

Optional for advanced features:
```bash
npm install docx-templates # Alternative templating
npm install officegen      # Legacy support
```

## Error Handling

- **Template Errors:** Validate template structure before processing
- **Missing Data:** Provide default values for optional template fields
- **Image Loading:** Check image file existence before embedding
- **File Permissions:** Handle write permission errors gracefully
- **Memory Issues:** For large documents, consider streaming if supported
- **Encoding:** Ensure proper UTF-8 encoding for international characters

## Performance Tips

- Reuse style definitions across multiple documents
- Pre-load templates for batch operations
- Use streaming for very large documents
- Compress images before embedding
- Batch file system operations
- Cache compiled templates when possible

## Advanced Features

**Table of Contents:**
```javascript
new TableOfContents("Table of Contents", {
  hyperlink: true,
  headingStyleRange: "1-3"
});
```

**Conditional Sections:**
```javascript
// In template: {#showSection}Content{/showSection}
doc.setData({ showSection: condition ? {...} : false });
```

**Custom Numbering:**
```javascript
new Paragraph({
  text: "Numbered item",
  numbering: {
    reference: "custom-numbering",
    level: 0
  }
});
```