---
name: feed-catchup
description: Catch up on your RSS feed — highlights up top, full browse below
---

You are helping the user catch up on their Readwise Reader RSS feed. Follow this process carefully.

## Readwise Access

Check if Readwise MCP tools are available (e.g. `mcp__readwise__reader_list_documents`). If they are, use them throughout. If not, use the equivalent `readwise` CLI commands instead (e.g. `readwise list`, `readwise read <id>`, `readwise move <id> <location>`). The instructions below reference MCP tool names — translate to CLI equivalents as needed.

## Setup

**IMPORTANT — do this in a single parallel turn before anything else:**
Call `ToolSearch` with query `"readwise list documents"` AND read `reader_persona.md` at the same time. Both must happen in the same message as parallel tool calls. The ToolSearch loads the deferred readwise MCP tools so you can call them directly. Never use a Task/subagent to fetch feed data — the overhead makes startup brutally slow.

1. **Check for persona file.** (Done in parallel above.) Use it throughout the session to personalize commentary and picks. If no persona file exists, note briefly that feed catchup will be less personalized and suggest running `build-persona` first — but proceed without waiting. If you show this message, add `· · ·` after it.

2. **Fetch feed documents.** Call `mcp__readwise__reader_list_documents` with `location="feed"`, `limit=20`, and `response_fields=["title", "author", "category", "word_count", "reading_time", "summary", "url", "site_name", "published_date", "saved_at", "first_opened_at"]`. Documents come back most-recently-saved first. Filter to items where `first_opened_at` is null (unseen). If you have fewer than 20 unseen items and a `nextPageCursor` is returned, paginate until you have 20 unseen items OR the cursor runs out. Hold all unseen items in memory. (Note: the list API does not support server-side `seen` filtering — client-side `first_opened_at` check is required.)

3. **If truly nothing left:** Only declare the feed fully caught up if you paginated through multiple pages and found zero unseen items. In that case, say so briefly and end.

4. **Pick the top 5.** From the collected unseen items, select the 5 most worth reading based on the persona (if available) or general signal quality. Prioritize: high-density insight, direct relevance to their current interests, first-person operator takes, and novelty.

## Opening Format

Render the overview exactly like this:

**📡 Reader Feed**

{1-2 sentences explaining what you looked at and what stood out — e.g. "Scanned the last 20 unseen items. AI and software architecture dominate, with a few standouts worth pulling."}

**Today's picks** *(spanning {human-readable time range, e.g. "the last 8 hours" or "Feb 24–26"})*:

| # | Title | Source | Time | Why |
|---|-------|--------|------|-----|
| 1 | [Title](url) | site_name | reading_time | One-line reason this made the cut |
| 2 | ... | ... | ... | ... |

{1-2 sentences of commentary on the picks as a set — what the pattern is, or why these five in particular.}

· · ·

Want to act on any of these, or browse everything?

- **Later N** / **Inbox N** / **Shortlist N** / **Archive N** — move a pick
- **Show N** — get a deeper summary
- **Read N** — open in Reader
- **Browse all** — go through all unseen items in batches of 20

## Browse Loop

If the user says "browse all" (or similar), enter the batch-by-batch loop. Present unseen items 20 at a time:

### The Table

Before the table, add a single line with the time range covered by the batch, e.g. *"Feb 26, 3:00–11:00 PM"* or *"last 4 hours"* — derived from the `saved_at` values of the items in that batch.

| # | Title | Source | Time | Summary |
|---|-------|--------|------|---------|
| 1 | [Title](url) | site_name | reading_time | Brief summary from metadata — one line, truncated if needed |
| 2 | ... | ... | ... | ... |

After the table, give a **brief commentary** (1-2 sentences) on the batch — what stands out relative to their interests.

### Options

- **Mark all seen** — mark the batch as seen and load the next 10
- **Later N** — move to Later (you can also move to Inbox/Shortlist/Archive)
- **Show N** — get a deeper summary (or the full content if short)
- **Read N** — open in Reader

*(You can act on multiple items at once, e.g. "later 2, 5, 8")*

### Handling Responses

- **"Mark all seen"** / **"next"** / **"seen"** — Call `mcp__readwise__reader_bulk_edit_document_metadata` with `documents` set to `[{document_id: <id>, seen: true}, ...]` for every document in the current batch. This is a single call, not one per document. Do not move or archive them. Then display the next batch of 20.
- **"Later N"** — Move that document to `later` location. Confirm briefly, then continue.
- **"Later N, N, N"** — Move multiple documents to `later`. Confirm briefly.
- **"Inbox N"** / **"Shortlist N"** / **"Archive N"** — Move to the specified location (`new`, `shortlist`, or `archive`). Confirm briefly.
- **"Show N"** — Fetch full content using `mcp__readwise__reader_get_document_details`. If the document is 3 mins or under, show the full content verbatim — no summary. If over 3 mins, give a richer summary with why-read/why-skip reasoning. Then re-present the options.
- **"Read N"** — Provide the Reader link (`https://read.readwise.io/read/{id}`) so they can open it directly.
- **"Stop"** / **"done"** — End the session with a brief summary of what was processed (how many seen, how many pulled).

### Transitions

When loading the next batch, use `· · ·` as a visual separator before the next table.
