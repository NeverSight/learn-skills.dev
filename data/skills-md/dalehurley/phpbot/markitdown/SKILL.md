---
name: markitdown
description: "Convert any document or file to Markdown using Microsoft's MarkItDown library. Use this skill when the user asks to convert a file to markdown, extract text from a document, turn a PDF/Word/Excel/PowerPoint/HTML/image/audio file into markdown, or parse document content. Supports PDF, DOCX, PPTX, XLSX, HTML, images (with OCR), audio, CSV, JSON, XML, ZIP, EPub, and more."
tags:
  [
    document-conversion,
    markdown,
    pdf,
    docx,
    pptx,
    xlsx,
    html,
    images,
    ocr,
    markitdown,
  ]
version: 0.1.0
---

# Skill: markitdown

## When to Use

Use this skill when the user asks to:

- Convert a document or file to Markdown
- Extract text/content from a PDF, Word, Excel, PowerPoint, or other document
- Parse a file into readable text
- Turn a file into Markdown format
- Read/extract content from images (OCR)
- Transcribe audio files to text
- Convert HTML pages to Markdown
- Process CSV, JSON, or XML files as Markdown
- Extract content from ZIP archives or EPub files

## Supported Formats

| Format     | Extensions                                       | Notes                                       |
| ---------- | ------------------------------------------------ | ------------------------------------------- |
| PDF        | `.pdf`                                           | Text extraction with structure preservation |
| Word       | `.docx`                                          | Headings, lists, tables preserved           |
| PowerPoint | `.pptx`                                          | Slide content and notes                     |
| Excel      | `.xlsx`                                          | Tables converted to Markdown tables         |
| Images     | `.jpg`, `.png`, `.gif`, `.webp`, `.bmp`, `.tiff` | EXIF metadata; OCR if available             |
| Audio      | `.mp3`, `.wav`                                   | EXIF metadata; transcription if available   |
| HTML       | `.html`, `.htm`                                  | Full HTML-to-Markdown conversion            |
| CSV        | `.csv`                                           | Converted to Markdown tables                |
| JSON       | `.json`                                          | Structured as Markdown                      |
| XML        | `.xml`                                           | Structured as Markdown                      |
| ZIP        | `.zip`                                           | Iterates over archive contents              |
| EPub       | `.epub`                                          | Book content extraction                     |

## Input Parameters

| Parameter     | Required | Description                                                     | Example                          |
| ------------- | -------- | --------------------------------------------------------------- | -------------------------------- |
| `file_path`   | Yes      | Path to the file to convert                                     | `/Users/me/Documents/report.pdf` |
| `output_path` | No       | Path to save the Markdown output. If omitted, outputs to stdout | `./output.md`                    |

## Procedure

1. Determine the file path from the user's request. If not provided, ask via `ask_user`.
2. Verify the file exists using `bash` or `read_file`.
3. Run the conversion script:
   ```bash
   python3 skills/markitdown/scripts/convert.py "{{file_path}}"
   ```
   Or save to a file:
   ```bash
   python3 skills/markitdown/scripts/convert.py "{{file_path}}" -o "{{output_path}}"
   ```
4. The script will auto-install `markitdown[all]` if not already available.
5. Present the Markdown output to the user, or confirm the output file was written.

## Bundled Scripts

| Script               | Type   | Description                                             |
| -------------------- | ------ | ------------------------------------------------------- |
| `scripts/convert.py` | Python | Convert any supported file to Markdown using markitdown |

### Script Usage

```bash
# Convert and print to stdout
python3 skills/markitdown/scripts/convert.py "/path/to/document.pdf"

# Convert and save to file
python3 skills/markitdown/scripts/convert.py "/path/to/document.pdf" -o output.md

# Convert with verbose output (shows metadata)
python3 skills/markitdown/scripts/convert.py "/path/to/document.pdf" -v
```

## Example

Example requests that trigger this skill:

```
convert this PDF to markdown
extract the text from report.docx
turn this spreadsheet into markdown
parse the content of presentation.pptx
convert ~/Downloads/invoice.pdf to markdown
```
