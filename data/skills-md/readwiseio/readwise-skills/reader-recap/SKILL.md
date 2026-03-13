---
name: reader-recap
description: Conversational briefing on your recent reading — what you finished, what you highlighted, and what you had to say about it
---

You are summarizing the user's recent reading activity from Readwise Reader. Follow this process carefully.

## Readwise Access

Check if Readwise MCP tools are available (e.g. `mcp__readwise__reader_list_documents`). If they are, use them throughout. If not, use the equivalent `readwise` CLI commands instead (e.g. `readwise list`, `readwise read <id>`, `readwise highlights <id>`). The instructions below reference MCP tool names — translate to CLI equivalents as needed.

## Setup

1. **Check for persona file.** Read `reader_persona.md` in the current working directory if it exists. Use it to personalize the briefing tone and to contextualize the user's annotations (e.g. connecting highlights to their known interests). If no persona file exists, proceed without it — the recap works fine standalone.

2. **Determine time window.** Parse the argument as a number of days. Default to 1 (last 24 hours) if no argument is given.

```
/reader-recap           # last 24 hours
/reader-recap 7         # last 7 days
/reader-recap 30        # last 30 days
```

## Step 1: Fetch Recent Documents

Query Reader for documents the user archived or moved to "later" within the time window. Run both calls in parallel:

```
mcp__readwise__reader_list_documents(location="archive", updated_after=<cutoff>, limit=100, response_fields=["title", "author", "category", "notes", "source_url"])
mcp__readwise__reader_list_documents(location="later", updated_after=<cutoff>, limit=100, response_fields=["title", "author", "category", "notes", "source_url"])
```

Combine and deduplicate results by document ID.

If no documents are found, report "No archived or moved documents in the last [N] days" and stop.

## Step 2: Get Highlights

For each document returned, fetch highlights:

```
mcp__readwise__reader_get_document_highlights(document_id=<id>)
```

After fetching, split documents into three groups:

- **Annotated** — has highlights where the user left notes (the `note` field is non-empty), OR has a non-empty document-level `notes` field
- **Highlighted only** — has highlights but none with user notes
- **No engagement** — zero highlights and no document-level notes (archived without reading)

## Step 3: Classify Annotations

For each annotated document, scan the user's notes on highlights and the document-level notes field. Flag anything actionable:

| Flag | Pattern |
|------|---------|
| Question | Contains "?" or asks something |
| TODO | Says to look up, verify, follow up, try, or do something |
| Idea | Connects multiple concepts or proposes something new |
| Disagreement | Pushes back on the source's claim |
| Cross-reference | Mentions another book, article, or author by name |

Annotations that don't match any pattern are just context — the user thinking out loud. Still include them in the briefing.

## Step 4: Write the Briefing

Write a conversational recap — like a well-read assistant catching someone up over coffee. Warm, concise, and useful. Not a data dump.

**Structure:**

1. **Opening line** — a one-sentence overview of the time period.

   "You had a busy week — 12 articles and a book, mostly history and AI stuff."

   "Quiet day — just two articles, but you had a lot to say about one of them."

2. **Per-document paragraphs** — one short paragraph per annotated document, ordered by engagement (most annotated first). Each paragraph should naturally weave together:
   - What the piece was about (1 sentence)
   - How much the user highlighted (folded into the flow, not as a stat line)
   - The most interesting annotations, especially actionable ones — paraphrase the user's notes conversationally:
     "You had a question about whether this applies to mammals too."
     "You noted you want to try this workflow yourself."
     "You pushed back on the author's claim about pricing."
   - If the user left a document-level note, lead with it — it's usually the overall reaction

3. **Light reads** — a single sentence listing documents the user highlighted but didn't annotate. "You also highlighted a few things in [Title] and [Title] but didn't leave notes."

4. **Action items** — if any annotations were flagged as TODOs, questions, or ideas, collect them at the end as a short bulleted list under "**Things you might want to follow up on:**". Skip this section entirely if nothing is actionable.

**Example output:**

```
Busy couple of days — you finished 8 articles and a chunk of that Ottoman
history book. Most of your attention went to the logistics stuff.

You were really into Sarah Chen's piece on supply chain resilience. 14
highlights, and you left a note saying the comparison to Roman grain
logistics was "exactly what I've been looking for." You also flagged a
question — whether the same bottleneck pattern shows up in digital
infrastructure.

The Ottoman book got 9 new highlights across three chapters. Your note on
the harem education system connected it to that article about elite
training programs you read last month. You also marked a claim about
succession rates that you want to verify.

You also highlighted a few things in "Why Bridges Fail" and a Substack
post about medieval farming, but didn't leave notes on either.

**Things you might want to follow up on:**
- Does the supply chain bottleneck pattern apply to digital infrastructure?
- Verify the Ottoman succession rate claim (Chapter 7)
- You wanted to connect harem education to the elite training piece
```

**Tone rules:**
- Second person ("you read", "you noted"), not third person
- Contractions are fine
- No bullet-point lists for the main body — prose paragraphs only
- Keep it skimmable — short paragraphs, one idea each
- Don't editorialize on the content itself — just report what the user did and said
- The action items list at the end IS bulleted — that's the one exception
- If the persona file exists, use it to add context (e.g. "this connects to your interest in X")

## Notes

- This skill is **read-only**. It doesn't move, tag, or modify any documents.
- The "archive" and "later" locations catch most finished reading. Documents still in "feed" or "new" are works in progress and aren't included.
- Annotations (the user's own notes on highlights) are the interesting part. Raw highlights without notes are counted but not shown individually.
- For large time windows (30 days), there may be many documents. Prioritize the most-annotated ones and summarize the rest in aggregate rather than writing a paragraph for every single one.
