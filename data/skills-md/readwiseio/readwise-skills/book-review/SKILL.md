---
name: book-review
description: Draft a long-form book review from your Reader highlights — synthesizing the book with your broader reading history to generate original arguments
---

Draft a long-form book review from a user's Reader highlights — not just the target book,
but pulling in related highlights from their entire library to build original arguments.

The goal is a review that's more interesting than the book itself: summary + critique + original ideas,
where the original ideas come from connecting the book to everything else the user has read.

## Readwise Access

Check if Readwise MCP tools are available (e.g. `mcp__readwise__reader_list_documents`). If they are, use them throughout. If not, use the equivalent `readwise` CLI commands instead (e.g. `readwise list`, `readwise read <id>`, `readwise highlights <id>`, `readwise search <query>`). The instructions below reference MCP tool names — translate to CLI equivalents as needed.

## Setup

1. **Check for persona file.** Read `reader_persona.md` in the current working directory if it exists. Use it to understand the user's interests, reading goals, and voice — this shapes the review's framing, what connections to prioritize, and what the user is likely to care about. If no persona file exists, proceed without it and ask the user about their purpose for reading the book if it's not obvious from their highlights.

2. **Parse the argument** as a book title or search term.

```
/book-review Merchant Kings
/book-review 7 Powers
```

---

## Phase 1: Pull the Book's Highlights

### 1.1 Find the book

Search Reader for the target book:

```
mcp__readwise__reader_search_documents(query="[book title]", category_in=["epub", "pdf"])
```

If no results, broaden to all categories. If multiple matches, list them and ask the user to pick.

### 1.2 Get highlights

```
mcp__readwise__reader_get_document_highlights(document_id="[book_id]")
```

Read every highlight. Count them. If fewer than 10, warn the user — may not be enough material
for a substantive review. Ask whether to proceed or wait.

### 1.3 Get the full document details

```
mcp__readwise__reader_get_document_details(document_id="[book_id]")
```

Pull title, author, summary, cover image. You'll need these for the final output.

---

## Phase 2: Extract Claims

Process every highlight into an atomic claim. This is the step that turns
"I highlighted this paragraph" into structured, searchable research material.

For each highlight:

1. Read the highlighted text and any user note/annotation
2. Write a single present-tense declarative claim (under 10 words when possible)
3. If the user left a note, weight the claim toward what the note focused on

**Claim quality standards:**

Good claims are specific, searchable facts or assertions:
- "chimney sweeps died of scrotal cancer from coal soot"
- "Ottoman harem trained slave girls as elite bureaucrats"
- "monsoon winds enabled global maritime trade"

Bad claims are vague or generic:
- "coal mining had health consequences"
- "the author discusses Ottoman succession"
- "interesting point about slavery"

**After processing all highlights**, review the full list. Reject and rewrite any that are:
- Generic/boring ("author discusses X")
- Duplicative (two claims saying the same thing differently — consolidate)
- Vague (doesn't stand alone without reading the highlight)

Store the claims as a working list grouped by theme. This becomes your outline.

---

## Phase 3: Search the Library for Related Material

This is what makes the review more than a summary. For each major theme cluster
from Phase 2, search the user's full Reader library for related content.

### 3.1 Theme-based searches

For each theme cluster (aim for 3-6 themes):

```
mcp__readwise__reader_search_documents(query="[theme keywords]", limit=20)
```

Pull highlights from the top hits:

```
mcp__readwise__reader_get_document_highlights(document_id="[related_doc_id]")
```

You're looking for:
- **Supporting evidence** from other sources that strengthens a claim
- **Contradictions** that complicate the book's argument
- **Parallel examples** from different domains (the user read about X in biology, the book says the same about economics)
- **The user's own prior thinking** visible in their notes/annotations on related docs

### 3.2 Author search

```
mcp__readwise__reader_search_documents(query="[book author name]")
```

Check if the user has read other work by the same author. Prior context enriches the review.

### 3.3 Extract related claims

For each relevant highlight from a related document, extract a claim the same way
as Phase 2. Tag it with its source document so you can cite it properly.

**Result:** You should now have:
- The book's claims (Phase 2), grouped by theme
- Related claims from the broader library (Phase 3), mapped to those same themes
- A sense of where the user's reading supports, complicates, or extends the book

---

## Phase 4: Supplement with Web Research

Fill gaps that the user's library doesn't cover. Keep this focused — the library
research is the core, web research is supplemental.

- Search for academic sources, author interviews, other reviews
- Look for Substack writers or bloggers covering the same topic

---

## Phase 5: Write the Review

A great book review has three elements (per the ACX Book Review Contest wisdom):

1. **Summary** — Show what the book is about and why it's interesting. Without this, readers are confused.
2. **Critique** — An actual quality and agreement judgment. Without this, it isn't a review.
3. **Original ideas** — Connect the book to broader patterns from the user's reading. Without this, nobody is particularly impressed.

The original ideas come from Phase 3 — the related highlights from the user's library.
This is the whole point of the skill.

### Structure

```
[Opening: What the book is and why it matters — a specific fact or scene, not a vague hook.
Leave a %% TODO %% for the user to add how they found the book and why they read it
if context wasn't already in the document note.]

## [Thematic section 1 — informative header, not clever]

[Summarize the book's argument on this theme. Use block quotes from the book's highlights.
Then EXPAND: bring in related material from the user's other reading. This is where the
review becomes more than a summary — it's synthesis.]

> "Block quote from the book" — Author, *Book Title*

[The user also highlighted something in [Related Document] that complicates/supports this:
weave it in naturally. Cite the source with a URL link to the original source, NOT the Reader link.]

## [Thematic section 2]

[Same pattern: book's argument → user's related reading → synthesis.
Each section should advance an argument, not just list facts.]

## [Thematic section 3+]

[Keep going. Organize by theme, not by chapter. Every section should have at least
one connection to something outside the book itself.]

## What the Book Gets Wrong (or Misses)

[Honest critique. Use the user's other reading as evidence where it contradicts
or complicates the book. This is where the related-document research pays off most.]

## Further Reading

- Description with [embedded link](url) for sources worth exploring that were NOT
  linked above but are related to the core themes of this review.
```

### Voice Rules

You are drafting FOR the user, not impersonating them:

- **Don't manufacture emotion** — No "I was struck by", "I was fascinated to learn." State facts. The user adds reactions.
- **Don't manufacture personal details** — No "this reminded me of my childhood." If the user wrote something in a highlight note, reference it. Otherwise, leave a `%% TODO %%`.
- **Leave explicit gaps** — Use `%% TODO: [what the user should add] %%` for personal hooks. These signal where the user needs to fill in their own experience.
- **Honest about gaps** — "I don't know" beats hedging. If unsure, say so or leave a TODO.
- **First person** — You're writing a draft the user will edit, not a report about them.
- If a persona file exists, use it to inform which connections to prioritize and what framing the user would find natural — but still leave TODOs for personal details you're not sure about.

### Length

Err long. 2,000-10,000 words for a substantial book. The ACX contest data shows longer reviews
with genuine insight outperform shorter ones. Depth > brevity, as long as every paragraph earns
its place. If the user's highlights are sparse (10-20), aim for 1,000-2,000 instead.

### Links and Sources

- **Bookshop.org link** for the target book on first mention
- **Real URLs only** — never leave placeholder links like `(url)` or `(link)`
- When citing a related document from the user's Reader library, link to the original source URL (from document details), not the Reader URL
- Bias toward web sources that can be read in full without a paywall, like Substack or open access PDFs. Do not source from books someone would need to purchase to read.

---

## Phase 6: Quality Gate

**Separate pass. Do not skip. Do not combine with Phase 5.**

Re-read the full draft and fix every instance of:

### Banned Vocabulary

Never use these. Find concrete alternatives.

| Banned | Use instead |
|--------|-------------|
| Additionally | "Also" or restructure |
| Crucial / Pivotal / Key (adj) | Be specific about why it matters |
| Delve / Delve into | "examine", "look at", or just start |
| Enhance / Fostering | Be specific about what improved |
| Landscape (abstract) | Name the actual domain |
| Tapestry (figurative) | Name the actual pattern |
| Underscore / Highlight (verb) | State the point directly |
| Showcase | "shows", "demonstrates" |
| Vibrant / Rich (figurative) | Be specific |
| Testament / Enduring | Just state the fact |
| Groundbreaking / Renowned | Be specific about what's notable |
| Garner | "get", "earn", "attract" |
| Intricate / Intricacies | "complex" or describe the actual complexity |
| Interplay | "relationship", "tension", or describe it |
| Serves as / Stands as | Use "is" |
| Nestled / In the heart of | Just name the location |

### Banned Structures

| Pattern | Fix |
|---------|-----|
| "Not just X, it's Y" / "Not A, but B" | State Y directly |
| Rule of three ("innovation, inspiration, and insights") | Use the number of items the content needs |
| "-ing" analysis ("highlighting the importance of...") | State the importance directly |
| "From X to Y" (false ranges) | List the actual items |
| Synonym cycling (protagonist/hero/central figure) | Pick one term, reuse it |
| "Despite challenges, the future looks bright" | State the actual situation |
| "Exciting times lie ahead" | End with a specific fact |
| "X wasn't Y. It was Z." (dramatic reveal) | Collapse to single positive statement |
| "The detail that stopped me in my tracks" | Start with the fact |
| "genuinely revolutionary" | Use a specific descriptor |
| Any melodramatic one-liner meant to sound profound | Delete it |
| "I'd forgotten I knew" | Delete. Never frame knowledge as rediscovered. |

### Checklist

- [ ] **6a. Grep the draft for every banned word/pattern above.** Fix every match.
- [ ] **6b. Check links** — every source has a real URL. No placeholders.
- [ ] **6c. Check em dash density** — max 2-3 per section. Convert excess to commas, colons, periods.
- [ ] **6d. Check word repetition** — any word appearing 3+ times in a paragraph. Vary or reduce.
- [ ] **6e. Read the opening paragraph.** Does it sound like a person or like an AI summarizing a book? If the latter, rewrite.
- [ ] **6f. Verify every section connects to material beyond the book itself.** If a section is pure summary with no synthesis, add related-library connections or cut it.

---

## Phase 7: Publish to Reader

Create the review as a new document in Reader:

```
mcp__readwise__reader_create_document(
  url="https://reader-review.internal/[slug]-[ISO-timestamp]",
  title="[book title] — Review Draft",
  author="Ghostreader",
  category="article",
  summary="Review draft based on [N] highlights from [Book Title] and [M] related documents",
  html="[converted HTML of the review]",
  notes="DRAFT for editing. Based on highlights from: [list source document titles]"
)
```

Return the document URL to the user.

---

## What Makes This Different from a Summary

The whole point of Phase 3 (library search) is that the review should contain ideas
the author of the book never had. The user's reading history is a unique lens:

- They read a book about Roman logistics AND a book about supply chain management →
  the review connects them in a way neither book does alone
- They highlighted a contradicting claim in a different source →
  the review challenges the book with evidence the user already found compelling
- They left a note on a highlight in an unrelated article that turns out to be relevant →
  the review surfaces a connection the user may not have consciously made

This is how you get "original ideas" — the third element that separates a competent
review from an impressive one. The user's library IS the original thinking.

---

## Error Handling

- **Book not found in Reader**: Report search terms tried, ask for correct title or document ID.
- **Fewer than 10 highlights**: Warn — may not be enough. Ask whether to proceed.
- **No related documents found**: Proceed with book-only review but warn that it'll be more summary-heavy. Lean harder on web research.
- **Reader create fails**: The draft text is already generated — output it as markdown so the user can save it manually.
- **Any unexpected failure**: Say what failed, what's already done, where partial output is.
