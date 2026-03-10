---
name: newsletter-digest
description: "Process newsletters into Second Brain digest. Use when user wants to process newsletters, create digest, or catch up on subscriptions. Not for web clippings (use process-clippings) or email bookmarks (use process-email-bookmarks)."
tools: Bash, Read, WebFetch
---

# ABOUTME: Process unread newsletters into Second Brain entries via Gmail and Obsidian
# ABOUTME: Batch extraction of actionable content from Substack, Beehiiv, and other platforms

# Newsletter Digest Skill

Process unread newsletters, extract actionable content for Second Brain, archive processed emails.

**Gmail:** See `../_GMAIL.md` | **Obsidian CLI:** See `../_OBSIDIAN.md` | **Integration:** See `../_SECOND_BRAIN.md`

## Newsletter Sources

**All newsletters are processed** - categorize by content, not by sender.

### Common Platforms

```bash
# Search for unread newsletters from common platforms
gog gmail search "is:unread (from:substack.com OR from:beehiiv.com OR from:convertkit.com OR from:mailchimp.com OR from:buttondown.email)" --account=maroffo@gmail.com --json --max=20
```

### Known Newsletter Labels

| Label | Description |
|-------|-------------|
| `📰Newsletter/🔴 Substack` | Substack newsletters |
| `📰Newsletter` | General newsletters |
| `👨🏻‍💻work-related` | Work-related content (higher priority) |

### Key Newsletters by Category

| Newsletter | Author | Category |
|------------|--------|----------|
| ByteByteGo | Alex Xu | AI/Development |
| Turing Post | - | AI/Open Source |
| Artificial Ignorance | Charlie Guo | AI/Management |
| The Beautiful Mess | John Cutler | Engineering Management |
| Tidy First? | Kent Beck | Engineering/Design |
| Javarevisited | - | Development |
| [mini]marketing | Gianluca Diegoli | Marketing |
| Paul Krugman | Paul Krugman | Politics/Economics |
| Appunti | Stefano Feltri | Politics (IT) |
| 270 by Youtrend | Youtrend | Politics (IT) |
| Il Mattinale Europeo | David Carretta | EU Politics |
| Il Post | - | News (IT) |
| Semafor | - | News (International) |
| Roberta Villa | Roberta Villa | Health/Science |
| Ellissi | - | Media/Culture |
| Sillabe | Elena Tosato | Literature |

## Processing Workflow

### Step 1: Find Unread Newsletters

```bash
gog gmail search "is:unread (from:substack.com OR from:beehiiv.com OR from:convertkit.com)" --account=maroffo@gmail.com --json --max=20
```

### Step 2: For Each Newsletter

Use the extraction script to get clean text content:

```bash
# Full content with metadata
gog gmail thread get <threadId> --account=maroffo@gmail.com --json \
  | python3 ~/.claude/skills/newsletter-digest/extract_email.py --meta

# Truncated (for quick triage)
gog gmail thread get <threadId> --account=maroffo@gmail.com --json \
  | python3 ~/.claude/skills/newsletter-digest/extract_email.py --meta --max-chars 3000
```

The script (`extract_email.py`) handles multipart MIME, base64 decoding, HTML fallback, and nested parts. No need to write inline Python for email parsing.

3. **Analyze content** - identify:
   - **Tools/libraries** mentioned → Second Brain - Development/AI
   - **Patterns/techniques** → Second Brain appropriate section
   - **News/opinions** → Reference only (skip or brief note)
   - **Tutorials/guides** → Extract key steps

4. **Categorize** per `../_SECOND_BRAIN.md` routing table
5. **Extract & integrate** via Obsidian CLI:
```bash
obsidian append file="Second Brain - <Topic>" content="<extracted>"
```
6. **Update Timeline**:
```bash
obsidian append file="Second Brain - Timeline" content="- **YYYY-MM-DD** | [Topic] | Source: Newsletter | -> Second Brain - <File>.md"
```
7. **Archive email** (see `../_GMAIL.md` for archive command)

## Output Format

After processing batch:

```
## Newsletter Digest - YYYY-MM-DD

### Processed (X newsletters)

1. **[Pragmatic Engineer]** - "Platform Teams Done Right"
   - Extracted: Platform team anti-patterns
   - → Second Brain - Engineering Management.md
   - ✓ Archived

2. **[ByteByteGo]** - "Rate Limiting Deep Dive"
   - Extracted: Token bucket algorithm summary
   - → Second Brain - Development.md
   - ✓ Archived

3. **[The Batch]** - "AI News Weekly"
   - Skipped: News only, no actionable content
   - ✓ Archived

### Summary
- Newsletters processed: X
- Second Brain entries added: Y
- Archived: X
```

## Content Extraction Guidelines

**Include in Second Brain:**
- Tool/library announcements with clear use case
- Architecture patterns with examples
- Techniques you can apply
- Commands/configs worth remembering
- **Important news** from news-focused newsletters (Il Post, Semafor, Appunti, Il Mattinale Europeo):
  - Geopolitical events with lasting impact
  - Policy changes (EU, IT, international)
  - Economic developments (trade, sanctions, markets)
  - Major political events (elections, government changes)
  - → Add to `Second Brain - Politics and Economics.md`

**Skip (archive only):**
- Tech industry news/opinions (funding, hype cycles)
- Funding announcements
- Job postings
- Content you've already captured
- Ephemeral news (daily weather, minor events)

**Ask user if unclear:**
- Mixed content (some actionable, some not)
- Topics outside usual categories

## Rules

See `../_SECOND_BRAIN.md` for shared rules. Additional:
- **Always archive** - processed = archived, no exceptions
- **Batch process** - handle multiple newsletters in one session
