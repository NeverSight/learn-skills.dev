---
name: markitdown-skill
description: OpenClaw agent skill for converting documents to Markdown. Documentation and utilities for Microsoft's MarkItDown library. Supports PDF, Word, PowerPoint, Excel, images (OCR), audio (transcription), HTML, YouTube.
metadata:
  openclaw:
    emoji: "📄"
    homepage: https://github.com/karmanverma/markitdown-skill
    requires:
      bins: ["python3", "pip", "markitdown"]
    install:
      - id: "markitdown"
        kind: "pip"
        package: "markitdown[all]"
        bins: ["markitdown"]
        label: "Install MarkItDown CLI (pip)"
---

# MarkItDown Skill

Documentation and utilities for converting documents to Markdown using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library.

> **Note:** This skill provides documentation and a batch script. The actual conversion is done by the `markitdown` CLI/library installed via pip.

## When to Use

**Use markitdown for:**
- 📄 Fetching documentation (README, API docs)
- 🌐 Converting web pages to markdown
- 📝 Document analysis (PDFs, Word, PowerPoint)
- 🎬 YouTube transcripts
- 🖼️ Image text extraction (OCR)
- 🎤 Audio transcription

## Quick Start

```bash
# Convert file to markdown
markitdown document.pdf -o output.md

# Convert URL
markitdown https://example.com/docs -o docs.md
```

## Supported Formats

| Format | Features |
|--------|----------|
| PDF | Text extraction, structure |
| Word (.docx) | Headings, lists, tables |
| PowerPoint | Slides, text |
| Excel | Tables, sheets |
| Images | OCR + EXIF metadata |
| Audio | Speech transcription |
| HTML | Structure preservation |
| YouTube | Video transcription |

## Installation

The skill requires Microsoft's `markitdown` CLI:

```bash
pip install 'markitdown[all]'
```

Or install specific formats only:
```bash
pip install 'markitdown[pdf,docx,pptx]'
```

## Common Patterns

### Fetch Documentation
```bash
markitdown https://github.com/user/repo/blob/main/README.md -o readme.md
```

### Convert PDF
```bash
markitdown document.pdf -o document.md
```

### Batch Convert
```bash
# Using included script
python ~/.openclaw/skills/markitdown/scripts/batch_convert.py docs/*.pdf -o markdown/ -v

# Or shell loop
for file in docs/*.pdf; do
  markitdown "$file" -o "${file%.pdf}.md"
done
```

## Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

## Troubleshooting

### "markitdown not found"
```bash
pip install 'markitdown[all]'
```

### OCR Not Working
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

## What This Skill Provides

| Component | Source |
|-----------|--------|
| `markitdown` CLI | Microsoft's pip package |
| `markitdown` Python API | Microsoft's pip package |
| `scripts/batch_convert.py` | This skill (utility) |
| Documentation | This skill |

## See Also

- [USAGE-GUIDE.md](USAGE-GUIDE.md) - Detailed examples
- [reference.md](reference.md) - Full API reference
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - Upstream library
