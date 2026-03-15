---
name: paperless-ngx
description: Manage documents in Paperless-ngx document management system. Use when the user asks to "upload document", "search paperless", "find document", "add to paperless", "tag document", "manage correspondents", "organize documents", "archive document", "export document", "delete document", or mentions Paperless-ngx, document management, OCR, or paperless office.
---

# Paperless-ngx Skill

**⚠️ MANDATORY SKILL INVOCATION ⚠️**

**YOU MUST invoke this skill (NOT optional) when the user mentions ANY of these triggers:**
- "upload document", "add document to paperless", "scan to paperless"
- "search paperless", "find document", "search documents"
- "tag document", "add tags", "manage tags in paperless"
- "manage correspondents", "add correspondent", "list correspondents"
- "update document", "edit document metadata", "change document type"
- "archive document", "export document", "download document"
- "delete document", "remove document from paperless"
- "list my documents", "show recent documents", "what documents do I have"
- Any mention of Paperless-ngx, document management, OCR, or paperless office

**Failure to invoke this skill when triggers occur violates your operational requirements.**

---

## Purpose

This skill provides **read-write** access to a self-hosted Paperless-ngx instance for document management with OCR. Paperless-ngx transforms physical documents into a searchable online archive with full-text search, tagging, and metadata management.

**Core capabilities:**
- Upload documents with auto-OCR and metadata extraction
- Search documents by content, tags, correspondent, or date
- Manage tags, correspondents, and document types
- Update document metadata (title, tags, correspondent, dates)
- Archive and export operations
- Delete documents (with confirmation)
- Bulk operations on multiple documents

**Primary use case:** Maintain a searchable digital archive of all documents with powerful organization and retrieval capabilities.

## Setup

### Prerequisites
- Paperless-ngx instance running and accessible
- API token generated from Paperless-ngx UI
- `curl` and `jq` installed

### Credential Configuration

Add these variables to `~/.homelab-skills/.env`:

```bash
# Paperless-ngx - Document management system
PAPERLESS_URL="https://paperless.example.com"
PAPERLESS_API_TOKEN="your-api-token-here"
```

**To generate an API token:**
1. Log into your Paperless-ngx instance
2. Go to Settings → My Profile
3. Click "Create Token" under "API Tokens"
4. Copy the generated token
5. Add to `.env` file as shown above

**Security:**
- `.env` file is gitignored (never commit)
- Set permissions: `chmod 600 ~/.homelab-skills/.env`
- Token has same permissions as your user account

## Commands

All commands return JSON output for LLM parsing. Scripts source credentials from `.env` automatically.

### Document Operations

**Upload a document:**
```bash
bash scripts/paperless-api.sh upload /path/to/document.pdf
bash scripts/paperless-api.sh upload scan.jpg --title "Receipt" --tags "expense,2024"
bash scripts/paperless-api.sh upload contract.pdf --correspondent "Acme Corp" --document-type "Contract"
```

**Search documents:**
```bash
bash scripts/paperless-api.sh search "invoice"
bash scripts/paperless-api.sh search "meeting notes" --limit 10
bash scripts/paperless-api.sh search "2024" --tags "tax"
bash scripts/paperless-api.sh search --correspondent "John Doe"
```

**List documents:**
```bash
bash scripts/paperless-api.sh list
bash scripts/paperless-api.sh list --limit 20
bash scripts/paperless-api.sh list --ordering "-created"
```

**Get document details:**
```bash
bash scripts/paperless-api.sh get <document-id>
```

**Download/export document:**
```bash
bash scripts/paperless-api.sh download <document-id>
bash scripts/paperless-api.sh download <document-id> --output /path/to/save.pdf
```

**Update document:**
```bash
bash scripts/paperless-api.sh update <document-id> --title "New Title"
bash scripts/paperless-api.sh update <document-id> --add-tags "urgent,reviewed"
bash scripts/paperless-api.sh update <document-id> --correspondent "Jane Smith"
bash scripts/paperless-api.sh update <document-id> --document-type "Invoice"
bash scripts/paperless-api.sh update <document-id> --archive-serial-number "2024-001"
```

**Delete document:**
```bash
bash scripts/paperless-api.sh delete <document-id>  # Prompts for confirmation
```

### Tag Management

**List tags:**
```bash
bash scripts/tag-api.sh list
bash scripts/tag-api.sh list --ordering "name"
```

**Create tag:**
```bash
bash scripts/tag-api.sh create "project-alpha"
bash scripts/tag-api.sh create "urgent" --color "#ff0000"
```

**Get tag details:**
```bash
bash scripts/tag-api.sh get <tag-id>
```

**Update tag:**
```bash
bash scripts/tag-api.sh update <tag-id> --name "new-name"
bash scripts/tag-api.sh update <tag-id> --color "#00ff00"
```

**Delete tag:**
```bash
bash scripts/tag-api.sh delete <tag-id>  # Prompts for confirmation
```

### Correspondent Management

**List correspondents:**
```bash
bash scripts/correspondent-api.sh list
```

**Create correspondent:**
```bash
bash scripts/correspondent-api.sh create "Acme Corporation"
```

**Get correspondent details:**
```bash
bash scripts/correspondent-api.sh get <correspondent-id>
```

**Update correspondent:**
```bash
bash scripts/correspondent-api.sh update <correspondent-id> --name "New Name"
```

**Delete correspondent:**
```bash
bash scripts/correspondent-api.sh delete <correspondent-id>  # Prompts for confirmation
```

### Bulk Operations

**Bulk tag documents:**
```bash
bash scripts/bulk-api.sh add-tag <tag-id> --documents "1,2,3"
bash scripts/bulk-api.sh remove-tag <tag-id> --documents "1,2,3"
```

**Bulk set correspondent:**
```bash
bash scripts/bulk-api.sh set-correspondent <correspondent-id> --documents "1,2,3"
```

**Bulk delete documents:**
```bash
bash scripts/bulk-api.sh delete --documents "1,2,3"  # Prompts for confirmation
```

## Workflow

When the user asks about Paperless-ngx:

1. **"Upload this document to Paperless"**
   - Save file locally if needed
   - Use `upload` command with appropriate metadata
   - Optionally add tags, correspondent, document type
   - Paperless will auto-OCR and extract text

2. **"Find my 2024 tax documents"**
   - Use `search "tax" --tags "2024"` or similar query
   - Present results with ID, title, date, tags
   - User can request full details with `get <id>`

3. **"Tag all invoices from Acme Corp as paid"**
   - Search for documents: `search "invoice" --correspondent "Acme Corp"`
   - Create or find "paid" tag
   - Use bulk operation to add tag to results

4. **"Show me documents without tags"**
   - Use `list` with filter parameter
   - Present untagged documents
   - Suggest tagging workflow

5. **"Delete this old document"**
   - Confirm document ID with user
   - Ask for explicit confirmation
   - Use `delete <id>` command

6. **"Add a new supplier as correspondent"**
   - Use `correspondent-api.sh create "Supplier Name"`
   - Return correspondent ID for future document uploads

### Detailed Flow: Document Upload

```
User: "Upload this receipt to Paperless and tag it as expense"

1. Verify file path exists and is readable
2. Upload document with metadata:
   bash scripts/paperless-api.sh upload /path/to/receipt.pdf --tags "expense"
3. Paperless processes document (OCR, thumbnail generation)
4. Return document ID and success confirmation
5. Optionally ask if user wants to set correspondent or document type
```

### Detailed Flow: Search and Organize

```
User: "Find all documents from last month that need review"

1. Calculate date range (last month)
2. Search documents by date range
3. Filter results by tag or keyword "review"
4. Present results with metadata
5. Offer to bulk-tag results or export list
```

### Detailed Flow: Bulk Tagging

```
User: "Tag all invoices from Q1 as archived"

1. Search for invoices in Q1 date range
2. Extract document IDs from results
3. Find or create "archived" tag
4. Use bulk operation to add tag to all documents
5. Report number of documents tagged
```

## Notes

### API Details

- **Authentication:** Token authentication via `Authorization: Token <token>` header
- **Base URL:** `/api/` endpoint
- **API Version:** Version 5 (specify via Accept header)
- **Rate limits:** No documented limits (self-hosted)
- **Pagination:** Uses `page` and `page_size` parameters

### Document Processing

Paperless-ngx automatically processes uploaded documents:
- OCR extraction (if not already text-based PDF)
- Thumbnail generation
- Metadata extraction (date, correspondent guessing)
- Full-text indexing for search

### Search Syntax

Search supports multiple query types:
- **Full-text:** `search "meeting notes"`
- **Tag filter:** `search --tags "work,urgent"`
- **Correspondent:** `search --correspondent "John Doe"`
- **Date range:** `search --created-after "2024-01-01"`
- **Document type:** `search --document-type "Invoice"`

### Tags vs Correspondents

- **Tags:** General-purpose labels (e.g., "urgent", "personal", "2024")
- **Correspondents:** People or organizations (e.g., "Acme Corp", "John Smith")
- **Document Types:** Categories of documents (e.g., "Invoice", "Contract", "Receipt")

All three provide different organizational axes for your documents.

### Destructive Operations

Delete operations require confirmation:
- **Delete document:** Permanently removes document and files
- **Delete tag:** Removes tag from all documents (documents remain)
- **Delete correspondent:** Removes from all documents (documents remain)

Always confirm with user before executing delete operations.

### Best Practices

1. **Tag consistently:** Use lowercase, hyphens for multi-word (e.g., "project-alpha")
2. **Set correspondents:** Makes searching by sender/recipient easier
3. **Use document types:** Categories help with organization and workflows
4. **Archive serial numbers:** Track original paper document storage
5. **Search before upload:** Avoid duplicates

### Common Errors

**401 Unauthorized:**
- Check API token in `.env`
- Token may have expired (regenerate in Paperless UI)
- Verify user permissions

**404 Not Found:**
- Verify document/tag/correspondent ID exists
- Check PAPERLESS_URL is correct

**400 Bad Request:**
- Invalid metadata (e.g., non-existent tag ID)
- Malformed file upload
- Check script output for specific error message

**Connection refused:**
- Paperless-ngx instance not running
- Verify URL in `.env`

## Reference

- **Official Docs:** https://docs.paperless-ngx.com/
- **API Reference:** See `references/api-endpoints.md` for complete API documentation
- **Quick Reference:** See `references/quick-reference.md` for command examples
- **Troubleshooting:** See `references/troubleshooting.md` for common issues
- **Scripts:** `skills/paperless-ngx/scripts/`

---

## 🔧 Agent Tool Usage Requirements

**CRITICAL:** When invoking scripts from this skill via the zsh-tool, **ALWAYS use `pty: true`**.

Without PTY mode, command output will not be visible even though commands execute successfully.

**Correct invocation pattern:**
```typescript
<invoke name="mcp__plugin_zsh-tool_zsh-tool__zsh">
<parameter name="command">./skills/paperless-ngx/scripts/paperless-api.sh [args]</parameter>
<parameter name="pty">true</parameter>
</invoke>
```
