---
name: allmd
description: Converts content to clean markdown. Supports web pages, Google Docs, PDFs, images, videos, audio files, YouTube videos, Word docs, EPUBs, CSVs, PowerPoints, tweets, and RSS feeds. Use when the user wants to convert a URL or file to markdown, extract text from a PDF or image, transcribe a video or audio file, save a web article, export a Google Doc, or get a YouTube transcript.
---

# Convert Anything to Markdown

A CLI tool that converts web pages, Google Docs, PDFs, images, video/audio files, YouTube videos, Word docs, EPUBs, CSVs, PowerPoints, tweets, and RSS feeds into clean markdown. Most converters use AI formatting; web pages use Firecrawl markdown directly.

## Reference Files

| File | Read when |
|------|-----------|
| `references/conversion-options.md` | You need details on shared types, CLI flags, AI formatting, or output options |
| `references/web.md` | Converting a web page URL |
| `references/gdoc.md` | Converting a Google Doc |
| `references/pdf.md` | Converting a PDF file |
| `references/image.md` | Converting an image file |
| `references/video.md` | Converting a video or audio file |
| `references/youtube.md` | Converting a YouTube video |
| `references/docx.md` | Converting a Word document (.docx) |
| `references/epub.md` | Converting an EPUB ebook |
| `references/csv.md` | Converting a CSV or TSV file |
| `references/pptx.md` | Converting a PowerPoint presentation (.pptx) |
| `references/tweet.md` | Converting a tweet / X post |
| `references/rss.md` | Converting an RSS or Atom feed |

## Dispatch Table

| Input | Command | Reference |
|-------|---------|-----------|
| Any URL or file | `allmd <input>` (auto-detect) | Dispatches to the appropriate converter |
| Web URL (http/https) | `allmd web <url>` | `references/web.md` |
| Google Docs URL (`docs.google.com/document/d/...`) | `allmd gdoc <url>` | `references/gdoc.md` |
| YouTube URL (`youtube.com`, `youtu.be`) | `allmd youtube <url>` or `allmd yt <url>` | `references/youtube.md` |
| Twitter/X URL (`twitter.com`, `x.com`) | `allmd tweet <url>` | `references/tweet.md` |
| RSS/Atom feed URL (`/feed`, `/rss`, `.xml`, `.atom`) | `allmd rss <url>` | `references/rss.md` |
| PDF file (`.pdf`) | `allmd pdf <file>` | `references/pdf.md` |
| Image file (`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`) | `allmd image <file>` | `references/image.md` |
| Video file (`.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`, `.flv`, `.wmv`, `.m4v`) | `allmd video <file>` | `references/video.md` |
| Audio file (`.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac`, `.wma`) | `allmd video <file>` | `references/video.md` |
| Word document (`.docx`, `.doc`) | `allmd docx <file>` | `references/docx.md` |
| EPUB ebook (`.epub`) | `allmd epub <file>` | `references/epub.md` |
| CSV/TSV file (`.csv`, `.tsv`) | `allmd csv <file>` | `references/csv.md` |
| PowerPoint (`.pptx`) | `allmd pptx <file>` | `references/pptx.md` |

## Shared Workflow

Most converters follow this pattern:

1. **Validate** input (URL format or file existence/extension)
2. **Extract** content (fetch HTML, parse PDF, read image, transcribe audio, fetch captions)
3. **AI format** — restructures into clean markdown via OpenAI GPT-5-mini
4. **Add frontmatter** — YAML header with title, source, date, type, and type-specific fields
5. **Output** — write to file (`-o`), directory (`-d`), clipboard (`--copy`), or stdout

Web page conversion differs at step 3: `allmd web` uses Firecrawl markdown directly and only applies optional frontmatter.

## CLI Quick Reference

| Command | Example |
|---------|---------|
| `allmd <input>` | `allmd https://example.com` (auto-detect) |
| `allmd web <url>` | `allmd web https://example.com/article` |
| `allmd gdoc <url>` | `allmd gdoc "https://docs.google.com/document/d/abc123/edit"` |
| `allmd youtube <url>` | `allmd yt https://youtu.be/dQw4w9WgXcQ` |
| `allmd tweet <url>` | `allmd tweet https://x.com/user/status/123` |
| `allmd rss <url>` | `allmd rss https://blog.example.com/feed` |
| `allmd pdf <file>` | `allmd pdf report.pdf -o report.md` |
| `allmd image <file>` | `allmd image screenshot.png` |
| `allmd video <file>` | `allmd video recording.mp4` |
| `allmd docx <file>` | `allmd docx document.docx -o doc.md` |
| `allmd epub <file>` | `allmd epub book.epub -o book.md` |
| `allmd csv <file>` | `allmd csv data.csv -o data.md` |
| `allmd pptx <file>` | `allmd pptx slides.pptx -o slides.md` |
| `allmd examples` | Show usage examples |
| `allmd completion install` | Install shell completions |
