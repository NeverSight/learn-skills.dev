---
name: feishu-docs
description: Create and manage Feishu cloud documents with user authorization. Use when creating new documents, writing content, editing existing documents, or managing document workflows. Creates documents in your personal folder with full editing permissions. Supports batch content insertion, formatting, and automatic token refresh.
---

# Feishu Docs

Create and manage Feishu (飞书) cloud documents with automatic user authorization. Documents are created in your personal folder with full editing permissions.

## Quick Start

### Create a Document

```bash
bash scripts/create_doc.sh "Document Title"
```

Returns document ID and link. Document is created in your folder.

### Write Content to Document

```bash
bash scripts/write_content.sh <doc_id> "path/to/content.json"
```

Content file should be JSON array of blocks. See [references/block-format.md](references/block-format.md).

### Edit Existing Document

```bash
bash scripts/append_content.sh <doc_id> "path/to/content.json"
```

Appends content to an existing document without replacing.

### Read Document Content

```bash
bash scripts/read_doc.sh <doc_id>
```

Extracts and displays document text content.

### Full Workflow Example

```bash
# 1. Create document and capture ID
DOC_ID=$(bash scripts/create_doc.sh "My Tutorial")

# 2. Prepare content (JSON array of blocks)
cat > content.json << 'EOF'
[
  {
    "block_type": 2,
    "text": {
      "style": {"heading_level": 1},
      "elements": [
        {
          "text_run": {
            "content": "Tutorial Title",
            "text_element_style": {"bold": true}
          }
        }
      ]
    }
  },
  {
    "block_type": 2,
    "text": {
      "style": {},
      "elements": [
        {
          "text_run": {
            "content": "Introduction paragraph here."
          }
        }
      ]
    }
  },
  {
    "block_type": 7,
    "divider": {}
  },
  {
    "block_type": 2,
    "text": {
      "style": {},
      "elements": [
        {
          "text_run": {
            "content": "✓ Step 1: Create the foundation"
          }
        }
      ]
    }
  },
  {
    "block_type": 2,
    "text": {
      "style": {},
      "elements": [
        {
          "text_run": {
            "content": "✓ Step 2: Add your content"
          }
        }
      ]
    }
  }
]
EOF

# 3. Write to document
bash scripts/write_content.sh "$DOC_ID" content.json
```

## Setup

### Prerequisites

- User must authorize with Feishu OAuth (one-time)
- Credentials stored at `~/.feishu-credentials.json`
- Required permissions: `docs:doc offline_access`

### Verify Setup

```bash
bash scripts/verify_setup.sh
```

### Get Authorization

If you don't have the required permissions, you need to authorize with `docs:doc` scope. Contact your Clawdbot admin for the authorization link.

## Scripts

| Script | Purpose |
|--------|---------|
| `create_doc.sh` | Create new document in your folder |
| `write_content.sh` | Write content blocks to document |
| `append_content.sh` | Append content to existing document |
| `read_doc.sh` | Read and display document content |
| `verify_setup.sh` | Check credentials and permissions |

## Important Notes

### Document Ownership

**⭐ User Mode (Preferred)**

- Documents are created in **your personal folder** with user authorization
- You own the documents and can edit them directly in Feishu UI
- Automatic token refresh keeps documents accessible long-term
- Your identity: `ou_1f553aa193ea382ef8239c16dee55fed`
- **优先级**: 所有文档操作都应该使用用户权限 (user_access_token)，而不是应用权限

**Authorization Note**
- User token requires OAuth authorization (one-time setup)
- Token automatically refreshes via `refresh_token` mechanism
- If token expires, refresh happens automatically when needed

### Supported Block Types

Only the following block type is fully supported and tested via API:

- **Type 2**: Text blocks (paragraphs, headings with formatting) ✅

For other block types, use creative text solutions:
- Lists: Use text blocks with "✓", "-", or "1." prefixes
- Dividers: Use separator lines made of text characters
- Other types: Not currently supported via API

See [references/block-format.md](references/block-format.md) for workarounds and examples.

See [references/block-format.md](references/block-format.md) for complete block reference and workarounds.

### Best Practices

1. **Batch inserts**: Use the `children` array to insert multiple blocks at once (one API call vs N calls)
2. **Filter empty lines**: Remove empty content before inserting to keep documents clean
3. **Use formatting sparingly**: Complex formatting may not render identically across platforms
4. **Test with small documents**: Verify your block structure on a test document first

## Troubleshooting

### "Document not found" after creation

The API likely succeeded. The document exists in app cloud space but isn't visible in your Feishu UI. This is expected behavior—see **Document Ownership** section above.

### "Invalid block structure" errors

Ensure your JSON blocks match the required format:
- `block_type` field is required (integer)
- Text blocks need `text` object with `elements` array
- Each text element needs proper `text_run` structure

See [references/block-format.md](references/block-format.md) for correct format.

### API token errors

Run `verify_setup.sh` to check:
- Credentials file exists and has correct format
- Network access to Feishu API
- Credentials are valid

## References

- [Feishu API Documentation](https://open.feishu.cn/document/server-docs/docs/docs-overview)
- [Block Format Reference](references/block-format.md) - Complete block type definitions and examples
- [API Endpoints](references/api-reference.md) - Feishu REST API endpoints used by this skill
