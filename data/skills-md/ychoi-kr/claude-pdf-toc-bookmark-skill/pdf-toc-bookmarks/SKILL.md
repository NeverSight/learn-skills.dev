---
name: pdf-toc-bookmarks
description: Extract table of contents from PDF pages visually and create clickable bookmarks. Use when user wants to add bookmarks/navigation to PDFs based on printed table of contents pages, or needs to convert TOC pages to navigable PDF bookmarks.
---

# PDF TOC to Bookmarks

Extract table of contents from PDF pages and create clickable bookmarks using visual analysis and PyMuPDF.

## When to Use This Skill

Use this skill when:
- User wants to add bookmarks to a PDF that lacks them
- PDF has printed TOC pages but no clickable navigation
- User mentions "bookmarks," "navigation," "TOC," or "table of contents" for PDFs

## Workflow

### 1. Extract TOC Pages as Images

Extract TOC pages at high resolution for visual analysis:

```python
from scripts.extract_toc_images import extract_toc_images

extract_toc_images(
    pdf_path="/path/to/file.pdf",
    toc_start_page=10,  # First TOC page (1-based)
    toc_end_page=16,    # Last TOC page (1-based)
    output_dir="/mnt/user-data/outputs/toc_images"
)
```

### 2. Analyze Images Visually

Use Claude's vision capabilities to read TOC structure from images:

```python
from view import view

# View each TOC image
view("/mnt/user-data/outputs/toc_images/page_010.png")
view("/mnt/user-data/outputs/toc_images/page_011.png")
# ... view all TOC pages
```

Manually transcribe TOC structure into Python list format:
```python
toc = [
    [1, "Chapter 1: Introduction", 10],
    [2, "1.1 Overview", 11],
    [3, "1.1.1 Background", 12],
    [2, "1.2 Methods", 15],
    [1, "Chapter 2: Results", 20],
]
```

**Format**: `[level, title, printed_page_number]`
- `level`: Hierarchy depth (1=chapter, 2=section, 3=subsection)
- `title`: Exact text from TOC
- `printed_page_number`: Page number as printed in book (not PDF page index)

### 3. Determine Page Offset

Calculate offset between printed page numbers and PDF page indices:

```python
import fitz

doc = fitz.open("/path/to/file.pdf")

# Find a known page (e.g., where Chapter 1 starts)
# If book says "page 13" but it's PDF page 17, offset = 4
offset = actual_pdf_page - printed_page_number
```

Common offsets: 0-10 pages (cover, copyright, preface typically not numbered)

### 4. Add Bookmarks to PDF

```python
from scripts.add_bookmarks import add_bookmarks

add_bookmarks(
    pdf_path="/path/to/input.pdf",
    toc_list=toc,
    page_offset=4,  # Offset calculated above
    output_path="/mnt/user-data/outputs/file_with_bookmarks.pdf"
)
```

### 5. Verify and Deliver

Open output PDF in viewer to confirm bookmarks navigate correctly. Provide download link to user.

## Critical Insights

**Vision > Text Parsing**: OCR/regex for TOC extraction is unreliable due to formatting variations. Visual analysis by Claude is faster and more accurate.

**Page Offset**: Always verify offset. Test by clicking a bookmark and checking if it lands on correct page.

**Hierarchy Levels**: Maintain consistent level numbering (1=chapter, 2=section, 3=subsection) for proper nesting in PDF viewer.

## PyMuPDF Reference

```python
import fitz

# Open PDF
doc = fitz.open("file.pdf")

# Extract page as image
page = doc[page_index]  # 0-based
mat = fitz.Matrix(2.0, 2.0)  # 2x zoom
pix = page.get_pixmap(matrix=mat)
pix.save("output.png")

# Set TOC (bookmarks)
toc = [
    [1, "Chapter 1", 10],  # level, title, page (1-based)
    [2, "Section 1.1", 11],
]
doc.set_toc(toc)

# Save PDF
doc.save("output.pdf")
doc.close()
```

## Example Session

```
User: "Add bookmarks to this PDF based on the table of contents"

1. Extract TOC pages (10-16) as images
2. View images and transcribe TOC structure
3. Calculate page offset (e.g., 4 pages)
4. Create toc list with 182 entries
5. Add bookmarks using add_bookmarks script
6. Provide download link

Result: PDF with hierarchical bookmarks matching printed TOC
```

## Time Savings

- Traditional (regex/OCR): 30-60 min with errors
- Vision-based (this skill): 10-15 min with high accuracy
