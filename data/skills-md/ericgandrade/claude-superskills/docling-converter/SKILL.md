---
name: docling-converter
description: This skill should be used when the user needs to convert documents (PDF, DOCX, PPTX, XLSX, HTML, images) into structured Markdown or JSON using Docling. Also use when the user wants to convert a PowerPoint presentation (.pptx) to Markdown.
license: MIT
---

# 📄 Docling Document Converter

**Version:** 1.0.1
**Status:** ✨ Production Ready | 🌍 Universal

Convert documents (PDF, DOCX, PPTX, Images, HTML) into structured Markdown and JSON using Docling's intelligent parsing engine.

---

## 📋 Overview

**Docling Converter** is a powerful document processing skill that transforms unstructured files into clean, structured Markdown and JSON. Unlike basic text extractors, it preserves document layout, tables, and hierarchy, making it ideal for RAG (Retrieval-Augmented Generation) pipelines and knowledge base ingestion.

### ✨ Key Features

- **📄 Multi-Format Support:** PDF, DOCX, PPTX, XLSX, HTML, Images, AsciiDoc.
- **🧠 Intelligent Parsing:** Preserves tables, headers, and document structure.
- **👁️ OCR Integration:** Handles scanned PDFs and images (requires `docling[ocr]`).
- **📝 Clean Markdown:** Generates LLM-ready Markdown output.
- **⚡ Batch Processing:** Handles single files or entire directories.

---

## 🚀 Quick Start

### Invoke the Skill

Use any of these trigger phrases:

```bash
copilot> convert this pdf to markdown: report.pdf
copilot> extract tables from: data.xlsx
copilot> docling convert: presentation.pptx
copilot> process document: scanned-contract.pdf --ocr
copilot> convert this pptx to markdown: deck.pptx
copilot> pptx to markdown: strategy-2026.pptx
claude> convert this presentation to markdown: roadmap.pptx
claude> pptx to markdown: proposal.pptx
```

---

## 🛠️ Workflow

### Step 0: Discovery & Setup

**Objective:** Verify Docling installation and dependencies.

**Actions:**

```bash
# Check if docling is installed
if python3 -c "import docling" 2>/dev/null; then
    echo "✅ Docling detected"
else
    echo "⚠️  Docling not found"
    echo "🔧 Installing docling..."
    pip install docling --break-system-packages
fi

# Check for OCR support if requested
if [[ "$OCR_REQUESTED" == "true" ]]; then
    if python3 -c "import easyocr" 2>/dev/null; then
        echo "✅ OCR dependencies detected"
    else
        echo "⚠️  OCR dependencies missing"
        echo "🔧 Installing docling[ocr]..."
        pip install "docling[ocr]" --break-system-packages
    fi
fi
```

### Step 1: Create Conversion Script

**Objective:** Generate a robust Python script to handle the conversion.

**Actions:**

Create a temporary script `.gemini/tmp/docling_convert.py`:

```python
import sys
import json
import os
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption, WordFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode

def convert_document(input_path, output_dir, use_ocr=False):
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Configure Pipeline
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = use_ocr
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

    converter = DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(pipeline_options=pipeline_options),
            "docx": WordFormatOption(),
            "pptx": WordFormatOption()
        }
    )

    print(f"🔄 Converting: {input_path.name}...")
    
    try:
        result = converter.convert(input_path)
        
        # Export Markdown
        md_output = result.document.export_to_markdown()
        md_path = output_dir / f"{input_path.stem}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_output)
            
        # Export JSON (structure)
        json_output = result.document.export_to_dict()
        json_path = output_dir / f"{input_path.stem}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_output, f, ensure_ascii=False, indent=2)

        print(f"✅ Success! Saved to: {md_path}")
        return True

    except Exception as e:
        print(f"❌ Error converting {input_path.name}: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python docling_convert.py <input_file> <output_dir> [ocr]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_directory = sys.argv[2]
    ocr_enabled = len(sys.argv) > 3 and sys.argv[3] == "--ocr"

    success = convert_document(input_file, output_directory, ocr_enabled)
    sys.exit(0 if success else 1)
```

### Step 2: Execute Conversion

**Objective:** Run the conversion script on the user's file.

**Actions:**

```bash
# Define paths
INPUT_FILE="$USER_INPUT_FILE"
OUTPUT_DIR="./converted_docs"

# Execute script
python3 .gemini/tmp/docling_convert.py "$INPUT_FILE" "$OUTPUT_DIR" $OCR_FLAG
```

### Step 3: Result & Validation

**Objective:** meaningful output to the user.

**Actions:**

```bash
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Conversion Complete!"
    echo "📂 Output Directory: $OUTPUT_DIR"
    ls -lh "$OUTPUT_DIR"
else
    echo "❌ Conversion Failed. Please check the error logs above."
fi
```

---

## Error Handling

| Error | Likely Cause | Action |
|-------|-------------|--------|
| Docling not installed | `docling` Python package missing | Offer to install with `pip install docling`; show manual instructions |
| Unsupported file format | File type not in supported list | Inform user of supported formats (PDF, DOCX, PPTX, XLSX, HTML, images); suggest CloudConvert for other formats |
| File not found or access denied | Path incorrect or insufficient permissions | Show exact error; ask user to verify path and file permissions |
| OCR required but unavailable | Scanned PDF with no text layer; `docling[ocr]` not installed | Offer to install OCR extras with `pip install "docling[ocr]"`; explain what OCR does |
| Conversion output empty | File has no extractable text (image-only PDF without OCR) | Suggest enabling OCR option; explain cause |
| Memory error on large file | File too large for available RAM | Suggest processing in smaller chunks; warn about file size |
| Corrupted file | Input file is damaged or incomplete | Inform user the file may be corrupted; ask for a valid copy |

## 📄 Version

**v1.0.1** | Agentic Workflow | Auto-Install
