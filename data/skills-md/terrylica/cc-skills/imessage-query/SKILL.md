---
name: imessage-query
description: Query macOS iMessage database (chat.db) via SQLite. Decode NSAttributedString messages, handle tapbacks, search conversations. TRIGGERS - imessage, chat.db, messages database, text messages, iMessage history, NSAttributedString, attributedBody
allowed-tools: Read, Bash, Grep, Glob, Write
---

# iMessage Database Query

Query the macOS iMessage SQLite database (`~/Library/Messages/chat.db`) to retrieve conversation history, decode messages stored in binary format, and build sourced timelines with precise timestamps.

## When to Use

- Retrieving iMessage conversation history for a specific contact
- Building sourced timelines with timestamps from text messages
- Searching for keywords across all conversations
- Debugging messages that appear empty but contain recoverable text
- Extracting message content that iOS stored in binary `attributedBody` format

## Prerequisites

1. **macOS only** — `chat.db` is a macOS-specific database
2. **Full Disk Access** — The terminal running Claude Code must have FDA granted in System Settings > Privacy & Security > Full Disk Access
3. **Read-only** — Never write to `chat.db`. Always use read-only SQLite access.
4. **Optional**: `pip install pytypedstream` — Enables tier 1 decoder (proper typedstream deserialization). Script works without it (falls through to pure-binary tiers 2/3).

## Critical Knowledge - The `text` vs `attributedBody` Problem

**IMPORTANT**: Many iMessage messages have a NULL or empty `text` column but contain valid, recoverable text in the `attributedBody` column. This is NOT because they are voice messages — iOS stores dictated messages, messages with rich formatting, and some regular messages in `attributedBody` as an NSAttributedString binary blob.

### How to detect

```sql
-- Messages with attributedBody but no text (these are NOT necessarily voice messages)
SELECT COUNT(*) as hidden_messages
FROM message m
JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
JOIN chat c ON cmj.chat_id = c.ROWID
WHERE c.chat_identifier = '<CHAT_IDENTIFIER>'
AND (m.text IS NULL OR length(m.text) = 0)
AND m.attributedBody IS NOT NULL
AND length(m.attributedBody) > 100
AND m.associated_message_type = 0
AND m.cache_has_attachments = 0;
```

### How to distinguish message types when `text` is NULL

| `cache_has_attachments` | `attributedBody` length | Likely type                                                                |
| ----------------------- | ----------------------- | -------------------------------------------------------------------------- |
| 0                       | > 100 bytes             | **Dictated/rich text** — recoverable via decode script                     |
| 1                       | any                     | Attachment (image, file, voice memo) — text may be in `attributedBody` too |
| 0                       | < 50 bytes              | Tapback reaction or system message — usually noise                         |

### How to decode

Use the bundled decode script for reliable extraction (v4 — 3-tier decoder + native pitfall protections):

```bash
python3 <skill-path>/scripts/decode_attributed_body.py --chat "<CHAT_IDENTIFIER>" --limit 50
```

The decoder uses a 3-tier strategy:

1. **Tier 1**: `pytypedstream` Unarchiver — proper Apple typedstream deserialization (requires `pip install pytypedstream`)
2. **Tier 2**: Multi-format binary — 0x2B/0x4F/0x49 length-prefix parsing (zero deps, ported from [macos-messages](https://github.com/bettercallsean/macos-messages))
3. **Tier 3**: NSString marker + length-prefix — v2 legacy approach (zero deps, last resort)

Falls through tiers on failure. Works without pytypedstream installed (skips tier 1). See [Cross-Repo Analysis](./references/cross-repo-analysis.md) for decoder comparison.

## Date Formula

iMessage stores dates as **nanoseconds since Apple epoch (2001-01-01 00:00:00 UTC)**.

```sql
datetime(m.date/1000000000 + 978307200, 'unixepoch', 'localtime') as timestamp
```

- `m.date / 1000000000` — Convert nanoseconds to seconds
- `+ 978307200` — Add offset from Unix epoch (1970) to Apple epoch (2001)
- `'unixepoch'` — Tell SQLite this is a Unix timestamp
- `'localtime'` — Convert to local timezone (CRITICAL — omitting this gives UTC)

## Quick Start Queries

### 1. List all conversations

```sql
sqlite3 ~/Library/Messages/chat.db \
  "SELECT c.chat_identifier, c.display_name, COUNT(cmj.message_id) as msg_count
   FROM chat c
   JOIN chat_message_join cmj ON c.ROWID = cmj.chat_id
   GROUP BY c.ROWID
   ORDER BY msg_count DESC
   LIMIT 20"
```

### 2. Get conversation thread (text column only)

```sql
sqlite3 ~/Library/Messages/chat.db \
  "SELECT datetime(m.date/1000000000 + 978307200, 'unixepoch', 'localtime') as ts,
          CASE WHEN m.is_from_me = 1 THEN 'Me' ELSE 'Them' END as sender,
          m.text
   FROM message m
   JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
   JOIN chat c ON cmj.chat_id = c.ROWID
   WHERE c.chat_identifier = '<CHAT_IDENTIFIER>'
   AND length(m.text) > 0
   AND m.associated_message_type = 0
   ORDER BY m.date DESC
   LIMIT 50"
```

### 3. Get ALL messages including attributedBody (use decode script)

```bash
python3 <skill-path>/scripts/decode_attributed_body.py \
  --chat "<CHAT_IDENTIFIER>" \
  --after "2026-01-01" \
  --limit 100
```

## Filtering Noise

### Tapback reactions

Tapback reactions (likes, loves, emphasis, etc.) are stored as separate message rows with `associated_message_type != 0`. Always filter:

```sql
AND m.associated_message_type = 0
```

### Shell escaping in zsh

The `!=` operator can cause issues in zsh. Use positive assertions instead:

```sql
-- BAD (breaks in zsh)
AND m.text != ''

-- GOOD (works everywhere)
AND length(m.text) > 0
```

## Using the Decode Script

The bundled `decode_attributed_body.py` handles all edge cases:

```bash
# Basic usage - get last 50 messages from a contact
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" --limit 50

# Search for keyword
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" --search "meeting"

# Search with surrounding context (3 messages before and after each match)
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" --search "meeting" --context 3

# Date range
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" --after "2026-01-01" --before "2026-02-01"

# Only messages from the other party
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" --sender them

# Only messages from me
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" --sender me

# Export conversation to NDJSON for offline analysis
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" --after "2026-02-01" --export thread.jsonl
```

Output format: `timestamp|sender|text` (pipe-delimited, one message per line)

### Context Search (`--context N`)

When `--search` is combined with `--context N`, the script shows N messages before and after each match:

- Matches are prefixed with `[match]`
- Non-contiguous context groups are separated by `--- context ---`
- Overlapping context windows are deduplicated

### NDJSON Export (`--export`)

Exports messages to a NDJSON (.jsonl) file for offline analysis:

```json
{
  "ts": "2026-02-13 18:30:17",
  "sender": "them",
  "is_from_me": false,
  "text": "Message text here",
  "decoded": true,
  "type": "text",
  "edited": true,
  "service": "SMS",
  "effect": "slam",
  "reply_to": {
    "ts": "2026-02-13 18:00:00",
    "sender": "me",
    "text": "Original message..."
  }
}
```

Fields `edited`, `service`, `effect`, `reply_to` are optional — only present when applicable. The `type` field is always present (`"text"`, `"audio"`, or `"attachment"`).

**Retracted messages are NEVER exported** — they are deterministically excluded (see Native Protections below).

**Export-first workflow** (recommended for multi-query analysis):

```bash
# Step 1: Export once
python3 <skill-path>/scripts/decode_attributed_body.py --chat "+1234567890" \
  --after "2026-02-01" --export thread.jsonl

# Step 2: Analyze many times without re-querying SQLite
grep -i "keyword" thread.jsonl
jq 'select(.text | test("reference"; "i"))' thread.jsonl
jq 'select(.sender == "them")' thread.jsonl
```

## Native Protections (v4)

The decode script natively handles these pitfalls — no manual SQL workarounds needed:

| Protection                     | Column Used                               | Behavior                                                                |
| ------------------------------ | ----------------------------------------- | ----------------------------------------------------------------------- |
| Retracted messages (Undo Send) | `date_retracted`, `date_edited`           | **Excluded** from output — content wiped by iOS, not admissible         |
| Edited messages                | `date_edited`                             | **Flagged** with `[edited]` / `"edited": true`                          |
| Audio/voice messages           | `is_audio_message`                        | **Identified** as `[audio message]` — not misclassified as empty        |
| Inline quotes (swipe-to-reply) | `thread_originator_guid`                  | **Resolved** to quoted message text via GUID index                      |
| Attachments without text       | `cache_has_attachments`, attachment table | **Surfaced** as `[attachment: filename]` instead of silently dropped    |
| Message effects                | `expressive_send_style_id`                | **Decoded** to human-readable names (slam, loud, gentle, invisible_ink) |
| Service type                   | `service`                                 | **Flagged** when SMS instead of iMessage                                |
| Tapback reactions              | `associated_message_type`                 | **Filtered** (only `= 0` included)                                      |

## Anti-Patterns to Avoid

1. **Searching multiple chat identifiers blindly** — Always run `--stats` first to confirm the right chat identifier has messages in the expected date range
2. **Keyword search without context** — Always use `--context 5` (or more) with `--search` to understand conversational meaning around matches
3. **Repeated narrow-window SQLite queries** — Export the full date range to NDJSON first, then grep/jq the file for all subsequent analysis

**Note**: Replace `<skill-path>` with the actual installed skill path. To find it:

```bash
find ~/.claude -path "*/imessage-query/scripts/decode_attributed_body.py" 2>/dev/null
```

## Reference Documentation

- [Schema Reference](./references/schema-reference.md) — Tables, columns, relationships
- [Query Patterns](./references/query-patterns.md) — Reusable SQL templates for common operations
- [Known Pitfalls](./references/known-pitfalls.md) — Every gotcha discovered and how to handle it
- [Cross-Repo Analysis](./references/cross-repo-analysis.md) — Comparison of 5 OSS decoder implementations and what we adopted

---

## TodoWrite Task Templates

### Template A - Retrieve Conversation Thread

```
1. Identify chat_identifier for the contact (phone number or email)
2. Run decode script with --chat and appropriate date range
3. Review output for attributedBody-decoded messages (marked with [decoded])
4. If searching for specific topic, add --search flag
5. Format results as needed for the task
```

### Template B - Debug Empty Messages

```
1. Query messages where text IS NULL but attributedBody IS NOT NULL
2. Check cache_has_attachments to distinguish voice/file from dictated text
3. Run decode script to extract hidden text content
4. Verify decoded content makes sense in conversation context
5. Document any new decode patterns in known-pitfalls.md
```

### Template C - Build Sourced Timeline

```
1. Identify all relevant chat_identifiers
2. Run decode script for each contact with date range
3. Merge and sort by timestamp
4. Format as sourced quotes with timestamps for documentation
5. Verify no messages were missed (compare total count vs decoded count)
```

### Template D - Export-First Deep Analysis

```
1. Run --stats to confirm chat_identifier and date range
2. Export full date range to NDJSON: --export thread.jsonl
3. Use grep/jq on the NDJSON file for all keyword searches
4. Use --search with --context 5 for contextual understanding of specific matches
5. All subsequent analysis reads from the NDJSON file (no more SQLite queries)
```

---

## Post-Change Checklist

After modifying this skill:

1. [ ] YAML frontmatter valid (name, description with triggers)
2. [ ] No private data (phone numbers, names, emails) in any file
3. [ ] All SQL uses parameterized placeholders
4. [ ] Decode script works with `python3` (pytypedstream optional, tiers 2/3 are stdlib-only)
5. [ ] All reference links are relative paths
6. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)
