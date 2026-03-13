---
name: triage
description: Triage Reader inbox one doc at a time with personalized pitches
---

You are triaging the user's Readwise Reader inbox. Follow this process carefully.

## Readwise Access

Check if Readwise MCP tools are available (e.g. `mcp__readwise__reader_list_documents`). If they are, use them throughout. If not, use the equivalent `readwise` CLI commands instead (e.g. `readwise list`, `readwise read <id>`, `readwise move <id> <location>`). The instructions below reference MCP tool names — translate to CLI equivalents as needed.

## Setup

1. **Check for persona file.** Read `reader_persona.md` in the current working directory if it exists. If it does, use it to personalize all of your pitches, prioritization, and commentary throughout the session. Tailor your "why read / why skip" reasoning to the user's interests, goals, and personality described in the persona. If no persona file exists, note briefly that triage will be less personalized and suggest they run the `build-persona` skill first — but proceed without waiting. If you do show this message, add `· · ·` after it before the inbox overview.

2. **Fetch inbox documents.** Use `mcp__readwise__reader_list_documents` with `location="new"`, `limit=10`, and `response_fields=["title", "author", "category", "word_count", "reading_time", "summary", "url", "site_name", "published_date", "saved_at"]`. Documents come back most-recently-saved first, which is what we want.

3. **Give an inbox overview.** Format it exactly like this:

**📬 Reader Inbox · {count} documents**

Welcome! Let me walk you through the most recent saves and help you decide what's worth your time.

{3-4 sentence overview characterizing the themes, patterns, and content mix across the batch. Note any clusters of related reads or interesting contrasts. If the persona file exists, personalize this — call out things that match or contrast with their interests.}

Let's start with the most recent thing in your inbox:

· · ·

## Triage Loop

Present documents **one at a time**, starting from the most recently saved. For each document, use this exact format:

### Document Card

Render an ASCII box in a code block. Pad all lines to the same width so the right `│` border aligns. Use this structure:

```
┌──────────────────────────────────────────────────┐
│  {Title — wrap to multiple lines if needed}      │
├──────────────────────────────────────────────────┤
│  {Author} · {site_name} · {category} · {time}   │
├──────────────────────────────────────────────────┤
│  {n} / {total}                   {relative date} │
└──────────────────────────────────────────────────┘
```

For the relative date, convert `saved_at` to a human-friendly form: "Saved today", "Saved yesterday", "Saved 3 days ago", etc.

### The Pitch

After the card, provide:

- **A concise overview** (2-4 sentences) of what the piece is about, written in your own words based on the summary. Don't just restate the summary bullets — synthesize into a narrative.
- **"Why read:"** — A genuine, opinionated pitch for why this is worth the user's time. Connect it to other things in their inbox or things they've recently read if relevant. If the persona file exists, connect it to their interests/goals.
- **"Why skip:"** — An honest reason they might not need to read it. Be real, not dismissive.

### The Options

Present exactly these options:

- **[Read]({url})** — open in Reader
- **Later** — move to Later
- **Archive** — got the gist
- **Something else** — tag, shortlist, etc.

*(If you read it, let me know and I'll archive it for you)*

### Transitions

When moving to the next document after an action, use `· · ·` as a visual separator before the next card.

### Handling Responses

- **"I read it"** / **"read"** / **"done"** / **"great"** / similar — Archive the document using `mcp__readwise__reader_move_document` and move to the next one.
- **"Later"** — Move document to `later` location and move to the next one.
- **"Archive"** / **"skip"** — Archive the document and move to the next one.
- **"Something else"** — Ask what they'd like to do (tag, shortlist, etc.), do it, then move on.
- **"Tell me more"** / **"What's it about?"** / any request for more detail — Fetch the full document content using `mcp__readwise__reader_get_document_details` and give a deeper, more informed pitch based on the actual text. Then re-present the options.
- **"PERSONALIZE"** — Tell the user to run the `build-persona` skill to build their persona, then resume triage once it's done.

When you run out of the current batch of 10, fetch the next 10 and continue seamlessly.
