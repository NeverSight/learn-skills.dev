---
name: far
description: File-Augmented Retrieval — generate persistent .meta sidecar files for PDFs, images, spreadsheets, videos and more, making every binary file readable to AI coding agents.
allowed-tools: Read, Write, Edit, Bash, Glob
user-invocable: true
---

# 📄 /far - File-Augmented Retrieval

> **"Making Every File Readable to Coding Agents via Persistent .meta Sidecars"**

FAR is a file augmentation protocol that generates persistent `.meta` sidecar files for binary documents (PDF, DOCX, XLSX, PPTX, Images, etc.). This allows AI coding agents (like OpenClaw, Cursor, GitHub Copilot) to "read" non-text files directly from the file system without requiring external RAG infrastructure.

**Current Version:** 1.0.0
**Author:** Kelly Peilin Chan

---

## 🚀 The Problem: AI "Blindness"

AI agents operating in a repository can read code (`.py`, `.js`, `.md`), but they are blind to 30-40% of critical context stored in binary formats:
- **Product Specs**: `requirements.docx`
- **Design Mocks**: `architecture.png`
- **Financial Data**: `budget.xlsx`
- **Contracts**: `agreement.pdf`

When an agent encounters `budget.xlsx`, it sees opaque bytes. It cannot reason about the content.

## 💡 The Solution: Persistent Sidecars

FAR solves this by generating a human-readable and machine-readable `.meta` file next to every binary file.

**Example:**
```
project/
├── budget.xlsx         (Binary, opaque)
└── budget.xlsx.meta    (Markdown, readable)
```

The agent simply reads `budget.xlsx.meta` to understand the spreadsheet. No vector database, no API calls, no runtime overhead.

---

## ✨ Features

### 1. Broad Format Support
FAR extracts text and structure from a wide range of formats:
*   **📄 PDF** (`.pdf`): Full text extraction with layout preservation. **OCR fallback** for scanned PDFs. **Embedded image extraction** (pdfimages + OCR/Vision).
*   **📝 Word** (`.docx`, `.doc`): Text extraction.
*   **📊 Excel** (`.xlsx`): Sheet data converted to Markdown tables.
*   **📽️ PowerPoint** (`.pptx`): Slide text extraction.
*   **🖼️ Images** (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`): **OCR** (Tesseract) + **Apple Vision (on-device, macOS)** + **AI Vision** (GPT-4o) if configured.
*   **🎬 Media** (`.mp4`, `.mov`, `.mp3`, `.wav`, `.m4a`, `.flac`): Technical metadata (FFprobe) + **Apple Vision video-frame analysis (macOS)** + **AI Transcription** (Whisper) if configured.
*   **📋 CSV** (`.csv`): Data rendered as Markdown tables (up to 100 rows).
*   **📓 Jupyter Notebook** (`.ipynb`): Markdown cells, code cells, and outputs.
*   **📚 EPUB** (`.epub`): Full text extracted from all chapters in spine order.
*   **📦 Tar** (`.tar`, `.tar.gz`, `.tgz`, `.bz2`, `.xz`): File listing with sizes.
*   **📧 Email** (`.eml`, `.msg`): Headers, body text, and attachment list.
*   **📝 RTF** (`.rtf`): Plain text extraction via control word stripping.
*   **🗄️ SQLite** (`.db`, `.sqlite`, `.sqlite3`): Table schemas + latest 20 rows per table as Markdown tables.
*   **📊 Parquet** (`.parquet`): Schema and row count via `pyarrow` (optional). *[Metadata only]*
*   **🎨 Design** (`.fig`, `.sketch`, `.xd`): File size and page/canvas count. *[Metadata only]*
*   **💻 Code/Text** (`.py`, `.js`, `.ts`, `.go`, `.rs`, `.md`, `.json`, ...): Direct content mirroring.

### 2. Intelligent Caching (Incremental Build)
FAR is designed for speed. It uses a **two-layer caching mechanism**:
1.  **Fast Check (mtime & size)**: If the file hasn't been modified, it skips processing instantly (0.003s).
2.  **Content Check (SHA256)**: If mtime changed, it calculates the file hash. If the content is identical, it updates the timestamp but skips re-extraction.

For directory summaries, FAR also avoids noisy rewrites: if `.dir.meta` summary content is unchanged, it keeps the file untouched (no `extracted_at` churn).

### 3. Directory Summaries (`.dir.meta`)
FAR generates a `.dir.meta` file in every directory, providing a high-level summary of all files within. This allows agents to "browse" a folder and understand its contents without reading every single file.

### 4. Git LFS Support
FAR automatically handles Git LFS pointer files. It will attempt to pull the real content before processing, ensuring you don't get empty metadata for LFS-tracked files.

---

## 🛠️ Usage

### Installation
The skill is pre-installed in the OpenClaw workspace:
```bash
~/.openclaw/workspace/.agents/skills/far/far_gen.py
```
A symlink is available as `far`:
```bash
far [directory_or_file]
```

### Commands

**Scan current directory (Recursive):**
```bash
far
```

**Scan specific directory:**
```bash
far ~/Documents/projects/files
```

**Process single file:**
```bash
far report.pdf
```

**Force regeneration (Ignore cache):**
```bash
far . --force
```

### Configuration (AI Features)
To enable AI features (Audio Transcription, Image Description), create a `.env` file in the skill directory or your home folder `~/.far.env`. 
Copy `.env.example` as a template:

```bash
OPENAI_API_KEY=sk-your-key-here
# Optional
OPENAI_BASE_URL=https://api.openai.com/v1
# Optional (macOS default: enabled)
FAR_USE_APPLE_VISION=1
# Optional (macOS default: enabled)
FAR_USE_MACOS_METADATA=1
# Optional tuning
FAR_APPLE_VISION_TIMEOUT=25
FAR_APPLE_VISION_MAX_FRAMES=6
```

If API keys are missing, FAR gracefully falls back to local tools (Tesseract, FFprobe),
and on macOS it also uses Apple Vision + Spotlight metadata on-device by default.

### Configuration (Ignore)
Create a `.farignore` file in your project root to exclude files or directories from scanning.
```gitignore
# .farignore
node_modules
.git
secrets/
*.tmp
```

---

## 🤖 Agent Integration

Add one rule to `AGENTS.md` or your system prompt:

```
## File Reading with FAR

When navigating a directory, first read `.dir.meta` for a high-level overview
before opening individual files.

When you encounter a binary file you cannot read directly
(.png, .pdf, .xlsx, .mp4, .fig, .db, etc.), check for a .meta file
beside it — it contains the extracted content as Markdown.

Navigation strategy:
1. Read <dir>/.dir.meta to understand directory structure
2. Read <file>.meta to access binary file content
3. Fall back to reading the source file only if no .meta exists
```

---

## 🏗️ Protocol Specification (v1)

Each `.meta` file follows a strict format with a YAML frontmatter header and Markdown body.

```markdown
--far_version: 1
source:
  sha256: 5a1cc2b8d...
  mime: application/pdf
  size: 129509
  mtime: 1708845210.5
extract:
  pipeline: far_gen_v14
  extracted_at: 2026-02-27T10:00:00Z
  deterministic: true
layout:
  pages: 24
---
# filename.pdf

[Extracted Content Here...]
```

Cache invalidation: a `.meta` is stale if `sha256` or `pipeline` version has changed.

---

## 🤝 Contributing

**Roadmap:**
- [x] PDF/Word/Excel/PowerPoint Support
- [x] Incremental Caching (SHA-256 + mtime)
- [x] Directory Summaries (`.dir.meta`)
- [x] OCR for Images/Scanned PDFs (Tesseract)
- [x] Media Metadata (FFprobe) + Transcription (Whisper)
- [x] AI Vision for Images (GPT-4o)
- [x] Apple Vision for Images (on-device, macOS)
- [x] Apple Vision for Video Frames (on-device labels/OCR/faces/barcodes/pose)
- [x] Apple Vision Feature Print fingerprint (on-device embedding hash)
- [x] macOS Spotlight metadata enrichment (mdls)
- [x] PDF Embedded Image Extraction
- [x] CSV → Markdown Tables
- [x] Jupyter Notebook Support
- [x] EPUB, ZIP/TAR, Email, RTF
- [x] SQLite Schema + Data Preview
- [x] Parquet Schema, Design File Metadata
- [x] Pipeline version stale detection
- [x] Layout frontmatter (pages/sheets/slides)
- [x] Full glob support in `.farignore`
- [ ] MCP resource server integration
- [ ] PII redaction rules
- [ ] Rust implementation for CI/CD speed
