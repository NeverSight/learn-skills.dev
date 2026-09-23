---
name: gutenberg
description: >-
  Search, download, and extract public-domain books from Project Gutenberg. Look up books
  by ID or keyword via gutendex, download plain-text and EPUB editions, strip licensing
  boilerplate, extract clean text from EPUB for illustrated works, and classify fiction vs
  non-fiction. Ships a portable CLI script with zero external dependencies. Use when the
  user says "gutenberg", "public domain", "download a book", "classic literature", "free
  ebook", "gutenberg.org", or names any public-domain title or author. Do not use this
  skill for unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Python 3.8+ with zero external dependencies. The CLI uses only the
  Python standard library (urllib.request, json, html.parser, zipfile, re, sys). For
  EPUB extraction, Python 3.8+ with only stdlib is required (zipfile + html.parser).
  The gutendex API (https://gutendex.com) requires no API key or registration. No
  env vars needed for basic operation.
metadata:
  tags: gutenberg, project-gutenberg, books, public-domain, literature, classics,
    ebooks, text-extraction, epub
  sources: https://gutendex.com, https://www.gutenberg.org
  skills: books, public-domain, literature, text-mining, ebooks
---

# Gutenberg — Public Domain Book Toolkit

Search, download, and extract clean text from [Project Gutenberg](https://www.gutenberg.org) — 70,000+ free public-domain ebooks. Ships a portable Python CLI with zero external dependencies.

## Quick Start

```bash
# Search for books
python3 scripts/gutenberg search "Moby Dick"

# Download by Gutenberg ID (plain text)
python3 scripts/gutenberg download 2701 --format txt

# Download EPUB (for illustrated books)
python3 scripts/gutenberg download 2701 --format epub

# Extract clean text (strips PG boilerplate)
python3 scripts/gutenberg extract 2701

# Classify fiction vs non-fiction
python3 scripts/gutenberg classify 2701

# Full pipeline: search → download → extract
python3 scripts/gutenberg pipeline "Alice's Adventures in Wonderland"
```

## How It Works

Project Gutenberg provides **70,000+ free public-domain ebooks** in multiple formats. The gutendex API (https://gutendex.com) offers a free, unauthenticated JSON catalog. No API key required — just curl or this CLI.

### Data Flow

```
User provides title/ID/author
       ↓
gutendex API search → pick book by ID
       ↓
Download plain text (preferred) or EPUB (fallback for illustrated books)
       ↓
Strip PG boilerplate → clean text
       ↓
Classify fiction/non-fiction → extract content
```

## CLI Reference

### `search` — Find books by keyword

```bash
python3 scripts/gutenberg search "Moby Dick"
python3 scripts/gutenberg search "Dracula" --limit 5
python3 scripts/gutenberg search "Sherlock Holmes" --json
python3 scripts/gutenberg search "Alice" --language en
```

Returns: ID, title, author (with life dates), language, subjects, download count. Results sorted by download count (most popular first).

### `metadata` — Get full metadata for a book by ID

```bash
python3 scripts/gutenberg metadata 2701          # Moby Dick
python3 scripts/gutenberg metadata 11            # Alice's Adventures
python3 scripts/gutenberg metadata 1342          # Pride and Prejudice
python3 scripts/gutenberg metadata 1342 --json   # JSON-only output
```

Returns: title, author(s), language(s), subjects, bookshelves, summaries, copyright status, download count, and all available format URLs.

### `download` — Download a book by Gutenberg ID

```bash
# Plain text (UTF-8, preferred — works for most books)
python3 scripts/gutenberg download 2701 --format txt

# EPUB with images (for illustrated/scientific books)
python3 scripts/gutenberg download 2701 --format epub

# HTML (alternative fallback)
python3 scripts/gutenberg download 2701 --format html

# Specify output directory
python3 scripts/gutenberg download 2701 --format txt --output ./books/
```

The file is saved to `./gutenberg-<id>.<ext>` (or `--output` path). Large books may take a moment.

### `extract` — Strip PG boilerplate and produce clean text

```bash
python3 scripts/gutenberg extract 2701            # from downloaded txt
python3 scripts/gutenberg extract 2701 --input ./gutenberg-2701.txt
python3 scripts/gutenberg extract 2701 --format epub  # extract from EPUB
```

Output: clean text without the Project Gutenberg license header/footer. For EPUB extraction (illustrated books), extracts text from all XHTML files and merges them into a single cleaned document.

Size detection: if a plain-text download is under 50KB for a known substantial book, warns that the text may be truncated and recommends EPUB mode.

### `classify` — Classify fiction vs non-fiction

```bash
python3 scripts/gutenberg classify 2701
python3 scripts/gutenberg classify 2701 --json
```

Uses the book's subjects and bookshelves to classify:
- **Fiction signals:** "Fiction", "novels", "short stories", "poetry", "drama", "fantasy", "horror"
- **Non-fiction signals:** "Essays", "History", "Philosophy", "Biography", "Science", "Religion"

Returns: `fiction`, `non-fiction`, or `ambiguous` (with explanation of why).

### `pipeline` — Full fetch pipeline

```bash
python3 scripts/gutenberg pipeline "Moby Dick"                           # search first
python3 scripts/gutenberg pipeline 2701                                   # by known ID
python3 scripts/gutenberg pipeline 2701 --clean /tmp/pipeline-output/     # save cleaned text
```

Runs: search (if title) → metadata → download (txt) → check size → extract (or EPUB fallback) → classify. Prints an executive summary at the end.

### Global Flags

| Flag | Effect |
|------|--------|
| `--json` | Output machine-readable JSON instead of human-readable text |
| `--quiet` | Suppress diagnostic output |
| `--dry-run` | Show what would be done without executing |
| `--output ./dir` | Save downloads to a specific directory |
| `--timeout 30` | Override API timeout (default 15s) |

## Fiction vs Non-Fiction Handling

When the classified result is **fiction**, the extracted text comes from an authored imagination. Consider splitting analysis into two tracks:

| Track | What it covers | Example claims |
|-------|----------------|----------------|
| **Canon** | Facts within the fictional world — named entities, quoted lines, story events, world rules | "In Stoker's text, Dracula can assume wolf, bat, and mist forms" |
| **Craft** | Real-world technique — how the author achieves effect, publication history, literary influence | "Stoker's epistolary form forces the reader to piece together the narrative like an investigator" |
| **Negative space** | Deliberate omissions — what the author notably leaves unspecified | "Dracula is never granted interior voice in the novel" |

When classified as **non-fiction**, claims can be treated as real-world factual assertions about the subject matter.

## Known Gotchas

- **Plain text truncation for illustrated books** — Books with diagrams, figures, or equations (geometry texts, scientific works, art books) may have plain-text downloads silently cut to 5-10KB (just the PG header). Always check file size. Under 50KB for a known substantial book → switch to EPUB extraction. The `pipeline` command does this check automatically.
- **Gutendex can be slow or timeout** — The API is a free service and can be slow for less popular books. The CLI uses a 15-second default timeout. Use `--timeout 30` for slow responses, or navigate directly to `https://www.gutenberg.org/ebooks/<id>` as a fallback.
- **HTML downloads include navigation markup** — HTML downloads contain site navigation and formatting. Prefer plain text or EPUB for clean text extraction.
- **Rare books may 404 on certain format URLs** — Not every book has every format. The CLI tries UTF-8 plain text first, falls back to US-ASCII, then to the `-0.txt` file path, then to EPUB, then to HTML. The `download` command reports which format was actually retrieved.
- **Rate limiting** — Gutendex is unauthenticated but rate-limited. Batch requests with `sleep 1` between calls for more than 10 rapid-fire requests.
- **utf-8 vs us-ascii** — Gutendex returns both a `text/plain; charset=utf-8` and a `text/plain; charset=us-ascii` URL. Prefer UTF-8; fall back to US-ASCII if the UTF-8 URL returns a 404.
- **Fiction classification ambiguity** — Books with both fiction and non-fiction subjects (e.g. "Historical Fiction" + "History") are marked `ambiguous`. Use `--json` to inspect the subject list and decide manually.

## References

- [scripts/gutenberg](scripts/gutenberg) — Portable Python CLI. Zero external dependencies (stdlib only). Covers all major Gutenberg workflows: search, download (txt/epub/html), boilerplate stripping, EPUB text extraction, fiction classification, and the full pipeline.
- [references/epub-extraction.md](references/epub-extraction.md) — EPUB text extraction details for illustrated books, with expanded Python walkthrough and format detection tips.
- [Project Gutenberg](https://www.gutenberg.org) — 70,000+ free ebooks.
- [Gutendex API](https://gutendex.com) — JSON web API for the Project Gutenberg catalog.
