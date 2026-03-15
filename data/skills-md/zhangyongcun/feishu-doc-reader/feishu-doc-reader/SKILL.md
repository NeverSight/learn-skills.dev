---
name: feishu-doc-reader
description: Read and extract content from Feishu (飞书) and Lark documents. Supports Lark International (open.larksuite.com), wiki URLs, and Markdown export.
metadata: {"moltbot":{"emoji":"📄","requires":{"bins":["python3","curl"]}}}
---

# Feishu/Lark Document Reader

Read and extract content from Feishu (飞书) and Lark documents using the official Open API. Supports both Feishu China (`open.feishu.cn`) and Lark International (`open.larksuite.com`).

## Configuration

### Set Up Credentials

1. Create `./reference/feishu_config.json` from the sample:

```json
{
  "app_id": "your_feishu_app_id",
  "app_secret": "your_feishu_app_secret",
  "api_base": "https://open.larksuite.com"
}
```

Set `api_base` to:
- `https://open.feishu.cn` — Feishu China
- `https://open.larksuite.com` — Lark International

2. Secure the file:
```bash
chmod 600 ./reference/feishu_config.json
```

Alternatively, use environment variables: `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_API_BASE`.

## Usage

### Read Documents

The main script accepts wiki URLs, wiki tokens, or document tokens:

```bash
# Wiki URL (auto-extracts token and resolves to document)
python scripts/read_feishu_doc.py "https://tenant.larksuite.com/wiki/XYZ123"

# Wiki token (auto-resolves)
python scripts/read_feishu_doc.py "XYZ123"

# Document token (direct)
python scripts/read_feishu_doc.py "docx_AbCdEfGh"

# Simplified Markdown output
python scripts/read_feishu_doc.py "docx_AbCdEfGh" --format simple

# Read a spreadsheet
python scripts/read_feishu_doc.py "sheet_token" --type sheet
```

### Get Raw Document Blocks

```bash
python scripts/get_feishu_doc_blocks.py "docx_AbCdEfGh"
```

### Shell Wrappers

```bash
./scripts/read_doc.sh "docx_token"
./scripts/get_blocks.sh "docx_token"
```

### Test Authentication

```bash
python scripts/test_auth.py "app_id" "app_secret" "https://open.larksuite.com"
```

## Supported Document Types

- **Docx** (new docs): Full Markdown extraction with tables, headings, code, lists
- **Doc** (legacy): Basic metadata and content
- **Sheet**: Spreadsheet data extraction
- **Wiki**: Auto-resolved to underlying document type via wiki API

## API Permissions Required

- `docx:document:readonly` — Read document content
- `wiki:wiki:readonly` — Read wiki pages (for wiki URL/token support)
- `sheets:spreadsheet:readonly` — Read spreadsheets (optional)

## Error Handling

- **401**: Check App ID / App Secret
- **403**: Grant API permissions; ensure document is shared with app
- **404**: Verify document token
- **Wrong region**: Use `open.larksuite.com` for Lark International

## Security

- Never commit `reference/feishu_config.json` (listed in `.gitignore`)
- Use `chmod 600` for credential files
- Access tokens are cached in memory only
