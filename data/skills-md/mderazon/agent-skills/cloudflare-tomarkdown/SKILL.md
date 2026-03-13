---
name: cloudflare-tomarkdown
description: Convert URLs, images, PDFs, and documents to clean Markdown using Cloudflare APIs. Scraping tool with image AI summarization and JS-rendering fallback.
references:
  - cloudflare@workers-ai
  - cloudflare@browser-rendering
---

# Cloudflare Markdown Conversion

Use this skill to convert URLs or local files (PDFs, Images, HTML, CSV, Office docs) into clean, structured Markdown for text analysis, RAG, and LLMs.

## Features & Supported Formats

- **Scraping URLs**: Extracts HTML, resolves relative links, handles JSON-LD, extracts title/description.
- **Images**: Automatically runs object-detection and uses an LLM (`gemma-3-12b-it`) to generate image descriptions. Converts SVG to raster.
- **PDFs**: Parses internal `StructTree` tagging for high-fidelity semantic Markdown extraction.
- **Office Docs**: Supports `.docx`, `.xlsx`, `.csv`, `.ods`, `.odt`, and more.

## Usage

## Setup & Authentication

This skill requires `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN`.

**Automatic Setup:** For convenience, the script automatically looks for a `.env` file in the current directory or its parents. If you have a `.env` file in your project root, it will work out of the box.

**Manual Setup:** Alternatively, you can export them in your shell or pass them as parameters (`--account` and `--token`).

**Instruction for the Agent:** If the skill fails due to missing environment variables, check if a `.env` file exists in the workspace root.

### Scraping a URL

```bash
# Basic usage (defaults to 'auto' method, trying AI parsing first, then browser rendering)
node scripts/render.js --url "https://example.com"
```

### Scraping with Options (CSS Selectors, etc.)

Cloudflare allows filtering elements using `cssSelector` or providing a `hostname`.

```bash
# Only extract the main content container
node scripts/render.js --url "https://developer.cloudflare.com" \
  --options '{"html": {"cssSelector": "main.content"}}'
```

### Converting a Local File (PDFs, Images, Office Docs)

```bash
node scripts/render.js --file "report.pdf"
```

### Converting Images with Language Options

Image descriptions are generated via AI. You can specify a desired output language for the description (`en`, `it`, `de`, `es`, `fr`, `pt`).

```bash
node scripts/render.js --file "cat.jpeg" \
  --options '{"image": {"descriptionLanguage": "es"}}'
```

### Advanced Options for JS-Heavy Sites

If a site requires complex JavaScript rendering or redirects, use the browser method with specific wait conditions.

```bash
# Wait for network to be idle before extracting content
node scripts/render.js --url "https://complex-site.com" --wait "networkidle2"

# Wait for a specific element to appear (e.g. price or main content)
node scripts/render.js --url "https://shop.com/prod" --selector ".product-price"

# Increase timeout for slow pages (in milliseconds)
node scripts/render.js --url "https://slow-site.com" --timeout 60000
```

Valid `--wait` options are: `load`, `domcontentloaded` (default), `networkidle0`, and `networkidle2`.

## How It Works Intelligently

The `--method auto` capability tests two separate rendering paths:

1. **Workers AI `tomarkdown` (Primary)**: Ideal for documents, standard web pages, extracting JSON-LD structured data, and resolving standard HTML features. Uses multipart form data.
2. **Browser Rendering API (Fallback)**: If the page uses complex JavaScript (e.g. Single Page Apps) and the AI path cannot see the content, the Browser Rendering engine opens a headless real browser for accurate conversion.

## Calling the REST API Directly (Advanced)

If you'd prefer not to use `scripts/render.js`, here is the curl equivalent for a local file using the `tomarkdown` REST API:

```bash
curl https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/ai/tomarkdown \
  -X POST \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -F "files=@document.pdf" \
  -F 'conversionOptions={"pdf":{"metadata":false}}'
```

**Note:** For URLs, you should use `curl` to fetch the source to a local file first before uploading it as `files=@<temp.html>`. The `tomarkdown` REST API does not directly ingest a `--data url="https..."`.
