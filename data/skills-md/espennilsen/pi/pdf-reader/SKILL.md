---
name: pdf-reader
description: >
  Read and extract content from PDF files — text, tables, metadata, and images.
  Use when asked to read a PDF, extract text from a PDF, summarize a PDF,
  analyze a PDF document, get tables from a PDF, or check PDF metadata.
  Also triggers on "open this PDF", "what does this PDF say", "parse PDF",
  "PDF to text", or when a .pdf file path or URL is provided.
---

# PDF Reader

Extract content from PDF files using `pdftotext` (Poppler) for text and
`pdfplumber` (Python) for tables and structured extraction.

## Quick Reference

| Task | Tool | Command |
|------|------|---------|
| Full text | pdftotext | `pdftotext file.pdf -` |
| Text with layout | pdftotext | `pdftotext -layout file.pdf -` |
| Specific pages | pdftotext | `pdftotext -f 3 -l 5 file.pdf -` |
| Tables | pdfplumber | `python3 scripts/extract.py tables file.pdf` |
| Metadata | pdfinfo | `pdfinfo file.pdf` |
| Page count | pdfinfo | `pdfinfo file.pdf \| grep Pages` |
| Images | pdfimages | `pdfimages -list file.pdf` |
| Fonts | pdffonts | `pdffonts file.pdf` |
| OCR (scanned PDF) | tesseract | `python3 scripts/extract.py ocr file.pdf` |
| Smart text + OCR | extract.py | `python3 scripts/extract.py text file.pdf` |
| Quick survey | extract.py | `python3 scripts/extract.py scan file.pdf` |

## Workflow

### Step 1: Get the PDF

If the user provides a URL, download it first:

```bash
curl -sL "URL" -o /tmp/document.pdf
```

Verify it's a valid PDF:

```bash
file /tmp/document.pdf  # should say "PDF document"
pdfinfo /tmp/document.pdf  # metadata + page count
```

### Step 2: Choose Extraction Method

**Plain text (most cases):**

```bash
pdftotext file.pdf -
```

This pipes output to stdout. For large PDFs, use page ranges:

```bash
pdftotext -f 1 -l 10 file.pdf -    # pages 1-10
```

**Layout-preserving text (columns, formatted docs):**

```bash
pdftotext -layout file.pdf -
```

Use `-layout` when the PDF has multi-column layouts, tables rendered as text,
or precise spacing that matters.

**Tables (structured data):**

```bash
python3 scripts/extract.py tables file.pdf
```

Or inline with pdfplumber:

```python
import pdfplumber

pdf = pdfplumber.open("file.pdf")
for i, page in enumerate(pdf.pages):
    tables = page.extract_tables()
    for table in tables:
        print(f"\n--- Table on page {i+1} ---")
        for row in table:
            print(" | ".join(str(cell or "") for cell in row))
pdf.close()
```

**Metadata only:**

```bash
pdfinfo file.pdf
```

Returns: title, author, creator, producer, page count, page size, dates.

### Step 3: Handle Large PDFs

For PDFs over ~50 pages, don't dump everything at once:

1. Get page count: `pdfinfo file.pdf | grep Pages`
2. Extract in chunks: `pdftotext -f 1 -l 20 file.pdf -`
3. Process chunk, then continue: `pdftotext -f 21 -l 40 file.pdf -`

For targeted extraction (searching for specific content):

```bash
# Extract all text, grep for relevant sections
pdftotext file.pdf - | grep -n -i "keyword"

# Then extract the specific page range
pdftotext -f PAGE -l PAGE file.pdf -
```

### Step 4: Handle Scanned PDFs (OCR)

If `pdftotext` returns empty or garbled output, the PDF is likely scanned.

**Detection:**
```bash
python3 scripts/extract.py scan file.pdf   # reports scanned pages
pdffonts file.pdf                           # empty = image-based
```

**Smart extraction (auto-fallback):**

`text` mode automatically detects scanned pages and OCRs them:

```bash
python3 scripts/extract.py text file.pdf
```

Pages with selectable text extract normally. Pages without selectable text
fall back to OCR via Tesseract. No manual detection needed.

**Force OCR on all pages:**

```bash
python3 scripts/extract.py ocr file.pdf
python3 scripts/extract.py ocr file.pdf --pages 1-5
python3 scripts/extract.py ocr file.pdf --dpi 400        # higher quality
python3 scripts/extract.py ocr file.pdf --lang eng+nor   # multi-language
```

**OCR options:**
- `--dpi 300` — resolution for page-to-image conversion (default: 300, higher = slower but better)
- `--lang eng` — Tesseract language pack (default: eng). Use `+` for multiple: `eng+nor+deu`
- `--pages 1-5` — limit to specific pages (recommended for large PDFs)

**Available language packs:**
```bash
tesseract --list-langs
```

Install additional languages via Homebrew:
```bash
brew install tesseract-lang    # all languages
```

### Step 5: Handle Other Edge Cases

**Mixed PDFs (some pages scanned, some not):**

Just use `text` mode — it handles mixed PDFs automatically:

```bash
python3 scripts/extract.py text file.pdf
```

Selectable pages extract instantly, scanned pages get OCR'd. The output
is tagged so you know which pages used OCR.

**Password-protected PDFs:**

```bash
pdftotext -upw "password" file.pdf -   # user password
pdftotext -opw "password" file.pdf -   # owner password
```

**Encoding issues (garbled output):**

```bash
pdftotext -enc UTF-8 file.pdf -
```

**Extract images:**

```bash
pdfimages -png file.pdf /tmp/images/img   # extracts as PNG
pdfimages -list file.pdf                  # list images without extracting
```

## Decision Tree

```
Is it a URL? → curl -sL "URL" -o /tmp/doc.pdf
            ↓
Run: python3 scripts/extract.py scan file.pdf
            ↓
All pages have selectable text?
  YES → pdftotext file.pdf -           (fast, simple)
  NO  → python3 scripts/extract.py text file.pdf  (auto OCR fallback)
            ↓
Need tables?
  YES → python3 scripts/extract.py tables file.pdf
```

## Tips

- **Start with `scan`** on unknown PDFs — it reports pages, tables, scanned detection, and a preview
- `pdftotext` is fastest for normal PDFs — try it first
- Use `-layout` for multi-column documents (academic papers, reports)
- `pdfplumber` is better for tables — it understands cell boundaries
- `text` mode auto-detects scanned pages and OCRs only those — preferred over raw `pdftotext` for unknown PDFs
- `ocr` mode is for forcing OCR on everything (useful when text extraction gives garbled output despite appearing selectable)
- Higher `--dpi` gives better OCR accuracy but is slower (300 is a good default, 400+ for small text)
- For PDFs from URLs, always download to `/tmp/` first — don't pipe curl to tools
- Large PDF text output may exceed context limits — use `--pages` to extract in ranges
