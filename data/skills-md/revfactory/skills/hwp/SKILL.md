---
name: hwp
description: "Use this skill whenever the user wants to do anything with HWP or HWPX files. This includes reading or extracting text/tables/images from HWP files, converting HWP to markdown or other formats, creating HWPX files from markdown/text, parsing HWP binary (OLE2/CFB) or HWPX (ZIP/XML) formats, and handling Korean document processing. If the user mentions a .hwp or .hwpx file, or asks about 한글 문서 processing, use this skill."
---

# HWP/HWPX Processing Guide

## Overview

HWP is the native format for Hancom's "한글" word processor, widely used in South Korea. Two formats exist:

| Format | Container | Detection | Extension |
|--------|-----------|-----------|-----------|
| **HWP (Binary)** | OLE2/CFB compound file | Magic bytes `0xD0 0xCF 0x11 0xE0` | `.hwp` |
| **HWPX** | ZIP archive with XML | Magic bytes `0x50 0x4B` (PK) | `.hwpx` |

For advanced patterns used in the MDView project (Web Workers, React hooks, progress tracking), see REFERENCE.md.

## Quick Start

### Node.js / TypeScript — Read HWP Binary

```typescript
import * as CFB from 'cfb';
import pako from 'pako';

// Read HWP binary file
const data = fs.readFileSync('document.hwp');
const cfb = CFB.read(data);

// Check encryption
const fileHeader = CFB.find(cfb, '/FileHeader');
if (fileHeader) {
  const flags = fileHeader.content[36] | (fileHeader.content[37] << 8);
  const isEncrypted = (flags & 0x02) !== 0;
  if (isEncrypted) throw new Error('Encrypted HWP files are not supported');
}

// Check compression flag
const isCompressed = (fileHeader.content[36] & 0x01) !== 0;

// Read body sections
const section = CFB.find(cfb, '/BodyText/Section0');
if (section && section.content) {
  let content = section.content;
  if (isCompressed) {
    content = pako.inflate(new Uint8Array(content));
  }
  // Parse binary records from content...
}
```

### Node.js / TypeScript — Read HWPX

```typescript
import JSZip from 'jszip';

const zip = await JSZip.loadAsync(fileBuffer);

// Find section XML files
const sectionFiles = Object.keys(zip.files)
  .filter(f => /Contents\/section\d+\.xml/i.test(f))
  .sort();

for (const sectionFile of sectionFiles) {
  const xml = await zip.file(sectionFile)!.async('string');
  // Parse XML to extract text from <hp:t> tags
  const textMatches = xml.match(/<hp:t[^>]*>([\s\S]*?)<\/hp:t>/g);
  // ...
}

// Extract images from BinData/
const imageFiles = Object.keys(zip.files)
  .filter(f => /BinData\//i.test(f) && !f.endsWith('/'));
```

### Python — Read HWP Binary

```python
import olefile
import zlib
import struct

def read_hwp(filepath):
    ole = olefile.OleFileIO(filepath)

    # Check encryption
    header = ole.openstream('FileHeader').read()
    flags = struct.unpack_from('<I', header, 36)[0]
    if flags & 0x02:
        raise ValueError('Encrypted HWP files are not supported')
    is_compressed = bool(flags & 0x01)

    # Read body sections
    sections = []
    for entry in ole.listdir():
        path = '/'.join(entry)
        if path.startswith('BodyText/Section'):
            data = ole.openstream(path).read()
            if is_compressed:
                data = zlib.decompress(data, -15)
            sections.append(data)

    # Extract images from BinData
    images = {}
    for entry in ole.listdir():
        path = '/'.join(entry)
        if path.startswith('BinData/'):
            img_data = ole.openstream(path).read()
            try:
                img_data = zlib.decompress(img_data, -15)
            except zlib.error:
                pass  # Not compressed
            images[path] = img_data

    ole.close()
    return sections, images

# Inline extended control chars: each occupies 8 UTF-16 code units (16 bytes).
# After reading the 2-byte char code, skip 14 more bytes.
EXTENDED_CTRL_CHARS = frozenset({
    1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
})

def extract_para_text(data):
    """Extract UTF-16 LE text from HWPTAG_PARA_TEXT record data."""
    text = ''
    i = 0
    while i < len(data) - 1:
        ch = struct.unpack_from('<H', data, i)[0]
        i += 2
        if ch == 0x000D:
            break
        elif ch == 0x0009:
            text += '\t'
        elif ch == 0x000A:
            text += '\n'
        elif ch in EXTENDED_CTRL_CHARS:
            i += 14  # Skip 14 bytes of inline control data
        elif ch < 0x0020:
            continue
        else:
            text += chr(ch)
    return text

def parse_records(data):
    """Parse binary records and extract text from HWPTAG_PARA_TEXT (tag_id=67)."""
    texts = []
    offset = 0
    while offset < len(data) - 4:
        header = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        tag_id = header & 0x3FF
        size = (header >> 20) & 0xFFF
        if size == 0xFFF:
            if offset + 4 > len(data):
                break
            size = struct.unpack_from('<I', data, offset)[0]
            offset += 4
        if offset + size > len(data):
            break
        record_data = data[offset:offset + size]
        offset += size
        if tag_id == 67 and size > 0:
            text = extract_para_text(record_data)
            if text.strip():
                texts.append(text)
    return texts
```

### Python — Read HWPX

```python
import zipfile
import xml.etree.ElementTree as ET

def read_hwpx(filepath):
    with zipfile.ZipFile(filepath, 'r') as z:
        # List section files
        section_files = sorted([
            f for f in z.namelist()
            if f.startswith('Contents/section') and f.endswith('.xml')
        ])

        text_content = []
        for sf in section_files:
            xml_data = z.read(sf).decode('utf-8')
            root = ET.fromstring(xml_data)
            # Extract text from hp:t elements
            ns = {'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph'}
            for t in root.iter('{http://www.hancom.co.kr/hwpml/2011/paragraph}t'):
                if t.text:
                    text_content.append(t.text)

        # Extract images
        images = {
            f: z.read(f) for f in z.namelist()
            if f.startswith('BinData/') and not f.endswith('/')
        }

        return text_content, images
```

## HWP Binary Record Format

HWP binary files store content as sequential records:

```
Record Header (4 bytes):
  - Tag ID:  bits 0-9   (10 bits) — identifies record type
  - Level:   bits 10-19 (10 bits) — nesting depth
  - Size:    bits 20-31 (12 bits) — data size (if 0xFFF, next 4 bytes = actual size)
```

### Key Record Tag IDs

| Constant | Tag ID | Description |
|----------|--------|-------------|
| `HWPTAG_PARA_HEADER` | 66 | Paragraph header |
| `HWPTAG_PARA_TEXT` | 67 | Paragraph text (UTF-16 LE) |
| `HWPTAG_CTRL_HEADER` | 71 | Control header (tables, images) |
| `HWPTAG_LIST_HEADER` | 72 | List header (cell content) |
| `HWPTAG_TABLE` | 77 | Table definition |

### Text Encoding

Paragraph text is encoded as **UTF-16 LE** with special control characters:

| Char Code | Meaning | Type |
|-----------|---------|------|
| `0x0001-0x0008` | Inline extended controls (reserved, section, field start/end, etc.) | **Extended** — 8 UTF-16 code units total (16 bytes). Skip 14 bytes after the 2-byte char code. |
| `0x0009` | Tab | Simple |
| `0x000A` | Line break | Simple |
| `0x000B` | Drawing/table placeholder | **Extended** — skip 14 bytes after char code |
| `0x000C` | Reserved | **Extended** — skip 14 bytes after char code |
| `0x000D` | Paragraph end | Simple (terminates text) |
| `0x000E-0x0017` | Extended controls (hidden comment, header/footer, footnote, auto number, bookmark, etc.) | **Extended** — skip 14 bytes after char code |
| `0x0020` | Space | Simple |
| `0x00A0` | Non-breaking space | Simple |
| `0x00AD` | Soft hyphen | Simple |

> **CRITICAL**: Inline extended control characters (codes 1-8, 11-12, 14-23) each occupy **8 UTF-16 code units** (16 bytes total). After reading the 2-byte character code, you MUST skip the next **14 bytes** of control data. Failing to do so causes binary metadata to leak into extracted text as garbage characters (e.g., `捤獥汤捯`, `汫╨`, `ȃ`).

### Parsing Records (TypeScript)

```typescript
interface HwpRecord {
  tagId: number;
  level: number;
  size: number;
  data: Uint8Array;
}

function parseRecords(buffer: Uint8Array): HwpRecord[] {
  const records: HwpRecord[] = [];
  let offset = 0;
  const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);

  while (offset < buffer.length - 4) {
    const header = view.getUint32(offset, true);
    offset += 4;

    const tagId = header & 0x3FF;
    const level = (header >> 10) & 0x3FF;
    let size = (header >> 20) & 0xFFF;

    if (size === 0xFFF) {
      size = view.getUint32(offset, true);
      offset += 4;
    }

    const data = buffer.slice(offset, offset + size);
    offset += size;

    records.push({ tagId, level, size, data });
  }

  return records;
}
```

### Extracting Text from Records (TypeScript)

```typescript
// Inline extended control chars: each occupies 8 UTF-16 code units (16 bytes).
// After reading the 2-byte char code, skip 14 more bytes.
const EXTENDED_CTRL_CHARS = new Set([
  1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
]);

function extractParaText(data: Uint8Array): string {
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  let text = '';
  let i = 0;

  while (i < data.length - 1) {
    const ch = view.getUint16(i, true);
    i += 2;
    if (ch === 0x000D) break;                    // Paragraph end
    if (ch === 0x0009) { text += '\t'; continue; }
    if (ch === 0x000A) { text += '\n'; continue; }
    if (EXTENDED_CTRL_CHARS.has(ch)) {
      i += 14;  // Skip 14 bytes of inline control data
      continue;
    }
    if (ch < 0x0020) continue;                   // Other control chars
    text += String.fromCharCode(ch);
  }

  return text;
}
```

## Creating HWPX Files

HWPX is a ZIP archive with the following structure:

```
document.hwpx
├── mimetype                    (uncompressed, "application/hwp+zip")
├── META-INF/
│   └── manifest.xml           (file entries)
├── Contents/
│   ├── content.hpf            (package manifest)
│   ├── header.xml             (page layout, fonts, styles)
│   └── section0.xml           (main content)
└── BinData/
    ├── image1.jpg             (embedded images)
    └── image2.png
```

### Generate HWPX (TypeScript)

```typescript
import JSZip from 'jszip';

async function generateHwpx(
  markdown: string,
  options: {
    paperSize?: 'A4' | 'Letter' | 'B5';
    orientation?: 'portrait' | 'landscape';
    margins?: { top: number; bottom: number; left: number; right: number }; // mm
    fontSize?: number;  // pt
    fontFamily?: string;
  } = {}
): Promise<Blob> {
  const {
    paperSize = 'A4',
    orientation = 'portrait',
    margins = { top: 20, bottom: 20, left: 20, right: 20 },
    fontSize = 10,
    fontFamily = '맑은 고딕',
  } = options;

  // Paper sizes in 1/100mm (HWPX unit)
  const paperSizes = {
    A4: { w: 21000, h: 29700 },
    Letter: { w: 21590, h: 27940 },
    B5: { w: 17600, h: 25000 },
  };

  const paper = paperSizes[paperSize];
  const [w, h] = orientation === 'portrait'
    ? [paper.w, paper.h]
    : [paper.h, paper.w];

  // Convert margins mm → 1/100mm
  const m = {
    top: margins.top * 100,
    bottom: margins.bottom * 100,
    left: margins.left * 100,
    right: margins.right * 100,
  };

  const zip = new JSZip();

  // mimetype (must be uncompressed)
  zip.file('mimetype', 'application/hwp+zip', { compression: 'STORE' });

  // META-INF/manifest.xml
  zip.file('META-INF/manifest.xml', `<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <manifest:file-entry manifest:full-path="/" manifest:media-type="application/hwp+zip"/>
  <manifest:file-entry manifest:full-path="Contents/content.hpf" manifest:media-type="application/xml"/>
  <manifest:file-entry manifest:full-path="Contents/header.xml" manifest:media-type="application/xml"/>
  <manifest:file-entry manifest:full-path="Contents/section0.xml" manifest:media-type="application/xml"/>
</manifest:manifest>`);

  // Contents/header.xml (page layout, fonts)
  zip.file('Contents/header.xml', `<?xml version="1.0" encoding="UTF-8"?>
<hh:head xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head">
  <hh:beginNum page="1"/>
  <hh:refList>
    <hh:fontfaces>
      <hh:fontface lang="hangul">
        <hh:font face="${escapeXml(fontFamily)}"/>
      </hh:fontface>
    </hh:fontfaces>
    <hh:charProperties>
      <hh:charPr>
        <hh:sz val="${fontSize * 100}"/>
      </hh:charPr>
    </hh:charProperties>
  </hh:refList>
  <hh:secDef>
    <hh:pageDef width="${w}" height="${h}"
      marginTop="${m.top}" marginBottom="${m.bottom}"
      marginLeft="${m.left}" marginRight="${m.right}"/>
  </hh:secDef>
</hh:head>`);

  // Contents/section0.xml — build paragraphs from markdown
  const paragraphs = markdownToParagraphXml(markdown, fontSize);
  zip.file('Contents/section0.xml', `<?xml version="1.0" encoding="UTF-8"?>
<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section">
${paragraphs}
</hs:sec>`);

  // Contents/content.hpf
  zip.file('Contents/content.hpf', `<?xml version="1.0" encoding="UTF-8"?>
<opf:package xmlns:opf="http://www.idpf.org/2007/opf">
  <opf:manifest>
    <opf:item id="header" href="Contents/header.xml" media-type="application/xml"/>
    <opf:item id="section0" href="Contents/section0.xml" media-type="application/xml"/>
  </opf:manifest>
  <opf:spine>
    <opf:itemref idref="section0"/>
  </opf:spine>
</opf:package>`);

  return await zip.generateAsync({ type: 'blob' });
}

function escapeXml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
```

### Generate HWPX (Python)

```python
import zipfile
import io

def generate_hwpx(text_content: str, output_path: str,
                   paper_size='A4', margins=(20, 20, 20, 20),
                   font_size=10, font_family='맑은 고딕'):
    paper_sizes = {
        'A4': (21000, 29700),
        'Letter': (21590, 27940),
        'B5': (17600, 25000),
    }
    w, h = paper_sizes[paper_size]
    mt, mb, ml, mr = [m * 100 for m in margins]

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        # mimetype must be uncompressed
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/hwp+zip',
                   compress_type=zipfile.ZIP_STORED)

        z.writestr('META-INF/manifest.xml', f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <manifest:file-entry manifest:full-path="/" manifest:media-type="application/hwp+zip"/>
  <manifest:file-entry manifest:full-path="Contents/content.hpf" manifest:media-type="application/xml"/>
  <manifest:file-entry manifest:full-path="Contents/header.xml" manifest:media-type="application/xml"/>
  <manifest:file-entry manifest:full-path="Contents/section0.xml" manifest:media-type="application/xml"/>
</manifest:manifest>''')

        z.writestr('Contents/header.xml', f'''<?xml version="1.0" encoding="UTF-8"?>
<hh:head xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head">
  <hh:secDef>
    <hh:pageDef width="{w}" height="{h}"
      marginTop="{mt}" marginBottom="{mb}"
      marginLeft="{ml}" marginRight="{mr}"/>
  </hh:secDef>
</hh:head>''')

        # Build paragraphs
        paragraphs = []
        for line in text_content.split('\n'):
            escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            paragraphs.append(f'  <hp:p><hp:run><hp:t>{escaped}</hp:t></hp:run></hp:p>')

        section_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section"
         xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph">
{"".join(paragraphs)}
</hs:sec>'''
        z.writestr('Contents/section0.xml', section_xml)

        z.writestr('Contents/content.hpf', '''<?xml version="1.0" encoding="UTF-8"?>
<opf:package xmlns:opf="http://www.idpf.org/2007/opf">
  <opf:manifest>
    <opf:item id="header" href="Contents/header.xml" media-type="application/xml"/>
    <opf:item id="section0" href="Contents/section0.xml" media-type="application/xml"/>
  </opf:manifest>
</opf:package>''')

    with open(output_path, 'wb') as f:
        f.write(buf.getvalue())
```

## Image Extraction

### From HWP Binary (TypeScript)

```typescript
import * as CFB from 'cfb';

function extractImages(cfb: CFB.CFBContainer, maxImages = 30, maxSizeKB = 200) {
  const images: { name: string; data: string; mimeType: string }[] = [];

  for (const entry of cfb.FileIndex) {
    if (!entry.name || !entry.content) continue;
    const path = CFB.utils.cfb_path(entry);
    if (!path.includes('BinData/')) continue;
    if (images.length >= maxImages) break;

    let data = new Uint8Array(entry.content);

    // Try decompression
    try {
      data = pako.inflate(data);
    } catch {
      try { data = pako.inflateRaw(data); } catch { /* not compressed */ }
    }

    if (data.length > maxSizeKB * 1024) continue; // Skip oversized

    // Detect MIME type from magic bytes
    const mimeType = detectMimeType(data);
    if (!mimeType) continue;

    const base64 = btoa(String.fromCharCode(...data));
    images.push({
      name: entry.name,
      data: `data:${mimeType};base64,${base64}`,
      mimeType,
    });
  }

  return images;
}

function detectMimeType(data: Uint8Array): string | null {
  if (data[0] === 0xFF && data[1] === 0xD8) return 'image/jpeg';
  if (data[0] === 0x89 && data[1] === 0x50) return 'image/png';
  if (data[0] === 0x47 && data[1] === 0x49) return 'image/gif';
  if (data[0] === 0x42 && data[1] === 0x4D) return 'image/bmp';
  return null;
}
```

### From HWPX (Python)

```python
import zipfile
import mimetypes

def extract_hwpx_images(filepath, output_dir='./images'):
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(filepath, 'r') as z:
        for name in z.namelist():
            if name.startswith('BinData/') and not name.endswith('/'):
                data = z.read(name)
                filename = os.path.basename(name)
                out_path = os.path.join(output_dir, filename)
                with open(out_path, 'wb') as f:
                    f.write(data)
                print(f'Extracted: {filename} ({len(data)} bytes)')
```

## Table Handling

HWP tables can be simple (GFM markdown) or complex (colspan/rowspan → HTML).

### Detect Complex Tables

```typescript
function isComplexTable(rows: TableRow[]): boolean {
  return rows.some(row =>
    row.cells.some(cell => cell.colspan > 1 || cell.rowspan > 1)
  );
}
```

### Render as Markdown Table

```typescript
function renderMarkdownTable(rows: TableRow[]): string {
  if (rows.length === 0) return '';

  const colCount = rows[0].cells.length;
  const header = '| ' + rows[0].cells.map(c => c.text).join(' | ') + ' |';
  const separator = '| ' + Array(colCount).fill('---').join(' | ') + ' |';
  const body = rows.slice(1).map(row =>
    '| ' + row.cells.map(c => c.text).join(' | ') + ' |'
  ).join('\n');

  return `${header}\n${separator}\n${body}`;
}
```

### Render as HTML Table (for complex layouts)

```typescript
function renderHtmlTable(rows: TableRow[]): string {
  let html = '<table>\n';
  rows.forEach((row, i) => {
    html += '  <tr>\n';
    const tag = i === 0 ? 'th' : 'td';
    row.cells.forEach(cell => {
      const attrs: string[] = [];
      if (cell.colspan > 1) attrs.push(`colspan="${cell.colspan}"`);
      if (cell.rowspan > 1) attrs.push(`rowspan="${cell.rowspan}"`);
      html += `    <${tag}${attrs.length ? ' ' + attrs.join(' ') : ''}>${cell.text}</${tag}>\n`;
    });
    html += '  </tr>\n';
  });
  html += '</table>';
  return html;
}
```

## Web Worker Pattern (Browser)

For non-blocking HWP processing in the browser:

```typescript
// Main thread
const worker = new Worker(
  new URL('./workers/hwp-parser.worker.ts', import.meta.url),
  { type: 'module' }
);

worker.onmessage = (e) => {
  const { type, progress, message, markdown, warnings, error } = e.data;
  switch (type) {
    case 'progress':
      console.log(`${progress}% - ${message}`);
      break;
    case 'complete':
      console.log('Markdown:', markdown);
      if (warnings?.length) console.warn('Warnings:', warnings);
      break;
    case 'error':
      console.error('Error:', error);
      break;
  }
};

const fileBuffer = await file.arrayBuffer();
worker.postMessage({
  type: 'parse',
  data: fileBuffer,
  fileName: file.name,
  options: { extractImages: true, convertTables: true },
});
```

## Command-Line Tools

### hwp5txt (pyhwp)

```bash
# Install
pip install pyhwp

# Extract text
hwp5txt document.hwp

# Convert to HTML
hwp5html document.hwp

# Extract metadata
hwp5odt --metadata document.hwp
```

### LibreOffice (batch conversion)

```bash
# HWP → PDF
libreoffice --headless --convert-to pdf document.hwp

# HWP → DOCX
libreoffice --headless --convert-to docx document.hwp

# Batch convert all HWP files
libreoffice --headless --convert-to pdf *.hwp
```

## Performance & Safety Limits

When processing HWP files, apply these safeguards:

| Limit | Value | Reason |
|-------|-------|--------|
| Max images | 30 | Prevent memory exhaustion |
| Max image size | 200 KB | Skip oversized embedded images |
| Max content size | 2 MB text | Prevent DOM/editor overload |
| Base64 chunk size | 8 KB | Avoid stack overflow in `btoa()` |
| Compression fallback | `inflate` → `inflateRaw` | Handle both zlib and raw deflate |

## Dependencies

### JavaScript/TypeScript

| Package | Purpose |
|---------|---------|
| `cfb` | OLE2/CFB compound file parsing (HWP binary) |
| `pako` | DEFLATE compression/decompression |
| `jszip` | ZIP archive creation/extraction (HWPX) |
| `marked` | Markdown → HTML conversion (for HWPX generation) |
| `file-saver` | Client-side file downloads |

### Python

| Package | Purpose |
|---------|---------|
| `olefile` | OLE2 compound file parsing (HWP binary) |
| `pyhwp` | HWP text/HTML extraction CLI |
| `python-hwp` | HWP/HWPX parsing library |

## Quick Reference

| Task | Best Tool | Language |
|------|-----------|----------|
| Read HWP binary | cfb + pako / olefile | TS / Python |
| Read HWPX | JSZip / zipfile | TS / Python |
| Extract text | Record parser / pyhwp | TS / Python |
| Extract images | BinData/ traversal | Both |
| Extract tables | Record tree → Markdown/HTML | TS |
| Create HWPX | JSZip / zipfile | Both |
| Batch convert | LibreOffice headless | CLI |
| Non-blocking (browser) | Web Worker | TS |

## Next Steps

- For MDView-specific implementation details (React hooks, progress UI, worker communication protocol), see REFERENCE.md
- For table/image pipeline patterns, see the `table-image-pipeline` skill
- For large document performance optimization, see the `large-doc-perf` skill
