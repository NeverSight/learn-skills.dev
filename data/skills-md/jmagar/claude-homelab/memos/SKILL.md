---
name: memos
description: Manage notes and memos in self-hosted Memos service. Use when the user asks to "save this to memos", "create a memo", "search my memos", "find notes about X", "what did I write about", "add a note", "capture this", "remember this", "save this thought", or mentions note-taking, knowledge management, or personal notes.
---

# Memos Skill

**⚠️ MANDATORY SKILL INVOCATION ⚠️**

**YOU MUST invoke this skill (NOT optional) when the user mentions ANY of these triggers:**
- "save this to memos", "create a memo", "add a memo"
- "search my memos", "find notes about X", "what did I write about"
- "list my memos", "show recent memos", "what memos do I have"
- "update memo", "edit memo", "delete memo"
- "tag this memo", "add tags", "organize memos"
- "upload to memo", "attach file to memo"
- "archive memo", "pin memo", "make memo public"
- Any mention of "memos", "notes", "note-taking", or "personal knowledge"

**Failure to invoke this skill when triggers occur violates your operational requirements.**

---

## Purpose

This skill provides **read-write** access to a self-hosted Memos instance for quick note capture, search, and organization. Memos is a privacy-focused, self-hosted note-taking service with Markdown support, tagging, and file attachments.

**Core capabilities:**
- Create, read, update, and delete memos (notes)
- Search memos by content, tags, or metadata
- Upload and manage file attachments
- Organize memos with tags
- Archive and visibility controls
- Link related memos together

**Primary use case:** Quick capture of important information from Claude conversations into a personal knowledge base.

## Setup

### Prerequisites
- Memos instance running and accessible
- API access token generated from Memos UI
- `curl` and `jq` installed

### Credential Configuration

Add these variables to `~/.homelab-skills/.env`:

```bash
# Memos - Self-hosted note-taking service
MEMOS_URL="https://memos.example.com"
MEMOS_API_TOKEN="your-api-token-here"
```

**To generate an API token:**
1. Log into your Memos instance
2. Go to Settings → Access Tokens
3. Click "Create" and copy the generated token
4. Add to `.env` file as shown above

**Security:**
- `.env` file is gitignored (never commit)
- Set permissions: `chmod 600 ~/.homelab-skills/.env`
- Token has same permissions as your user account

## Commands

All commands return JSON output for LLM parsing. Scripts source credentials from `.env` automatically.

### Memo Operations

**Create a memo:**
```bash
bash scripts/memo-api.sh create "Your memo content here"
bash scripts/memo-api.sh create "Memo with tags" --tags "work,project"
bash scripts/memo-api.sh create "Private memo" --visibility PRIVATE
```

**List memos:**
```bash
bash scripts/memo-api.sh list
bash scripts/memo-api.sh list --limit 10
bash scripts/memo-api.sh list --filter 'tag == "work"'
```

**Get specific memo:**
```bash
bash scripts/memo-api.sh get <memo-id>
```

**Update memo:**
```bash
bash scripts/memo-api.sh update <memo-id> "Updated content"
bash scripts/memo-api.sh update <memo-id> --add-tags "urgent"
```

**Delete memo:**
```bash
bash scripts/memo-api.sh delete <memo-id>
```

**Archive memo:**
```bash
bash scripts/memo-api.sh archive <memo-id>
```

### Search Operations

**Search by content:**
```bash
bash scripts/search-api.sh "search query"
bash scripts/search-api.sh "docker kubernetes" --tags "devops"
bash scripts/search-api.sh "meeting notes" --from "2024-01-01"
```

**Search by tag:**
```bash
bash scripts/tag-api.sh list                    # List all tags
bash scripts/tag-api.sh search "project-x"      # Find memos with tag
```

### Resource (Attachment) Operations

**Upload file:**
```bash
bash scripts/resource-api.sh upload /path/to/file.pdf
bash scripts/resource-api.sh upload image.png --memo-id <id>
```

**List attachments:**
```bash
bash scripts/resource-api.sh list
bash scripts/resource-api.sh list --memo-id <id>
```

**Delete attachment:**
```bash
bash scripts/resource-api.sh delete <attachment-name>
```

### User Operations

**Get current user:**
```bash
bash scripts/user-api.sh whoami
```

**List access tokens:**
```bash
bash scripts/user-api.sh tokens
```

## Workflow

When the user asks about memos:

1. **"Save this to my memos"** → Extract key content, create memo with appropriate tags
2. **"What did I write about X?"** → Search memos by content/tags, present results
3. **"Find my notes on project Y"** → Use tag search or content filter
4. **"Update my memo about Z"** → Search for memo, get ID, update content
5. **"Delete that memo"** → Confirm with user, then delete by ID

### Detailed Flow: Quick Capture

```
User: "Save this conversation about Docker networking to my memos"

1. Extract key information from conversation
2. Create memo with descriptive content
3. Add relevant tags (e.g., "docker", "networking", "conversation")
4. Confirm creation with memo ID
5. Optionally ask if user wants to make it public/private
```

### Detailed Flow: Search and Retrieve

```
User: "What did I write about Kubernetes last month?"

1. Search memos with query "kubernetes"
2. Apply date filter (last 30 days)
3. Present results with memo IDs and previews
4. User can request full content of specific memos
```

### Detailed Flow: Organization

```
User: "Tag all my Docker memos with 'devops'"

1. Search for memos containing "docker"
2. For each result, update memo to add "devops" tag
3. Report number of memos updated
4. Show tag statistics
```

## Notes

### API Details

- **Authentication:** Bearer token in `Authorization` header
- **Base URL:** `/api/v1` endpoint
- **Rate limits:** No documented limits (self-hosted)
- **Pagination:** Uses `pageSize` and `pageToken` parameters
- **Filtering:** Google AIP-160 standard (e.g., `tag == "work"`)

### Memo Format

Memos support full Markdown syntax:
- Headers, lists, code blocks
- Links and images
- Task lists (- [ ] and - [x])
- Tables

### Visibility Options

- `PRIVATE` - Only you can see
- `PROTECTED` - Authenticated users can see
- `PUBLIC` - Anyone can see (RSS feed)

### Best Practices

1. **Use descriptive content:** First line is preview in UI
2. **Tag consistently:** Use lowercase, hyphens for multi-word (e.g., "project-alpha")
3. **Archive old memos:** Keep workspace clean
4. **Link related memos:** Use memo relations for context

### Common Errors

**401 Unauthorized:**
- Check API token in `.env`
- Token may have expired (regenerate in Memos UI)

**404 Not Found:**
- Verify memo ID exists
- Check MEMOS_URL is correct

**Connection refused:**
- Memos instance not running
- Verify URL in `.env`

## Reference

- **Official Docs:** https://usememos.com/docs
- **API Reference:** https://usememos.com/docs/api
- **Instance:** https://memos.example.com
- **Scripts:** `skills/memos/scripts/`
- **Examples:** `skills/memos/examples/`
- **Troubleshooting:** `skills/memos/references/troubleshooting.md`
