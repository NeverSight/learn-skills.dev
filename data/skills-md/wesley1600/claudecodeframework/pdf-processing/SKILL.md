---
name: pdf-processing
description: Process and analyze PDF documents including text extraction, table extraction, chart analysis, and visual content understanding. Use when working with PDFs, extracting structured data, generating summaries, or converting PDFs to other formats (markdown, JSON, CSV).
allowed-tools: "Read, Write, Bash, Glob, Grep"
version: 1.0.0
---

# PDF Processing Skill

## Overview

This skill provides comprehensive PDF processing capabilities leveraging Claude's native PDF support, which can:
- Extract and parse text content
- Identify and extract tables with structure preservation
- Analyze charts, graphs, and visual elements
- Understand document layout and formatting
- Generate summaries and insights
- Convert PDFs to various formats (Markdown, JSON, CSV, plain text)

## When to Use

Claude should automatically activate this skill when:
- User provides a PDF file path or wants to process a PDF
- User asks to extract text, tables, or data from PDFs
- User requests PDF analysis, summarization, or conversion
- User needs to understand charts, diagrams, or visual content in PDFs
- User wants to transform PDF content to another format

## Key Capabilities

### 1. Text Extraction
- Full document text extraction with formatting preservation
- Page-by-page text extraction
- Section and paragraph identification
- Header and footer detection

### 2. Table Extraction
- Automatic table detection and extraction
- Structure-preserving conversion to CSV, JSON, or Markdown
- Multi-page table handling
- Cell merging and complex table support

### 3. Visual Content Analysis
- Chart and graph interpretation
- Diagram and flowchart understanding
- Image and figure description
- Infographic analysis

### 4. Document Understanding
- Layout analysis and structure detection
- Multi-column text handling
- Form field identification
- Metadata extraction (title, author, creation date, page count)

### 5. Format Conversion
- PDF to Markdown (preserving headings, lists, tables)
- PDF to JSON (structured data extraction)
- PDF to CSV (table extraction)
- PDF to plain text

## Instructions

### Step 1: Validate PDF Input

First, determine how the PDF is provided:

**Option A: File Path**
```bash
# Verify the file exists and is a PDF
ls -lh /path/to/document.pdf
file /path/to/document.pdf
```

**Option B: Base64-Encoded PDF**
If the user provides base64-encoded content, save it first:
```bash
# Decode and save base64 PDF
python .claude/skills/pdf-processing/scripts/decode_pdf.py --input base64_string.txt --output document.pdf
```

**Option C: URL**
If the user provides a URL, download it:
```bash
# Download PDF from URL
python .claude/skills/pdf-processing/scripts/download_pdf.py --url "https://example.com/doc.pdf" --output document.pdf
```

### Step 2: Read and Analyze PDF

Use the **Read tool** to access PDF files. Claude's native PDF support will:
- Display the PDF content visually
- Extract text and structure automatically
- Identify tables, charts, and images

```python
# Example: Read PDF using the Read tool
# The Read tool handles PDFs natively and extracts text + visual content
Read(file_path="/absolute/path/to/document.pdf")
```

### Step 3: Process Based on User Request

#### A. Text Extraction

For simple text extraction:
```bash
python .claude/skills/pdf-processing/scripts/extract_text.py \
  --input document.pdf \
  --output document.txt \
  --preserve-formatting true
```

For page-specific extraction:
```bash
python .claude/skills/pdf-processing/scripts/extract_text.py \
  --input document.pdf \
  --pages 1,3,5-10 \
  --output selected_pages.txt
```

#### B. Table Extraction

Extract all tables to CSV:
```bash
python .claude/skills/pdf-processing/scripts/extract_tables.py \
  --input document.pdf \
  --format csv \
  --output-dir ./extracted_tables/
```

Extract tables to JSON with structure:
```bash
python .claude/skills/pdf-processing/scripts/extract_tables.py \
  --input document.pdf \
  --format json \
  --output tables.json
```

#### C. Document Summarization

Generate a summary of the PDF:
```bash
python .claude/skills/pdf-processing/scripts/summarize_pdf.py \
  --input document.pdf \
  --output summary.md \
  --style concise  # Options: concise, detailed, executive
```

#### D. Format Conversion

Convert PDF to Markdown:
```bash
python .claude/skills/pdf-processing/scripts/convert_pdf.py \
  --input document.pdf \
  --output document.md \
  --format markdown \
  --preserve-images true
```

Convert PDF to structured JSON:
```bash
python .claude/skills/pdf-processing/scripts/convert_pdf.py \
  --input document.pdf \
  --output document.json \
  --format json \
  --extract-metadata true
```

#### E. Visual Content Analysis

Analyze charts and graphs:
```bash
python .claude/skills/pdf-processing/scripts/analyze_visuals.py \
  --input document.pdf \
  --output analysis.json \
  --elements charts,graphs,diagrams
```

### Step 4: Post-Processing and Output

After extraction/conversion:

1. **Validate Output**: Check that the output file was created successfully
```bash
ls -lh output_file.{txt,md,json,csv}
```

2. **Preview Results**: Show the user a preview of the extracted content
```bash
head -n 20 output_file.txt  # For text files
cat output_file.json | python -m json.tool | head -n 50  # For JSON
```

3. **Provide Summary**: Summarize what was extracted and offer next steps

### Step 5: Handle Edge Cases

#### Password-Protected PDFs
```bash
python .claude/skills/pdf-processing/scripts/extract_text.py \
  --input document.pdf \
  --password "user_provided_password" \
  --output document.txt
```

#### Scanned PDFs (OCR Required)
```bash
# Use OCR for scanned PDFs
python .claude/skills/pdf-processing/scripts/ocr_pdf.py \
  --input scanned_document.pdf \
  --output document.txt \
  --language eng  # Language code: eng, fra, deu, etc.
```

#### Large PDFs (Memory Optimization)
```bash
# Process large PDFs in chunks
python .claude/skills/pdf-processing/scripts/extract_text.py \
  --input large_document.pdf \
  --output document.txt \
  --chunk-size 10  # Process 10 pages at a time
```

## Error Handling

### Common Issues

1. **File Not Found**
   - Verify the path with `ls` or `Glob`
   - Check for typos in the filename
   - Ensure absolute paths are used

2. **Corrupted PDF**
   - Try reading with the Read tool first
   - Use repair mode: `python scripts/repair_pdf.py --input corrupted.pdf --output repaired.pdf`

3. **Unsupported PDF Features**
   - Some PDFs with complex DRM or encryption may fail
   - Inform the user and suggest alternatives

4. **OCR Failures**
   - Check if tesseract is installed: `which tesseract`
   - Verify image quality is sufficient
   - Try different language settings

## Best Practices

1. **Always use the Read tool first** - This leverages Claude's native PDF support for best results
2. **Preserve structure** - When extracting tables or converting formats, maintain the original structure
3. **Validate outputs** - Always check that output files were created successfully
4. **Provide context** - Tell the user what was extracted and what they can do next
5. **Handle errors gracefully** - If processing fails, explain why and suggest alternatives
6. **Respect privacy** - Remind users not to upload sensitive documents without proper authorization

## Output Formats

### Text Output
```
Plain text with optional formatting preservation
Line breaks and paragraphs maintained
Special characters preserved
```

### Markdown Output
```markdown
# Document Title

## Section Heading

Paragraph text with **bold** and *italic* formatting.

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

![Chart Description](chart_extracted.png)
```

### JSON Output
```json
{
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "pages": 42,
    "creation_date": "2024-01-15"
  },
  "content": [
    {
      "page": 1,
      "type": "text",
      "content": "Page 1 text content..."
    },
    {
      "page": 2,
      "type": "table",
      "headers": ["Col1", "Col2", "Col3"],
      "rows": [["A", "B", "C"], ["D", "E", "F"]]
    }
  ]
}
```

### CSV Output (for tables)
```csv
Column1,Column2,Column3
Value1,Value2,Value3
Value4,Value5,Value6
```

## Advanced Features

### Batch Processing
```bash
# Process multiple PDFs
python .claude/skills/pdf-processing/scripts/batch_process.py \
  --input-dir ./pdfs/ \
  --output-dir ./extracted/ \
  --format markdown
```

### Custom Templates
```bash
# Use custom conversion templates
python .claude/skills/pdf-processing/scripts/convert_pdf.py \
  --input document.pdf \
  --output document.md \
  --template .claude/skills/pdf-processing/assets/custom_template.md
```

### Selective Extraction
```bash
# Extract only specific sections
python .claude/skills/pdf-processing/scripts/extract_sections.py \
  --input document.pdf \
  --sections "Introduction,Methods,Results" \
  --output extracted_sections.md
```

## Integration with Other Tools

This skill works well with:
- **Data analysis tools** - Extract tables and feed to pandas/numpy
- **Documentation generators** - Convert PDFs to Markdown for wikis
- **Search systems** - Extract text for indexing
- **Automation workflows** - Batch process invoices, reports, forms

## Examples

### Example 1: Extract and Summarize
```bash
# User: "Please extract the key points from this research paper"
1. Read(file_path="/path/to/paper.pdf")
2. python scripts/summarize_pdf.py --input paper.pdf --output summary.md --style executive
3. Show the user the summary with key findings highlighted
```

### Example 2: Extract Tables to CSV
```bash
# User: "Get all tables from this financial report"
1. Read(file_path="/path/to/report.pdf")
2. python scripts/extract_tables.py --input report.pdf --format csv --output-dir ./tables/
3. List the extracted CSV files and preview the first table
```

### Example 3: Convert to Markdown
```bash
# User: "Convert this PDF to markdown"
1. Read(file_path="/path/to/document.pdf")
2. python scripts/convert_pdf.py --input document.pdf --output document.md --format markdown
3. Show preview of the markdown and confirm successful conversion
```

## Dependencies

The scripts in this skill require:
- Python 3.8+
- PyPDF2 or pypdf (PDF parsing)
- pdfplumber (table extraction)
- pdf2image (image extraction)
- pytesseract (OCR for scanned PDFs)
- Pillow (image processing)
- requests (URL downloads)

These are installed via the requirements file in `assets/requirements.txt`.

## References

See the `references/` directory for:
- `pdf_capabilities.md` - Detailed breakdown of Claude's PDF support
- `api_reference.md` - Complete API documentation for all scripts
- `examples.md` - More usage examples and use cases
- `troubleshooting.md` - Common issues and solutions

## Notes for Claude

- **Always read PDFs with the Read tool first** - This is the most reliable method
- **After reading, analyze what the user needs** - Text, tables, summary, conversion?
- **Use the appropriate script** - Don't try to do everything manually
- **Validate outputs** - Always check that files were created successfully
- **Provide helpful context** - Explain what was extracted and suggest next steps
- **Handle errors gracefully** - If something fails, explain why and offer alternatives
- **Be efficient** - Use batch processing for multiple PDFs
- **Preserve structure** - Maintain document formatting when converting

## Version History

- **1.0.0** (2025-11-18) - Initial release with core PDF processing capabilities
