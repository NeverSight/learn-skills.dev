---
name: coda
description: Export Coda document pages to local Markdown files. Use when a user wants to export, download, or extract content from Coda docs, list pages in a Coda document, or convert Coda page trees into Markdown. Triggers on tasks involving Coda API, Coda docs, or Coda page export.
---

# Coda Export

Export Coda pages and their descendants into local Markdown files using `scripts/coda_export.py`.

## Prerequisites

- Python 3.9+
- A Coda API token and doc ID

## Getting Coda API Credentials

### API Token

1. Go to [Coda Account Settings](https://coda.io/account)
2. Scroll to **API Settings**
3. Click **Generate API token**
4. Give it a name and copy the token

### Doc ID

The doc ID is in the URL of your Coda document:

```
https://coda.io/d/Your-Doc-Name_d<DOC_ID>
```

For example, in `https://coda.io/d/My-Notes_dAbCdEfGhI`, the doc ID is `AbCdEfGhI`.

### Setting Environment Variables

```bash
export CODA_DOC_ID="your-doc-id"
export CODA_API_TOKEN="your-api-token"
```

If your project uses different env var names (e.g. `CODA_CONTRACT_DOC_ID`), use the `--doc-id-env` / `--token-env` flags instead of renaming your vars:

```bash
python scripts/coda_export.py --doc-id-env CODA_CONTRACT_DOC_ID --token-env CODA_TOKEN_CONTRACT_PAGE export-doc
```

Or pass credentials directly:

```bash
python scripts/coda_export.py --doc-id <DOC_ID> --token <TOKEN> export-doc
```

## Quick Start

```bash
# 1. Check your credentials work
python scripts/coda_export.py validate-auth

# 2. Export the entire doc
python scripts/coda_export.py export-doc

# 3. With custom env var names
python scripts/coda_export.py --doc-id-env MY_DOC_ID --token-env MY_TOKEN export-doc
```

## Commands

### validate-auth

Check if your token and doc ID are valid before exporting.

```bash
python scripts/coda_export.py validate-auth
```

Prints token status (valid/invalid) and doc accessibility (accessible/forbidden/not found). Exits 0 on success, 1 on failure.

### list-pages

```bash
python scripts/coda_export.py list-pages
```

Filter by name:

```bash
python scripts/coda_export.py list-pages --contains <search-term>
```

### export-doc

Export all pages in a document in one run.

```bash
python scripts/coda_export.py export-doc
```

With custom output directory:

```bash
python scripts/coda_export.py export-doc --out-dir <DIR>
```

### export-subtree

Export a single page and its descendants.

```bash
python scripts/coda_export.py export-subtree --root-page-id <PAGE_ID>
```

With custom output directory:

```bash
python scripts/coda_export.py export-subtree --root-page-id <PAGE_ID> --out-dir <DIR>
```

### Overwrite behavior

By default, existing files are **skipped** with a notice. A summary at the end shows how many were skipped.

To overwrite existing files:

```bash
python scripts/coda_export.py export-doc --overwrite
python scripts/coda_export.py export-subtree --root-page-id <PAGE_ID> --overwrite
```

## Output

- One `.md` file per page
- Nested directories mirror the Coda page hierarchy
- Filenames include page IDs to avoid collisions
- Final summary: pages discovered, files written, files skipped

## Notes

- The script retries transient API/network failures automatically (configurable via `--retries`, default 6).
- HTTP timeout is configurable via `--timeout` (default 90s).
- Keep tokens out of git commits.
