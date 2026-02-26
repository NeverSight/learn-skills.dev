---
name: inputs
description: Prepare inputs for MTHDS methods. Use when user says "prepare inputs", "create inputs", "use my files", "generate test data", "template", "synthesize inputs", "mock inputs", "I have a PDF/image/document to use", "make sample data", or wants to create inputs.json for running a .mthds pipeline. Handles user-provided files, synthetic data generation, placeholder templates, and mixed approaches. Defaults to automatic mode.
---

# Prepare Inputs for MTHDS methods

Prepare input data for running MTHDS method bundles. This skill is the single entry point for all input preparation needs: extracting a placeholder template, generating synthetic test data, integrating user-provided files, or any combination.

## Mode Selection

See [Mode Selection](../shared/mode-selection.md) for general mode behavior.

**Default**: Automatic.

**Input strategy detection heuristics** (evaluated in order):

| Signal | Strategy |
|--------|----------|
| User provides file paths, folder paths, or mentions "my data" / "this file" / "use these images" / "here's my PDF" | **User Data** (or Mixed if some inputs remain unfilled) |
| User says "test data" / "generate inputs" / "synthesize" / "fake data" / "sample data" | **Synthetic** |
| User says "template" / "schema" / "placeholder" / "what inputs does it need?" | **Template** |
| No clear signal (e.g., called after `/build` with no further context) | **Template**, then offer to populate |

**Interactive additions**: Ask about:
- Which user files map to which inputs (when ambiguous)
- Domain/industry context for realistic synthetic data
- Whether to generate edge cases or happy-path data
- Specific values or constraints for certain fields

---

## Prerequisites

See [CLI Prerequisites](../shared/prerequisites.md)

---

## Process

### Step 1: Identify the Target Method

Determine the `.mthds` bundle and its output directory (`<output_dir>`). This is usually the directory containing `bundle.mthds` (e.g., `mthds-wip/pipeline_01/`).

The `inputs.json` file is saved directly in this directory (next to `bundle.mthds`):
- `<output_dir>/inputs.json`

If data files need to be generated or copied (images, PDFs, etc.), they go in a subdirectory:
- `<output_dir>/inputs/`

The `/inputs` subdirectory is only created when there are actual data files to store. Paths to these files are referenced from within `inputs.json`.

### Step 2: Get Input Schema

Extract the input template from the method:

```bash
mthds-agent pipelex inputs pipe <bundle.mthds> -L <bundle-dir>/ [--pipe specific_pipe]
```

**Output format:**
```json
{
  "success": true,
  "pipe_code": "process_document",
  "inputs": {
    "document": {
      "concept": "native.Document",
      "content": {"url": "url_value"}
    },
    "context": {
      "concept": "native.Text",
      "content": {"text": "text_value"}
    }
  }
}
```

For error handling, see [Error Handling Reference](../shared/error-handling.md).

### Step 3: Choose Input Strategy

Based on the heuristics above and what the user has provided, follow the appropriate strategy:

- [Template Strategy](#template-strategy) — placeholder JSON, no real data
- [Synthetic Strategy](#synthetic-strategy) — AI-generated realistic test data
- [User Data Strategy](#user-data-strategy) — integrate user-provided files
- [Mixed Strategy](#mixed-strategy) — user files + synthetic for the rest

---

## Template Strategy

The fastest path. Produces a placeholder `inputs.json` that the user can fill in manually.

1. Take the `inputs` object from Step 2's output
2. Save it to `<output_dir>/inputs.json` (next to `bundle.mthds`)
3. Report the saved file path and show the template content
4. Offer: "To populate this with realistic test data, re-run /inputs and ask for synthetic data. Or provide your own files."

---

## Synthetic Strategy

Generate realistic fake data tailored to the method's purpose.

### Identify Input Types

Parse the schema to identify what types of synthetic data are needed:

| Concept | Content Fields | Synthesis Method |
|---------|---------------|------------------|
| `native.Text` | `text` | Generate realistic text matching the method context |
| `native.Number` | `number` | Generate appropriate numeric values |
| `native.Image` | `url`, `caption?`, `mime_type?` | Use `synthesize_image` pipeline |
| `native.Document` | `url`, `mime_type?` | Use document generation skills or Python |
| `native.Page` | `text_and_images`, `page_view?` | Composite: text + optional images |
| `native.TextAndImages` | `text?`, `images?` | Composite: text + image list |
| `native.JSON` | `json_obj` | Generate structured JSON matching context |
| Custom structured | Per-field types | Recurse through structure fields |

**List types** (`Type[]` or `Type[N]`): Generate multiple items. Variable lists typically need 2-5 items; fixed lists need exactly N items.

### Generate Text Content

Create realistic text that matches the method's purpose:
- If the method processes invoices, generate invoice-like text
- If it analyzes reports, generate report-style content
- Match expected length (short prompts vs long documents)

### Generate Numeric Content

Generate sensible values within expected ranges based on the method context.

### Generate Structured Concepts

Fill each field according to its type and description.

### Generate File Inputs

When inputs require actual files (Image, Document), use the appropriate generation method. See [Image Generation](#image-generation) and [Document Generation](#document-generation) below.

### Assemble and Save

Create the complete `inputs.json` and save to `<output_dir>/inputs.json` (next to `bundle.mthds`). Any generated data files go in `<output_dir>/inputs/`.

---

## User Data Strategy

Integrate the user's own files into the method's input schema.

### Step A: Inventory User Files

Collect all files the user has provided (explicit paths, folders, or files mentioned earlier in conversation). For each file, determine its type:

| Extension(s) | Detected Type | Maps To |
|--------------|---------------|---------|
| `.pdf` | PDF document | `native.Document` (mime: `application/pdf`) |
| `.docx`, `.doc` | Word document | `native.Document` (mime: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`) |
| `.xlsx`, `.xls` | Spreadsheet | `native.Document` (mime: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`) |
| `.pptx`, `.ppt` | Presentation | `native.Document` (mime: `application/vnd.openxmlformats-officedocument.presentationml.presentation`) |
| `.jpg`, `.jpeg` | JPEG image | `native.Image` (mime: `image/jpeg`) |
| `.png` | PNG image | `native.Image` (mime: `image/png`) |
| `.webp` | WebP image | `native.Image` (mime: `image/webp`) |
| `.gif` | GIF image | `native.Image` (mime: `image/gif`) |
| `.svg` | SVG image | `native.Image` (mime: `image/svg+xml`) |
| `.tiff`, `.tif` | TIFF image | `native.Image` (mime: `image/tiff`) |
| `.bmp` | BMP image | `native.Image` (mime: `image/bmp`) |
| `.txt` | Plain text | `native.Text` (read file content) |
| `.md` | Markdown text | `native.Text` (read file content) |
| `.json` | JSON data | `native.JSON` or custom structured concept |
| `.csv` | CSV data | `native.Text` (read as text) or `native.JSON` (parse to objects) |
| `.html`, `.htm` | HTML | `native.Html` |

### Step B: Expand Folders

When the user provides a folder path:

1. List all files in the folder (non-recursive by default, recursive if user requests)
2. Filter to supported file types
3. Group files by detected type
4. Match to list-type inputs (`Image[]`, `Document[]`, etc.)

**Example**: User provides `./invoices/` containing 5 PDFs. The method expects `documents: Document[]`. Map all 5 PDFs to that list input.

### Step C: Match Files to Inputs

For each input variable in the schema, attempt to match user-provided files:

**Matching rules** (applied in order):

1. **Exact name match**: Input variable `invoice` matches a file named `invoice.pdf`
2. **Type match (single candidate)**: If only one input expects `native.Image` and the user provided exactly one image file, match them
3. **Type match (multiple candidates)**: If multiple inputs of the same type exist:
   - In **automatic mode**: match by name similarity (variable name vs filename)
   - In **interactive mode**: ask the user which file goes where
4. **Folder to list**: If a folder contains files of a single type and an input expects a list of that type, map the folder contents to that input
5. **Unmatched files**: Report them and ask if they should be ignored or mapped to a specific input
6. **Unfilled inputs**: After matching, any inputs still without data can be left as placeholders or filled with synthetic data (see [Mixed Strategy](#mixed-strategy))

### Step D: Copy Files to Output Directory

Copy (or symlink) user files into `<output_dir>/inputs/` so `inputs.json` uses paths relative to the output directory. This keeps the pipeline directory self-contained. Only create the `inputs/` subdirectory if there are actual files to copy.

Use descriptive filenames: if the input variable is `invoice`, copy to `<output_dir>/inputs/invoice.pdf` (preserving original extension).

### Step E: Build Content Objects

For each matched file, construct the proper content object:

**Document input:**
```json
{
  "concept": "native.Document",
  "content": {
    "url": "<output_dir>/inputs/invoice.pdf",
    "mime_type": "application/pdf"
  }
}
```

**Image input:**
```json
{
  "concept": "native.Image",
  "content": {
    "url": "<output_dir>/inputs/photo.jpg",
    "mime_type": "image/jpeg"
  }
}
```

**Text input** (from `.txt` or `.md` file — read the file content):
```json
{
  "concept": "native.Text",
  "content": {
    "text": "<actual file content read from the .txt/.md file>"
  }
}
```

**Image list input** (from folder):
```json
{
  "concept": "native.Image",
  "content": [
    {"url": "<output_dir>/inputs/img_001.jpg", "mime_type": "image/jpeg"},
    {"url": "<output_dir>/inputs/img_002.jpg", "mime_type": "image/jpeg"},
    {"url": "<output_dir>/inputs/img_003.png", "mime_type": "image/png"}
  ]
}
```

### Step F: Assemble and Save

Combine all content objects into a single `inputs.json` and save to `<output_dir>/inputs.json` (next to `bundle.mthds`).

### Step G: Report

Show the user:
- Which files were matched to which inputs
- Any unfilled inputs (offer synthetic or placeholder)
- The final `inputs.json` content
- Path to the saved file

---

## Mixed Strategy

Combines user data with synthetic generation for any remaining gaps.

1. Follow [User Data Strategy](#user-data-strategy) Steps A-E to match user files
2. For each unfilled input, apply [Synthetic Strategy](#synthetic-strategy)
3. Assemble the complete `inputs.json` combining both sources
4. Report which inputs came from user data and which were synthesized

---

## Image Generation

Use the `synthesize_image` Pipelex pipeline to generate test images.

**Command:**

First, create an input file (e.g., `<output_dir>/image_request.json`):
```json
{
  "request": {
    "concept": "synthetic_data.ImageRequest",
    "content": {
      "category": "<category>",
      "description": "<optional description>"
    }
  }
}
```

Then run:
```bash
mthds-agent pipelex run pipe pipelex/builder/synthetic_inputs/synthesize_image.mthds --inputs <output_dir>/image_request.json
```

**Image Categories:**

| Category | Use For | Example Description |
|----------|---------|---------------------|
| `photograph` | Real-world photos, product images, portraits | "A professional headshot of a business person" |
| `screenshot` | UI mockups, app screens, web pages | "A mobile banking app dashboard showing account balance" |
| `chart` | Data visualizations, graphs, plots | "A bar chart showing quarterly sales by region" |
| `diagram` | Technical diagrams, flowcharts, architecture | "A system architecture diagram with microservices" |
| `document_scan` | Scanned papers, receipts, forms | "A scanned invoice from a hardware store" |
| `handwritten` | Handwritten notes, signatures | "Handwritten meeting notes on lined paper" |

**Output**: The pipeline saves the generated image to `<output_dir>/inputs/` and returns the file path.

For image synthesis error handling, see [Error Handling Reference](../shared/error-handling.md).

---

## Document Generation

Generate test documents based on the document type needed.

### PDF Documents

> `reportlab` is a dependency of `pipelex` — always available, no additional installation needed.

#### Basic PDF (Canvas API)
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("<output_dir>/inputs/test_document.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Multi-Page PDF (Platypus)
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("<output_dir>/inputs/test_report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Professional Reports with Tables
```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Sample data
data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4'],
    ['Widgets', '120', '135', '142', '158'],
    ['Gadgets', '85', '92', '98', '105']
]

# Create PDF with table
doc = SimpleDocTemplate("<output_dir>/inputs/test_report.pdf")
elements = []

# Add title
styles = getSampleStyleSheet()
title = Paragraph("Quarterly Sales Report", styles['Title'])
elements.append(title)

# Add table with advanced styling
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(table)

doc.build(elements)
```

**Last resort** — use a public test PDF URL:
```json
{
  "url": "https://www.w3.org/WAI/WCAG21/Techniques/pdf/img/table-word.pdf",
  "mime_type": "application/pdf"
}
```

### Word Documents (DOCX)

**If `example-skills:docx` skill is available:**
```
Use the /docx skill to create a Word document with the following content:
[Describe the document content, structure, and formatting]
Save to: <output_dir>/inputs/<filename>.docx
```

**If skill is NOT available**, create using Python:
```python
# Requires: pip install python-docx
from docx import Document

doc = Document()
doc.add_heading('Test Document', 0)
doc.add_paragraph('This is synthetic test content for method testing.')
# Add more content as needed
doc.save('<output_dir>/inputs/test_document.docx')
```

### Spreadsheets (XLSX)

**If `example-skills:xlsx` skill is available:**
```
Use the /xlsx skill to create a spreadsheet with the following data:
[Describe columns, rows, and sample data]
Save to: <output_dir>/inputs/<filename>.xlsx
```

**If skill is NOT available**, create using Python:
```python
# Requires: pip install openpyxl
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = 'Column1'
ws['B1'] = 'Column2'
ws['A2'] = 'Value1'
ws['B2'] = 'Value2'
wb.save('<output_dir>/inputs/test_spreadsheet.xlsx')
```

---

**Fallback Strategy:**
1. For PDFs: use `reportlab` (always available via pipelex) with the patterns above
2. For DOCX/XLSX: use the `/docx` or `/xlsx` skill (install from the Anthropic example-skills marketplace if not available)
3. For any format: use public test file URLs as fallback
4. As last resort, ask user to provide test files

---

## Validate & Run

After assembling the inputs, confirm readiness:

> Inputs are ready. `inputs.json` has been saved with real values — no placeholders remain.

Then offer to run:

```bash
# Dry run with the prepared inputs (directory mode auto-detects bundle, inputs, library dir)
mthds-agent pipelex run pipe <bundle-dir>/ --dry-run

# Full run (uses actual AI/extraction models)
mthds-agent pipelex run pipe <bundle-dir>/
```

---

## Native Concept Content Structures

### Text
```json
{"text": "The actual text content"}
```

### Number
```json
{"number": 42}
```

### Image
```json
{
  "url": "/path/to/image.jpg",
  "caption": "Optional description",
  "mime_type": "image/jpeg"
}
```

### Document
```json
{
  "url": "/path/to/document.pdf",
  "mime_type": "application/pdf"
}
```

### TextAndImages
```json
{
  "text": {"text": "Main text content"},
  "images": [
    {"url": "/path/to/img1.png", "caption": "Figure 1"}
  ]
}
```

### Page
```json
{
  "text_and_images": {
    "text": {"text": "Page content..."},
    "images": []
  },
  "page_view": null
}
```

### JSON
```json
{"json_obj": {"key": "value", "nested": {"data": 123}}}
```

---

## Complete Examples

### Example 1: Template for a Haiku writer

**Method**: Haiku pipeline expecting `theme: Text`

```bash
mthds-agent pipelex inputs pipe mthds-wip/pipeline_01/bundle.mthds -L mthds-wip/pipeline_01/
```

Save the `inputs` from the output directly to `mthds-wip/pipeline_01/inputs.json`.

### Example 2: Synthetic data for an image analysis pipeline

**Method**: Image analyzer expecting `image: Image` and `analysis_prompt: Text`

1. Get schema, identify needs: test photograph + instruction text
2. Generate image via `synthesize_image.mthds` with category `photograph`
3. Write analysis prompt text matching the method context
4. Assemble:
```json
{
  "image": {
    "concept": "native.Image",
    "content": {
      "url": "mthds-wip/pipeline_01/inputs/city_street.jpg",
      "mime_type": "image/jpeg"
    }
  },
  "analysis_prompt": {
    "concept": "native.Text",
    "content": {
      "text": "Analyze this street scene. Count visible people and describe the atmosphere."
    }
  }
}
```

### Example 3: User-provided invoice PDF

**Method**: Invoice processor expecting `invoice: Document` and `instructions: Text`

User says: "Use my file `~/documents/invoice_march.pdf`"

1. Get schema: needs `invoice` (Document) + `instructions` (Text)
2. Inventory: user provided `invoice_march.pdf` (PDF = Document type)
3. Match: `invoice_march.pdf` maps to `invoice` input (name similarity + type match)
4. Copy: `cp ~/documents/invoice_march.pdf mthds-wip/pipeline_01/inputs/invoice.pdf`
5. Unfilled: `instructions` has no user file. Generate synthetic text: "Extract all line items, totals, and vendor information from this invoice."
6. Assemble:
```json
{
  "invoice": {
    "concept": "native.Document",
    "content": {
      "url": "mthds-wip/pipeline_01/inputs/invoice.pdf",
      "mime_type": "application/pdf"
    }
  },
  "instructions": {
    "concept": "native.Text",
    "content": {
      "text": "Extract all line items, totals, and vendor information from this invoice."
    }
  }
}
```

### Example 4: Folder of images for batch processing

**Method**: Batch image captioner expecting `images: Image[]`

User says: "Use the photos in `./product-photos/`"

1. Get schema: needs `images` (Image[])
2. Expand folder: `./product-photos/` contains `shoe.jpg`, `hat.png`, `bag.jpg`
3. Copy all to `<output_dir>/inputs/`
4. Assemble:
```json
{
  "images": {
    "concept": "native.Image",
    "content": [
      {"url": "mthds-wip/pipeline_01/inputs/shoe.jpg", "mime_type": "image/jpeg"},
      {"url": "mthds-wip/pipeline_01/inputs/hat.png", "mime_type": "image/png"},
      {"url": "mthds-wip/pipeline_01/inputs/bag.jpg", "mime_type": "image/jpeg"}
    ]
  }
}
```

---

## Reference

- [CLI Prerequisites](../shared/prerequisites.md) — read at skill start to check CLI availability
- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
- [MTHDS Language Reference](../shared/mthds-reference.md) — read for concept definitions and syntax
- [Native Content Types](../shared/native-content-types.md) — read for the full attribute reference of each native content type when assembling input JSON
