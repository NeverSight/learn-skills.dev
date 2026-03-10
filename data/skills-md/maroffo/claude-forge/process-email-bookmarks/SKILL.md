---
name: process-email-bookmarks
description: "Process bookmarks from Gmail. Use when user mentions email bookmarks, Gmail bookmarks, or wants to process saved links from email. Not for web clippings (use process-clippings) or newsletters (use newsletter-digest)."
tools: Bash, Read, WebFetch
---

# ABOUTME: Process bookmarks from Gmail into Second Brain via WebFetch and Obsidian
# ABOUTME: Extracts URLs from bookmark-labeled emails, fetches content, categorizes and integrates

# Process Email Bookmarks Skill

You process bookmarks sent via email (Gmail label "📑 Bookmarks") and integrate them into the Second Brain.

**Gmail:** See `../_GMAIL.md` | **Obsidian CLI:** See `../_OBSIDIAN.md` | **Integration:** See `../_SECOND_BRAIN.md`
**Label**: 📑 Bookmarks (ID: Label_2765838113845362546)

## Processing Workflow

### Step 1: Find Unread Bookmark Emails

```bash
gog gmail search "label:📑 Bookmarks is:unread" --account=maroffo@gmail.com --json
```

### Step 2: For Each Email Thread

1. **Get full thread content**:
```bash
gog gmail thread get <threadId> --account=maroffo@gmail.com --json
```

2. **Extract bookmark info**:
   - URL (from email body or links)
   - Title (from subject or link text)
   - Description (from email body)
   - Any notes added by user

3. **Categorize** per `../_SECOND_BRAIN.md` routing table
4. **Decide**: Actionable -> Fetch via WebFetch, extract, add to Second Brain | Reference -> Bookmarks
5. **Integrate** via Obsidian CLI:
```bash
# Actionable content -> Second Brain
obsidian append file="Second Brain - <Topic>" content="<extracted>"
# Reference only -> Bookmarks
obsidian create path="Bookmarks/<title>.md" content="- [Title](url) - Brief description" silent
```
6. **Update Timeline**:
```bash
obsidian append file="Second Brain - Timeline" content="- **YYYY-MM-DD** | [Topic] | Source: Email bookmark | -> Second Brain - <File>.md"
```
7. **Mark email as read** (see `../_GMAIL.md` for command)

## Output Format

After processing each bookmark:
```
✓ Processed: [Title]
  → Source: Email (thread: <threadId>)
  → Added to: Second Brain - [File].md#[Section]
  → Type: [Actionable/Reference]
  → Email marked as read
```

## Example

**Input email**: Subject "Interesting Go library for CLI" with link to charm.sh

**Processing**:
1. Search unread bookmarks
2. Get thread content
3. Extract URL: https://charm.sh
4. Fetch page content
5. Categorize: Development (Go, CLI)
6. Extract: Charm - Go libraries for CLI apps (Bubble Tea, Lip Gloss, etc.)
7. Add to Second Brain - Development.md
8. Log to Timeline
9. Mark email read

## Rules

See `../_SECOND_BRAIN.md` for shared rules. Additional:
- **Always fetch full content** - don't rely on email snippet alone
- **Mark as read** - only after successful integration
