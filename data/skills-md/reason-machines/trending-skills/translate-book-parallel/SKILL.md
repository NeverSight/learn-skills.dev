---
name: translate-book-parallel
description: Translate entire books (PDF/DOCX/EPUB) into any language using Claude Code parallel subagents with resumable chunked pipeline
triggers:
  - translate this book to another language
  - convert my PDF to Spanish
  - translate a book using Claude Code
  - parallel book translation with subagents
  - translate epub to Chinese
  - translate docx to Japanese
  - book translation pipeline
  - translate PDF to any language
---

# Translate Book (Parallel Subagents)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Claude Code skill that translates entire books (PDF/DOCX/EPUB) into any language using parallel subagents. Each chunk gets an isolated context window — preventing truncation and context accumulation that plague single-session translation.

## Pipeline Overview

```
Input (PDF/DOCX/EPUB)
  │
  ▼
Calibre ebook-convert → HTMLZ → HTML → Markdown
  │
  ▼
Split into chunks (~6000 chars each)
  │  manifest.json tracks SHA-256 hashes
  ▼
Parallel subagents (8 concurrent by default)
  │  each: read chunk → translate → write output_chunk*.md
  ▼
Validate (manifest hash check, 1:1 source↔output match)
  │
  ▼
Merge → Pandoc → HTML (with TOC) → Calibre → DOCX / EPUB / PDF
```

## Prerequisites

```bash
# 1. Calibre (provides ebook-convert)
# macOS
brew install --cask calibre
# Linux
sudo apt-get install calibre
# Or download from https://calibre-ebook.com/

# 2. Pandoc
brew install pandoc        # macOS
sudo apt-get install pandoc # Linux

# 3. Python dependencies
pip install pypandoc beautifulsoup4
```

Verify all tools are available:

```bash
ebook-convert --version
pandoc --version
python3 -c "import pypandoc; print('pypandoc ok')"
```

## Installation

**Option A: npx (recommended)**

```bash
npx skills add deusyu/translate-book -a claude-code -g
```

**Option B: ClawHub**

```bash
clawhub install translate-book
```

**Option C: Git clone**

```bash
git clone https://github.com/deusyu/translate-book.git ~/.claude/skills/translate-book
```

## Usage in Claude Code

Once the skill is installed, use natural language inside Claude Code:

```
translate /path/to/book.pdf to Chinese
```

```
translate ~/Downloads/mybook.epub to Japanese
```

```
/translate-book translate /path/to/book.docx to French
```

The skill orchestrates the full pipeline automatically.

## Supported Languages

| Code | Language   |
|------|-----------|
| `zh` | Chinese    |
| `en` | English    |
| `ja` | Japanese   |
| `ko` | Korean     |
| `fr` | French     |
| `de` | German     |
| `es` | Spanish    |

Language codes are extensible — add new ones in the skill definition.

## Running Pipeline Steps Manually

### Step 1: Convert to Markdown Chunks

```bash
python3 scripts/convert.py /path/to/book.pdf --olang zh
```

This produces inside `{book_name}_temp/`:
- `chunk0001.md`, `chunk0002.md`, ... (source chunks, ~6000 chars each)
- `manifest.json` (SHA-256 hashes for validation)

```bash
# For EPUB input
python3 scripts/convert.py /path/to/book.epub --olang ja

# For DOCX input
python3 scripts/convert.py /path/to/book.docx --olang fr
```

### Step 2: Translate (Parallel Subagents)

The skill handles this step — it launches 8 concurrent subagents per batch, each translating one chunk independently:

```
# Each subagent receives exactly this task:
Read chunk0042.md → translate to target language → write output_chunk0042.md
```

**Resumable:** Already-translated chunks (valid `output_chunk*.md` files) are skipped on re-run.

### Step 3: Merge and Build All Formats

```bash
python3 scripts/merge_and_build.py \
  --temp-dir book_name_temp \
  --title "《Book Title in Target Language》"
```

Before merging, validation checks:
- Every source chunk has a matching output file (1:1)
- Source chunk hashes match `manifest.json` (no stale outputs)
- No output files are empty

Outputs produced:

| File | Description |
|------|-------------|
| `output.md` | Merged translated Markdown |
| `book.html` | Web version with floating TOC |
| `book.docx` | Word document |
| `book.epub` | E-book format |
| `book.pdf` | Print-ready PDF |

## Project Structure

```
translate-book/
├── SKILL.md                    # Claude Code skill definition (orchestrator)
├── scripts/
│   ├── convert.py              # PDF/DOCX/EPUB → Markdown chunks via Calibre HTMLZ
│   ├── manifest.py             # SHA-256 chunk tracking and merge validation
│   ├── merge_and_build.py      # Merge chunks → HTML → DOCX/EPUB/PDF
│   ├── calibre_html_publish.py # Calibre wrapper for format conversion
│   ├── template.html           # Web HTML template with floating TOC
│   └── template_ebook.html     # Ebook HTML template
└── README.md
```

## How Manifest Validation Works

```python
# scripts/manifest.py (conceptual usage)

# During convert.py — records source hashes
manifest = {
    "chunk0001.md": "sha256:abc123...",
    "chunk0002.md": "sha256:def456...",
    # ...
}

# During merge_and_build.py — validates before merging
# 1. Check every chunk has a corresponding output_chunk
# 2. Re-hash source chunks and compare against manifest
# 3. Reject if any hash mismatches (stale/corrupt output)
# 4. Reject if any output file is empty
```

If validation fails, the script auto-deletes stale `output.md` and re-merges from valid chunk outputs.

## Real-World Example: Translate a Technical Book

```bash
# 1. Install the skill
npx skills add deusyu/translate-book -a claude-code -g

# 2. Open Claude Code in your working directory
cd ~/books

# 3. Say in Claude Code:
# "translate clean-code.pdf to Chinese"

# Claude Code will:
# - Run convert.py to split into chunks
# - Launch 8 parallel subagents per batch
# - Each subagent translates one chunk
# - Validate all outputs via manifest
# - Merge and build all formats

# 4. Outputs appear in:
ls clean-code_temp/
# chunk0001.md  chunk0002.md  ...  (source)
# output_chunk0001.md  ...         (translated)
# manifest.json
# output.md
# book.html
# book.docx
# book.epub
# book.pdf
```

## Resuming an Interrupted Translation

```bash
# If translation is interrupted, just re-run the same command:
# "translate clean-code.pdf to Chinese"

# The skill detects existing output_chunk*.md files
# and skips already-translated chunks automatically.
# Only missing or failed chunks are retried.
```

## Changing Output Metadata After Translation

If you need to update the title, author, template, or image assets without re-translating:

```bash
# Delete only the final artifacts (keeps translated chunks)
cd book_name_temp/
rm -f output.md book*.html book.docx book.epub book.pdf

# Re-run merge step
python3 ../scripts/merge_and_build.py \
  --temp-dir . \
  --title "《New Title》"
```

**Do NOT delete chunk files** — those are your translated content. Only delete final artifacts when changing metadata.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Calibre ebook-convert not found` | Install Calibre; ensure `ebook-convert` is in `$PATH` |
| `Manifest validation failed` | Source chunks changed — re-run `convert.py` |
| `Missing source chunk` | Source file deleted — re-run `convert.py` to regenerate |
| Incomplete translation | Re-run the skill — resumes from last valid chunk |
| Changed title/template but output unchanged | Delete `output.md`, `book*.html`, `book.docx`, `book.epub`, `book.pdf` then re-run `merge_and_build.py` |
| `output.md exists but manifest invalid` | Script auto-deletes stale output and re-merges |
| PDF generation fails | Verify Calibre has PDF output support; try `ebook-convert --help` |
| Empty output chunks | Retry failed chunks; check API rate limits |

## Diagnosing Chunk Issues

```bash
# Check which chunks are missing translation
ls book_temp/chunk*.md | wc -l          # total source chunks
ls book_temp/output_chunk*.md | wc -l   # translated chunks so far

# Find missing output chunks
for f in book_temp/chunk*.md; do
  base=$(basename "$f" .md)
  out="book_temp/output_${base}.md"
  if [ ! -f "$out" ] || [ ! -s "$out" ]; then
    echo "Missing: $out"
  fi
done

# Check manifest
cat book_temp/manifest.json | python3 -m json.tool | head -30
```

## Configuration Tips

- **Chunk size:** ~6000 chars per chunk is the default. Smaller chunks = more parallelism but more API calls.
- **Concurrency:** Default is 8 parallel subagents per batch. Adjust in `SKILL.md` if hitting rate limits.
- **Languages:** Add new language codes to the skill triggers and translation prompt in `SKILL.md`.
- **Templates:** Customize `scripts/template.html` and `scripts/template_ebook.html` for different HTML/ebook styling.

## Key Design Principles

1. **Isolated context per chunk** — each subagent starts fresh, preventing context overflow on long books
2. **Hash-based integrity** — SHA-256 tracking catches stale or corrupt translated chunks before merging
3. **Resumable at chunk granularity** — never re-translate what's already done
4. **Format-agnostic input** — Calibre handles PDF/DOCX/EPUB normalization before the pipeline begins
5. **Multiple output formats** — single pipeline produces HTML, DOCX, EPUB, and PDF simultaneously
