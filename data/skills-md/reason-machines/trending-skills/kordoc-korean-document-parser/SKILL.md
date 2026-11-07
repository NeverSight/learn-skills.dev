---
name: kordoc-korean-document-parser
description: Parse HWP, HWPX, and PDF Korean documents to Markdown using kordoc — supports CLI, programmatic API, and MCP server integration.
triggers:
  - parse hwp file to markdown
  - convert korean document to text
  - extract text from hwpx
  - parse pdf to markdown with kordoc
  - compare two hwp documents
  - extract form fields from korean document
  - set up kordoc mcp server
  - convert hwp hwpx pdf to structured data
---

# kordoc Korean Document Parser

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

kordoc is a TypeScript library and CLI for parsing Korean government documents (HWP 5.x, HWPX, PDF) into Markdown and structured `IRBlock[]` data. It handles proprietary HWP binary formats, table extraction, form field recognition, document diffing, and reverse Markdown→HWPX generation.

---

## Installation

```bash
# Core library
npm install kordoc

# PDF support (optional peer dependency)
npm install pdfjs-dist

# CLI (no install needed)
npx kordoc document.hwpx
```

---

## Core API

### Auto-detect and Parse Any Document

```typescript
import { parse } from "kordoc"
import { readFileSync } from "fs"

const buffer = readFileSync("document.hwpx")
const result = await parse(buffer.buffer) // ArrayBuffer required

if (result.success) {
  console.log(result.markdown)   // string: full Markdown
  console.log(result.blocks)     // IRBlock[]: structured data
  console.log(result.metadata)   // { title, author, createdAt, pageCount, ... }
  console.log(result.outline)    // OutlineItem[]: document structure
  console.log(result.warnings)   // ParseWarning[]: skipped elements
} else {
  console.error(result.error)    // string message
  console.error(result.code)     // ErrorCode: "ENCRYPTED" | "ZIP_BOMB" | "IMAGE_BASED_PDF" | ...
}
```

### Format-Specific Parsers

```typescript
import { parseHwpx, parseHwp, parsePdf, detectFormat } from "kordoc"

// Detect format first
const fmt = detectFormat(buffer.buffer) // "hwpx" | "hwp" | "pdf" | "unknown"

// Parse by format
const hwpxResult = await parseHwpx(buffer.buffer)
const hwpResult  = await parseHwp(buffer.buffer)
const pdfResult  = await parsePdf(buffer.buffer)
```

### Parse Options

```typescript
import { parse, ParseOptions } from "kordoc"

const result = await parse(buffer.buffer, {
  pages: "1-3",          // page range string
  // pages: [1, 5, 10], // or specific page numbers
  ocr: async (pageImage, pageNumber, mimeType) => {
    // Pluggable OCR for image-based PDFs
    // pageImage: ArrayBuffer of the page image
    return await myOcrService.recognize(pageImage)
  }
})
```

---

## Working with IRBlocks

```typescript
import type { IRBlock, IRBlockType, IRTable, IRCell } from "kordoc"

// IRBlock types: "heading" | "paragraph" | "table" | "list" | "image" | "separator"
for (const block of result.blocks) {
  if (block.type === "heading") {
    console.log(`H${block.level}: ${block.text}`)
    console.log(block.bbox)       // { x, y, width, height, page }
  }

  if (block.type === "table") {
    const table = block as IRTable
    for (const row of table.rows) {
      for (const cell of row) {
        console.log(cell.text, cell.colspan, cell.rowspan)
      }
    }
  }

  if (block.type === "paragraph") {
    console.log(block.text)
    console.log(block.style)      // InlineStyle: { bold, italic, fontSize, ... }
    console.log(block.pageNumber)
  }
}
```

### Convert Blocks Back to Markdown

```typescript
import { blocksToMarkdown } from "kordoc"

const markdown = blocksToMarkdown(result.blocks)
```

---

## Document Comparison

```typescript
import { compare } from "kordoc"

const bufA = readFileSync("v1.hwp").buffer
const bufB = readFileSync("v2.hwpx").buffer  // cross-format supported

const diff = await compare(bufA, bufB)

console.log(diff.stats)
// { added: 3, removed: 1, modified: 5, unchanged: 42 }

for (const d of diff.diffs) {
  // d.type: "added" | "removed" | "modified" | "unchanged"
  // d.blockA, d.blockB: IRBlock
  // d.cellDiffs: CellDiff[] for table blocks
  console.log(d.type, d.blockA?.text ?? d.blockB?.text)
}
```

---

## Form Field Extraction

```typescript
import { parse, extractFormFields } from "kordoc"

const result = await parse(buffer.buffer)
if (result.success) {
  const form = extractFormFields(result.blocks)

  console.log(form.confidence)  // 0.0–1.0
  for (const field of form.fields) {
    // { label: "성명", value: "홍길동", row: 0, col: 0 }
    console.log(`${field.label}: ${field.value}`)
  }
}
```

---

## Markdown → HWPX Generation

```typescript
import { markdownToHwpx } from "kordoc"
import { writeFileSync } from "fs"

const markdown = `
# 제목

본문 내용입니다.

| 구분 | 내용 |
| --- | --- |
| 항목1 | 값1 |
| 항목2 | 값2 |
`

const hwpxBuffer = await markdownToHwpx(markdown)
writeFileSync("output.hwpx", Buffer.from(hwpxBuffer))
```

---

## CLI Usage

```bash
# Basic conversion — output to stdout
npx kordoc document.hwpx

# Save to file
npx kordoc document.hwp -o output.md

# Batch convert all PDFs to a directory
npx kordoc *.pdf -d ./converted/

# JSON output with blocks + metadata
npx kordoc report.hwpx --format json

# Parse specific pages only
npx kordoc report.hwpx --pages 1-3

# Watch mode — auto-convert new files
npx kordoc watch ./incoming -d ./output

# Watch with webhook notification on conversion
npx kordoc watch ./docs --webhook https://api.example.com/hook
```

---

## MCP Server Setup

Add to your MCP config (Claude Desktop, Cursor, Windsurf):

```json
{
  "mcpServers": {
    "kordoc": {
      "command": "npx",
      "args": ["-y", "kordoc-mcp"]
    }
  }
}
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `parse_document` | Parse HWP/HWPX/PDF → Markdown + metadata + outline + warnings |
| `detect_format` | Detect file format via magic bytes |
| `parse_metadata` | Extract only metadata (fast, no full parse) |
| `parse_pages` | Parse a specific page range |
| `parse_table` | Extract the Nth table from a document |
| `compare_documents` | Diff two documents (cross-format supported) |
| `parse_form` | Extract form fields as structured JSON |

---

## TypeScript Types Reference

```typescript
import type {
  // Results
  ParseResult, ParseSuccess, ParseFailure,
  ErrorCode,        // "ENCRYPTED" | "ZIP_BOMB" | "IMAGE_BASED_PDF" | ...

  // Blocks
  IRBlock, IRBlockType, IRTable, IRCell, CellContext,

  // Metadata & structure
  DocumentMetadata, OutlineItem,
  ParseWarning, WarningCode,
  BoundingBox,      // { x, y, width, height, page }
  InlineStyle,      // { bold, italic, fontSize, color, ... }

  // Options
  ParseOptions, FileType,
  OcrProvider,      // async (image, pageNum, mime) => string
  WatchOptions,

  // Diff
  DiffResult, BlockDiff, CellDiff, DiffChangeType,

  // Forms
  FormField, FormResult,
} from "kordoc"
```

---

## Common Patterns

### Batch Process Files with Error Handling

```typescript
import { parse, detectFormat } from "kordoc"
import { readFileSync } from "fs"
import { glob } from "glob"

const files = await glob("./docs/**/*.{hwp,hwpx,pdf}")

for (const file of files) {
  const buffer = readFileSync(file)
  const fmt = detectFormat(buffer.buffer)

  if (fmt === "unknown") {
    console.warn(`Skipping unknown format: ${file}`)
    continue
  }

  const result = await parse(buffer.buffer)

  if (!result.success) {
    if (result.code === "ENCRYPTED") {
      console.warn(`Encrypted, skipping: ${file}`)
    } else if (result.code === "IMAGE_BASED_PDF") {
      console.warn(`Image-based PDF needs OCR: ${file}`)
    } else {
      console.error(`Failed: ${file} — ${result.error}`)
    }
    continue
  }

  console.log(`Parsed ${file}: ${result.blocks.length} blocks`)
}
```

### Extract All Tables from a Document

```typescript
import { parse } from "kordoc"
import type { IRTable } from "kordoc"

const result = await parse(buffer.buffer)
if (result.success) {
  const tables = result.blocks.filter(b => b.type === "table") as IRTable[]

  tables.forEach((table, i) => {
    console.log(`\n--- Table ${i + 1} ---`)
    for (const row of table.rows) {
      const cells = row.map(cell => cell.text.trim()).join(" | ")
      console.log(`| ${cells} |`)
    }
  })
}
```

### OCR with Tesseract.js

```typescript
import { parse } from "kordoc"
import Tesseract from "tesseract.js"

const result = await parse(buffer.buffer, {
  ocr: async (pageImage, pageNumber, mimeType) => {
    const blob = new Blob([pageImage], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const { data } = await Tesseract.recognize(url, "kor+eng")
    URL.revokeObjectURL(url)
    return data.text
  }
})
```

### Watch Mode Programmatic API

```typescript
import { watch } from "kordoc"

const watcher = watch("./incoming", {
  output: "./converted",
  webhook: process.env.WEBHOOK_URL,
  onFile: async (file, result) => {
    if (result.success) {
      console.log(`Converted: ${file}`)
    }
  }
})

// Stop watching
watcher.stop()
```

---

## Troubleshooting

**`buffer.buffer` vs `Buffer`** — kordoc requires `ArrayBuffer`, not Node.js `Buffer`. Always pass `readFileSync("file").buffer` or use `.buffer` on a `Uint8Array`.

**PDF tables not detected** — Line-based detection requires pdfjs-dist installed. Install it: `npm install pdfjs-dist`. For borderless tables, kordoc uses cluster-based heuristics automatically.

**`"IMAGE_BASED_PDF"` error** — The PDF contains scanned images with no text layer. Provide an `ocr` function in parse options.

**`"ENCRYPTED"` error** — HWP DRM/password-protected files cannot be parsed without the decryption key. No workaround.

**Korean characters garbled in output** — Ensure your terminal/file uses UTF-8 encoding. kordoc outputs UTF-8 Markdown by default.

**Large files are slow** — Use `pages` option to parse only needed pages: `parse(buf, { pages: "1-5" })`. Metadata-only extraction is faster: `parse_metadata` MCP tool or check `result.metadata` directly.

**HWP table columns wrong** — Update to v1.6.1+. Earlier versions had a 2-byte offset misalignment in LIST_HEADER parsing causing column explosion.
