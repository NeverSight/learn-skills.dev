---
name: skill-tools
description: >
  Local Node.js tools for web knowledge gathering and processing: search PDFs and images, stream-download
  and validate files, convert PDFs to structured Markdown, and generate speech locally with Supertone
  Supertonic ONNX Runtime. Use when Codex needs no-API-key search, safe file downloads, PDF text extraction,
  or on-device TTS (with a one-time model download to ./models/supertonic-2/).
---

# skill-tools

Use this skill as a local utility toolkit for search, file acquisition, PDF conversion, and TTS.

## Setup

Install dependencies from the skill directory:

```bash
npm install
```

Import functions in ESM:

```javascript
import {
  searchPDFs,
  searchImages,
  downloadFile,
  convertPdfToMarkdown,
  generateSpeech,
} from './index.js';
```

## Functions

### `searchPDFs(query, limit = 10)`

- Uses Bing HTML search (not DuckDuckGo).
- Returns `Array<{ title, url }>` filtered to `.pdf` URLs.
- Returns `[]` on recoverable failures.
- Includes a short randomized delay to reduce bot blocking.

```javascript
const pdfs = await searchPDFs('machine learning tutorial', 5);
```

### `searchImages(query, limit = 10)`

- Uses `google-img-scrap`.
- Returns `Array<{ title, url }>`.
- Returns `[]` on recoverable failures.

```javascript
const images = await searchImages('space wallpaper hd', 3);
```

### `downloadFile(url, outputDir, expectedType)`

Stream-downloads to disk, validates content type using magic bytes, and fixes file extension.

- `expectedType`: `'pdf'` | `'image'`
- Returns saved file path on success, `null` on failure
- Caller should ensure `outputDir` exists first

```javascript
import fs from 'node:fs/promises';

await fs.mkdir('./downloads', { recursive: true });
const localPath = await downloadFile(pdfs[0].url, './downloads', 'pdf');
```

### `convertPdfToMarkdown(pdfPath, options?)`

Converts PDFs to Markdown using `unpdf` (Mozilla PDF.js) with heuristics for headings, paragraphs, bullets, and URL repair.

Options (defaults shown):

- `detectHeadings = true`
- `joinParagraphs = true`
- `normaliseBullets = true`
- `fixBrokenUrls = true`
- `includeMetadata = false`

Returns Markdown string on success, `null` on failure.

```javascript
const md = await convertPdfToMarkdown('./report.pdf', { includeMetadata: true });
```

### `generateSpeech(text, outputPath, options?)`

Generates a WAV file locally using Supertone Supertonic ONNX models (`onnxruntime-node`).

Automatic download on first use (Supertonic 2):

- ONNX assets to `./models/supertonic-2/onnx/`
- Voice style JSON to `./models/supertonic-2/voice_styles/`

Supported options:

- `voice` (default `'F1'`): `F1`-`F5`, `M1`-`M5`, or a local voice-style JSON path
- `lang` (default `'en'`): `en`, `ko`, `es`, `pt`, `fr`
- `speed` (default `1.0`)
- `steps` (default `20`)
- `useGpu` (default `false`, currently unsupported)
- `modelRoot` (default `./models/supertonic-2`)

Returns output WAV path on success, `null` on failure.

```javascript
await generateSpeech('Hello!', './out.wav', {
  voice: 'M2',
  lang: 'en',
  speed: 1.1,
  steps: 10,
});
```

## End-to-end example

```javascript
import fs from 'node:fs/promises';
import {
  searchPDFs,
  downloadFile,
  convertPdfToMarkdown,
  generateSpeech,
} from './index.js';

await fs.mkdir('./downloads', { recursive: true });

const [first] = await searchPDFs('javascript guide', 3);
const pdfPath = await downloadFile(first.url, './downloads', 'pdf');
const markdown = await convertPdfToMarkdown(pdfPath, { includeMetadata: true });

await fs.writeFile(pdfPath.replace('.pdf', '.md'), markdown);
await generateSpeech(markdown.slice(0, 400), './summary.wav', { voice: 'F1', lang: 'en' });
```

## Testing

Use the fast suite by default:

```bash
npm test
```

Integration suites are explicit and opt-in:

```bash
npm run test:integration:search  # requires RUN_NETWORK_TESTS=1
npm run test:integration:tts     # requires RUN_TTS_INTEGRATION=1
```
