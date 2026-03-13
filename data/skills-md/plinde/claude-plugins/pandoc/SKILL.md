---
name: pandoc
description: This skill should be used when converting documents between formats (Markdown, DOCX, PDF, HTML, LaTeX, etc.) using pandoc. Use for format conversion, document generation, and preparing markdown for Google Docs or other word processors.
---

# Pandoc Document Conversion Skill

Convert documents between formats using pandoc, the universal document converter.

## Prerequisites

```bash
# Check if pandoc is installed
pandoc --version

# Install via Homebrew if needed
brew install pandoc
```

## Common Conversions

### Markdown to Word (.docx)

```bash
# Basic conversion
pandoc input.md -o output.docx

# With table of contents
pandoc input.md --toc -o output.docx

# With custom reference doc (for styling)
pandoc input.md --reference-doc=template.docx -o output.docx

# Standalone with metadata
pandoc input.md -s --metadata title="Document Title" -o output.docx
```

### Markdown to PDF

```bash
# Requires LaTeX - install one of:
#   brew install --cask basictex      # Smaller (~100MB)
#   brew install --cask mactex-no-gui # Full (~4GB)
# After install: eval "$(/usr/libexec/path_helper)" or new terminal

# Basic conversion (uses pdflatex)
pandoc input.md -o output.pdf

# With table of contents and custom margins
pandoc input.md -s --toc --toc-depth=2 -V geometry:margin=1in -o output.pdf

# Using xelatex (better Unicode support - box drawings, arrows, etc.)
export PATH="/Library/TeX/texbin:$PATH"
pandoc input.md --pdf-engine=xelatex -V geometry:margin=1in -o output.pdf
```

**PDF Engine Selection:**

| Engine | Use When |
|--------|----------|
| `pdflatex` | Default, ASCII content only |
| `xelatex` | Unicode characters (arrows, box-drawing, emojis) |
| `lualatex` | Complex typography, OpenType fonts |

### Markdown to HTML

**Critical:** Always use `-f gfm` (GitHub Flavored Markdown) for proper line break and list handling. Standard markdown collapses consecutive lines into paragraphs.

```bash
# RECOMMENDED: GitHub Flavored Markdown with full styling
pandoc -f gfm -s -H <(cat << 'STYLE'
<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:800px;margin:0 auto;padding:2em;line-height:1.6}
h1{border-bottom:2px solid #333;padding-bottom:0.3em}
h2{border-bottom:1px solid #ccc;padding-bottom:0.2em;margin-top:1.5em}
h3{margin-top:1.2em}
ul,ol{margin:0.5em 0 0.5em 1.5em;padding-left:1em}
ul{list-style-type:disc}ol{list-style-type:decimal}
li{margin:0.3em 0}ul ul,ol ul{list-style-type:circle;margin:0.2em 0 0.2em 1em}
table{border-collapse:collapse;width:100%;margin:1em 0}
th,td{border:1px solid #ddd;padding:8px;text-align:left}
th{background-color:#f5f5f5}
code{background-color:#f4f4f4;padding:2px 6px;border-radius:3px}
pre{background-color:#f4f4f4;padding:1em;overflow-x:auto;border-radius:5px}
blockquote{border-left:4px solid #ddd;margin:1em 0;padding-left:1em;color:#666}
</style>
STYLE
) input.md -o output.html

# Quick version (minimal styling)
pandoc -f gfm -s input.md -o output.html

# With hard line breaks (newlines become <br>)
pandoc -f markdown+hard_line_breaks -s input.md -o output.html

# Self-contained (embeds images/CSS)
pandoc -f gfm -s --embed-resources --standalone input.md -o output.html
```

**Format Options:**

| Option | Use When |
|--------|----------|
| `-f gfm` | Default choice - handles lists, line breaks, tables correctly |
| `-f markdown+hard_line_breaks` | Force all newlines to become `<br>` |
| `-f commonmark` | Strict CommonMark compliance |

### HTML for Print-to-PDF (No LaTeX Required)

When LaTeX isn't available, create styled HTML and print to PDF from browser:

```bash
# Create inline CSS file
cat > /tmp/print-style.css << 'EOF'
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       max-width: 800px; margin: 0 auto; padding: 2em; line-height: 1.6; }
h1 { border-bottom: 2px solid #333; padding-bottom: 0.3em; }
h2 { border-bottom: 1px solid #ccc; padding-bottom: 0.2em; margin-top: 1.5em; }
h3 { margin-top: 1.2em; }
/* Lists - critical for proper rendering */
ul, ol { margin: 0.5em 0 0.5em 1.5em; padding-left: 1em; }
ul { list-style-type: disc; }
ol { list-style-type: decimal; }
li { margin: 0.3em 0; }
ul ul, ol ul { list-style-type: circle; margin: 0.2em 0 0.2em 1em; }
ul ol, ol ol { margin: 0.2em 0 0.2em 1em; }
ul ul ul, ol ul ul { list-style-type: square; }
/* Tables */
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f5f5f5; }
/* Code */
code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
pre { background-color: #f4f4f4; padding: 1em; overflow-x: auto; border-radius: 5px; }
/* Other */
blockquote { border-left: 4px solid #ddd; margin: 1em 0; padding-left: 1em; color: #666; }
@media print { body { max-width: none; } }
EOF

# Convert with embedded styles (ALWAYS use -f gfm)
pandoc -f gfm input.md -s --toc --toc-depth=2 -c /tmp/print-style.css --embed-resources --standalone -o output.html

# Open and print to PDF (Cmd+P > Save as PDF)
open output.html
```

### Word to Markdown

```bash
# Extract markdown from docx
pandoc input.docx -o output.md

# With ATX-style headers
pandoc input.docx --atx-headers -o output.md
```

## Useful Options

| Option | Description |
|--------|-------------|
| `-s` / `--standalone` | Produce standalone document with header/footer |
| `--toc` | Generate table of contents |
| `--toc-depth=N` | TOC depth (default: 3) |
| `-V key=value` | Set template variable |
| `--metadata key=value` | Set metadata field |
| `--reference-doc=FILE` | Use FILE for styling (docx/odt) |
| `--template=FILE` | Use custom template |
| `--highlight-style=STYLE` | Syntax highlighting (pygments, tango, etc.) |
| `--number-sections` | Number section headings |
| `-f FORMAT` | Input format (if not auto-detected) |
| `-t FORMAT` | Output format (if not auto-detected) |

## Format Identifiers

| Format | Identifier |
|--------|------------|
| Markdown | `markdown`, `gfm` (GitHub), `commonmark` |
| Word | `docx` |
| PDF | `pdf` |
| HTML | `html`, `html5` |
| LaTeX | `latex` |
| RST | `rst` |
| EPUB | `epub` |
| ODT | `odt` |
| RTF | `rtf` |

## Google Docs Workflow

To get markdown into Google Docs with formatting preserved:

```bash
# 1. Convert to docx
pandoc document.md -o document.docx

# 2. Upload to Google Drive
# 3. Right-click > Open with > Google Docs
```

Google Docs imports .docx files well and preserves:
- Headings
- Bold/italic
- Lists (bulleted and numbered)
- Tables
- Links
- Code blocks (as monospace)

## PSI Document Conversion

For PSI documents with tables and complex formatting:

```bash
# Convert PSI markdown to Word
pandoc PSI-document.md \
  --standalone \
  --toc \
  --toc-depth=2 \
  -o PSI-document.docx

# Open for review
open PSI-document.docx
```

## Troubleshooting

### Lists/Lines Running Together (HTML)

If bullet points, numbered lists, or consecutive lines merge into one paragraph:

**Cause:** Standard markdown treats consecutive lines as one paragraph. Lists need blank lines before them.

**Fix:** Use GitHub Flavored Markdown (`-f gfm`):
```bash
# Always use -f gfm for reliable formatting
pandoc -f gfm -s input.md -o output.html

# For documents where newlines should be <br> tags
pandoc -f markdown+hard_line_breaks -s input.md -o output.html
```

**Why this happens:**
- Standard markdown: `Line 1\nLine 2` → `<p>Line 1 Line 2</p>` (merged)
- GFM: Better list detection, handles edge cases
- `+hard_line_breaks`: `Line 1\nLine 2` → `Line 1<br>Line 2` (preserved)

### Tables Not Rendering

Pandoc requires proper markdown table syntax:
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

### Code Blocks Missing Highlighting

Use fenced code blocks with language identifier:
```markdown
```python
def example():
    pass
```
```

### PDF Generation Fails

**"pdflatex not found"** - Install LaTeX:
```bash
# Smaller option (~100MB)
brew install --cask basictex

# Full option (~4GB)
brew install --cask mactex-no-gui

# After install, update PATH
eval "$(/usr/libexec/path_helper)"
# Or open a new terminal
```

**Unicode character errors (box-drawing, arrows, emojis):**
```bash
# Use xelatex instead of pdflatex
export PATH="/Library/TeX/texbin:$PATH"
pandoc input.md --pdf-engine=xelatex -o output.pdf
```

**No LaTeX available** - Use HTML print-to-PDF workflow:
```bash
pandoc input.md -s --toc -o output.html
open output.html
# Then Cmd+P > Save as PDF
```

## Self-Test

```bash
# Verify pandoc installation
pandoc --version | head -1

# Test basic conversion
echo "# Test\n\nHello **world**" | pandoc -f markdown -t html
```
