---
name: claudemem
description: >
  Persistent memory that survives across conversations. Automatically remembers important context
  (API specs, decisions, quirks, preferences) and saves session summaries. Searches past knowledge
  before starting new tasks. Responds naturally to phrases like "remember this", "what do you know
  about...", "save this session", or "what did we do last time". All local, zero network.
---

# claudemem — Your Persistent Memory

Memory that carries across conversations. Automatically captures important knowledge during work
and saves structured session summaries when you're done. Searches past context before new tasks.

## Slash Commands

- **/wrap-up** — End-of-session save: extracts ALL important knowledge + saves session summary in one step. Deduplicates automatically.
- **/save-session** — Save only the session summary (without extracting notes)
- **/recall [topic]** — Search persistent memory for a topic, or show recent activity

## Natural Trigger Phrases

These natural phrases also activate memory operations:

**To save knowledge:**
- "remember this" / "save this" / "note this down" / "keep this in mind"

**To search memory:**
- "what do you remember about..." / "do you recall..." / "what do we know about..."

**To wrap up (save everything):**
- "wrap up" / "let's wrap up" / "save everything" — triggers /wrap-up (notes + session)
- "save this session" / "summarize what we did" — triggers /save-session (session only)

**To recall past work:**
- "what did we do last time" / "show me recent sessions" / "what happened with [topic]"

## Setup

Before first use, verify the CLI is installed. If `claudemem` is not found on PATH, install it:

```bash
curl -fsSL https://raw.githubusercontent.com/zelinewang/claudemem/main/skills/claudemem/scripts/install.sh | bash
```

Or run the bundled installer:

```bash
bash "SKILL_DIR/scripts/install.sh"
```

After installation, verify with `claudemem --version`.

## Commands

```bash
# Notes (knowledge fragments)
claudemem note add <category> --title "..." --content "..." --tags "tag1,tag2"
claudemem note search "query" [--in category] [--tag tags]
claudemem note list [category]
claudemem note get <id>
claudemem note update <id> --content "..." [--title "..."] [--tags "..."]
claudemem note append <id> "additional content"
claudemem note delete <id>
claudemem note categories
claudemem note tags

# Sessions (conversation summaries)
claudemem session save --title "..." --branch "..." --project "..." --session-id "..." --content "..."
claudemem session list [--last N] [--date today] [--date-range 7d] [--branch X]
claudemem session search "query" [--branch X]
claudemem session get <id>

# Unified search (across notes AND sessions)
claudemem search "query" [--type note|session] [--limit N]

# Statistics
claudemem stats

# Configuration
claudemem config set/get/list/delete <key> [value]

# Data portability
claudemem export [output-file]              # Backup as tar.gz
claudemem import <archive-file>             # Restore from backup (auto-reindexes)

# Data integrity
claudemem verify                            # Check DB-file consistency
claudemem repair                            # Fix orphaned entries
```

Add `--format json` to any command for structured output.

## Autonomous Behavior

### Recommended: Auto Wrap-Up Before Session Ends

If the user has enabled auto wrap-up in their CLAUDE.md, automatically execute /wrap-up before the conversation ends:
1. Extract unsaved knowledge fragments → save as notes (with dedup)
2. Generate session summary → save as session
3. Show brief report of what was saved

### Auto-Save Notes (Silent + Brief Indicator)

Automatically capture knowledge **without asking** during normal conversation. After saving,
add a brief indicator at the end of your response so the user knows what was captured:

```
[📝 Saved: "TikTok Rate Limits" → api-specs]
```

**What to auto-save** (proactive, no user prompt needed):
* API specs, field mappings, rate limits, endpoint details
* Technical decisions with rationale (why X over Y)
* Integration quirks, gotchas, workarounds
* Resolved bugs and their root causes
* Configuration requirements, thresholds, defaults
* User preferences and project conventions
* Important URLs, endpoints, environment configs
* Domain terminology, aliases, abbreviations
* External context shared by the user (specs, docs, requirements)
* Business requirements, use cases, user stories
* System constraints, assumptions, exclusions

**How to auto-save gracefully:**
1. Identify the knowledge fragment during your normal response
2. Choose an appropriate category (create new if none fits)
3. Before saving, quickly search to avoid duplicates: `claudemem note search "keyword" --format json`
4. If related note exists: `claudemem note append <id> "new info"` instead of creating duplicate
5. Save: `claudemem note add <category> --title "..." --content "..." --tags "..."`
6. Show the indicator: `[📝 Saved: "<title>" → <category>]`

**Do NOT auto-save:**
* Temporary debugging output or transient state
* File paths or code snippets without context
* General programming knowledge available in docs
* Information the user is likely to change immediately

### Auto-Search Before Tasks (Silent)

Search memory at the start of tasks that might benefit from prior context:
* Before implementing a feature in a domain previously discussed
* When working with an API or system previously documented
* Before making architectural decisions

Search silently. If relevant results found, mention them briefly:
```
[🔍 Found related memory: "TikTok Rate Limits" — rate limit is 100/min]
```

### Save Sessions (On Request via /save-session or Natural Phrase)

Session summaries are saved when the user explicitly asks — via `/save-session` command
or natural phrases like "save this session" or "wrap up". Do NOT auto-save sessions
without the user's request, as they may want to continue the conversation.

### Workflow Rules

1. **Before saving**: search existing content first — update or append if related note exists
2. **Before working**: search for relevant context that may inform the current task
3. **Merge related information** under existing categories/titles when possible
4. **Preserve existing content** unless contradicted by new information
5. **Focus on evergreen knowledge**, not transient conversation artifacts

## Session Summary Template

When saving a session, generate content following this structure. Include ALL sections —
these enable daily/weekly/monthly reporting for personal review and team updates.

```markdown
## Summary
One or two paragraphs describing what was accomplished.

## Purpose & Goals
- Why this work was done
- What problem it solves

## Key Decisions
- Decision 1 with rationale
- Decision 2 with rationale

## What Changed
- `path/to/file.py` — Description of change

## Achievements & Impact
- What was delivered (quantify where possible: lines of code, tests passing, performance gains)
- Significance of the work (e.g., "unblocked 3 downstream features", "reduced query time from 2s to 10ms")

## Problems & Solutions
- **Problem**: Description of issue
  **Solution**: How it was resolved

## Questions Raised
- Open question needing future attention

## Next Steps
- [ ] First follow-up task
- [ ] Second follow-up task
```

Sessions always include: `--project` (which codebase), `--branch` (which feature), `--tags` (for filtering).
This enables reviewing by: `claudemem session list --date today` (daily), `--date-range 7d` (weekly), `--date-range 30d` (monthly).

## What NOT to Capture

* Temporary debugging sessions or transient state
* File paths or code snippets without context
* General programming knowledge available in docs
* Meta-commentary about the conversation itself
* Information that changes frequently without lasting value

## Data Portability

All data stored at `~/.claudemem/` as plain Markdown files with YAML frontmatter.
SQLite FTS5 index is a rebuildable cache — only the Markdown files matter.

**Backup**: `claudemem export backup.tar.gz`
**Restore**: `claudemem import backup.tar.gz` (auto-rebuilds search index)

## Storage

`~/.claudemem/` — Plain text Markdown files organized by type (notes/ and sessions/).
FTS5 SQLite index for sub-10ms full-text search. File permissions: 0600/0700.
